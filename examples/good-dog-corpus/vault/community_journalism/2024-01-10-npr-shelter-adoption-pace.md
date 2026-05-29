---
note_id: cj_2024_npr_shelter_adoption_pace
source_url: https://www.npr.org/2024/01/10/1223890115/pet-adoptions-are-not-keeping-pace-with-the-number-of-animals-coming-in
source_title: "Pet adoptions are not keeping pace with the number of animals coming in"
source_date: "2024-01-10"
source_publisher: "NPR (National Public Radio)"
license: fair_use_excerpt
license_note: "Copyright held by NPR. Excerpted for non-commercial research under fair use. NPR articles are publicly readable without paywall."
accessed_on: "2026-04-30"
domain: community_journalism

entities:
  - id: pub_npr_shelter_adoption_pace_2024_01
    type: publication
    canonical: "Pet adoptions are not keeping pace with the number of animals coming in (NPR, 2024-01-10)"
  - id: org_npr
    type: organization
    canonical: "NPR (National Public Radio)"
    is_regulatory: false
  - id: org_shelter_animals_count
    type: organization
    canonical: "Shelter Animals Count"
    is_regulatory: false
  - id: org_humane_rescue_alliance
    type: organization
    canonical: "Humane Rescue Alliance"
    is_regulatory: false
  - id: person_stephanie_filer
    type: person
    canonical: "Stephanie Filer"
  - id: person_julie_depenbrock
    type: person
    canonical: "Julie Depenbrock"
  - id: loc_washington_dc
    type: location
    canonical: "Washington, D.C."
    jurisdiction_type: municipal
  - id: event_shelter_intake_adoption_gap_2023
    type: event
    canonical: "Post-pandemic shelter intake-vs-adoption gap (2023)"
    timestamp: "2023"
    status: ongoing
  - id: concept_post_pandemic_adoption_decline
    type: concept
    canonical: "Post-pandemic shelter adoption decline"
    aliases: ["post-pandemic adoption decline", "shelter overcrowding crisis"]

edges:
  - from: pub_npr_shelter_adoption_pace_2024_01
    type: authored_by
    to: org_npr
    evidence: "Article published on npr.org under NPR News byline"
  - from: pub_npr_shelter_adoption_pace_2024_01
    type: authored_by
    to: person_julie_depenbrock
    evidence: "Article reporting credited to NPR's Julie Depenbrock"
  - from: pub_npr_shelter_adoption_pace_2024_01
    type: subject_of
    to: event_shelter_intake_adoption_gap_2023
    evidence: "Article's primary subject is the 2023 shelter overcrowding situation — intake outpacing adoption"
  - from: pub_npr_shelter_adoption_pace_2024_01
    type: subject_of
    to: concept_post_pandemic_adoption_decline
    evidence: "Article frames the gap as a post-pandemic phenomenon driven by return-to-office, rising costs, and rental restrictions"
  - from: pub_npr_shelter_adoption_pace_2024_01
    type: mentions
    to: org_shelter_animals_count
    evidence: "Article cites Shelter Animals Count as the data source on national shelter intake (~7,000 shelters tracked; intake up 10% from 2021)"
  - from: pub_npr_shelter_adoption_pace_2024_01
    type: mentions
    to: org_humane_rescue_alliance
    evidence: "Article reports from the Humane Rescue Alliance shelter in Washington, D.C."
  - from: pub_npr_shelter_adoption_pace_2024_01
    type: mentions
    to: person_stephanie_filer
    evidence: "Article quotes Stephanie Filer, executive director of Shelter Animals Count, on the 'perfect storm' of staffing, funding, and veterinarian shortages"
  - from: person_stephanie_filer
    type: affiliated_with
    to: org_shelter_animals_count
    evidence: "Article identifies Stephanie Filer as executive director of Shelter Animals Count"
  - from: person_julie_depenbrock
    type: affiliated_with
    to: org_npr
    evidence: "Article credited to NPR reporter Julie Depenbrock"
  - from: org_humane_rescue_alliance
    type: located_in
    to: loc_washington_dc
    evidence: "Article describes reporting from the Humane Rescue Alliance shelter in Washington, D.C."

tags: [community_journalism, shelter, adoption, post_pandemic, organization_diversity]
---

# Pet adoptions are not keeping pace with the number of animals coming in (NPR, 2024-01-10)

## Summary

This NPR Morning Edition story, reported by NPR's **Julie Depenbrock**, covers the 2023 shelter overcrowding situation in the United States: animal-shelter intake is outpacing adoption, leading to worsening conditions and rising euthanasia rates at many shelters.

Per the article, **Shelter Animals Count** — a nonprofit that aggregates intake and outcome data from approximately 7,000 animal shelters nationwide — reports that shelter intake is up roughly 10% from 2021. The article surfaces multiple compounding causes:

- **Post-pandemic return to work**, reducing the at-home time that drove pandemic-era pet acquisition.
- **Rising food and veterinary costs**, making pet ownership less affordable.
- **Pet restrictions at rental properties**, limiting where animals can be housed.
- **Renewed popularity of breeder-sourced "designer" pets**, drawing demand away from shelter adoption.
- **Shortages of shelter staffing, funding, and veterinarians** — described in the article as combining into a "perfect storm" by Stephanie Filer, executive director of Shelter Animals Count.

The article includes on-the-ground reporting from the **Humane Rescue Alliance** shelter in Washington, D.C.

## Cross-domain connections

This note is intentionally the **organization-diversity / entity-resolution stress** shape called out in the source manifest. A single article surfaces:

- A national data aggregator (`org_shelter_animals_count`)
- A local shelter (`org_humane_rescue_alliance`)
- A reporter affiliation (`person_julie_depenbrock → org_npr`)
- A spokesperson affiliation (`person_stephanie_filer → org_shelter_animals_count`)

That density of organization mentions in a single source is precisely what tests whether an ingestion pipeline correctly resolves slightly-varied surface forms (e.g. "Shelter Animals Count" vs "the nonprofit Shelter Animals Count") to one canonical entity, vs fragmenting them.

The note connects loosely to the `behavioral_research` domain via the implicit role of training and behavior in adoption-readiness, but does not introduce behavioral-research entities directly — that connection is left for a future cross-link if a behavioral-research note covering the same theme lands.

## Provenance and limitations

Article retrieved via WebSearch top-result match for the source URL. Direct WebFetch was not available in this authoring session. Specific numeric claims that appeared in WebSearch summaries (the "~7,000 shelters" figure and the "intake up 10% from 2021" figure) are reported here as quoted from the WebSearch result; both should be re-verified against the live NPR page (and ideally cross-checked against Shelter Animals Count's own published 2023 / 2024 reports at shelteranimalscount.org) before either number is treated as load-bearing for evaluation purposes. The "6.5M cats and dogs entered shelters in 2023" figure mentioned in the source manifest's `summary_hint` did not surface in this session's verification searches and is therefore deliberately omitted from this summary.

## Sources

- NPR article (canonical URL of record): https://www.npr.org/2024/01/10/1223890115/pet-adoptions-are-not-keeping-pace-with-the-number-of-animals-coming-in
- Shelter Animals Count summary of the same story: https://www.shelteranimalscount.org/pet-adoptions-are-not-keeping-pace-with-the-number-of-animals-coming-in/
