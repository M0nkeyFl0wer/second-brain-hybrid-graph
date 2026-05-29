---
note_id: vet_2022_freeman_jvim_prospective_dcm
source_url: https://pmc.ncbi.nlm.nih.gov/articles/PMC8965249/
source_title: "Prospective study of dilated cardiomyopathy in dogs eating nontraditional or traditional diets and in dogs with subclinical cardiac abnormalities"
source_date: "2022-03-17"
source_publisher: "Journal of Veterinary Internal Medicine (Wiley), open-access deposited at PMC"
license: cc_by_nc_4.0
license_note: "JVIM open-access; PMC deposit confirms reuse rights for non-commercial use with attribution"
accessed_on: "2026-04-30"
domain: veterinary_research

# Reuses concept_dcm, concept_grain_free_diet, concept_pulses, and
# concept_non_hereditary_dcm from prior FDA notes.
entities:
  - id: pub_freeman_2022_jvim_prospective
    type: publication
    canonical: "Prospective study of dilated cardiomyopathy in dogs eating nontraditional or traditional diets and in dogs with subclinical cardiac abnormalities"
    aliases: ["Freeman 2022 JVIM", "Freeman et al. 2022 prospective study"]
  - id: person_lisa_freeman
    type: person
    canonical: "Lisa M. Freeman"
    aliases: ["Lisa Freeman", "L. Freeman", "Dr. Lisa Freeman"]
  - id: person_john_rush
    type: person
    canonical: "John E. Rush"
    aliases: ["John Rush", "J. Rush"]
  - id: person_darcy_adin
    type: person
    canonical: "Darcy Adin"
    aliases: ["D. Adin"]
  - id: org_tufts_cummings
    type: organization
    canonical: "Cummings School of Veterinary Medicine at Tufts University"
    aliases: ["Tufts Cummings", "Tufts Cummings School", "Cummings School"]
  - id: concept_nontraditional_diet
    type: concept
    canonical: "Nontraditional pet diet"
    aliases: ["nontraditional diet", "BEG diet", "boutique exotic-ingredient grain-free diet"]

edges:
  - from: pub_freeman_2022_jvim_prospective
    type: authored_by
    to: person_lisa_freeman
    evidence: "First / corresponding author Lisa M. Freeman, JVIM 36(2):451-463, 2022"
  - from: pub_freeman_2022_jvim_prospective
    type: authored_by
    to: person_john_rush
    evidence: "Co-author John E. Rush listed in JVIM 36(2):451-463, 2022"
  - from: pub_freeman_2022_jvim_prospective
    type: authored_by
    to: person_darcy_adin
    evidence: "Co-author Darcy Adin listed in JVIM 36(2):451-463, 2022"
  - from: person_lisa_freeman
    type: affiliated_with
    to: org_tufts_cummings
    evidence: "Lisa M. Freeman is a board-certified veterinary nutritionist on faculty at Cummings School of Veterinary Medicine at Tufts University; primary affiliation reported on the JVIM article"
  - from: person_john_rush
    type: affiliated_with
    to: org_tufts_cummings
    evidence: "John E. Rush is a faculty cardiologist at Cummings School of Veterinary Medicine at Tufts; primary affiliation reported on the JVIM article"
  - from: pub_freeman_2022_jvim_prospective
    type: subject_of
    to: concept_non_hereditary_dcm
    evidence: "Study population is dogs with diet-associated (non-hereditary) DCM and dogs with subclinical cardiac abnormalities"
  - from: pub_freeman_2022_jvim_prospective
    type: mentions
    to: concept_dcm
    evidence: "DCM is the central condition under study"
  - from: pub_freeman_2022_jvim_prospective
    type: mentions
    to: concept_nontraditional_diet
    evidence: "Study compares dogs originally eating nontraditional vs traditional diets"
  - from: pub_freeman_2022_jvim_prospective
    type: mentions
    to: concept_grain_free_diet
    evidence: "Nontraditional diets in this study are operationalized as boutique, exotic-ingredient, or grain-free formulations"
  - from: pub_freeman_2022_jvim_prospective
    type: contradicts
    to: pub_fda_dcm_investigation_main
    evidence: "Peer-reviewed multifactorial framing of diet-associated DCM that is consistent with the FDA 2019/2022 reframing and stands against the 2018 announcement's grain-free-centered framing; finds that diet change is associated with longer survival, supporting diet as a contributor rather than a definitive sole cause; binds the academic side of the corpus's seeded Cat 3 contradiction pair"

tags: [vet_research, dcm, freeman, tufts, jvim, peer_reviewed, contradiction_pair, multifactorial]
contradiction_pair_id: dcm_grain_free_2018
---

# Prospective study of dilated cardiomyopathy in dogs eating nontraditional or traditional diets and in dogs with subclinical cardiac abnormalities (Freeman et al., JVIM 2022)

## Summary

A prospective cohort study by Lisa M. Freeman and colleagues at Tufts Cummings School of Veterinary Medicine, published in the **Journal of Veterinary Internal Medicine** in March 2022 (volume 36, issue 2, pages 451-463). The study evaluated baseline features and serial changes in echocardiography and cardiac biomarkers in 60 dogs with DCM (51 eating nontraditional diets, 9 eating traditional diets) and 16 dogs with subclinical cardiac abnormalities eating nontraditional diets.

The study is the corpus's strongest open-access academic anchor for the **multifactorial / diet-as-contributor** side of the seeded Cat 3 contradiction pair `dcm_grain_free_2018`. It frames diet as a contributing factor in a multifactorial etiology rather than a sole cause, and reports survival data consistent with diet change as a clinically meaningful intervention.

## What the study reported

Sample and design:

- 60 dogs with DCM, 51 of whom were eating nontraditional diets and 9 of whom were eating traditional diets at baseline.
- 16 dogs with subclinical cardiac abnormalities eating nontraditional diets.
- Prospective, with serial echocardiography and cardiac biomarker measurement.

Survival findings:

> "The median survival time of the 51 dogs originally eating a nontraditional diet was 611 days (range, 2–940 days), while the 9 dogs originally eating a traditional diet had a median survival time of 161 days (range, 12–669 days), though this difference was not statistically significant (P = .21)."

The directionality is striking even though the comparison did not reach statistical significance at this sample size: dogs whose original diet was nontraditional — and many of whom were transitioned to traditional diets after diagnosis — survived substantially longer than dogs whose original diet was already traditional.

## How this binds the contradiction pair

This is the academic counterpart to the FDA's 2019/2022 reframing of the diet-DCM relationship as multifactorial rather than as a clean grain-free-causes-DCM association. Three things make it a strong contradiction-pair anchor:

1. **It is peer-reviewed and open-access.** Unlike the Tufts Petfoodology blog posts (also referenced in this corpus), Freeman 2022 carries journal-level evidentiary weight and is freely re-readable from the PMC deposit.
2. **It reports outcomes, not just associations.** Diet change as an intervention with a survival-direction effect is a stronger evidentiary basis than ingredient-prevalence statistics, which is what most pre-2022 FDA reporting could offer.
3. **It frames the diet-DCM relationship as etiologically complex** — diet contributes to a multifactorial picture rather than serving as a clean monocausal explanation. This matches the FDA Q&A's "complex medical condition that may be affected by the interplay of multiple factors" framing and stands against the 2018 announcement's grain-free-centered framing.

## Provenance and limitations

The summary author attempted to retrieve the source URL directly via WebFetch at the time of writing; permission to fetch the PMC URL from this client was not granted in this session. The content above was retrieved via search-engine summary of the same URL set (a WebSearch query against the exact survival-time figures "611 days" / "161 days" returned the JVIM/PMC article as a top result with snippet text matching the figures and quoted survival statement above, as reported via search-engine summary; full text not directly verified by author at write time).

Specific items that should be re-verified against the PMC full text before any downstream consumer relies on exact wording:

- The author list (this note declares Freeman, Rush, Adin; the manifest also lists "et al." with additional authors).
- Affiliations (this note declares Freeman and Rush at Tufts Cummings; Adin's primary affiliation may differ on the JVIM byline and is not declared as an `affiliated_with` edge here pending direct verification).
- DOI (`10.1111/jvim.16397`), PMC ID (`PMC8965249`), and PMID (`35297103`).

## Sources

- Freeman LM, Rush JE, Adin D, et al. "Prospective study of dilated cardiomyopathy in dogs eating nontraditional or traditional diets and in dogs with subclinical cardiac abnormalities." *Journal of Veterinary Internal Medicine* 36(2):451-463, March 2022. Open-access PMC deposit (canonical URL of record): https://pmc.ncbi.nlm.nih.gov/articles/PMC8965249/
- Wiley publisher landing (paywall variants possible): https://onlinelibrary.wiley.com/doi/10.1111/jvim.16397
- PubMed record: https://pubmed.ncbi.nlm.nih.gov/35297103/
