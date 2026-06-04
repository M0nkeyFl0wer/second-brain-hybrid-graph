#!/usr/bin/env bash
# Experiment: does a tailored ontology improve structural-memory quality?
#
# Builds the SAME corpus (good-dog) twice — once under the generic built-in
# ontology, once under the corpus's hand-designed ontology.yaml — then runs
# the multipass SME suite against both and diffs the structural readings.
#
# Throwaway graphs under data/exp/. Zero production risk. Each phase logs to
# its own file; a failure in one phase doesn't lose the prior phase's work.
#
# Usage: bash scripts/experiment_ontology_impact.sh
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

PY=.venv/bin/python
VAULT=examples/good-dog-corpus/vault
ONTO=examples/good-dog-corpus/ontology.yaml
SME=/home/user/Projects/multipass-structural-memory-eval/.venv/bin/sme-eval
EXP=data/exp
mkdir -p "$EXP"
LOG="$EXP/run.log"
: > "$LOG"
log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }

build() {  # name, extra-args...
    local name="$1"; shift
    log "── build '$name' ───────────────────────────────"
    rm -rf data/graph.lbug data/graph.lbug.wal data/chunks.duckdb 2>/dev/null
    $PY scripts/ingest_obsidian.py --vault "$VAULT" "$@" >> "$EXP/build-$name.log" 2>&1
    local rc=$?
    if [ $rc -ne 0 ]; then log "  BUILD FAILED rc=$rc (see build-$name.log)"; return $rc; fi
    # archive the artifacts for this variant
    rm -rf "$EXP/$name" 2>/dev/null; mkdir -p "$EXP/$name"
    [ -e data/graph.lbug ]    && cp -r data/graph.lbug    "$EXP/$name/graph.lbug"
    [ -e data/chunks.duckdb ] && cp    data/chunks.duckdb "$EXP/$name/chunks.duckdb"
    log "  built '$name' → $EXP/$name/graph.lbug"
}

sme() {  # name
    local name="$1"
    local db="$EXP/$name/graph.lbug"
    log "── SME '$name' ─────────────────────────────────"
    [ -e "$db" ] || { log "  no graph for '$name', skipping SME"; return 1; }
    # discover edge (REL) tables so we scope SME to the semantic layer
    local rels
    rels=$($PY - "$db" <<'PYED' 2>>"$LOG"
import sys
try: import ladybug as lb
except ImportError: import real_ladybug as lb
db=lb.Database(sys.argv[1], read_only=True); c=lb.Connection(db)
rs=c.execute("CALL show_tables() RETURN *")
rels=[r[1] for r in iter(lambda: rs.get_next() if rs.has_next() else None, None) if r[2]=='REL']
print(",".join(rels))
PYED
)
    log "  REL tables: ${rels:-<none>}"
    # analyze (entropy, components, communities) + check (Cat 4 + Cat 5)
    $SME analyze --adapter ladybugdb --db "$db" ${rels:+--edge-tables "$rels"} \
        --json "$EXP/$name/sme-analyze.json" >> "$EXP/sme-$name.log" 2>&1 \
        && log "  analyze → $EXP/$name/sme-analyze.json" \
        || log "  analyze FAILED (see sme-$name.log)"
    $SME check --adapter ladybugdb --db "$db" ${rels:+--edge-tables "$rels"} --no-homology \
        --json "$EXP/$name/sme-check.json" >> "$EXP/sme-$name.log" 2>&1 \
        && log "  check → $EXP/$name/sme-check.json" \
        || log "  check FAILED (see sme-$name.log)"
}

log "=== Ontology-impact experiment START ==="
build generic                          || log "generic build failed — continuing"
build custom --ontology "$ONTO"        || log "custom build failed — continuing"
sme generic
sme custom

log "── COMPARISON ──────────────────────────────────"
$PY - <<'PYCMP' 2>>"$LOG" | tee -a "$LOG"
import json, os
EXP="data/exp"
def load(p):
    try: return json.load(open(p))
    except Exception: return {}
def graph_counts(name):
    db=f"{EXP}/{name}/graph.lbug"
    if not os.path.exists(db): return (None,None)
    try:
        import ladybug as lb
    except ImportError:
        import real_ladybug as lb
    d=lb.Database(db, read_only=True); c=lb.Connection(d)
    try:
        ents=c.execute("MATCH (e:Entity) RETURN count(e)").get_next()[0]
    except Exception: ents=None
    del c,d
    return ents
print(f"{'metric':<32}{'generic':>14}{'custom':>14}")
print("-"*60)
for name in ("generic","custom"):
    pass
g_ent=graph_counts("generic"); c_ent=graph_counts("custom")
print(f"{'entities':<32}{str(g_ent):>14}{str(c_ent):>14}")
ga=load(f"{EXP}/generic/sme-analyze.json"); ca=load(f"{EXP}/custom/sme-analyze.json")
for k in ("edge_type_entropy_normalized","largest_component_size","components","bridges"):
    print(f"{k:<32}{str(ga.get(k)):>14}{str(ca.get(k)):>14}")
gc=load(f"{EXP}/generic/sme-check.json"); cc=load(f"{EXP}/custom/sme-check.json")
print("\n(full SME reports in data/exp/*/sme-*.json)")
PYCMP

log "=== Ontology-impact experiment DONE ==="