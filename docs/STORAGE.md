# Storage substrates — why DuckDB + LadybugDB, and when to deviate

This project is opinionated: the default stack is **DuckDB** (chunks,
embeddings, full-text) + **LadybugDB** (the typed-edge graph). Both are
**embedded, single-file, zero-daemon** databases. You can run the whole
hybrid graph-RAG on a laptop with nothing listening on a port.

That choice is deliberate. This doc explains why it's the default, when you'd
reach for Postgres or SQLite instead, and how to use the Postgres variant.

## The split

| Layer | Substrate | Holds |
|---|---|---|
| Columnar source-of-truth | **DuckDB** | chunks, embeddings (HNSW/vss), full-text (BM25), hybrid retrieval (RRF) |
| Typed-edge graph | **LadybugDB** | entities, relationships, multi-hop traversal, topology |

The graph references chunks/entities by id; the columnar store holds the bulk
text and vectors. Retrieval fuses both: vector + FTS from DuckDB, structural
traversal from LadybugDB.

## Why DuckDB is the default (not SQLite, not Postgres)

A RAG chunk store is an **analytical** workload: scan thousands of vectors for
similarity, BM25 over a full-text index, aggregate and rank. That's what
columnar engines are built for.

- **vs SQLite** — SQLite is row-oriented and ubiquitous, but a vector/FTS scan
  over a chunk corpus is exactly the analytical pattern it's *weakest* at. You
  also need extensions (sqlite-vec) bolted on for vectors. DuckDB ships
  first-class `vss` (HNSW) and `fts` (BM25) and is columnar, so the scans are
  fast natively. Same single-file embeddability, better fit for the job.
- **vs Postgres** — Postgres is excellent but it's a **server**: a daemon to
  run, a port to bind, a role/auth model, a process to supervise. That breaks
  the "truly local, embedded, self-hostable on a laptop" promise. You take on
  operational weight you don't need for a single-user knowledge graph.
- **DuckDB is the sweet spot** — embedded and single-file like SQLite, but with
  the columnar + native-vector + native-FTS performance the workload actually
  needs. Pairs naturally with LadybugDB (also embedded single-file). Two files,
  zero daemons.

## When Postgres becomes necessary

Switch the columnar layer to Postgres when you outgrow single-process embedded:

1. **Concurrent multi-writer.** DuckDB and LadybugDB are single-writer. If
   several processes (a daemon, an enricher, an API, a scheduled job) all need
   to *write* the chunk store at once, you want Postgres's MVCC. Embedded DBs
   force you to serialize writes through one process (the "single short-lived
   writer" pattern) — fine for personal use, friction at scale.
2. **Multi-tenant.** One Postgres instance cleanly hosts many isolated
   knowledge graphs (separate roles/databases). Embedded files don't share.
3. **A server you already run.** If Postgres is already in your stack, reusing
   it beats adding two embedded files.
4. **Operational tooling.** `EXPLAIN ANALYZE`, `pg_stat_statements`, connection
   pooling, decades of battle-testing — worth it under real production load.
5. **Working set beyond one machine's comfort.** Embedded is happiest when the
   hot data fits one box.

If none of these apply — i.e. it's *your* second brain on *your* machine — the
embedded default is the right call. Don't take on a database server you'll
spend evenings babysitting.

## The Postgres variant (branched option)

A Postgres-backed configuration of this exact pipeline exists — Postgres 17 +
pgvector (HNSW, binary-quantized for >2000-dim) + tsvector (FTS), with
LadybugDB still the graph layer. It's the substrate the maintainer's
multi-tenant production stack runs on (six concurrent producers, several
isolated tenants — case 1 + 2 above).

It lives on a **branch / variant**, not `main`, precisely because it's the
deviation, not the default:

```
# (planned) the pg variant
git checkout variant/postgres-substrate
# ChunkStore → PostgresChunkStore; same retrieval interface, server-backed
```

The retrieval interface (`ChunkStore`) is the seam: the hybrid CTE, RRF fusion,
and the LadybugDB graph layer are substrate-agnostic. Swapping DuckDB ↔
Postgres is a backend change behind that interface, not a rewrite.

## SQLite — when you'd still pick it

One case: you need maximum portability/ubiquity and your corpus is small enough
that analytical performance doesn't matter (a few hundred chunks). SQLite is
everywhere and needs nothing. But for anything that grows, DuckDB gives you the
same embeddability with a query engine suited to vector + FTS work, so it's the
better default even at the small end.

## Summary

| Situation | Use |
|---|---|
| Personal / single-user / laptop / self-hosted | **DuckDB + LadybugDB** (default) |
| Many concurrent writers, multi-tenant, server already present | **Postgres + LadybugDB** (`variant/postgres-substrate`) |
| Tiny corpus, maximum ubiquity, perf irrelevant | SQLite (possible, rarely worth it over DuckDB) |

Default to embedded. Reach for the server only when a concrete one of the
five Postgres triggers actually bites.
