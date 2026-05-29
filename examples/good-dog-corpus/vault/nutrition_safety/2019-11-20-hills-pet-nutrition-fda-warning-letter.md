---
note_id: nut_2019_11_hills_warning_letter
source_url: https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/hills-pet-nutrition-inc-576564-11202019
source_title: "Hill's Pet Nutrition Inc. - 576564 - 11/20/2019"
source_date: "2019-11-20"
source_publisher: "U.S. Food and Drug Administration"
license: public_domain
license_note: "U.S. federal government work, 17 U.S.C. § 105"
accessed_on: "2026-04-30"
domain: nutrition_safety
lifecycle_id: hills_vitamin_d_2019_recall

# Reuses entities from prior three notes; introduces only the warning-letter
# publication node and the regulatory-followup event.
entities:
  - id: pub_hills_warning_letter_2019_11
    type: publication
    canonical: "FDA Warning Letter to Hill's Pet Nutrition Inc., MARCS-CMS 576564 (2019-11-20)"
  - id: event_hills_warning_letter_2019_11
    type: event
    canonical: "FDA Warning Letter issued to Hill's Pet Nutrition (regulatory followup to 2019 vitamin D recall)"
    timestamp: "2019-11-20"
    status: resolved

edges:
  # The third supersession edge — Warning Letter is the regulatory-followup
  # stage that closes the public-facing lifecycle past the May expansion.
  - from: pub_hills_warning_letter_2019_11
    type: supersedes
    to: pub_hills_vitd_expansion_2019_05
    evidence: "FDA Warning Letter is dated 2019-11-20, six months after the May 20 expansion; it is the regulatory-followup stage that documents inspection findings stemming from the same vitamin D contamination event the May expansion belongs to, closing the public-facing recall-lifecycle chain"
  - from: pub_hills_warning_letter_2019_11
    type: subject_of
    to: event_hills_warning_letter_2019_11
    evidence: "Publication is the canonical record of the Nov 20 2019 Warning Letter event"
  - from: pub_hills_warning_letter_2019_11
    type: authored_by
    to: org_us_fda
    evidence: "Warning Letter issued by FDA's Center for Veterinary Medicine; hosted on fda.gov in the warning-letters directory"
  - from: pub_hills_warning_letter_2019_11
    type: mentions
    to: org_hills_pet_nutrition
    evidence: "Warning Letter is addressed to Hill's Pet Nutrition Inc., the recipient firm"
  - from: pub_hills_warning_letter_2019_11
    type: mentions
    to: concept_vitamin_d_toxicity
    evidence: "Letter cites unsafe vitamin D levels in finished animal food as the underlying violation"
  - from: pub_hills_warning_letter_2019_11
    type: cites
    to: pub_hills_vitd_announcement_2019_01
    evidence: "Letter explicitly references the Jan 2019 recall (and subsequent expansions) as the events that triggered the FDA inspections of the Topeka, KS facility"
  - from: org_us_fda
    type: regulates
    to: org_hills_pet_nutrition
    evidence: "Warning Letter cites violations of the Federal Food, Drug, and Cosmetic Act and FSMA preventive-controls regulation, asserting FDA jurisdiction over Hill's animal-food manufacturing"
    needs_grounding: true

tags: [nutrition_safety, recall, hills, vitamin_d, lifecycle_regulatory_followup, fda, warning_letter, supersedes_chain]
---

# FDA Warning Letter to Hill's Pet Nutrition Inc. (MARCS-CMS 576564, Nov 20 2019)

## Summary

On **November 20, 2019**, the FDA issued a Warning Letter (MARCS-CMS 576564) to Hill's Pet Nutrition Inc. as a regulatory followup to the 2019 vitamin D contamination recalls. According to search-engine summaries of the source page and a PDF of the letter mirrored at petful.com, the letter consolidates findings from FDA inspections of Hill's facility at **320 NE Crane St., Topeka, Kansas**, conducted **February 1 through February 19, 2019** and **March 25 through 27, 2019** — inspections triggered by the firm's Reportable Food Registry filing and by the recall of products with toxic levels of vitamin D.

This is the **regulatory-followup stage** of the Hill's vitamin D 2019 lifecycle and the fourth and final document in the Cat 6 supersedes chain documented in `sources/nutrition_safety.yaml`.

## What the FDA reported

According to the search-engine summary of the source page (the maintainer was unable to fetch the live FDA URL directly — see "Provenance and limitations"):

- FDA inspections confirmed that animal food products with **unsafe levels of vitamin D** were manufactured and marketed by the firm.
- The unsafe vitamin D levels were the result of an ingredient (the vitamin premix) that was received and accepted in a manner not in accordance with the firm's own receiving procedures.
- Lot-specific testing reported in the letter (per the search-engine summary): lot code "BEST BEFORE 10 2020, T1911124 3912" measured **100,170 to 107,282 IU/kg of vitamin D**, and lot "BEST BEFORE 10 2020, T1911125 3912" measured **102,829 to 102,346 IU/kg** [sic, range as quoted] of vitamin D in canned dog food.
- AAFCO's 2017 Official Publication, cited as the safety reference, sets safe vitamin D levels for dog foods at **between 500 and 3,000 IU per kg**.
- The letter concluded that Hill's "did not sufficiently assess the probability that a vitamin D toxicity or deficiency hazard would occur," and "failed to implement a prerequisite program to ensure that the vitamin premix did not contain an excess of vitamin D."

## Why this closes the lifecycle chain

The Warning Letter sits at the end of the public-facing lifecycle for three structural reasons:

1. It is the **last document** in the chain that the FDA publishes about this incident on its own canonical URLs — subsequent activity (Hill's response, FDA close-out, civil litigation) is either internal correspondence or not part of the FDA's safety-alert / warning-letter corpus.
2. It is **dated after the immediate recall is operationally closed** (the May 20 expansion's recall status was subsequently terminated per FDA records cited in `sources/nutrition_safety.yaml`), so the Warning Letter post-dates the recall's resolution.
3. It documents the **regulatory consequences** of the same contamination event the prior three documents tracked, citing the same vitamin premix root cause and the same recalled products.

This makes the chain structurally identical to the Mid-America Pet Food / Victor brand 2023-2024 lifecycle described in `sources/nutrition_safety.yaml#recall_lifecycles`: announcement → expansion(s) → resolution → regulatory followup.

## Lifecycle position (final state)

```
pub_hills_vitd_announcement_2019_01   (Jan 31 2019, announcement)
              ▲
              │ supersedes
              │
pub_hills_vitd_expansion_2019_03      (Mar 20 2019, expansion)
              ▲
              │ supersedes
              │
pub_hills_vitd_expansion_2019_05      (May 20 2019, second expansion / resolution)
              ▲
              │ supersedes
              │
pub_hills_warning_letter_2019_11      (Nov 20 2019, regulatory followup)
```

Three `supersedes` edges, four publication nodes, one shared `event_hills_vitd_recall_2019` underlying recall event referenced as `subject_of` from each of the first three publications, and one separate `event_hills_warning_letter_2019_11` event for the followup stage.

## Provenance and limitations

Direct WebFetch against `fda.gov` returned HTTP 404 from this client. All factual claims above — including the lot code identifiers, the IU/kg measurements, and the quoted regulatory findings — are sourced from search-engine summaries of the FDA URL of record. Independent corroboration is available from a PDF mirror of the letter hosted at petful.com and from coverage at Food Safety News, AVMA JAVMA News, Pet Food Processing, and PetfoodIndustry; these are not used as primary sources here but are listed below as cross-reference sources for downstream verification.

A future revision of this note should re-fetch the canonical fda.gov URL directly and verify each quoted measurement and citation against the live page text. The frontmatter `source_url` is the canonical URL of record.

## Sources

- FDA Warning Letter — Hill's Pet Nutrition Inc., MARCS-CMS 576564, Nov 20 2019 (canonical URL of record): https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/hills-pet-nutrition-inc-576564-11202019
- Mirrored PDF of the Warning Letter (petful.com): https://www.petful.com/wp-content/uploads/2020/06/Hills-Pet-Nutrition-Warning-Letter-from-FDA-Nov2019.pdf
- Food Safety News coverage: https://www.foodsafetynews.com/2019/12/fda-issues-warning-letters-to-friendlys-for-ice-cream-plant-and-hills-pet-nutrition-for-vitamin-d/
- AVMA JAVMA News coverage: https://www.avma.org/javma-news/2020-02-15/update-fda-says-hills-failed-follow-own-procedures
- Pet Food Processing coverage: https://www.petfoodprocessing.net/articles/13519-fda-warns-hills-pet-nutrition-for-violating-fdc-fsma-regulations
