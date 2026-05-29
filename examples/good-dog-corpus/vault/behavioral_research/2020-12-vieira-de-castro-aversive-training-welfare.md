---
note_id: bhv_2020_vieira_de_castro_aversive_training_welfare
source_url: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0225023
source_title: "Does training method matter? Evidence for the negative impact of aversive-based methods on companion dog welfare"
source_date: "2020-12-16"
source_publisher: "PLOS ONE 15(12): e0225023"
license: cc_by_4.0
license_note: "PLOS ONE publishes under Creative Commons Attribution 4.0 (CC-BY 4.0); full-text quote and redistribute with attribution permitted. Most permissive license among the seeded behavioral_research sources."
accessed_on: "2026-04-30"
domain: behavioral_research

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: person_ana_catarina_vieira_de_castro
    type: person
    canonical: "Ana Catarina Vieira de Castro"
    aliases: ["A. C. Vieira de Castro", "Vieira de Castro AC"]
  - id: pub_vieira_de_castro_2020_plos
    type: publication
    canonical: "Does training method matter? Evidence for the negative impact of aversive-based methods on companion dog welfare (Vieira de Castro et al. 2020, PLOS ONE 15(12):e0225023)"
    aliases: ["Vieira de Castro 2020", "Vieira de Castro et al. 2020"]
  - id: concept_aversive_training
    type: concept
    canonical: "Aversive-based dog training methods"
    aliases: ["aversive training", "positive punishment", "negative reinforcement training"]

# Edges introduced or strengthened by this note.
edges:
  - from: pub_vieira_de_castro_2020_plos
    type: authored_by
    to: person_ana_catarina_vieira_de_castro
    evidence: "Vieira de Castro is the lead (first) author of the PLOS ONE article; full author list per the canonical PLOS record: Vieira de Castro AC, Fuchs D, Morello GM, Pastur S, de Sousa L, Olsson IAS."
  - from: pub_vieira_de_castro_2020_plos
    type: subject_of
    to: concept_aversive_training
    evidence: "Title and abstract identify aversive- vs reward-based training methods as the study's primary subject; 'aversive-based methods' appears in the title."
  - from: pub_vieira_de_castro_2020_plos
    type: mentions
    to: concept_positive_reinforcement_training
    evidence: "Abstract describes recruitment from 'three reward-based schools (Group Reward, n = 42)' and contrasts reward-based training with aversive and mixed approaches throughout."
  - from: pub_vieira_de_castro_2020_plos
    type: contradicts
    to: pub_schenkel_1947_wolf_expression
    evidence: "Vieira de Castro 2020 supplies modern empirical evidence that the training tradition descended from dominance theory (whose academic foundation is Schenkel 1947) is harmful to dog welfare: 'Dogs from Group Aversive displayed more stress-related behaviors ... exhibited higher post-training increases in cortisol levels ... were more pessimistic in the cognitive bias task than dogs from Group Reward.' Conclusion: 'aversive-based training methods, especially if used in high proportions, compromise the welfare of companion dogs both within and outside the training context.'"
    needs_grounding: true
  - from: pub_vieira_de_castro_2020_plos
    type: cites
    to: pub_avsab_2008_dominance_position
    evidence: "Modern dog-training-welfare literature in this lineage routinely cites the AVSAB position statements as the clinical-guidance backdrop for empirical work on aversive methods. The exact citation of AVSAB 2008 in Vieira de Castro 2020's references list was not verified by direct PDF fetch in this authoring session; flagged for human grounding."
    needs_grounding: true

tags: [behavioral_research, aversive_training, dog_welfare, empirical_study, plos_one, post_correction, open_access]
contradiction_pair_id: dominance_theory_pre_vs_post_1999
---

# Vieira de Castro et al. 2020 — Does training method matter?

## Summary

In **December 2020**, Vieira de Castro and colleagues published a controlled empirical study in *PLOS ONE* (15(12): e0225023, CC-BY 4.0) measuring the welfare effects of aversive-based vs reward-based dog training methods on **92 companion dogs** recruited from 7 training schools across Portugal. Dogs trained with aversive methods showed more stress-related behaviors, higher post-training cortisol, and a more pessimistic cognitive bias than dogs trained with reward-based methods. This is the **modern empirical endpoint** of the post-correction side of the dominance-theory contradiction — the kind of primary research that the 2008 AVSAB position statement anticipated and that updates to AVSAB's humane-training guidance (2021) draw on.

## What the source reported

From the abstract (per the PLOS ONE canonical record):

> "Ninety-two companion dogs were recruited from three reward-based schools (Group Reward, n = 42), and from four aversive-based schools, two using low proportions of aversive-based methods (Group Mixed, n = 22) and two using high proportions of aversive-based methods (Group Aversive, n = 28)."

Outcome measures:

> "Dogs from Group Aversive displayed more stress-related behaviors, were more frequently in tense and low behavioral states and panted more during training, and exhibited higher post-training increases in cortisol levels than dogs from Group Reward. Additionally, dogs from Group Aversive were more 'pessimistic' in the cognitive bias task than dogs from Group Reward."

Conclusion:

> "These findings indicate that aversive-based training methods, especially if used in high proportions, compromise the welfare of companion dogs both within and outside the training context."

Publication metadata: PLOS ONE 15(12): e0225023, DOI `10.1371/journal.pone.0225023`, published 2020-12-16, license CC-BY 4.0. Full author list: Vieira de Castro AC, Fuchs D, Morello GM, Pastur S, de Sousa L, Olsson IAS.

## Why this fits the corpus

This note caps the post-correction arm of the Cat 3 / Cat 6 chain with **modern empirical primary research**, distinct from professional-body opinion (AVSAB 2008/2021) or wolf-behavior reframing (Mech 1999):

- **Cat 3 (contradiction).** The `contradicts` edge from `pub_vieira_de_castro_2020_plos` to `pub_schenkel_1947_wolf_expression` is bound at the empirical-evidence level: the captive-wolf dominance framework underwrites aversive training methodology, and Vieira de Castro 2020 measures direct welfare harms from that methodology in companion dogs. The contradiction is not at the species level (wolves vs dogs) but at the level of the training-tradition descended from the dominance framing.
- **Cat 6 (temporal).** Vieira de Castro 2020 sits at year 2020 in the temporal chain `dominance_to_positive_reinforcement`, between the 2017 Ziv literature review and the 2021 AVSAB humane-training position statement (neither of which has been authored as a vault note in this batch).
- **Open-access citability.** PLOS ONE's CC-BY 4.0 license makes this the most permissive source in the seeded behavioral_research manifest; quotes above are explicitly within the license terms.

The `concept_dominance_theory` entity is not introduced or referenced by this note (Vieira de Castro 2020 is downstream of the conceptual reframing and does not invoke "dominance theory" as such); the contradicts/supersedes binding to Schenkel 1947 is the way this note participates in the seeded pair.

## Provenance and limitations

Direct WebFetch of the PLOS ONE article page was denied in this authoring session. All quoted passages above are reported from search-engine summaries citing the same canonical PLOS URL. The quotes appear consistently across multiple independent search excerpts and are reproduced word-for-word in the PubMed abstract record (`https://pubmed.ncbi.nlm.nih.gov/33326450/`) and the PMC mirror, which provides cross-source verification.

The `cites` edge from Vieira de Castro 2020 to AVSAB 2008 is plausible but not directly verified; it is flagged `needs_grounding: true` so the corpus maintainer can confirm against the paper's References section in a future revision.

## Sources

- PLOS ONE canonical article (URL of record): https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0225023
- PLOS printable PDF: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0225023&type=printable
- PMC mirror: https://pmc.ncbi.nlm.nih.gov/articles/PMC7743949/
- PubMed abstract: https://pubmed.ncbi.nlm.nih.gov/33326450/
- Primary publication: Vieira de Castro AC, Fuchs D, Morello GM, Pastur S, de Sousa L, Olsson IAS. 2020. "Does training method matter? Evidence for the negative impact of aversive-based methods on companion dog welfare." *PLOS ONE* 15(12): e0225023. DOI 10.1371/journal.pone.0225023. CC-BY 4.0.
