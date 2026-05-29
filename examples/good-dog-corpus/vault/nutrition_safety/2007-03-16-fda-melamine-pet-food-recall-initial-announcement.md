---
note_id: nut_2007_03_melamine_recall_initial
source_url: https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/enforcement-story-archive/introduction-2007
source_title: "Investigation Update: Melamine and Pet Food — 2007 Recall"
source_date: "2007-03-16"
source_publisher: "U.S. Food and Drug Administration"
license: public_domain
license_note: "U.S. federal government work, 17 U.S.C. § 105"
accessed_on: "2026-05-03"
domain: nutrition_safety
lifecycle_id: melamine_2007_pet_food_recall

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: org_menu_foods
    type: organization
    canonical: "Menu Foods Inc."
    is_regulatory: false
  - id: org_us_fda
    type: organization
    canonical: "U.S. Food and Drug Administration"
    is_regulatory: true
  - id: org_chemnutra
    type: organization
    canonical: "ChemNutra LLC"
    is_regulatory: false
  - id: org_wilbur_ellis
    type: organization
    canonical: "Wilbur-Ellis Company"
    is_regulatory: false
  - id: org_hills_pet_nutrition
    type: organization
    canonical: "Hill's Pet Nutrition"
    is_regulatory: false
  - id: org_del_monte
    type: organization
    canonical: "Del Monte Pet Products"
    is_regulatory: false
  - id: org_nestle_purina
    type: organization
    canonical: "Nestlé Purina PetCare Company"
    is_regulatory: false
  - id: concept_melamine_contamination
    type: concept
    canonical: "Melamine contamination of pet food (2007)"
    aliases: ["melamine pet food recall 2007", "2007 pet food contamination", "wheat gluten melamine"]
  - id: concept_cyanuric_acid
    type: concept
    canonical: "Cyanuric acid co-contamination with melamine"
    aliases: ["melamine analogue", "triazine contaminant"]
  - id: event_melamine_2007_recall
    type: event
    canonical: "2007 melamine pet food recall"
    timestamp: "2007-03-16"
    status: resolved
  - id: pub_melamine_2007_initial_recall
    type: publication
    canonical: "FDA 2007 Melamine Pet Food Recall — Initial Announcement and Investigation (2007-03-16)"

# Edges introduced or strengthened by this note.
edges:
  - from: pub_melamine_2007_initial_recall
    type: subject_of
    to: event_melamine_2007_recall
    evidence: "Publication documents the March 16 2007 announcement and FDA investigation launch — the lifecycle's announcement stage"
  - from: pub_melamine_2007_initial_recall
    type: authored_by
    to: org_us_fda
    evidence: "Hosted on fda.gov as FDA's enforcement story archive documenting the 2007 investigation"
  - from: org_us_fda
    type: regulates
    to: org_menu_foods
    evidence: "FDA exercised jurisdiction under FFDCA over Menu Foods as a pet food manufacturer; FDA issued import alert and recall coordination"
    needs_grounding: true
  - from: org_us_fda
    type: regulates
    to: concept_melamine_contamination
    evidence: "FDA asserted regulatory authority over pet food contaminated with melamine under the Federal Food, Drug, and Cosmetic Act — unsafe adulterant"
    needs_grounding: true
  - from: pub_melamine_2007_initial_recall
    type: mentions
    to: org_menu_foods
    evidence: "Menu Foods is the index firm — the manufacturer whose 'cuts and gravy' products first triggered the recall"
  - from: pub_melamine_2007_initial_recall
    type: mentions
    to: org_chemnutra
    evidence: "ChemNutra is identified as the U.S. importer of the Chinese wheat gluten ultimately traced as the primary contamination source"
  - from: pub_melamine_2007_initial_recall
    type: mentions
    to: org_wilbur_ellis
    evidence: "Wilbur-Ellis is identified as the U.S. importer of rice protein concentrate from a second Chinese supplier that was found to contain melamine analogues"
  - from: pub_melamine_2007_initial_recall
    type: mentions
    to: org_hills_pet_nutrition
    evidence: "Hill's Pet Nutrition participated voluntarily in the Menu Foods recall and recalled Prescription Diet m/d Feline dry food on March 30 2007"
  - from: pub_melamine_2007_initial_recall
    type: mentions
    to: org_del_monte
    evidence: "Del Monte issued voluntary recalls of Jerky Treats, Gravy Train Beef Sticks, and Pounce products containing wheat gluten from the identified Chinese supplier"
  - from: pub_melamine_2007_initial_recall
    type: mentions
    to: org_nestle_purina
    evidence: "Nestlé Purina recalled ALPO Prime Cuts in Gravy wet dog food and withdrew Mighty Dog pouch products in response to the same contamination event"
  - from: pub_melamine_2007_initial_recall
    type: mentions
    to: concept_melamine_contamination
    evidence: "Source details melamine as the primary contaminant identified in pet food and wheat gluten imported from China"
  - from: pub_melamine_2007_initial_recall
    type: mentions
    to: concept_cyanuric_acid
    evidence: "Source notes that melamine combined with its analogue cyanuric acid forms crystals in urine and kidney tissue, producing more severe toxicity than melamine alone"

tags: [nutrition_safety, recall, melamine, contamination, fda, lifecycle_announcement, china, ingredient_supplier]
---

# 2007 Melamine Pet Food Recall — Initial Announcement and Investigation

## Summary

On **March 16, 2007**, Menu Foods Inc. announced a nationwide voluntary recall of "cuts and gravy" style wet dog and cat food produced at its facilities in Emporia, Kansas, and Pennsauken, New Jersey, between **December 3, 2006, and March 6, 2007**. The firm's action came after it received consumer complaints of kidney failure in cats and dogs, and after internal taste trials confirmed the illness and death of nine cats and one dog. The FDA launched its investigation within 24 hours of notification. This is the **announcement stage** of the 2007 melamine recall lifecycle.

By April 26, 2007, the recall had expanded to involve **18 firms**, **over 5,300 product lines**, and **more than 17,000 consumer complaints** spanning approximately 1,950 cat deaths and 2,200 dog deaths reported to the FDA.

## The contamination pathway

FDA's Forensic Chemistry Center identified **melamine** and **melamine analogues** — including **cyanuric acid** — in both the finished pet foods and the wheat gluten used as an ingredient. The agency traced the contamination to two Chinese suppliers:

1. **ChemNutra LLC** — imported wheat gluten from Xuzhou Anying Biologic Technology Development Company (China), the primary source. ChemNutra issued its own recall on **April 3, 2007**.
2. **Wilbur-Ellis Company** — imported rice protein concentrate from a second Chinese supplier also found to contain melamine analogues. Wilbur-Ellis issued its recall on **April 18, 2007**, and the ripple recall from this source extended to Chenango Valley Pet Foods, Diamond Pet Foods, and Costco's Kirkland Signature brand.

The mechanism was deliberate adulteration: melamine was added to the vegetable proteins to boost the apparent protein content when measured by standard assays (which detect nitrogen content — melamine is nitrogen-rich but not nutritionally protein).

## Key events and dates

| Date | Action |
|------|--------|
| Nov 2006 | First shipment of melamine-contaminated wheat gluten arrives in U.S. (per FDA) |
| Dec 3, 2006 | Menu Foods begins production window for affected cuts-and-gravy products |
| Mar 15, 2007 | Menu Foods notifies FDA of 14 animal deaths |
| Mar 16, 2007 | Menu Foods announces nationwide recall; FDA launches investigation |
| Mar 30, 2007 | FDA announces melamine as identified contaminant; Hill's, Del Monte, Purina issue recalls |
| Apr 3, 2007 | ChemNutra recalls all suspect wheat gluten |
| Apr 17, 2007 | Melamine found in rice protein (Wilbur-Ellis source); Natural Balance issues recall |
| Apr 19, 2007 | FDA issues Import Alert #99-29 — all vegetable protein products from China detained |
| Apr 27, 2007 | Expanded: all vegetable protein products from China under Import Alert |
| Aug 21, 2007 | Mars Petcare recalls two dry dog food products (dry food, separate Salmonella event) |

## Human health and regulatory context

FDA determined that the combination of **melamine and cyanuric acid** is significantly more toxic than either compound alone — the two substances form crystals in urine and kidney tissue, leading to acute renal failure. Of 750 samples of wheat gluten and products containing wheat gluten that FDA tested, 330 were positive for melamine. Of 85 samples of rice protein concentrate and products made with it, 27 were positive.

Contaminated pet food was also fed to hogs at farms in Utah, Ohio, North Carolina, and California; hogs in at least five states were quarantined as a precaution. No contaminated meat reached the human food supply.

## What this note covers

This note documents the **announcement stage** of the 2007 melamine recall lifecycle. Additional documents in this lifecycle — expanding the recall scope, documenting regulatory followup — are tracked as separate publications with their own `lifecycle_id: melamine_2007_pet_food_recall`. The supersession chain for this lifecycle is seeded via `supersedes` edges in those subsequent publications.

## Provenance and limitations

All factual claims above are sourced from the FDA Enforcement Story Archive page (primary source URL of record), the AVMA comprehensive recall list, and corroborating coverage in Wikipedia's timeline of the 2007 recalls and FDA's Center for Veterinary Medicine FY2007 report. Lot-level product identifiers for each of the 18 firms are not reproduced into this note; downstream consumers should consult the FDA's accessdata database for the complete product list.

## Sources

- FDA Investigation Update: Melamine and Pet Food — 2007 Recall (FDA Enforcement Story Archive, canonical URL of record): https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/enforcement-story-archive/introduction-2007
- AVMA comprehensive recalled products list (April 27, 2007): https://web.archive.org/web/20070429130538/www.avma.org/aa/menufoodsrecall/default.asp
- Wikipedia timeline of the 2007 pet food recalls: https://en.wikipedia.org/wiki/Timeline_of_the_2007_pet_food_recalls
- FDA Center for Veterinary Medicine FY2007 report (PDF): https://fda.gov/media/72971/download