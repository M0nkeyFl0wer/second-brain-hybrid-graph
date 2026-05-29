---
note_id: breed_akc_german_shepherd_dog_standard
source_url: https://images.akc.org/pdf/breeds/standards/GermanShepherdDog.pdf
source_title: "Official Standard of the German Shepherd Dog"
source_date: "1978-02-11"
source_publisher: "American Kennel Club"
license: fair_use_excerpt
license_note: "AKC holds copyright in the breed standard text. Short excerpts are quoted in this note under fair use for non-commercial research and evaluation; the full standard is not reproduced. Source attribution per note frontmatter."
accessed_on: "2026-04-30"
domain: breed_standards
alias_pair_id: german_shepherd

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: breed_german_shepherd_dog
    type: breed
    canonical: "German Shepherd Dog"
    aliases: ["GSD", "German Shepherd", "Alsatian"]
  - id: breed_gsd_abbreviation
    type: breed
    canonical: "GSD"
    notes: "Surface form: the colloquial abbreviation. Bound to canonical breed_german_shepherd_dog via alias_of."
  - id: org_akc
    type: organization
    canonical: "American Kennel Club"
    is_regulatory: false
    notes: "Breed registry authority for the United States. Not regulatory in the FDA sense; holds private-association registry authority."
  - id: pub_akc_gsd_standard
    type: publication
    canonical: "Official Standard of the German Shepherd Dog (AKC)"

edges:
  - from: pub_akc_gsd_standard
    type: authored_by
    to: org_akc
    evidence: "Document is published by the American Kennel Club; AKC logo and 'AMERICAN KENNEL CLUB' appear on each page of the standard PDF."
  - from: pub_akc_gsd_standard
    type: mentions
    to: breed_german_shepherd_dog
    evidence: "Title: 'Official Standard of the German Shepherd Dog'. Canonical name 'German Shepherd Dog' appears throughout the standard text (e.g., 'A German Shepherd Dog is a trotting dog')."
  - from: breed_gsd_abbreviation
    type: alias_of
    to: breed_german_shepherd_dog
    evidence: "GSD is the conventional English abbreviation for German Shepherd Dog as registered by AKC. Registered in ontology.yaml#aliases.german_shepherd."
    needs_grounding: true
  - from: org_akc
    type: regulates
    to: breed_german_shepherd_dog
    evidence: "AKC is the breed registry authority that issues and maintains the official standard for the German Shepherd Dog in the United States."

tags: [breed_standards, akc, german_shepherd, gsd, alias_chain]
---

# AKC Official Standard of the German Shepherd Dog

## Summary

The American Kennel Club (AKC) publishes an official breed standard titled **"Official Standard of the German Shepherd Dog."** Throughout the three-page standard the breed is named consistently as the "German Shepherd Dog." The standard was **approved February 11, 1978** and **reformatted July 11, 1994**.

The opening sentence establishes the canonical name in use:

> "The first impression of a good German Shepherd Dog is that of a strong, agile, well muscled animal, alert and full of life."

Later sections continue with the same canonical form, e.g.:

> "A German Shepherd Dog is a trotting dog, and its structure has been developed to meet the requirements of its work."

The AKC standard establishes "German Shepherd Dog" as the registered breed name on the U.S. side. The AKC document does **not** itself use the abbreviation "GSD" or the historical UK name "Alsatian"; those alias surfaces are documented separately (the "GSD" abbreviation is in widespread AKC and breeder usage outside the standard text; the "Alsatian" naming history is bound by the UK Royal Kennel Club source, see `royal-kennel-club-german-shepherd-dog.md`).

## Documented aliases / canonical name

The AKC standard documents the canonical full form: **"German Shepherd Dog."** The shorter form "German Shepherd" is in common AKC promotional usage but is not present as an alternative title in the standard text itself. The "GSD" abbreviation is registered in this corpus's `ontology.yaml#aliases.german_shepherd` and is bound to the canonical entity here via an `alias_of` edge.

## Why this exercises Cat 4 (alias resolution)

The AKC standard is the U.S.-registry anchor for the canonical name "German Shepherd Dog." A memory system that ingests this note alongside the Royal Kennel Club note (which documents the historical "Alsatian" naming) and any community-journalism note that uses "GSD" colloquially must collapse all three surface forms — "German Shepherd Dog" (AKC canonical), "Alsatian" (UK historical), "GSD" (colloquial abbreviation) — onto a single graph entity. Failure to collapse fragments the breed into multiple disconnected nodes, which is the canonical Cat 4 failure mode.

## Provenance and limitations

The source PDF was retrieved successfully and its full text was parsed page-by-page in this note's drafting session (AKC GermanShepherdDog.pdf, 182.6 KB, three pages, "Approved February 11, 1978 / Reformatted July 11, 1994" footer verified). Quoted phrases above are excerpted directly from the standard text. The "GSD" abbreviation alias is bound by the registry entry in `ontology.yaml#aliases.german_shepherd` rather than by a quote from the AKC standard itself; the `needs_grounding: true` flag on that edge marks this as an alias-registry-grounded edge rather than a source-text-grounded edge.

## Sources

- Official Standard of the German Shepherd Dog — American Kennel Club (canonical URL of record): https://images.akc.org/pdf/breeds/standards/GermanShepherdDog.pdf
- Corpus alias registry: `ontology.yaml#aliases.german_shepherd`
