---
note_id: vet_2022_fda_qa_non_hereditary_dcm
source_url: https://www.fda.gov/animal-veterinary/animal-health-literacy/questions-answers-fdas-work-potential-causes-non-hereditary-dcm-dogs
source_title: "Questions & Answers: FDA's Work on Potential Causes of Non-Hereditary DCM in Dogs"
source_date: "2022-11-01"
source_publisher: "U.S. Food and Drug Administration, Center for Veterinary Medicine"
license: public_domain
license_note: "U.S. federal government work, 17 U.S.C. § 105"
accessed_on: "2026-04-30"
domain: veterinary_research

# Reuses org_us_fda, concept_dcm, concept_grain_free_diet, and
# pub_fda_dcm_investigation_main from the existing 2018-07 FDA note.
# Reuses concept_pulses from the 2019 Third Status Report note.
entities:
  - id: pub_fda_dcm_qa_non_hereditary
    type: publication
    canonical: "Questions & Answers: FDA's Work on Potential Causes of Non-Hereditary DCM in Dogs"
    aliases: ["FDA non-hereditary DCM Q&A", "FDA DCM FAQ 2022"]
  - id: concept_non_hereditary_dcm
    type: concept
    canonical: "Non-hereditary canine dilated cardiomyopathy"
    aliases: ["non-hereditary DCM", "atypical DCM", "diet-associated DCM"]

edges:
  - from: pub_fda_dcm_qa_non_hereditary
    type: authored_by
    to: org_us_fda
    evidence: "Page is published by FDA / Center for Veterinary Medicine; byline FDA"
  - from: pub_fda_dcm_qa_non_hereditary
    type: subject_of
    to: concept_non_hereditary_dcm
    evidence: "Title and full document are about FDA's work on potential causes of non-hereditary DCM in dogs"
  - from: pub_fda_dcm_qa_non_hereditary
    type: mentions
    to: concept_dcm
    evidence: "DCM is the central subject of the Q&A document"
  - from: pub_fda_dcm_qa_non_hereditary
    type: mentions
    to: concept_grain_free_diet
    evidence: "Q&A discusses the historical association between grain-free diets and reported DCM cases"
  - from: pub_fda_dcm_qa_non_hereditary
    type: mentions
    to: concept_pulses
    evidence: "Q&A discusses ingredient sourcing and formulation, including pulse ingredients (peas, lentils) raised in earlier status reports"
  - from: org_us_fda
    type: regulates
    to: concept_grain_free_diet
    evidence: "Q&A states FDA 'is a regulatory agency and has regulatory authority over animal food, including pet food', explaining the agency's focus on diet as a potential contributor"
  - from: pub_fda_dcm_qa_non_hereditary
    type: contradicts
    to: pub_fda_dcm_investigation_main
    evidence: "The Q&A explicitly states FDA 'has not taken regulatory action against or declared any specific pet food products unsafe or definitively linked to DCM' and reframes non-hereditary DCM as 'a complex medical condition that may be affected by the interplay of multiple factors such as genetics, underlying medical conditions, and diet' — a multifactorial framing that walks back the 2018 announcement's grain-free-centered framing without retracting any specific 2018 fact"

tags: [vet_research, dcm, fda, multifactorial, framing_shift, contradiction_pair, non_hereditary]
contradiction_pair_id: dcm_grain_free_2018
---

# Questions & Answers: FDA's Work on Potential Causes of Non-Hereditary DCM in Dogs

## Summary

This FDA Center for Veterinary Medicine Q&A page is the framing-shift document for the agency's diet-DCM investigation. As of its November 1, 2022 update, it characterizes non-hereditary DCM as a multifactorial condition — diet is one contributor, alongside genetics and underlying medical conditions — and explicitly notes that the agency has not taken regulatory action against or definitively linked any pet food product to DCM.

It is the third anchor in the corpus's Cat 3 contradiction pair `dcm_grain_free_2018`, alongside the 2018 main investigation page and the June 2019 Third Status Report.

## What the FDA Q&A states

On regulatory action and definitive linkage:

> "FDA has not taken regulatory action against or declared any specific pet food products unsafe or definitively linked to DCM."

On the multifactorial framing of non-hereditary DCM:

> "Emerging science appears to indicate that non-hereditary forms of DCM occur in dogs as a complex medical condition that may be affected by the interplay of multiple factors such as genetics, underlying medical conditions, and diet."

> "Aspects of diet that may interact with genetics and underlying medical conditions may include nutritional makeup of the ingredients and how dogs digest them, ingredient sourcing, processing, formulation, and/or feeding practices."

On why the agency keeps focusing on diet despite the multifactorial framing:

> "FDA is a regulatory agency and has regulatory authority over animal food, including pet food, thus the reason for the agency's focus on diet as a potential contributor."

On whether the diets should be removed from the market:

> "FDA has no definitive information indicating that the diets are inherently unsafe and need to be removed from the market, but the agency is continuing to work with stakeholders in assessing how the diets may interact with other factors that may be impacting non-hereditary DCM."

## The framing shift in plain terms

Three load-bearing changes from the 2018 announcement:

1. **From "grain-free association" to "multifactorial complex condition."** The 2018 framing centered grain-free diets; the Q&A centers the interplay of genetics, medical conditions, and diet — with diet itself further decomposed into ingredient nutrition, sourcing, processing, and formulation rather than the grain-free label.
2. **Explicit non-action.** No regulatory action has been taken; no product has been declared unsafe; no definitive link has been established. The agency keeps investigating because food is its statutory remit, not because the link is established.
3. **Coining of "non-hereditary DCM" as the corpus-of-interest term.** The Q&A reframes the question as "what causes non-hereditary DCM in dogs" rather than "is grain-free food causing DCM," which broadens the scientific question and narrows the regulatory implication.

This is the same investigation as the 2018 page; it is the corpus's seeded Cat 3 contradiction-pair anchor at id `dcm_grain_free_2018`. The contradiction is again **normative** — what the agency now emphasizes as load-bearing — rather than a retraction of any specific 2018 numerical finding.

## Provenance and limitations

The summary author attempted to retrieve the source URL directly via WebFetch at the time of writing; the fetch returned HTTP 404 from this client. The content above was retrieved via search-engine summary of the same URL set (multiple WebSearch queries against the canonical fda.gov path returned both the canonical URL and the cacmap.fda.gov mirror as live results, with snippet text matching every quoted statement above, as reported via search-engine summary; full text not directly verified by author at write time).

Pattern follows the existing 2018-07 FDA note in this domain. The 2022-11-01 source_date reflects the date of the report-count update on the page; the page itself is updated in place over time.

## Sources

- Questions & Answers: FDA's Work on Potential Causes of Non-Hereditary DCM in Dogs (canonical URL of record): https://www.fda.gov/animal-veterinary/animal-health-literacy/questions-answers-fdas-work-potential-causes-non-hereditary-dcm-dogs
- FDA Investigation into Potential Link between Certain Diets and Canine Dilated Cardiomyopathy (the 2018 main investigation page being reframed): https://www.fda.gov/animal-veterinary/outbreaks-and-advisories/fda-investigation-potential-link-between-certain-diets-and-canine-dilated-cardiomyopathy
- FDA Third Status Report (June 2019; the intermediate report in the same chain): https://www.fda.gov/animal-veterinary/cvm-updates/fda-provides-third-status-report-investigation-potential-connection-between-certain-diets-and-cases
