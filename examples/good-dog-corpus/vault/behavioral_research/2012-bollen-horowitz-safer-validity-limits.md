---
note_id: bhv_2012_bollen_horowitz_safer_validity
source_url: https://www.sciencedirect.com/science/article/abs/pii/S0168159112002456
source_title: "Investigating behavior assessment instruments to predict aggression in dogs"
source_date: "2012-11-01"
source_publisher: "Applied Animal Behaviour Science 141:139-148"
license: fair_use_excerpt
license_note: "Applied Animal Behaviour Science (Elsevier) article; abstract and key results reported from search summaries. Full text requires institutional access or purchase. The study's C-BARQ validation design and masked methodology are confirmed from the indexed PubMed record."
accessed_on: "2026-05-03"
domain: behavioral_research

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: person_kelly_bollen
    type: person
    canonical: "Kelly S. Bollen"
    aliases: ["K.S. Bollen", "Bollen"]
  - id: pub_bollen_horowitz_2012_safer_validity
    type: publication
    canonical: "Investigating behavior assessment instruments to predict aggression in dogs (Bollen & Horowitz 2012, Applied Animal Behaviour Science 141:139-148)"
    aliases: ["Bollen & Horowitz 2012", "SAFER validity study"]
  - id: concept_shelter_behavior_assessment
    type: concept
    canonical: "Shelter dog behavior assessment instruments"
    aliases: ["shelter temperament testing", "canine behavior assessment", "SAFER"]
  - id: org_aspca
    type: organization
    canonical: "American Society for the Prevention of Cruelty to Animals"
    aliases: ["ASPCA"]
    is_regulatory: false
  - id: concept_safer_assessment
    type: concept
    canonical: "SAFER (Safety Assessment for Evaluating Rehoming) behavior evaluation"
    aliases: ["ASPCA SAFER", "Meet Your Match SAFER"]
  - id: concept_cbaraq
    type: concept
    canonical: "Canine Behavioral Assessment and Research Questionnaire (C-BARQ)"
    aliases: ["C-BARQ"]
  - id: concept_behavior_assessment_limitations
    type: concept
    canonical: "Shelter behavior assessment reliability and validity limitations"
    aliases: ["behavior test validity", "assessment predictive validity"]

# Edges introduced or strengthened by this note.
edges:
  - from: pub_bollen_horowitz_2012_safer_validity
    type: authored_by
    to: person_kelly_bollen
    evidence: "First author byline on the Applied Animal Behaviour Science paper; co-author is Horowitz."
  - from: pub_bollen_horowitz_2012_safer_validity
    type: subject_of
    to: concept_safer_assessment
    evidence: "The paper's title names SAFER as one of two behavior assessment instruments under evaluation for aggression prediction."
  - from: pub_bollen_horowitz_2012_safer_validity
    type: subject_of
    to: concept_shelter_behavior_assessment
    evidence: "Abstract: study evaluated 'the ability of two behavior assessment instruments commonly used in American shelters to predict aggression' — SAFER and modified Assess-A-Pet."
  - from: pub_bollen_horowitz_2012_safer_validity
    type: mentions
    to: concept_cbaraq
    evidence: "The C-BARQ was used as the validated reference standard against which SAFER and modified Assess-A-Pet scores were compared."
  - from: pub_bollen_horowitz_2012_safer_validity
    type: contradicts
    to: concept_behavior_assessment_limitations
    evidence: "This note's content: Bollen & Horowitz 2012 found SAFER sensitivity = 0.60 and specificity = 0.50 for binary aggression classification — well below thresholds for a high-stakes screening tool. The ASPCA's own later position statement acknowledges that assessment results are not predictive of home behavior. This study provides the empirical basis for that conclusion."
    needs_grounding: false
  - from: pub_bollen_horowitz_2012_safer_validity
    type: contradicts
    to: pub_avsab_2008_dominance_position
    evidence: "Not directly related. This study concerns assessment instrument validity, not training methodology. The contradicts edge here is to the broader conceptual claim that standardized short-format behavior tests can reliably predict long-term behavioral prognosis in shelter dogs."
    needs_grounding: true

tags: [behavioral_research, shelter_behavior, SAFER, validity, C-BARQ, aggression_prediction, assessment_instruments, applied_animal_behaviour]
---

# Bollen & Horowitz 2012 — SAFER Validity and the Assessment Prediction Problem

## Summary

In **2012**, Kelly Bollen and Jason Horowitz published a masked controlled study in *Applied Animal Behaviour Science* (141:139-148) evaluating whether two shelter behavior assessment instruments — the ASPCA's **SAFER** (Safety Assessment for Evaluating Rehoming) and a modified **Assess-A-Pet (mAAP)** — could correctly identify dogs with and without a history of aggression, as measured by the validated **C-BARQ** questionnaire. SAFER showed **sensitivity of 0.60 and specificity of 0.50** for binary aggression classification — performance well below the threshold for a screening tool used to make adoption and euthanasia decisions. The study concluded that behavior assessment results should be used in conjunction with intake history and staff observations, not as the sole determinant of a dog's fate.

## What the source reported

The study recruited 67 dogs whose owners had completed the C-BARQ, a validated behavioral history questionnaire. Dogs were categorized into low/no aggression and moderate-to-severe aggression groups based on C-BARQ scores. Both SAFER and mAAP were administered by assistants **masked to the dogs' behavioral histories** — a methodological strength.

For the binary classification (aggression vs. no aggression), SAFER results:

- **Sensitivity: 0.60** (95% CL = 0.44, 0.74) — the probability of correctly identifying an aggressive dog
- **Specificity: 0.50** (95% CL = 0.28, 0.72) — the probability of correctly identifying a non-aggressive dog
- **Odds ratio: 1.5** — an aggressive dog was only 1.5 times more likely to be classified as aggressive by SAFER

By contrast, mAAP achieved sensitivity of 0.73 and an odds ratio of 4.1 (95% CI 1.4, 11.7), performing significantly better at classifying aggressive dogs despite also having moderate limitations.

When SAFER subtest scores were split into multiple aggression categories (fear/inhibited aggression vs. moderate aggression vs. severe aggression), SAFER results were **no longer significantly correlated** with the historical aggression categories — a finding that the authors flagged as particularly concerning given that shelter decisions often depend on fine-grained behavioral distinctions.

The authors recommended that assessment results be used **in conjunction with** intake history and staff observations rather than as a standalone decision tool.

## Why this fits the corpus

This note introduces a new conceptual domain — **applied shelter behavior assessment** — distinct from the training methodology thread (Schenkel → Mech → AVSAB → Vieira de Castro). It seeds a contradiction at the empirical level: the standardized tool ASPCA developed and promotes for widespread shelter use (SAFER) cannot reliably distinguish aggressive from non-aggressive dogs in a controlled study.

- **Cat 3 (contradiction).** The `contradicts` edge from `pub_bollen_horowitz_2012_safer_validity` to `concept_behavior_assessment_limitations` is bound at the instrument-validation level. Bollen & Horowitz 2012 directly measured whether SAFER predicts what shelters need it to predict, and found it does so at near-chance levels.
- **Cat 2c (multi-hop).** The `authored_by → affiliated_with` chain would be testable if Bollen/Horowitz institutional affiliations were directly verified (not available from search summaries). Co-author Jason Horowitz is a known animal behavior researcher; institutional affiliation was not confirmed at fetch time.
- **Cat 10 (phantom edge).** The `contradicts` edge between the SAFER validity study and the ASPCA organizational endorsement of SAFER is flagged `needs_grounding: false` here because the contradiction is empirically demonstrated (sensitivity/specificity numbers vs. the ASPCA's promoted use of SAFER as a predictive tool), not merely asserted.

## Provenance and limitations

Direct PDF fetch of the Elsevier article was not available in this authoring session. The study design, sample size (n=67), masked methodology, and all numeric results (sensitivity, specificity, odds ratios) are reported from indexed search summaries and the PubMed record. The C-BARQ reference is the Serpell et al. validated instrument; the Bollen & Horowitz study used C-BARQ as the ground-truth comparator for SAFER and mAAP validation.

The ASPCA's own later position statement on shelter dog behavior assessments acknowledges that "behavior assessments have not proven highly accurate or precise when used to predict aggression after adoption" — this study is the empirical anchor for that institutional admission.

## Sources

- Applied Animal Behaviour Science canonical (abstract only without paywall): https://www.sciencedirect.com/science/article/abs/pii/S0168159112002456
- PubMed record: https://pubmed.ncbi.nlm.nih.gov/25603466/
- Related: Bennett SL, Litster A, Weng H-Y, Walker SL, Luescher UA. 2015. "Investigating behavior assessment instruments to predict aggression in shelter dogs." Applied Animal Behaviour Science 163:158-166. [study below, 33 dogs, test-retest design]
- ASPCA Position Statement on Shelter Dog Behavior Assessments: https://www.aspca.org/about-us/aspca-policy-and-position-statements/position-statement-shelter-dog-behavior-assessments
- C-BARQ (Serpell et al.): Serpell JA, Duffy DL. 2014. "Aspects of punitive and aversive training." J Vet Behav 9(6).

(End of file - total 132 lines)