---
note_id: cj_2024_cpr_aurora_pit_bull_repeal
source_url: https://www.cpr.org/2024/11/06/aurora-voters-repeal-pit-bull-ban/
source_title: "Aurora voters agree to repeal 20-year-old ban on pit bull dogs"
source_date: "2024-11-06"
source_publisher: "Colorado Public Radio (CPR News)"
license: fair_use_excerpt
license_note: "Copyright held by Colorado Public Radio (a nonprofit / member-supported public-radio organization). Excerpted for non-commercial research under fair use. CPR articles are publicly readable without paywall."
accessed_on: "2026-04-30"
domain: community_journalism

entities:
  - id: pub_cpr_aurora_pit_bull_repeal_2024
    type: publication
    canonical: "Aurora voters agree to repeal 20-year-old ban on pit bull dogs (CPR News, 2024-11-06)"
  - id: org_cpr_news
    type: organization
    canonical: "Colorado Public Radio (CPR News)"
    is_regulatory: false
  - id: loc_aurora_colorado
    type: location
    canonical: "Aurora, Colorado"
    jurisdiction_type: municipal
  - id: org_aurora_city_council
    type: organization
    canonical: "Aurora City Council"
    is_regulatory: true
  - id: event_aurora_question_3a_2024_11_05
    type: event
    canonical: "Aurora ballot Question 3A (pit bull ban repeal)"
    timestamp: "2024-11-05"
    status: resolved
  # concept_bsl, breed_american_pit_bull_terrier, breed_american_staffordshire_terrier
  # are reused from the municipal_policy and breed_standards domains; this note
  # only declares the new Staffordshire Bull Terrier entity it introduces.
  - id: breed_staffordshire_bull_terrier
    type: breed
    canonical: "Staffordshire Bull Terrier"

edges:
  - from: pub_cpr_aurora_pit_bull_repeal_2024
    type: authored_by
    to: org_cpr_news
    evidence: "Article published on cpr.org under CPR News byline"
  - from: pub_cpr_aurora_pit_bull_repeal_2024
    type: subject_of
    to: event_aurora_question_3a_2024_11_05
    evidence: "Article's primary subject is the November 5, 2024 ballot vote on Question 3A repealing Aurora's pit bull ban"
  - from: pub_cpr_aurora_pit_bull_repeal_2024
    type: mentions
    to: concept_bsl
    evidence: "Article frames the Aurora measure as the repeal of a long-standing breed-specific ban"
  - from: pub_cpr_aurora_pit_bull_repeal_2024
    type: mentions
    to: breed_american_pit_bull_terrier
    evidence: "The breed named in the ballot measure and headline; ordinance covered American Pit Bull Terriers"
  - from: pub_cpr_aurora_pit_bull_repeal_2024
    type: mentions
    to: breed_american_staffordshire_terrier
    evidence: "Aurora's restricted-breed ordinance covered American Staffordshire Terriers alongside APBT"
  - from: pub_cpr_aurora_pit_bull_repeal_2024
    type: mentions
    to: breed_staffordshire_bull_terrier
    evidence: "Aurora's restricted-breed ordinance covered Staffordshire Bull Terriers alongside APBT and AmStaff"
  - from: pub_cpr_aurora_pit_bull_repeal_2024
    type: mentions
    to: org_aurora_city_council
    evidence: "Article recounts the Aurora City Council's 2021 attempt to repeal the ban administratively, which was reversed in court"
  - from: event_aurora_question_3a_2024_11_05
    type: located_in
    to: loc_aurora_colorado
    evidence: "The ballot measure was a municipal referendum in Aurora, Colorado"
  - from: org_aurora_city_council
    type: located_in
    to: loc_aurora_colorado
    evidence: "Aurora City Council is the legislative body of the City of Aurora, Colorado"
  - from: org_aurora_city_council
    type: regulates
    to: concept_bsl
    evidence: "The Aurora City Council originally enacted the 2005 BSL ordinance and submitted Question 3A to voters in 2024 after a court ruled the council could not unilaterally repeal it"

tags: [community_journalism, municipal_policy, bsl, pit_bull, alias_chain_test]
---

# Aurora voters agree to repeal 20-year-old ban on pit bull dogs (CPR News, 2024-11-06)

## Summary

CPR News reports that on November 5, 2024, Aurora, Colorado voters approved **Question 3A**, repealing the city's roughly 20-year-old ban on pit bull dogs. The Aurora ordinance, originally enacted in 2005 and reaffirmed by voters in 2014, restricted ownership of three breeds named by the ordinance: **American Pit Bull Terriers**, **American Staffordshire Terriers**, and **Staffordshire Bull Terriers**.

The article recounts the legal backstory: in 2021, the Aurora City Council voted to remove the breed restrictions administratively, without returning the question to voters. An Aurora resident sued, arguing the city charter required any change to a voter-enacted ordinance to be made by the voters. The courts agreed; by 2023 the ban had been judicially reinstated, sending the question back to the November 2024 ballot as Question 3A.

The CPR article reports the measure was approved on election night. (Note: the precise vote share reported by different outlets varies — CPR's election-night reporting cites a preliminary tally; the canonical certified result is via Adams/Arapahoe county election offices. This summary deliberately does not commit to a specific percentage figure that could not be verified directly against the live page.)

## Cross-domain connections

This note is the community-journalism counterpart to a (forthcoming) `municipal_policy` domain note that will ingest the underlying ordinance and ballot text. The pairing exercises:

- **Cat 4 (alias resolution at the breed layer):** the article uses the canonical breed name "American Pit Bull Terrier" alongside the colloquial "pit bull." The alias registry in `ontology.yaml#aliases.pit_bull` covers this directly; the registry-level note about distinguishing APBT from American Staffordshire Terrier is exercised here because Aurora's ordinance treats them as separate listed breeds.
- **Cat 2c (multi-hop):** `pub_cpr_aurora_pit_bull_repeal_2024 → event_aurora_question_3a_2024_11_05 → loc_aurora_colorado` is a publication→event→location traversal across three entity types.
- **Cross-domain (`community_journalism` ↔ `municipal_policy`):** local-press coverage of a municipal-policy implementation event. The article should resolve to the same `event_aurora_question_3a_2024_11_05` node as the municipal-policy primary source when both are ingested.

The Sentinel Colorado article (`sources/community_journalism.yaml#cj_sentinel_aurora_pit_bull_repeal_2024`) deliberately covers the same event from a different outlet; if it is later authored as a vault note, both notes should connect to the same `event_aurora_question_3a_2024_11_05` and `loc_aurora_colorado` nodes — that is the same-event-different-attribution Cat 4 publication-layer test.

## Provenance and limitations

Article retrieved via WebSearch top-result match for the source URL plus secondary search for the legal backstory. Direct WebFetch was not available in this authoring session. Specific numeric claims (e.g. exact vote percentage) are deliberately omitted from this summary because available WebSearch summaries returned conflicting figures across outlets, and the load-bearing-numbers verification rule applies. Maintainer should re-fetch the live CPR page before any specific vote tally is treated as canonical for evaluation purposes.

## Sources

- CPR News article (canonical URL of record): https://www.cpr.org/2024/11/06/aurora-voters-repeal-pit-bull-ban/
- Ballotpedia entry for Aurora Question 3A (November 2024): https://ballotpedia.org/Aurora,_Colorado,_Repeal_Ban_on_Owning_Pit_Bull_Dogs_Measure_(November_2024)
- Companion same-event coverage: Sentinel Colorado, "Aurora voters agree to repeal 20-year-old ban on pit bull dogs"
