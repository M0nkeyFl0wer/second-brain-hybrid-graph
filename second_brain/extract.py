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
    "concept", "person", "source", "project", "insight",
    "question", "practice", "place", "method", "tool",
]


def _build_extraction_prompt(
    text: str, edge_types: list[str], node_types: list[str],
) -> str:
    """The triplet-extraction prompt, shared by the local (Ollama) and remote
    (OpenAI-compatible) backends so both ask for exactly the same thing."""
    return f"""Extract triplets (subject, relationship, object) from the following text.

For each relationship found, return:
- source entity label
- target entity label
- edge type (one of: {", ".join(edge_types)})
- verbatim evidence quote from the text (min 10 characters)
- confidence: 0.9 deterministic / 0.7 NLP / 0.5 LLM

Entity types: {", ".join(node_types)}

Respond ONLY with valid JSON (no markdown, no explanation):
{{
  "entities": [
    {{"label": "entity name", "type": "entity_type", "meta": {{}}}}
  ],
  "edges": [
    {{
      "source": "source entity label",
      "target": "target entity label",
      "type": "EDGE_TYPE",
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
    max_tokens: int = 2048,
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

        # Parse JSON from response
        return _parse_json_response(response_text)

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
        return _parse_json_response(content)
    except Exception as ex:
        # Same fail-loud contract as the local path: surface the error so the
        # ingest refuses to declare success on a degraded/unauthorized backend.
        logger.warning("extract_triplets_openai failed (model=%s, base=%s): %s",
                       model, base, ex)
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
            return json.loads(cleaned[first_brace:last_brace + 1])
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
            self.model = model or _cfg("LOCAL_EXTRACTION_MODEL", DEFAULT_MODEL) or DEFAULT_MODEL
            self.host = host or _cfg("OLLAMA_HOST", DEFAULT_HOST) or DEFAULT_HOST

        # Type vocabulary to constrain the LLM — pulled from the ontology so a
        # custom ontology actually drives extraction (entity types AND edges).
        self.edge_types = sorted(getattr(ontology, "EDGE_TYPES", []) or [])
        self.node_types = sorted(getattr(ontology, "NODE_TYPES", []) or [])

    def extract_from_text(
        self, text: str, source_url: str = "", doc_id: str | None = None,
    ) -> dict[str, Any]:
        """Extract entities + edges from text, id-resolved and enriched.

        Returns {"entities": [...], "edges": [...]} where each entity has
        id / entity_type / label / description / confidence / source_url /
        provenance, and each edge has source_id / target_id / edge_type /
        evidence / confidence / source_url. Edge endpoints are resolved from
        the LLM's label references to entity ids; edges whose endpoints don't
        resolve are dropped (fail-soft).
        """
        if self.backend == "openai":
            raw = extract_triplets_openai(
                text, self.edge_types, model=self.remote_model,
                api_base=self.remote_base, api_key=self.api_key,
                node_types=self.node_types or None,
            )
        else:
            raw = extract_triplets_from_text(
                text, self.edge_types, model=self.model, host=self.host,
                node_types=self.node_types or None,
            )

        label_to_id: dict[str, str] = {}
        entities: list[dict[str, Any]] = []
        for ent in raw.get("entities", []):
            label = (ent.get("label") or "").strip()
            if not label:
                continue
            eid = generate_entity_id(label)
            label_to_id[label] = eid
            entities.append({
                "id": eid,
                "entity_type": ent.get("type") or "concept",
                "label": label,
                "description": (ent.get("meta") or {}).get("description", ""),
                "confidence": float(ent.get("confidence", 0.5)),
                "source_url": source_url,
                "provenance": "llm_extraction",
            })

        edges: list[dict[str, Any]] = []
        for edge in raw.get("edges", []):
            src_label = (edge.get("source") or "").strip()
            tgt_label = (edge.get("target") or "").strip()
            src_id = label_to_id.get(src_label) or (
                generate_entity_id(src_label) if src_label else None)
            tgt_id = label_to_id.get(tgt_label) or (
                generate_entity_id(tgt_label) if tgt_label else None)
            if not src_id or not tgt_id:
                continue
            edges.append({
                "source_id": src_id,
                "target_id": tgt_id,
                "edge_type": edge.get("type") or "ASSOCIATED_WITH",
                "evidence": edge.get("evidence", ""),
                "confidence": float(edge.get("confidence", 0.5)),
                "source_url": source_url,
            })

        out = {"entities": entities, "edges": edges}
        if raw.get("_error"):
            out["_error"] = raw["_error"]   # propagate backend failure to caller
        return out