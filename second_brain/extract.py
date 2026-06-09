"""
Triplet extraction from text — entity-relationship-entity with evidence.

Uses LLM (Ollama) to extract triplets from note chunks.
Evidence is REQUIRED on every edge — verbatim quote from source text.

Returns:
    {
        "entities": [{"label": "...", "type": "...", "meta": {...}}, ...],
        "edges": [{"source": "...", "target": "...", "type": "...", "evidence": "...", "confidence": 0.5}, ...]
    }
"""

import json
import logging
import os
import urllib.request
from typing import Any

from second_brain.models import ExtractionResult

logger = logging.getLogger(__name__)

# Default extraction model. NOTE: a 14B model makes local ingestion crawl;
# the Extractor class overrides this with config.LOCAL_EXTRACTION_MODEL
# (llama3.2:3b). Kept here only as the bare-function fallback.
DEFAULT_MODEL = "qwen3:14b"
DEFAULT_HOST = "http://localhost:11434"
# Per-call extraction timeout. Bumped 60→120 (a 60s cap silently dropped
# every call on a contended/cold backend → 0-edge graphs). Override via
# SECOND_BRAIN_EXTRACT_TIMEOUT.
TIMEOUT_SECONDS = int(os.environ.get("SECOND_BRAIN_EXTRACT_TIMEOUT", "120"))


DEFAULT_NODE_TYPES = [
    "concept",
    "person",
    "source",
    "project",
    "insight",
    "question",
    "practice",
    "place",
    "method",
    "tool",
]


def _build_extraction_prompt(
    text: str,
    edge_types: list[str],
    node_types: list[str],
) -> str:
    """The triplet-extraction prompt, shared by the local (Ollama) and remote
    (OpenAI-compatible) backends so both ask for exactly the same thing."""
    return f"""Extract entities and the relationships (triplets) between them from the text below.

LABEL RULES (important):
- A label is the entity's natural surface form EXACTLY as it appears in the text
  — e.g. "FDA", "German Shepherd", "grain-free diet", "Dr. Lisa Freeman".
- Do NOT invent ids, slugs, snake_case keys, or prefixes (NOT "org_us_fda",
  NOT "concept_dcm"). Use the human-readable name as written.
- List every entity you reference. Every edge `source`/`target` MUST be the
  label of an entity in your `entities` list.

For each relationship return: source label, target label, edge type
(one of: {", ".join(edge_types)}), a verbatim evidence quote from the text
(min 10 characters), and confidence (0.9 deterministic / 0.7 NLP / 0.5 LLM).

Entity types (use these exact lowercase values): {", ".join(node_types)}

Respond ONLY with valid JSON (no markdown, no explanation):
{{
  "entities": [
    {{"label": "German Shepherd", "type": "breed", "meta": {{}}}},
    {{"label": "dilated cardiomyopathy", "type": "concept", "meta": {{}}}},
    {{"label": "2019 FDA DCM status report", "type": "event", "meta": {{}}}}
  ],
  "edges": [
    {{
      "source": "German Shepherd",
      "target": "American Kennel Club",
      "type": "{(edge_types[0] if edge_types else "mentions")}",
      "evidence": "exact quote from text",
      "confidence": 0.5
    }}
  ]
}}

Text to analyze:
---
{text[:4000]}
---

JSON response:"""


def extract_triplets_from_text(
    text: str,
    edge_types: list[str],
    model: str = DEFAULT_MODEL,
    host: str = DEFAULT_HOST,
    max_tokens: int = 3072,
    node_types: list[str] | None = None,
) -> dict[str, Any]:
    """
    Extract triplets from a text chunk using Ollama LLM.

    Args:
        text: the note chunk text to analyze
        edge_types: list of edge types to extract (from config)
        model: Ollama model name
        host: Ollama host URL
        max_tokens: max tokens for LLM response

    Returns:
        dict with "entities" and "edges" lists
    """
    if not text or len(text.strip()) < 20:
        return {"entities": [], "edges": []}

    node_types = node_types or DEFAULT_NODE_TYPES

    prompt = _build_extraction_prompt(text, edge_types, node_types)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        # Disable reasoning models' chain-of-thought (e.g. qwen3): extraction
        # wants structured JSON, not CoT (which burns the token budget and can
        # return empty content). Non-thinking models ignore this field.
        "think": False,
        "options": {
            "temperature": 0.1,
            "num_predict": max_tokens,
        },
    }

    try:
        req = urllib.request.Request(
            f"{host}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            response_text = result.get("response", "").strip()

        # Parse JSON, then validate through the canonical Pydantic template.
        # from_raw is fail-soft: schema-invalid entities/edges are dropped and
        # logged rather than poisoning the batch. to_legacy_dict preserves the
        # {entities, edges} dict contract this function's callers expect.
        raw = _parse_json_response(response_text)
        return ExtractionResult.from_raw(raw).to_legacy_dict()

    except Exception as ex:
        # Surface the failure instead of masking it. A silent empty return
        # on timeout/connection-error makes a degraded backend (e.g. Ollama
        # saturated by other workloads) produce a 0-edge graph that still
        # reports "ingestion complete" — indistinguishable from "the text
        # genuinely had no relationships." The "_error" key lets callers
        # count failures and refuse to declare success on a starved run.
        # 2026-05-28: an 85-min ingest produced 142 entities / 0 edges
        # because every extraction call timed out and was silently dropped.
        logger.warning("extract_triplets failed (model=%s): %s", model, ex)
        return {"entities": [], "edges": [], "_error": str(ex)}


def extract_triplets_openai(
    text: str,
    edge_types: list[str],
    model: str,
    api_base: str,
    api_key: str,
    max_tokens: int = 2048,
    node_types: list[str] | None = None,
    timeout: int = TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Extract triplets via an OpenAI-compatible /v1/chat/completions endpoint.

    Backend-agnostic: works with any OpenAI-compatible server ([vendor],
    Together, Groq, vLLM, a local OpenAI-shim, etc.). Selected when
    PRIVACY_MODE is "hybrid"/"remote" and a remote base is configured — the
    extraction (not embedding) leaves the machine. Same prompt and same
    fail-loud `_error` contract as the local path.
    """
    if not text or len(text.strip()) < 20:
        return {"entities": [], "edges": []}

    node_types = node_types or DEFAULT_NODE_TYPES
    prompt = _build_extraction_prompt(text, edge_types, node_types)

    base = api_base.rstrip("/")
    # Accept either a bare host ("https://api.example.ai") or one that already
    # includes the /v1 prefix.
    url = base + ("/chat/completions" if base.endswith("/v1") else "/v1/chat/completions")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": max_tokens,
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        # OpenAI-compatible: choices[0].message.content holds the model output.
        choices = result.get("choices") or []
        content = (choices[0].get("message", {}).get("content", "") if choices else "").strip()
        raw = _parse_json_response(content)
        return ExtractionResult.from_raw(raw).to_legacy_dict()
    except Exception as ex:
        # Same fail-loud contract as the local path: surface the error so the
        # ingest refuses to declare success on a degraded/unauthorized backend.
        logger.warning("extract_triplets_openai failed (model=%s, base=%s): %s", model, base, ex)
        return {"entities": [], "edges": [], "_error": str(ex)}


def instructor_available() -> bool:
    """True iff the optional `instructor` extra (and openai SDK) are importable.

    Kept as a function (not an import-time flag) so the core stays import-clean:
    nothing pulls in instructor/openai unless this is called.
    """
    try:
        import instructor  # noqa: F401
        import openai  # noqa: F401

        return True
    except ImportError:
        return False


def extract_triplets_instructor(
    text: str,
    node_types: list[str],
    edge_types: list[str],
    model: str,
    base_url: str,
    api_key: str = "ollama",
    timeout: int = TIMEOUT_SECONDS,
    max_retries: int = 2,
) -> dict[str, Any]:
    """Extract triplets via Instructor — structured output validated against the
    `ExtractionResult` schema, with automatic retry-on-validation-error.

    Opt-in only (`pip install 'open-second-brain[instructor]'`, then enable via
    config/env). Works against any OpenAI-compatible endpoint, including Ollama's
    `/v1` surface (`base_url="http://localhost:11434/v1"`, `api_key="ollama"`).
    Unlike the urllib paths, Instructor drives the JSON schema from the model
    itself, so there is no hand-written JSON shape in the prompt and no
    `_parse_json_response` repair step — that is the whole point of taking the
    dependency. Same fail-loud `_error` contract as the urllib backends.
    """
    try:
        import instructor
        from openai import OpenAI
    except ImportError as ex:
        raise RuntimeError(
            "Instructor backend requested but not installed. "
            "Install with: pip install 'open-second-brain[instructor]'"
        ) from ex

    if not text or len(text.strip()) < 20:
        return {"entities": [], "edges": []}

    client = instructor.from_openai(
        OpenAI(base_url=base_url, api_key=api_key or "ollama", timeout=timeout),
        mode=instructor.Mode.JSON,
    )
    # Schema comes from ExtractionResult; the prompt only needs the task + the
    # allowed vocabulary (so the model picks valid types) and the text.
    prompt = (
        "Extract entities and the typed relationships between them from the "
        "text below.\n"
        f"Allowed entity types: {', '.join(node_types)}\n"
        f"Allowed edge types: {', '.join(edge_types)}\n"
        "Every edge needs a verbatim evidence quote from the text.\n\n"
        f"Text:\n---\n{text[:4000]}\n---"
    )
    try:
        result: ExtractionResult = client.chat.completions.create(
            model=model,
            response_model=ExtractionResult,
            max_retries=max_retries,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}],
        )
        return result.to_legacy_dict()
    except Exception as ex:
        logger.warning(
            "extract_triplets_instructor failed (model=%s, base=%s): %s",
            model,
            base_url,
            ex,
        )
        return {"entities": [], "edges": [], "_error": str(ex)}


def _parse_json_response(response_text: str) -> dict[str, Any]:
    """
    Parse JSON from LLM response, handling trailing prose or malformed JSON.

    Strategy:
    1. Try raw JSON parse
    2. Strip markdown code blocks if present
    3. Find first { and last } and try again
    4. Fall back to empty result
    """
    if not response_text:
        return {"entities": [], "edges": []}

    # Try direct parse
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # Strip markdown code blocks
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:])  # Remove first line (```json)
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Find JSON bounds
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(cleaned[first_brace : last_brace + 1])
        except json.JSONDecodeError:
            pass

    # Failed to parse
    print(f"[extract_triplets] Failed to parse JSON response: {cleaned[:200]}...")
    return {"entities": [], "edges": []}


def extract_triplets_batch(
    texts: list[str],
    edge_types: list[str],
    model: str = DEFAULT_MODEL,
    host: str = DEFAULT_HOST,
) -> list[dict[str, Any]]:
    """
    Extract triplets from multiple texts in sequence.

    For parallel extraction, run this function concurrently with thread pool.
    Ollama handles concurrency via its internal thread management.
    """
    results = []
    for text in texts:
        result = extract_triplets_from_text(text, edge_types, model, host)
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Extractor — compatibility class over the functional API.
#
# The kg-common ontology refactor moved extraction to module-level functions
# (extract_triplets_from_text), but ingest_obsidian.py, ingest_folder.py, and
# mcp_server.py still import an `Extractor` class + `generate_entity_id`. This
# class restores that interface: it wraps the functional API and does the
# label→id resolution and field enrichment the callsites expect (the functional
# API returns label-keyed entities/edges; callsites want id-resolved rows with
# source_url / provenance / entity_type / edge_type).
# ---------------------------------------------------------------------------


def generate_entity_id(label: str) -> str:
    """Stable entity id from a label (slug-based, matches ontology.slugify)."""
    from second_brain.ontology import slugify

    return slugify(label)


class Extractor:
    """Thin wrapper: ontology-aware triplet extraction returning id-resolved rows."""

    def __init__(self, ontology, model: str | None = None, host: str | None = None):
        self.ontology = ontology
        try:
            from second_brain import config
        except Exception:
            config = None

        def _cfg(name, default=""):
            return getattr(config, name, default) if config else default

        # Backend selection mirrors config.PRIVACY_MODE:
        #   "local"  -> Ollama (default; nothing leaves the machine)
        #   "hybrid" -> embeddings local, EXTRACTION via remote OpenAI-compatible API
        #   "remote" -> everything remote
        # Each knob is env-overridable so a remote run needs no committed secret
        # or URL. SECONDBRAIN_API_KEY is read from the environment only.
        mode = os.environ.get("SECOND_BRAIN_PRIVACY_MODE") or _cfg("PRIVACY_MODE", "local")
        remote_base = os.environ.get("REMOTE_API_BASE") or _cfg("REMOTE_API_BASE", "")
        remote_model = os.environ.get("REMOTE_MODEL") or _cfg("REMOTE_MODEL", "")
        api_key = os.environ.get("SECONDBRAIN_API_KEY", "")

        if mode in ("hybrid", "remote") and remote_base and api_key:
            self.backend = "openai"
            self.remote_base = remote_base
            self.remote_model = model or remote_model
            self.api_key = api_key
            self.model = self.remote_model
            self.host = remote_base
        else:
            # Local Ollama. Default to LOCAL_EXTRACTION_MODEL (llama3.2:3b — fast),
            # NOT extract.py's DEFAULT_MODEL (qwen3:14b, which crawls). Caller can override.
            self.backend = "ollama"
            self.model = (
                model
                or os.environ.get("SECOND_BRAIN_LOCAL_MODEL")
                or _cfg("LOCAL_EXTRACTION_MODEL", DEFAULT_MODEL)
                or DEFAULT_MODEL
            )
            # SECOND_BRAIN_EXTRACT_HOST lets extraction target a different
            # Ollama than embeddings (which use the ollama client's OLLAMA_HOST).
            # This decouples a big extraction model on a GPU box from a light
            # embedding model elsewhere, avoiding single-GPU VRAM contention.
            self.host = (
                host
                or os.environ.get("SECOND_BRAIN_EXTRACT_HOST")
                or os.environ.get("OLLAMA_HOST")
                or _cfg("OLLAMA_HOST", DEFAULT_HOST)
                or DEFAULT_HOST
            )

        # Type vocabulary to constrain the LLM — pulled from the ontology so a
        # custom ontology actually drives extraction (entity types AND edges).
        self.edge_types = sorted(getattr(ontology, "EDGE_TYPES", []) or [])
        self.node_types = sorted(getattr(ontology, "NODE_TYPES", []) or [])

        # Optional Instructor backend — schema-validated structured output with
        # retry-on-validation-error. Off by default: the core ships no
        # instructor/openai SDK. Enable with SECOND_BRAIN_USE_INSTRUCTOR=1 (or
        # config.USE_INSTRUCTOR) AND `pip install 'open-second-brain[instructor]'`.
        want_instructor = str(
            os.environ.get("SECOND_BRAIN_USE_INSTRUCTOR") or _cfg("USE_INSTRUCTOR", "")
        ).strip().lower() in ("1", "true", "yes", "on")
        self.use_instructor = want_instructor and instructor_available()
        if want_instructor and not self.use_instructor:
            logger.warning(
                "USE_INSTRUCTOR is set but the 'instructor' extra is not "
                "installed — falling back to the urllib backend. Install with: "
                "pip install 'open-second-brain[instructor]'"
            )
        # OpenAI-compatible base for the instructor client (Ollama exposes /v1).
        if self.backend == "openai":
            base = self.remote_base.rstrip("/")
            self._instructor_base = base if base.endswith("/v1") else base + "/v1"
            self._instructor_key = self.api_key
        else:
            self._instructor_base = self.host.rstrip("/") + "/v1"
            self._instructor_key = "ollama"

    def extract_from_text(
        self,
        text: str,
        source_url: str = "",
        doc_id: str | None = None,
    ) -> dict[str, Any]:
        """Extract entities + edges from text, id-resolved and enriched.

        Returns {"entities": [...], "edges": [...]} where each entity has
        id / entity_type / label / description / confidence / source_url /
        provenance, and each edge has source_id / target_id / edge_type /
        evidence / confidence / source_url. Edge endpoints are resolved from
        the LLM's label references to entity ids; edges whose endpoints don't
        resolve are dropped (fail-soft).
        """
        if self.use_instructor:
            raw = extract_triplets_instructor(
                text,
                self.node_types,
                self.edge_types,
                model=self.model,
                base_url=self._instructor_base,
                api_key=self._instructor_key,
            )
        elif self.backend == "openai":
            raw = extract_triplets_openai(
                text,
                self.edge_types,
                model=self.remote_model,
                api_base=self.remote_base,
                api_key=self.api_key,
                node_types=self.node_types or None,
            )
        else:
            raw = extract_triplets_from_text(
                text,
                self.edge_types,
                model=self.model,
                host=self.host,
                node_types=self.node_types or None,
            )

        # Canonicalize LLM-produced type strings to the ontology's declared
        # casing. LLMs vary ("authored_by" vs "AUTHORED_BY", "Publication" vs
        # "publication"); map case-insensitively so a YAML ontology (lowercase)
        # and the default SecondBrainOntology (UPPER_SNAKE) both validate.
        # Unknown types pass through unchanged for the graph to reject.
        _node_canon = {nt.lower(): nt for nt in self.node_types}
        _edge_canon = {et.lower(): et for et in self.edge_types}

        def _canon_node(t):
            return _node_canon.get((t or "").lower(), t or "concept")

        def _canon_edge(t):
            t = t or "ASSOCIATED_WITH"
            return _edge_canon.get(t.lower(), t)

        label_to_id: dict[str, str] = {}
        entities: list[dict[str, Any]] = []
        for ent in raw.get("entities", []):
            label = (ent.get("label") or "").strip()
            if not label:
                continue
            eid = generate_entity_id(label)
            label_to_id[label] = eid
            entities.append(
                {
                    "id": eid,
                    "entity_type": _canon_node(ent.get("type")),
                    "label": label,
                    "description": (ent.get("meta") or {}).get("description", ""),
                    "confidence": float(ent.get("confidence", 0.5)),
                    "source_url": source_url,
                    "doc_id": doc_id or "",
                    "provenance": "llm_extraction",
                }
            )

        edges: list[dict[str, Any]] = []
        for edge in raw.get("edges", []):
            src_label = (edge.get("source") or "").strip()
            tgt_label = (edge.get("target") or "").strip()
            src_id = label_to_id.get(src_label) or (
                generate_entity_id(src_label) if src_label else None
            )
            tgt_id = label_to_id.get(tgt_label) or (
                generate_entity_id(tgt_label) if tgt_label else None
            )
            if not src_id or not tgt_id:
                continue
            edges.append(
                {
                    "source_id": src_id,
                    "target_id": tgt_id,
                    "edge_type": _canon_edge(edge.get("type")),
                    "evidence": edge.get("evidence", ""),
                    "confidence": float(edge.get("confidence", 0.5)),
                    "source_url": source_url,
                }
            )

        out = {"entities": entities, "edges": edges}
        if raw.get("_error"):
            out["_error"] = raw["_error"]  # propagate backend failure to caller
        return out
