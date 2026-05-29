---
note_id: nut_2019_03_hills_vitd_expansion
source_url: https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/hills-pet-nutrition-expands-voluntary-recall-select-canned-dog-food-elevated-vitamin-d
source_title: "Hill's Pet Nutrition Expands Voluntary Recall of Select Canned Dog Food for Elevated Vitamin D"
source_date: "2019-03-20"
source_publisher: "U.S. Food and Drug Administration"
license: public_domain
license_note: "U.S. federal government work, 17 U.S.C. § 105"
accessed_on: "2026-04-30"
domain: nutrition_safety
lifecycle_id: hills_vitamin_d_2019_recall

# Ontology-aligned entity declarations introduced by this note.
# Reuses org_hills_pet_nutrition, brand_hills_science_diet,
# brand_hills_prescription_diet, concept_vitamin_d_toxicity,
# event_hills_vitd_recall_2019, and pub_hills_vitd_announcement_2019_01
# from the Jan 31 2019 announcement note.
entities:
  - id: pub_hills_vitd_expansion_2019_03
    type: publication
    canonical: "Hill's Pet Nutrition Expands Voluntary Recall of Select Canned Dog Food for Elevated Vitamin D (2019-03-20)"

# Edges introduced or strengthened by this note.
edges:
  # The supersession edge — March expansion supersedes January announcement.
  - from: pub_hills_vitd_expansion_2019_03
    type: supersedes
    to: pub_hills_vitd_announcement_2019_01
    evidence: "Source explicitly identifies the March 20 2019 expansion as covering additional products affected by the same vitamin premix that was the source of the January 31 2019 recall, expanding the prior recall's product list"
  - from: pub_hills_vitd_expansion_2019_03
    type: subject_of
    to: event_hills_vitd_recall_2019
    evidence: "Publication is the FDA-published expansion notice for the same underlying recall event"
  - from: pub_hills_vitd_expansion_2019_03
    type: authored_by
    to: org_us_fda
    evidence: "Hosted on fda.gov as an FDA-published safety alert reproducing the firm's expanded recall notice"
  - from: pub_hills_vitd_expansion_2019_03
    type: mentions
    to: org_hills_pet_nutrition
    evidence: "Recall expansion issued by Hill's Pet Nutrition; firm named throughout"
  - from: pub_hills_vitd_expansion_2019_03
    type: mentions
    to: brand_hills_science_diet
    evidence: "Expanded recall lists Hill's Science Diet varieties"
  - from: pub_hills_vitd_expansion_2019_03
    type: mentions
    to: brand_hills_prescription_diet
    evidence: "Expanded recall lists Hill's Prescription Diet varieties"
  - from: pub_hills_vitd_expansion_2019_03
    type: mentions
    to: concept_vitamin_d_toxicity
    evidence: "Source attributes the expansion to elevated vitamin D from the same vitamin premix"

tags: [nutrition_safety, recall, hills, vitamin_d, lifecycle_expansion, fda, supersedes_chain]
---

# Hill's Pet Nutrition Expands Voluntary Recall of Select Canned Dog Food for Elevated Vitamin D (Mar 20 2019)

## Summary

On **March 20, 2019**, Hill's Pet Nutrition expanded its January 31 2019 voluntary recall of select canned dog foods to cover additional products affected by the **same vitamin premix** that caused the original recall. According to the FDA notice (as reflected in search-engine summaries and AVMA JAVMA News coverage citing the FDA page), the expansion brought the recall to a total of **85 lots across 33 varieties** of canned dog food marketed under Hill's Science Diet and Hill's Prescription Diet brands.

This is the **first expansion stage** of the Hill's vitamin D 2019 lifecycle. The temporal chain edge is `(pub_hills_vitd_expansion_2019_03)-[supersedes]->(pub_hills_vitd_announcement_2019_01)`.

## What was newly recalled

The expansion added previously unrecalled SKUs whose lot codes traced back to the same contaminated vitamin premix lot from Hill's U.S. supplier. Specific SKU and lot identifiers are listed on the FDA page; this summary does not reproduce them because the maintainer could not directly fetch the source page (see "Provenance and limitations").

## What the FDA and Hill's reported

According to the source notice and corroborating coverage:

- The expansion was caused by the same vitamin premix received from a U.S. supplier that was the source of the January 31, 2019 recall.
- It was being conducted in cooperation with the U.S. Food and Drug Administration.
- Hill's stated that its review determined there were additional products affected by the vitamin premix, and that this was the reason for the expansion.
- The clinical signs of vitamin D toxicity described matched the January announcement: vomiting, loss of appetite, increased thirst and urination, excessive drooling, weight loss; at high levels, possibly life-threatening renal dysfunction.

## Lifecycle position

This note materializes the first `supersedes` edge in the Hill's 2019 chain:

```
pub_hills_vitd_announcement_2019_01  (Jan 31 2019, 25 products)
              ▲
              │ supersedes
              │
pub_hills_vitd_expansion_2019_03    (Mar 20 2019, 85 lots / 33 varieties)
```

The edge is grounded in explicit source language: the March notice identifies its trigger as the same vitamin premix as the January recall and frames the action as expanding (i.e., replacing) the prior recall's product list.

## Provenance and limitations

As with the January 31 2019 announcement note, direct WebFetch against `fda.gov` returned HTTP 404 from this client. All factual claims above are sourced from search-engine summaries of the FDA URL of record plus corroborating coverage from AVMA JAVMA News, dvm360, Dog Food Advisor, and Longwood Vet Center that cited the same FDA page. SKU-level lot codes were not reproduced into this note.

## Sources

- Hill's Pet Nutrition Expands Voluntary Recall of Select Canned Dog Food for Elevated Vitamin D (FDA safety alert, Mar 20 2019, canonical URL of record): https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/hills-pet-nutrition-expands-voluntary-recall-select-canned-dog-food-elevated-vitamin-d
- AVMA JAVMA News coverage: https://www.avma.org/javma-news/2019-05-15/march-hills-expands-canned-dog-food-recall
- dvm360 coverage: https://www.dvm360.com/view/hill-s-expands-recall-products-containing-excess-vitamin-d
- Dog Food Advisor recall expansion summary: https://www.dogfoodadvisor.com/dog-food-recalls/hills-dog-food-recall-expands/
