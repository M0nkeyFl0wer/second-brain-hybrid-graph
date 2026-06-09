"""
DuckDB chunk store for open-second-brain — FTS + HNSW + RRF hybrid retrieval.

Architecture:
- chunks.duckdb: single-file embedded DuckDB
- FTS index: BM25 via fts_main_chunk.match_bm25
- HNSW index: vector similarity via vss extension

Write strategy:
- Bulk insert: COPY FROM (fast)
- Re-embed: DELETE matching rows + INSERT fresh (HNSW blocks UPDATE)

Two-handle RRF pattern:
- _ro (read-only persistent handle): FTS (match_bm25) queries
- _mem (in-memory handle): HNSW queries
- Python-side RRF fusion in search_hybrid()

Concurrency: one writer only (DuckDB allows one write process).
Readers can share _ro handle (read_only=True).
"""

import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import duckdb

# Default config
DEFAULT_CHUNK_SIZE = 500
DEFAULT_EMBEDDING_DIM = 768
RRF_K = 60  # Standard RRF constant from Cormack 2009


class ChunkStore:
    """
    DuckDB wrapper for chunk storage + hybrid retrieval.

    Usage:
        # Writer process (single)
        store = ChunkStore("data/chunks.duckdb")
        store.init_schema()
        store.write_chunks(chunks)

        # Reader process (multiple OK)
        store_ro = ChunkStore("data/chunks.duckdb", read_only=True)
        results = store_ro.search_hybrid("query", embedding)
    """

    def __init__(
        self,
        db_path: str | Path,
        read_only: bool = False,
        embedding_dim: int = DEFAULT_EMBEDDING_DIM,
    ):
        self.db_path = Path(db_path)
        self.read_only = read_only
        self.embedding_dim = int(embedding_dim)
        if self.embedding_dim <= 0:
            raise ValueError("embedding_dim must be positive")
        self._ro: Optional[duckdb.DuckDBPyConnection] = None
        self._mem: Optional[duckdb.DuckDBPyConnection] = None

    def _open_ro(self) -> duckdb.DuckDBPyConnection:
        """Open read-only persistent handle for FTS queries."""
        if self._ro is None:
            self._ro = duckdb.connect(str(self.db_path), read_only=True)
            try:
                self._ro.execute("LOAD fts;")
            except Exception:
                pass
        return self._ro

    def _open_mem(self) -> duckdb.DuckDBPyConnection:
        """Open in-memory handle for HNSW queries (built from on-disk data at boot).

        Embeddings are pulled through the already-open read-only handle as Arrow
        and materialized in memory. We deliberately do NOT ``ATTACH`` the file
        here: the persistent ``_ro`` handle already holds it open, and DuckDB
        forbids attaching a file that another connection in the same process has
        open as its main database ("Unique file handle conflict").
        """
        if self._mem is None:
            mem = duckdb.connect(":memory:")
            mem.execute("LOAD vss;")
            # Pull embeddings via the existing read-only handle (no 2nd file handle).
            ro = self._open_ro()
            vec_arrow = ro.execute(
                "SELECT id, embedding FROM chunk WHERE embedding IS NOT NULL"
            ).arrow()
            mem.register("chunk_vec_src", vec_arrow)
            mem.execute("CREATE TABLE chunk_vec AS SELECT * FROM chunk_vec_src;")
            mem.unregister("chunk_vec_src")
            # HNSW index built in-memory for fast cosine queries.
            mem.execute("""
                CREATE INDEX chunk_emb_hnsw ON chunk_vec
                USING HNSW (embedding)
                WITH (metric='cosine', ef_construction=200, M=32);
            """)
            self._mem = mem
        return self._mem

    def _open_rw(self) -> duckdb.DuckDBPyConnection:
        """Open read-write handle for writer process."""
        conn = duckdb.connect(str(self.db_path), read_only=False)
        try:
            conn.execute("LOAD vss;")
        except Exception:
            pass
        return conn

    def init_schema(self) -> None:
        """
        Initialize DuckDB schema: chunk table, FTS index, HNSW index.

        Call once during first setup. Safe to re-run (idempotent).
        """
        rw = self._open_rw()
        try:
            try:
                rw.execute("LOAD fts;")
            except Exception:
                pass

            # Chunk table — FLOAT[dim] for fixed-dim HNSW compatibility
            rw.execute(f"""
                CREATE TABLE IF NOT EXISTS chunk (
                    id              VARCHAR PRIMARY KEY,
                    doc_id          VARCHAR NOT NULL,
                    source_uri      VARCHAR NOT NULL,
                    title           VARCHAR,
                    body            VARCHAR NOT NULL,
                    chunk_index     INTEGER NOT NULL,
                    entity_ids      VARCHAR,
                    embedding       FLOAT[{self.embedding_dim}],
                    sensitivity     VARCHAR DEFAULT 'public',
                    created_at      TIMESTAMP DEFAULT current_timestamp,
                    source_mtime    TIMESTAMP,
                    embedded_at     TIMESTAMP
                );
            """)

            # Indexes
            rw.execute("CREATE INDEX IF NOT EXISTS idx_chunk_doc ON chunk(doc_id);")
            rw.execute("CREATE INDEX IF NOT EXISTS idx_chunk_sensitivity ON chunk(sensitivity);")

            # FTS index (BM25) — must rebuild after batch inserts
            # PRAGMA create_fts_index is idempotent with overwrite=1
            rw.execute("""
                PRAGMA create_fts_index(
                    'chunk', 'id',
                    'body', 'title',
                    stemmer='porter',
                    stopwords='english',
                    overwrite=1
                );
            """)

            # HNSW is built in memory by _open_mem(). Avoid persistent HNSW here:
            # DuckDB marks persistent HNSW experimental, and writes require the
            # vss extension loaded in every modifying connection.

        finally:
            rw.close()

    def write_chunks(self, chunks: list[dict[str, Any]]) -> int:
        """
        Write chunks via COPY FROM (fast bulk insert).

        Each chunk dict must have:
            id, doc_id, source_uri, body, chunk_index

        Optional:
            title, entity_ids (list), sensitivity, source_mtime, embedded_at

        Returns count of chunks written.
        """
        if not chunks:
            return 0

        rw = self._open_rw()
        try:
            rows = [
                {
                    "id": c["id"],
                    "doc_id": c["doc_id"],
                    "source_uri": c["source_uri"],
                    "title": c.get("title"),
                    "body": c["body"],
                    "chunk_index": c["chunk_index"],
                    "entity_ids": json.dumps(c.get("entity_ids", [])),
                    "embedding": c.get("embedding"),
                    "sensitivity": c.get("sensitivity", "public"),
                    "created_at": datetime.now(timezone.utc),
                    "source_mtime": c.get("source_mtime"),
                    # Stamp embedded_at whenever an embedding is present so
                    # get_stats() reflects embedding coverage accurately.
                    "embedded_at": c.get("embedded_at")
                    or (datetime.now(timezone.utc) if c.get("embedding") is not None else None),
                }
                for c in chunks
            ]
            self._copy_rows_to_chunk_table(rw, rows)

            # Rebuild FTS after batch insert (FTS doesn't auto-update)
            rw.execute("""
                PRAGMA create_fts_index(
                    'chunk', 'id',
                    'body', 'title',
                    stemmer='porter',
                    stopwords='english',
                    overwrite=1
                );
            """)

            return len(chunks)

        finally:
            rw.close()

    def delete_chunks_by_doc_id(self, doc_id: str) -> int:
        """
        Delete all chunks for a document (for re-embed workflow).

        Returns count of chunks deleted.
        """
        rw = self._open_rw()
        try:
            result = rw.execute("SELECT count(*) FROM chunk WHERE doc_id = ?", [doc_id]).fetchone()
            count = result[0] if result else 0

            rw.execute("DELETE FROM chunk WHERE doc_id = ?", [doc_id])

            # Rebuild HNSW after delete (HNSW marks deleted rows, doesn't remove)
            # For simplicity: detach and re-attach to force index refresh
            # In production at scale, use PRAGMA hnsw_compact_index()

            return count

        finally:
            rw.close()

    def _copy_rows_to_chunk_table(
        self,
        rw: duckdb.DuckDBPyConnection,
        rows: list[dict[str, Any]],
    ) -> None:
        """
        Write rows to chunk table via Parquet COPY (shared by write_chunks and upsert).

        Deduplicates structural duplication detected by codetopo.
        """
        import tempfile

        import pyarrow as pa
        import pyarrow.parquet as pq

        table = pa.Table.from_pylist(rows)
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as f:
            pq.write_table(table, f.name)
            rw.execute("INSERT INTO chunk BY NAME SELECT * FROM read_parquet(?)", [f.name])
            Path(f.name).unlink()

    def upsert_chunk_with_embedding(
        self,
        chunk_id: str,
        doc_id: str,
        source_uri: str,
        body: str,
        chunk_index: int,
        embedding: list[float],
        title: Optional[str] = None,
        entity_ids: Optional[list[str]] = None,
        sensitivity: str = "public",
        source_mtime: Optional[datetime] = None,
    ) -> None:
        """
        Upsert a single chunk with its embedding.

        For re-embed: use delete_chunks_by_doc_id first, then this for INSERT.
        (HNSW blocks UPDATE, so DELETE + INSERT is the required pattern)
        """
        rw = self._open_rw()
        try:
            rw.execute("DELETE FROM chunk WHERE id = ?", [chunk_id])

            row = {
                "id": chunk_id,
                "doc_id": doc_id,
                "source_uri": source_uri,
                "title": title,
                "body": body,
                "chunk_index": chunk_index,
                "entity_ids": json.dumps(entity_ids or []),
                "sensitivity": sensitivity,
                "created_at": datetime.now(timezone.utc),
                "source_mtime": source_mtime,
                "embedded_at": datetime.now(timezone.utc),
                "embedding": embedding,
            }
            self._copy_rows_to_chunk_table(rw, [row])

        finally:
            rw.close()

    def search_hybrid(
        self,
        query: str,
        query_embedding: Optional[list[float]] = None,
        sensitivity_filter: Optional[list[str]] = None,
        limit: int = 12,
    ) -> list[dict[str, Any]]:
        """
        Hybrid search: BM25 + HNSW + RRF fusion.

        Args:
            query: text query for BM25
            query_embedding: vector embedding for ANN (if None, BM25 only)
            sensitivity_filter: list of sensitivity levels to include
            limit: max results

        Returns:
            list of dicts with {id, body, title, source_uri, rrf_score}
        """
        filters = sensitivity_filter or ["public"]

        # BM25 via persistent read-only handle
        ro = self._open_ro()
        filter_sql = ", ".join("?" for _ in filters)
        bm25_results = ro.execute(
            f"""
            WITH bm25 AS (
                SELECT
                    id,
                    ROW_NUMBER() OVER (ORDER BY score DESC) AS rank
                FROM (
                    SELECT
                        chunk.id,
                        fts_main_chunk.match_bm25(id, ?) AS score
                    FROM chunk
                    WHERE sensitivity IN ({filter_sql})
                ) t
                WHERE score IS NOT NULL
                    ORDER BY score DESC
                    LIMIT 50
            )
            SELECT id, rank FROM bm25 ORDER BY rank;
        """,
            [query, *filters],
        ).fetchall()

        if query_embedding is None:
            # BM25-only fallback
            ids = [r[0] for r in bm25_results[:limit]]
            if not ids:
                return []
            rows = self._fetch_chunks_by_ids(ro, ids)
            return [
                {
                    "id": r[0],
                    "body": r[1],
                    "title": r[2],
                    "source_uri": r[3],
                    "doc_id": r[4],
                    "rrf_score": 1.0 / (60 + rank),
                }
                for rank, r in enumerate(rows, 1)
            ]

        # ANN via in-memory handle (HNSW). Cast the query vector to FLOAT[dim]
        # to match the column type — a Python list binds as DOUBLE[] otherwise
        # and array_cosine_distance has no FLOAT[]/DOUBLE[] overload.
        mem = self._open_mem()
        cast = f"CAST(? AS FLOAT[{self.embedding_dim}])"
        ann_results = mem.execute(
            f"""
            SELECT id, ROW_NUMBER() OVER (ORDER BY array_cosine_distance(embedding, {cast})) AS rank
            FROM chunk_vec
            ORDER BY array_cosine_distance(embedding, {cast})
            LIMIT 50;
        """,
            [query_embedding, query_embedding],
        ).fetchall()

        # RRF fusion in Python
        bm25_map = {id_: rank for id_, rank in bm25_results}
        ann_map = {id_: rank for id_, rank in ann_results}

        all_ids = set(bm25_map.keys()) | set(ann_map.keys())
        rrf_scores = []
        for id_ in all_ids:
            bm25_rank = bm25_map.get(id_, 0)
            ann_rank = ann_map.get(id_, 0)
            rrf = (1.0 / (RRF_K + bm25_rank) if bm25_rank else 0.0) + (
                1.0 / (RRF_K + ann_rank) if ann_rank else 0.0
            )
            rrf_scores.append((id_, rrf))

        rrf_scores.sort(key=lambda x: x[1], reverse=True)
        top_ids = [id_ for id_, _ in rrf_scores[:limit]]

        if not top_ids:
            return []

        # Fetch full chunk data via persistent handle
        rows = self._fetch_chunks_by_ids(ro, top_ids)

        score_map = dict(rrf_scores)
        return [
            {
                "id": r[0],
                "body": r[1],
                "title": r[2],
                "source_uri": r[3],
                "doc_id": r[4],
                "rrf_score": score_map[r[0]],
            }
            for r in rows
        ]

    @staticmethod
    def _fetch_chunks_by_ids(
        conn: duckdb.DuckDBPyConnection, ids: list[str]
    ) -> list[tuple[str, str, str, str, str]]:
        placeholders = ", ".join("?" for _ in ids)
        rows = conn.execute(
            f"""
            SELECT id, body, title, source_uri, doc_id
            FROM chunk
            WHERE id IN ({placeholders})
            """,
            ids,
        ).fetchall()
        row_by_id = {row[0]: row for row in rows}
        return [row_by_id[id_] for id_ in ids if id_ in row_by_id]

    def get_chunk_by_id(self, chunk_id: str) -> Optional[dict[str, Any]]:
        """Get a single chunk by ID."""
        ro = self._open_ro()
        row = ro.execute(
            "SELECT id, doc_id, source_uri, title, body, chunk_index, entity_ids, sensitivity, embedded_at FROM chunk WHERE id = ?",
            [chunk_id],
        ).fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "doc_id": row[1],
            "source_uri": row[2],
            "title": row[3],
            "body": row[4],
            "chunk_index": row[5],
            "entity_ids": json.loads(row[6]) if row[6] else [],
            "sensitivity": row[7],
            "embedded_at": row[8],
        }

    def get_stats(self) -> dict[str, Any]:
        """Return chunk store stats for health checks."""
        ro = self._open_ro()
        try:
            total = ro.execute("SELECT count(*) FROM chunk").fetchone()[0]
            embedded = ro.execute(
                "SELECT count(*) FROM chunk WHERE embedded_at IS NOT NULL"
            ).fetchone()[0]
            sensitivity_counts = dict(
                ro.execute("""
                SELECT sensitivity, count(*) FROM chunk GROUP BY sensitivity
            """).fetchall()
            )
            return {
                "total_chunks": total,
                "embedded_chunks": embedded,
                "unembedded_chunks": total - embedded,
                "sensitivity_counts": sensitivity_counts,
                "db_path": str(self.db_path),
                "read_only": self.read_only,
            }
        finally:
            ro.close()
            self._ro = None

    def close(self) -> None:
        """Close all handles."""
        if self._ro:
            self._ro.close()
            self._ro = None
        if self._mem:
            self._mem.close()
            self._mem = None

    def backup(self, backup_path: Optional[str] = None) -> Path:
        """Create a timestamped backup of the DuckDB file."""
        if backup_path:
            dest = Path(backup_path)
        else:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
            dest = self.db_path.with_suffix(f".duckdb.bak.{stamp}")
        shutil.copy2(self.db_path, dest)
        return dest

    def compact_hnsw(self) -> None:
        """Compact HNSW index to reclaim space after deletes."""
        rw = self._open_rw()
        try:
            rw.execute("PRAGMA hnsw_compact_index('chunk_embedding_hnsw');")
        finally:
            rw.close()


def chunk_id_from_uri(uri: str, position: int) -> str:
    """
    Generate deterministic UUID5 chunk ID from source URI + position.

    Ensures same chunk content always gets same ID (idempotent upsert).
    """
    namespace = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
    return str(uuid.uuid5(namespace, f"{uri}:{position}"))
