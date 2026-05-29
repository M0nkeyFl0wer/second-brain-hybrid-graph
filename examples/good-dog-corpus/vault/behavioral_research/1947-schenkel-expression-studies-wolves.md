---
note_id: bhv_1947_schenkel_expression_studies_wolves
source_url: https://davemech.org/wolf-news-and-information/schenkels-classic-wolf-behavior-study-available-in-english/
source_title: "Schenkel's Classic Wolf Behavior Study Available in English"
source_date: "1947"
source_publisher: "Behaviour 1:81-129 (original); davemech.org (English translation host)"
license: fair_use_excerpt
license_note: "Original Schenkel 1947 was published in journal Behaviour (Brill). English translation hosted by L. David Mech for scholarly access; treated as fair-use citation surrogate. Short quotes only; cite the Brill original as primary publication."
accessed_on: "2026-04-30"
domain: behavioral_research

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: person_rudolf_schenkel
    type: person
    canonical: "Rudolf Schenkel"
    aliases: ["Rudolph Schenkel"]
  - id: pub_schenkel_1947_wolf_expression
    type: publication
    canonical: "Expression Studies on Wolves (Schenkel 1947, Behaviour 1:81-129)"
    aliases: ["Schenkel 1947", "Expressions Studies on Wolves"]
  - id: concept_dominance_theory
    type: concept
    canonical: "Dominance theory (canine behavior)"
    aliases: ["alpha-wolf model", "dominance hierarchy model", "pack dominance theory"]
  - id: org_basel_zoo
    type: organization
    canonical: "Basel Zoo"
    aliases: ["Zoologischer Garten Basel"]
    is_regulatory: false

# Edges introduced or strengthened by this note.
edges:
  - from: pub_schenkel_1947_wolf_expression
    type: authored_by
    to: person_rudolf_schenkel
    evidence: "Sole author of the 1947 Behaviour paper; cited by name on davemech.org's announcement of the English translation."
  - from: pub_schenkel_1947_wolf_expression
    type: subject_of
    to: concept_dominance_theory
    evidence: "davemech.org states the study 'gave rise to the now outmoded notion of alpha wolves' and that wolves were observed to 'fight within a pack to gain dominance and that the winner is the alpha wolf' — i.e., the publication's primary subject is the dominance/alpha-wolf framing later imported into dog training."
  - from: pub_schenkel_1947_wolf_expression
    type: located_in
    to: org_basel_zoo
    evidence: "Search-engine summaries of the paper consistently state the observations were of captive wolves at Basel Zoo, Switzerland (the paper's study site)."
    needs_grounding: true
  - from: pub_schenkel_1947_wolf_expression
    type: mentions
    to: org_basel_zoo
    evidence: "Basel Zoo is named as the study site in derivative summaries of the paper."

tags: [behavioral_research, dominance_theory, wolves, schenkel, contradiction_pair_candidate, pre_correction]
contradiction_pair_id: dominance_theory_pre_vs_post_1999
---

# Schenkel 1947 — Expression Studies on Wolves

## Summary

In **1947**, Swiss animal behaviorist Rudolf Schenkel published "Expression Studies on Wolves" in the journal *Behaviour* (vol. 1, pages 81–129). The paper described a strict pack hierarchy among wolves with an "alpha" pair maintaining dominance through aggression. This framing — derived from observations of captive, unrelated wolves housed together at Basel Zoo — became the foundation for decades of subsequent dominance-based dog training advice. It is the **pre-correction pole** of the dominance-theory contradiction pair seeded in this corpus.

## What the source reported

According to the davemech.org announcement page (the canonical URL of record for this note), Schenkel's study "gave rise to the now outmoded notion of alpha wolves," based on observations that "wolves fight within a pack to gain dominance and that the winner is the 'alpha' wolf."

Search-engine summaries of the paper add detail not directly visible on the davemech.org page: Schenkel observed wolves in captivity at the Basel Zoo throughout the 1930s and 1940s; he characterized wolf social structure in terms of a "bitch wolf" (dominant female) and a "lead wolf" (dominant male); and the wolves under observation were unrelated adults forced into a shared enclosure — a configuration that does not occur in the wild. These contextual details are reported here as derived from search-engine summaries rather than verbatim from the paper text, because direct retrieval of the full English-translation PDF segments hosted on davemech.org was not available in this authoring session.

## Why this fits the corpus

This note seats the **origin node** of the Cat 3 / Cat 6 chain documented in `sources/behavioral_research.yaml`:

- **Cat 3 (contradiction).** Schenkel 1947 is one side of the seeded `contradicts` pair `dominance_theory_pre_vs_post_1999`. The opposing side is bound by Mech 1999 (next note), which explicitly retracts the captive-wolf basis as a description of natural pack structure.
- **Cat 6 (temporal).** Schenkel 1947 is the origin node of the temporal chain `dominance_to_positive_reinforcement` (origin year 1947). Subsequent notes (Mech 1999, AVSAB 2008) introduce `supersedes` edges back to this publication.

The `concept_dominance_theory` entity is introduced here so it can be reused (not redeclared) by every later note in this domain.

## Provenance and limitations

The davemech.org page was successfully fetched at WebFetch time and confirmed the "outmoded notion" framing and the alpha/dominance summary quoted above. Direct retrieval of the underlying English-translation PDF segments (the 10-page chunks `ExpressionstudiesP.1-10.pdf` and following) was not attempted in this authoring session. Claims about the Basel Zoo study site, the captive vs wild distinction, and Schenkel's "bitch wolf / lead wolf" terminology are therefore attributed to the davemech.org source URL with the caveat that they were retrieved via search-engine summary of derivative pages, not from the paper's body text.

The original 1947 publication in *Behaviour* (Brill) is the primary publication of record. Any future revision of this note that quotes paper text verbatim should cite the Brill original or the Internet Archive full-text mirror at `https://archive.org/details/SchenkelCaptiveWolfStudy.compressed`, not the davemech.org excerpts.

## Sources

- Schenkel's Classic Wolf Behavior Study Available in English (canonical URL of record for this note): https://davemech.org/wolf-news-and-information/schenkels-classic-wolf-behavior-study-available-in-english/
- Internet Archive full-text mirror (English translation, derivative): https://archive.org/details/SchenkelCaptiveWolfStudy.compressed
- Original primary publication (not directly fetched in this session): Schenkel, R. 1947. "Expression Studies on Wolves." *Behaviour* 1: 81-129. Brill.
