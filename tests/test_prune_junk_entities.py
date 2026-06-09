"""Tests for junk-pruning dry-run classification."""

import pytest

from scripts.prune_junk_entities import classify_candidates, rebuild_filtered_graph, summarize
from second_brain.graph import Graph


def test_classify_candidates_only_prunes_unlinked_junk():
    entities = [
        {
            "id": "tag_fda",
            "label": "fda",
            "entity_type": "concept",
            "provenance": "obsidian_tag",
        },
        {
            "id": "1999",
            "label": "1999",
            "entity_type": "event",
            "provenance": "llm_extraction",
        },
        {
            "id": "fda",
            "label": "FDA",
            "entity_type": "organization",
            "provenance": "llm_extraction",
        },
        {
            "id": "concept_dcm",
            "label": "concept_dcm",
            "entity_type": "concept",
            "provenance": "llm_extraction",
        },
    ]
    edges = [{"source_id": "1999", "target_id": "fda", "edge_type": "mentions"}]

    candidates, connected = classify_candidates(entities, edges)

    assert connected == {"1999", "fda"}
    assert {entity["id"] for entity in candidates} == {"tag_fda", "concept_dcm"}


def test_summarize_reports_projected_prune_counts():
    entities = [
        {"id": "tag_fda", "label": "fda", "entity_type": "concept", "provenance": "obsidian_tag"},
        {"id": "fda", "label": "FDA", "entity_type": "organization", "provenance": "llm_extraction"},
    ]
    candidates = [entities[0]]

    report = summarize(entities, documents=[{"id": "d1"}], edges=[], candidates=candidates)

    assert report["entities_total"] == 2
    assert report["prune_candidates"] == 1
    assert report["entities_after_projected"] == 1
    assert report["by_provenance"] == {"obsidian_tag": 1}


def test_rebuild_filtered_graph_copies_only_kept_entities(tmp_path, ontology):
    source_dir = tmp_path / "source.lbug"
    target_dir = tmp_path / "target.lbug"
    source = Graph(source_dir, ontology)
    try:
        source.add_document("d1", "note.md", "Note")
        source.add_entity("tag_noise", "concept", "noise", provenance="obsidian_tag")
        source.add_entity("kept", "concept", "Kept", provenance="llm_extraction")
        source.add_entity("source", "source", "Source", provenance="llm_extraction")
        source.add_edge("kept", "source", "LEARNED_FROM", evidence="Kept source")
        source.bulk_add_mentions([{"entity_id": "kept", "doc_id": "d1"}])
    finally:
        source.close()

    report = rebuild_filtered_graph(source_dir, target_dir)

    assert report["entities_dropped"] == 1
    assert report["candidate_ids"] == ["tag_noise"]

    rebuilt = Graph(target_dir, ontology, read_only=True)
    try:
        rows = rebuilt.query("MATCH (e:Entity) RETURN e.id AS id ORDER BY id")
        assert rows == [{"id": "kept"}, {"id": "source"}]
        rels = rebuilt.query(
            """
            MATCH (a:Entity)-[r:RELATES_TO]->(b:Entity)
            RETURN a.id AS src, b.id AS tgt, r.edge_type AS type
            """
        )
        assert rels == [{"src": "kept", "tgt": "source", "type": "LEARNED_FROM"}]
        mentions = rebuilt.query(
            """
            MATCH (e:Entity)-[r:MENTIONED_IN]->(d:Document)
            RETURN e.id AS entity_id, d.id AS doc_id, r.edge_type AS type
            """
        )
        assert mentions == [{"entity_id": "kept", "doc_id": "d1", "type": "MENTIONED_IN"}]
    finally:
        rebuilt.close()

    original = Graph(source_dir, ontology, read_only=True)
    try:
        rows = original.query("MATCH (e:Entity {id: 'tag_noise'}) RETURN e.id AS id")
        assert rows == [{"id": "tag_noise"}]
    finally:
        original.close()


def test_rebuild_filtered_graph_refuses_existing_target(tmp_path):
    source_dir = tmp_path / "source.lbug"
    target_dir = tmp_path / "target.lbug"
    target_dir.mkdir()

    with pytest.raises(FileExistsError):
        rebuild_filtered_graph(source_dir, target_dir)
