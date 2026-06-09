#!/usr/bin/env python3
"""
Ingest notes from an Obsidian vault into the knowledge graph.
Parses wikilinks, frontmatter, tags. Runs three-phase extraction.
Idempotent — only processes new or modified notes.
"""

import sys
import time
import argparse

sys.path.insert(0, ".")

from second_brain.graph import Graph
from second_brain.extract import Extractor
from second_brain.embed import embed_text
from second_brain.ontology import slugify
from second_brain.obsidian import scan_vault
from second_brain.pipeline.resolve import canonicalize_extracted_graph
from second_brain import config


def _entity_document_mentions(entities: list[dict]) -> list[dict]:
    mentions = []
    for entity in entities:
        doc_ids = entity.get("doc_ids") or ([entity.get("doc_id")] if entity.get("doc_id") else [])
        for doc_id in doc_ids:
            mentions.append(
                {
                    "entity_id": entity["id"],
                    "doc_id": doc_id,
                    "confidence": entity.get("confidence", 0.8),
                    "source_url": entity.get("source_url", ""),
                    "provenance": entity.get("provenance", "document_mention"),
                }
            )
    return mentions


def main():
    parser = argparse.ArgumentParser(description="Ingest Obsidian vault")
    parser.add_argument("--vault", "-v", default=config.VAULT_PATH, help="Path to Obsidian vault")
    parser.add_argument(
        "--force", "-f", action="store_true", help="Re-ingest all notes (ignore existing)"
    )
    parser.add_argument(
        "--ontology",
        "-o",
        default=None,
        help="Path to a YAML ontology (default: built-in SecondBrainOntology)",
    )
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=1,
        help="Parallel extraction workers. 1 (default) is right "
        "for local Ollama (it serializes on one GPU); use "
        "8-16 for a remote OpenAI-compatible backend.",
    )
    args = parser.parse_args()

    if not args.vault:
        print("No vault path configured.")
        print("Set VAULT_PATH in second_brain/config.py or use --vault")
        return

    print(f"Scanning vault: {args.vault}")
    notes = scan_vault(args.vault)
    print(f"Found {len(notes)} notes.\n")

    if not notes:
        return

    from second_brain.ontology_yaml import load_ontology

    ontology = load_ontology(args.ontology)
    if args.ontology:
        print(
            f"Ontology: {args.ontology} "
            f"({len(ontology.NODE_TYPES)} node types, {len(ontology.EDGE_TYPES)} edge types)"
        )
    else:
        print("Ontology: built-in SecondBrainOntology (default)")
    graph = Graph(ontology=ontology)
    try:
        extractor = Extractor(ontology)

        # Check which notes are already ingested
        if not args.force:
            existing = set()
            for doc in graph.query("MATCH (d:Document) RETURN d.id AS id"):
                existing.add(doc["id"])
            new_notes = [n for n in notes if n["doc_id"] not in existing]
            if len(new_notes) < len(notes):
                print(f"Skipping {len(notes) - len(new_notes)} already-ingested notes.")
            notes = new_notes

        if not notes:
            print("All notes already ingested. Use --force to re-ingest.")
            return

        all_entities = []
        all_edges = []
        t_start = time.time()
        extract_failures = 0  # extractions that errored (e.g. backend timeout)

        # --- Phase 1: extraction (parallelizable) -------------------------
        # extract_from_text is pure (HTTP + parsing, no DB writes), so it's
        # safe to run concurrently. This is a big win for REMOTE backends
        # (OpenAI-compatible APIs serve concurrent requests, and the bottleneck
        # is per-call latency, not local CPU). Local Ollama serializes on one
        # GPU, so --workers>1 mainly helps the remote path. DB writes happen in
        # Phase 2 on the main thread only (LadybugDB is single-writer).
        def _extract(note):
            return note, extractor.extract_from_text(
                note["body"], source_url=note["path"], doc_id=note["doc_id"]
            )

        workers = max(1, args.workers)
        if workers > 1:
            from concurrent.futures import ThreadPoolExecutor

            print(f"Extracting {len(notes)} notes with {workers} parallel workers...")
            with ThreadPoolExecutor(max_workers=workers) as pool:
                extracted = list(pool.map(_extract, notes))
        else:
            extracted = [_extract(n) for n in notes]

        # --- Phase 2: register docs + assemble (main thread, DB-touching) --
        for i, (note, result) in enumerate(extracted, 1):
            print(f"[{i}/{len(notes)}] {note['relative_path']}")

            # Register document
            graph.add_document(note["doc_id"], note["path"], note["title"])

            if result.get("_error"):
                extract_failures += 1
                print(f"  ⚠ extraction FAILED: {result['_error']}")
            print(
                f"  Extracted: {len(result['entities'])} entities, " f"{len(result['edges'])} edges"
            )

            # Store wikilinks as ASSOCIATED_WITH edges between linked notes
            # (links are note-title → note-title, resolved by label match)
            if note["wikilinks"]:
                print(f"  Wikilinks: {len(note['wikilinks'])}")
                for link_target in note["wikilinks"]:
                    # Create a concept entity for the linked note if not yet extracted
                    link_id = f"wikilink_{__import__('hashlib').sha256(link_target.encode()).hexdigest()[:16]}"
                    result["entities"].append(
                        {
                            "id": link_id,
                            "entity_type": "concept",
                            "label": link_target,
                            "description": f"Linked note: [[{link_target}]]",
                            "confidence": 0.8,
                            "source_url": note["path"],
                            "doc_id": note["doc_id"],
                            "provenance": "obsidian_wikilink",
                        }
                    )
                    # Edge from this note's doc to the linked concept
                    result["edges"].append(
                        {
                            "source_id": note["doc_id"],
                            "target_id": link_id,
                            "edge_type": "ASSOCIATED_WITH",
                            "confidence": 0.9,
                            "source_url": note["path"],
                            "provenance": "obsidian_wikilink",
                        }
                    )

            # Add tags as entities
            for tag in note["tags"]:
                tag_entity = {
                    "id": f"tag_{slugify(tag)}",
                    "entity_type": "concept",
                    "label": tag,
                    "description": f"Tag: #{tag}",
                    "confidence": 0.8,
                    "source_url": note["path"],
                    "doc_id": note["doc_id"],
                    "provenance": "obsidian_tag",
                }
                result["entities"].append(tag_entity)

            all_entities.extend(result["entities"])
            all_edges.extend(result["edges"])

        # Resolve aliases before writing so tags/wikilinks/LLM labels converge
        # onto one canonical entity ID in this ingest batch.
        all_entities, all_edges, resolution = canonicalize_extracted_graph(all_entities, all_edges)
        if resolution.merged_count:
            print(f"Resolved entity aliases: {resolution.merged_count} labels folded.")

        # Deduplicate entities across notes — same ID from different notes
        # should keep the highest-confidence version
        seen = {}
        for e in all_entities:
            eid = e["id"]
            if eid not in seen or e.get("confidence", 0) > seen[eid].get("confidence", 0):
                seen[eid] = e
        all_entities = list(seen.values())

        # Bulk load entities
        if all_entities:
            print(f"\nBulk loading {len(all_entities)} entities (after dedup)...")
            loaded = graph.bulk_add_entities(all_entities)
            print(f"  Loaded: {loaded}")

            mentions = _entity_document_mentions(all_entities)
            mentioned = graph.bulk_add_mentions(mentions)
            print(f"  Document mentions: {mentioned}")

            # Embed entity descriptions
            print("Computing entity embeddings...")
            for entity in all_entities:
                embed_str = f"{entity['label']}: {entity.get('description', '')}"
                try:
                    emb = embed_text(embed_str)
                    graph.set_embedding(entity["id"], emb)
                except Exception as e:
                    print(f"  Embedding failed for {entity['label']}: {e}")

        if all_edges:
            print(f"Loading {len(all_edges)} edges...")
            loaded = graph.bulk_add_edges(all_edges)
            print(f"  Loaded: {loaded}")

        # Rebuild HNSW vector indexes after bulk embedding
        print("Rebuilding vector indexes...")
        graph.rebuild_vector_indexes()

        # Summary
        elapsed = time.time() - t_start
        edge_count = graph.edge_count()
        print(f"\n{'=' * 50}")
        # Don't claim success if extraction silently failed. A 0-edge graph
        # with extraction failures means the LLM backend was unreachable /
        # timing out (e.g. Ollama saturated) — NOT that the corpus had no
        # relationships. Surface it loudly so the operator re-runs rather
        # than shipping a hollow graph.
        if extract_failures and edge_count == 0:
            print(
                f"⚠  INGEST DEGRADED — {extract_failures}/{len(notes)} extractions "
                f"failed and the graph has 0 edges."
            )
            print(
                f"   The extraction backend (Ollama @ {getattr(extractor,'host','?')}) "
                f"likely timed out or was unreachable."
            )
            print(
                "   Documents + entities were stored, but NO relationships were "
                "extracted. Re-run when the backend is responsive."
            )
        else:
            print(f"Ingestion complete in {elapsed:.1f}s.")
            if extract_failures:
                print(f"  ⚠ {extract_failures}/{len(notes)} extractions failed " f"(partial graph)")
        print(f"  Notes processed:     {len(notes)}")
        print(f"  Total entities:      {graph.entity_count()}")
        print(f"  Total edges:         {edge_count}")
        print(f"  Total documents:     {graph.document_count()}")
        print("\nNext steps:")
        print("  Search:    python scripts/search_cli.py -q 'your query'")
        print("  Analyze:   python scripts/run_analysis.py")
        print("  Reflect:   python scripts/daily_briefing.py")

        # Ontology rejections (optional — not all ontology types track these)
        rejections = (
            ontology.get_rejection_counts() if hasattr(ontology, "get_rejection_counts") else {}
        )
        if rejections:
            print("\nOntology rejections:")
            for type_name, count in list(rejections.items())[:10]:
                print(f"  {type_name}: {count}")
            print("  Tip: Consider adding frequently rejected types to ONTOLOGY.md")
    finally:
        graph.close()


if __name__ == "__main__":
    main()
