"""B-Cubed entity-resolution quality metric — precision, recall, F1.

B-Cubed (Bagga & Baldwin 1998; Amigó et al. 2009, "A comparison of extrinsic
clustering evaluation metrics based on formal constraints") is the standard
metric for coreference / entity-resolution clustering. It is computed per item
and averaged, which (unlike pairwise F1 or purity) satisfies all four of Amigó's
formal constraints — it is not fooled by one giant cluster or by all-singletons.

For each item i, with predicted cluster C(i) and gold cluster L(i):

    precision(i) = |C(i) ∩ L(i)| / |C(i)|     # how pure i's predicted cluster is
    recall(i)    = |C(i) ∩ L(i)| / |L(i)|     # how complete i's gold cluster is

B-Cubed precision/recall are the means of these over all items; F1 is their
harmonic mean. Perfect clustering → 1.0; all-singletons → precision 1, recall
low; one-big-cluster → recall 1, precision low.

Dependency-free on purpose: the metric is ~30 lines with a canonical definition,
so a tested local implementation beats adding the `bcubed-metrics` package. The
unit tests pin it to hand-computed values.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Hashable, Mapping


def clusters_to_assignment(clusters: list[list[Hashable]]) -> dict[Hashable, int]:
    """Convert a list of clusters (each a list of items) into an
    item -> cluster-id assignment map. Items not appearing are simply absent."""
    assignment: dict[Hashable, int] = {}
    for cid, members in enumerate(clusters):
        for item in members:
            assignment[item] = cid
    return assignment


def bcubed(
    predicted: Mapping[Hashable, Hashable],
    gold: Mapping[Hashable, Hashable],
) -> tuple[float, float, float]:
    """Compute (precision, recall, f1) over the items present in BOTH maps.

    `predicted` / `gold` map each item to a cluster id (any hashable label).
    Only items keyed in both are scored, so a resolver that drops items is
    measured on what it kept (caller should log coverage separately).
    """
    items = [i for i in gold if i in predicted]
    if not items:
        return 0.0, 0.0, 0.0

    pred_members: dict[Hashable, list[Hashable]] = defaultdict(list)
    gold_members: dict[Hashable, list[Hashable]] = defaultdict(list)
    for i in items:
        pred_members[predicted[i]].append(i)
        gold_members[gold[i]].append(i)

    p_sum = 0.0
    r_sum = 0.0
    for i in items:
        c = set(pred_members[predicted[i]])
        l = set(gold_members[gold[i]])
        inter = len(c & l)
        p_sum += inter / len(c)
        r_sum += inter / len(l)

    precision = p_sum / len(items)
    recall = r_sum / len(items)
    f1 = 0.0 if (precision + recall) == 0 else 2 * precision * recall / (precision + recall)
    return precision, recall, f1
