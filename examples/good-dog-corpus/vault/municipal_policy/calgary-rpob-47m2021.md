---
note_id: muni_calgary_rpob_47m2021
source_url: https://www.calgary.ca/content/dam/www/cs/documents/47m2021-responsible-pet-ownership-bylaw.pdf
source_title: "Responsible Pet Ownership Bylaw 47M2021"
source_date: "2021"
source_publisher: "City of Calgary"
license: open_government_license_calgary
license_note: "Calgary publishes bylaws on calgary.ca for public access; bylaw text is reproducible with attribution under the city's open-data terms."
accessed_on: "2026-04-30"
domain: municipal_policy
jurisdiction: "Calgary, AB, Canada"

# Ontology-aligned entity declarations introduced by this note.
# concept_pit_bull and concept_calgary_model are reused from the Montreal
# repeal note to bind cross-jurisdiction queries.
entities:
  - id: org_city_of_calgary
    type: organization
    canonical: "City of Calgary"
    is_regulatory: true
  - id: loc_calgary_ab
    type: location
    canonical: "Calgary, AB, Canada"
    jurisdiction_type: municipal
  - id: pub_calgary_rpob_47m2021
    type: publication
    canonical: "City of Calgary Responsible Pet Ownership Bylaw 47M2021"
  - id: pub_calgary_rpob_23m2006
    type: publication
    canonical: "City of Calgary Responsible Pet Ownership Bylaw 23M2006 (predecessor, 2006)"
  - id: event_calgary_rpob_in_force_2022
    type: event
    canonical: "Calgary Responsible Pet Ownership Bylaw 47M2021 takes effect"
    timestamp: "2022-01-01"
    status: resolved

# Edges introduced by this note.
edges:
  # The 47M2021 -> 23M2006 supersedes is a continuity supersession (same
  # regime, updated form), distinct in nature from the Montreal 2018->2016
  # supersession (policy reversal). Both are valid Cat 6 chain instances.
  - from: pub_calgary_rpob_47m2021
    type: supersedes
    to: pub_calgary_rpob_23m2006
    evidence: "Calgary newsroom and ACLRC reporting confirm 47M2021 replaces the previous Responsible Pet Ownership Bylaw 23M2006 (2006), updating it for the first time in over a decade. The replacement is a continuity update, not a policy reversal: both bylaws instantiate the behaviour-based 'Calgary model.'"
  - from: pub_calgary_rpob_47m2021
    type: subject_of
    to: event_calgary_rpob_in_force_2022
    evidence: "47M2021 takes effect 2022-01-01 per City of Calgary newsroom announcement and the bylaw's own commencement provision."
  - from: pub_calgary_rpob_47m2021
    type: mentions
    to: concept_calgary_model
    evidence: "47M2021 is the current statutory instantiation of the responsible-pet-ownership framework that municipal-policy literature names the 'Calgary model.' The Montreal 2018 repeal note (vault/municipal_policy/montreal-bsl-2018-repeal.md) cites this same framework as the alternative Montreal would emulate when replacing 16-060."
  - from: pub_calgary_rpob_47m2021
    type: mentions
    to: concept_pit_bull
    evidence: "47M2021 governs all dogs without breed-specific bans; pit-bull-type dogs are within scope as ordinary regulated dogs subject to the same licensing and behaviour-based vicious-animal provisions as any other breed. Cross-jurisdiction relevance is precisely the absence of breed-specific provisions."
  - from: org_city_of_calgary
    type: regulates
    to: concept_calgary_model
    evidence: "The City of Calgary is the regulatory authority that codifies and enforces the responsible-pet-ownership framework via 47M2021 and its predecessor 23M2006."
  - from: org_city_of_calgary
    type: regulates
    to: concept_pit_bull
    evidence: "47M2021 establishes Calgary's regulatory authority over all dogs in the city, including pit-bull-type dogs, without breed-specific restrictions."
  - from: org_city_of_calgary
    type: located_in
    to: loc_calgary_ab
    evidence: "City of Calgary is the municipal government of Calgary, AB."
  - from: event_calgary_rpob_in_force_2022
    type: located_in
    to: loc_calgary_ab
    evidence: "Bylaw 47M2021 is in force in the City of Calgary."

tags: [municipal_policy, calgary, calgary_model, responsible_pet_ownership, behaviour_based, cross_jurisdiction_anchor, no_bsl]
---

# Calgary Responsible Pet Ownership Bylaw 47M2021

## Summary

**Bylaw 47M2021**, the City of Calgary's Responsible Pet Ownership Bylaw, took effect **2022-01-01** and replaced the **23M2006** Responsible Pet Ownership Bylaw that had governed pet ownership in Calgary for over a decade. Both bylaws instantiate the behaviour-based regulatory framework that municipal-policy literature names the **"Calgary model"**: licensing, owner-responsibility provisions, and per-animal dangerous-dog determinations, **without breed-specific bans**. This is the canonical North American counter-example to BSL — the framework the Plante administration in Montreal cited as the alternative it would emulate when repealing 16-060 (see `vault/municipal_policy/montreal-bsl-2018-repeal.md`).

## What the bylaw does

Per the City of Calgary newsroom announcement and Alberta Civil Liberties Research Centre (ACLRC) summary:

- **Licensing.** Mandatory licensing of cats and dogs is the foundational requirement of the regime; the new bylaw also expands licensing to cover an urban hen program and bee-keeping regulation.
- **Pet ownership limits.** Households are limited to **six dogs and six cats**, and an individual may bring no more than six dogs to an off-leash area at one time.
- **Vicious animal designations.** The Chief Bylaw Officer may designate an animal as **vicious** when there are reasonable grounds to believe the animal poses a risk to the health and safety of Calgarians. The Officer can also allow such an animal to return home faster, with conditions that ensure public safety.
- **Appeals.** Appeals of decisions under 47M2021 must be heard by a panel of the Licence and Community Standards Appeal Board (LCSAB) that includes at least one veterinarian and one certified professional dog trainer.
- **No breed-specific bans.** Dangerous-dog determinations are made per-animal on behavioural grounds; the bylaw does not prohibit, license-restrict, or otherwise differentiate dogs by breed.

## Status

**Active.** In force since 2022-01-01. Predecessor bylaw 23M2006 is superseded but is referenced here as a `publication` entity to support the secondary Cat 6 chain (`23M2006 -> 47M2021`), which is a *continuity supersession* — same policy posture, updated statutory form — distinct in nature from the Montreal 2016 → 2018 supersession, which is a *policy reversal*.

## Cross-jurisdiction comparison

This note anchors the cross-jurisdiction comparison required by the corpus's Cat 2c multi-hop scenarios. Three jurisdictions in the corpus, three different policy postures over `concept_pit_bull`:

- **Calgary, AB** (this note): behaviour-based, no breed-specific provisions. `org_city_of_calgary` -[regulates]-> `concept_pit_bull` via `pub_calgary_rpob_47m2021`.
- **Ontario** (`vault/municipal_policy/ontario-dola-statute.md`): province-wide breed-specific prohibition under DOLA, in force since 2005-08-29.
- **Montreal, QC** (`vault/municipal_policy/montreal-bsl-2016-enactment.md` and `montreal-bsl-2018-repeal.md`): municipal-level BSL enacted 2016, repealed 2018, current regime is behaviour-based. The Plante administration explicitly cited the Calgary model as the framework it would emulate.

## Provenance and limitations

WebFetch against the calgary.ca PDF was denied by the agent's sandbox; PDF parsing through that tool would in any case have been brittle. Content was retrieved via WebSearch summary, the same retrieval method documented in `vault/veterinary_research/2018-07-fda-dcm-investigation.md`. Specific section numbers within 47M2021 (e.g., the section that codifies the six-dog household limit) are not pinned in this note's frontmatter; a future revision should add them by reading the PDF directly.

## Sources

- City of Calgary, Responsible Pet Ownership Bylaw 47M2021 (PDF): https://www.calgary.ca/content/dam/www/cs/documents/47m2021-responsible-pet-ownership-bylaw.pdf
- City of Calgary newsroom, "Responsible Pet Ownership Bylaw Update passed by Calgary City Council": https://newsroom.calgary.ca/responsible-pet-ownership-bylaw-update-passed-by-calgary-city-council/
- Alberta Civil Liberties Research Centre, "Calgary's Responsible Pet Ownership Bylaw | Key Changes Explained" (2021-08-09): https://www.aclrc.com/blog/2021-8-9-calgarys-responsible-pet-ownership-bylaw-1/
- Source manifest entry: `sources/municipal_policy.yaml#muni_calgary_rpob_47m2021`
