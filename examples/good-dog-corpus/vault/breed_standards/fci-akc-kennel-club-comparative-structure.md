---
note_id: breed_fci_akc_kc_comparative_structure
source_url: https://en.wikipedia.org/wiki/F%C3%A9d%C3%A9ration_Cynologique_Internationale
source_title: "Fédération Cynologique Internationale — Wikipedia overview of FCI structure and agreements"
source_date: "2026-05-03"
source_publisher: "Wikipedia contributors"
license: cc_by_sa
license_note: "Wikipedia content is licensed under CC BY-SA 4.0. Facts about FCI structure verified against multiple sources including breedarchive.com and official FCI nomenclature page."
accessed_on: "2026-05-03"
domain: breed_standards
alias_pair_id: null

entities:
  - id: org_fci
    type: organization
    canonical: "Fédération Cynologique Internationale"
    is_regulatory: false
    notes: "International federation of 98 national kennel clubs. Not a registry itself — does not issue pedigrees. Coordinates breed standards, judges, and show rules across member countries. Based in Thuin, Belgium. Founded 1911."
  - id: org_akc
    type: organization
    canonical: "American Kennel Club"
    is_regulatory: false
    notes: "U.S. national breed registry. FCI Letter of Agreement partner since November 5, 2005. Not an FCI member. Issues AKC pedigrees and maintains breed standards for 200 recognized breeds."
  - id: org_tkc
    type: organization
    canonical: "The Kennel Club (UK)"
    is_regulatory: false
    notes: "UK national breed registry. FCI Letter of Agreement partner since May 1, 2017. Not an FCI member. Formerly known as 'The Kennel Club' — rebranded as 'Royal Kennel Club' in 2024 in the UK context, though the entity is the same."
  - id: org_ukc
    type: organization
    canonical: "United Kennel Club"
    is_regulatory: false
    notes: "U.S.-based registry. FCI does NOT recognize UKC, no agreement in place. UKC focuses on working and performance breeds; issues its own breed standards separate from AKC/FCI."
  - id: concept_closed_stud_book
    type: concept
    canonical: "Closed stud book"
    notes: "A breed registry system in which dogs must have registered ancestors (typically several generations) to be eligible for registration. Prevents outside blood from entering the registry. Most major registries (AKC, KC, FCI member clubs) operate closed stud books. Contrast with open registry."
  - id: concept_open_registry
    type: concept
    canonical: "Open registry"
    notes: "A breed registry system that allows dogs to be registered without documented pedigree ancestry, based on conformation or performance evaluation. Associated with health-improvement goals through genetic diversity. Pioneer: Swedish open registry (1970s), credited with reducing hip dysplasia incidence by 50% over 13 years in Swedish breeding stock."
  - id: breed_group_fci_system
    type: concept
    canonical: "FCI breed group taxonomy"
    notes: "FCI divides its 356 recognized breeds into 10 groups. Differs from AKC (7 groups) and KC (7 groups). FCI groups: (1) Sheepdogs and Cattledogs, (2) Pinscher and Schnauzer and Molossoid, (3) Terriers, (4) Dachshunds, (5) Spitz and Primitive Types, (6) Scent Hounds and Related Breeds, (7) Pointing Dogs, (8) Retrievers and Flushing Dogs and Water Dogs, (9) Companion and Toy Dogs, (10) Sighthounds."
  - id: breed_group_akc_system
    type: concept
    canonical: "AKC breed group taxonomy"
    notes: "AKC divides its ~200 recognized breeds into 7 groups: Sporting, Hound, Working, Terrier, Toy, Non-Sporting, Herding (added 1983). Group assignments differ from FCI for the same breed in some cases."

edges:
  - from: org_fci
    type: regulates
    to: concept_breed_group_fci_system
    evidence: "FCI publishes and maintains the official breed group taxonomy (10 groups) for all breeds recognized by its 98 member national clubs. The nomenclature page at fci.be/nomenclature.aspx lists every breed under its assigned group and section."
  - from: org_akc
    type: regulates
    to: breed_group_akc_system
    evidence: "AKC assigns each of its ~200 recognized breeds to one of seven groups and publishes the group taxonomy at akc.org/dog-breeds/groups/. The Herding Group was the last group added in 1983."
  - from: org_fci
    type: regulates
    to: concept_closed_stud_book
    evidence: "FCI coordinates breed standards across member national clubs, all of which maintain their own stud books. FCI itself does not issue pedigrees; that function belongs to each national club, most of which operate closed stud books. The FCI system of breed ownership (each breed 'owned' by a specific country) reinforces closed-registry norms."
  - from: concept_open_registry
    type: contradicts
    to: concept_closed_stud_book
    evidence: "The open vs closed registry debate is documented in multiple sources as a substantive disagreement. Proponents of open registries (e.g., JoAnn Teems, GDC advocates) argue closed stud books cause inbreeding depression and genetic disease accumulation. Closed registry advocates argue open registries dilute breed type and compromise conformation standards. This is a genuine contemporary disagreement — both positions have credentialed professional advocates. This seeded pair exercises Cat 3 (contradiction detection)."
  - from: org_akc
    type: member_of
    to: org_fci
    evidence: "AKC is not a direct member of FCI but holds a 'Letter of Agreement' for mutual pedigree and judge recognition, signed November 5, 2005. This is a formal agreement-level relationship, not full membership. The same agreement structure exists for The Kennel Club (UK) and Canadian Kennel Club."
  - from: org_tkc
    type: member_of
    to: org_fci
    evidence: "The Kennel Club (UK) holds a Letter of Agreement with FCI effective May 1, 2017. The UK Kennel Club is not a full FCI member; like AKC, it operates independently but with mutual recognition arrangements."
  - from: org_ukc
    type: member_of
    to: org_fci
    evidence: "The United Kennel Club is explicitly NOT recognized by FCI. Wikipedia and breedarchive.com both confirm: 'In contrast, the FCI does not recognise the UKC and no agreement is in place.' This creates a real regulatory asymmetry for breeds registered with UKC but not AKC."
  - from: org_akc
    type: regulates
    to: breed_german_shepherd_dog
    evidence: "AKC is the U.S. breed registry authority for German Shepherd Dog. Issues AKC registration and publishes the official breed standard for the breed in the United States. (Entity breed_german_shepherd_dog already declared in akc-german-shepherd-dog.md.)"
  - from: org_tkc
    type: regulates
    to: breed_german_shepherd_dog
    evidence: "The Kennel Club is the UK breed registry authority for German Shepherd Dog, classified in the Pastoral Group (distinct from AKC's Herding Group classification). (Entity breed_german_shepherd_dog already declared.)"

tags: [breed_standards, fci, akc, kennel_club, registry_systems, breed_groups, closed_registry, open_registry, cross_registry]
---

# FCI vs AKC vs The Kennel Club: Structural Comparison

## Summary

Three major registry systems dominate the global purebred dog world: the **Fédération Cynologique Internationale (FCI)**, the **American Kennel Club (AKC)**, and **The Kennel Club (UK)** — recently rebranded as the **Royal Kennel Club** in some contexts. Understanding their structural differences is foundational to interpreting breed standards, breed group classifications, and why the same breed can have different official classifications and requirements depending on which registry issues the standard.

## FCI: The International Coordinator

The **Fédération Cynologique Internationale** is the largest international federation of national kennel clubs, with 98 member and contract partner organizations (one per country). It was founded in 1911 by clubs from Germany, Austria, Belgium, France, and the Netherlands.

**Key structural facts about FCI:**

- **Not a registry.** FCI does not issue pedigrees or maintain breeder records. That function belongs to each national club.
- **Breed "ownership."** Each recognized breed is assigned as the "property" of a specific country. That country writes the breed standard in partnership with FCI's Standards and Scientific Commissions. FCI publishes and translates standards into English, French, German, and Spanish.
- **10-group taxonomy.** FCI divides its 356 recognized breeds into 10 groups (vs. 7 for AKC and KC).
- **Judges and shows.** FCI maintains the qualification standards for judges at FCI international shows. National clubs issue judge licenses under FCI oversight.

**FCI's relationship to AKC and KC:** Both AKC and The Kennel Club are **not FCI members** — they are independent registries that have instead signed **Letters of Agreement** with FCI for mutual pedigree and judge recognition. AKC's agreement dates from November 5, 2005; The Kennel Club's from May 1, 2017. The **United Kennel Club (UKC) has no such agreement with FCI** — this is a documented asymmetry.

## AKC: The U.S. Standard-Bearer

The **American Kennel Club** is the oldest and largest U.S. breed registry, founded 1884. It maintains the official stud book for approximately 200 recognized breeds and publishes breed standards for each.

**Key structural facts about AKC:**

- **Closed stud book.** AKC requires documented ancestry (both parents registered) for litter registration. It maintains a policy of not registering dogs from registries it does not recognize.
- **7-group taxonomy.** AKC organizes breeds into Sporting, Hound, Working, Terrier, Toy, Non-Sporting, and Herding (added 1983).
- **CHIC program.** The Canine Health Information Center (CHIC) is a recommended screening database, not a requirement — AKC does not mandate health testing for breeding stock. (This contrasts with FCI-member national clubs that often require breed-specific health screening as a condition of registration.)
- **Parent club system.** Each AKC-recognized breed has a parent breed club that advises on the standard and breeding recommendations.

**AKC breed group for German Shepherd Dog: Herding Group** — distinct from the Pastoral Group classification assigned by The Kennel Club for the same breed.

## The Kennel Club (UK): The Original Registry

**The Kennel Club** (now trading as Royal Kennel Club in the UK) was founded in 1873 and is the oldest kennel club in the world.

**Key structural facts about The Kennel Club:**

- **Closed stud book.** Similar to AKC, Kennel Club registration requires registered ancestry.
- **7-group taxonomy** (same structure as AKC: Gundog, Hound, Pastoral, Terrier, Toy, Utility, Working — terminology differs slightly from AKC).
- **BVA/KC health schemes.** The Kennel Club co-administers hip and elbow dysplasia screening schemes with the British Veterinary Association. Breed-specific health requirements are more prescriptive than AKC's guidelines — the KC's Assured Breeders scheme mandates specific tests for specific breeds.

**Kennel Club breed group for German Shepherd Dog: Pastoral Group** — different from AKC's Herding Group for the same breed. This is a cross-registry classification difference available as a Cat 3 seed.

## The Closed vs. Open Registry Debate

This comparison note seeds a Cat 3 (contradiction) pair between two concepts: **closed stud book** and **open registry**.

**The closed registry position** (dominant in AKC, KC, FCI-member clubs): A closed stud book maintains breed type and genetic integrity. It ensures that show dogs conform to established standards. It creates a traceable pedigree record for every registered dog.

**The open registry position** (advocated by canine geneticists, organizations like GDC — Genetic Disease Control in Animals, and working-dog registries): Closed stud books cause inbreeding depression. Starting with small founder populations and never adding outside blood causes progressive accumulation of harmful recessive alleles. The Swedish open registry, begun in the 1970s, reportedly reduced hip dysplasia incidence by 50% over 13 years in Swedish breeding stock. The OFA (Orthopedic Foundation for Animals) certifies only disease-free animals — keeping affected animals' status secret — whereas open registries publish all test results including carriers.

Both positions have credentialed professional advocates. This is a genuine contradiction in breeding philosophy, not a factual error on either side.

## Sources

- Fédération Cynologique Internationale — Wikipedia: https://en.wikipedia.org/wiki/F%C3%A9d%C3%A9ration_Cynologique_Internationale
- FCI Breed Nomenclature (definitive group assignments): http://fci.be/nomenclature.aspx?lang=en
- A Look Into the FCI — Breed Archive: https://breedarchive.com/blog/view/35/a-look-into-the-fci
- AKC Breed Groups: Understanding Breed Groups at Dog Shows: https://www.akc.org/dog-breeds/groups/
- History of AKC Breed Groups (Caroline Coile, PhD, 2025): https://akc.org/expert-advice/dog-breeds/history-akc-breed-groups
- Open Registry Offers Rx For Dog Ailments (Divine Farm / GDC historical source, 1995): http://devinefarm.net/rp/rporeg.htm
- Breed registry — Citizendium (closed vs open stud book definitions): https://citizendium.org/wiki/Breed_registry
- Companion GSD registry notes: `vault/breed_standards/akc-german-shepherd-dog.md`, `vault/breed_standards/royal-kennel-club-german-shepherd-dog.md`