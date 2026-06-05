"""
LadybugDB graph wrapper. Handles schema creation, entity/edge writing, and queries.
The graph is a directory on disk. No server. No configuration.

LadybugDB is a KuzuDB fork — same Cypher dialect, same embedded architecture.
Bulk ingestion uses COPY FROM Parquet (25x faster than iterative MERGE).
Vector search uses native FLOAT[768] columns + array_cosine_similarity.
"""
import logging
import time
import tempfile
from pathlib import Path

from kg_common.write.ladybug import (
    GraphWriter,
    _KG_COMMON_META_DDL,
    _acquire_writer_lock,
    _import_ladybug,
    _release_writer_lock,
)

from .ontology import Ontology
from . import config

logger = logging.getLogger(__name__)


class Graph(GraphWriter):
    """Knowledge graph backed by LadybugDB.

    Subclasses kg_common's GraphWriter to inherit the single-writer pidfile
    lock, the dual ladybug/real_ladybug import, and the KgCommonMeta stamp
    (ontology class / version / checksum + kg_common version recorded in the
    graph at write time) — while keeping open-second-brain's custom
    FLOAT[768] Entity/Chunk/CommunityMeta schema, the EdgeNode hypergraph,
    and all custom bulk/vector/query methods.

    The ABC's generic `schema_ddl()` is intentionally NOT used: `_ensure_schema`
    is overridden to run the custom DDL (`_init_schema`) and then stamp
    KgCommonMeta. We also do NOT call `super().__init__()` — the base opens the
    DB read-write unconditionally and has no read_only path — so the lock/open
    logic is replicated here via the base's own module-level helpers (lock
    semantics and dual-import stay identical to the base).
    """

    def __init__(self, graph_dir: Path = None, ontology: Ontology = None,
                 read_only: bool = False):
        # --- Public-API attributes (unchanged contract used across the repo) ---
        self.graph_dir = Path(graph_dir) if graph_dir else config.GRAPH_DIR
        self.ontology = ontology or Ontology()
        self.read_only = read_only
        self.db = None
        self.conn = None
        # SHACL-vocabulary violations accumulated by bulk writes (entities or
        # edges rejected for an out-of-ontology type). Machine-readable via
        # ValidationViolation.to_shacl_dict(). Append-only across calls; assign
        # `graph.last_violations = []` to start a fresh report.
        self.last_violations: list = []

        # --- Base-class private attrs that inherited GraphWriter methods
        # (execute / query / _stamp_meta / flush / close) read. Mirror them
        # onto the same objects as the public attrs. ---
        self._db_path = self.graph_dir
        self._ontology = self.ontology
        self._audit_log_path = None
        self._lockfile = None

        self.graph_dir.parent.mkdir(parents=True, exist_ok=True)

        if read_only:
            # No writer lock, no schema DDL, no meta stamp, no migrations.
            ldb = _import_ladybug()
            self.db = ldb.Database(str(self.graph_dir), read_only=True)
            self.conn = ldb.Connection(self.db)
            self._db = self.db
            self._conn = self.conn
            return

        # Write path: acquire the single-writer pidfile lock first (friendly
        # PID-bearing error on contention), then open read-write, run the
        # custom schema + KgCommonMeta stamp, then migrations. On any failure
        # below the lock, release the pidfile so the next attempt isn't
        # falsely blocked (mirrors the base __init__ try/except contract).
        self._lockfile = _acquire_writer_lock(self._db_path)
        try:
            ldb = _import_ladybug()
            self.db = ldb.Database(str(self.graph_dir))
            self.conn = ldb.Connection(self.db)
            self._db = self.db
            self._conn = self.conn
            self._ensure_schema()
            from .migrations import ensure_schema_version
            ensure_schema_version(self.conn)
        except Exception:
            _release_writer_lock(self._lockfile)
            self._lockfile = None
            raise

    def _ensure_schema(self) -> None:
        """Custom open-second-brain schema, then the kg-common meta stamp.

        Overrides GraphWriter._ensure_schema so we keep the FLOAT[768]
        Entity/Chunk/CommunityMeta + EdgeNode hypergraph + 5 edge tables +
        FTS index (`_init_schema`) INSTEAD of the ABC's generic `schema_ddl()`.
        We still create the KgCommonMeta table and call the inherited
        `_stamp_meta()` so the graph records which ontology version / checksum
        + kg_common version wrote it.
        """
        self._init_schema()
        try:
            self._conn.execute(_KG_COMMON_META_DDL)
        except Exception as exc:
            logger.warning("KgCommonMeta DDL failed (may pre-exist): %s", exc)
        self._stamp_meta()
        logger.info("Schema ensured (custom + KgCommonMeta) for %s", self.graph_dir)

    def _init_schema(self):
        """Create node and edge tables if they don't exist."""
        # --- Load extensions (log failures instead of silently swallowing) ---
        for ext in ("vector", "fts", "algo"):
            try:
                self.conn.execute(f"INSTALL {ext}; LOAD EXTENSION {ext};")
                logger.debug("Loaded extension: %s", ext)
            except Exception as e:
                logger.warning("Extension '%s' not available: %s", ext, e)

        # --- Core node tables ---
        self.conn.execute("""
            CREATE NODE TABLE IF NOT EXISTS Entity (
                id STRING PRIMARY KEY,
                entity_type STRING,
                label STRING,
                description STRING DEFAULT '',
                confidence DOUBLE DEFAULT 0.5,
                source_url STRING DEFAULT '',
                provenance STRING DEFAULT 'unknown',
                created_at INT64 DEFAULT 0,
                updated_at INT64 DEFAULT 0,
                embedding FLOAT[768],
                layer STRING DEFAULT 'domain'
            )
        """)

        self.conn.execute("""
            CREATE NODE TABLE IF NOT EXISTS Document (
                id STRING PRIMARY KEY,
                path STRING,
                title STRING DEFAULT '',
                ingested_at INT64 DEFAULT 0,
                chunk_count INT32 DEFAULT 0
            )
        """)

        self.conn.execute("""
            CREATE NODE TABLE IF NOT EXISTS Chunk (
                id STRING PRIMARY KEY,
                doc_id STRING,
                text STRING,
                chunk_index INT32 DEFAULT 0,
                created_at INT64 DEFAULT 0,
                embedding FLOAT[768]
            )
        """)

        # --- Semantic Spacetime: edge-nodes for hypergraph support ---
        self.conn.execute("""
            CREATE NODE TABLE IF NOT EXISTS EdgeNode (
                id STRING PRIMARY KEY,
                semantic_type STRING,
                label STRING DEFAULT '',
                weight DOUBLE DEFAULT 1.0,
                confidence DOUBLE DEFAULT 0.5,
                provenance STRING DEFAULT 'unknown',
                created_at INT64 DEFAULT 0,
                expired_at INT64 DEFAULT 0
            )
        """)

        # --- Community summaries (pre-computed for "zoom out" queries) ---
        self.conn.execute("""
            CREATE NODE TABLE IF NOT EXISTS CommunityMeta (
                id STRING PRIMARY KEY,
                community_id INT64,
                size INT64,
                summary STRING DEFAULT '',
                top_entities STRING DEFAULT '',
                computed_at INT64 DEFAULT 0,
                embedding FLOAT[768]
            )
        """)

        # --- Core edge tables ---
        edge_defs = [
            ("MENTIONED_IN", "Entity", "Document"),
            ("CHUNK_OF", "Chunk", "Document"),
            ("RELATES_TO", "Entity", "Entity"),
            ("CONNECTS", "Entity", "EdgeNode"),
            ("BINDS", "EdgeNode", "Entity"),
        ]
        for edge_name, from_table, to_table in edge_defs:
            self.conn.execute(f"""
                CREATE REL TABLE IF NOT EXISTS {edge_name} (
                    FROM {from_table} TO {to_table},
                    edge_type STRING DEFAULT '',
                    weight DOUBLE DEFAULT 1.0,
                    confidence DOUBLE DEFAULT 0.5,
                    evidence STRING DEFAULT '',
                    source_url STRING DEFAULT '',
                    provenance STRING DEFAULT 'unknown',
                    created_at INT64 DEFAULT 0,
                    expired_at INT64 DEFAULT 0
                )
            """)

        # --- Create FTS indexes (safe to create at init) ---
        for table, index_name, cols in [
            ("Entity", "entity_fts", ["label", "description"]),
        ]:
            try:
                col_list = str(cols).replace("'", '"')
                self.conn.execute(f"""
                    CALL CREATE_FTS_INDEX('{table}', '{index_name}', {col_list})
                """)
            except Exception:
                pass  # Index already exists

        # NOTE: HNSW vector indexes are NOT created at init because they
        # block SET operations on the embedding column. Call rebuild_vector_indexes()
        # after bulk embedding operations are complete.

    # =========================================================================
    # Incremental writes (single entity/edge at a time)
    # =========================================================================

    def add_edge_node(self, edge_node_id: str, semantic_type: str,
                      label: str = "", weight: float = 1.0,
                      confidence: float = 0.5, provenance: str = "unknown",
                      participants: list[str] = None) -> bool:
        """
        Create a Semantic Spacetime edge-node and link it to participants.
        Supports hypergraphs: one edge-node can connect 3+ entities.
        """
        now = int(time.time())
        self.conn.execute("""
            MERGE (en:EdgeNode {id: $eid})
            ON CREATE SET en.semantic_type = $stype, en.label = $elabel,
                en.weight = $ew, en.confidence = $econf,
                en.provenance = $eprov, en.created_at = $enow
        """, parameters={
            "eid": edge_node_id, "stype": semantic_type, "elabel": label,
            "ew": weight, "econf": confidence,
            "eprov": provenance, "enow": now,
        })

        if participants:
            for i, entity_id in enumerate(participants):
                if i == 0:
                    # First participant: CONNECTS (source → edge-node)
                    self.conn.execute("""
                        MATCH (e:Entity {id: $src}), (en:EdgeNode {id: $enid})
                        MERGE (e)-[:CONNECTS]->(en)
                    """, parameters={"src": entity_id, "enid": edge_node_id})
                else:
                    # Remaining participants: BINDS (edge-node → target)
                    self.conn.execute("""
                        MATCH (en:EdgeNode {id: $enid}), (e:Entity {id: $tgt})
                        MERGE (en)-[:BINDS]->(e)
                    """, parameters={"enid": edge_node_id, "tgt": entity_id})
        return True

    def add_entity(self, entity_id: str, entity_type: str, label: str,
                   description: str = "", confidence: float = 0.5,
                   source_url: str = "", provenance: str = "unknown") -> bool:
        """Add an entity to the graph. Validates against ontology first."""
        if not self.ontology.validate_entity_type(entity_type):
            return False

        now = int(time.time())
        self.conn.execute("""
            MERGE (e:Entity {id: $eid})
            ON CREATE SET e.entity_type = $etype, e.label = $elabel,
                e.description = $edesc, e.confidence = $econf,
                e.source_url = $eurl, e.provenance = $eprov,
                e.created_at = $enow, e.updated_at = $enow
            ON MATCH SET e.updated_at = $enow
        """, parameters={
            "eid": entity_id, "etype": entity_type, "elabel": label,
            "edesc": description, "econf": confidence,
            "eurl": source_url, "eprov": provenance, "enow": now,
        })
        return True

    def add_edge(self, source_id: str, target_id: str, edge_type: str,
                 weight: float = 1.0, confidence: float = 0.5,
                 evidence: str = "", source_url: str = "",
                 provenance: str = "unknown") -> bool:
        """Add a typed edge between two entities.

        `evidence` is the verbatim source quote justifying the edge — the
        ontology requires it on every extracted relationship. Persisting it
        keeps edges traceable back to their text (otherwise the graph asserts
        relationships with no record of why).
        """
        if not self.ontology.validate_edge_type(edge_type):
            return False

        # Grade-locality: when both endpoint types are known, enforce the
        # ontology's domain/range. Unknown endpoints fall through to the MERGE.
        rows = self.query(
            "MATCH (e:Entity) WHERE e.id = $src OR e.id = $tgt "
            "RETURN e.id AS id, e.entity_type AS t",
            parameters={"src": source_id, "tgt": target_id},
        )
        tmap = {r["id"]: r.get("t") for r in rows}
        st, tt = tmap.get(source_id), tmap.get(target_id)
        if st is not None and tt is not None and not self.ontology.validate_grade(edge_type, st, tt):
            from .models import validation as v
            self.last_violations.append(v.grade_violation(
                v.edge_key(source_id, edge_type, target_id), edge_type, st, tt))
            return False

        self.conn.execute("""
            MATCH (a:Entity {id: $src}), (b:Entity {id: $tgt})
            MERGE (a)-[r:RELATES_TO {edge_type: $etype}]->(b)
            ON CREATE SET r.weight = $w, r.confidence = $conf,
                r.evidence = $ev, r.source_url = $url, r.provenance = $prov,
                r.created_at = $now
        """, parameters={
            "src": source_id, "tgt": target_id, "etype": edge_type,
            "w": weight, "conf": confidence, "ev": evidence,
            "url": source_url, "prov": provenance, "now": int(time.time()),
        })
        return True

    def add_document(self, doc_id: str, path: str, title: str = "") -> None:
        """Register a source document."""
        self.conn.execute("""
            MERGE (d:Document {id: $id})
            ON CREATE SET d.path = $path, d.title = $title,
                d.ingested_at = $now
        """, parameters={
            "id": doc_id, "path": path, "title": title,
            "now": int(time.time()),
        })

    # =========================================================================
    # Bulk writes (Parquet-based, 25x faster than iterative)
    # =========================================================================

    def _record_entity_violations(self, invalid: list[dict]) -> None:
        """Build + log SHACL-vocabulary violations for entities rejected on an
        out-of-ontology type. Accumulates on self.last_violations; never raises."""
        from .models import validation as v
        for e in invalid:
            viol = v.unknown_entity_type(e.get("id", ""), e.get("entity_type", ""))
            self.last_violations.append(viol)
        logger.info(
            "Rejected %d entities (type not in ontology): %s",
            len(invalid),
            [viol.to_shacl_dict() for viol in self.last_violations[-len(invalid):]],
        )

    def _record_edge_violations(self, invalid: list[dict]) -> None:
        """Build + log SHACL-vocabulary violations for edges rejected on an
        out-of-ontology type. Accumulates on self.last_violations; never raises."""
        from .models import validation as v
        for e in invalid:
            key = v.edge_key(
                e.get("source_id", ""), e.get("edge_type", ""), e.get("target_id", "")
            )
            self.last_violations.append(v.unknown_edge_type(key, e.get("edge_type", "")))
        logger.info(
            "Rejected %d edges (type not in ontology): %s",
            len(invalid),
            [viol.to_shacl_dict() for viol in self.last_violations[-len(invalid):]],
        )

    def _record_grade_violations(self, invalid: list[dict]) -> None:
        """Build + log SHACL-vocabulary violations for edges rejected on
        grade locality (endpoint types not in the ontology's EDGE_DOMAIN_RANGE).
        Each dict carries `_src_type`/`_tgt_type` set by `_grade_filter`."""
        from .models import validation as v
        for e in invalid:
            key = v.edge_key(
                e.get("source_id", ""), e.get("edge_type", ""), e.get("target_id", "")
            )
            self.last_violations.append(v.grade_violation(
                key, e.get("edge_type", ""),
                e.get("_src_type", ""), e.get("_tgt_type", ""),
            ))
        logger.info(
            "Rejected %d edges (grade locality): %s",
            len(invalid),
            [viol.to_shacl_dict() for viol in self.last_violations[-len(invalid):]],
        )

    def _grade_filter(self, edges: list[dict]) -> tuple[list[dict], list[dict]]:
        """Split `edges` by grade locality (EDGE_DOMAIN_RANGE). An edge is
        rejected only when BOTH endpoint types are known in the graph AND the
        ontology's `validate_grade` disallows the (src_type, tgt_type) pair.
        Unconstrained edge types pass automatically (validate_grade returns
        True); endpoints whose type can't be resolved (node not yet written)
        fall through to the MERGE, which no-ops on a missing endpoint."""
        type_map = {
            r["id"]: r.get("entity_type")
            for r in self.query(
                "MATCH (e:Entity) RETURN e.id AS id, e.entity_type AS entity_type"
            )
        }
        ok, bad = [], []
        for e in edges:
            st = type_map.get(e.get("source_id"))
            tt = type_map.get(e.get("target_id"))
            if (st is not None and tt is not None
                    and not self.ontology.validate_grade(e["edge_type"], st, tt)):
                bad.append({**e, "_src_type": st, "_tgt_type": tt})
            else:
                ok.append(e)
        return ok, bad

    def bulk_add_entities(self, entities: list[dict]) -> int:
        """
        Bulk-load entities via COPY FROM Parquet.
        Each dict must have: id, entity_type, label, description, confidence,
        source_url, provenance, created_at, updated_at.
        All validated against ontology before loading.
        Returns count of entities loaded (after validation filtering).
        """
        valid, invalid = [], []
        for e in entities:
            (valid if self.ontology.validate_entity_type(e["entity_type"]) else invalid).append(e)
        if invalid:
            self._record_entity_violations(invalid)

        if not valid:
            return 0

        import pandas as pd

        # Deduplicate by id — keep last occurrence (highest confidence
        # if caller sorted that way). Prevents COPY PK violations.
        seen = {}
        for e in valid:
            seen[e["id"]] = e
        valid = list(seen.values())

        df = pd.DataFrame(valid)

        # Ensure all required columns exist with defaults
        defaults = {
            "description": "", "confidence": 0.5, "source_url": "",
            "provenance": "unknown", "created_at": int(time.time()),
            "updated_at": int(time.time()),
        }
        for col, default in defaults.items():
            if col not in df.columns:
                df[col] = default

        # Select columns in schema order, include embedding as null
        cols = ["id", "entity_type", "label", "description", "confidence",
                "source_url", "provenance", "created_at", "updated_at"]
        df = df[cols]

        # Write via PyArrow to get properly-typed null embedding column
        import pyarrow as pa
        import pyarrow.parquet as pq

        # Build arrow table from the DataFrame columns
        table = pa.Table.from_pandas(df)

        # Add embedding as a fixed-size list of float32, all nulls
        emb_type = pa.list_(pa.float32(), config.EMBEDDING_DIM)
        null_embs = pa.nulls(len(df), type=emb_type)
        table = table.append_column("embedding", null_embs)

        # Add layer column (default 'domain', reserved for semantic layering)
        layer_col = pa.array(["domain"] * len(df), type=pa.string())
        table = table.append_column("layer", layer_col)

        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as f:
            pq.write_table(table, f.name)
            self.conn.execute(f"COPY Entity FROM '{f.name}'")
            Path(f.name).unlink()

        return len(valid)

    def bulk_add_edges(self, edges: list[dict]) -> int:
        """
        Load edges via parameterized MERGE (iterative, not bulk Parquet).
        COPY FROM for rel tables requires exact internal ID format, so we
        use MERGE for correctness. Each dict must have: source_id, target_id,
        edge_type. Optional: weight, confidence, evidence, source_url,
        provenance, created_at.
        All validated against ontology before loading.
        """
        valid, invalid = [], []
        for e in edges:
            (valid if self.ontology.validate_edge_type(e["edge_type"]) else invalid).append(e)
        if invalid:
            self._record_edge_violations(invalid)

        # Grade-locality enforcement (EDGE_DOMAIN_RANGE): drop edges whose
        # endpoint types the ontology disallows. No-op for unconstrained edges.
        valid, grade_invalid = self._grade_filter(valid)
        if grade_invalid:
            self._record_grade_violations(grade_invalid)

        if not valid:
            return 0

        # Edges must be inserted via MERGE (COPY FROM for rel tables
        # requires matching source/target node IDs in specific format).
        # Batch them but use parameterized MERGE for correctness.
        now = int(time.time())
        for e in valid:
            self.conn.execute("""
                MATCH (a:Entity {id: $src}), (b:Entity {id: $tgt})
                MERGE (a)-[r:RELATES_TO {edge_type: $etype}]->(b)
                ON CREATE SET r.weight = $w, r.confidence = $conf,
                    r.evidence = $ev, r.source_url = $url, r.provenance = $prov,
                    r.created_at = $now
            """, parameters={
                "src": e.get("source_id", ""),
                "tgt": e.get("target_id", ""),
                "etype": e["edge_type"],
                "w": e.get("weight", 1.0),
                "conf": e.get("confidence", 0.5),
                "ev": e.get("evidence", ""),
                "url": e.get("source_url", ""),
                "prov": e.get("provenance", "unknown"),
                "now": e.get("created_at", now),
            })

        return len(valid)

    # =========================================================================
    # Embedding storage and vector search
    # =========================================================================

    def set_embedding(self, entity_id: str, embedding: list[float]) -> None:
        """Store an embedding vector on an entity node."""
        self.conn.execute("""
            MATCH (e:Entity {id: $id})
            SET e.embedding = $emb
        """, parameters={"id": entity_id, "emb": embedding})

    def rebuild_vector_indexes(self) -> None:
        """
        (Re)build HNSW vector indexes. Call after bulk embedding operations.
        Drops existing indexes first, then recreates.
        """
        for table, index_name, col in [
            ("Entity", "entity_vec", "embedding"),
            ("CommunityMeta", "community_vec", "embedding"),
        ]:
            try:
                self.conn.execute(
                    f"CALL DROP_VECTOR_INDEX('{table}', '{index_name}')")
            except Exception:
                pass
            try:
                self.conn.execute(f"""
                    CALL CREATE_VECTOR_INDEX('{table}', '{index_name}', '{col}',
                        mu := 30, ml := 60, metric := 'cosine', efc := 200)
                """)
            except Exception:
                pass

    def vector_search(self, query_embedding: list[float],
                      limit: int = 10) -> list:
        """Find entities by vector similarity. Uses HNSW index if available, falls back to brute force."""
        # Try HNSW index first
        try:
            result = self.conn.execute("""
                CALL QUERY_VECTOR_INDEX('Entity', 'entity_vec', $qemb, $limit)
                RETURN node.id AS id, node.label AS label,
                       node.entity_type AS type, distance AS score
            """, parameters={"qemb": query_embedding, "limit": limit})
            columns = result.get_column_names()
            rows = []
            while result.has_next():
                row = result.get_next()
                rows.append(dict(zip(columns, row)))
            if rows:
                return rows
        except Exception:
            pass

        # Fallback: brute-force cosine similarity
        from .queries import QUERIES
        return self.query(QUERIES["vector_search"],
                          parameters={"qemb": query_embedding, "limit": limit})

    # =========================================================================
    # Queries
    # =========================================================================

    def query(self, cypher: str, parameters: dict = None) -> list:
        """Run a Cypher query and return results as list of dicts."""
        result = self.conn.execute(cypher, parameters=parameters or {})
        columns = result.get_column_names()
        rows = []
        while result.has_next():
            row = result.get_next()
            rows.append(dict(zip(columns, row)))
        return rows

    def entity_count(self) -> int:
        from .queries import QUERIES
        result = self.query(QUERIES["entity_count"])
        return result[0]["cnt"] if result else 0

    def edge_count(self) -> int:
        from .queries import QUERIES
        result = self.query(QUERIES["edge_count"])
        return result[0]["cnt"] if result else 0

    def document_count(self) -> int:
        from .queries import QUERIES
        result = self.query(QUERIES["document_count"])
        return result[0]["cnt"] if result else 0

    def find_path(self, source_label: str, target_label: str,
                  max_hops: int = 4) -> list:
        """Find typed paths between two entities by label."""
        raw = self.query("""
            MATCH p = (a:Entity)-[r:RELATES_TO*1..%d]->(b:Entity)
            WHERE a.label CONTAINS $src AND b.label CONTAINS $tgt
            RETURN nodes(p) AS path_nodes,
                   rels(p) AS path_rels,
                   length(p) AS hops
            LIMIT 5
        """ % max_hops, parameters={"src": source_label, "tgt": target_label})

        # Post-process into clean format
        results = []
        for row in raw:
            node_labels = [n["label"] for n in row["path_nodes"]]
            edge_types = [r["edge_type"] for r in row["path_rels"]]
            path_conf = 1.0
            for r in row["path_rels"]:
                path_conf *= r.get("confidence", 1.0)
            results.append({
                "node_labels": node_labels,
                "edge_types": edge_types,
                "path_confidence": round(path_conf, 4),
            })
        return sorted(results, key=lambda p: -p["path_confidence"])

    def find_contradictions(self, entity_ids: list[str],
                            limit: int = 10) -> list[dict]:
        """Find CONFLICTS_WITH edges for the given entities.

        Returns dicts with: source_label, target_label, edge_type,
        confidence, provenance.
        """
        results = []
        seen = set()
        for eid in entity_ids[:20]:
            rows = self.query("""
                MATCH (a:Entity {id: $eid})-[r:RELATES_TO {edge_type: 'CONFLICTS_WITH'}]->(b:Entity)
                RETURN a.label AS source_label, b.label AS target_label,
                       r.confidence AS confidence, r.provenance AS provenance
            """, parameters={"eid": eid})
            for row in rows:
                key = f"{row['source_label']}|{row['target_label']}"
                if key in seen:
                    continue
                seen.add(key)
                results.append(row)
                if len(results) >= limit:
                    return results
        return results

    def flush(self) -> None:
        """Cycle the connection to flush buffered writes, keeping BOTH the
        public `conn` and the base `_conn` handle pointing at the new
        connection. (The inherited GraphWriter.flush rebinds only `_conn`,
        which would leave `self.conn` stale.)"""
        ldb = _import_ladybug()
        self._conn = ldb.Connection(self._db)
        self.conn = self._conn

    def close(self):
        # Drop the connection then the database (Lady releases its own file
        # lock here), keeping the public + base attrs in sync.
        if getattr(self, "conn", None) is not None:
            self.conn = None
        self._conn = None
        if getattr(self, "db", None) is not None:
            self.db = None
        self._db = None
        # Release the single-writer pidfile LAST (no-op in read_only mode,
        # where _lockfile is None). Order matters: a sibling spinning on the
        # pidfile must not see it vanish before Lady's lock actually releases.
        _release_writer_lock(getattr(self, "_lockfile", None))
        self._lockfile = None
