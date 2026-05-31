"""Run B-Cubed entity-resolution evaluation against the gold set.

Scores a clustering against `eval/er_gold.json`:

  * **B-Cubed P/R/F1** over the coreference `clusters` (the recall story;
    comparable across runs). Target F1 >= 0.85.
  * **merge violations** — a precision guard. `clusters` + `contrast` are
    treated as distinct gold groups; any pair the prediction puts in the same
    cluster but the gold puts in different groups is a violation (e.g. merging
    `Brucella canis` with `brucellosis`, or `Hill's` with `Hill's Science Diet`).

With no `--pred`, it scores the current slug-identity baseline (`slugify(label)`),
which has nothing to hook a real resolver into yet.

Usage:
    python -m eval.run_er_eval                  # slug baseline
    python -m eval.run_er_eval --pred FILE.json # a resolver's {clusters:[...]} output
    python -m eval.run_er_eval --resolver       # the deterministic EntityResolver
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eval.er_metrics import bcubed, clusters_to_assignment

_GOLD_PATH = Path(__file__).parent / "er_gold.json"
TARGET_F1 = 0.85


def _load_gold(path: Path) -> tuple[list[list[str]], list[list[str]]]:
    data = json.loads(path.read_text())
    coref = [c["members"] for c in data.get("clusters", [])]
    contrast = [c["members"] for c in data.get("contrast", [])]
    return coref, contrast


def slug_baseline_assignment(items: list[str]) -> dict[str, str]:
    """Cluster each item by slugify(label) — the system's current identity rule."""
    from second_brain.ontology import slugify
    return {item: slugify(item) for item in items}


def count_merge_violations(
    predicted: dict[str, object], groups: list[list[str]]
) -> list[tuple[str, str]]:
    """Pairs the prediction merged that belong to different gold groups."""
    group_of = clusters_to_assignment(groups)
    items = [i for i in group_of if i in predicted]
    violations = []
    for a_i in range(len(items)):
        for b_i in range(a_i + 1, len(items)):
            a, b = items[a_i], items[b_i]
            if group_of[a] != group_of[b] and predicted[a] == predicted[b]:
                violations.append((a, b))
    return violations


def _resolver_assignment(items: list[str]) -> dict[str, str]:
    from second_brain.pipeline import EntityResolver
    result = EntityResolver([{"label": i, "entity_type": ""} for i in items]).resolve()
    asg: dict[str, str] = {}
    for cid, cluster in enumerate(result.clusters):
        for m in cluster.members:
            asg[m] = cid
    return asg


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gold", default=str(_GOLD_PATH))
    ap.add_argument("--pred", default=None, help="Resolver output JSON ({clusters:[{members:[...]}]}).")
    ap.add_argument("--resolver", action="store_true",
                    help="Score the built-in deterministic EntityResolver.")
    args = ap.parse_args(argv)

    coref_clusters, contrast_clusters = _load_gold(Path(args.gold))
    gold = clusters_to_assignment(coref_clusters)
    coref_items = list(gold.keys())
    # universe for the precision guard = coref + contrast members
    all_items = sorted(set(coref_items) | {m for g in contrast_clusters for m in g})

    if args.pred:
        pred_clusters = [c["members"] for c in json.loads(Path(args.pred).read_text())["clusters"]]
        predicted = clusters_to_assignment(pred_clusters)
        label = f"resolver output ({args.pred})"
    elif args.resolver:
        predicted = _resolver_assignment(all_items)
        label = "deterministic EntityResolver (Phase A)"
    else:
        predicted = slug_baseline_assignment(all_items)
        label = "slug-identity baseline (current system)"

    p, r, f1 = bcubed(predicted, gold)
    violations = count_merge_violations(predicted, coref_clusters + contrast_clusters)

    print(f"B-Cubed entity-resolution eval — {label}")
    print(f"  gold: {len(coref_items)} entities in {len(coref_clusters)} coreference clusters")
    print(f"  precision: {p:.3f}")
    print(f"  recall:    {r:.3f}")
    print(f"  F1:        {f1:.3f}   (target >= {TARGET_F1})")
    if f1 >= TARGET_F1:
        print(f"  ✓ meets target (margin +{f1 - TARGET_F1:.3f})")
    else:
        print(f"  ✗ below target by {TARGET_F1 - f1:.3f}")
    print(f"  merge violations (must-not-merge pairs wrongly merged): {len(violations)}")
    for a, b in violations[:10]:
        print(f"      ✗ merged {a!r} + {b!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
