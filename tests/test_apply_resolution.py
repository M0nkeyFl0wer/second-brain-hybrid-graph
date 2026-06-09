"""Tests for apply_resolution.build_merged (entity-resolution apply, Phase D)."""

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "apply_resolution", Path(__file__).resolve().parent.parent / "scripts" / "apply_resolution.py"
)
apply_resolution = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(apply_resolution)


def _ent(eid, label, etype="organization", conf=0.8):
    return {
        "id": eid,
        "label": label,
        "entity_type": etype,
        "description": f"desc {label}",
        "confidence": conf,
        "source_url": "",
        "provenance": "test",
        "embedding": None,
    }


def test_build_merged_folds_acronym_and_repoints_edges():
    entities = [
        _ent("american_kennel_club", "American Kennel Club"),
        _ent("akc", "AKC"),
        _ent("dog", "Dog", etype="concept"),
    ]
    edges = [
        {"source_id": "akc", "target_id": "dog", "edge_type": "mentions", "confidence": 0.7},
    ]
    merged, med, id_map, emb_map, _m = apply_resolution.build_merged(
        entities, edges, use_embeddings=False
    )

    # AKC + American Kennel Club fold into one canonical; Dog stands alone.
    assert id_map["akc"] == id_map["american_kennel_club"]
    assert len({e["id"] for e in merged}) == 2

    # The edge endpoint is repointed onto the canonical id, not the alias.
    assert len(med) == 1
    assert med[0]["source_id"] == id_map["akc"]
    assert med[0]["target_id"] == "dog"


def test_build_merged_drops_self_loops_and_dups():
    # Two aliases that fold together, with an edge BETWEEN them -> self-loop.
    entities = [
        _ent("american_kennel_club", "American Kennel Club"),
        _ent("akc", "AKC"),
    ]
    edges = [
        {"source_id": "akc", "target_id": "american_kennel_club", "edge_type": "alias_of"},
        {"source_id": "american_kennel_club", "target_id": "akc", "edge_type": "alias_of"},
    ]
    merged, med, id_map, _e, _m = apply_resolution.build_merged(entities, edges, use_embeddings=False)
    assert len(merged) == 1
    # Both edges collapse to a self-loop on the canonical and are dropped.
    assert med == []


def test_build_merged_carries_embedding_to_canonical():
    entities = [
        _ent("american_kennel_club", "American Kennel Club"),
        {**_ent("akc", "AKC"), "embedding": [0.1, 0.2, 0.3]},
    ]
    _, _, id_map, emb_map, _m = apply_resolution.build_merged(entities, [], use_embeddings=False)
    canonical = id_map["akc"]
    # The only member with an embedding contributes it to the canonical node.
    assert emb_map.get(canonical) == [0.1, 0.2, 0.3]
