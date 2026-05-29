# Ontology Design — good-dog-corpus

This document is the research-process narrative behind `ontology.yaml`. It exists because in the three-corpus benchmark reported in [mempalace#101](https://github.com/MemPalace/mempalace/issues/101), the most load-bearing finding was that *different ontologies answer different questions* — and that ontology choice is load-bearing in ways most memory benchmarks make invisible.

If a corpus ships only its data and a schema file, the reader has to reverse-engineer why that schema and not another. The schema looks like a fact when it's actually a series of judgment calls. This document shows the work.

The structure below is the order the design was actually done in: domain → questions → entity types → edge types → evidence rules → scope boundaries → category mapping. Each section documents what was considered, what was chosen, and what was rejected.

---

## 1. Starting point: what does someone want to ask about dogs?

Before any schema, the question is what a memory system over this corpus would need to answer. A non-exhaustive sample, organized by the SME category each question would land in:

| Question | Category | What it requires the schema to support |
|---|---|---|
| What's the current vet consensus on grain-free diets? | Cat 6 (temporal) | Versioned recommendations with supersession |
| Who are the breed registry authorities for German Shepherds? | Cat 1 (factual) | Authority entities, jurisdictional scope |
| What recalls happened to brand X in 2023? | Cat 6 (temporal) | Event entities with timestamps and product links |
| How does my city's leash law compare to neighboring city's? | Cat 2c (multi-hop) | Policy entities with location and content scoping |
| Did the 2009 AVSAB rebuttal change shelter training methods? | Cat 2c + Cat 3 | Cross-domain causal chain, contradictions |
| What breeds are mentioned in this article about a local park incident? | Cat 1 + Cat 4 (alias) | Entity extraction with alias resolution |
| What did this researcher publish, and at which institutions? | Cat 2c | Author + affiliation chains |
| Is this dog food recall still active? | Cat 6 | Event status over time |

Reading those questions sideways, the entity and edge types start to emerge. Three observations from this exercise that shaped what followed:

- **Temporal evolution is everywhere in this domain.** Recalls, recommendations, training methodology — most non-trivial questions about dogs require knowing what was true *when*. Any schema that doesn't first-class temporal supersession will read these queries wrong.
- **Aliases matter more than the dataset suggests at first glance.** "GSD," "German Shepherd," "Alsatian" all refer to the same breed. "Pit Bull" maps to several distinct registered breeds depending on the source. "Pitbull" without space is a media spelling. A KG that treats these as distinct entities silently fragments the graph.
- **Authority and scope are explicit in this domain.** Unlike many corpora where "who said this and why does it count" is left implicit, dog-related sources are structured around named regulatory bodies (FDA, AKC, AVMA, AVSAB) with explicit jurisdictional scope. The schema can encode authority cleanly because the source material does.

---

## 2. Entity types

The eight entity types in `ontology.yaml` came from grouping the questions in §1 by what kind of thing each one requires the graph to know about. Decisions and rejections:

**Kept:**

- **`breed`** — A recognized dog breed or breed group. The most common entity referenced across all six source domains. Rejected the alternative of folding `breed` into `concept` because breeds have explicit registry authority, hierarchical relationships (breed groups), and ALIAS_OF relationships that are central to Cat 4 evaluation; collapsing them would lose the alias-resolution test.
- **`person`** — Named individual: researcher, vet, trainer, journalist, council member. One type rather than per-role subtypes. The role information lives in edges (`affiliated_with`, `authored_by`) rather than entity subtypes, because most people in this corpus play multiple roles (a researcher who also testifies at council hearings).
- **`organization`** — Kennel club, university, vet hospital, municipality, regulatory body. Considered splitting `regulatory_body` into its own type since it has different evidence requirements; rejected because the regulatory aspect is captured cleanly by `regulates` edges and a separate `is_regulatory: true` flag would do the same job with less proliferation.
- **`publication`** — Study, article, bylaw, recall notice — anything authored. Considered splitting into `study`, `news_article`, `regulatory_document`, etc.; rejected because the *what kind of publication* axis is well-served by source domain (which is encoded by file path) and `subject_of` edges, and proliferating publication subtypes would explode the type vocabulary without earning information.
- **`concept`** — Idea or methodology: dominance theory, positive reinforcement, BSL. The trickiest type. Considered eliminating concepts entirely and treating them as "topics" via tags; rejected because concepts have first-class behavior in this domain — they get superseded (dominance theory → positive reinforcement consensus shift), they regulate practice (BSL is a concept that some municipalities encode as policy), and multi-hop questions traverse them as nodes.
- **`product`** — Specific commercial product, brand, or SKU. Necessary for the recall chain (Cat 6). Brand entities and product entities are not separated; the brand is captured as an attribute. This was a judgment call — separating them would let queries like "all recalls by manufacturer X" be cleaner, but the corpus doesn't have enough product-level granularity to make the distinction earn itself.
- **`event`** — Recall announcement, council vote, study publication, attack incident. Events are first-class because they anchor temporal queries and the `subject_of` relationship. Without event entities, recalls become "publications about a thing that happened" rather than "the thing itself," and the temporal chain queries get harder to express.
- **`location`** — City, park, shelter, jurisdiction. Necessary for cross-jurisdiction policy comparison.

**Rejected:**

- **`role`** — Initially considered as a way to handle multi-role people. Replaced by edge-level role information (`authored_by`, `affiliated_with`) because roles are inherently relational, not entitative.
- **`claim`** — Considered as an entity type to make `contradicts` and `supersedes` cleaner. Rejected because materializing every claim as an entity would explode the graph and require claim extraction at ingest time, which is a hard NLP problem outside the corpus's scope. Claims live as text inside `publication` entities, and `contradicts` / `supersedes` edges connect publications directly.
- **`taxonomy_node`** — For breed groups (e.g., Sporting Group containing Labrador, Golden Retriever). Rejected as a separate type because the relationship is well-captured by a `member_of` edge between `breed` entities. Breed group membership doesn't require a type with different fields.

---

## 3. Edge types

The eleven edge types in `ontology.yaml` were derived by examining the questions in §1 again, this time looking at what *relationships* between entities each question requires. The edge type is the minimum vocabulary to express those relationships without leaking modeling decisions.

**Kept:**

- **`mentions`** — Base relation: a document mentions an entity. Every other edge type is some refinement of "this thing references that thing in this specific way." `mentions` is the floor.
- **`alias_of`** — Two surface forms refer to the same canonical entity. Required for Cat 4 (ingestion integrity / dedup). Lives at the entity level, not the document level — this is canonical-form information, not narrative.
- **`supersedes`** — Newer finding/policy/recommendation replaces older. The temporal axis. Required for Cat 6.
- **`contradicts`** — Two publications make incompatible claims about the same entity. Distinct from `supersedes`: contradictory publications can be contemporaneous (two studies disagreeing), where `supersedes` requires a time order. Required for Cat 3.
- **`cites`** — Explicit reference. Required for provenance chains and multi-hop reasoning.
- **`authored_by`** — Publication → Person. Cheap to extract (byline match), high value for Cat 2c chains.
- **`affiliated_with`** — Person → Organization. Often time-bounded (a researcher's affiliation changes), but the corpus stays at "currently affiliated" granularity to keep the v0 schema shippable.
- **`regulates`** — Organization → Product or Concept. Captures "FDA regulates pet food," "AKC regulates breed standards," etc. Necessary for jurisdictional questions.
- **`subject_of`** — Publication → Event or Concept. Distinguishes "this article *is about* the 2018 DCM finding" from "this article *mentions* DCM in passing." Required for Cat 1 precision.
- **`member_of`** — Breed → Breed group, Person → Organization (when affiliation is membership rather than employment). Reused across two relationship shapes; flagged in `ontology.yaml` for review in v0.2.
- **`located_in`** — Event or Organization → Location. Cross-jurisdiction queries.

**Rejected:**

- **`opposes`** as distinct from `contradicts` — Considered for cases where a publication explicitly argues *against* another publication's recommendation, not just states an incompatible finding. Rejected as a v0.1 distinction: too subtle for the substring matcher to read, and the upgrade to LLM-judge-grounded edge typing is the right place to introduce finer distinctions.
- **`replaces` distinct from `supersedes`** — Similar reasoning: `replaces` would have been for hard substitution (Brand X recall replaces Brand Y in shelves), `supersedes` for normative replacement (2009 AVSAB position supersedes 1970s dominance recommendations). Collapsed into one edge type with a `nature` attribute deferred to v0.2.
- **`influences`** — For cases where one publication shaped another without explicit citation. Rejected as too speculative for ground truth annotation; the corpus stays with edges that are evidentiable from source text.

---

## 4. Evidence rules per edge type (the phantom-edge connection)

This is the section that didn't exist in the original v0.1 ontology design until the [phantom-edge proposal at SME #4](https://github.com/M0nkeyFl0wer/multipass-structural-memory-eval/issues/4) made it necessary. The proposal — that every edge in the graph should be probable against an evidence rule registered with its edge type — turned what would have been "edge types are loosely defined" into "every edge type ships its rule for what counts as supporting evidence."

The rules in `ontology.yaml` are deliberately heterogeneous because the underlying evidence is heterogeneous:

- **Lexical-overlap rules** for `mentions`. Cheapest, most fallible, most automatable. Caveat noted in the phantom-edge proposal: when the edge-creation rule itself was substring matching, a substring-matching probe is circular and reports zero phantoms by construction. The escape is per-edge-type thresholds — `mentions` runs lexical, but other edges register different rules.
- **Registry rules** for `alias_of`. The alias registry in `ontology.yaml#aliases` is the authoritative source. Edges that don't appear in the registry are phantom by definition.
- **Explicit-marker rules** for `supersedes`. Temporal-replacement phrases ("now recommended over," "supersedes," "withdrawn") in source text. False negatives expected — supersession is often implicit — but a probe that demands explicit markers earns its precision.
- **Claim-pair rules** for `contradicts`. The hardest. v0.1 marks these as `requires_human_grounding: true` rather than pretending an automated rule exists. The honest position: contradiction detection is a research problem, and the corpus annotations are the human grounding the eval framework needs to validate any future automated detector.
- **Explicit-reference rules** for `cites`. DOI, URL, or formal citation match. High precision, low recall.
- **Byline / affiliation phrase rules** for `authored_by` and `affiliated_with`. Pattern matching on author and affiliation fields.
- **Topic-match rules** for `subject_of`. Title or abstract subject extraction. Also marked `requires_human_grounding: true` for the same reason as contradiction — distinguishing "primarily about" from "mentions in passing" is not currently solvable by lexical rules alone.

The heterogeneity is the point. Cat 10 (phantom edges) is not a single threshold; it's a per-edge-type contract about what counts as evidence, and the corpus is the first place that contract gets written down.

---

## 5. What's deliberately out of scope

Three classes of content are excluded from the ontology and therefore from the corpus:

- **Subjective stance modeling.** Opinion-level claims (BSL pros/cons as advocacy positions, breed reputation debates, training philosophy advocacy) are out. The corpus stays at the level of factual claims that can be sourced and contested with evidence. Stance modeling is a separate problem; mixing it in here would muddy the contradiction signal.
- **Individual dog narratives.** Specific named dogs in adoption stories or local incidents are treated as character mentions in `publication` text, not as graph entities. Including them would explode the entity count without earning meaningful retrieval signal — there is no question in §1 that requires "given dog X, find all stories about dog X" as a structural query.
- **Image content.** Visual content of source articles is out. The KG is text-only.

These exclusions are documented in `ontology.yaml#out_of_scope` so anyone extending the corpus knows what was left out *on purpose* vs what was omitted by accident.

---

## 6. How this ontology connects to SME categories

The ontology was designed against the published SME categories, not retrofitted to them. Each category exercises a specific subset of the schema, documented in `ontology.yaml#sme_category_coverage`. The mapping at a glance:

| Category | Edges exercised | Representative scenario |
|---|---|---|
| Cat 1 (factual retrieval) | `mentions`, `subject_of` | "What recalls happened to brand X in 2023?" |
| Cat 2c (multi-hop) | `authored_by`, `affiliated_with`, `cites`, `subject_of` | "Vet author → affiliation → studies cited in council policy" |
| Cat 3 (contradiction) | `contradicts` | Grain-free DCM debate (2018 → 2022 reversal); dominance theory (1970s → 2009 AVSAB) |
| Cat 4 (ingestion integrity / alias resolution) | `alias_of` | GSD / German Shepherd / Alsatian collapse |
| Cat 6 (temporal) | `supersedes` | Pet food recall lifecycle: announced → investigated → resolved |
| Cat 8 (ontology coherence) | the entire schema vs the built graph | Did the corpus build the graph it claimed it would? |
| Cat 10 (phantom edges) | `evidence_rule` field on every edge type | First worked example of per-edge-type evidence registration |

The corpus deliberately seeds material for each category: contradiction pairs in `vault/veterinary_research/` and `vault/behavioral_research/`, alias pairs in `vault/breed_standards/`, temporal chains in `vault/nutrition_safety/` (recall lifecycles) and `vault/behavioral_research/` (training methodology evolution), and cross-domain hop chains spanning `vault/veterinary_research/` → `vault/municipal_policy/` → `vault/community_journalism/`.

---

## 7. How to extend this ontology

The `ontology.yaml` schema is versioned. Extensions go through the same documentation discipline used here:

1. Identify a question the current ontology can't express.
2. Determine whether it needs a new entity type, a new edge type, or a refinement of an existing one. Default: refine an existing one.
3. If a new edge type is required, register its evidence rule before merging. The phantom-edge probe depends on this.
4. Document the alternatives considered and the rejection rationale. The teaching artifact is the design narrative, not the schema.
5. Bump the `version` field. v0.1 → v0.2.

Extensions should be opened as issues against the SME repo with `[good-dog-corpus]` in the title.

---

## Status

v0.1, drafted 2026-04-30. Subject to revision as the corpus content fills in and edge cases surface. Major revisions will be reflected in `ontology.yaml`'s `version` field and a changelog appended to this document.
