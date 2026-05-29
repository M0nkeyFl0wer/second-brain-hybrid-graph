---
note_id: nut_2018_02_fda_raw_pet_food_safety_study
source_url: https://www.fda.gov/animal-veterinary/animal-health-literacy/get-facts-raw-pet-food-diets-can-be-dangerous-you-and-your-pet
source_title: "Get the Facts! Raw Pet Food Diets can be Dangerous to You and Your Pet"
source_date: "2018-02-22"
source_publisher: "U.S. Food and Drug Administration"
license: public_domain
license_note: "U.S. federal government work, 17 U.S.C. § 105"
accessed_on: "2026-05-03"
domain: nutrition_safety

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: org_us_fda
    type: organization
    canonical: "U.S. Food and Drug Administration"
    is_regulatory: true
  - id: concept_raw_pet_food_safety
    type: concept
    canonical: "Raw pet food safety risk"
    aliases: ["raw pet food hazards", "raw diet safety", "raw pet food pathogen risk"]
  - id: concept_salmonella_petfood
    type: concept
    canonical: "Salmonella contamination in pet food"
    aliases: ["salmonella in pet food", "Salmonella spp. pet food"]
  - id: concept_listeria_petfood
    type: concept
    canonical: "Listeria monocytogenes contamination in pet food"
    aliases: ["Listeria monocytogenes in pet food", "L. mono pet food"]
  - id: event_fda_raw_food_study_2010_2012
    type: event
    canonical: "FDA CVM raw pet food pathogen study (2010-2012)"
    timestamp: "2010-10-01"
    status: resolved
  - id: event_performance_dog_recall_2019
    type: event
    canonical: "Bravo Packing Performance Dog raw pet food recall (2019)"
    timestamp: "2019-09-27"
    status: resolved
  - id: pub_fda_raw_pet_food_factsheet_2018
    type: publication
    canonical: "FDA Raw Pet Food Diets can be Dangerous to You and Your Pet (2018-02-22)"
  - id: org_bravo_packing
    type: organization
    canonical: "Bravo Packing Inc."
    is_regulatory: false
  - id: product_performance_dog_raw
    type: product
    canonical: "Performance Dog frozen raw pet food"
    brand: "Bravo Packing Inc."
  - id: pub_fda_raw_meat_guidance_2004
    type: publication
    canonical: "FDA Guidance for Industry #122 — Manufacture and Labeling of Raw Meat Foods for Companion Animals (2004)"

# Edges introduced or strengthened by this note.
edges:
  - from: pub_fda_raw_pet_food_factsheet_2018
    type: subject_of
    to: event_fda_raw_food_study_2010_2012
    evidence: "Publication summarizes the two-year FDA CVM study (Oct 2010–Jul 2012) screening over 1,000 pet food samples for foodborne pathogens — the study is the primary data source the factsheet cites"
  - from: pub_fda_raw_pet_food_factsheet_2018
    type: authored_by
    to: org_us_fda
    evidence: "Published on FDA.gov animal health literacy section as an FDA-authored public guidance document"
  - from: pub_fda_raw_pet_food_factsheet_2018
    type: supersedes
    to: pub_fda_raw_meat_guidance_2004
    evidence: "The 2018 factsheet updates the FDA's position on raw pet food risk; the 2004 guidance was the prior authoritative statement but the 2018 factsheet represents the agency's current position and recommendation against raw feeding, incorporating new study data not available in 2004"
  - from: pub_fda_raw_pet_food_factsheet_2018
    type: mentions
    to: concept_raw_pet_food_safety
    evidence: "Factsheet is explicitly about the dangers of raw pet food diets to pets and owners"
  - from: pub_fda_raw_pet_food_factsheet_2018
    type: mentions
    to: concept_salmonella_petfood
    evidence: "Salmonella is one of the two primary pathogens studied; factsheet reports 15 of 196 raw samples positive"
  - from: pub_fda_raw_pet_food_factsheet_2018
    type: mentions
    to: concept_listeria_petfood
    evidence: "Listeria monocytogenes is one of the two primary pathogens studied; factsheet reports 32 of 196 raw samples positive and notes L. mono as a first-ever finding in commercial pet food"
  - from: org_us_fda
    type: regulates
    to: concept_raw_pet_food_safety
    evidence: "FDA asserts regulatory authority over raw pet food under the Federal Food, Drug, and Cosmetic Act; considers raw pet food adulterated when contaminated with Salmonella or Listeria and not subject to subsequent heat treatment"
    needs_grounding: true
  - from: org_us_fda
    type: regulates
    to: product_performance_dog_raw
    evidence: "FDA issued a public health alert against Performance Dog frozen raw pet food after sampletesting confirmed Salmonella and L. mono contamination — exercising regulatory authority over the specific product"
    needs_grounding: true
  - from: pub_fda_raw_pet_food_factsheet_2018
    type: mentions
    to: org_bravo_packing
    evidence: "Performance Dog is a product of Bravo Packing Inc.; the 2019 recall of this product is cited in the factsheet as a concrete example of the risk the FDA warns against"
  - from: pub_fda_raw_pet_food_factsheet_2018
    type: mentions
    to: product_performance_dog_raw
    evidence: "Performance Dog frozen raw pet food is explicitly named as the product associated with the 2019 Bravo Packing recall and the FDA's advisory against raw pet food"

tags: [nutrition_safety, raw_food, salmonella, listeria, fda, pathogen_study, guidance, supersedes_chain]
---

# FDA Raw Pet Food Diets Can Be Dangerous to You and Your Pet (Feb 22 2018)

## Summary

On **February 22, 2018**, the FDA published a public health factsheet titled "Get the Facts! Raw Pet Food Diets can be Dangerous to You and Your Pet" on its animal health literacy website. The publication synthesizes findings from a **two-year FDA Center for Veterinary Medicine (CVM) study** conducted between **October 2010 and July 2012** that screened over 1,000 pet food samples for disease-causing bacteria. The study found that raw pet food was significantly more likely to be contaminated with **Salmonella** and **Listeria monocytogenes** than any other category of pet food tested. The factsheet explicitly recommends against feeding raw diets to pets and advises strict handling precautions for owners who choose to do so.

This publication's `subject_of` event is the 2010–2012 study itself (`event_fda_raw_food_study_2010_2012`), not the 2019 Bravo Packing recall — though the recall is mentioned as a concrete illustration.

## The FDA CVM two-year study (Oct 2010 – Jul 2012)

The study was conducted in two phases:

**Phase 1:** Approximately 1,000 samples of various pet food types were purchased from retail outlets and online and screened for Salmonella.

**Phase 2:** Expanded to 196 raw pet food samples (dog and cat food, primarily frozen and freeze-dried in tube-like packages), analyzed at six participating laboratories for both **Salmonella** and **Listeria monocytogenes**.

Key quantitative findings:

| Pet Food Type | Samples Tested | Salmonella+ | L. monocytogenes+ |
|---|---|---|---|
| Raw pet food | 196 | 15 | 32 |
| Dry exotic pet food | 190 | 0 | 0 |
| Jerky-type treats | 190 | 0 | 0 |
| Semi-moist dog food | 120 | 0 | 0 |
| Semi-moist cat food | 120 | 0 | 0 |
| Dry dog food | 120 | 0 | 0 |
| Dry cat food | 120 | 1 | 0 |

The study was the first to document **Listeria monocytogenes contamination of commercial pet food** in the United States. Dr. Renate Reimschuessel, CVM veterinarian and one of the study's principal investigators, stated that "quite a large percentage of the raw foods for pets we tested were positive for the pathogen Listeria monocytogenes."

Raw pet food contamination rates: **7.7% for Salmonella, 16.3% for L. monocytogenes** in the Phase 2 sample set.

## FDA's regulatory position on raw pet food

The factsheet articulates the FDA's position:

- **Raw pet food poses significant health risks to both pets and pet owners.** The single best thing an owner can do to prevent infection is not to feed a raw diet.
- Pet food is considered **adulterated** under the Federal Food, Drug, and Cosmetic Act when contaminated with Salmonella and not subject to a subsequent commercial heat step or other process that will kill the Salmonella (21 CFR 500.35).
- The agency does not currently have a formal definition of "raw pet food" but considers products where the primary protein source is uncooked animal tissue to fall within the scope of its concern.
- Contaminated pet food can serve as a **zoonotic reservoir** — infected animals can shed Salmonella and L. mono in feces, contaminating the home environment and exposing human household members without appearing ill themselves.

## The supersession chain

This note seeds a `supersedes` edge from the 2018 factsheet to `pub_fda_raw_meat_guidance_2004` (FDA Guidance for Industry #122, "Manufacture and Labeling of Raw Meat Foods for Companion and Captive Noncompanion Carnivores and Omnivores," May 2004 / revised November 2004). The 2004 guidance documented the FDA's concern about health risks from raw meat products for animals and recommended against feeding raw meat to domestic pets, but it preceded the CVM's systematic two-year dataset. The 2018 factsheet represents the FDA's updated position incorporating new quantitative evidence from the study, explicitly stating "FDA thinks that raw pet food poses significant health risks."

```
pub_fda_raw_meat_guidance_2004      (Guidance #122, 2004)
               ▲
               │ supersedes
               │
pub_fda_raw_pet_food_factsheet_2018  (factsheet, Feb 22 2018)
```

## The 2019 Bravo Packing / Performance Dog recall

The factsheet references — as a concrete example of ongoing risk — the 2019 recall of **Performance Dog frozen raw pet food** manufactured by **Bravo Packing Inc.** of Carneys Point, New Jersey. During a routine inspection, FDA collected two product samples:

- **Performance Dog raw pet food, lot code 072219** — positive for both **Salmonella** and **Listeria monocytogenes**
- **Bravo Packing beef raw pet food** — positive for Salmonella (not yet distributed)

The FDA issued a public health alert in **September 2019** cautioning pet owners against all Performance Dog frozen raw pet food produced on or after July 22, 2019, because the products lack lot codes on retail packaging, making complete recall impossible.

## Provenance and limitations

All quantitative claims above are sourced from the FDA factsheet (primary source URL of record), the published study (Nemser et al., *Foodborne Pathogens and Disease*, 2014; 11(5): 388–396), and the FDA Compliance Policy Guide Sec. 690.800. The factsheet's primary data source is the CVM study; the study results were first published in the peer-reviewed literature before being summarized in the factsheet.

## Sources

- FDA factsheet — "Get the Facts! Raw Pet Food Diets can be Dangerous to You and Your Pet" (Feb 22 2018, canonical URL of record): https://www.fda.gov/animal-veteretary/animal-health-literacy/get-facts-raw-pet-food-diets-can-be-dangerous-you-and-your-pet
- FDA Guidance for Industry #122 — "Manufacture and Labeling of Raw Meat Foods for Companion and Captive Noncompanion Carnivores and Omnivores" (May 2004, revised Nov 2004): https://fda.gov/media/70183/download
- FDA Compliance Policy Guide Sec. 690.800 — "Salmonella in Food for Animals" (final, Jul 2013): https://fda.gov/media/86240/download
- Nemser et al. (2014), "Investigation of Listeria, Salmonella, and Toxigenic Escherichia coli in Various Pet Foods," *Foodborne Pathogens and Disease* 11(5): 388–396
- FDA public health alert — Performance Dog raw pet food (Sep 2019): https://www.fda.gov/animal-veterinary/news-events/fda-cautions-pet-owners-not-feed-performance-dog-raw-pet-food-due-salmonella-listeria-monocytogenes