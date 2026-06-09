<img src="static/logo.png" alt="Second Brain — Hybrid Graph" width="400">

# Second Brain — Hybrid Graph

My homelab stack for a **hybrid graph-RAG second brain**: the personal attempts
at each stage of moving notes from *flat vector search* to *graph traversal* —
where a query doesn't just return the nearest chunks, it walks the typed
relationships between the ideas behind them.

It is **local-first and zero-daemon**. Two embedded databases do the work:

- **DuckDB** — chunks, embeddings, and full-text search (BM25 + HNSW, fused with
  Reciprocal Rank Fusion). The retrieval substrate.
- **LadybugDB** — the typed-edge graph: entities and the evidence-bearing
  relationships between them. The traversal substrate.

Plus **Ollama** (local extraction + embeddings) and **NetworkX / Ripser** (graph
analysis). No server to run, no cloud, no API keys required.

> This is a personal stack shared in the open, not a product. It is shown as a
> **pipeline with feedback loops** — additions, pruning, pathfinding, and
> enrichment — so you can take the stage you need and leave the rest. Some
> stages run flawlessly today; some are works in progress. The
> [Pipeline maturity](#pipeline-maturity) table is honest about which is which.

---

## The pipeline

```
        ┌─────────────────────────────────────────────────────────────┐
        │                                                             ▼
   sources ──▶ chunk ──▶ embed ──▶ extract triplets ──▶ typed graph ──▶ query / traverse / visualize
   (vault,     (DuckDB)  (Ollama)  (entities + edges,    (LadybugDB)    (vector · keyword · hybrid · path)
    folder)                         evidence-bearing)         │
        ▲                                                     │
        │            feedback loops                           │
        └──── enrichment ◀── pruning ◀── pathfinding ◀────────┘
              (grow it)     (clean it)   (connect it)
```

- **Additions** — ingest a vault, a folder, or nothing; new content flows in.
- **Pathfinding** — find how two ideas connect across the graph, not just whether
  they're similar.
- **Pruning** — clean a live graph by *reconstruct-and-swap*: build a filtered
  copy, verify it on disk, then swap it in behind a backup
  (`scripts/apply_resolution.py`, `scripts/prune_junk_entities.py`). A
  deliberately conservative default for irreversible bulk mutation.
- **Enrichment** — scheduled passes that re-read recent notes and grow the graph.

---

## Pipeline maturity

A tighter core that definitely works shares better than a broad stack that
half-works. The **core** below is import-clean and schema-coherent; the
**experimental** stages are real but still being reconciled (and some need a
non-trivial local LLM run to exercise).

| Stage | Entry point | Status |
|---|---|---|
| **Ingest** (vault / folder) | `scripts/ingest_obsidian.py`, `scripts/ingest_folder.py` | ✅ core |
| **Typed graph** (LadybugDB) | `second_brain/graph.py` | ✅ core |
| **Inspect** | `python -m second_brain.check` | ✅ core |
| **Search** (vector / keyword / hybrid / path / chunks) | `scripts/search_cli.py` | ✅ core |
| **Chunk store** (DuckDB: BM25 + HNSW + RRF) | `second_brain/chunk_store.py`, `second_brain/pipeline/chunks.py` | ✅ core |
| **Topology analysis** | `scripts/run_analysis.py`, `second_brain/topology.py` | ✅ core |
| **Visualize** (NetworkX → pyvis + homology) | `scripts/visualize.py` | ✅ core |
| **Pluggable ontology** (YAML) | `--ontology path.yaml` | ✅ core |
| **Pathfinding** module | `second_brain/path_finder.py` | 🧪 experimental |
| **Enrichment loop** (DuckDB-hybrid, scheduled) | `scripts/enrich.py` | 🧪 experimental¹ |
| **Health/ops monitoring** | `scripts/health_check.py` | 🧪 experimental¹ |
| **Daily briefing / reflection** | `scripts/daily_briefing.py` | 🧪 experimental |
| **MCP server** (AI assistants) | `second_brain/mcp_server.py` | 🧪 experimental |
| **Web dashboard** | `second_brain/dashboard.py` | 🧪 experimental |

¹ **The DuckDB chunk store is now populated by core ingest.** Both ingest paths
chunk each document, embed the chunks (best-effort — chunks still land
BM25-searchable if the embed backend is down), and write them to
`data/chunks.duckdb`. Query it with `search_cli.py --mode chunks` for
passage-level hybrid retrieval (BM25 + HNSW + RRF fusion) — this is the
substrate a RAG answer grounds in. So **the graph holds entities, edges, and
*entity* embeddings in LadybugDB; the chunk store holds the source *passages*
and their embeddings.** What remains experimental is the *scheduled enrichment
loop* (`enrich.py` — periodic re-reads / re-embeds over time), not the chunk
substrate itself.

---

## Quick start

```bash
git clone https://github.com/M0nkeyFl0wer/second-brain-hybrid-graph.git
cd second-brain-hybrid-graph
bash setup.sh            # venv + deps (from requirements.txt) + Ollama models
```

Then run the bundled demo corpus end to end:

```bash
# Ingest 36 demo docs with a custom ontology
python scripts/ingest_obsidian.py \
    --vault examples/good-dog-corpus/vault \
    --ontology examples/good-dog-corpus/ontology.yaml

python -m second_brain.check                 # inspect the graph
python scripts/search_cli.py -q 'your query' # vector / keyword / hybrid / path
python scripts/visualize.py                  # interactive HTML + H0/H1 homology
```

> Ingestion runs a local LLM per note, so a cold first run takes minutes, not
> seconds. That's the cost of keeping everything local and key-free.

Point it at **your own** content instead:

```bash
python scripts/ingest_folder.py              # a folder of documents
python scripts/ingest_obsidian.py --vault /path/to/vault
```

---

## Custom ontology — not hardcoded

The ontology (what entity and edge types exist) is a **loadable YAML config**,
defaulting to a built-in second-brain ontology. Point any ingest at your own:

```bash
python scripts/ingest_obsidian.py --vault ./notes --ontology ./my-ontology.yaml
```

```yaml
# my-ontology.yaml
entity_types: [concept, person, source, project, insight, question]
edge_types:
  LEARNED_FROM:   { direction: "concept -> source" }
  CONFLICTS_WITH: { direction: "*" }      # any -> any
  SUPPORTS:       { direction: "*" }
```

A tailored ontology drives extraction (the LLM is told your types) and validates
every edge against domain/range. See [ONTOLOGY.md](ONTOLOGY.md) and the worked
example in [`examples/good-dog-corpus/`](examples/good-dog-corpus/).

That domain/range validation is a **precision/recall dial**. The strict
good-dog ontology rejects ~75–80% of LLM-proposed edges (the ones whose
endpoints violate a declared type) — a deliberately sparse, high-confidence
graph, not a broken one. The built-in default sits looser. The tradeoff, the
measured attrition, and how to dial toward density are written up in
[`examples/good-dog-corpus/ONTOLOGY.md` §8](examples/good-dog-corpus/ONTOLOGY.md#8-precision-vs-recall-the-domainrange-tradeoff-why-the-built-graph-is-sparse).

---

## Storage: why DuckDB + LadybugDB

Embedded, columnar, zero-daemon, local-first — the chunk/retrieval workload
fits DuckDB, the typed-edge/traversal workload fits LadybugDB, and neither needs
a running server. **Postgres is the documented escape hatch** for when you
outgrow embedded (multi-writer, multi-tenant, network-shared). The full
rationale, the five triggers that mean "switch to Postgres," and a planned
`variant/postgres-substrate` branch are in **[docs/STORAGE.md](docs/STORAGE.md)**.

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) for local extraction + embeddings
  (`nomic-embed-text`, `llama3.2:3b` — both small)
- Everything else installs via `requirements.txt` (`setup.sh` handles it)

---

## License & contact

MIT — see [LICENSE](LICENSE). Tools don't own what you build with them.

Feedback and contributions welcome. Open an issue or PR.
