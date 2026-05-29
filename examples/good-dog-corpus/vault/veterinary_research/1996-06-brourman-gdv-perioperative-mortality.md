---
note_id: vet_1996_brourman_gdv_perioperative_mortality
source_url: https://avmajournals.avma.org/view/journals/javma/208/11/javma.1996.208.11.1855.xml
source_title: "Factors associated with perioperative mortality in dogs with surgically managed gastric dilatation-volvulus: 137 cases (1988–1993)"
source_date: "1996-06-01"
source_publisher: "Journal of the American Veterinary Medical Association"
license: fair_use_excerpt
license_note: "JAVMA peer-reviewed article; excerpted under fair use for corpus purposes with attribution. Full text available via AVMA journals."
accessed_on: "2026-05-03"
domain: veterinary_research

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: pub_brourman_1996_gdv_mortality
    type: publication
    canonical: "Factors associated with perioperative mortality in dogs with surgically managed gastric dilatation-volvulus: 137 cases (1988–1993)"
    aliases: ["Brourman 1996 JAVMA GDV study", "Brourman et al. 1996"]
  - id: person_jeff_brourman
    type: person
    canonical: "Jeff D. Brourman"
    aliases: ["J.D. Brourman", "Brourman"]
  - id: concept_gdv
    type: concept
    canonical: "Gastric dilatation-volvulus"
    aliases: ["GDV", "bloat", "gastric torsion"]
  - id: concept_gastric_necrosis
    type: concept
    canonical: "Gastric necrosis secondary to GDV"
    aliases: ["stomach wall necrosis", "gastric ischemia"]
  - id: concept_prophylactic_gastropexy
    type: concept
    canonical: "Prophylactic gastropexy"
    aliases: ["gastropexy", "preventive gastropexy"]
  - id: breed_great_dane
    type: breed
    canonical: "Great Dane"
    aliases: ["Great Danes"]
  - id: breed_st_bernard
    type: breed
    canonical: "Saint Bernard"
    aliases: ["St. Bernard", "St Bernard"]

edges:
  - from: pub_brourman_1996_gdv_mortality
    type: authored_by
    to: person_jeff_brourman
    evidence: "Jeff D. Brourman is first and corresponding author of JAVMA 208(11):1855-1858, 1996"
  - from: pub_brourman_1996_gdv_mortality
    type: subject_of
    to: concept_gdv
    evidence: "Primary topic: perioperative mortality in surgically managed GDV in 137 dogs"
  - - from: pub_brourman_1996_gdv_mortality
      type: mentions
      to: concept_gastric_necrosis
      evidence: "Gastric necrosis identified as the factor most strongly associated with mortality (46% vs baseline)"
  - from: pub_brourman_1996_gdv_mortality
    type: mentions
    to: concept_prophylactic_gastropexy
    evidence: "Study notes that without gastropexy, GDV recurs in up to 80% of affected dogs"
  - from: pub_brourman_1996_gdv_mortality
    type: mentions
    to: breed_great_dane
    evidence: "Great Danes represented the largest breed category in the study cohort (noted as a high-risk breed)"
  - from: pub_brourman_1996_gdv_mortality
    type: mentions
    to: breed_st_bernard
    evidence: "Saint Bernards noted as another overrepresented breed in the GDV case population"

tags: [vet_research, gdv, bloat, surgery, mortality, gastric_necrosis, breed_predisposition]
---

# Factors associated with perioperative mortality in dogs with surgically managed gastric dilatation-volvulus: 137 cases (1988–1993) (Brourman et al., JAVMA 1996)

## Summary

A retrospective analysis of 137 surgically managed GDV cases presenting to university and private specialty practices between 1988 and 1993, published in the *Journal of the American Veterinary Medical Association* (volume 208, issue 11, pages 1855–1858). The study evaluated signalment, preoperative and postoperative treatments, intraoperative findings, surgical technique, and laboratory results for association with mortality. Overall perioperative mortality was **18%** (24/137). The study found that certain clinical findings — gastric necrosis, need for partial gastrectomy or splenectomy, and preoperative cardiac arrhythmias — were statistically associated with mortality rates above 30%, while signalment factors including age did not significantly influence survival.

This note provides a baseline mortality figure (18%) for the surgical management of GDV from the pre-prophylactic-gastropexy-era literature, and is a key reference point for the later 2003 Ellison cost-effectiveness analysis and the 2023 prophylactic gastropexy outcomes study also in this domain.

## Key findings

Sample and overall mortality:
- 137 dogs with surgically managed GDV; cases drawn from both university and private specialty referral practices.
- Overall perioperative mortality: **18%** (24/137).
- Mortality did not differ significantly between university and private specialty practice settings, suggesting that institutional setting and management differences were not the primary drivers of outcome.

Factors significantly associated with increased mortality:
- **Gastric necrosis** identified at surgery: mortality **46%** (13/28). This was the single strongest predictor.
- **Partial gastrectomy** performed: mortality **35%** (8/23).
- **Splenectomy** performed: mortality **32%** (10/31).
- **Both partial gastrectomy and splenectomy** performed together: mortality **55%** (6/11).
- **Preoperative cardiac arrhythmias**: mortality **38%** (6/16).

Age and signalment:
- Mortality in dogs over 10 years old was **not** significantly greater than in younger dogs, contrary to some prior assumptions.
- Breed representation aligned with known GDV predisposition: Great Danes and Saint Bernards were overrepresented.

Surgical technique:
- Surgical technique differences between institutions were not associated with mortality.
- The study does not directly evaluate prophylactic gastropexy (which is performed on healthy at-risk dogs, not at the time of emergency GDV surgery), but notes: "Without corrective surgery (gastropexy), GDV recurs in up to 80% of affected dogs" — citing a median survival of 188 days without gastropexy.

## Place in the corpus

This note seeds the `concept_gdv` and `concept_gastric_necrosis` entity surfaces in the veterinary research domain, distinct from the DCM/diet thread already established in notes 1–5. The 18% baseline perioperative mortality figure is the reference point against which later studies measuring the effect of prophylactic gastropexy and specialist-vs-general-surgeon outcomes are compared. It also anchors the `breed_great_dane` and `breed_st_bernard` breed entities as canonical GDV-predisposed breeds with sourced prevalence data.

## Sources

- Brourman JD, Schertel ER, Allen DA, et al. "Factors associated with perioperative mortality in dogs with surgically managed gastric dilatation-volvulus: 137 cases (1988–1993)." *J Am Vet Med Assoc* 208(11):1855–1858, 1996. (canonical URL of record): https://avmajournals.avma.org/view/journals/javma/208/11/javma.1996.208.11.1855.xml