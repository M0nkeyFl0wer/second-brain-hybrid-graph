---
note_id: muni_on_dola_statute
source_url: https://www.ontario.ca/laws/statute/90d16
source_title: "Dog Owners' Liability Act, R.S.O. 1990, c. D.16"
source_date: "1990"
source_publisher: "Government of Ontario (e-Laws)"
license: open_government_license_canada
license_note: "Ontario statutes published on e-Laws are Crown copyright but reproducible under the Queen's Printer for Ontario / Open Government Licence — Ontario for non-commercial reuse with attribution. Excerpting bylaw text in an evaluation corpus is within scope."
accessed_on: "2026-04-30"
domain: municipal_policy
jurisdiction: "Ontario, Canada"

# Ontology-aligned entity declarations introduced by this note.
# concept_pit_bull and concept_bsl are reused from the Montreal notes so
# cross-jurisdiction queries traverse a single shared concept entity.
entities:
  - id: org_government_of_ontario
    type: organization
    canonical: "Government of Ontario"
    is_regulatory: true
  - id: loc_ontario_ca
    type: location
    canonical: "Ontario, Canada"
    jurisdiction_type: regional
  - id: pub_ontario_dola_statute
    type: publication
    canonical: "Dog Owners' Liability Act, R.S.O. 1990, c. D.16 (Ontario)"
  - id: pub_ontario_bill_132_2005
    type: publication
    canonical: "Public Safety Related to Dogs Statute Law Amendment Act, 2005 (Ontario Bill 132)"
  - id: event_ontario_pit_bull_ban_in_force
    type: event
    canonical: "Ontario pit-bull restrictions take effect under DOLA as amended by Bill 132"
    timestamp: "2005-08-29"
    status: active
  - id: event_ontario_bill_132_royal_assent
    type: event
    canonical: "Bill 132 receives Royal Assent (Ontario)"
    timestamp: "2005-03-09"
    status: resolved

# Edges introduced by this note.
edges:
  - from: pub_ontario_bill_132_2005
    type: supersedes
    to: pub_ontario_dola_statute
    evidence: "Bill 132 (Public Safety Related to Dogs Statute Law Amendment Act, 2005) substantively amended the 1990 DOLA to add the pit-bull restriction provisions; amended sections supersede the prior un-amended text. Per the Legislative Assembly of Ontario record, the bill received Royal Assent 2005-03-09 and the pit-bull restrictions came into force 2005-08-29."
  - from: pub_ontario_bill_132_2005
    type: subject_of
    to: event_ontario_bill_132_royal_assent
    evidence: "Bill 132 is the document whose adoption is the Royal Assent event of 2005-03-09."
  - from: pub_ontario_dola_statute
    type: subject_of
    to: event_ontario_pit_bull_ban_in_force
    evidence: "DOLA as amended by Bill 132 is the statute whose pit-bull provisions came into force on 2005-08-29."
  - from: pub_ontario_dola_statute
    type: mentions
    to: concept_pit_bull
    evidence: "DOLA's Bill 132 amendments define 'pit bull' for the purposes of the statute and prohibit owning, breeding, transferring, abandoning, or importing pit bulls in Ontario, subject to the grandfather clause."
  - from: pub_ontario_dola_statute
    type: mentions
    to: concept_bsl
    evidence: "DOLA's pit-bull provisions are the canonical Canadian example of breed-specific legislation at the provincial level; BSL literature consistently names DOLA as the province-level Canadian instance."
  - from: pub_ontario_bill_132_2005
    type: mentions
    to: concept_pit_bull
    evidence: "Bill 132 is the statute-amendment instrument that introduced the 'pit bull' definition and the prohibition into Ontario law."
  - from: org_government_of_ontario
    type: regulates
    to: concept_pit_bull
    evidence: "DOLA establishes provincial regulatory authority over pit-bull-type dogs across Ontario; the Government of Ontario is the regulator."
  - from: org_government_of_ontario
    type: regulates
    to: concept_bsl
    evidence: "Bill 132 is the legislative instrument by which Ontario chose breed-specific legislation as its regulatory posture; the Government of Ontario regulates the BSL framework directly at the provincial level (in contrast to municipal-level BSL such as Montreal 16-060)."
  - from: org_government_of_ontario
    type: located_in
    to: loc_ontario_ca
    evidence: "The Government of Ontario is the provincial government of Ontario."
  - from: event_ontario_pit_bull_ban_in_force
    type: located_in
    to: loc_ontario_ca
    evidence: "The pit-bull restrictions are in force province-wide in Ontario."

tags: [municipal_policy, ontario, dola, bsl, pit_bull, cross_jurisdiction_anchor, province_level]
---

# Ontario Dog Owners' Liability Act (DOLA) — pit-bull restrictions

## Summary

The **Dog Owners' Liability Act, R.S.O. 1990, c. D.16 (DOLA)** is Ontario's province-wide statute governing dog-owner liability and dangerous dogs. It is the canonical Canadian example of **breed-specific legislation at the provincial level**. The pit-bull restrictions were added by **Bill 132** (the *Public Safety Related to Dogs Statute Law Amendment Act, 2005*), which received Royal Assent on **2005-03-09**, with the pit-bull provisions coming into force on **2005-08-29**.

## What the statute does

Per the Legislative Assembly of Ontario record and the (former) Ontario Ministry of the Attorney General DOLA summary:

- **Prohibition.** As amended by Bill 132, DOLA prohibits owning, breeding, transferring, abandoning, or importing **pit bulls** in Ontario, subject to a grandfather clause for dogs already in Ontario when the law came into force.
- **Grandfather clause.** A pit bull qualifies as grandfathered ("restricted pit bull") if it was owned by a resident of Ontario on **2005-08-29** (the day the amendment came into force), or born in Ontario before the end of the 90-day period beginning on that date.
- **Compliance window.** Owners of pit bulls existing on 2005-08-29 had until **2005-10-28** to ensure their dogs were spayed or neutered, and were muzzled and leashed while in public.
- **Replacement of grandfathered dogs.** A person who owned one or more pit bulls on 2005-08-29 may acquire additional restricted pit bulls so long as the effect would not be to leave the person with more pit bulls than they owned on 2005-08-29 (i.e., replacement, not increase).
- **Implementing regulation.** Ontario Regulation 157/05 (manifest id `muni_on_dola_regulation_157_05`) prescribes the operational conditions — muzzling, leashing, sterilization, licensing — for restricted pit bulls.

## Status

**Active.** Ontario's pit-bull restrictions remain in force province-wide as of the corpus accessed_on date (2026-04-30). Repeated repeal attempts have not succeeded; the Supreme Court of Canada declined to hear a constitutional challenge to the law. Within the corpus, this provincial-level statute remaining in force while a municipal-level instance (Montreal 16-060) was repealed is precisely the cross-jurisdiction signal Cat 2c is meant to surface.

## Cross-jurisdiction comparison

Three jurisdictions in the corpus, three different policy postures over the same regulated concept (`concept_pit_bull`), all bound to the same shared concept entity so the cross-jurisdiction query is a single graph traversal rather than a string-match exercise:

- **Ontario** (this note): province-wide BSL via DOLA + Bill 132, active since 2005-08-29.
- **Montreal, QC** (`vault/municipal_policy/montreal-bsl-2016-enactment.md` + `montreal-bsl-2018-repeal.md`): municipal-level BSL, enacted 2016, repealed 2018; current regime is behaviour-based.
- **Calgary, AB** (`vault/municipal_policy/calgary-rpob-47m2021.md`): no BSL; behaviour-based "Calgary model" since 2006 (23M2006), updated as 47M2021 in 2022.

The Toronto Municipal Code Chapter 349 source in the manifest (`muni_toronto_chapter_349`) is the city-level enforcement layer that operationalizes DOLA within Toronto, available to extend the multi-hop chain `pub_ontario_dola_statute -> Toronto Chapter 349 -> animal-services enforcement` in a future v0.2 pass.

## Provenance and limitations

WebFetch against the e-Laws statute URL was permitted but returned essentially empty content (only an "e-Laws | Ontario.ca" header) — the e-Laws portal appears to render statute text via client-side JavaScript that the fetcher does not execute. Content was therefore retrieved via WebSearch summary of the same canonical URL set together with the Legislative Assembly of Ontario's Bill 132 record and the (archived) Ministry of the Attorney General DOLA summary, the same retrieval method documented in `vault/veterinary_research/2018-07-fda-dcm-investigation.md` for the FDA source. The frontmatter `source_url` is the canonical e-Laws URL of record. A future revision should re-fetch the statute through a JavaScript-capable client (or pull the consolidated statute from Ontario's Open Data publishing) and pin specific section numbers (e.g., the s.1 definition of "pit bull" and the s.6 prohibition) directly from the live text.

## Sources

- Government of Ontario, Dog Owners' Liability Act, R.S.O. 1990, c. D.16 (canonical e-Laws URL): https://www.ontario.ca/laws/statute/90d16
- Legislative Assembly of Ontario, Bill 132 — Public Safety Related to Dogs Statute Law Amendment Act, 2005: https://www.ola.org/en/legislative-business/bills/parliament-38/session-1/bill-132
- Ministry of the Attorney General, "Information on The Dog Owners' Liability Act and Public Safety Related to Dogs Statute Law Amendment Act, 2005" (archived): https://wayback.archive-it.org/16312/20210402033009/http://www.attorneygeneral.jus.gov.on.ca/english/about/pubs/dola-pubsfty/dola-pubsfty.php
- Ontario Regulation 157/05 (implementing regulation): https://www.ontario.ca/laws/regulation/050157
- Source manifest entries: `sources/municipal_policy.yaml#muni_on_dola_statute` and `#muni_on_dola_regulation_157_05`
