---
note_id: vet_2018_cdc_brucellosis_canis_endemic
source_url: https://wwwnc.cdc.gov/eid/article/24/8/17-1171_article
source_title: "Brucellosis in Dogs and Public Health Risk"
source_date: "2018-08"
source_publisher: "Centers for Disease Control and Prevention — Emerging Infectious Diseases journal"
license: public_domain
license_note: "CDC Emerging Infectious Diseases article; U.S. government work in public domain. Available at https://wwwnc.cdc.gov/eid/"
accessed_on: "2026-05-03"
domain: veterinary_research

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: pub_cdc_brucellosis_canis_2018
    type: publication
    canonical: "Brucellosis in Dogs and Public Health Risk"
    aliases: ["CDC 2018 brucellosis in dogs EID article", "B. canis public health 2018"]
  - id: org_cdc
    type: organization
    canonical: "Centers for Disease Control and Prevention"
    is_regulatory: false
    notes: "CDC is a public health authority, not a veterinary regulatory body; however it issues guidance that intersects with USDA/state animal health regulations"
  - id: org_usda_aphis
    type: organization
    canonical: "U.S. Department of Agriculture Animal and Plant Health Inspection Service"
    is_regulatory: true
    aliases: ["USDA-APHIS", "APHIS"]
  - id: concept_brucellosis_canis
    type: concept
    canonical: "Canine brucellosis (Brucella canis)"
    aliases: ["B. canis", "brucellosis in dogs", "canine brucellosis"]
  - id: concept_brucellosis_treatment
    type: concept
    canonical: "Antimicrobial treatment of canine brucellosis"
    aliases: ["brucellosis treatment protocol", "B. canis treatment"]
  - id: concept_brucellosis_testing
    type: concept
    canonical: "Diagnostic testing for canine brucellosis"
    aliases: ["B. canis testing", "serological screening", "RSAT", "AGID"]

edges:
  - from: pub_cdc_brucellosis_canis_2018
    type: authored_by
    to: org_cdc
    evidence: "Published in CDC Emerging Infectious Diseases journal; byline CDC"
  - from: pub_cdc_brucellosis_canis_2018
    type: subject_of
    to: concept_brucellosis_canis
    evidence: "Full article addresses B. canis prevalence, transmission, regulations, and public health risk"
  - - from: pub_cdc_brucellosis_canis_2018
      type: mentions
      to: concept_brucellosis_testing
      evidence: "Article reviews diagnostic methods including culture (gold standard), serology (RSAT, AGID), and PCR; notes that B. canis is the primary serovar in US dogs and culture requires up to 9 days"
  - from: pub_cdc_brucellosis_canis_2018
    type: mentions
    to: concept_brucellosis_treatment
    evidence: "Article states that treatment alone after reproductive failure is usually unsuccessful; recommended multimodal approach includes surgical sterilization plus antimicrobial drugs"
  - from: pub_cdc_brucellosis_canis_2018
    type: mentions
    to: org_usda_aphis
    evidence: "Article references USDA guidance and notes the absence of federal mandate for B. canis testing before interstate dog movement"
  - from: concept_brucellosis_testing
    type: mentions
    to: concept_brucellosis_canis
    evidence: "Testing protocols (RSAT, AGID, culture, PCR) are described as tools for detecting B. canis infection"

tags: [vet_research, brucellosis, b_canis, testing, treatment, zoonotic, cdc, usda, interstate_movement]
---

# Brucellosis in Dogs and Public Health Risk (CDC Emerging Infectious Diseases, August 2018)

## Summary

An analysis published in *Emerging Infectious Diseases* (volume 24, number 8, August 2018) evaluating serologic data, transmission patterns, and regulations relating to *Brucella canis* in dogs in the United States. The article, authored by CDC staff, concludes that canine brucellosis remains endemic to many parts of the world and poses a persistent threat to human health and animal welfare unless stronger control measures are implemented — specifically, mandatory testing of dogs before interstate or international movement. It reviews diagnostic testing, treatment limitations, and the regulatory gap between veterinary and public health authorities.

The note is included to diversify the corpus's veterinary research domain beyond the DCM/diet thread and to seed a potential Cat 3 contradiction pair: the article frames treatment as generally unsuccessful as a standalone intervention ("antimicrobial drug treatment alone after signs of reproductive failure is usually unsuccessful") while other sources in the corpus note that treatment *with* neutering is the recommended multimodal protocol when euthanasia is declined — a tension between "treatment doesn't work" and "treatment is a fallback option that requires neutering."

## What the article addresses

On the regulatory gap:
> "The World Health Organization and the World Organisation for Animal Health do not have policies relating to brucellosis caused by B. canis. In the United States, where B. canis was first isolated, the response is piecemeal."

The article notes that the absence of a federal mandate for B. canis testing before interstate dog movement is a critical gap. It specifically cites kennel outbreaks in the US, Hungary, Sweden, and Colombia linked to interregional and international movement of breeding dogs.

On diagnostic testing:
- **Culture** is described as the standard test for B. canis — though it requires up to 9 days, poses biosafety risk to laboratory personnel, and can produce false negatives due to intermittent bacteremia.
- Serologic tests (RSAT, AGID) are used for screening and surveillance but have specificity limitations; positive screening results require confirmatory testing.
- PCR is noted as an alternative for direct detection.

On treatment:
> "Antimicrobial drug treatment alone after signs of reproductive failure is usually unsuccessful because of the ability of the bacteria to sequester intracellularly for long periods and cause episodic bacteremia."

The recommended course when euthanasia is declined is described as **multimodal**: surgical sterilization (spay/neuter) plus antimicrobial drugs. Treatment failures are noted as more frequent in males because of bacterial sequestration in the prostate.

On the human health risk:
The article emphasizes zoonotic transmission risk, especially for high-exposure professional groups (veterinarians, breeders, kennel workers). It references educational materials and reporting recommendations as prevention tools.

## A note on the treatment contradiction

This article's framing — that treatment alone is "usually unsuccessful" — contrasts with other veterinary sources (e.g., USDA APHIS guidance and Cosford 2018) that present treatment as a viable fallback option provided neutering is performed and monitoring is ongoing. The corpus treats this as a normative contradiction (what level of success do you attribute to treatment, and under what conditions) rather than a factual one. A forthcoming note on brucellosis treatment protocols will anchor the alternative position.

## Provenance and limitations

The summary author accessed the CDC Emerging Infectious Diseases article directly via WebFetch. All quoted statements above are sourced from the live article text. Specific items that should be verified: the article does not provide a specific US prevalence figure for B. canis; the "interstate movement" gap is stated but no specific legislation or rulemaking effort is cited.

## Sources

- "Brucellosis in Dogs and Public Health Risk." *Emerging Infectious Diseases* 24(8), August 2018. CDC (canonical URL of record): https://wwwnc.cdc.gov/eid/article/24/8/17-1171_article
- USDA APHIS brucellosis guidance for dog breeders (corpus companion source): https://www.aphis.usda.gov/publications/animal_welfare/2016/bro-brucellosis-breeders.pdf
- Cosford KL. "Brucella canis: An update on research and clinical management." *Can Vet J* 2018 (corpus companion source for treatment protocol detail): https://ncbi.nlm.nih.gov/pmc/articles/PMC5731389/