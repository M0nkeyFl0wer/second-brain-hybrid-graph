---
note_id: breed_akc_american_staffordshire_terrier_standard
source_url: https://images.akc.org/pdf/breeds/standards/AmericanStaffordshireTerrier.pdf
source_title: "Official Standard of the American Staffordshire Terrier"
source_date: "1936-06-10"
source_publisher: "American Kennel Club"
license: fair_use_excerpt
license_note: "AKC holds copyright in the breed standard text. Short excerpts are quoted under fair use for non-commercial research and evaluation; the full standard is not reproduced."
accessed_on: "2026-04-30"
domain: breed_standards
alias_pair_id: pit_bull

entities:
  - id: breed_american_staffordshire_terrier
    type: breed
    canonical: "American Staffordshire Terrier"
    aliases: ["AmStaff"]
    notes: "Distinct AKC-registered breed, frequently conflated in media with the UKC-registered American Pit Bull Terrier. The two are separately registered breeds with separate official standards."
  - id: breed_amstaff_abbreviation
    type: breed
    canonical: "AmStaff"
    notes: "Surface form: standard breeder/handler abbreviation of American Staffordshire Terrier. Bound to canonical via alias_of."
  - id: pub_akc_amstaff_standard
    type: publication
    canonical: "Official Standard of the American Staffordshire Terrier (AKC)"
  - id: event_akc_amstaff_recognized_1936
    type: event
    canonical: "AKC recognizes Staffordshire Terrier as a distinct registered breed"
    timestamp: "1936-06-10"
    status: resolved

edges:
  - from: pub_akc_amstaff_standard
    type: authored_by
    to: org_akc
    evidence: "Document is published by the American Kennel Club; AKC logo appears on the standard PDF."
  - from: pub_akc_amstaff_standard
    type: mentions
    to: breed_american_staffordshire_terrier
    evidence: "Title: 'Official Standard of the American Staffordshire Terrier'. Canonical breed name appears throughout the standard text."
  - from: pub_akc_amstaff_standard
    type: subject_of
    to: event_akc_amstaff_recognized_1936
    evidence: "Standard's footer reads: 'Approved June 10, 1936'. Per AKC's own breed history coverage, on this date approximately 50 dogs from the UKC American Pit Bull Terrier stud book were entered into the AKC stud book under the new name 'Staffordshire Terrier'; the word 'American' was added to the name in 1972."
  - from: breed_amstaff_abbreviation
    type: alias_of
    to: breed_american_staffordshire_terrier
    evidence: "AmStaff is the conventional abbreviation for American Staffordshire Terrier in breeder and registry usage."
    needs_grounding: true
  - from: org_akc
    type: regulates
    to: breed_american_staffordshire_terrier
    evidence: "AKC is the breed registry authority that recognized the American Staffordshire Terrier in 1936 and publishes its official standard."

tags: [breed_standards, akc, american_staffordshire_terrier, amstaff, conflation_test_pair, alias_chain]
---

# AKC Official Standard of the American Staffordshire Terrier

## Summary

The American Kennel Club (AKC) publishes an official breed standard titled **"Official Standard of the American Staffordshire Terrier."** The standard was **approved June 10, 1936** (per the document's own footer).

The standard's opening framing:

> "The American Staffordshire Terrier should give the impression of great strength for his size, a well put-together dog, muscular, but agile and graceful, keenly alive to his surroundings. He should be stocky, not long-legged or racy in outline. His courage is proverbial."

The breed was originally registered by AKC in 1936 simply as "Staffordshire Terrier"; the word **"American"** was added to the official name in **1972** to distinguish it more clearly from the Staffordshire Bull Terrier, which the AKC recognized as a separate breed in 1974.

## Documented aliases

The AKC standard establishes **"American Staffordshire Terrier"** as the registered canonical name. The breeder/handler abbreviation **"AmStaff"** is in widespread use and is bound to the canonical entity here via an `alias_of` edge. The standard text itself does not introduce additional aliases.

Importantly, **the AKC American Staffordshire Terrier and the UKC American Pit Bull Terrier are two separately registered breeds**, not aliases of one another. Per AKC's own published breed-history coverage:

> "When owners of these dogs sought AKC registration in the 1930s, the AKC would not register a breed with the word 'pit' in its name. The compromise was a new designation: the Staffordshire Terrier, after the English county most associated with bull-and-terrier breeding."

> "The breed selection was based entirely on conformation and established breed standards that for decades have transformed the American Staffordshire Terrier into a much different breed from the American Pit Bull Terrier."

The shared ancestry (the original 1936 AKC stud-book entries came from the UKC APBT registry) is the historical reason for the persistent media conflation; the divergent breeding programs since 1936 are the reason the two are now distinct registered breeds.

## Why this exercises Cat 4 (alias resolution)

This note is the **conflation-test pair** that the corpus's `ontology.yaml#aliases.pit_bull` notes block flags explicitly:

> "Distinct from American Staffordshire Terrier despite frequent conflation in media. The conflation itself is a Cat 4 test: a system that collapses APBT and AmStaff is silently merging two registered breeds."

A correctly behaving memory system, when ingesting both this note and `ukc-american-pit-bull-terrier.md`, must build TWO distinct `breed`-typed entities (`breed_american_pit_bull_terrier` and `breed_american_staffordshire_terrier`) rather than collapsing them into one. The colloquial "Pit Bull" surface form binds (via `alias_of`) only to the UKC APBT canonical entity in this corpus's ontology — not to the AmStaff. The AmStaff has its own registry name and its own AKC-registered identity.

A system that fails this test by merging APBT and AmStaff is making the same kind of silent-merge error described for the GSD/Alsatian case, except that here the correct behavior is the opposite — keep them separate, not collapse them.

## Provenance and limitations

The AKC American Staffordshire Terrier standard PDF was retrieved successfully and its full text was parsed in this note's drafting session (AmericanStaffordshireTerrier.pdf, 174 KB, single page, "Approved June 10, 1936" footer verified). Quoted excerpts from the standard above are taken directly from the parsed PDF text.

The 1936 stud-book history (50 UKC APBT-registry dogs entering the AKC stud book under the new "Staffordshire Terrier" name) and the 1972 name change to add "American" are not in the standard PDF itself; they are sourced from AKC's published breed-history coverage on akc.org, which was retrieved via WebSearch in this drafting session. A future revision of this note should re-verify these dates against the AKC breed-history article URL directly.

## Sources

- Official Standard of the American Staffordshire Terrier — American Kennel Club (canonical URL of record): https://images.akc.org/pdf/breeds/standards/AmericanStaffordshireTerrier.pdf
- American Staffordshire Terrier History: How the AmStaff Separated From the "Pit Bull" — American Kennel Club: https://www.akc.org/expert-advice/dog-breeds/american-staffordshire-terrier-history-amstaff/
- American Staffordshire Terrier Dog Breed Information — American Kennel Club: https://www.akc.org/dog-breeds/american-staffordshire-terrier/
- Corpus alias registry: `ontology.yaml#aliases.pit_bull` (AmStaff distinction documented in the notes block)
- Companion APBT registry note: `vault/breed_standards/ukc-american-pit-bull-terrier.md`
