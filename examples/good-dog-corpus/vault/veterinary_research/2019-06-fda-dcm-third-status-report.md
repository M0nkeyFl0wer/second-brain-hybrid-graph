---
note_id: vet_2019_fda_dcm_third_status_report
source_url: https://www.fda.gov/animal-veterinary/cvm-updates/fda-provides-third-status-report-investigation-potential-connection-between-certain-diets-and-cases
source_title: "FDA Provides Third Status Report on Investigation into Potential Connection Between Certain Diets and Cases of Canine Heart Disease"
source_date: "2019-06-27"
source_publisher: "U.S. Food and Drug Administration, Center for Veterinary Medicine"
license: public_domain
license_note: "U.S. federal government work, 17 U.S.C. § 105"
accessed_on: "2026-04-30"
domain: veterinary_research

# Ontology-aligned entity declarations.
# Reuses org_us_fda, concept_dcm, concept_grain_free_diet, and
# pub_fda_dcm_investigation_main from the existing 2018-07 FDA note.
entities:
  - id: pub_fda_dcm_third_status_report_2019
    type: publication
    canonical: "FDA Third Status Report on Investigation into Potential Connection Between Certain Diets and Cases of Canine Heart Disease"
    aliases: ["FDA Third Status Report", "June 2019 FDA DCM update"]
  - id: event_fda_dcm_third_status_report_2019_06
    type: event
    canonical: "FDA issues Third Status Report on diet-DCM investigation"
    timestamp: "2019-06-27"
    status: resolved
  - id: concept_pulses
    type: concept
    canonical: "Pulses (peas, lentils, and other legume seeds)"
    aliases: ["peas and lentils", "legume seeds", "pulse ingredients"]

edges:
  - from: pub_fda_dcm_third_status_report_2019
    type: authored_by
    to: org_us_fda
    evidence: "Page is published by FDA / Center for Veterinary Medicine as a CVM Update; byline FDA"
  - from: pub_fda_dcm_third_status_report_2019
    type: subject_of
    to: event_fda_dcm_third_status_report_2019_06
    evidence: "Publication is the canonical record of the June 27, 2019 status report"
  - from: pub_fda_dcm_third_status_report_2019
    type: mentions
    to: concept_dcm
    evidence: "Subject matter throughout: 524 cumulative DCM reports through April 30, 2019"
  - from: pub_fda_dcm_third_status_report_2019
    type: mentions
    to: concept_grain_free_diet
    evidence: "More than 90 percent of products named in DCM reports were labeled grain-free"
  - from: pub_fda_dcm_third_status_report_2019
    type: mentions
    to: concept_pulses
    evidence: "93 percent of reported products contained peas and/or lentils; smaller proportion contained potatoes"
  - from: pub_fda_dcm_third_status_report_2019
    type: contradicts
    to: pub_fda_dcm_investigation_main
    evidence: "The Third Status Report reframes the diet-DCM connection from a grain-free-centered association (2018 framing, 90% of single-diet cases were grain-free) to a multifactorial picture in which non-hereditary DCM has been reported in dogs eating both grain-free and grain-containing diets, with pulses (peas/lentils) as the more salient shared ingredient feature; this framing shift is the seeded Cat 3 contradiction pair for the corpus"

tags: [vet_research, dcm, grain_free, fda, contradiction_pair, pulses, multifactorial]
contradiction_pair_id: dcm_grain_free_2018
---

# FDA Third Status Report on Investigation into Potential Connection Between Certain Diets and Cases of Canine Heart Disease

## Summary

On **June 27, 2019**, the U.S. Food and Drug Administration's Center for Veterinary Medicine (CVM) issued its Third Status Report on the diet-DCM investigation. The report did three things at once: it raised the cumulative case count, it named the pet-food brands most frequently cited in reports for the first time, and it shifted the agency's framing of the diet-DCM relationship away from "grain-free" as the primary signal and toward a multifactorial picture in which **pulses** (peas and lentils) were the more striking shared ingredient feature.

This note documents the seeded Cat 3 contradiction-pair partner to the existing 2018 FDA note in this corpus.

## What the Third Status Report stated

Cumulative report count and date range:

> "Between January 1, 2014, when FDA first received a few sporadic reports, and April 30, 2019, the FDA received 524 reports of DCM (515 canine reports, 9 feline reports)."

Note that this 524-report figure is **cumulative since January 2014**, not "since the prior status report." Some of these reports involved more than one affected animal from the same household, so the total number of affected animals exceeds 524.

Ingredient analysis on the named products:

- **More than 90 percent** of products named in DCM reports were labeled "grain-free."
- **93 percent** of reported products contained **peas and/or lentils**.
- A far smaller proportion contained potatoes.

Brand analysis:

- The FDA identified **16 dog food companies** that had ten or more cases of DCM associated with their food, and named those companies publicly for the first time in this status report.

## The framing shift (why this is a Cat 3 contradiction-pair partner)

The 2018 announcement and 2018 status update framed the issue as one centered on grain-free diets. The Third Status Report does not retract that framing — the >90% grain-free figure is still in the new ingredient summary — but it adds two pieces of analysis that change the load-bearing inference downstream:

1. **Pulses (peas and/or lentils) appeared in 93% of reported products**, an even higher rate than "grain-free" labeling. This shifts attention from "grain-free" as a category to specific ingredients used to replace grains.
2. The agency began to frame the underlying mechanism as multifactorial rather than as a clean diet-causes-DCM association.

The corpus treats the 2018 → 2019 framing change as the canonical Cat 3 contradiction pair under id `dcm_grain_free_2018`. The contradiction is normative (what the agency emphasizes as the load-bearing variable) rather than factual (no specific 2018 fact is stated to be wrong by the 2019 report).

## Provenance and limitations

The summary author attempted to retrieve the source URL directly via WebFetch at the time of writing; the fetch returned HTTP 404 from this client. The content above was retrieved via search-engine summary of the same URL set (a WebSearch query against the exact URL and the distinctive figures "524 reports" / "peas and/or lentils" returned the FDA page as the top result with snippet text matching the figures quoted above, as reported via search-engine summary; full text not directly verified by author at write time).

Pattern follows the existing 2018-07 FDA note in this domain. The frontmatter `source_url` is the canonical URL of record; verification against that URL is the responsibility of any downstream consumer who relies on the exact quoted wording.

## Sources

- FDA Provides Third Status Report on Investigation into Potential Connection Between Certain Diets and Cases of Canine Heart Disease (June 27, 2019; canonical URL of record): https://www.fda.gov/animal-veterinary/cvm-updates/fda-provides-third-status-report-investigation-potential-connection-between-certain-diets-and-cases
- FDA Investigation into Potential Link between Certain Diets and Canine Dilated Cardiomyopathy (main investigation page; the 2018 framing this report partly walks back): https://www.fda.gov/animal-veterinary/outbreaks-and-advisories/fda-investigation-potential-link-between-certain-diets-and-canine-dilated-cardiomyopathy
