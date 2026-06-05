#!/usr/bin/env python3
"""
Incremental enrichment script for open-second-brain.

Schedule: runs every 4 hours via systemd timer.
Manual use:
    python scripts/enrich.py --vault /path/to/vault

This script is deliberately graph-only for now. The older DuckDB-hybrid
version used stale GraphWriter/ChunkStore APIs and different DB paths
(brain.ldb / chunks.duckdb). Until the DuckDB substrate is wired into core
ingest, this enrichment pass writes only to the current LadybugDB Graph API.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from second_brain import config
from second_brain.embed import embed_text
from second_brain.extract import Extractor
from second_brain.graph import Graph
from second_brain.obsidian import scan_vault
from second_brain.ontology_yaml import load_ontology


DATA_DIR = config.GRAPH_DIR.parent
LAST_RUN_FILE = DATA_DIR / "enrichment_last_run.txt"
ENRICHMENT_LOG = DATA_DIR / "enrichment.log"


def log(msg: str) -> None:
    """Log to enrichment.log with timestamp."""
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    ENRICHMENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(ENRICHMENT_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {msg}\n")
    print(f"[enrich] {msg}")


def get_last_run_time(path: Path = LAST_RUN_FILE) -> datetime:
    """Get timestamp of last successful enrichment run."""
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return datetime.fromisoformat(f.read().strip())
    return datetime(1970, 1, 1, tzinfo=timezone.utc)


def set_last_run_time(ts: datetime, path: Path = LAST_RUN_FILE) -> None:
    """Update last run timestamp."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(ts.isoformat())


def select_recent_notes(vault_path: str, since: datetime) -> list[dict]:
    """Return notes whose source file mtime is newer than since."""
    notes = []
    for note in scan_vault(vault_path):
        mtime = datetime.fromtimestamp(Path(note["path"]).stat().st_mtime, tz=timezone.utc)
        if mtime > since:
            notes.append(note)
    return notes


def _wikilink_entity_id(label: str) -> str:
    digest = hashlib.sha256(label.encode()).hexdigest()[:16]
    return f"wikilink_{digest}"


def _add_obsidian_entities(note: dict, result: dict, ontology) -> None:
    """Add deterministic entities/edges derived from Obsidian metadata."""
    for tag in note["tags"]:
        result["entities"].append({
            "id": f"tag_{tag}",
            "entity_type": "concept",
            "label": tag,
            "description": f"Tag: #{tag}",
            "confidence": 0.8,
            "source_url": note["path"],
            "provenance": "obsidian_tag",
        })

    if not ontology.validate_edge_type("ASSOCIATED_WITH"):
        return

    for link_target in note["wikilinks"]:
        link_id = _wikilink_entity_id(link_target)
        result["entities"].append({
            "id": link_id,
            "entity_type": "concept",
            "label": link_target,
            "description": f"Linked note: [[{link_target}]]",
            "confidence": 0.8,
            "source_url": note["path"],
            "provenance": "obsidian_wikilink",
        })
        result["edges"].append({
            "source_id": note["doc_id"],
            "target_id": link_id,
            "edge_type": "ASSOCIATED_WITH",
            "confidence": 0.9,
            "source_url": note["path"],
            "provenance": "obsidian_wikilink",
        })


def enrich_note(note: dict, graph: Graph, extractor: Extractor, ontology, embed: bool) -> dict[str, int]:
    """Extract entities/edges from one note and write through Graph API."""
    result = extractor.extract_from_text(
        note["body"], source_url=note["path"], doc_id=note["doc_id"]
    )
    _add_obsidian_entities(note, result, ontology)

    graph.add_document(note["doc_id"], note["path"], note["title"])

    stats = {
        "entities_seen": len(result["entities"]),
        "entities_written": 0,
        "edges_seen": len(result["edges"]),
        "edges_written": 0,
        "embedding_failures": 0,
        "extract_failures": 1 if result.get("_error") else 0,
    }

    seen_entities = {}
    for entity in result["entities"]:
        eid = entity["id"]
        if eid not in seen_entities or entity.get("confidence", 0) > seen_entities[eid].get("confidence", 0):
            seen_entities[eid] = entity

    for entity in seen_entities.values():
        written = graph.add_entity(
            entity["id"],
            entity["entity_type"],
            entity["label"],
            description=entity.get("description", ""),
            confidence=entity.get("confidence", 0.5),
            source_url=entity.get("source_url", note["path"]),
            provenance=entity.get("provenance", "llm_extraction"),
        )
        if written:
            stats["entities_written"] += 1

        if embed and written:
            try:
                emb_text = f"{entity['label']}: {entity.get('description', '')}"
                graph.set_embedding(entity["id"], embed_text(emb_text))
            except Exception:
                stats["embedding_failures"] += 1

    for edge in result["edges"]:
        written = graph.add_edge(
            edge["source_id"],
            edge["target_id"],
            edge["edge_type"],
            confidence=edge.get("confidence", 0.5),
            evidence=edge.get("evidence", ""),
            source_url=edge.get("source_url", note["path"]),
            provenance=edge.get("provenance", "llm_extraction"),
        )
        if written:
            stats["edges_written"] += 1

    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Incrementally enrich an Obsidian vault")
    parser.add_argument("--vault", "-v", default=config.VAULT_PATH, help="Path to Obsidian vault")
    parser.add_argument("--ontology", "-o", default=None, help="YAML ontology path")
    parser.add_argument("--graph", default=str(config.GRAPH_DIR), help="Graph DB path")
    parser.add_argument("--last-run-file", default=str(LAST_RUN_FILE), help="Last-run marker path")
    parser.add_argument("--limit", type=int, default=None, help="Limit notes processed (smoke tests)")
    parser.add_argument("--force", action="store_true", help="Process all notes regardless of last-run marker")
    parser.add_argument("--dry-run", action="store_true", help="Scan and extract, but do not write graph")
    parser.add_argument("--embed", action="store_true", help="Embed new/updated entities during enrichment")
    args = parser.parse_args()

    if not args.vault:
        log("No vault path configured. Set VAULT_PATH or pass --vault.")
        return 2

    start = datetime.now(timezone.utc)
    last_run_file = Path(args.last_run_file)
    since = datetime(1970, 1, 1, tzinfo=timezone.utc) if args.force else get_last_run_time(last_run_file)

    log("=== Starting enrichment pass ===")
    log(f"Vault: {args.vault}")
    log(f"Processing notes modified since {since.isoformat()}")

    notes = select_recent_notes(args.vault, since)
    if args.limit is not None:
        notes = notes[:args.limit]
    log(f"Found {len(notes)} notes to process")

    if not notes:
        set_last_run_time(start, last_run_file)
        log("No new notes to process")
        return 0

    ontology = load_ontology(args.ontology)
    extractor = Extractor(ontology)

    totals = {
        "entities_seen": 0,
        "entities_written": 0,
        "edges_seen": 0,
        "edges_written": 0,
        "embedding_failures": 0,
        "extract_failures": 0,
        "errors": 0,
    }

    graph = None
    try:
        if not args.dry_run:
            graph = Graph(graph_dir=Path(args.graph), ontology=ontology)

        for i, note in enumerate(notes, 1):
            try:
                if args.dry_run:
                    result = extractor.extract_from_text(note["body"], source_url=note["path"], doc_id=note["doc_id"])
                    stats = {
                        "entities_seen": len(result["entities"]),
                        "entities_written": 0,
                        "edges_seen": len(result["edges"]),
                        "edges_written": 0,
                        "embedding_failures": 0,
                        "extract_failures": 1 if result.get("_error") else 0,
                    }
                else:
                    stats = enrich_note(note, graph, extractor, ontology, args.embed)
                for key, value in stats.items():
                    totals[key] += value
                log(
                    f"  [{i}/{len(notes)}] {note['relative_path']}: "
                    f"{stats['entities_written']}/{stats['entities_seen']} entities, "
                    f"{stats['edges_written']}/{stats['edges_seen']} edges"
                )
            except Exception as ex:
                totals["errors"] += 1
                log(f"  [{i}/{len(notes)}] {note['relative_path']}: ERROR {ex}")

        if graph is not None:
            graph.flush()
        set_last_run_time(start, last_run_file)
    finally:
        if graph is not None:
            graph.close()

    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    log(
        "=== Enrichment complete: "
        f"{totals['entities_written']}/{totals['entities_seen']} entities, "
        f"{totals['edges_written']}/{totals['edges_seen']} edges, "
        f"{totals['extract_failures']} extraction failures, "
        f"{totals['errors']} errors in {elapsed:.1f}s ==="
    )

    return 1 if totals["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
