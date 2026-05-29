# good-dog-corpus — demo corpus

A small, real-world, multi-domain corpus you can ingest in minutes to see
the hybrid graph do its thing. 36 markdown notes drawn from public
dog-related sources across six domains:

- **breed_standards** — kennel-club breed definitions
- **veterinary_research** — clinical findings
- **behavioral_research** — cognition and training studies
- **nutrition_safety** — diet, recalls, FDA findings
- **municipal_policy** — bylaws, licensing, breed legislation
- **community_journalism** — local reporting that ties the above together

## Why dogs

Most retrieval benchmarks use tech-domain content (auth migrations, API
configs) — convenient for engineers, opaque to everyone else. Dogs are a
domain everyone has intuition about, with the same structural properties a
graph needs to show its value: cross-domain entities, contradictions over
time, aliases, and connections that only surface through traversal.

## What to look for after ingesting

This corpus is deliberately shaped to make the graph's advantage visible:

- **Cross-domain hidden connections** — e.g. a behavioral-research finding
  and a municipal bylaw that both hinge on the same breed, with no direct
  link in the text. Flat vector search returns each separately; graph
  traversal surfaces the bridge.
- **A real contradiction edge** — the grain-free / canine DCM story (a 2018
  FDA signal later reassessed in 2022). Two notes that disagree; the graph
  records the contradiction instead of averaging it away.
- **Alias resolution** — "German Shepherd Dog" / "GSD" / "Alsatian" collapse
  to one entity (see the `aliases` declarations in note frontmatter).

## Ingest it

```bash
# from the repo root, point ingestion at this vault
python scripts/ingest_obsidian.py --vault examples/good-dog-corpus/vault
# then check graph health + what got extracted
python -m second_brain.check
```

`ontology.yaml` + `ONTOLOGY.md` ship alongside as a worked example of
ontology-first schema design — entity types, edge types, and per-edge
evidence rules, with the design narrative explaining each decision.

## Source & license

Adapted from the **good-dog-corpus** in
[multipass-structural-memory-eval](https://github.com/M0nkeyFl0wer/multipass-structural-memory-eval)
(MIT). Source documents are public; each note's frontmatter carries its
`source_url`, publisher, and license note (short fair-use excerpts for
copyrighted breed standards, full text where the source is open). This is a
clean copy with the eval-framework scaffolding removed — just the corpus and
its ontology.
