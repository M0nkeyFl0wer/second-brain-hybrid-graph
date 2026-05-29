---
note_id: muni_montreal_bsl_2018_repeal
source_url: https://aldf.org/article/montreal-repeals-controversial-pit-bull-ban/
source_title: "Montreal Repeals Controversial Pit Bull Ban"
source_date: "2018"
source_publisher: "Animal Legal Defense Fund"
license: fair_use_excerpt
license_note: "ALDF article excerpted under fair-dealing for research and private study (Canadian Copyright Act s. 29) / fair use (17 U.S.C. § 107). Used for date and procedural attestation of the repeal event."
accessed_on: "2026-04-30"
domain: municipal_policy
jurisdiction: "Montreal, QC, Canada"
lifecycle_id: montreal_bsl_lifecycle

# Ontology-aligned entity declarations introduced by this note.
# org_city_of_montreal, loc_montreal_qc, concept_pit_bull, concept_bsl, and
# event_montreal_bsl_lifecycle are reused from
# vault/municipal_policy/montreal-bsl-2016-enactment.md so the temporal
# supersedes chain is queryable across both notes.
entities:
  - id: pub_montreal_2018_repeal_bylaw
    type: publication
    canonical: "Montreal replacement animal-control bylaw (2018, post-repeal of 16-060)"
  - id: event_montreal_bsl_repeal_2018
    type: event
    canonical: "Montreal city council adoption of replacement animal-control bylaw replacing 16-060"
    timestamp: "2018"
    status: resolved
  - id: concept_calgary_model
    type: concept
    canonical: "Calgary model (responsible-pet-ownership / behaviour-based dangerous-dog framework)"
    aliases: ["Calgary model", "responsible pet ownership model", "behaviour-based dangerous-dog framework"]
    notes: "Concept entity for the policy framework Montreal's incoming administration cited as the alternative to BSL. Calgary's instantiation of the model is documented in vault/municipal_policy/calgary-rpob-47m2021.md."

# Edges introduced by this note.
edges:
  # The supersedes edge — load-bearing for the Cat 6 temporal chain.
  - from: pub_montreal_2018_repeal_bylaw
    type: supersedes
    to: pub_montreal_2016_bsl_bylaw
    evidence: "ALDF: 'Montreal Repeals Controversial Pit Bull Ban' — the 2018 replacement bylaw, adopted under Mayor Valérie Plante and Projet Montréal, repealed the breed-targeting provisions of bylaw 16-060 and replaced them with a behaviour-based dangerous-dog framework. Per CBC News follow-up, restrictions now apply equally to all dogs regardless of breed."
  - from: pub_montreal_2018_repeal_bylaw
    type: subject_of
    to: event_montreal_bsl_repeal_2018
    evidence: "The 2018 replacement bylaw is the document adopted at the council session that repealed 16-060's breed-targeting provisions."
  - from: pub_montreal_2018_repeal_bylaw
    type: subject_of
    to: event_montreal_bsl_lifecycle
    evidence: "Same shared event entity as the 2016 enactment note — the repeal closes the lifecycle that the 2016 bylaw opened, making the chain queryable as a single event with two endpoints."
  - from: pub_montreal_2018_repeal_bylaw
    type: mentions
    to: concept_pit_bull
    evidence: "ALDF reports the 2018 replacement explicitly removes the pit-bull-specific provisions of 16-060."
  - from: pub_montreal_2018_repeal_bylaw
    type: mentions
    to: concept_calgary_model
    evidence: "CBC News follow-up coverage: Montreal's new administration suggested it would emulate the 'Calgary model,' which focuses on owner education as the key element to preventing dog attacks and ensuring public safety."
  - from: pub_montreal_2018_repeal_bylaw
    type: mentions
    to: concept_bsl
    evidence: "ALDF article frames the repeal as Montreal exiting breed-specific legislation in favour of a behaviour-based regime."
  - from: org_city_of_montreal
    type: regulates
    to: concept_pit_bull
    evidence: "Even after repeal of breed-specific provisions, the City of Montreal retains regulatory authority over all dogs (including pit-bull-type dogs) under the replacement framework's behaviour-based dangerous-dog provisions, which apply equally regardless of breed."
  - from: event_montreal_bsl_repeal_2018
    type: located_in
    to: loc_montreal_qc
    evidence: "Repeal vote occurred at Montreal city council."

tags: [municipal_policy, montreal, bsl_repeal, pit_bull, cat_6_temporal_chain, lifecycle_close, supersedes]
---

# Montreal pit-bull bylaw repealed and replaced (2018)

## Summary

In **2018**, under Mayor **Valérie Plante** and Projet Montréal, the City of Montreal repealed the breed-targeting provisions of Animal Control By-Law 16-060 and replaced them with a behaviour-based dangerous-dog framework. This note is the closing half of the Montreal BSL lifecycle that opens with `vault/municipal_policy/montreal-bsl-2016-enactment.md`. The two notes share the `event_montreal_bsl_lifecycle` event entity and the `pub_montreal_2018_repeal_bylaw` -[supersedes]-> `pub_montreal_2016_bsl_bylaw` edge declared here is the load-bearing edge for the corpus's Cat 6 temporal-supersession test.

## What the replacement bylaw does

Per ALDF and CBC News follow-up reporting, the 2018 replacement:

- **Removed** the breed-specific provisions of 16-060 (the special permit requirement for owners of "pit bull-type dogs," the muzzling and short-leash requirements applied by breed, and the prohibition on acquiring such dogs).
- **Retained and refactored** dangerous-dog restrictions to apply **equally to all dogs regardless of breed**, on the basis of individual animal behaviour.
- Established that a dog that bites or attacks a human in Montreal would be deemed **at risk** and would need to undergo evaluation by experts trained by the city. The dog's owner would need to alert authorities of the incident **within 72 hours**, keep the dog muzzled outdoors, and bring it in for an evaluation by specialized animal inspectors.

The Plante administration described the new approach as emulating the **"Calgary model"** — a behaviour-based responsible-pet-ownership framework focused on owner education and per-animal dangerous-dog determinations, documented in `vault/municipal_policy/calgary-rpob-47m2021.md`.

## Status

**Active / current state.** The repeal closes the supersedes chain from 16-060. Montreal's current animal-control framework continues to be the post-2018 behaviour-based regime; the citizen-facing summary at `montreal.ca/en/topics/obligations-and-responsibilities-pet-owners` (manifest id `muni_montreal_current_pet_owner_obligations`) attests the current state and is available to extend this note in a future v0.2 pass.

## Cross-references

- **Enactment half of the lifecycle:** `vault/municipal_policy/montreal-bsl-2016-enactment.md` — declares `pub_montreal_2016_bsl_bylaw` and `event_montreal_bsl_lifecycle`. This note's `supersedes` edge points back to that publication.
- **Calgary model reference:** `vault/municipal_policy/calgary-rpob-47m2021.md` — the canonical North American behaviour-based alternative the Plante administration cited.
- **Province-level BSL contrast:** `vault/municipal_policy/ontario-dola-statute.md` — same regulated concept (`concept_pit_bull`), opposite policy posture at a different level of government.

## Provenance and limitations

WebFetch against the ALDF URL was denied by the agent's sandbox. Content was retrieved via WebSearch summary of the same canonical URL set, the same retrieval method documented in `vault/veterinary_research/2018-07-fda-dcm-investigation.md` for the FDA source. The exact council-vote date for the 2018 replacement bylaw is not pinned to a single date in the search-engine summary; the source manifest at `sources/municipal_policy.yaml#muni_montreal_repeal_2018_aldf` records "August 2018," but the ALDF article itself should be re-fetched directly to verify. The frontmatter `source_url` is the canonical URL of record.

## Sources

- Animal Legal Defense Fund, "Montreal Repeals Controversial Pit Bull Ban" (2018): https://aldf.org/article/montreal-repeals-controversial-pit-bull-ban/
- CBC News, "Montreal ditches breed ban in favour of dangerous-dog restrictions" (2018) — redundant attestation: https://www.cbc.ca/news/canada/montreal/montreal-ditches-breed-ban-in-favour-of-dangerous-dog-restrictions-1.4704968
- Source manifest entry: `sources/municipal_policy.yaml#muni_montreal_repeal_2018_aldf`
