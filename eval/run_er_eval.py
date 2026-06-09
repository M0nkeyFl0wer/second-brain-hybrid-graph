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

from kg_common.measure.er_quality import bcubed

_GOLD_PATH = Path(__file__).parent / "er_gold.json"
_EMB_PATH = Path(__file__).parent / "er_gold_embeddings.json"
TARGET_F1 = 0.85


def clusters_to_assignment(clusters: list[list]) -> dict:
    """Convert a list of clusters (each a list of items) into an
    item -> cluster-id assignment map. Items not appearing are simply absent."""
    assignment: dict = {}
    for cid, members in enumerate(clusters):
        for item in members:
            assignment[item] = cid
    return assignment


def bcubed_pr_f1(gold: dict, predicted: dict) -> tuple[float, float, float]:
    """(precision, recall, F1) over the items present in BOTH maps, computed by
    the canonical ``kg_common.measure.er_quality.bcubed``.

    This is a thin ADAPTER, not a metric reimplementation: it restricts both
    maps to their shared item set (so a resolver that drops items is scored on
    what it kept — the original ``eval/er_metrics`` semantics) and unpacks
    kg_common's ``BCubedScore`` into the ``(p, r, f1)`` tuple the eval and tests
    expect. kg_common's ``bcubed`` is strict about identical keys (it raises on
    a mismatch), which is why the shared-key restriction happens here rather
    than inside the metric."""
    shared = [i for i in gold if i in predicted]
    g = {i: gold[i] for i in shared}
    p = {i: predicted[i] for i in shared}
    score = bcubed(g, p)
    return score.precision, score.recall, score.f1


def _load_gold(path: Path) -> tuple[list[list[str]], list[list[str]], dict[str, str]]:
    data = json.loads(path.read_text())
    coref = [c["members"] for c in data.get("clusters", [])]
    contrast = [c["members"] for c in data.get("contrast", [])]
    types = data.get("types", {})
    return coref, contrast, types


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


def _resolver_assignment(
    items: list[str], types: dict[str, str], embeddings: dict[str, list[float]] | None
) -> dict[str, str]:
    from second_brain.pipeline import EntityResolver

    entities = [{"label": i, "entity_type": types.get(i, "")} for i in items]
    result = EntityResolver(entities, embeddings=embeddings).resolve()
    asg: dict[str, str] = {}
    for cid, cluster in enumerate(result.clusters):
        for m in cluster.members:
            asg[m] = cid
    return asg


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gold", default=str(_GOLD_PATH))
    ap.add_argument(
        "--pred", default=None, help="Resolver output JSON ({clusters:[{members:[...]}]})."
    )
    ap.add_argument("--resolver", action="store_true", help="Score the built-in EntityResolver.")
    ap.add_argument(
        "--no-embeddings",
        action="store_true",
        help="With --resolver, disable the embedding tier (string/deterministic only).",
    )
    ap.add_argument(
        "--fail-under",
        type=float,
        default=None,
        help="Exit non-zero if F1 is below this threshold.",
    )
    ap.add_argument(
        "--max-violations",
        type=int,
        default=None,
        help="Exit non-zero if merge violations exceed this count.",
    )
    args = ap.parse_args(argv)

    coref_clusters, contrast_clusters, types = _load_gold(Path(args.gold))
    gold = clusters_to_assignment(coref_clusters)
    coref_items = list(gold.keys())
    # universe for the precision guard = coref + contrast members
    all_items = sorted(set(coref_items) | {m for g in contrast_clusters for m in g})

    if args.pred:
        pred_clusters = [c["members"] for c in json.loads(Path(args.pred).read_text())["clusters"]]
        predicted = clusters_to_assignment(pred_clusters)
        label = f"resolver output ({args.pred})"
    elif args.resolver:
        embeddings = None
        if not args.no_embeddings and _EMB_PATH.exists():
            embeddings = json.loads(_EMB_PATH.read_text())
        predicted = _resolver_assignment(all_items, types, embeddings)
        label = "EntityResolver" + ("" if embeddings else " (deterministic only)")
    else:
        predicted = slug_baseline_assignment(all_items)
        label = "slug-identity baseline (current system)"

    p, r, f1 = bcubed_pr_f1(gold, predicted)
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

    failed = False
    if args.fail_under is not None and f1 < args.fail_under:
        print(f"  FAIL: F1 {f1:.3f} < --fail-under {args.fail_under:.3f}")
        failed = True
    if args.max_violations is not None and len(violations) > args.max_violations:
        print(
            f"  FAIL: merge violations {len(violations)} > --max-violations {args.max_violations}"
        )
        failed = True
    if failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
