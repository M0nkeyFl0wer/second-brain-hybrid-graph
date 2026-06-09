#!/usr/bin/env python3
"""Dry-run junk-entity pruning audit.

This tool never mutates the graph. Pruning happens by reconstructing a filtered
graph copy and swapping it in after verification — a deliberately conservative
path for irreversible bulk mutation. (In-place bulk DELETE was unsafe on the
older `real_ladybug` build this stack started on; it tests clean on the current
ladybug 0.17.1 — see `scripts/repro_bulk_delete.py` — but reconstruct-and-swap
stays the default because a verified-then-swapped copy is recoverable and an
in-place delete is not.)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from second_brain import config
from second_brain.graph import Graph
from second_brain.pipeline.resolve import _is_unlinked_junk_entity


def _query_or_empty(graph: Graph, query: str) -> list[dict]:
    try:
        return graph.query(query)
    except Exception:
        return []


def load_graph_rows(graph_dir: Path) -> tuple[list[dict], list[dict], list[dict]]:
    graph = Graph(graph_dir, read_only=True)
    try:
        entities = graph.query(
            """
            MATCH (e:Entity)
            RETURN e.id AS id, e.label AS label, e.entity_type AS entity_type,
                   e.confidence AS confidence, e.source_url AS source_url,
                   e.provenance AS provenance, e.description AS description,
                   e.created_at AS created_at, e.updated_at AS updated_at,
                   e.embedding AS embedding, e.layer AS layer
            """
        )
        documents = graph.query(
            """
            MATCH (d:Document)
            RETURN d.id AS id, d.path AS path, d.title AS title,
                   d.ingested_at AS ingested_at, d.chunk_count AS chunk_count
            """
        )
        rel_edges = graph.query(
            """
            MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
            RETURN a.id AS source_id, b.id AS target_id, r.edge_type AS edge_type,
                   r.weight AS weight, r.confidence AS confidence,
                   r.evidence AS evidence, r.source_url AS source_url,
                   r.provenance AS provenance, r.created_at AS created_at,
                   r.expired_at AS expired_at, 'RELATES_TO' AS rel_table
            """
        )
        mention_edges = _query_or_empty(
            graph,
            """
            MATCH (e:Entity)-[r:MENTIONED_IN]->(d:Document)
            RETURN e.id AS source_id, d.id AS target_id, r.edge_type AS edge_type,
                   r.weight AS weight, r.confidence AS confidence,
                   r.evidence AS evidence, r.source_url AS source_url,
                   r.provenance AS provenance, r.created_at AS created_at,
                   r.expired_at AS expired_at, 'MENTIONED_IN' AS rel_table
            """,
        )
        connects_edges = _query_or_empty(
            graph,
            """
            MATCH (e:Entity)-[r:CONNECTS]->(n:EdgeNode)
            RETURN e.id AS source_id, n.id AS target_id, r.edge_type AS edge_type,
                   r.weight AS weight, r.confidence AS confidence,
                   r.evidence AS evidence, r.source_url AS source_url,
                   r.provenance AS provenance, r.created_at AS created_at,
                   r.expired_at AS expired_at, 'CONNECTS' AS rel_table
            """,
        )
        binds_edges = _query_or_empty(
            graph,
            """
            MATCH (n:EdgeNode)-[r:BINDS]->(e:Entity)
            RETURN n.id AS source_id, e.id AS target_id, r.edge_type AS edge_type,
                   r.weight AS weight, r.confidence AS confidence,
                   r.evidence AS evidence, r.source_url AS source_url,
                   r.provenance AS provenance, r.created_at AS created_at,
                   r.expired_at AS expired_at, 'BINDS' AS rel_table
            """,
        )
    finally:
        graph.close()
    return entities, documents, rel_edges + mention_edges + connects_edges + binds_edges


def load_full_graph_rows(graph_dir: Path) -> dict[str, list[dict]]:
    graph = Graph(graph_dir, read_only=True)
    try:
        entities, documents, entity_edges = load_graph_rows(graph_dir)
        return {
            "entities": entities,
            "documents": documents,
            "chunks": _query_or_empty(
                graph,
                """
                MATCH (c:Chunk)
                RETURN c.id AS id, c.doc_id AS doc_id, c.text AS text,
                       c.chunk_index AS chunk_index, c.created_at AS created_at,
                       c.embedding AS embedding
                """,
            ),
            "edge_nodes": _query_or_empty(
                graph,
                """
                MATCH (n:EdgeNode)
                RETURN n.id AS id, n.semantic_type AS semantic_type, n.label AS label,
                       n.weight AS weight, n.confidence AS confidence,
                       n.provenance AS provenance, n.created_at AS created_at,
                       n.expired_at AS expired_at
                """,
            ),
            "communities": _query_or_empty(
                graph,
                """
                MATCH (c:CommunityMeta)
                RETURN c.id AS id, c.community_id AS community_id, c.size AS size,
                       c.summary AS summary, c.top_entities AS top_entities,
                       c.computed_at AS computed_at, c.embedding AS embedding
                """,
            ),
            "entity_edges": entity_edges,
            "chunk_edges": _query_or_empty(
                graph,
                """
                MATCH (c:Chunk)-[r:CHUNK_OF]->(d:Document)
                RETURN c.id AS source_id, d.id AS target_id, r.edge_type AS edge_type,
                       r.weight AS weight, r.confidence AS confidence,
                       r.evidence AS evidence, r.source_url AS source_url,
                       r.provenance AS provenance, r.created_at AS created_at,
                       r.expired_at AS expired_at, 'CHUNK_OF' AS rel_table
                """,
            ),
        }
    finally:
        graph.close()


def classify_candidates(entities: list[dict], edges: list[dict]) -> tuple[list[dict], set[str]]:
    connected_ids = {
        entity_id
        for edge in edges
        for entity_id in (edge.get("source_id"), edge.get("target_id"))
        if entity_id
    }
    candidates = []
    for entity in entities:
        if entity["id"] in connected_ids:
            continue
        if not _is_unlinked_junk_entity(entity):
            continue
        candidates.append(entity)
    return candidates, connected_ids


def summarize(entities: list[dict], documents: list[dict], edges: list[dict], candidates: list[dict]) -> dict:
    by_type = Counter(e.get("entity_type") or "<blank>" for e in candidates)
    by_provenance = Counter(e.get("provenance") or "<blank>" for e in candidates)
    by_source = Counter(e.get("source_url") or "<blank>" for e in candidates)
    return {
        "entities_total": len(entities),
        "documents_total": len(documents),
        "edges_total": len(edges),
        "prune_candidates": len(candidates),
        "entities_after_projected": len(entities) - len(candidates),
        "by_type": dict(by_type.most_common()),
        "by_provenance": dict(by_provenance.most_common()),
        "top_sources": dict(by_source.most_common(20)),
        "candidate_ids": [e["id"] for e in candidates],
    }


def _create_node(graph: Graph, label: str, row: dict, props: list[str]) -> None:
    graph.conn.execute(f"CREATE (n:{label} {{id: $id}})", parameters={"id": row["id"]})
    for prop in props:
        if prop in row and row[prop] is not None:
            graph.conn.execute(
                f"MATCH (n:{label} {{id: $id}}) SET n.{prop} = $value",
                parameters={"id": row["id"], "value": row[prop]},
            )


def _create_rel(graph: Graph, rel: dict) -> None:
    table = rel.get("rel_table")
    if table == "RELATES_TO":
        match = "MATCH (a:Entity {id: $src}), (b:Entity {id: $tgt})"
    elif table == "MENTIONED_IN":
        match = "MATCH (a:Entity {id: $src}), (b:Document {id: $tgt})"
    elif table == "CHUNK_OF":
        match = "MATCH (a:Chunk {id: $src}), (b:Document {id: $tgt})"
    elif table == "CONNECTS":
        match = "MATCH (a:Entity {id: $src}), (b:EdgeNode {id: $tgt})"
    elif table == "BINDS":
        match = "MATCH (a:EdgeNode {id: $src}), (b:Entity {id: $tgt})"
    else:
        return

    graph.conn.execute(
        f"""
        {match}
        CREATE (a)-[r:{table}]->(b)
        SET r.edge_type = $edge_type, r.weight = $weight,
            r.confidence = $confidence, r.evidence = $evidence,
            r.source_url = $source_url, r.provenance = $provenance,
            r.created_at = $created_at, r.expired_at = $expired_at
        """,
        parameters={
            "src": rel.get("source_id"),
            "tgt": rel.get("target_id"),
            "edge_type": rel.get("edge_type") or table,
            "weight": rel.get("weight", 1.0),
            "confidence": rel.get("confidence", 0.5),
            "evidence": rel.get("evidence", ""),
            "source_url": rel.get("source_url", ""),
            "provenance": rel.get("provenance", "unknown"),
            "created_at": rel.get("created_at", 0),
            "expired_at": rel.get("expired_at", 0),
        },
    )


def rebuild_filtered_graph(source_graph_dir: Path, target_graph_dir: Path) -> dict:
    """Create a filtered graph copy using only CREATE writes.

    The source graph is opened read-only and never mutated. The target path must
    not exist; callers can move it into place only after external verification.
    """
    if target_graph_dir.exists():
        raise FileExistsError(f"Target graph already exists: {target_graph_dir}")

    rows = load_full_graph_rows(source_graph_dir)
    candidates, _ = classify_candidates(rows["entities"], rows["entity_edges"])
    candidate_ids = {e["id"] for e in candidates}
    kept_entity_ids = {e["id"] for e in rows["entities"] if e["id"] not in candidate_ids}
    kept_doc_ids = {d["id"] for d in rows["documents"]}
    kept_chunk_ids = {c["id"] for c in rows["chunks"]}
    kept_edge_node_ids = {n["id"] for n in rows["edge_nodes"]}

    target = Graph(target_graph_dir)
    try:
        for entity in rows["entities"]:
            if entity["id"] not in kept_entity_ids:
                continue
            _create_node(
                target,
                "Entity",
                entity,
                [
                    "entity_type",
                    "label",
                    "description",
                    "confidence",
                    "source_url",
                    "provenance",
                    "created_at",
                    "updated_at",
                    "embedding",
                    "layer",
                ],
            )

        for doc in rows["documents"]:
            _create_node(target, "Document", doc, ["path", "title", "ingested_at", "chunk_count"])

        for chunk in rows["chunks"]:
            _create_node(target, "Chunk", chunk, ["doc_id", "text", "chunk_index", "created_at", "embedding"])

        for edge_node in rows["edge_nodes"]:
            _create_node(
                target,
                "EdgeNode",
                edge_node,
                ["semantic_type", "label", "weight", "confidence", "provenance", "created_at", "expired_at"],
            )

        for community in rows["communities"]:
            _create_node(
                target,
                "CommunityMeta",
                community,
                ["community_id", "size", "summary", "top_entities", "computed_at", "embedding"],
            )

        kept_entity_edges = []
        for rel in rows["entity_edges"]:
            table = rel.get("rel_table")
            src = rel.get("source_id")
            tgt = rel.get("target_id")
            if table == "RELATES_TO" and src in kept_entity_ids and tgt in kept_entity_ids:
                kept_entity_edges.append(rel)
            elif table == "MENTIONED_IN" and src in kept_entity_ids and tgt in kept_doc_ids:
                kept_entity_edges.append(rel)
            elif table == "CONNECTS" and src in kept_entity_ids and tgt in kept_edge_node_ids:
                kept_entity_edges.append(rel)
            elif table == "BINDS" and src in kept_edge_node_ids and tgt in kept_entity_ids:
                kept_entity_edges.append(rel)

        kept_chunk_edges = [
            rel
            for rel in rows["chunk_edges"]
            if rel.get("source_id") in kept_chunk_ids and rel.get("target_id") in kept_doc_ids
        ]
        for rel in kept_entity_edges + kept_chunk_edges:
            _create_rel(target, rel)
    except Exception:
        target.close()
        if target_graph_dir.exists():
            shutil.rmtree(target_graph_dir)
        raise
    finally:
        target.close()

    return {
        "source_graph": str(source_graph_dir),
        "target_graph": str(target_graph_dir),
        "prune_candidates": len(candidate_ids),
        "entities_copied": len(kept_entity_ids),
        "entities_dropped": len(candidate_ids),
        "documents_copied": len(rows["documents"]),
        "chunks_copied": len(rows["chunks"]),
        "edge_nodes_copied": len(rows["edge_nodes"]),
        "communities_copied": len(rows["communities"]),
        "edges_copied": len(kept_entity_edges) + len(kept_chunk_edges),
        "candidate_ids": sorted(candidate_ids),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", default=str(config.GRAPH_DIR), help="Graph directory/path")
    parser.add_argument("--json", default="", help="Write dry-run report JSON to this path")
    parser.add_argument("--limit", type=int, default=30, help="Candidate sample size to print")
    parser.add_argument(
        "--rebuild-to",
        default="",
        help="Create a filtered graph copy at this path. Source graph is untouched.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Refused by default: use reconstruct-filtered rebuild, not in-place pruning.",
    )
    args = parser.parse_args(argv)

    if args.apply:
        print(
            "--apply is intentionally unsupported. Pruning uses reconstruct-filtered "
            "rebuild + swap so the pre-prune graph stays recoverable.",
            file=sys.stderr,
        )
        return 2

    if args.rebuild_to:
        report = rebuild_filtered_graph(Path(args.graph), Path(args.rebuild_to))
        print("Filtered graph rebuild complete")
        print(f"  source: {report['source_graph']}")
        print(f"  target: {report['target_graph']}")
        print(f"  entities copied: {report['entities_copied']}")
        print(f"  entities dropped: {report['entities_dropped']}")
        print(f"  edges copied: {report['edges_copied']}")
        if args.json:
            out = Path(args.json)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=2))
            print(f"\nReport written to {out}")
        return 0

    entities, documents, edges = load_graph_rows(Path(args.graph))
    candidates, connected_ids = classify_candidates(entities, edges)
    report = summarize(entities, documents, edges, candidates)

    print("Junk-entity pruning dry run")
    print(f"  graph: {args.graph}")
    print(f"  entities: {len(entities)}")
    print(f"  documents: {len(documents)}")
    print(f"  edges considered: {len(edges)}")
    print(f"  connected entity ids: {len(connected_ids)}")
    print(f"  prune candidates: {len(candidates)}")
    print(f"  projected entities after prune: {report['entities_after_projected']}")

    print("\nBy type:")
    for key, value in report["by_type"].items():
        print(f"  {key}: {value}")

    print("\nBy provenance:")
    for key, value in report["by_provenance"].items():
        print(f"  {key}: {value}")

    print(f"\nSample candidates (first {args.limit}):")
    for entity in candidates[: args.limit]:
        print(
            f"  {entity['id']} | {entity.get('entity_type')} | {entity.get('label')} | "
            f"{entity.get('provenance')} | {entity.get('source_url')}"
        )

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2))
        print(f"\nReport written to {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
