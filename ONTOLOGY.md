# Personal Knowledge Ontology v1.1

This file documents every entity type and edge type the knowledge graph accepts.
Edit it for your thinking style. The system validates all entities and edges
against the ontology at write time — types not listed are rejected and logged
(as machine-readable SHACL-vocabulary violations; see *Validation output* below).

> **Source of truth.** The *enforced* vocabulary lives in
> `second_brain/ontology.py` (`NODE_TYPES`, `EDGE_TYPES`, `EDGE_DOMAIN_RANGE`).
> This document mirrors it. If the two ever disagree, the code wins — and the
> doc is the bug. v1.1 reconciled this file to the code (added `method`/`tool`
> and `IMPLEMENTS`/`REQUIRES`; moved `ASSOCIATED_WITH` to structural-only).

## Entity Types

Ten types. The **Rigidity / Identity** column records OntoClean meta-properties
(see *Meta-properties* below) — these are methodology, not an imported library.

| Type | Rigidity / Identity | Description | Archetypical | Exotypical (NOT this type) |
|------|--------------------|-------------|-------------|---------------------------|
| concept | +R / +I | An idea, topic, principle, or belief | "spaced repetition" | "Anki" → tool (the app, not the idea) |
| person | +R / +I | An individual — author, mentor, friend, historical figure | "Richard Feynman" | "Feynman Lectures" → source |
| source | +R / +I | A book, article, podcast, course, or other knowledge origin | "Thinking, Fast and Slow" | "Daniel Kahneman" → person |
| place | +R / +I | A location with personal meaning or context | "the coffee shop on Queen St" | "Toronto" → only if the city itself matters |
| tool | +R / +I | Software, app, or resource you use | "Obsidian", "DuckDB" | "version control" → concept (the idea, not the app) |
| method | +R / +I | A technique or approach (codified, reusable) | "causal inference", "counterfactual reasoning" | "morning journaling" → practice (your routine) |
| project | ~R / +I | A personal project, initiative, or ongoing effort | "learning Rust" | "Rust" → concept (the language, not your project) |
| insight | ~R / +I | An original thought, realization, or synthesis you had | "sleep deprivation compounds like debt" | "sleep debt" → concept (the general idea) |
| question | ~R / +I | An open question, uncertainty, or thing to explore | "why does meditation reduce anxiety?" | "meditation" → concept |
| practice | ~R / +I | A habit, routine, or technique *you* use | "morning journaling" | "Getting Things Done" → source (the book) |

### Meta-properties (OntoClean)

OntoClean (Guarino & Welty) is a methodology — there is no library to import.
We steal two meta-properties to keep the type hierarchy coherent:

- **+R (rigid):** essential to every instance. A `person` is necessarily a
  person in every context; ditto `place`, `source`, `concept`, `tool`, `method`.
- **~R (anti-rigid):** contingent — the instance can leave the type without
  ceasing to exist. An `insight` can be reclassified as a `concept`; a
  `question` can be answered and become an `insight`; a `practice` can be
  abandoned; a `project` can be completed. These are the types most likely to
  *migrate*, so resolution/dedup should treat them as mutable.
- **+I (identity):** every type carries name-based identity — two entities are
  the same iff their canonical labels (after `slugify`) match. `id =
  slugify(label)`; the same label from different documents resolves to one node,
  which is what lets cross-document edges connect.

**Coherence rule: `~R` cannot subsume `+R`.** If an anti-rigid type
(`practice`, `insight`, `question`, `project`) ever appears as the *parent* of a
rigid type (`source`, `person`, `place`, `concept`, `tool`, `method`) in a
PART_OF / is-a hierarchy, the ontology is incoherent — fix the edge direction or
the types. (Diagnostic only; not auto-enforced.)

### Vocabulary encoding (SKOS-aligned)

The vocabulary speaks SKOS without importing rdflib:

- `entity.name` (model) / `label` (graph) = **`skos:prefLabel`** — the canonical
  surface form.
- `entity.aliases` = **`skos:altLabel`** — alternative surface forms the system
  has seen for the same concept.
- Type-to-type relationships are discussed with **`skos:broader` / `skos:narrower`**
  terminology (e.g. `method` is *narrower* than `concept` in conversation,
  though the graph stores no is-a edge between *types*).

## Edge Types

Ten types. **From → To** is the *enforced* domain/range from
`EDGE_DOMAIN_RANGE`. Where it says **any → any**, the edge is structurally
unconstrained in code today — the "intended" column is convention/guidance the
extractor is prompted toward, not a hard gate.

| Type | From → To (enforced) | Intended use | Signal |
|------|---------------------|--------------|--------|
| LEARNED_FROM | any → any | concept/insight/practice → source/person | Knowledge provenance |
| INSPIRED_BY | any → any | insight → concept/person/source | Creative lineage |
| CONFLICTS_WITH | any → any | concept → concept | Cognitive tension, growth edge |
| SUPPORTS | any → any | concept → concept | Belief structure |
| PART_OF | any → any | concept → concept | Knowledge organization |
| PRACTICED_IN | {practice, method, tool} → any | practice/method/tool → project | Theory → practice link |
| ASKED_ABOUT | {question} → any | question → concept | Research direction |
| ANSWERS | any → {question} | insight/source → question | Knowledge closure |
| IMPLEMENTS | {tool, method} → any | tool/method → concept | Tool ↔ idea link |
| REQUIRES | any → any | tool/concept → tool/concept | Dependency |

> **`ASSOCIATED_WITH` is not in this table on purpose.** It is a *structural*
> edge type (`STRUCTURAL_EDGE_TYPES` in `second_brain/ontology_base.py`), used as
> the untyped-extraction fallback and for wikilink/tag edges. It always
> validates, but it is **not** a domain edge — prefer any typed edge above it.
> Watch its share: if `ASSOCIATED_WITH` exceeds ~10% of all edges, the graph is
> drifting toward a `RELATED`-everything monoculture and the extractor needs
> tighter prompting.

### Edge cardinality / quality constraints

These are the constraints the pipeline cares about (the "SHACL steal" — we use
SHACL *report* vocabulary, not the SHACL engine):

- **Evidence required.** Every extracted edge should carry a verbatim evidence
  quote (≥10 chars) from the source text — strongest for `SUPPORTS` and
  `CONFLICTS_WITH`, which assert belief structure. Missing/short evidence is a
  `warning`-severity violation (it does not drop the edge).
- **Confidence ∈ [0, 1].** Enforced by the Pydantic extraction models
  (`second_brain/models/extraction.py`); out-of-range values are clamped.
- **Type membership.** `entity_type ∈ NODE_TYPES` and `edge_type ∈ EDGE_TYPES ∪
  {ASSOCIATED_WITH}` — enforced at write time. Double-enforced when the optional
  Instructor backend is used (the LLM is constrained to the schema *and* the
  writer re-checks).

## Validation output (SHACL report vocabulary)

When the writer rejects an entity (unknown type) or an edge (unknown type), or a
lint pass finds a missing evidence quote, it emits a structured
`ValidationViolation` (`second_brain/models/validation.py`) using SHACL report
field names — `focusNode`, `resultPath`, `sourceConstraintComponent`,
`resultMessage`, `severity`. The rejection log is therefore machine-readable by
anyone who knows SHACL vocabulary, with **no pyshacl dependency**. The Python
validation logic is unchanged; only the output format is standardized.

## Semantic Spacetime Edge-Nodes

For complex, multi-way, or annotated relationships, the graph supports
**edge-nodes** — first-class nodes that represent the relationship itself. An
edge-node connects to its participants via CONNECTS and BINDS edges.

| Edge-Node Type | Meaning | Example |
|---------------|---------|---------|
| similar_edge | Proximity, analogy — "X is like Y" | "spaced repetition" is similar to "compound interest" |
| contains_edge | Hierarchy, composition — "X contains Y" | "cognitive science" contains "memory", "attention" |
| property_edge | State, attribute — "X has property Y" | "meditation" has property "requires consistency" |
| leads_to_edge | Causality, sequence — "X leads to Y" | "sleep deprivation" leads to "impaired decisions" |

Edge-nodes support **hypergraphs** (one relationship linking 3+ entities) and
**metagraphs** (thoughts about thoughts) without schema changes.

- **Direct edge:** simple, binary, well-typed relationship (the edges above).
- **Edge-node:** relationship needs annotation, connects 3+ things, or is itself
  a thought about a relationship.

## Extending This Ontology

- Only add a type when you've seen 3+ instances that don't fit existing types.
- New anti-rigid (`~R`) types are cheap; new rigid (`+R`) types reshape identity
  — add them deliberately.
- Edit `second_brain/ontology.py` (the source of truth), then update this file.
- Run `sb-validate` (or `python -m scripts.validate_ontology`) after editing.
- The rejection log after ingestion tells you which types your notes actually
  need.
