"""Tests for enrich.py chunk-store re-embed/re-link (scheduled enrichment)."""

import importlib.util
from pathlib import Path

from second_brain.chunk_store import ChunkStore

# enrich.py is a script, not a package module — load it by path.
_spec = importlib.util.spec_from_file_location(
    "enrich", Path(__file__).resolve().parent.parent / "scripts" / "enrich.py"
)
enrich = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(enrich)


class _FakeExtractor:
    """Returns empty LLM extraction so chunk-sync is tested without loading the
    real (slow, spaCy-backed) Extractor. The obsidian tag/wikilink entities that
    do the linking are added by enrich._add_obsidian_entities, not the LLM."""

    def extract_from_text(self, text, source_url=None, doc_id=None):
        return {"entities": [], "edges": []}


def _note():
    return {
        "body": "Notes on productivity and deep work habits for focus.",
        "path": "/vault/productivity.md",
        "relative_path": "productivity.md",
        "doc_id": "d_prod",
        "title": "Productivity",
        "tags": ["productivity"],
        "wikilinks": [],
    }


def test_enrich_note_syncs_chunks_and_links(tmp_path, graph, ontology, mock_ollama):
    extractor = _FakeExtractor()
    store = ChunkStore(tmp_path / "chunks.duckdb", embedding_dim=768)
    store.init_schema()
    try:
        stats = enrich.enrich_note(
            _note(), graph, extractor, ontology, embed=False, chunk_store=store
        )
        # Body chunked into the store.
        assert stats["chunks_written"] >= 1
        # The obsidian "productivity" tag entity (now carrying doc_id) links to
        # the chunk whose body mentions "productivity".
        assert stats["chunk_links"] >= 1

        hit = store.search_hybrid("deep work", query_embedding=None, limit=1)
        assert hit and "tag_productivity" in hit[0]["entity_ids"]
    finally:
        store.close()


def test_enrich_note_idempotent_chunks_on_rerun(tmp_path, graph, ontology, mock_ollama):
    extractor = _FakeExtractor()
    store = ChunkStore(tmp_path / "chunks.duckdb", embedding_dim=768)
    store.init_schema()
    try:
        first = enrich.enrich_note(
            _note(), graph, extractor, ontology, embed=False, chunk_store=store
        )
        count_after_first = store.get_stats()["total_chunks"]
        second = enrich.enrich_note(
            _note(), graph, extractor, ontology, embed=False, chunk_store=store
        )
        # Re-enriching the same note replaces its chunks, not duplicates them.
        assert first["chunks_written"] == second["chunks_written"]
        assert store.get_stats()["total_chunks"] == count_after_first
    finally:
        store.close()


def test_enrich_note_without_chunk_store_is_graph_only(tmp_path, graph, ontology, mock_ollama):
    extractor = _FakeExtractor()
    stats = enrich.enrich_note(
        _note(), graph, extractor, ontology, embed=False, chunk_store=None
    )
    assert stats["chunks_written"] == 0
    assert stats["chunk_links"] == 0
