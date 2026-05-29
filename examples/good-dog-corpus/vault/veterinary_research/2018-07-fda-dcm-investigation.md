---
note_id: vet_2018_fda_dcm_investigation
source_url: https://www.fda.gov/animal-veterinary/outbreaks-and-advisories/fda-investigation-potential-link-between-certain-diets-and-canine-dilated-cardiomyopathy
source_title: "FDA Investigation into Potential Link between Certain Diets and Canine Dilated Cardiomyopathy"
source_date: "2018-07"
source_publisher: "U.S. Food and Drug Administration"
license: public_domain
license_note: "U.S. federal government work, 17 U.S.C. § 105"
accessed_on: "2026-04-30"
domain: veterinary_research

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: org_us_fda
    type: organization
    canonical: "U.S. Food and Drug Administration"
    is_regulatory: true
  - id: concept_dcm
    type: concept
    canonical: "Canine Dilated Cardiomyopathy"
    aliases: ["DCM", "canine DCM", "dilated cardiomyopathy"]
  - id: concept_grain_free_diet
    type: concept
    canonical: "Grain-free pet diet"
    aliases: ["grain-free diet", "grain-free dog food"]
  - id: event_fda_dcm_investigation_open_2018_07
    type: event
    canonical: "FDA opens investigation into diet-DCM link"
    timestamp: "2018-07"
    status: ongoing
  - id: pub_fda_dcm_investigation_main
    type: publication
    canonical: "FDA Investigation into Potential Link between Certain Diets and Canine Dilated Cardiomyopathy"

# Edges introduced or strengthened by this note.
edges:
  - from: pub_fda_dcm_investigation_main
    type: authored_by
    to: org_us_fda
    evidence: "Source page is published by FDA Center for Veterinary Medicine; byline FDA"
  - from: pub_fda_dcm_investigation_main
    type: subject_of
    to: event_fda_dcm_investigation_open_2018_07
    evidence: "Publication is the canonical record of the July 2018 announcement"
  - from: pub_fda_dcm_investigation_main
    type: mentions
    to: concept_dcm
    evidence: "Subject matter throughout"
  - from: pub_fda_dcm_investigation_main
    type: mentions
    to: concept_grain_free_diet
    evidence: "Identifies grain-free as common feature in 90% of single-diet cases (2018 update)"
  - from: org_us_fda
    type: regulates
    to: concept_grain_free_diet
    evidence: "FDA regulates pet food generally; the specific statutory citation is not verified in this note's source"
    needs_grounding: true

tags: [vet_research, dcm, grain_free, fda, contradiction_pair_candidate]
contradiction_pair_id: dcm_grain_free_2018
---

# FDA Investigation into Potential Link between Certain Diets and Canine Dilated Cardiomyopathy

## Summary

In **July 2018**, the U.S. Food and Drug Administration (FDA) announced that it had begun investigating reports of canine dilated cardiomyopathy (DCM) in dogs eating certain pet foods, many labeled as "grain-free," which contained a high proportion of peas, lentils, other legume seeds (pulses), and/or potatoes in various forms (whole, flour, protein) as main ingredients.

The agency framed the work as a possible diet-DCM connection rather than a confirmed causal finding from the start.

## What the FDA reported in successive updates

In the **2018 status update** (covering reports received through November 30, 2018), the FDA stated that between January 1, 2014 and November 30, 2018 it had received **300 reports of DCM** (294 canine reports, 6 feline reports). Approximately 276 of these were reported after the July 2018 public notification (273 canine, 3 feline).

> "In cases in which dogs ate a single primary diet, 90 percent reported feeding a grain-free food. Many of these case reports included breeds of dogs not previously known to have a genetic predisposition to the disease."

The **June 2019 status update** (the agency's "Third Status Report") raised the cumulative count to **524 reports** (515 canine, 9 feline) through April 30, 2019, and also clarified that the agency had received reports of non-hereditary DCM associated with both grain-free *and* grain-containing diets, with most diets in reports sharing non-soy legumes and pulses (e.g., peas, lentils) high in their ingredient lists.

A count of reports submitted to the FDA was added to the agency's Questions & Answers documentation as of **November 1, 2022**.

## The FDA's stated position

The FDA has consistently characterized the diet-DCM relationship as unresolved rather than established:

> "Based on the data collected and analyzed thus far, the agency believes that the potential association between diet and DCM in dogs is a complex scientific issue that may involve multiple factors."

> "To date, the FDA has not established why certain diets may be associated with the development of DCM in some dogs."

This position is the source of the canonical Cat 3 contradiction pair seeded by this corpus: the **2018 announcement framed an apparent grain-free / DCM association strong enough to publicize**, while **subsequent FDA statements and follow-up veterinary literature described the relationship as multifactorial and not causally established**. A second note (forthcoming in `vault/veterinary_research/`) will document the follow-up framing and bind the contradiction pair.

## Provenance and limitations

All claims in this summary are sourced from the FDA's own published statements about its investigation. The summary author did not directly access the source pages at the time of writing (a fetch attempt against the FDA URL returned HTTP 404 from this client; the content was retrieved via search-engine summary of the same URL set). A future revision of this note should re-fetch the source page directly and verify each quoted statement against the live page text.

This is a known limitation for v0.1 of the corpus: source-fetch resilience is not yet built into the ingestion pipeline. The frontmatter's `source_url` is the canonical URL of record; verification against that URL is the responsibility of any downstream consumer who relies on the exact quoted wording.

## Sources

- FDA Investigation into Potential Link between Certain Diets and Canine Dilated Cardiomyopathy — main investigation page (canonical URL of record): https://www.fda.gov/animal-veterinary/outbreaks-and-advisories/fda-investigation-potential-link-between-certain-diets-and-canine-dilated-cardiomyopathy
- FDA Provides Third Status Report (June 2019): https://www.fda.gov/animal-veterinary/cvm-updates/fda-provides-third-status-report-investigation-potential-connection-between-certain-diets-and-cases
- Questions & Answers: FDA's Work on Potential Causes of Non-Hereditary DCM in Dogs (count updated 2022-11-01): https://www.fda.gov/animal-veterinary/animal-health-literacy/questions-answers-fdas-work-potential-causes-non-hereditary-dcm-dogs
