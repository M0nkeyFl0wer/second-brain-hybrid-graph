---
note_id: nut_2019_01_hills_vitd_announcement
source_url: https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/hills-pet-nutrition-voluntarily-recalls-select-canned-dog-food-excessive-vitamin-d
source_title: "Hill's Pet Nutrition Voluntarily Recalls Select Canned Dog Food for Excessive Vitamin D"
source_date: "2019-01-31"
source_publisher: "U.S. Food and Drug Administration"
license: public_domain
license_note: "U.S. federal government work, 17 U.S.C. § 105"
accessed_on: "2026-04-30"
domain: nutrition_safety
lifecycle_id: hills_vitamin_d_2019_recall

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: org_hills_pet_nutrition
    type: organization
    canonical: "Hill's Pet Nutrition"
    is_regulatory: false
  - id: brand_hills_science_diet
    type: product
    canonical: "Hill's Science Diet"
    brand: "Hill's Pet Nutrition"
  - id: brand_hills_prescription_diet
    type: product
    canonical: "Hill's Prescription Diet"
    brand: "Hill's Pet Nutrition"
  - id: concept_vitamin_d_toxicity
    type: concept
    canonical: "Vitamin D toxicity in dogs"
    aliases: ["excessive vitamin D", "elevated vitamin D", "vitamin D toxicosis"]
  - id: event_hills_vitd_recall_2019
    type: event
    canonical: "Hill's Pet Nutrition vitamin D recall (2019)"
    timestamp: "2019-01-31"
    status: ongoing
  - id: pub_hills_vitd_announcement_2019_01
    type: publication
    canonical: "Hill's Pet Nutrition Voluntarily Recalls Select Canned Dog Food for Excessive Vitamin D (2019-01-31)"

# Edges introduced or strengthened by this note.
edges:
  - from: pub_hills_vitd_announcement_2019_01
    type: subject_of
    to: event_hills_vitd_recall_2019
    evidence: "Publication is the canonical FDA safety alert announcing the Jan 31 2019 recall — the lifecycle's announcement stage"
  - from: pub_hills_vitd_announcement_2019_01
    type: authored_by
    to: org_us_fda
    evidence: "Hosted on fda.gov as an FDA-published safety alert reproducing the firm's recall notice"
  - from: pub_hills_vitd_announcement_2019_01
    type: mentions
    to: org_hills_pet_nutrition
    evidence: "Recall notice issued by Hill's Pet Nutrition; firm named throughout"
  - from: pub_hills_vitd_announcement_2019_01
    type: mentions
    to: brand_hills_science_diet
    evidence: "Affected canned dog food includes Hill's Science Diet varieties (per FDA listing of recalled SKUs)"
  - from: pub_hills_vitd_announcement_2019_01
    type: mentions
    to: brand_hills_prescription_diet
    evidence: "Affected canned dog food includes Hill's Prescription Diet varieties (per FDA listing of recalled SKUs)"
  - from: pub_hills_vitd_announcement_2019_01
    type: mentions
    to: concept_vitamin_d_toxicity
    evidence: "Source describes excessive vitamin D as the basis for the recall"
  - from: org_us_fda
    type: regulates
    to: brand_hills_science_diet
    evidence: "FDA regulates pet food under FFDCA / FSMA; Hill's products are subject to FDA recall coordination"
    needs_grounding: true
  - from: org_us_fda
    type: regulates
    to: brand_hills_prescription_diet
    evidence: "FDA regulates pet food under FFDCA / FSMA; Hill's products are subject to FDA recall coordination"
    needs_grounding: true

# Note: org_us_fda is reused from vault/veterinary_research/2018-07-fda-dcm-investigation.md
# and is not redeclared here per corpus guidance.

tags: [nutrition_safety, recall, hills, vitamin_d, lifecycle_announcement, fda]
---

# Hill's Pet Nutrition Voluntarily Recalls Select Canned Dog Food for Excessive Vitamin D (Jan 31 2019)

## Summary

On **January 31, 2019**, Hill's Pet Nutrition announced a voluntary recall of select canned dog food products marketed under the **Hill's Science Diet** and **Hill's Prescription Diet** brands due to potentially elevated levels of vitamin D. The recall was published as an FDA safety alert on the same date. According to the FDA notice, the initial recall covered **twenty-five (25) different canned dog food products**.

This is the **announcement stage** of the Hill's vitamin D 2019 lifecycle — the first of four FDA-published documents that together form the Cat 6 supersession chain documented in `sources/nutrition_safety.yaml`.

## What was recalled

The notice covered selected canned dog foods from Hill's Science Diet and Hill's Prescription Diet lines distributed through retail pet stores and veterinary clinics nationwide. The FDA notice listed specific product names and lot codes; this summary does not reproduce individual lot codes because the maintainer was unable to reach the source page directly (see "Provenance and limitations" below) and will not invent SKU-level identifiers.

## What the FDA and Hill's reported

According to the FDA notice and Hill's accompanying statement (as reflected in search-engine summaries of the source page):

- Hill's learned of the issue after receiving a complaint about a dog showing signs of elevated vitamin D levels; an internal investigation traced the cause to a supplier error in a vitamin premix.
- Symptoms of vitamin D toxicity in dogs include vomiting, loss of appetite, increased thirst, increased urination, excessive drooling, and weight loss. At very high levels, vitamin D consumption can cause serious health issues including renal dysfunction.
- Hill's stated it had identified and isolated the error and required its supplier to implement additional quality testing prior to release of ingredients, and added its own further testing of incoming ingredients.

## Provenance and limitations

Direct WebFetch against `fda.gov` returned HTTP 404 from this client at the time of authoring (the same condition documented in `vault/veterinary_research/2018-07-fda-dcm-investigation.md`). All factual claims above are sourced from search-engine summaries of the FDA URL of record and corroborating coverage that cited the same FDA page (AVMA JAVMA News, dvm360, NBC News). No SKU-level lot codes are quoted because the maintainer could not verify the exact lot list against the live source page.

The frontmatter `source_url` is the canonical URL of record. Verification against that URL is the responsibility of any downstream consumer who relies on the exact product list or quoted wording.

## Sources

- Hill's Pet Nutrition Voluntarily Recalls Select Canned Dog Food for Excessive Vitamin D (FDA safety alert, Jan 31 2019, canonical URL of record): https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/hills-pet-nutrition-voluntarily-recalls-select-canned-dog-food-excessive-vitamin-d
- AVMA JAVMA News coverage: https://www.avma.org/javma-news/2019-03-15/hills-products-recalled-excess-vitamin-d
- dvm360 coverage: https://www.dvm360.com/view/hill-s-pet-nutrition-voluntarily-recalls-select-canned-dog-food-excessive-vitamin-d
