---
note_id: breed_ukc_american_pit_bull_terrier_standard
source_url: https://www.ukcdogs.com/docs/breeds/american-pit-bull-terrier.pdf
source_title: "American Pit Bull Terrier — Official UKC Breed Standard (Revised May 1, 2017)"
source_date: "2017-05-01"
source_publisher: "United Kennel Club"
license: fair_use_excerpt
license_note: "United Kennel Club holds copyright in its breed standards. Short excerpts are quoted under fair use for non-commercial research and evaluation; the full standard is not reproduced."
accessed_on: "2026-04-30"
domain: breed_standards
alias_pair_id: pit_bull

entities:
  - id: breed_american_pit_bull_terrier
    type: breed
    canonical: "American Pit Bull Terrier"
    aliases: ["APBT", "Pit Bull", "Pitbull"]
  - id: breed_apbt_abbreviation
    type: breed
    canonical: "APBT"
    notes: "Surface form: standard English-language abbreviation of American Pit Bull Terrier. Bound to canonical via alias_of."
  - id: breed_pit_bull_colloquial
    type: breed
    canonical: "Pit Bull"
    notes: "Surface form: the colloquial / informal name for the American Pit Bull Terrier. Distinct from the AKC-registered American Staffordshire Terrier despite frequent media conflation; that distinction is bound via the AmStaff note (see akc-american-staffordshire-terrier.md)."
  - id: org_ukc
    type: organization
    canonical: "United Kennel Club"
    is_regulatory: false
    notes: "Founded 1898. First registry to recognize the American Pit Bull Terrier."
  - id: pub_ukc_apbt_standard
    type: publication
    canonical: "American Pit Bull Terrier — Official UKC Breed Standard (Revised May 1, 2017)"
  - id: event_ukc_apbt_first_registration_1898
    type: event
    canonical: "UKC issues first registration for American Pit Bull Terrier (Bennett's Ring, registration #1)"
    timestamp: "1898-02-10"
    status: resolved

edges:
  - from: pub_ukc_apbt_standard
    type: authored_by
    to: org_ukc
    evidence: "Document title and publisher field name UKC as the issuer; PDF is hosted at ukcdogs.com under /docs/breeds/."
  - from: pub_ukc_apbt_standard
    type: mentions
    to: breed_american_pit_bull_terrier
    evidence: "Title: 'AMERICAN PIT BULL TERRIER Official UKC Breed Standard Revised May 1, 2017'. Canonical breed name appears throughout."
  - from: pub_ukc_apbt_standard
    type: subject_of
    to: event_ukc_apbt_first_registration_1898
    evidence: "Standard documents the breed UKC has registered since 1898. UKC founder C.Z. Bennett assigned UKC registration number 1 to his APBT 'Bennett's Ring' on February 10, 1898; reported across multiple breed-history sources verifying the UKC registry-origin date."
  - from: breed_apbt_abbreviation
    type: alias_of
    to: breed_american_pit_bull_terrier
    evidence: "APBT is the standard abbreviation of the canonical breed name. Registered in ontology.yaml#aliases.pit_bull."
  - from: breed_pit_bull_colloquial
    type: alias_of
    to: breed_american_pit_bull_terrier
    evidence: "Per ontology.yaml#aliases.pit_bull, the canonical UKC-registered name is 'American Pit Bull Terrier' and 'Pit Bull' is documented as its colloquial alias. The corpus also documents that 'Pit Bull' is frequently conflated in media with the distinct AKC-registered American Staffordshire Terrier — see akc-american-staffordshire-terrier.md for the conflation-test pair."
    needs_grounding: true
  - from: org_ukc
    type: regulates
    to: breed_american_pit_bull_terrier
    evidence: "UKC is the breed registry authority that recognized the American Pit Bull Terrier in 1898 and continues to publish and maintain the official APBT breed standard."

tags: [breed_standards, ukc, american_pit_bull_terrier, apbt, alias_chain, conflation_test_pair]
---

# UKC Official Breed Standard: American Pit Bull Terrier

## Summary

The United Kennel Club (UKC) publishes an official breed standard titled **"AMERICAN PIT BULL TERRIER — Official UKC Breed Standard (Revised May 1, 2017)."** UKC was the first registry to recognize this breed: founder **C. Z. Bennett** assigned UKC registration number 1 to his own American Pit Bull Terrier, "Bennett's Ring," on **February 10, 1898**, which is the registry-origin date for the breed.

Reported summary of the registry recognition:

> "The United Kennel Club was the first registry to recognize the American Pit Bull Terrier. ... On February 10, 1898, the breed was recognized by the United Kennel Club (UKC) named as American Pit Bull Terrier."

The UKC standard describes the breed as a medium-sized, solidly built, short-coated dog — a description carried forward across multiple revisions, most recently revised May 1, 2017.

## Documented aliases

UKC registers and publishes the canonical name **"American Pit Bull Terrier."** The standard abbreviation **"APBT"** is in widespread breeder, registry, and breed-fancier use; it is registered in this corpus's `ontology.yaml#aliases.pit_bull` and bound to the canonical breed via an `alias_of` edge here. The colloquial **"Pit Bull"** (with or without the space; "Pitbull" is a media spelling) is also bound as an alias of the canonical breed in the corpus's alias registry.

The colloquial "Pit Bull" surface form is the load-bearing alias-resolution case in this domain because it is frequently used in media to refer either to the UKC-registered American Pit Bull Terrier OR to the distinct AKC-registered American Staffordshire Terrier (see `akc-american-staffordshire-terrier.md`). The corpus treats this as the higher-value Cat 4 conflation test, separate from the trivial APBT abbreviation collapse.

## Why this exercises Cat 4 (alias resolution)

This note is the UKC-registry anchor for the alias chain `American Pit Bull Terrier ⟷ APBT ⟷ Pit Bull`. The deeper Cat 4 test — distinguishing the APBT from the American Staffordshire Terrier despite shared media labeling and shared historical ancestry — is bound by the companion AmStaff note. A memory system that collapses APBT and AmStaff onto one entity is silently merging two distinct registered breeds, which the corpus catches as a Cat 4 failure.

## Provenance and limitations

The UKC standard PDF was not directly fetched in this note's drafting session (WebFetch and a follow-up retry were both sandbox-denied for the ukcdogs.com URLs). Verification was via WebSearch, which returned the live PDF URL with the title "AMERICAN PIT BULL TERRIER Official UKC Breed Standard Revised May 1, 2017" and surfaced the 1898 / Bennett's Ring registration-origin facts in independently published breed-history results consistent with the UKC's own public statements. The "medium-sized, solidly built, short-coated" descriptor is paraphrased from multiple WebSearch result snippets; the verbatim wording of the current UKC standard text was not parsed by the drafter and is not directly quoted in this note. A future revision should re-fetch the PDF directly, parse the standard text, and replace any paraphrased description with verbatim quoted excerpts.

This is the same limitation pattern documented in `vault/veterinary_research/2018-07-fda-dcm-investigation.md`'s "Provenance and limitations" section: the source URL is the canonical record; downstream consumers who rely on exact wording should verify against the live source.

## Sources

- AMERICAN PIT BULL TERRIER Official UKC Breed Standard Revised May 1, 2017 (canonical URL of record): https://www.ukcdogs.com/docs/breeds/american-pit-bull-terrier.pdf
- Breed Standards : American Pit Bull Terrier | United Kennel Club (UKC) — registry landing page: https://www.ukcdogs.com/american-pit-bull-terrier
- American Pit Bull Terrier — Wikipedia (used here as orientation/cross-reference, not as a primary registry source): https://en.wikipedia.org/wiki/American_Pit_Bull_Terrier
- Corpus alias registry: `ontology.yaml#aliases.pit_bull`
- Companion conflation-test note: `vault/breed_standards/akc-american-staffordshire-terrier.md`
