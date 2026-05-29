---
note_id: muni_montreal_bylaw_16_060_enactment
source_url: https://www.cbc.ca/news/canada/montreal/montreal-pit-bull-dangerous-dogs-animal-control-bylaw-1.3780335
source_title: "Montreal passes controversial pit bull ban"
source_date: "2016-09-27"
source_publisher: "CBC News"
license: fair_use_excerpt
license_note: "CBC News article cited for date-of-passage and bylaw-content attestation. Quoted text limited to short factual excerpts under fair-dealing for research and private study (Canadian Copyright Act s. 29)."
accessed_on: "2026-04-30"
domain: municipal_policy
jurisdiction: "Montreal, QC, Canada"
lifecycle_id: montreal_bsl_lifecycle

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: org_city_of_montreal
    type: organization
    canonical: "City of Montreal"
    is_regulatory: true
  - id: loc_montreal_qc
    type: location
    canonical: "Montreal, QC, Canada"
    jurisdiction_type: municipal
  - id: concept_pit_bull
    type: concept
    canonical: "Pit Bull"
    aliases: ["pit bull", "pit bull-type dog", "American Pit Bull Terrier", "APBT", "Pitbull"]
    notes: "Concept entity for the cross-domain regulatory category 'pit-bull-type dogs.' The breed-registry counterpart (American Pit Bull Terrier) is registered in ontology.yaml#aliases under pit_bull and may be introduced as a separate breed entity by breed_standards/* notes."
  - id: concept_bsl
    type: concept
    canonical: "Breed-specific legislation"
    aliases: ["BSL", "breed ban", "breed-specific law"]
  - id: event_montreal_bsl_lifecycle
    type: event
    canonical: "Montreal breed-specific-legislation lifecycle (2016 enactment through 2018 repeal)"
    timestamp: "2016-09-27"
    status: resolved
  - id: event_montreal_council_vote_16_060
    type: event
    canonical: "Montreal city council adoption of Animal Control By-Law 16-060"
    timestamp: "2016-09-27"
    status: resolved
  - id: pub_montreal_2016_bsl_bylaw
    type: publication
    canonical: "Montreal By-Law Concerning Animal Control 16-060 (2016)"

# Edges introduced by this note.
edges:
  - from: pub_montreal_2016_bsl_bylaw
    type: subject_of
    to: event_montreal_council_vote_16_060
    evidence: "Bylaw 16-060 is the document adopted at the Montreal city council session on 2016-09-27 reported by CBC; the publication is the canonical text whose passage is the event."
  - from: pub_montreal_2016_bsl_bylaw
    type: subject_of
    to: event_montreal_bsl_lifecycle
    evidence: "Bylaw 16-060 is the originating instrument of the Montreal BSL lifecycle that closes with its 2018 repeal (see vault/municipal_policy/montreal-bsl-2018-repeal.md)."
  - from: pub_montreal_2016_bsl_bylaw
    type: mentions
    to: concept_pit_bull
    evidence: "Bylaw 16-060 defines and restricts ownership of 'pit bull-type dogs' (American pit bull terrier, American Staffordshire terrier, Staffordshire bull terrier, and crossbreeds with several morphological traits of those breeds)."
  - from: pub_montreal_2016_bsl_bylaw
    type: mentions
    to: concept_bsl
    evidence: "The bylaw is the worked example of municipal-level breed-specific legislation in Canadian municipal-policy literature; news coverage names it as such."
  - from: org_city_of_montreal
    type: regulates
    to: concept_pit_bull
    evidence: "Bylaw 16-060 establishes Montreal's regulatory authority over pit-bull-type dogs within the city limits; CBC reports the bylaw applies 'across all 19 Montreal boroughs.'"
  - from: org_city_of_montreal
    type: located_in
    to: loc_montreal_qc
    evidence: "City of Montreal is the municipal government of Montreal, QC."
  - from: event_montreal_council_vote_16_060
    type: located_in
    to: loc_montreal_qc
    evidence: "The council vote took place at Montreal city hall (CBC News, 2016-09-27)."

tags: [municipal_policy, montreal, bsl, pit_bull, cat_6_temporal_chain, lifecycle_origin]
---

# Montreal By-Law 16-060 — pit-bull restrictions enacted (2016-09-27)

## Summary

On **2016-09-27**, the city council of Montreal, under Mayor Denis Coderre, adopted Animal Control By-Law **16-060**, restricting ownership of "pit bull-type dogs" within the city. The new rules went into effect across all 19 Montreal boroughs starting **2016-10-03**. The bylaw is the originating instrument of the Montreal BSL lifecycle that closes with the Plante administration's 2018 repeal — see `vault/municipal_policy/montreal-bsl-2018-repeal.md` for the second half of the chain.

## What the bylaw does

Per CBC News reporting on the day of passage, By-Law 16-060:

- Made it illegal to **adopt or otherwise acquire** any dog identified as a "pit bull-type dog" within Montreal city limits.
- Defined "pit bull-type dog" as: a dog of the **American pit bull terrier, American Staffordshire terrier, or Staffordshire bull terrier** breed; a dog born of a crossbreeding between one of those breeds and another dog; or a dog showing several morphological traits of the listed breeds and crossbreedings.
- Required existing owners (residents of Montreal who already owned such a dog) to **acquire a special permit** to keep their pet.
- Required any grandfathered pit bulls to be **muzzled when in public** and kept on a **leash no longer than four feet**.
- Created two categories of dogs of all breeds — **at-risk** (exhibits aggressive behaviour, e.g. has bitten someone) and **dangerous** (has killed someone or is deemed dangerous by an expert).

## Status

**Resolved / superseded.** Bylaw 16-060 was suspended in late 2017 following the change of administration after the November 2017 municipal election, and its breed-targeting provisions were repealed and replaced under Mayor Valérie Plante in 2018. The supersession is bound on the repeal-side note (`montreal-bsl-2018-repeal.md`) via a `supersedes` edge from the 2018 replacement bylaw to this 2016 bylaw, and both notes share the `event_montreal_bsl_lifecycle` event id so the temporal chain is queryable.

## Cross-references

- **Repeal half of the lifecycle:** `vault/municipal_policy/montreal-bsl-2018-repeal.md`
- **Behaviour-based alternative model:** `vault/municipal_policy/calgary-rpob-47m2021.md` — the "Calgary model" the Plante administration cited as the framework it would emulate when replacing 16-060.
- **Province-level BSL counterpart in Canada:** `vault/municipal_policy/ontario-dola-statute.md` — Ontario's province-wide pit-bull restrictions remain in force, providing the cross-jurisdiction comparison anchor (province-level BSL still active vs. municipal-level BSL repealed).

## Provenance and limitations

The summary author did not directly access the source page at the time of writing — `WebFetch` against the CBC URL was denied by the agent's sandbox. Content was retrieved via `WebSearch` summary of the same canonical URL set, the same retrieval method documented in `vault/veterinary_research/2018-07-fda-dcm-investigation.md` for the FDA source. The frontmatter `source_url` is the canonical URL of record; verification against that URL is the responsibility of any downstream consumer who relies on exact quoted wording. A future revision of this note should re-fetch the CBC article and verify each factual claim against the live page text. A primary-source PDF of bylaw 16-060 from Montreal's municipal archive should be added in v0.2 if accessible.

## Sources

- CBC News, "Montreal passes controversial pit bull ban" (2016-09-27): https://www.cbc.ca/news/canada/montreal/montreal-pit-bull-dangerous-dogs-animal-control-bylaw-1.3780335
- Source manifest entry: `sources/municipal_policy.yaml#muni_montreal_bylaw_16_060_summary`
