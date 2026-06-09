"""Apply entity resolution to the live graph via RECONSTRUCT-FILTERED.

Phase D of entity resolution. The resolver (`scripts/resolve_entities.py`) only
proposes a clustering; this applies it. We never mutate in place: we build a NEW
graph that already has the merges baked in (all CREATE, zero DELETE), verify it
on disk, and only then swap it in behind a backup. In-place node/edge DELETE was
unsafe on the older `real_ladybug` build this stack started on; it tests clean on
ladybug 0.17.1 (see `scripts/repro_bulk_delete.py`), but reconstruct-and-swap
stays the default because the pre-merge graph remains recoverable — a merge you
got wrong is one `mv` away from undo.

Flow:
  1. Read every entity (with embedding) and RELATES_TO edge from the source.
  2. Cluster with the SAME EntityResolver + embeddings the dry-run/eval used.
  3. Map id -> canonical_id (slugify of the cluster's canonical label); merge
     each group into one node; repoint edges, drop self-loops, dedup.
  4. Write a fresh graph at --out; set embeddings; rebuild vector indexes.
  5. Verify: counts reconcile, no orphan edge endpoints, embeddings present,
     a search returns results. Report collateral.
  6. --swap only: back up the live graph, then mv the new graph into place.

    python -m scripts.apply_resolution                 # build + verify, no swap
    python -m scripts.apply_resolution --swap          # build, verify, then swap
    python -m scripts.apply_resolution --no-embeddings # Phase-A only (F1 0.808)
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from second_brain import config
from second_brain.ontology import slugify
from second_brain.pipeline import EntityResolver

RELATES_TO = "RELATES_TO"


def _remove_path(p: Path) -> None:
    """Remove a LadybugDB store whether it is a single file or a directory."""
    if not p.exists():
        return
    if p.is_dir():
        shutil.rmtree(p)
    else:
        p.unlink()


def _read_graph(graph_dir: Path) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """Read entities (props + embedding), edges, documents, and mentions.

    Documents are independent nodes (not merged); mentions are Entity->Document
    provenance edges that must be repointed through the merge id map.
    """
    from second_brain.graph import Graph

    g = Graph(graph_dir, read_only=True)
    try:
        ent_rows = g.query(
            "MATCH (e:Entity) RETURN e.id AS id, e.label AS label, "
            "e.entity_type AS entity_type, e.description AS description, "
            "e.confidence AS confidence, e.source_url AS source_url, "
            "e.provenance AS provenance, e.embedding AS embedding"
        )
        edge_rows = g.query(
            f"MATCH (a:Entity)-[r:{RELATES_TO}]->(b:Entity) "
            "RETURN a.id AS source_id, b.id AS target_id, r.edge_type AS edge_type, "
            "r.confidence AS confidence, r.evidence AS evidence, "
            "r.source_url AS source_url, r.provenance AS provenance, r.weight AS weight"
        )
        doc_rows = g.query(
            "MATCH (d:Document) RETURN d.id AS id, d.path AS path, d.title AS title"
        )
        mention_rows = g.query(
            "MATCH (e:Entity)-[r:MENTIONED_IN]->(d:Document) "
            "RETURN e.id AS entity_id, d.id AS doc_id, r.confidence AS confidence, "
            "r.source_url AS source_url, r.provenance AS provenance"
        )
    finally:
        g.close()

    entities = [dict(r) for r in ent_rows]
    for e in entities:
        e["embedding"] = list(e["embedding"]) if e.get("embedding") is not None else None
    edges = [dict(r) for r in edge_rows]
    documents = [dict(r) for r in doc_rows]
    mentions = [dict(r) for r in mention_rows]
    return entities, edges, documents, mentions


def _canonical_map(entities: list[dict], use_embeddings: bool) -> dict[str, str]:
    """Return label -> canonical_label from the resolver clustering."""
    resolver_input = [{"label": e["label"], "entity_type": e["entity_type"]} for e in entities]
    embeddings = None
    if use_embeddings:
        embeddings = {
            e["label"]: e["embedding"] for e in entities if e.get("embedding") is not None
        }
    result = EntityResolver(resolver_input, embeddings=embeddings).resolve()
    return {
        member: cluster.canonical for cluster in result.clusters for member in cluster.members
    }


def _merge_group(canonical_id: str, canonical_label: str, group: list[dict]) -> dict:
    """Merge a cluster of source entities into one canonical node dict.

    Type prefers a typed (non-concept) member by confidence; description is the
    longest; confidence is the max. Embedding preference is handled by caller.
    """

    def conf(e: dict) -> float:
        try:
            return float(e.get("confidence", 0.5))
        except (TypeError, ValueError):
            return 0.5

    typed = [e for e in group if (e.get("entity_type") or "concept") != "concept"]
    type_src = max(typed or group, key=conf)
    desc_src = max(group, key=lambda e: len(e.get("description") or ""))
    best = max(group, key=conf)
    return {
        "id": canonical_id,
        "entity_type": type_src.get("entity_type") or "concept",
        "label": canonical_label,
        "description": desc_src.get("description") or "",
        "confidence": max(conf(e) for e in group),
        "source_url": best.get("source_url", ""),
        "provenance": best.get("provenance", "resolved"),
    }


def build_merged(
    entities: list[dict], edges: list[dict], use_embeddings: bool, mentions: list[dict] | None = None
):
    """Compute the merged entity set, edge set, id map, embedding map, mentions."""
    label_to_canonical = _canonical_map(entities, use_embeddings)

    id_to_canonical: dict[str, str] = {}
    groups: dict[str, list[dict]] = {}
    canonical_label_for: dict[str, str] = {}
    for e in entities:
        label = (e.get("label") or "").strip()
        canonical_label = label_to_canonical.get(label, label)
        canonical_id = slugify(canonical_label)
        id_to_canonical[e["id"]] = canonical_id
        groups.setdefault(canonical_id, []).append(e)
        canonical_label_for[canonical_id] = canonical_label

    merged_entities = []
    embedding_map: dict[str, list[float]] = {}
    for canonical_id, group in groups.items():
        canonical_label = canonical_label_for[canonical_id]
        merged_entities.append(_merge_group(canonical_id, canonical_label, group))
        # Prefer the embedding of the member whose label IS the canonical label;
        # else the highest-confidence member that has one.
        with_emb = [e for e in group if e.get("embedding") is not None]
        if with_emb:
            canon_member = next((e for e in with_emb if e["label"] == canonical_label), None)
            chosen = canon_member or max(
                with_emb, key=lambda e: float(e.get("confidence", 0.5) or 0.5)
            )
            embedding_map[canonical_id] = chosen["embedding"]

    # Repoint edges, drop self-loops, dedup by (src, tgt, type).
    merged_edges = []
    seen = set()
    for edge in edges:
        src = id_to_canonical.get(edge["source_id"], edge["source_id"])
        tgt = id_to_canonical.get(edge["target_id"], edge["target_id"])
        if src == tgt:
            continue
        key = (src, tgt, edge.get("edge_type"))
        if key in seen:
            continue
        seen.add(key)
        merged_edges.append({**edge, "source_id": src, "target_id": tgt})

    # Repoint mentions (Entity->Document) onto canonical entity ids; dedup.
    merged_mentions = []
    seen_m = set()
    for m in mentions or []:
        eid = id_to_canonical.get(m["entity_id"], m["entity_id"])
        key = (eid, m["doc_id"])
        if key in seen_m:
            continue
        seen_m.add(key)
        merged_mentions.append({**m, "entity_id": eid})

    return merged_entities, merged_edges, id_to_canonical, embedding_map, merged_mentions


def write_graph(
    out_dir: Path, merged_entities, merged_edges, embedding_map, documents, merged_mentions, ontology
):
    """Write the merged graph to a fresh path (all CREATE)."""
    from second_brain.graph import Graph

    _remove_path(out_dir)
    g = Graph(out_dir, ontology=ontology)
    try:
        loaded = g.bulk_add_entities(merged_entities)
        for cid, emb in embedding_map.items():
            try:
                g.set_embedding(cid, emb)
            except Exception as ex:  # noqa: BLE001
                print(f"  warn: embedding set failed for {cid}: {ex}", file=sys.stderr)
        for d in documents:
            g.add_document(d["id"], d.get("path", ""), d.get("title", ""))
        edges_loaded = g.bulk_add_edges(merged_edges)
        mentions_loaded = g.bulk_add_mentions(merged_mentions)
        g.rebuild_vector_indexes()
        g.flush()
        return loaded, edges_loaded, len(documents), mentions_loaded
    finally:
        g.close()


def verify(
    out_dir: Path,
    expected_entities: int,
    merged_edges: list[dict],
    expected_documents: int,
) -> tuple[bool, list[str]]:
    """Re-open the new graph from a fresh handle and check integrity."""
    from second_brain.graph import Graph

    notes: list[str] = []
    ok = True
    g = Graph(out_dir, read_only=True)
    try:
        n_ent = g.entity_count()
        n_edge = g.edge_count()
        n_doc = g.document_count()
        notes.append(f"entities: {n_ent} (expected {expected_entities})")
        if n_ent != expected_entities:
            ok = False
            notes.append("  ✗ entity count mismatch")
        notes.append(f"documents: {n_doc} (expected {expected_documents})")
        if n_doc != expected_documents:
            ok = False
            notes.append("  ✗ document count mismatch — documents lost in rebuild")

        # Every edge endpoint must resolve to a real node.
        type_of = {r["id"]: r["t"] for r in g.query("MATCH (e:Entity) RETURN e.id AS id, e.entity_type AS t")}
        ids = set(type_of)
        orphan = sum(
            1 for e in merged_edges if e["source_id"] not in ids or e["target_id"] not in ids
        )
        notes.append(f"edges in graph: {n_edge}; repointed edges computed: {len(merged_edges)}")
        if orphan:
            ok = False
            notes.append(f"  ✗ {orphan} edges reference a missing endpoint")

        # Audit every dropped edge. In a reconstruct the only drop mechanisms are
        # the ontology type gate and grade-locality enforcement — both legitimate.
        # A drop whose endpoints DO exist is a grade-locality drop (expected,
        # explained); we list them so the loss is never silent.
        persisted = {
            (r["s"], r["t"], r["et"])
            for r in g.query(
                f"MATCH (a:Entity)-[r:{RELATES_TO}]->(b:Entity) "
                "RETURN a.id AS s, b.id AS t, r.edge_type AS et"
            )
        }
        missing = [
            e
            for e in merged_edges
            if (e["source_id"], e["target_id"], e["edge_type"]) not in persisted
        ]
        if missing:
            notes.append(f"  {len(missing)} edge(s) dropped (grade-locality / type gate):")
            for e in missing:
                st, tt = type_of.get(e["source_id"], "?"), type_of.get(e["target_id"], "?")
                notes.append(
                    f"    {e['edge_type']}: {e['source_id']} [{st}] -> {e['target_id']} [{tt}]"
                )

        # Embedding coverage + a working vector search.
        emb = g.query("MATCH (e:Entity) WHERE e.embedding IS NOT NULL RETURN count(e) AS c")[0]["c"]
        notes.append(f"entities with embedding: {emb}")
        sample = g.query("MATCH (e:Entity) RETURN e.embedding AS v LIMIT 1")
        if sample and sample[0]["v"] is not None:
            hits = g.vector_search(list(sample[0]["v"]), limit=3)
            notes.append(f"vector_search sanity: {len(hits)} hits")
            if not hits:
                ok = False
                notes.append("  ✗ vector search returned nothing")
    finally:
        g.close()
    return ok, notes


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--graph", default=str(config.GRAPH_DIR), help="Source graph")
    ap.add_argument("--out", default=str(config.GRAPH_DIR) + ".merged", help="New graph path")
    ap.add_argument(
        "--ontology",
        default=None,
        help="Ontology the graph was built with (YAML or markdown ONTOLOGY.md). "
        "MUST match the graph's entity types or bulk load silently drops them.",
    )
    ap.add_argument("--no-embeddings", action="store_true", help="Phase-A only (no similarity)")
    ap.add_argument("--swap", action="store_true", help="Back up + swap into place if verified")
    args = ap.parse_args(argv)

    src = Path(args.graph)
    out = Path(args.out)

    if args.ontology:
        from second_brain.ontology_yaml import load_ontology

        ontology = load_ontology(args.ontology)
    else:
        from second_brain.ontology import Ontology

        ontology = Ontology()
    print(f"Ontology node types: {sorted(ontology.NODE_TYPES)}")

    print(f"Reading source graph: {src}")
    entities, edges, documents, mentions = _read_graph(src)
    print(f"  {len(entities)} entities, {len(edges)} edges, {len(documents)} docs, "
          f"{len(mentions)} mentions")

    merged_entities, merged_edges, id_map, embedding_map, merged_mentions = build_merged(
        entities, edges, use_embeddings=not args.no_embeddings, mentions=mentions
    )
    folded = len(entities) - len(merged_entities)
    print(
        f"Merge plan: {len(entities)} -> {len(merged_entities)} entities "
        f"({folded} folded), {len(edges)} -> {len(merged_edges)} edges "
        f"({len(edges) - len(merged_edges)} self-loops/dups removed), "
        f"{len(documents)} docs preserved"
    )

    print(f"Writing merged graph: {out}")
    loaded, edges_loaded, docs_loaded, mentions_loaded = write_graph(
        out, merged_entities, merged_edges, embedding_map, documents, merged_mentions, ontology
    )
    print(f"  loaded {loaded} entities, {edges_loaded} edges, {docs_loaded} docs, "
          f"{mentions_loaded} mentions")

    # Collateral: edges that should have written but did not (e.g. grade filter).
    edge_collateral = len(merged_edges) - edges_loaded
    print("Verifying...")
    ok, notes = verify(
        out,
        expected_entities=len(merged_entities),
        merged_edges=merged_edges,
        expected_documents=len(documents),
    )
    for n in notes:
        print(f"  {n}")
    print(f"  edge collateral (computed - written): {edge_collateral}")
    if edge_collateral != 0:
        print("  ⚠ some repointed edges did not persist (likely grade-locality filter)")

    if not ok:
        print("\n✗ VERIFICATION FAILED — live graph untouched, not swapping.", file=sys.stderr)
        return 1

    print("\n✓ Verification passed.")
    if not args.swap:
        print(f"Merged graph left at {out}. Re-run with --swap to back up + install it.")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = src.with_name(src.name + f".bak-{stamp}")
    print(f"Backing up live graph -> {backup}")
    shutil.copytree(src, backup) if src.is_dir() else shutil.copy2(src, backup)
    # Verify the backup opens and counts before we touch the live graph.
    from second_brain.graph import Graph

    bg = Graph(backup, read_only=True)
    try:
        bcount = bg.entity_count()
    finally:
        bg.close()
    print(f"  backup verified: opens read-only, {bcount} entities")

    print("Swapping merged graph into place...")
    _remove_path(src)
    shutil.move(str(out), str(src))
    print(f"✓ Swapped. Backup at {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
