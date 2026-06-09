"""Faithful repro: does in-place bulk DELETE corrupt the LadybugDB rel store?

The README claims "bulk deletes corrupt LadybugDB's rel store"; prune_junk_entities.py
and apply_resolution.py both REFUSE in-place delete and reconstruct instead. This
checks whether that claim reproduces on the pinned ladybug>=0.17.1.

Method: copy the live graph, then exercise the two real prune patterns —
  (A) bulk DELETE a subset of edges  (MATCH ()-[r]->() ... DELETE r)
  (B) DETACH DELETE a subset of nodes (the entity-fold case)
After each, verify the REMAINING (valid, untouched) data is intact, both
in the open handle and after close+reopen. Corruption = remaining valid
edges vanish, counts disagree, traversal errors, or reopen fails.
"""

import shutil
import traceback
from pathlib import Path

SRC = Path("data/graph.lbug")
import ladybug as lb  # noqa: E402


def counts(conn):
    e = conn.execute("MATCH (n:Entity) RETURN count(n)").get_as_df().iloc[0, 0]
    r = (
        conn.execute("MATCH (:Entity)-[x:RELATES_TO]->(:Entity) RETURN count(x)")
        .get_as_df()
        .iloc[0, 0]
    )
    return int(e), int(r)


def _load_ext(conn):
    for ext in ("vector", "fts", "algo"):
        try:
            conn.execute(f"INSTALL {ext}; LOAD EXTENSION {ext};")
        except Exception as ex:
            print(f"  (ext {ext} load: {ex})")


def open_rw(path):
    db = lb.Database(str(path))
    conn = lb.Connection(db)
    _load_ext(conn)
    return db, conn


def reopen_ro(path):
    db = lb.Database(str(path), read_only=True)
    conn = lb.Connection(db)
    _load_ext(conn)
    return db, conn


def run_case(name, mutate):
    work = Path(f"/tmp/repro_{name}.lbug")
    for p in (work, Path(str(work) + ".wal")):
        if p.exists():
            p.unlink()
    shutil.copy2(SRC, work)
    wal = Path(str(SRC) + ".wal")
    if wal.exists():
        shutil.copy2(wal, str(work) + ".wal")
    print(f"\n========== CASE {name} ==========")
    db, conn = open_rw(work)
    e0, r0 = counts(conn)
    print(f"before: entities={e0} edges={r0}")
    # capture a sample of edges we will NOT touch, to verify they survive
    survivors = conn.execute(
        "MATCH (a:Entity)-[x:RELATES_TO]->(b:Entity) "
        "WHERE x.edge_type='authored_by' RETURN a.id, b.id, x.edge_type LIMIT 5"
    ).get_as_df()
    print(f"tracking {len(survivors)} 'authored_by' survivor edges")
    try:
        deleted = mutate(conn)
        e1, r1 = counts(conn)
        print(f"after mutate (same handle): entities={e1} edges={r1}  (deleted reported={deleted})")
    except Exception:
        print("!! mutate raised:")
        traceback.print_exc()
    # close + reopen
    try:
        conn.close()
        db.close()
    except Exception as ex:
        print(f"!! close raised: {ex}")
    try:
        db2, conn2 = reopen_ro(work)
    except Exception:
        print("!! REOPEN FAILED — store unreadable after delete:")
        traceback.print_exc()
        return
    e2, r2 = counts(conn2)
    print(f"after reopen (ro): entities={e2} edges={r2}")
    # verify tracked survivors still present and traversable
    bad = 0
    for _, row in survivors.iterrows():
        q = (
            "MATCH (a:Entity {id:$a})-[x:RELATES_TO {edge_type:$t}]->(b:Entity {id:$b}) "
            "RETURN count(x)"
        )
        try:
            c = int(
                conn2.execute(q, {"a": row.iloc[0], "b": row.iloc[1], "t": row.iloc[2]})
                .get_as_df()
                .iloc[0, 0]
            )
            if c != 1:
                bad += 1
                print(
                    f"  LOST survivor edge {row.iloc[0]}-[{row.iloc[2]}]->{row.iloc[1]} (found {c})"
                )
        except Exception as ex:
            bad += 1
            print(f"  TRAVERSAL ERROR on survivor: {ex}")
    # multi-hop traversal smoke (rel-store integrity)
    try:
        hop = (
            conn2.execute("MATCH (a:Entity)-[:RELATES_TO*1..3]->(b:Entity) RETURN count(*)")
            .get_as_df()
            .iloc[0, 0]
        )
        print(f"multi-hop (1..3) traversal ok: {int(hop)} paths")
    except Exception:
        print("!! multi-hop traversal FAILED:")
        traceback.print_exc()
        bad += 1
    # vector-index integrity after delete (HNSW could be the thing that corrupts)
    try:
        qv = conn2.execute(
            "MATCH (e:Entity) WHERE e.embedding IS NOT NULL RETURN e.embedding LIMIT 1"
        ).get_as_df()
        if len(qv):
            vec = list(qv.iloc[0, 0])
            res = conn2.execute(
                "CALL QUERY_VECTOR_INDEX('Entity','entity_vec',$q,5) RETURN node.id ORDER BY distance",
                {"q": vec},
            ).get_as_df()
            print(f"vector-index query ok: {len(res)} hits")
        else:
            print("vector-index: no embeddings present to query")
    except Exception as ex:
        print(f"!! vector-index query FAILED (index may be corrupt): {ex}")
        bad += 1
    verdict = "CORRUPTION" if bad else "clean"
    print(f"VERDICT {name}: {verdict}  (survivor losses/errors={bad})")
    conn2.close()
    db2.close()


def case_A_edges(conn):
    # bulk-delete every 'mentions' edge (the noisiest type) — a real prune op
    before = int(
        conn.execute(
            "MATCH (:Entity)-[x:RELATES_TO {edge_type:'mentions'}]->(:Entity) RETURN count(x)"
        )
        .get_as_df()
        .iloc[0, 0]
    )
    conn.execute("MATCH (:Entity)-[x:RELATES_TO {edge_type:'mentions'}]->(:Entity) DELETE x")
    return before


def case_B_nodes(conn):
    # DETACH DELETE 15 concept nodes whose label==id (the junk-fold case)
    ids = (
        conn.execute(
            "MATCH (n:Entity) WHERE n.entity_type='concept' AND n.id = n.label RETURN n.id LIMIT 15"
        )
        .get_as_df()
        .iloc[:, 0]
        .tolist()
    )
    for i in ids:
        conn.execute("MATCH (n:Entity {id:$id}) DETACH DELETE n", {"id": i})
    return len(ids)


def case_C_aggressive(conn):
    # large-scale fold: DETACH DELETE 120 concept/event nodes (real prune scale)
    ids = (
        conn.execute(
            "MATCH (n:Entity) WHERE n.entity_type IN ['concept','event'] RETURN n.id LIMIT 120"
        )
        .get_as_df()
        .iloc[:, 0]
        .tolist()
    )
    for i in ids:
        conn.execute("MATCH (n:Entity {id:$id}) DETACH DELETE n", {"id": i})
    return len(ids)


def case_D_delete_all_but_authored(conn):
    # near-total wipe: delete EVERY edge except the tracked 'authored_by' ones,
    # so the survivor check stays meaningful (delete-everything-but-X is the
    # strongest "does the rel store survive a massive delete" test)
    before = int(
        conn.execute(
            "MATCH (:Entity)-[x:RELATES_TO]->(:Entity) WHERE x.edge_type <> 'authored_by' RETURN count(x)"
        )
        .get_as_df()
        .iloc[0, 0]
    )
    conn.execute(
        "MATCH (:Entity)-[x:RELATES_TO]->(:Entity) WHERE x.edge_type <> 'authored_by' DELETE x"
    )
    return before


def case_E_delete_then_write(conn):
    # delete 20 nodes, then ADD a new node+edge in the same handle (post-delete write)
    ids = (
        conn.execute("MATCH (n:Entity) WHERE n.entity_type='concept' RETURN n.id LIMIT 20")
        .get_as_df()
        .iloc[:, 0]
        .tolist()
    )
    for i in ids:
        conn.execute("MATCH (n:Entity {id:$id}) DETACH DELETE n", {"id": i})
    conn.execute("CREATE (n:Entity {id:'repro_new', label:'Repro New', entity_type:'concept'})")
    # link it to a surviving 'authored_by' source if any node remains
    anc = conn.execute("MATCH (n:Entity) WHERE n.id<>'repro_new' RETURN n.id LIMIT 1").get_as_df()
    if len(anc):
        conn.execute(
            "MATCH (a:Entity {id:'repro_new'}),(b:Entity {id:$b}) "
            "CREATE (a)-[:RELATES_TO {edge_type:'mentions'}]->(b)",
            {"b": anc.iloc[0, 0]},
        )
    return len(ids)


if __name__ == "__main__":
    print(f"ladybug {getattr(lb, '__version__', '?')}  src={SRC}")
    run_case("A_bulk_edge_delete", case_A_edges)
    run_case("B_detach_delete_nodes", case_B_nodes)
    run_case("C_aggressive_120_nodes", case_C_aggressive)
    run_case("D_delete_all_but_authored", case_D_delete_all_but_authored)
    run_case("E_delete_then_write", case_E_delete_then_write)
