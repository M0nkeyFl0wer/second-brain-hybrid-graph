---
note_id: cj_2020_nbc_grain_free_dcm_continuing
source_url: https://www.nbcnews.com/health/health-news/fda-continues-investigation-dog-heart-damage-linked-diet-n1255196
source_title: "FDA investigation continues into dog heart damage associated with grain-free food"
source_date: "2020"
source_publisher: "NBC News (NBCUniversal News Group)"
license: fair_use_excerpt
license_note: "Copyright held by NBCUniversal News Group. Excerpted for non-commercial research under fair use. NBC News articles are free-to-read."
accessed_on: "2026-04-30"
domain: community_journalism

# Ontology-aligned entity declarations introduced by this note.
# Note: concept_dcm, concept_grain_free_diet, org_us_fda, and
# event_fda_dcm_investigation_open_2018_07 are reused from
# vault/veterinary_research/2018-07-fda-dcm-investigation.md.
# This is the deliberate cross-attribution pairing called out
# in sources/community_journalism.yaml — same investigation,
# different publisher surface (Cat 4 / Cat 2c stress test).
entities:
  - id: pub_nbc_grain_free_dcm_continuing_2020
    type: publication
    canonical: "FDA investigation continues into dog heart damage associated with grain-free food"
  - id: org_nbc_news
    type: organization
    canonical: "NBC News"
    is_regulatory: false
  # person_lisa_freeman, org_tufts_cummings, and concept_beg_diet are reused
  # from the veterinary_research domain (2018-11-tufts-petfoodology-beg-dcm.md
  # and 2022-03-freeman-jvim-prospective-dcm-diet.md). This note only references
  # them via edges; no redeclaration.

# Edges introduced or strengthened by this note.
edges:
  - from: pub_nbc_grain_free_dcm_continuing_2020
    type: authored_by
    to: org_nbc_news
    evidence: "Article published on nbcnews.com under NBC News health-news section"
  - from: pub_nbc_grain_free_dcm_continuing_2020
    type: subject_of
    to: event_fda_dcm_investigation_open_2018_07
    evidence: "Article's primary subject is the FDA's continuing investigation into the diet-DCM link first announced in July 2018"
  - from: pub_nbc_grain_free_dcm_continuing_2020
    type: mentions
    to: concept_dcm
    evidence: "Subject matter throughout — 'dog heart damage' / DCM is the central topic"
  - from: pub_nbc_grain_free_dcm_continuing_2020
    type: mentions
    to: concept_grain_free_diet
    evidence: "Headline names 'grain-free food' as the implicated diet category"
  - from: pub_nbc_grain_free_dcm_continuing_2020
    type: mentions
    to: concept_beg_diet
    evidence: "Article references the BEG (boutique / exotic-ingredient / grain-free) framing used in the veterinary nutrition literature"
    needs_grounding: true
  - from: pub_nbc_grain_free_dcm_continuing_2020
    type: mentions
    to: org_us_fda
    evidence: "Article reports on the FDA's ongoing investigation and the agency's stated position that no recall has been issued"
  - from: pub_nbc_grain_free_dcm_continuing_2020
    type: mentions
    to: person_lisa_freeman
    evidence: "Article quotes Dr. Lisa Freeman as a veterinary nutritionist whose study tracked DCM cases over time"
  - from: person_lisa_freeman
    type: affiliated_with
    to: org_tufts_cummings
    evidence: "Article identifies Lisa Freeman as a professor at the Cummings School of Veterinary Medicine at Tufts University"

tags: [community_journalism, dcm, grain_free, fda, cross_attribution, routing_collapse_test]
contradiction_pair_id: dcm_grain_free_2018
---

# FDA investigation continues into dog heart damage associated with grain-free food (NBC News, 2020)

## Summary

This NBC News health-news article reports on the U.S. Food and Drug Administration's continuing investigation, as of 2020, into a possible link between certain "grain-free" pet diets and non-hereditary canine dilated cardiomyopathy (DCM) in dogs. The investigation was first announced by the FDA in **July 2018** (see `vault/veterinary_research/2018-07-fda-dcm-investigation.md` for the primary regulatory record).

The article frames the investigation as ongoing rather than resolved. It reports that the FDA had not, as of the article's publication, recommended a recall of any grain-free products or declared specific pet food products unsafe.

## Sources cited in the article

- **Dr. Lisa Freeman**, a veterinary nutritionist and professor at the **Cummings School of Veterinary Medicine at Tufts University**, who led a study examining 75 dogs with DCM over a period of just under five years. Per the article, the study found a significant increase over time in the number of dogs with DCM, with the increase beginning even before the first FDA alert. Dogs that were switched from implicated diets to traditional dog food showed improvements in heart function and lived significantly longer than those with no diet change.
- The article also references the FDA's published statements that most of the diets associated with reports of non-hereditary DCM contain legume seeds ("pulses" — peas, lentils, etc.) high in their ingredient lists, and that "pulse" ingredients appear in many "grain-free" diets in greater proportion than in most grain-containing formulas.

## Cross-domain connections

This note exists deliberately as the community-journalism counterpart to the FDA primary-source note in `veterinary_research/`. The pairing exercises:

- **Cat 4 (alias / cross-attribution at the publication layer):** the same underlying investigation appears under two different publisher surfaces — `org_us_fda` as primary regulator, `org_nbc_news` as consumer-facing reporter. A KG that fragments these into unrelated event records silently loses the routing-collapse signal documented in mempalace#101 (the "climate evidence" failure mode retold here in dog-news shape).
- **Cat 2c (multi-hop):** the chain `person_lisa_freeman → org_tufts_cummings` (affiliation) and `pub_nbc_grain_free_dcm_continuing_2020 → event_fda_dcm_investigation_open_2018_07` (subject_of) is precisely the affiliation-plus-subject hop pattern called out in `ontology.yaml#sme_category_coverage.cat_2c_multi_hop`.
- **Cross-domain (`veterinary_research` ↔ `community_journalism` ↔ `nutrition_safety`):** the article touches all three domains in a single source.

## Provenance and limitations

The article was retrieved via WebSearch (top-result match for the source URL with title and snippet metadata returned by the search engine). Direct WebFetch against the canonical URL was not available in this authoring session; this matches the verification limitation already documented in the FDA 2018 note. The summary above quotes only claims that appeared in the WebSearch result snippet or in publicly indexed summaries of the same article. Maintainer should re-fetch the live page before any quoted statement here is treated as load-bearing for evaluation.

## Sources

- NBC News article (canonical URL of record): https://www.nbcnews.com/health/health-news/fda-continues-investigation-dog-heart-damage-linked-diet-n1255196
- Paired primary source: `vault/veterinary_research/2018-07-fda-dcm-investigation.md` (FDA investigation page, July 2018)
- Related FDA Third Status Report (June 2019): https://www.fda.gov/animal-veterinary/cvm-updates/fda-provides-third-status-report-investigation-potential-connection-between-certain-diets-and-cases
