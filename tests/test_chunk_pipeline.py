"""Tests for document → chunk-store ingestion (second_brain.pipeline.chunks)."""

import pytest

from second_brain.chunk_store import ChunkStore
from second_brain.pipeline.chunks import chunk_document, ingest_document_chunks


def _fake_embed(dim=4):
    """Deterministic embed_batch stand-in: one fixed vector per input chunk."""

    def embed(texts):
        return [[float(len(t) % 7), 1.0, 0.0, 0.0][:dim] for t in texts]

    return embed


def test_chunk_document_overlap_and_empty():
    assert chunk_document("") == []
    assert chunk_document("   \n\t ") == []
    chunks = chunk_document("x" * 2500, chunk_size=1000, overlap=200)
    # 1000-char windows stepping 800 chars over 2500 chars -> 4 windows.
    assert len(chunks) == 4
    with pytest.raises(ValueError):
        chunk_document("abc", chunk_size=100, overlap=100)


def test_ingest_writes_embedded_chunks(tmp_path):
    store = ChunkStore(tmp_path / "chunks.duckdb", embedding_dim=4)
    store.init_schema()
    try:
        n = ingest_document_chunks(
            store,
            doc_id="d1",
            source_uri="note.md",
            title="Note",
            text="A graph database stores typed relationships between entities.",
            embed_batch_fn=_fake_embed(),
        )
        assert n >= 1
        stats = store.get_stats()
        assert stats["total_chunks"] == n
        assert stats["embedded_chunks"] == n  # embeddings present -> embedded_at stamped
    finally:
        store.close()


def test_ingest_is_idempotent_per_doc(tmp_path):
    store = ChunkStore(tmp_path / "chunks.duckdb", embedding_dim=4)
    store.init_schema()
    try:
        text = "Persistent homology detects topological holes in point clouds."
        first = ingest_document_chunks(
            store, doc_id="d1", source_uri="note.md", title="N",
            text=text, embed_batch_fn=_fake_embed(),
        )
        # Re-ingesting the same doc must replace, not duplicate.
        second = ingest_document_chunks(
            store, doc_id="d1", source_uri="note.md", title="N",
            text=text, embed_batch_fn=_fake_embed(),
        )
        assert first == second
        assert store.get_stats()["total_chunks"] == first
    finally:
        store.close()


def test_ingest_falls_back_to_bm25_when_embedding_fails(tmp_path):
    store = ChunkStore(tmp_path / "chunks.duckdb", embedding_dim=4)
    store.init_schema()

    def boom(texts):
        raise RuntimeError("embed backend down")

    try:
        n = ingest_document_chunks(
            store,
            doc_id="d1",
            source_uri="note.md",
            title="Note",
            text="Reciprocal rank fusion merges keyword and vector rankings.",
            embed_batch_fn=boom,
        )
        assert n >= 1
        stats = store.get_stats()
        assert stats["total_chunks"] == n
        assert stats["embedded_chunks"] == 0  # no embeddings, but chunks landed
        # BM25-only retrieval still works.
        hits = store.search_hybrid("rank fusion", query_embedding=None, limit=1)
        assert hits and "fusion" in hits[0]["body"]
    finally:
        store.close()


def test_ingest_hybrid_retrieval_end_to_end(tmp_path):
    store = ChunkStore(tmp_path / "chunks.duckdb", embedding_dim=4)
    store.init_schema()
    try:
        ingest_document_chunks(
            store, doc_id="d1", source_uri="graph.md", title="Graph",
            text="A graph database stores typed relationships.",
            embed_batch_fn=_fake_embed(),
        )
        ingest_document_chunks(
            store, doc_id="d2", source_uri="garden.md", title="Garden",
            text="Tomatoes grow in warm soil.",
            embed_batch_fn=_fake_embed(),
        )
        results = store.search_hybrid(
            "typed relationships", query_embedding=[1.0, 1.0, 0.0, 0.0], limit=1
        )
        assert results and "relationships" in results[0]["body"]
    finally:
        store.close()
