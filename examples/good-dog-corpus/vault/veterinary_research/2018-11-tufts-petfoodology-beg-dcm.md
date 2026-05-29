---
note_id: vet_2018_tufts_petfoodology_beg_dcm
source_url: https://sites.tufts.edu/petfoodology/2018/11/29/dcm-update/
source_title: "It's Not Just Grain-Free: An Update on Diet-Associated Dilated Cardiomyopathy"
source_date: "2018-11-29"
source_publisher: "Tufts Cummings School of Veterinary Medicine — Petfoodology"
license: fair_use_excerpt
license_note: "Tufts blog post; not explicitly CC-licensed. Corpus use is fair-use summary plus attribution; full text not republished."
accessed_on: "2026-04-30"
domain: veterinary_research

# Reuses concept_dcm, concept_grain_free_diet, concept_pulses, person_lisa_freeman,
# org_tufts_cummings, and concept_nontraditional_diet introduced in prior notes.
entities:
  - id: pub_tufts_petfoodology_beg_2018
    type: publication
    canonical: "It's Not Just Grain-Free: An Update on Diet-Associated Dilated Cardiomyopathy"
    aliases: ["Tufts BEG update 2018", "Petfoodology DCM update 2018-11"]
  - id: concept_beg_diet
    type: concept
    canonical: "BEG diet (boutique, exotic-ingredient, or grain-free)"
    aliases: ["BEG", "BEG diets", "boutique exotic-ingredient grain-free diet"]

edges:
  - from: pub_tufts_petfoodology_beg_2018
    type: authored_by
    to: person_lisa_freeman
    evidence: "Post is published on the Tufts Petfoodology blog under Dr. Lisa Freeman's byline; she is the author who coined / disseminated the BEG terminology in this November 2018 update"
  - from: person_lisa_freeman
    type: affiliated_with
    to: org_tufts_cummings
    evidence: "Petfoodology is the public-facing blog of the Clinical Nutrition Service at the Cummings School of Veterinary Medicine at Tufts University; Freeman is a board-certified veterinary nutritionist on faculty there"
  - from: pub_tufts_petfoodology_beg_2018
    type: subject_of
    to: concept_beg_diet
    evidence: "Post introduces and disseminates the BEG (boutique, exotic-ingredient, grain-free) terminology for the suspected diet category"
  - from: pub_tufts_petfoodology_beg_2018
    type: mentions
    to: concept_dcm
    evidence: "DCM is the central condition under discussion in the update"
  - from: pub_tufts_petfoodology_beg_2018
    type: mentions
    to: concept_grain_free_diet
    evidence: "The post's central argument is that the apparent diet-DCM signal is 'not just grain-free' — it implicates ingredients used to replace grains"
  - from: pub_tufts_petfoodology_beg_2018
    type: mentions
    to: concept_pulses
    evidence: "Post discusses lentils and chickpeas (pulses) as ingredients used to replace grains in grain-free diets and as candidate culprits in the diet-DCM signal"
  - from: pub_tufts_petfoodology_beg_2018
    type: mentions
    to: concept_nontraditional_diet
    evidence: "BEG diets are the subset of nontraditional diets the post argues are most associated with reported DCM cases"
  - from: pub_tufts_petfoodology_beg_2018
    type: cites
    to: pub_fda_dcm_investigation_main
    evidence: "Post is explicitly framed as an update on the FDA's diet-DCM investigation, building on the FDA's July 2018 announcement"

tags: [vet_research, dcm, beg, freeman, tufts, terminology, contradiction_pair_supporting]
contradiction_pair_id: dcm_grain_free_2018
---

# It's Not Just Grain-Free: An Update on Diet-Associated Dilated Cardiomyopathy (Tufts Petfoodology, November 2018)

## Summary

A November 29, 2018 post on the Tufts Cummings School of Veterinary Medicine's Petfoodology blog by Dr. Lisa Freeman, a board-certified veterinary nutritionist on the Tufts Clinical Nutrition Service. This post is the canonical surface where the **BEG (boutique, exotic-ingredient, or grain-free)** shorthand entered wide circulation among veterinary cardiologists and pet owners.

The post is included in the corpus for two reasons: it introduces the BEG concept entity that the corpus's diet-DCM thread leans on, and it is the academic-counterpart precursor to the FDA's later multifactorial reframing — written by the same Tufts group whose 2022 JVIM prospective study would later anchor the peer-reviewed side of the seeded Cat 3 contradiction pair.

## What the post argued

Two load-bearing claims:

1. **The apparent diet-DCM signal is "not just grain-free."** Freeman argued that the implicated category is broader than grain-free dog food per se — it includes pet food made by **boutique companies**, food containing **exotic ingredients** (e.g., kangaroo, alligator, bison, lentils, chickpeas), and food labeled grain-free, taken together. The post coined the **BEG** acronym to name this category.
2. **The likely mechanism is ingredient-driven, not grain-absence-driven.** The apparent association may turn on ingredients used to replace grains in grain-free diets (lentils, chickpeas, peas) and on other ingredients commonly found in BEG diets (exotic meats, vegetables, fruits) — rather than on the grain-free label itself.

A search-engine summary of the post characterized the argument this way:

> "The apparent link between BEG diets and DCM may be due to ingredients used to replace grains in grain-free diets, such as lentils or chickpeas, but also may be due to other common ingredients commonly found in BEG diets, such as exotic meats, vegetables, and fruits."

The November 2018 post followed an earlier (June 4, 2018) Petfoodology post by Freeman titled "A broken heart: Risk of heart disease in boutique or grain-free diets and exotic ingredients," which had received over 180,000 page views in its first week according to coverage of the BEG-terminology arc. The November update was framed explicitly as a follow-up to both that June post and the FDA's July 2018 announcement.

## Why this note is in the corpus

The BEG concept entity (`concept_beg_diet`) is referenced obliquely by other notes in the dietary thread but had no sourced surface introducing it until this note. Cat 8 (ontology coherence) requires that any concept the graph traverses has a sourced surface where the concept is defined; this note provides that surface from a publicly retrievable, attributable origin.

This note is also a Cat 2c hop bridge: `pub_tufts_petfoodology_beg_2018 -authored_by-> person_lisa_freeman -affiliated_with-> org_tufts_cummings`, with the same Freeman / Tufts pair recurring in the 2022 JVIM prospective study note. Multi-hop traversals from the FDA investigation through the academic literature into the BEG terminology should land on this note.

## Provenance and limitations

The summary author attempted to retrieve the source URL directly via WebFetch at the time of writing; permission to fetch the Tufts URL from this client was not granted in this session. The content above was retrieved via search-engine summary of the same URL set (a WebSearch query against the post title and the BEG terminology returned the canonical Tufts URL and a vetnutrition.tufts.edu mirror as live results, with snippet text matching every quoted statement above, as reported via search-engine summary; full text not directly verified by author at write time).

Specific items that should be re-verified against the live Tufts post before any downstream consumer relies on exact wording:

- The exact phrasing of the BEG acronym expansion (this note follows the manifest's "boutique, exotic-ingredient, or grain-free" canonicalization; some downstream sources render it as "boutique companies, exotic ingredients, or grain-free").
- The exact taurine discussion in the post body (taurine deficiency was a candidate mechanistic explanation in the 2018 cardiology literature; this note does not declare specific taurine claims because the search-summary excerpt did not surface direct quotes).

## Sources

- "It's Not Just Grain-Free: An Update on Diet-Associated Dilated Cardiomyopathy" (canonical URL of record): https://sites.tufts.edu/petfoodology/2018/11/29/dcm-update/
- Tufts vetnutrition mirror of the same post: https://vetnutrition.tufts.edu/2018/11/dcm-update/
- Earlier Petfoodology post that primed the BEG framing (June 4, 2018): https://sites.tufts.edu/petfoodology/2018/06/04/a-broken-heart-risk-of-heart-disease-in-boutique-or-grain-free-diets-and-exotic-ingredients/
