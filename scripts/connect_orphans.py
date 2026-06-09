#!/usr/bin/env python3
"""
Targeted edge-finding for orphan / under-connected entities — the "additions"
feedback loop.

The first extraction pass over a document sometimes leaves entities stranded:
a concept gets named but never linked, an alias ("amstaff") never gets tied to
its canonical entity ("American Staffordshire Terrier"), a recurring term ("dcm")
floats free. This pass hunts those orphans and runs a SECOND, targeted
extraction that asks the model one focused question per source document:

    "Here is the document. Here are the entities already in the graph from it.
     These specific ones are disconnected. What edges connect them — to each
     other or to the connected ones? Evidence required."

Far cheaper than re-extracting everything: one call per document that has
orphans, scoped to connecting known entities (not discovering new ones).

Edges are added with evidence (see Graph.add_edge), validated against the
ontology, and only between entities that already exist in the graph.

Usage:
    # local Ollama (default):
    python scripts/connect_orphans.py --ontology examples/good-dog-corpus/ontology.yaml
    # remote backend (set the same env as ingest):
    SECONDBRAIN_API_KEY=... SECOND_BRAIN_PRIVACY_MODE=hybrid \
    REMOTE_API_BASE=https://api.example.com REMOTE_MODEL=google/gemma-4-31B-it \
    python scripts/connect_orphans.py --ontology examples/good-dog-corpus/ontology.yaml --workers 8
"""

import argparse
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from second_brain.graph import Graph
from second_brain.ontology_yaml import load_ontology
from second_brain.extract import (
    DEFAULT_HOST,
    DEFAULT_MODEL,
    _parse_json_response,
    generate_entity_id,
)
import json
import os
import urllib.request


def _connect_prompt(text, edge_types, orphan_labels, candidate_labels):
    return f"""You are connecting entities already extracted from a document.

The entities below are DISCONNECTED — they appear in the graph but have no
relationships. Find edges that link each disconnected entity to OTHER entities
in the list (or to each other), using ONLY relationships actually supported by
the text. Common cases: an alias linked to its canonical name (alias_of), a
term that is the subject of a publication (subject_of), an org a person belongs
to (member_of/affiliated_with).

Edge types (use ONLY these): {", ".join(edge_types)}

DISCONNECTED entities to connect:
{chr(10).join("  - " + label for label in orphan_labels)}

ALL entities available as endpoints (use these exact labels):
{chr(10).join("  - " + label for label in candidate_labels)}

Respond ONLY with valid JSON (no markdown):
{{
  "edges": [
    {{"source": "exact label", "target": "exact label", "type": "EDGE_TYPE",
      "evidence": "verbatim quote from the text", "confidence": 0.6}}
  ]
}}

Only emit an edge if the text supports it. Empty list if nothing connects.

Document text:
---
{text[:6000]}
---

JSON response:"""


def _call_llm(prompt, model, host, api_base, api_key, timeout=120):
    if api_base and api_key:
        url = api_base.rstrip("/")
        url += "/chat/completions" if url.endswith("/v1") else "/v1/chat/completions"
        body = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 2048,
        }
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        req = urllib.request.Request(
            url, data=json.dumps(body).encode(), headers=headers, method="POST"
        )
        r = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
        ch = r.get("choices") or []
        return _parse_json_response((ch[0]["message"].get("content", "") if ch else "").strip())
    else:
        body = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 2048},
        }
        req = urllib.request.Request(
            f"{host}/api/generate",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        r = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
        return _parse_json_response(r.get("response", "").strip())


def main():
    ap = argparse.ArgumentParser(description="Connect orphan entities via targeted re-extraction")
    ap.add_argument("--ontology", "-o", default=None)
    ap.add_argument("--workers", "-w", type=int, default=1)
    ap.add_argument(
        "--max-degree",
        type=int,
        default=0,
        help="Treat entities with degree <= this as needing connection (0 = strict orphans)",
    )
    ap.add_argument("--dry-run", action="store_true", help="Find + propose edges but don't write")
    args = ap.parse_args()

    onto = load_ontology(args.ontology)
    edge_types = sorted(onto.EDGE_TYPES)
    graph = Graph(ontology=onto)

    # backend (same env contract as extract.Extractor)
    mode = os.environ.get("SECOND_BRAIN_PRIVACY_MODE", "") or "local"
    api_base = os.environ.get("REMOTE_API_BASE", "")
    api_key = os.environ.get("SECONDBRAIN_API_KEY", "")
    if mode in ("hybrid", "remote") and api_base and api_key:
        model = os.environ.get("REMOTE_MODEL", "")
        host = ""
        print(f"Backend: remote {model} @ {api_base}")
    else:
        api_base = api_key = ""
        model = getattr(
            __import__("second_brain.config", fromlist=["x"]),
            "LOCAL_EXTRACTION_MODEL",
            DEFAULT_MODEL,
        )
        host = DEFAULT_HOST
        print(f"Backend: local Ollama {model}")

    try:
        # Find orphans/under-connected and group by source document.
        rows = graph.query(f"""
            MATCH (e:Entity)
            OPTIONAL MATCH (e)-[r:RELATES_TO]-()
            WITH e, count(r) AS d WHERE d <= {args.max_degree}
            RETURN e.id AS id, e.label AS label, e.source_url AS src
        """)
        orphans_by_doc = defaultdict(list)
        for row in rows:
            orphans_by_doc[row["src"] or ""].append((row["id"], row["label"]))
        # All entities per doc = candidate endpoints.
        all_rows = graph.query(
            "MATCH (e:Entity) RETURN e.id AS id, e.label AS label, e.source_url AS src"
        )
        cand_by_doc = defaultdict(list)
        label_to_id = {}
        for row in all_rows:
            cand_by_doc[row["src"] or ""].append(row["label"])
            label_to_id[row["label"]] = row["id"]

        docs = [d for d in orphans_by_doc if d and Path(d).exists()]
        print(
            f"Orphans (degree <= {args.max_degree}): {sum(len(v) for v in orphans_by_doc.values())} "
            f"across {len(docs)} readable documents\n"
        )

        def _find(doc):
            # Fail-soft per document: a slow/failed call must not abort the
            # whole pool (pool.map raises on the first exception otherwise).
            try:
                text = Path(doc).read_text(errors="ignore")
                orphan_labels = [label for _, label in orphans_by_doc[doc]]
                candidates = cand_by_doc[doc]
                prompt = _connect_prompt(text, edge_types, orphan_labels, candidates)
                return doc, _call_llm(prompt, model, host, api_base, api_key, timeout=180)
            except Exception as ex:
                return doc, {"edges": [], "_error": str(ex)}

        if args.workers > 1:
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                results = list(pool.map(_find, docs))
        else:
            results = [_find(d) for d in docs]

        # Write phase (main thread — single writer).
        added = 0
        proposed = 0
        failures = 0
        for doc, out in results:
            if out.get("_error"):
                failures += 1
                print(f"  ⚠ {Path(doc).name}: {out['_error']}")
                continue
            for e in out.get("edges", []):
                src_id = label_to_id.get(e.get("source", "")) or generate_entity_id(
                    e.get("source", "")
                )
                tgt_id = label_to_id.get(e.get("target", "")) or generate_entity_id(
                    e.get("target", "")
                )
                etype = e.get("type", "")
                if not src_id or not tgt_id or src_id == tgt_id:
                    continue
                if not onto.validate_edge_type(etype):
                    continue
                proposed += 1
                print(f"  + {e.get('source')} -[{etype}]-> {e.get('target')}")
                if not args.dry_run:
                    if graph.add_edge(
                        src_id,
                        tgt_id,
                        etype,
                        confidence=float(e.get("confidence", 0.6)),
                        evidence=e.get("evidence", ""),
                        provenance="orphan_connect",
                    ):
                        added += 1

        print(f"\n{'='*50}")
        print(f"  Proposed: {proposed}  |  Added: {added}  |  doc failures: {failures}")
        if args.dry_run:
            print("  (dry-run — nothing written)")
        else:
            print(f"  Total edges now: {graph.edge_count()}")
    finally:
        graph.close()


if __name__ == "__main__":
    main()
