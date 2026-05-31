"""Run B-Cubed entity-resolution evaluation against the gold set.

There is no dedicated resolver module yet (dedup today is `slugify(label)`
identity in the ingest loop). So this scores the **current slug-identity
baseline**: each entity label is clustered by its slug, and that clustering is
compared to `eval/er_gold.json`. The resulting F1 is the baseline a real
resolver must beat; target F1 >= 0.85 (per the canonicalization brief).

Usage:
    python -m eval.run_er_eval                  # score the slug baseline
    python -m eval.run_er_eval --pred FILE.json # score a resolver's output
                                                #   (same {clusters:[{members:[...]}]} shape)

The slug baseline merges case/whitespace variants (which share a slug) but
splits acronym<->expansion and singular<->plural (different slugs) — exactly the
coreference the gold set captures, so the gap is meaningful, not cosmetic.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eval.er_metrics import bcubed, clusters_to_assignment

_GOLD_PATH = Path(__file__).parent / "er_gold.json"
TARGET_F1 = 0.85


def _load_clusters(path: Path) -> list[list[str]]:
    data = json.loads(path.read_text())
    return [c["members"] for c in data["clusters"]]


def slug_baseline_assignment(items: list[str]) -> dict[str, str]:
    """Cluster each item by slugify(label) — the system's current identity rule."""
    from second_brain.ontology import slugify
    return {item: slugify(item) for item in items}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gold", default=str(_GOLD_PATH))
    ap.add_argument("--pred", default=None,
                    help="Resolver output JSON (same shape as the gold). "
                         "If omitted, scores the slug-identity baseline.")
    args = ap.parse_args(argv)

    gold_clusters = _load_clusters(Path(args.gold))
    gold = clusters_to_assignment(gold_clusters)
    items = list(gold.keys())
    n_clusters = len(gold_clusters)

    if args.pred:
        predicted = clusters_to_assignment(_load_clusters(Path(args.pred)))
        label = f"resolver output ({args.pred})"
    else:
        predicted = slug_baseline_assignment(items)
        label = "slug-identity baseline (current system)"

    p, r, f1 = bcubed(predicted, gold)
    covered = sum(1 for i in items if i in predicted)

    print(f"B-Cubed entity-resolution eval — {label}")
    print(f"  gold: {len(items)} entities in {n_clusters} coreference clusters")
    print(f"  coverage: {covered}/{len(items)} gold items present in prediction")
    print(f"  precision: {p:.3f}")
    print(f"  recall:    {r:.3f}")
    print(f"  F1:        {f1:.3f}   (target >= {TARGET_F1})")
    gap = TARGET_F1 - f1
    if f1 >= TARGET_F1:
        print(f"  ✓ meets target (margin +{-gap:.3f})")
    else:
        print(f"  ✗ below target by {gap:.3f} — this is the gap a real resolver must close")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
