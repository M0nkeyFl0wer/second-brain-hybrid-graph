---
note_id: vet_2023_acvim_leptospirosis_consensus
source_url: https://onlinelibrary.wiley.com/doi/10.1111/jvim.16903
source_title: "ACVIM consensus statement on leptospirosis in dogs"
source_date: "2023-11-01"
source_publisher: "Journal of Veterinary Internal Medicine (Wiley) — open access"
license: cc_by_4_0
license_note: "Open-access JVIM article under CC BY 4.0; PMC deposit confirmed for reuse"
accessed_on: "2026-05-03"
domain: veterinary_research

# Ontology-aligned entity declarations introduced by this note.
entities:
  - id: pub_acvim_leptospirosis_consensus_2023
    type: publication
    canonical: "ACVIM consensus statement on leptospirosis in dogs"
    aliases: ["Sykes 2023 ACVIM leptospirosis", "ACVIM consensus 2023"]
  - id: person_jane_sykes
    type: person
    canonical: "Jane E. Sykes"
    aliases: ["J.E. Sykes", "Sykes"]
  - id: org_acvim
    type: organization
    canonical: "American College of Veterinary Internal Medicine"
    aliases: ["ACVIM"]
  - id: concept_leptospirosis
    type: concept
    canonical: "Canine leptospirosis"
    aliases: ["leptospirosis in dogs", "canine lepto"]
  - id: concept_leptospirosis_vaccine
    type: concept
    canonical: "Leptospirosis vaccination in dogs"
    aliases: ["lepto vaccine", "leptospirosis vaccine", "4-serovar leptospirosis vaccine"]
  - id: concept_leptospiral_bacterin
    type: concept
    canonical: "Leptospiral bacterin vaccine"
    aliases: ["bacterin vaccine", "killed whole-cell leptospirosis vaccine"]
  - id: concept_4_serovar_vaccine
    type: concept
    canonical: "Four-serovar leptospirosis vaccine"
    aliases: ["4-serovar vaccine", "quadrivalent leptospirosis vaccine"]
    notes: "In North America: serovars Icterohaemorrhagiae, Canicola, Grippotyphosa, Pomona"

edges:
  - from: pub_acvim_leptospirosis_consensus_2023
    type: authored_by
    to: person_jane_sykes
    evidence: "First author Jane E. Sykes, BVSc (Hons) PhD MBA MPH FNAP DACVIM; ACVIM consensus statement published November 2023"
  - - from: pub_acvim_leptospirosis_consensus_2023
      type: subject_of
      to: concept_leptospirosis
      evidence: "Consensus statement covers diagnosis, treatment, prevention, and control of canine leptospirosis"
  - from: pub_acvim_leptospirosis_consensus_2023
    type: subject_of
    to: concept_leptospirosis_vaccine
    evidence: "Statement includes explicit recommendations on vaccination: all dogs annually, regardless of breed, age, or lifestyle"
  - from: pub_acvim_leptospirosis_consensus_2023
    type: mentions
    to: concept_4_serovar_vaccine
    evidence: "Statement recommends 4-serovar vaccines (Icterohaemorrhagiae, Canicola, Grippotyphosa, Pomona) for North American dogs"
  - from: pub_acvim_leptospirosis_consensus_2023
    type: mentions
    to: concept_leptospiral_bacterin
    evidence: "Statement notes that current vaccines are adjuvanted killed whole-cell bacterins but that nonadjuvanted options have been marketed more recently"
  - from: person_jane_sykes
    type: affiliated_with
    to: org_acvim
    evidence: "Sykes holds ACVIM diplomate status and the consensus statement is published under ACVIM auspices"
  - from: pub_acvim_leptospirosis_consensus_2023
    type: contradicts
    to: pub_legacy_lepto_vaccine_reaction_consensus
    evidence: "The 2023 consensus statement reverses the historical 'vaccinate only high-risk dogs, be cautious in small breeds' position; states that current 4-serovar vaccines have safety profiles similar to DAPP vaccines, adverse reactions are rare (<53 per 10,000 doses), and all dogs in North America should be vaccinated annually regardless of breed or size — a direct contradiction of pre-2020 guidance that recommended limiting vaccination in small breeds due to perceived higher reaction risk"

tags: [vet_research, leptospirosis, vaccination, acvim, consensus, adverse_reactions, breed, 4_serovar]
contradiction_pair_id: lepto_vaccine_adverse_reactions_2023
---

# ACVIM consensus statement on leptospirosis in dogs (Sykes et al., JVIM 2023)

## Summary

A peer-reviewed consensus statement published in the *Journal of Veterinary Internal Medicine* (volume 36, issue 6, November 2023) by Jane E. Sykes and colleagues under the auspices of the American College of Veterinary Internal Medicine (ACVIM). The statement addresses diagnosis, treatment, prevention, and control of canine leptospirosis, and represents the most current comprehensive guidance from a specialty college on the disease.

Two load-bearing positions in the statement are relevant to the corpus's Cat 3 (contradiction) and Cat 4 (alias/ingestion integrity) objectives:

1. **Universal annual vaccination recommendation.** The statement recommends that all dogs in North America — regardless of breed, age, sex, lifestyle, or geographic location — receive annual leptospirosis vaccination with a 4-serovar vaccine. This is a marked shift from earlier guidance that was breed- and lifestyle-specific.

2. **Modern leptospirosis vaccines have safety profiles comparable to other canine vaccines.** The statement directly addresses the historical concern about elevated adverse reaction rates, especially in small-breed dogs, finding that contemporary data do not support this concern at a statistically significant level.

This note is the anchor for the corpus's second Cat 3 contradiction pair, `lepto_vaccine_adverse_reactions_2023`, which pairs the 2023 consensus position against prior guidance that recommended caution in small breeds.

## Key recommendations

On universal vaccination:
> "Vaccines should be administered annually to all dogs starting at 12 weeks of age, regardless of breed, because leptospirosis is a zoonotic disease, can be severe or fatal despite treatment, and exposure can occur regardless of age, geography, or lifestyle."

On vaccine safety and adverse reactions:
> "Based on available information, adverse reactions to leptospiral vaccines seem to be rare, with <53 adverse events per 10,000 doses. Most adverse reactions are minor, and serious anaphylactic reactions were reported no more often for dogs given leptospiral vaccines than for other vaccine antigens."

> "Patient factors such as breed and size can influence the risk of vaccine-associated adverse events, regardless of the antigen source. Research approximately 2 decades ago indicated that some vaccines for dogs that included a Leptospira component contained high concentrations of bovine serum albumin, which could account for post-vaccinal IgE-based adverse events. More recent research indicates protein content, concentrations, and severe adverse event rates are not higher for leptospirosis vaccines than distemper-parvovirus or rabies vaccines."

On vaccine efficacy:
- Current 4-serovar bacterin vaccines provide at least 12 months of duration of immunity.
- Protection against clinical disease: ~84% overall pooled efficacy across commercial vaccines (from systematic review and meta-analysis cited in the statement).
- Protection against renal carrier state: ~88%.
- Vaccines are serogroup-specific; partial cross-protection to heterologous serogroups has been documented.
- Leptospirosis in fully vaccinated dogs has been documented but appears uncommon.

## The Cat 3 contradiction pair

The 2023 ACVIM consensus directly reverses the pre-2020 normative position that:
- Leptospirosis vaccination was recommended primarily for large-breed dogs with rural outdoor exposure.
- Small-breed dogs were frequently unvaccinated due to concerns about adverse reactions.
- Vaccination every 6 months was sometimes recommended for high-risk dogs.

The contradiction pair `lepto_vaccine_adverse_reactions_2023` pairs this 2023 consensus statement (universal annual vaccination for all dogs, modern vaccines have equivalent safety to other vaccines) against the prior consensus (selective vaccination based on breed/lifestyle, historical concern about elevated reaction rates in small dogs).

## Sources

- Sykes JE, et al. "ACVIM consensus statement on leptospirosis in dogs." *J Vet Intern Med* 36(6), November 2023. Open access (canonical URL of record): https://onlinelibrary.wiley.com/doi/10.1111/jvim.16903
- PMC deposit (open access): https://pmc.ncbi.nlm.nih.gov/articles/PMC10689572/
- AAHA 2022 Canine Vaccination Guidelines (companion source for 2022 pre-consensus position): https://www.aaha.org/resources/2022-aaha-canine-vaccination-guidelines/leptospirosis/
- Systematic review and meta-analysis (vaccine efficacy): B. Adler et al., *Vaccine* 40(2022):2950–2958, DOI: 10.1016/j.vaccine.2022.03.044