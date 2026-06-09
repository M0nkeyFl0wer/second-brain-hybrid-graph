"""Document → DuckDB chunk-store ingestion.

The graph (LadybugDB) stores typed entities, edges, and *entity* embeddings.
This module stores *document chunks* — overlapping text windows plus their
embeddings — in the DuckDB chunk store, which is the substrate for chunk-level
hybrid retrieval (BM25 + HNSW + RRF). It is the bridge that makes the "hybrid"
half of the stack real during core ingest, not just an experimental side path.

Embedding is best-effort: if the embed backend is unreachable, chunks are still
written with NULL embeddings so they remain BM25-searchable. A 0-embedding
chunk store still answers keyword queries; it just can't do ANN until re-embed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, Optional

from second_brain.chunk_store import ChunkStore, chunk_id_from_uri
from second_brain.obsidian import chunk_text

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_OVERLAP = 200

# An embed function maps a batch of strings to a list of vectors, one per input.
EmbedBatchFn = Callable[[list[str]], list[list[float]]]


def chunk_document(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[str]:
    """Split text into overlapping chunks for embedding/retrieval.

    Thin guard over the canonical ``obsidian.chunk_text`` sliding window so
    there is a single chunking implementation. Overlap preserves context across
    chunk boundaries; returns [] for empty/whitespace-only input.
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    return chunk_text(text, chunk_size=chunk_size, overlap=overlap)


def ingest_document_chunks(
    store: ChunkStore,
    *,
    doc_id: str,
    source_uri: str,
    title: Optional[str],
    text: str,
    embed_batch_fn: EmbedBatchFn,
    sensitivity: str = "public",
    source_mtime: Optional[datetime] = None,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> int:
    """Chunk a document, embed the chunks, and write them to the chunk store.

    Idempotent per document: any existing chunks for ``doc_id`` are deleted
    first, so a re-ingest replaces rather than duplicates. Returns the number
    of chunks written (0 if the document is empty).

    Embedding is best-effort — if ``embed_batch_fn`` raises (backend down),
    chunks are written with NULL embeddings so they stay BM25-searchable.
    """
    bodies = chunk_document(text, chunk_size=chunk_size, overlap=overlap)
    if not bodies:
        # Still clear stale chunks for a now-empty document.
        store.delete_chunks_by_doc_id(doc_id)
        return 0

    embeddings: list[Optional[list[float]]]
    try:
        embeddings = list(embed_batch_fn(bodies))
        if len(embeddings) != len(bodies):
            # Partial/garbled result — drop embeddings rather than misalign them.
            embeddings = [None] * len(bodies)
    except Exception:
        embeddings = [None] * len(bodies)

    now = datetime.now(timezone.utc)
    rows = [
        {
            "id": chunk_id_from_uri(source_uri, i),
            "doc_id": doc_id,
            "source_uri": source_uri,
            "title": title,
            "body": body,
            "chunk_index": i,
            "entity_ids": [],
            "embedding": embeddings[i],
            "sensitivity": sensitivity,
            "source_mtime": source_mtime,
            "embedded_at": now if embeddings[i] is not None else None,
        }
        for i, body in enumerate(bodies)
    ]

    # Replace-by-doc for idempotency, then bulk write.
    store.delete_chunks_by_doc_id(doc_id)
    return store.write_chunks(rows)
