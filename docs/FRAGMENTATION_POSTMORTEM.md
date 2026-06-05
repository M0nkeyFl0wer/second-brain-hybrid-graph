# Fragmentation Postmortem — open-second-brain v0.2.2

**Date**: 2026-06-05
**Graph**: 682 entities / 143 edges / 36 docs
**SME Scores**: Cat 4 warning, Cat 5 concerning, Cat 8 1 PROV violation

---

## Executive Summary

The smoke-test graph exhibits **severe fragmentation** (76.5% isolates, 584 components, 4% connectivity in largest component). Root causes trace to three pipeline stages where quality gates either didn't exist or were bypassed.

---

## Failure Mode Catalog

### 1. Canonicalization Failure (Stage 3-4)
**Symptom**: 24 case-insensitive collision groups creating duplicate entity IDs
- `AmStaff`/`amstaff` → separate entities
- `APBT`/`apbt`, `C-BARQ`/`C-BARQ`, `GSD`/`gsd`, etc.
- Tag entities colliding with content entities (`tag_fda` vs `fda`)

**Root cause**: `generate_entity_id(label)` in `extract.py` uses slugify without case-folding or collision detection. Bulk `COPY` bypasses per-entity MERGE dedup.

**Fix**: Canonicalize to lowercase before ID generation, or run Phase-A resolver during ingest.

### 2. Grade Enforcement Over-Dropping (Stage 6-7)
**Symptom**: Strict domain/range drops ~74% of extracted edges
- `member_of` (person→org): 1 edge extracted (expected many)
- `grouped_under` (breed→breed): 1 edge extracted (expected many)
- `cites` (pub→pub): 3 edges
- `regulates` (org→product): 4 edges

**Root cause**: qwen3:14b consistently prefers `affiliated_with` over `member_of` for person→org; doesn't extract breed→breed relations. Ontology has overlapping edge types with no guidance.

**Fix**: Relax ontology to merge overlapping types, or add one-shot examples to extraction prompt.

### 3. Wikilink → Document-Star Topology (Ingest post-processing)
**Symptom**: 88% of edges are structural bridges; star topology with Document at center

**Root cause**: Wikilinks create `ASSOCIATED_WITH` edges `Document → concept`, not Entity → Entity. No cross-document entity resolution from wikilinks.

**Fix**: Resolve wikilinks to existing entities, create Entity → Entity edges.

### 4. No Cross-Document Resolution During Ingest
**Symptom**: Same entity ("FDA") extracted from 10+ docs → different IDs

**Root cause**: Phase-A resolver (B-Cubed 0.874) runs *after* ingest, not during. Bulk `COPY` bypasses per-entity MERGE dedup.

**Fix**: Run resolver during ingest, or per-entity MERGE instead of bulk COPY.

---

## Quality Gates That Should Have Caught This

| Gate | Status | Why It Failed |
|------|--------|---------------|
| **Sample-before-scale** (30 entities) | ❌ Not run | Full ingest executed without 30-entity smoke |
| **SME Cat 4/5/8 on interim graph** | ❌ Not run | SME only run post-hoc |
| **Phase-A resolver dry-run during ingest** | ❌ Not run | Resolver only runs as separate CLI step |
| **Canonicalization collision check** | ❌ Missing | No pre-write check for case variants |
| **Edge-type coverage guard** | ❌ Missing | No alert when 74% edges dropped |

---

## Repo / Skills Gaps That Enabled This

### In `open-second-brain` repo:
1. **No smoke-test script** that runs: ingest 30 entities → SME → gate → proceed/fail
2. **No `scripts/smoke_test.py`** as specified in PLAN.md (still ⬜ Todo)
3. **No CI pipeline** that runs SME on PR graphs
4. **Ingest script lacks `--limit` gate** that triggers SME after N entities
5. **Resolver not wired into ingest** — separate CLI only

### In `edge-finder` skill:
- Already addresses this: "Sample before you scale. Check 30 entities before ingesting 50K"
- But no integration with open-second-brain ingest pipeline

### In `kg-ingestion` skill:
- Postmortem documents this exact failure mode: "3 hours of compute, 0 entities and 0 edges landed... all preventable"
- But no automated check that runs during ingest

### In `ladybug` skill:
- Concurrency rules exist but no "dedup at write" pattern enforced

---

## Ensuring Users Don't Hit This

### 1. Add `scripts/smoke_test.py` (PLAN.md item)
```python
# Ingest 30 entities → run SME Cat 4/5/8 → gate on:
# - canonical_collisions == 0
# - isolate_pct < 30%
# - edge_drop_pct < 50%
# - connectivity > 20%
```

### 2. Wire resolver into ingest
```python
# In ingest_obsidian.py, after bulk_add_entities:
# Run EntityResolver on entities written so far
# Apply merge mapping before bulk_add_edges
```

### 3. Canonicalization fix in `extract.py`
```python
def generate_entity_id(label: str) -> str:
    # Add case-folding and hyphen/underscore normalization
    canonical = label.lower().replace('_', '-').replace(' ', '-')
    return slugify(canonical)
```

### 4. Add pre-write collision detector
```python
# In Graph.bulk_add_entities:
# Check for case-insensitive duplicates before COPY
```

### 5. SME gate in CI
```yaml
# .github/workflows/sme-gate.yml
# On PR: spin up temp graph, ingest fixture corpus, run SME, fail on warnings
```

### 6. Documentation
- `docs/INSTALL.md`: Run smoke test first
- `docs/PIPELINE.md`: Quality gates at each stage
- `docs/TROUBLESHOOTING.md`: "High isolate count? Check canonicalization + grade enforcement"

---

## Immediate Next Steps (Running Now)

1. **Run Phase-A resolver on current graph** — merge 80 label clusters
2. **Score resolver** — confirm B-Cubed F1 ~0.874
3. **Apply canonicalization fix** to `generate_entity_id`
4. **Re-ingest with fixes** — verify SME scores improve
5. **Add smoke_test.py** to repo

---

## Commands to Run

```bash
# 1. Resolver dry-run (already done, re-running)
.venv/bin/python -m scripts.resolve_entities --graph data/graph.lbug --out data/resolution.json

# 2. Score resolver
.venv/bin/python -m eval.run_er_eval --resolver

# 3. Apply canonicalization fix to extract.py
# (edit generate_entity_id)

# 4. Re-ingest fresh
rm -f data/graph.lbug*
SECOND_BRAIN_EXTRACT_HOST=http://localhost:11434 OLLAMA_HOST=http://localhost:11434 \
  SECOND_BRAIN_LOCAL_MODEL=qwen3:14b SECOND_BRAIN_EXTRACT_TIMEOUT=300 \
  .venv/bin/python scripts/ingest_obsidian.py --vault examples/good-dog-corpus/vault \
  --ontology examples/good-dog-corpus/ontology.yaml --force --workers 1

# 5. Run SME on new graph
.venv/bin/python -m sme.cli check --adapter ladybugdb --db data/graph.lbug --auto-discover
```