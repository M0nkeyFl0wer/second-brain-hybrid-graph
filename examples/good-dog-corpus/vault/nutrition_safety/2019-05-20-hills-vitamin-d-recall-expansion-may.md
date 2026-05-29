---
note_id: nut_2019_05_hills_vitd_expansion_may
source_url: https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/hills-pet-nutrition-additionally-expands-voluntary-recall-select-canned-dog-food-elevated-vitamin-d
source_title: "Hill's Pet Nutrition Additionally Expands Voluntary Recall of Select Canned Dog Food for Elevated Vitamin D"
source_date: "2019-05-20"
source_publisher: "U.S. Food and Drug Administration"
license: public_domain
license_note: "U.S. federal government work, 17 U.S.C. § 105"
accessed_on: "2026-04-30"
domain: nutrition_safety
lifecycle_id: hills_vitamin_d_2019_recall

# Reuses entities from the Jan 31 and Mar 20 notes; introduces only the
# stage publication node for the May 20 expansion.
entities:
  - id: pub_hills_vitd_expansion_2019_05
    type: publication
    canonical: "Hill's Pet Nutrition Additionally Expands Voluntary Recall of Select Canned Dog Food for Elevated Vitamin D (2019-05-20)"

edges:
  # The supersession edge — May expansion supersedes March expansion.
  - from: pub_hills_vitd_expansion_2019_05
    type: supersedes
    to: pub_hills_vitd_expansion_2019_03
    evidence: "Source describes May 20 2019 as an additional expansion of the same recall first expanded on March 20 2019, attributing the same vitamin premix root cause and updating the product/lot list"
  - from: pub_hills_vitd_expansion_2019_05
    type: subject_of
    to: event_hills_vitd_recall_2019
    evidence: "Publication is the FDA-published second-expansion notice for the same underlying recall event"
  - from: pub_hills_vitd_expansion_2019_05
    type: authored_by
    to: org_us_fda
    evidence: "Hosted on fda.gov as an FDA-published safety alert reproducing the firm's expanded recall notice"
  - from: pub_hills_vitd_expansion_2019_05
    type: mentions
    to: org_hills_pet_nutrition
    evidence: "Recall expansion issued by Hill's Pet Nutrition; firm named throughout"
  - from: pub_hills_vitd_expansion_2019_05
    type: mentions
    to: concept_vitamin_d_toxicity
    evidence: "Source identifies elevated vitamin D as the basis for the additional expansion"

tags: [nutrition_safety, recall, hills, vitamin_d, lifecycle_expansion, fda, supersedes_chain]
---

# Hill's Pet Nutrition Additionally Expands Voluntary Recall of Select Canned Dog Food for Elevated Vitamin D (May 20 2019)

## Summary

On **May 20, 2019**, Hill's Pet Nutrition issued a third FDA safety alert in the vitamin D recall sequence: a further "additional" expansion of the recall that began with the January 31 2019 announcement and was previously expanded on March 20 2019. According to search-engine summaries of the source page and corroborating coverage, this stage added an additional lot code that had been **inadvertently omitted from the prior recall list** but was tied to the same contaminated vitamin premix.

This is the **second expansion stage** of the Hill's vitamin D 2019 lifecycle and the third document in the supersedes chain.

## What was newly recalled

The May 20 expansion added a single can date / lot code within an already recalled case of dog food that had been omitted from the prior list. The exact SKU and lot identifier are listed on the FDA source page; this summary does not reproduce specific lot codes for the same provenance reasons documented below.

## What the FDA and Hill's reported

According to the source notice and corroborating coverage:

- The trigger was the same vitamin premix received from the same U.S. supplier responsible for the January and March recalls.
- The action was conducted in cooperation with the U.S. Food and Drug Administration.
- Hill's framed the additional expansion as a correction to the prior recall list rather than the discovery of a new contamination event — i.e., the same defect, more completely accounted for.
- According to FDA records (as reflected in `sources/nutrition_safety.yaml` source-discovery notes), the recall was subsequently terminated after Hill's required its supplier to add testing of incoming ingredients. The termination is recorded as a status field on each of the three FDA safety-alert pages rather than as its own canonical document.

## Lifecycle position

This note adds the second `supersedes` edge to the chain:

```
pub_hills_vitd_announcement_2019_01  (Jan 31 2019)
              ▲
              │ supersedes
              │
pub_hills_vitd_expansion_2019_03    (Mar 20 2019)
              ▲
              │ supersedes
              │
pub_hills_vitd_expansion_2019_05    (May 20 2019)
```

The fourth note (Nov 20 2019 FDA Warning Letter) closes the chain with a third `supersedes` edge representing the regulatory-followup stage past the immediate recall lifecycle.

## Provenance and limitations

Direct WebFetch against `fda.gov` returned HTTP 404 from this client; claims above are sourced from search-engine summaries of the FDA URL of record and from corroborating veterinary-press coverage that cited the same FDA page. The summary characterization of the May 20 expansion as a correction for an inadvertently-omitted lot is supported by multiple search-engine summaries that cite the FDA page directly, but the maintainer could not verify the exact lot identifier against the live source page.

## Sources

- Hill's Pet Nutrition Additionally Expands Voluntary Recall of Select Canned Dog Food for Elevated Vitamin D (FDA safety alert, May 20 2019, canonical URL of record): https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/hills-pet-nutrition-additionally-expands-voluntary-recall-select-canned-dog-food-elevated-vitamin-d
- iHeartDogs expanded-list summary: https://iheartdogs.com/breaking-fda-announces-expanded-list-of-recalled-hills-prescription-diet-science-diet-dog-food/
- Defense Commissary Agency news release reproducing the FDA expansion: https://corp.commissaries.com/our-agency/newsroom/news-releases/hills-pet-nutrition-expands-recall-select-canned-dog-food-0
