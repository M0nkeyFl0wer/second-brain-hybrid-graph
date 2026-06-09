"""Tests for the MCP server's passage-retrieval helper (memory_search chunks mode)."""

import second_brain.mcp_server as mcp_server
from second_brain.chunk_store import ChunkStore
from second_brain.embed import embed_batch
from second_brain.pipeline.chunks import ingest_document_chunks, link_entities_to_chunks


def test_passage_search_returns_passages_with_entity_pivots(tmp_path, graph, mock_ollama):
    # Entities present in the graph so pivots resolve to labels/types.
    graph.add_entity("border_collie", "concept", "Border Collie", confidence=0.9)
    graph.add_entity("agility", "concept", "agility", confidence=0.8)

    store = ChunkStore(tmp_path / "chunks.duckdb", embedding_dim=768)
    store.init_schema()
    try:
        ingest_document_chunks(
            store,
            doc_id="d1",
            source_uri="collie.md",
            title="Collie",
            text="Border Collies are intelligent herding dogs that excel at agility.",
            embed_batch_fn=embed_batch,
        )
        link_entities_to_chunks(
            store,
            [
                # Canonicalization folds the plural into aliases — the body says
                # "Border Collies", matched via the alias, not the canonical label.
                {
                    "id": "border_collie",
                    "label": "Border Collie",
                    "aliases": ["Border Collie", "Border Collies"],
                    "doc_ids": ["d1"],
                },
                {"id": "agility", "label": "agility", "doc_ids": ["d1"]},
            ],
        )

        out = mcp_server.passage_search(graph, store, "herding dogs", limit=5)

        assert "passages for" in out
        assert "Border Collies are intelligent" in out
        # Pivots resolve to graph labels + types, not raw ids.
        assert "Border Collie (concept)" in out
        assert "agility (concept)" in out
    finally:
        store.close()


def test_passage_search_handles_no_results(tmp_path, graph, mock_ollama):
    store = ChunkStore(tmp_path / "chunks.duckdb", embedding_dim=768)
    store.init_schema()
    try:
        out = mcp_server.passage_search(graph, store, "nonexistent topic", limit=5)
        assert "No passages found" in out
    finally:
        store.close()


def test_thought_doc_id_is_deterministic():
    a = mcp_server.thought_doc_id("a captured thought")
    b = mcp_server.thought_doc_id("a captured thought")
    c = mcp_server.thought_doc_id("a different thought")
    assert a == b and a != c
    assert a.startswith("mcp_")


def test_store_thought_passages_round_trips(tmp_path, mock_ollama):
    store = ChunkStore(tmp_path / "chunks.duckdb", embedding_dim=768)
    store.init_schema()
    try:
        text = "Reciprocal rank fusion merges keyword and vector rankings robustly."
        doc_id = mcp_server.thought_doc_id(text)
        # Entities carry the thought's doc_id (as memory_write threads it through).
        entities = [
            {"id": "rrf", "label": "rank fusion", "doc_ids": [doc_id]},
        ]
        links = mcp_server.store_thought_passages(store, text, doc_id, entities)
        assert links == 1

        hits = store.search_hybrid("rank fusion", query_embedding=None, limit=1)
        assert hits and "rrf" in hits[0]["entity_ids"]

        # Re-storing the same thought replaces rather than duplicates (idempotent).
        before = store.get_stats()["total_chunks"]
        mcp_server.store_thought_passages(store, text, doc_id, entities)
        assert store.get_stats()["total_chunks"] == before
    finally:
        store.close()


def test_get_chunk_store_none_when_absent(tmp_path, monkeypatch):
    monkeypatch.setattr(
        mcp_server.config, "CHUNK_STORE_PATH", tmp_path / "does-not-exist.duckdb"
    )
    monkeypatch.setattr(mcp_server, "_chunk_store", None)
    assert mcp_server._get_chunk_store() is None
