---
note_id: muni_bsl_court_challenges
source_url: https://law.justia.com/cases/colorado/supreme-court/1991/90sa342-0.html
source_title: "Colorado Dog Fanciers Association, Inc. v. Denver"
source_date: "1991-11-12"
source_publisher: "Justia (Colorado Supreme Court)"
license: public_domain_judicial
license_note: "Colorado Supreme Court opinions are public domain; citing for legal holdings, procedural posture, and outcome."
accessed_on: "2026-05-03"
domain: municipal_policy
jurisdiction: "Multi-jurisdiction (CO, IA, OH, IL, FL)"
event_status: resolved

# Ontology-aligned entity declarations introduced by this note.
# concept_pit_bull and concept_bsl are reused from the Montreal and Ontario
# notes so cross-jurisdiction query traverses shared concept entities.
entities:
  - id: pub_colorado_dog_fanciers_v_denver_1991
    type: publication
    canonical: "Colorado Dog Fanciers Association, Inc. v. City and County of Denver, 814 P.2d 646 (Colo. 1991)"
  - id: pub_toledo_v_tellings_2007
    type: publication
    canonical: "Toledo v. Tellings, 114 Ohio St.3d 278, 871 N.E.2d 1152 (Ohio 2007)"
  - id: pub_danker_v_council_bluffs_2022
    type: publication
    canonical: "Danker v. City of Council Bluffs, 57 F.4th 583 (8th Cir. 2023)"
  - id: pub_aurora_v_acf
    type: publication
    canonical: "American Canine Foundation v. City of Aurora (D. Colo. 2020)"
  - id: event_colorado_dog_fanciers_decision
    type: event
    canonical: "Colorado Supreme Court decision in Colorado Dog Fanciers v. Denver"
    timestamp: "1991-11-12"
    status: resolved
  - id: event_toledo_v_tellings_decision
    type: event
    canonical: "Ohio Supreme Court decision in Toledo v. Tellings"
    timestamp: "2007-08-29"
    status: resolved
  - id: event_danker_council_bluffs_decision
    type: event
    canonical: "8th Circuit decision in Danker v. City of Council Bluffs"
    timestamp: "2022-11-08"
    status: resolved
  - id: concept_due_process
    type: concept
    canonical: "Procedural due process (legal concept)"
  - id: concept_equal_protection
    type: concept
    canonical: "Equal protection (legal concept)"
  - id: concept_vagueness_doctrine
    type: concept
    canonical: "Vagueness doctrine (legal concept)"
  - id: concept_rational_basis
    type: concept
    canonical: "Rational basis review (legal concept)"

# Edges introduced by this note.
edges:
  - from: pub_colorado_dog_fanciers_v_denver_1991
    type: subject_of
    to: event_colorado_dog_fanciers_decision
    evidence: "Colorado Dog Fanciers Association, Inc. v. City and County of Denver is the Colorado Supreme Court opinion whose date is 1991-11-12; the opinion is the publication that is the event."
  - from: pub_toledo_v_tellings_2007
    type: subject_of
    to: event_toledo_v_tellings_decision
    evidence: "Toledo v. Tellings is the Ohio Supreme Court opinion whose date is 2007-08-29."
  - from: pub_danker_v_council_bluffs_2022
    type: subject_of
    to: event_danker_council_bluffs_decision
    evidence: "Danker v. City of Council Bluffs is the 8th Circuit opinion filed 2022-11-08."
  - from: pub_colorado_dog_fanciers_v_denver_1991
    type: mentions
    to: concept_pit_bull
    evidence: "The case concerns Denver's Revised Municipal Code Sec. 8-55 prohibiting pit bulls; the opinion references the breed definition and the city's rationale for targeting pit bulls specifically."
  - from: pub_colorado_dog_fanciers_v_denver_1991
    type: mentions
    to: concept_bsl
    evidence: "Colorado Dog Fanciers v. Denver is the foundational case in which a court applied rational basis review to a municipal BSL ordinance and upheld it."
  - from: pub_colorado_dog_fanciers_v_denver_1991
    type: mentions
    to: concept_rational_basis
    evidence: "The Colorado Supreme Court applied rational basis review: the ordinance neither proceeded along suspect lines nor infringed a fundamental right, so it was upheld if rationally related to a legitimate government interest."
  - from: pub_toledo_v_tellings_2007
    type: mentions
    to: concept_pit_bull
    evidence: "Toledo v. Tellings challenged Ohio's statutory definition of 'vicious dog' including pit bulls and Toledo's municipal code restrictions on pit bull ownership; the court found the laws unconstitutional as applied."
  - from: pub_toledo_v_tellings_2007
    type: mentions
    to: concept_due_process
    evidence: "The Ohio Supreme Court held that R.C. 955.22 and Toledo Municipal Code 505.14 violated procedural due process by not providing dog owners a meaningful opportunity to be heard on whether their dog was 'vicious'; the court also held the laws failed rational basis review once the trial court found pit bulls were not inherently dangerous."
  - from: pub_toledo_v_tellings_2007
    type: mentions
    to: concept_vagueness_doctrine
    evidence: "The appellate court had held the statutes void for vagueness due to the lack of an exact statutory definition of 'pit bull' and the highly subjective nature of breed identification; the Ohio Supreme Court reversed on this specific ground but upheld the due process holding."
  - from: pub_danker_v_council_bluffs_2022
    type: mentions
    to: concept_pit_bull
    evidence: "Danker concerns Council Bluffs Municipal Code Sec. 4.20.112 (effective 2005-01-01) which prohibited owning, possessing, or harboring any pit bull within the city."
  - from: pub_danker_v_council_bluffs_2022
    type: mentions
    to: concept_equal_protection
    evidence: "Dog owners argued the Council Bluffs ordinance violated equal protection; the 8th Circuit applied rational basis review and affirmed summary judgment for the city, finding the ordinance rationally related to the city's interest in public health and safety."
  - from: pub_danker_v_council_bluffs_2022
    type: mentions
    to: concept_rational_basis
    evidence: "The court held that dog bites are a public health issue, that the City had a conceivable basis to believe banning pit bulls would promote safety, and that the ordinance did not need to be a perfect fit — rational basis review requires only that the legislature could have had a rational reason for the classification."
  - from: org_city_and_county_of_denver
    type: regulates
    to: concept_pit_bull
    evidence: "The Colorado Supreme Court in Colorado Dog Fanciers v. Denver confirmed Denver's regulatory authority over pit-bull-type dogs via Sec. 8-55."
  - from: org_city_and_county_of_denver
    type: located_in
    to: loc_denver_co
    evidence: "City and County of Denver is located in Colorado."
  - from: event_colorado_dog_fanciers_decision
    type: located_in
    to: loc_denver_co
    evidence: "The Colorado Supreme Court decision was issued in Denver, CO."

tags: [municipal_policy, court_challenges, bsl, pit_bull, constitutional_law, due_process, equal_protection, vagueness, rational_basis, multi_jurisdiction]
---

# Court challenges to municipal breed-specific legislation

## Summary

Breed-specific legislation (BSL) has been the subject of repeated constitutional litigation across U.S. jurisdictions, with challenges proceeding on grounds of **procedural due process**, **substantive due process**, **equal protection**, and the **void-for-vagueness doctrine**. This note surveys four key cases at the municipal level — two upholding BSL ordinances and two finding fault — to surface the cross-jurisdiction pattern of how courts evaluate breed-based regulation.

The general doctrinal result: courts consistently apply **rational basis review** to BSL ordinances, and under that deferential standard, most BSL survives. The rare unconstitutional findings tend to involve procedural due process failures (no hearing opportunity) or vagueness in breed-identification definitions, rather than a substantive ruling that breed-based classification is per se irrational.

## Case 1: Colorado Dog Fanciers Association v. Denver (Colo. 1991)

**Citation:** Colorado Dog Fanciers Association, Inc. v. City and County of Denver, 814 P.2d 646 (Colo. 1991)

**Procedural posture:** Multiple consolidated lawsuits challenged Denver Revised Municipal Code Sec. 8-55 on constitutional grounds. Denver District Court upheld the ordinance (Judge Rothenberg, June 28, 1990). Plaintiffs appealed to the Colorado Supreme Court.

**Outcome:** Affirmed in part, reversed in part. The Colorado Supreme Court upheld the ordinance under **rational basis review** as a constitutional exercise of Denver's police power. The Court held:
- The ordinance neither implicated a suspect classification nor a fundamental right, so rational basis was the correct standard.
- Denver's factual findings — that pit bulls are stronger than most dogs, give no warning signals before attacking, are less willing to retreat, and inflict more severe injuries — were a sufficient rational basis for the ban.
- The burden of proof at any hearing to contest whether a dog is a pit bull rests on the **city**, not the dog owner, but only a **preponderance of the evidence** standard applies (not proof beyond a reasonable doubt) because the proceeding is regulatory, not criminal.
- The portion of Sec. 8-55 limiting pit bull license applications to owners of **previously licensed** dogs was severed as lacking rational basis.

**Significance:** The foundational BSL case establishing that rational basis review is the default standard and that legislative findings about pit bull attack severity are sufficient to survive it.

## Case 2: Toledo v. Tellings (Ohio 2007)

**Citation:** Toledo v. Tellings, 114 Ohio St.3d 278, 871 N.E.2d 1152 (Ohio 2007)

**Procedural posture:** Paul Tellings owned three dogs identified as pit bulls. He was charged under Toledo Municipal Code 505.14(a) and Ohio Revised Code 955.22 for violating the one-pit-bull-per-household limit and failing to maintain liability insurance. Tellings challenged the constitutionality of both the municipal code and the state statute.

**Outcome:** Split decision. The Ohio Supreme Court held:
- **Procedural due process:** R.C. 955.22 violated procedural due process by not providing dog owners a meaningful opportunity to be heard on whether their dog was "vicious" before charges were filed.
- **Substantive due process / rational basis:** Once the trial court found that pit bulls as a breed are not more dangerous than other breeds, the statutes were not rationally related to a legitimate state interest and thus failed substantive due process.
- **Vagueness:** The appellate court had held the laws void for vagueness due to the lack of an exact statutory definition of "pit bull." The Ohio Supreme Court reversed on this specific ground, holding "pit bull" has a discernible meaning and that breed identification is a factual question for the evidence, not a constitutional question.

**Key distinction from Colorado Dog Fanciers:** The trial court record in Toledo included expert testimony specifically finding that pit bulls are not inherently more dangerous. That factual finding undermined the rational basis for the law in a way that Denver's deferential review posture did not.

**Significance:** One of the few BSL cases where an appellate court found a constitutional violation — driven by the procedural due process failure and the anti-correlation evidence in the record.

## Case 3: Danker v. City of Council Bluffs (8th Cir. 2022)

**Citation:** Danker v. City of Council Bluffs, 57 F.4th 583 (8th Cir. 2023); see also 569 F. Supp. 3d 866 (S.D. Iowa 2021)

**Procedural posture:** Dog owners sued Council Bluffs, Iowa under 42 U.S.C. § 1983, challenging Municipal Code § 4.20.112 (effective **January 1, 2005**) which prohibited owning, possessing, or harboring any pit bull within the city. The ordinance defined pit bull as any dog that is an American Pit Bull Terrier, American Staffordshire Terrier, or Staffordshire Bull Terrier; any dog displaying the majority of physical traits of those breeds; or any dog substantially conforming to AKC or UKC breed standards.

The district court granted summary judgment to the city on all claims (equal protection, procedural due process, vagueness). The 8th Circuit affirmed on appeal, applying **rational basis review**.

**Outcome:** Affirmed. The 8th Circuit held:
- The ordinance was subject to rational basis review (no suspect classification, no fundamental right).
- The city had a "conceivable basis" for the ban: a disproportionate number of dog bites in Council Bluffs were attributed to pit bulls in 2003–2004.
- The ordinance's classification did not need to be a "perfect fit"; rational basis requires only that the legislature could have had a rational reason.
- Dog owners' expert evidence (canine behavior research, scientific studies) was insufficient to negate every conceivable basis for the ordinance.
- From 2007 through 2020, reported dog bites in Council Bluffs were **25 percent lower** than before the ordinance — a factual claim the city presented to support the law's effectiveness.

**Significance:** Confirms that BSL survives equal protection challenge under rational basis; the city's post-ordinance bite data is cited as an effectiveness argument, which is the kind of empirical claim that fuels Cat 1 retrieval ("does BSL reduce dog attacks?").

## Case 4: American Canine Foundation v. City of Aurora (D. Colo. 2020)

**Citation:** American Canine Foundation v. City of Aurora (D. Colo. 2020)

**Procedural posture:** ACF sued the City of Aurora, Colorado to challenge Aurora City Code § 14-75, which regulated possession of pit bulls and other restricted breeds. Several claims were dismissed. The remaining takings, substantive due process, and equal protection claims were tried to the bench.

**Outcome:** For defendant (City of Aurora) on all remaining claims. The court found:
- The ordinance had a **legitimate purpose** (protecting health and safety of residents).
- Ample evidence established a **rational relationship** between the ordinance and that purpose: pit bulls tend to be stronger than other breeds, give no warning signals before attacking, are less willing to retreat, and attacks result in multiple bites and greater severity.
- Plaintiffs did not meet the burden of showing the ordinance was not rationally related to the legitimate purpose.
- No deprivation of due process or equal protection; no abuse of the city's police power.

**Aurora context:** Aurora's ordinance was enacted in 2005 or later, after Aurora awaited the outcome of Denver's litigation against the state preemption law (HB 1279, 2004). Aurora City Council found that incidents involving restricted breeds were continuing to occur and that the ordinance was necessary.

**Significance:** Confirms the Colorado pattern — after the Colorado Supreme Court's 1991 Denver decision, Colorado municipalities continued to enact and successfully defend BSL.

## Cross-case doctrinal pattern

| Case | Court | Year | Result | Primary grounds |
|------|-------|------|--------|-----------------|
| Colorado Dog Fanciers v. Denver | CO Supreme Court | 1991 | Upheld | Rational basis |
| Toledo v. Tellings | OH Supreme Court | 2007 | **Struck down** (procedural due process; rational basis failed on facts) | Due process, rational basis |
| Danker v. Council Bluffs | 8th Cir. | 2022 | Upheld | Equal protection, rational basis |
| Aurora v. ACF | D. Colo. | 2020 | Upheld | Substantive due process, equal protection |

**Overall outcome rate:** 3 of 4 cases upheld the BSL ordinance. The one exception (Toledo v. Tellings) involved both a procedural due process failure and fact-specific evidence that pit bulls were not more dangerous — suggesting the challenge route most likely to succeed requires both a procedural defect *and* counter-evidence on breed dangerousness.

## Cross-references

- **Denver BSL (enactment):** `vault/municipal_policy/denver-bsl-1989-enactment.md` — includes Colorado Dog Fanciers v. Denver as the court challenge to Denver's Sec. 8-55.
- **Calgary model (no BSL):** `vault/municipal_policy/calgary-rpob-47m2021.md` — the behaviour-based alternative that avoids BSL litigation exposure entirely.
- **Ontario DOLA:** `vault/municipal_policy/ontario-dola-statute.md` — provincial-level BSL that survived a Supreme Court of Canada challenge (Ontario's DOLA provisions remained in force).

## Sources

- Justia, "Colorado Dog Fanciers Association, Inc. v. City and County of Denver, 814 P.2d 646 (Colo. 1991)": https://law.justia.com/cases/colorado/supreme-court/1991/90sa342-0.html
- vLex, "Toledo v. Tellings, 114 Ohio St.3d 278, 871 N.E.2d 1152 (Ohio 2007)": https://case-law.vlex.com/vid/toledo-v-tellings-no-891675944
- Casetext, "Danker v. City of Council Bluffs, 57 F.4th 583 (8th Cir. 2023)": https://casetext.com/case/danker-v-the-city-of-council-bluffs-iowa
- DogsBite.org PDF, "Aurora v. American Canine Foundation (Florence Vianzon)": https://www.dogsbite.org/pdf/aurora-v-acf-florence-vianzon.pdf
- Source manifest entry: `sources/municipal_policy.yaml#muni_bsl_court_challenges`