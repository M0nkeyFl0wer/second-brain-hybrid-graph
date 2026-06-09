#!/usr/bin/env python3
"""
Ingest documents from the ingest/ folder into the knowledge graph.
Supports: .txt, .md, .pdf, .html
Uses COPY FROM Parquet for bulk entity loading.
"""

import sys
import hashlib
import time
from pathlib import Path

sys.path.insert(0, ".")

from second_brain.graph import Graph
from second_brain.extract import Extractor
from second_brain.embed import embed_text, embed_batch
from second_brain.ontology import Ontology
from second_brain.chunk_store import ChunkStore
from second_brain.pipeline.chunks import ingest_document_chunks
from second_brain.pipeline.resolve import canonicalize_extracted_graph
from second_brain import config


def _entity_document_mentions(entities: list[dict]) -> list[dict]:
    mentions = []
    for entity in entities:
        doc_ids = entity.get("doc_ids") or ([entity.get("doc_id")] if entity.get("doc_id") else [])
        for doc_id in doc_ids:
            mentions.append(
                {
                    "entity_id": entity["id"],
                    "doc_id": doc_id,
                    "confidence": entity.get("confidence", 0.8),
                    "source_url": entity.get("source_url", ""),
                    "provenance": entity.get("provenance", "document_mention"),
                }
            )
    return mentions


def read_document(path: Path) -> str:
    """Read document content. Handles txt, md, html. PDF needs pdftotext."""
    suffix = path.suffix.lower()

    if suffix in (".txt", ".md"):
        return path.read_text(errors="replace")

    if suffix == ".html":
        try:
            from html.parser import HTMLParser

            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []

                def handle_data(self, data):
                    self.text.append(data)

            parser = TextExtractor()
            parser.feed(path.read_text(errors="replace"))
            return " ".join(parser.text)
        except Exception:
            return path.read_text(errors="replace")

    if suffix == ".pdf":
        try:
            import subprocess

            result = subprocess.run(
                ["pdftotext", str(path), "-"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.stdout
        except FileNotFoundError:
            print("  Warning: pdftotext not found. Install: sudo apt install poppler-utils")
            return ""
        except Exception as e:
            print(f"  Warning: Could not read PDF {path.name}: {e}")
            return ""

    print(f"  Skipping unsupported format: {path.name}")
    return ""


def main():
    ingest_dir = getattr(config, "INGEST_DIR", __import__("pathlib").Path("ingest"))
    if not ingest_dir.exists():
        ingest_dir.mkdir(parents=True)
        print(f"Created ingest directory: {ingest_dir}/")
        print("Add documents there and run again.")
        return

    files = list(ingest_dir.iterdir())
    supported = [
        f for f in files if f.is_file() and f.suffix.lower() in (".txt", ".md", ".pdf", ".html")
    ]

    if not supported:
        print(f"No supported documents in {ingest_dir}/")
        print("Supported formats: .txt, .md, .pdf, .html")
        return

    print(f"Found {len(supported)} documents to ingest.\n")

    ontology = Ontology()
    graph = Graph(ontology=ontology)
    chunk_store = ChunkStore(config.CHUNK_STORE_PATH, embedding_dim=config.EMBEDDING_DIM)
    chunk_store.init_schema()
    try:
        extractor = Extractor(ontology)

        all_entities = []
        all_edges = []
        total_chunks = 0
        t_start = time.time()

        for i, filepath in enumerate(supported, 1):
            print(f"[{i}/{len(supported)}] {filepath.name}")

            text = read_document(filepath)
            if not text.strip():
                print("  Empty or unreadable, skipping.")
                continue

            doc_id = hashlib.sha256(str(filepath).encode()).hexdigest()[:16]
            source_url = str(filepath)

            # Register document
            graph.add_document(doc_id, str(filepath), filepath.stem)

            # Extract entities and relationships
            result = extractor.extract_from_text(text, source_url=source_url, doc_id=doc_id)
            print(
                f"  Extracted: {len(result['entities'])} entities, " f"{len(result['edges'])} edges"
            )

            # Chunk the document into the DuckDB chunk store for hybrid
            # (BM25 + HNSW) retrieval. Best-effort embedding — chunks still
            # land (BM25-searchable) if the embed backend is down.
            written = ingest_document_chunks(
                chunk_store,
                doc_id=doc_id,
                source_uri=source_url,
                title=filepath.stem,
                text=text,
                embed_batch_fn=embed_batch,
            )
            total_chunks += written
            if written:
                print(f"  Chunked: {written} chunks → chunk store")

            all_entities.extend(result["entities"])
            all_edges.extend(result["edges"])

        # Resolve aliases before writing so duplicate labels converge onto one
        # canonical entity ID in this ingest batch.
        all_entities, all_edges, resolution = canonicalize_extracted_graph(all_entities, all_edges)
        if resolution.merged_count:
            print(f"Resolved entity aliases: {resolution.merged_count} labels folded.")

        # Bulk load entities
        if all_entities:
            print(f"\nBulk loading {len(all_entities)} entities...")
            loaded = graph.bulk_add_entities(all_entities)
            print(f"  Loaded: {loaded}")

            mentions = _entity_document_mentions(all_entities)
            mentioned = graph.bulk_add_mentions(mentions)
            print(f"  Document mentions: {mentioned}")

            # Embed entity descriptions and store vectors
            print("Computing entity embeddings...")
            for entity in all_entities:
                embed_text_str = f"{entity['label']}: {entity.get('description', '')}"
                try:
                    emb = embed_text(embed_text_str)
                    graph.set_embedding(entity["id"], emb)
                except Exception as e:
                    print(f"  Embedding failed for {entity['label']}: {e}")
        else:
            print("\nNo entities extracted.")

        if all_edges:
            print(f"Loading {len(all_edges)} edges...")
            loaded = graph.bulk_add_edges(all_edges)
            print(f"  Loaded: {loaded}")

        # Rebuild HNSW vector indexes after bulk loading
        print("Rebuilding vector indexes...")
        graph.rebuild_vector_indexes()

        # Summary
        elapsed = time.time() - t_start
        print(f"\n{'=' * 50}")
        print(f"Ingestion complete in {elapsed:.1f}s.")
        print(f"  Documents processed: {len(supported)}")
        print(f"  Chunks embedded:     {total_chunks}")
        print(f"  Total entities:      {graph.entity_count()}")
        print(f"  Total edges:         {graph.edge_count()}")
        print(f"  Total documents:     {graph.document_count()}")
        print("\nNext steps:")
        print("  Search:    python scripts/search_cli.py -q 'your query'")
        print("  Analyze:   python scripts/run_analysis.py")
        print("  Briefing:  python scripts/daily_briefing.py")

        # Show ontology rejections
        rejections = ontology.get_rejection_counts()
        if rejections:
            print("\nOntology rejections (types not in ONTOLOGY.md):")
            for type_name, count in list(rejections.items())[:10]:
                print(f"  {type_name}: {count} rejections")
            print("  Tip: Consider adding frequently rejected types to ONTOLOGY.md")

        chunk_stats = chunk_store.get_stats()
        print(
            f"  Chunk store:         {chunk_stats['total_chunks']} chunks "
            f"({chunk_stats['embedded_chunks']} embedded) → {config.CHUNK_STORE_PATH.name}"
        )
    finally:
        graph.close()
        chunk_store.close()


if __name__ == "__main__":
    main()
