---
note_id: muni_denver_pit_bull_ban_1989
source_url: https://www.animallaw.info/local/louscodenver8_55.htm
source_title: "CO - Denver - Breed - Sec. 8-55. Pit bulls prohibited."
source_date: "1989"
source_publisher: "Animal Legal & Historical Center (archived)"
license: fair_use_research
license_note: "Animal Legal & Historical Center is a public legal education resource; ordinance text excerpted for factual attestation of bylaw content and date."
accessed_on: "2026-05-03"
domain: municipal_policy
jurisdiction: "Denver, CO, USA"
lifecycle_id: denver_pit_bull_ban_lifecycle

# Ontology-aligned entity declarations introduced by this note.
# concept_pit_bull and concept_bsl are reused from the Montreal and Ontario
# notes so cross-jurisdiction queries traverse shared concept entities.
entities:
  - id: org_city_and_county_of_denver
    type: organization
    canonical: "City and County of Denver"
    is_regulatory: true
  - id: loc_denver_co
    type: location
    canonical: "Denver, CO, USA"
    jurisdiction_type: municipal
  - id: pub_denver_rmc_sec_8_55_1989
    type: publication
    canonical: "Denver Revised Municipal Code Sec. 8-55, Ordinance No. 404, Series of 1989"
  - id: pub_denver_ballot_measure_2j_2020
    type: publication
    canonical: "Denver Ballot Measure 2J (2020)"
  - id: event_denver_ban_enacted_1989
    type: event
    canonical: "Denver city council adoption of pit bull ban (Ordinance No. 404, Series of 1989)"
    timestamp: "1989-08-01"
    status: resolved
  - id: event_denver_ballot_measure_2j_2020
    type: event
    canonical: "Denver voters approve Ballot Measure 2J repealing pit bull ban"
    timestamp: "2020-11-03"
    status: resolved
  - id: event_denver_ban_repeal_effective
    type: event
    canonical: "Denver pit bull ban repeal takes effect"
    timestamp: "2025-01-01"
    status: resolved

# Edges introduced by this note.
edges:
  - from: pub_denver_ballot_measure_2j_2020
    type: supersedes
    to: pub_denver_rmc_sec_8_55_1989
    evidence: "Ballot Measure 2J (2020) was the voter-approved instrument that formally repealed Denver's Sec. 8-55 pit bull ban; per Denver news reporting, the measure led with over 65% approval on 2020-11-03 and the repeal took effect 2025-01-01."
  - from: pub_denver_rmc_sec_8_55_1989
    type: subject_of
    to: event_denver_ban_enacted_1989
    evidence: "Denver Revised Municipal Code Sec. 8-55 is the document adopted at the July 31-August 1, 1989 Denver city council session (Bill No. 434, Series of 1989), signed by Mayor Federico Peña on 1989-08-02."
  - from: pub_denver_ballot_measure_2j_2020
    type: subject_of
    to: event_denver_ballot_measure_2j_2020
    evidence: "Ballot Measure 2J is the document adopted by Denver voters on 2020-11-03 that repealed Sec. 8-55."
  - from: pub_denver_rmc_sec_8_55_1989
    type: mentions
    to: concept_pit_bull
    evidence: "Sec. 8-55 defines 'pit bull' as any dog that is an American Pit Bull Terrier, American Staffordshire Terrier, Staffordshire Bull Terrier, or any dog displaying the majority of physical traits of any of those breeds, or any dog substantially conforming to AKC or UKC standards for those breeds."
  - from: pub_denver_rmc_sec_8_55_1989
    type: mentions
    to: concept_bsl
    evidence: "Denver's Sec. 8-55 is a canonical and long-running North American instance of breed-specific legislation; it predates most other major municipal BSL in the US."
  - from: org_city_and_county_of_denver
    type: regulates
    to: concept_pit_bull
    evidence: "Denver Revised Municipal Code Sec. 8-55 established the City and County of Denver's regulatory authority over pit-bull-type dogs within its jurisdiction from 1989 until the 2025 repeal."
  - from: org_city_and_county_of_denver
    type: located_in
    to: loc_denver_co
    evidence: "City and County of Denver is the municipal government of Denver, CO."
  - from: event_denver_ban_enacted_1989
    type: located_in
    to: loc_denver_co
    evidence: "The ordinance was adopted at Denver city council."
  - from: event_denver_ballot_measure_2j_2020
    type: located_in
    to: loc_denver_co
    evidence: "The ballot measure was voted on in Denver, CO."
  - from: event_denver_ban_repeal_effective
    type: located_in
    to: loc_denver_co
    evidence: "The repeal took effect in Denver city limits."

tags: [municipal_policy, denver, bsl, pit_bull, cat_6_temporal_chain, lifecycle_origin, ballot_measure, home_rule]
---

# Denver Revised Municipal Code Sec. 8-55 — pit bull ban enacted (1989)

## Summary

On the night of **July 31–August 1, 1989**, the Denver City Council adopted **Bill No. 434, Series of 1989**, enacting **Denver Revised Municipal Code Sec. 8-55 ("Pit bulls prohibited")** by a vote of **9 Ayes, 2 Nays, and 1 Abstention**. Mayor **Federico Peña** signed the ordinance on **August 2, 1989**. The law made it unlawful for any person to own, possess, keep, exercise control over, maintain, harbor, transport, or sell any pit bull within the City and County of Denver.

This note is the originating half of the Denver BSL lifecycle. The closing half is the voter-approved **Ballot Measure 2J** passed on **November 3, 2020** (over 65% approval), which formally repealed the ban; the repeal took effect **January 1, 2025**.

## What the ordinance did

Per the Animal Legal & Historical Center's archived ordinance text, Sec. 8-55:

- **Prohibited** owning or harboring any pit bull within Denver city limits, defined as any dog that is an American Pit Bull Terrier, American Staffordshire Terrier, Staffordshire Bull Terrier; any dog displaying the majority of physical traits of one or more of those breeds; or any dog substantially conforming to AKC or UKC breed standards for those breeds.
- **Grandfather clause** (pre-ordinance licensed dogs): Dogs already licensed as pit bulls before the ordinance's publication date (**August 7, 1989**) could remain if their owners applied for and received an annual pit bull license by **January 1, 1990**. Grandfathered owners were required to: (1) obtain **$100,000 liability insurance**; (2) confine the dog in an **eight-foot-high fenced enclosure** posted with "PIT BULL DOG" signs; (3) **muzzle** the dog at all times when outdoors; and (4) have the dog **tattooed with a registration number**.
- **Grandfathered dogs' offspring**: Puppies of grandfathered pit bulls had to be removed from the city or surrendered to the animal shelter for destruction.
- Approximately **300 pit bulls** were registered under the grandfather clause. By 2003, all had died, closing the legal window for any pit bull to legally remain in Denver.

## Triggering incident

The ordinance was catalyzed by a **October 1986 fatal mauling** of a three-year-old boy, **Willie Billingsley**, by a pit bull in southwest Denver. A prior non-fatal pit bull attack in February 1989 of a seven-year-old girl in **Miami, Florida** (which prompted Dade County's pit bull ban) contributed to the political momentum. City Councilmembers **Ramona Martinez** and **Mary DeGroot** cited the Miami case in urging Denver to adopt a similar ban.

## Court challenge: Colorado Dog Fanciers v. Denver

Multiple parties filed consolidated lawsuits in Denver District Court in fall 1989 challenging the ordinance's constitutionality. On **June 28, 1990**, District Judge **Rothenberg** issued a written decision upholding Sec. 8-55 as a constitutional exercise of legislative authority.

Plaintiffs appealed to the **Colorado Supreme Court**. On **November 12, 1991**, the Court affirmed, finding Denver had a **rational basis** for the ban. The Court upheld the city's factual findings that pit bull characteristics — including strength, tenacity, and lack of warning signals before attacking — meant attacks had the potential to be "more severe and more likely to result in fatalities." The Court placed the burden of proof on the city (not the dog owner) to prove a disputed dog was a pit bull at any hearing, but did not require proof beyond a reasonable doubt for a regulatory (non-criminal) purpose. The portion of the ordinance limiting pit bull license applications to owners of **previously licensed** dogs was severed as lacking rational basis.

## State preemption and home rule

In **2004**, the Colorado Legislature enacted **House Bill 1279**, which prohibited municipalities from enacting breed-specific legislation. Denver, as a **home-rule city**, challenged the state's authority over municipal dog regulation. The city prevailed in that litigation, and Sec. 8-55 remained in effect as a home-rule municipal ordinance even after the state law.

## Timeline of repeal attempts

- **February 2020**: Councilman **Chris Herndon** introduced a full repeal measure. Denver City Council passed it **7–4** (Kniesch, Black, Clark, Herndon, Hinds, Sandoval, Torres in favor; Flynn, Kashmann, Ortega, Sawyer opposed). Mayor **Michael Hancock vetoed** the measure — his first and only veto in three terms — citing public safety risk. Council failed to override the veto: the override vote fell **8–5** (nine votes needed).
- **August 2020**: Herndon placed a revised repeal measure on the **November 2020 ballot** as **Ballot Measure 2J**. Denver City Council voted to send it to voters **11–1** (Ortega opposed).
- **November 3, 2020**: Denver voters approved **Ballot Measure 2J** with over **65%** approval.
- **January 1, 2025**: Repeal of Sec. 8-55 took effect. The replacement regime requires a **breed-restricted license** with conditions; dogs with no behavioral incidents within three years graduate to a standard license.

## Status

**Resolved / superseded.** The Denver BSL lifecycle (1989–2025) is now closed. Sec. 8-55 is the originating instrument; Ballot Measure 2J is the closing instrument that [supersedes] it. The 35-year gap between enactment and repeal makes this the longest-running individual-municipal BSL case in the corpus.

## Cross-references

- **Closing half of the lifecycle:** The 2020 Ballot Measure 2J supersession edge is declared in this note; a separate note covering the 2020 ballot measure and 2025 effective date can be added in v0.2 to expand the lifecycle.
- **Court challenge:** `vault/municipal_policy/denver-bsl-court-challenges.md` — covers Colorado Dog Fanciers v. Denver (1991 Colorado Supreme Court) and other municipal BSL court cases (Council Bluffs, Toledo v. Tellings, Aurora v. ACF).
- **Calgary model contrast:** `vault/municipal_policy/calgary-rpob-47m2021.md` — the canonical behaviour-based alternative cited across jurisdictions.
- **Ontario DOLA contrast:** `vault/municipal_policy/ontario-dola-statute.md` — province-level BSL that remains active while Denver's municipal BSL was repealed.

## Sources

- Animal Legal & Historical Center, "CO - Denver - Breed - Sec. 8-55. Pit bulls prohibited." ( ordinance text archived, last checked May 2012): https://www.animallaw.info/local/louscodenver8_55.htm
- Denver Westword, "For two decades, pit bulls have been public enemy #1 in Denver" (2009-09-24): https://www.westword.com/news/for-two-decades-pit-bulls-have-been-public-enemy-1-in-denver-but-maybe-its-time-for-a-recount-5105359
- DogsBite.org, "Denver's Pit Bull Ordinance — History & Judicial Rulings" (2005): https://www.dogsbite.org/pdf/denver-pitbull-ordinance-history-judicial-rulings.pdf
- Denver Post, "Denver City Council fails to overturn Mayor Hancock's veto of pit bull ban repeal" (2020-02-25): https://www.denverpost.com/2020/02/24/denver-pit-bull-repeal-fails/
- Denver Post, "Denver voters repealed the city's pit bull ban. What's next?" (2020-11-06): https://www.denverpost.com/2020/11/06/denver-pit-bull-ban-repeal-details/
- TODAY, "Denver overturns pit bull ban after more than 30 years" (2024-08-29): https://www.today.com/pets/denver-overturns-pit-bull-ban-after-more-30-years-t197853
- Source manifest entry: `sources/municipal_policy.yaml#muni_denver_ban_1989`