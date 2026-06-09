"""Tests for the DuckDB chunk substrate."""

import duckdb

from second_brain.chunk_store import ChunkStore


def test_chunk_store_initializes_and_writes_chunks(tmp_path):
    store = ChunkStore(tmp_path / "chunks.duckdb")
    try:
        store.init_schema()
        count = store.write_chunks(
            [
                {
                    "id": "c1",
                    "doc_id": "d1",
                    "source_uri": "note.md",
                    "title": "Note",
                    "body": "A graph database stores typed relationships.",
                    "chunk_index": 0,
                    "entity_ids": ["graph_database"],
                }
            ]
        )

        assert count == 1
        assert store.get_stats()["total_chunks"] == 1
        assert store.get_chunk_by_id("c1")["entity_ids"] == ["graph_database"]
    finally:
        store.close()


def test_chunk_store_defines_embedding_column(tmp_path):
    db_path = tmp_path / "chunks.duckdb"
    store = ChunkStore(db_path, embedding_dim=3)
    try:
        store.init_schema()
        store.upsert_chunk_with_embedding(
            chunk_id="c1",
            doc_id="d1",
            source_uri="note.md",
            body="Embedding backed chunk.",
            chunk_index=0,
            embedding=[1.0, 0.0, 0.0],
        )
    finally:
        store.close()

    conn = duckdb.connect(str(db_path), read_only=True)
    try:
        row = conn.execute("SELECT embedding FROM chunk WHERE id = 'c1'").fetchone()
        assert list(row[0]) == [1.0, 0.0, 0.0]
    finally:
        conn.close()


def test_chunk_store_searches_bm25_without_embedding(tmp_path):
    store = ChunkStore(tmp_path / "chunks.duckdb")
    try:
        store.init_schema()
        store.write_chunks(
            [
                {
                    "id": "c1",
                    "doc_id": "d1",
                    "source_uri": "graph.md",
                    "title": "Graph",
                    "body": "A graph database stores typed relationships.",
                    "chunk_index": 0,
                },
                {
                    "id": "c2",
                    "doc_id": "d2",
                    "source_uri": "garden.md",
                    "title": "Garden",
                    "body": "Tomatoes grow in warm soil.",
                    "chunk_index": 0,
                },
            ]
        )

        results = store.search_hybrid("typed relationships", query_embedding=None, limit=1)

        assert [r["id"] for r in results] == ["c1"]
    finally:
        store.close()
