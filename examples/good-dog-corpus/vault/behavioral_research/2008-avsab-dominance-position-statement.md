---
note_id: bhv_2008_avsab_dominance_position_statement
source_url: https://avsab.org/wp-content/uploads/2018/03/Dominance_Position_Statement_download-10-3-14.pdf
source_title: "AVSAB Position Statement on the Use of Dominance Theory in Behavior Modification of Animals"
source_date: "2008"
source_publisher: "American Veterinary Society of Animal Behavior (AVSAB)"
license: fair_use_excerpt
license_note: "AVSAB explicitly distributes this PDF for public dissemination from its own site (avsab.org). Verbatim full-text redistribution should be avoided; short excerpts with attribution are appropriate. The Internet Archive mirror at archive.org/details/dominance-position-statement is a stable backup."
accessed_on: "2026-04-30"
domain: behavioral_research

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: org_avsab
    type: organization
    canonical: "American Veterinary Society of Animal Behavior"
    aliases: ["AVSAB"]
    is_regulatory: false
  - id: pub_avsab_2008_dominance_position
    type: publication
    canonical: "AVSAB Position Statement on the Use of Dominance Theory in Behavior Modification of Animals (2008)"
    aliases: ["AVSAB 2008 dominance statement", "AVSAB Dominance Position Statement"]
  - id: concept_positive_reinforcement_training
    type: concept
    canonical: "Positive reinforcement training (animal behavior modification)"
    aliases: ["reward-based training", "positive reinforcement"]

# Edges introduced or strengthened by this note. The supersession back
# to Schenkel 1947 (via the dominance-theory concept) is the clinical-
# practice side of the post-1999 consensus.
edges:
  - from: pub_avsab_2008_dominance_position
    type: authored_by
    to: org_avsab
    evidence: "Position statement is an institutional publication of AVSAB; byline is the society itself, with the document hosted on avsab.org."
  - from: pub_avsab_2008_dominance_position
    type: subject_of
    to: concept_dominance_theory
    evidence: "The document title names dominance theory as its primary subject: 'Position Statement on the Use of Dominance Theory in Behavior Modification of Animals.'"
  - from: pub_avsab_2008_dominance_position
    type: mentions
    to: concept_positive_reinforcement_training
    evidence: "The position statement contrasts dominance-based training with reward-based / positive-reinforcement methods, recommending the latter; the AVSAB position page identifies positive-reinforcement training as the recommended alternative."
  - from: pub_avsab_2008_dominance_position
    type: contradicts
    to: pub_schenkel_1947_wolf_expression
    evidence: "AVSAB's 2008 statement directly opposes the dominance-hierarchy framing whose academic foundation is Schenkel 1947. The statement's load-bearing claim — 'most undesirable behaviors in our pets are not related to priority access to resources; rather, they are due to accidental rewarding of the undesirable behavior' — repudiates the priority-access / dominance-hierarchy explanatory framework that Schenkel-derived training advice rests on."
  - from: pub_avsab_2008_dominance_position
    type: supersedes
    to: pub_schenkel_1947_wolf_expression
    evidence: "AVSAB 2008 supersedes dominance-theory-derived clinical guidance (whose origin is Schenkel 1947) by formally recommending against its use in behavior modification. Per ontology.yaml#supersedes, this is a normative-replacement rather than literal-marker case; flagged for human grounding."
    needs_grounding: true
  - from: org_avsab
    type: regulates
    to: concept_dominance_theory
    evidence: "AVSAB is the professional veterinary-behavior body whose position statements set clinical guidance for the field. While AVSAB is not a statutory regulator (is_regulatory: false), within ontology terms its position statements carry professional-jurisdictional authority over behavior-modification practice."
    needs_grounding: true

tags: [behavioral_research, dominance_theory, avsab, position_statement, contradiction_pair, post_correction]
contradiction_pair_id: dominance_theory_pre_vs_post_1999
---

# AVSAB 2008 — Position Statement on the Use of Dominance Theory

## Summary

In **2008**, the American Veterinary Society of Animal Behavior (AVSAB) issued a formal position statement recommending **against** the use of dominance theory as a guide for behavior modification in companion animals. The statement codified, at the level of professional-body clinical guidance, the post-1999 scientific position that Mech's wild-wolf research had already established in the academic literature. It is the **clinical-practice side** of the dominance-theory contradiction and one of the four canonical post-correction nodes in the temporal chain seeded for this corpus.

## What the source reported

The position statement's load-bearing claim, quoted in multiple independent third-party reproductions of the document:

> "Most undesirable behaviors in our pets are not related to priority access to resources; rather, they are due to accidental rewarding of the undesirable behavior."

This sentence does specific work. It identifies the *explanatory framework* that dominance theory imports into clinical practice — the assumption that pet misbehavior reflects a struggle for "priority access to resources" — and rejects it in favor of a learning-theory account: behaviors persist because they are reinforced, intentionally or otherwise. The recommended alternative, stated throughout the document and reflected in AVSAB's broader resource library, is reward-based / positive-reinforcement training.

The statement is short (a one-page position document on AVSAB letterhead) and is distributed publicly on AVSAB's own site for clinician use, owner handouts, and citation in subsequent veterinary-behavior literature.

## Why this fits the corpus

This note binds the **clinical-practice arm** of the Cat 3 contradiction pair `dominance_theory_pre_vs_post_1999`:

- **Cat 3 (contradiction).** AVSAB 2008 declares a `contradicts` edge to Schenkel 1947 — not because AVSAB cites Schenkel by name in the position statement, but because the explanatory framework AVSAB rejects ("priority access to resources / dominance hierarchy") is the framework whose academic foundation is Schenkel-derived captive-wolf observations. The contradiction is at the level of the explanatory model, not specific quotation.
- **Cat 6 (temporal).** AVSAB 2008 declares a `supersedes` edge to Schenkel 1947 in the clinical-practice register, paralleling the academic supersession that Mech 1999 supplies. Together they bound the 1947 → 1999 → 2008 segment of the temporal chain `dominance_to_positive_reinforcement`.
- **Cat 4 (alias / canonicalization).** The `concept_dominance_theory` entity reused here is the same id introduced by the Schenkel 1947 note and reused by Mech 1999. A system that fragments dominance theory into multiple distinct concept entities across these three notes is failing the alias-resolution test even within a single domain's vocabulary.

The `concept_dominance_theory` entity is **reused** (not redeclared). The `concept_positive_reinforcement_training` entity is introduced here for the first time and is referenced by edges, so it does not orphan.

## Provenance and limitations

Direct WebFetch of the avsab.org PDF was denied in this authoring session. The quoted "priority access to resources / accidental rewarding" passage is reported from search-engine summaries that cite the same canonical AVSAB URL; the same passage appears in independent third-party reproductions of the document on caninewelfare.centers.purdue.edu (Purdue Canine Welfare Science Center) and at the Internet Archive mirror, which provides cross-source confirmation that the quote is not fabricated by any single secondary site.

The Internet Archive mirror at `https://archive.org/details/dominance-position-statement` is the recommended fallback for any future re-verification. The AVSAB position-statements index at `https://avsab.org/resources/position-statements/` lists the 2008 statement among AVSAB's currently-active positions.

The `regulates` edge from AVSAB to dominance theory is flagged `needs_grounding: true` because AVSAB's `is_regulatory` flag is `false` (it is a professional society, not a statutory regulator); the edge is recorded in the corpus to capture professional-jurisdictional authority but should be reviewed when v0.2 of the ontology distinguishes statutory regulation from professional-society guidance.

## Sources

- AVSAB Position Statement (canonical URL of record): https://avsab.org/wp-content/uploads/2018/03/Dominance_Position_Statement_download-10-3-14.pdf
- AVSAB position statements index: https://avsab.org/resources/position-statements/
- Internet Archive mirror: https://archive.org/details/dominance-position-statement
- Purdue Canine Welfare Science Center reproduction: https://caninewelfare.centers.purdue.edu/resource/dominance-position-statement/
