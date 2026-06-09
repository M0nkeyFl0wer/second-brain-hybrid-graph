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

import re
from datetime import datetime, timezone
from typing import Callable, Optional

from second_brain.chunk_store import ChunkStore, chunk_id_from_uri
from second_brain.obsidian import chunk_text

# Surface forms shorter than this are skipped when linking entities to chunks —
# 1-2 char tokens (initials, stray letters) produce too many spurious matches.
MIN_SURFACE_LEN = 3

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


def _surface_forms(entity: dict, min_len: int = MIN_SURFACE_LEN) -> set[str]:
    """All distinct surface forms for an entity (canonical label + aliases)."""
    forms = [entity.get("label") or "", *(entity.get("aliases") or [])]
    return {f.strip() for f in forms if len(f.strip()) >= min_len}


def _mentions(body_lower: str, surface_lower: str) -> bool:
    """Whole-word(ish) containment — guards against substring false positives
    ('AI' inside 'rain', 'cat' inside 'category')."""
    return re.search(rf"(?<!\w){re.escape(surface_lower)}(?!\w)", body_lower) is not None


def link_entities_to_chunks(
    store: ChunkStore,
    entities: list[dict],
    *,
    min_surface_len: int = MIN_SURFACE_LEN,
) -> int:
    """Attach entity IDs to the chunks that mention them.

    Run AFTER entity resolution / bulk load so the IDs written are the final
    canonical IDs. For each entity, its surface forms (canonical label + merged
    aliases) are matched against the bodies of the chunks belonging to that
    entity's source documents; a match links the entity's id onto that chunk.

    This is what turns a passage hit into a graph pivot: a chunk returned by
    retrieval now carries the canonical entities to expand in the graph.

    Returns the total number of (chunk, entity) links written.
    """
    # entity surface forms grouped by the documents they came from
    by_doc: dict[str, list[tuple[str, set[str]]]] = {}
    for entity in entities:
        eid = entity.get("id")
        if not eid:
            continue
        surfaces = {s.lower() for s in _surface_forms(entity, min_surface_len)}
        if not surfaces:
            continue
        doc_ids = entity.get("doc_ids") or ([entity.get("doc_id")] if entity.get("doc_id") else [])
        for doc_id in doc_ids:
            if doc_id:
                by_doc.setdefault(doc_id, []).append((eid, surfaces))
    if not by_doc:
        return 0

    rows = store.fetch_chunks_for_docs(list(by_doc))
    chunks_by_doc: dict[str, list[tuple[str, str]]] = {}
    for r in rows:
        chunks_by_doc.setdefault(r["doc_id"], []).append((r["id"], (r["body"] or "").lower()))

    links: dict[str, set[str]] = {}
    for doc_id, ent_forms in by_doc.items():
        for chunk_id, body_lower in chunks_by_doc.get(doc_id, []):
            for eid, surfaces in ent_forms:
                if any(_mentions(body_lower, s) for s in surfaces):
                    links.setdefault(chunk_id, set()).add(eid)

    if not links:
        return 0
    store.set_entity_ids({cid: sorted(ids) for cid, ids in links.items()})
    return sum(len(ids) for ids in links.values())
