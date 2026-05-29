---
note_id: breed_rkc_german_shepherd_dog_standard
source_url: https://www.royalkennelclub.com/breed-standards/pastoral/german-shepherd-dog/
source_title: "German Shepherd Dog | Breed Standards | The Kennel Club"
source_date: "2016-08-01"
source_publisher: "The Royal Kennel Club (UK)"
license: fair_use_excerpt
license_note: "The Royal Kennel Club holds copyright in its breed standards. Short excerpts are quoted under fair use for non-commercial research and evaluation; the full standard is not reproduced. The 'Alsatian' naming history is sourced from independently reported coverage of the 1977 UK Kennel Club name reversion (see Provenance and limitations)."
accessed_on: "2026-04-30"
domain: breed_standards
alias_pair_id: german_shepherd

entities:
  - id: breed_alsatian
    type: breed
    canonical: "Alsatian"
    notes: "Surface form: the historical UK name used for the German Shepherd Dog from the post-WWI era until the UK Kennel Club's 1977 reversion to 'German Shepherd Dog'. Bound to breed_german_shepherd_dog via alias_of."
  - id: org_rkc
    type: organization
    canonical: "The Royal Kennel Club (UK)"
    is_regulatory: false
    notes: "Breed registry authority for the United Kingdom. Formerly known as 'The Kennel Club'."
  - id: pub_rkc_gsd_standard
    type: publication
    canonical: "Royal Kennel Club Breed Standard: German Shepherd Dog (Pastoral Group)"

edges:
  - from: pub_rkc_gsd_standard
    type: authored_by
    to: org_rkc
    evidence: "Page is published on royalkennelclub.com under the Breed Standards section, Pastoral Group."
  - from: pub_rkc_gsd_standard
    type: mentions
    to: breed_german_shepherd_dog
    evidence: "Page title: 'German Shepherd Dog | Breed Standards | The Kennel Club'. The RKC classifies the breed in the Pastoral Group, distinct from the AKC's Herding Group classification."
  - from: breed_alsatian
    type: alias_of
    to: breed_german_shepherd_dog
    evidence: "The UK Kennel Club registered the breed as 'Alsatian' (originally 'Alsatian Wolf Dog') in the post-WWI era and reverted to 'German Shepherd Dog' in 1977. Reported in coverage of the UK reversion: 'The UK Kennel Club finally allowed the official reversion back to German Shepherd Dog in 1977.' Registered in ontology.yaml#aliases.german_shepherd."
  - from: org_rkc
    type: regulates
    to: breed_german_shepherd_dog
    evidence: "The Royal Kennel Club is the UK breed registry authority that issues and maintains the official UK breed standard for the German Shepherd Dog."

tags: [breed_standards, royal_kennel_club, german_shepherd, alsatian, alias_chain, cross_registry_classification]
---

# Royal Kennel Club Breed Standard: German Shepherd Dog

## Summary

The Royal Kennel Club (RKC, formerly "The Kennel Club") is the United Kingdom's national breed registry. The RKC publishes its breed standard for this breed under the title **"German Shepherd Dog"** and classifies it within the **Pastoral Group**. The RKC standard page is the UK-side anchor for the German Shepherd Dog canonical name.

The standard wording on the RKC page was last amended **August 2016** per the page metadata cited in the corpus source manifest.

## Documented aliases / historical naming

The breed was historically registered in the UK under a different name. Following World War I, the UK Kennel Club renamed the breed to **"Alsatian Wolf Dog"** and later simply **"Alsatian"**, on the rationale that the "German" association was problematic during the period of intense post-war anti-German sentiment. The name "Alsatian" derives from the Alsace-Lorraine region on the French-German border.

In **1977**, the UK Kennel Club restored the original name. Reporting on the reversion summarizes:

> "The UK Kennel Club finally allowed the official reversion back to German Shepherd Dog in 1977, marking a formal end to the wartime terminology."

After 1977 the registered UK name is "German Shepherd Dog" again, the same canonical form used by the AKC. "Alsatian" survives in popular UK usage but is no longer the registered form.

This naming history is the reason the corpus's alias chain in `ontology.yaml#aliases.german_shepherd` lists "Alsatian" alongside "GSD" and "German Shepherd Dog" as surface forms of one canonical breed.

## Why this exercises Cat 4 (alias resolution)

The "Alsatian" alias is the historically deepest surface form in the German Shepherd Dog alias chain — it is not just an abbreviation (like "GSD") but a full alternative breed name once held by an authoritative national registry. A memory system that ingests AKC content (which uses "German Shepherd Dog"), older UK material (which uses "Alsatian"), and modern UK material (which uses "German Shepherd Dog" again) must collapse all three surfaces onto one canonical breed entity to answer questions like "what is the UK registry's classification of the breed Americans call the German Shepherd?" without fragmenting the graph.

## Cross-registry framing note

This note also seeds a Cat 3 candidate: the RKC classifies the German Shepherd Dog in the **Pastoral Group**, while the AKC classifies the same breed in the **Herding Group** (per `akc-german-shepherd-dog.md` and the AKC group taxonomy). Same canonical breed, different registry-level group classification. This is a real, citable, and registry-level disagreement available for future contradiction-pair binding; it is not bound as a `contradicts` edge in v0.1 because both registry classifications can be simultaneously correct under their own taxonomies.

## Provenance and limitations

The Royal Kennel Club page itself was not directly fetched in this note's drafting session (WebFetch was sandbox-denied for the URL). Verification was via WebSearch, which returned the live RKC URL in its results with current title and reporting that confirmed the 1977 name reversion as documented across multiple independently published sources. The Pastoral Group classification is documented in the RKC source manifest (`sources/breed_standards.yaml#breed_gsd_uk_kennel_club`) and in the WebSearch results page metadata. A future revision of this note should re-fetch the RKC URL directly and verify that the page text matches the cited classification and any wording amendments since 2016-08-01.

## Sources

- German Shepherd Dog | Breed Standards | The Kennel Club (canonical URL of record): https://www.royalkennelclub.com/breed-standards/pastoral/german-shepherd-dog/
- Wikipedia, "German Shepherd" — historical naming context (the Alsatian name change post-WWI and 1977 reversion): https://en.wikipedia.org/wiki/German_Shepherd
- Corpus alias registry: `ontology.yaml#aliases.german_shepherd`
- Companion AKC anchor: `vault/breed_standards/akc-german-shepherd-dog.md`
