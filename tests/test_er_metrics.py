"""Tests for the B-Cubed entity-resolution metric, pinned to hand-computed
values, plus a smoke test of the gold set + runner against real data."""

import json
from pathlib import Path

import pytest

from eval.er_metrics import bcubed, clusters_to_assignment


def _asg(*clusters):
    return clusters_to_assignment([list(c) for c in clusters])


class TestBCubed:
    def test_perfect_clustering(self):
        gold = _asg("abc", "de")
        p, r, f1 = bcubed(gold, gold)
        assert (p, r, f1) == (1.0, 1.0, 1.0)

    def test_all_singletons(self):
        """gold {a,b,c},{d,e}; predicted all singletons → P=1, R=0.4, F1=4/7."""
        gold = _asg("abc", "de")
        predicted = _asg("a", "b", "c", "d", "e")
        p, r, f1 = bcubed(predicted, gold)
        assert p == pytest.approx(1.0)
        assert r == pytest.approx(0.4)
        assert f1 == pytest.approx(2 * 1.0 * 0.4 / 1.4)

    def test_one_big_cluster(self):
        """gold {a,b,c},{d,e}; predicted one cluster → P=0.52, R=1, F1≈0.684."""
        gold = _asg("abc", "de")
        predicted = _asg("abcde")
        p, r, f1 = bcubed(predicted, gold)
        assert p == pytest.approx(0.52)
        assert r == pytest.approx(1.0)
        assert f1 == pytest.approx(2 * 0.52 / 1.52)

    def test_empty_inputs(self):
        assert bcubed({}, {}) == (0.0, 0.0, 0.0)

    def test_scores_only_shared_items(self):
        """Items missing from the prediction are not scored (coverage is the
        caller's concern)."""
        gold = _asg("ab", "cd")
        predicted = clusters_to_assignment([["a", "b"]])  # c, d dropped
        p, r, f1 = bcubed(predicted, gold)
        assert p == pytest.approx(1.0)
        assert r == pytest.approx(1.0)


class TestGoldSet:
    def _gold(self):
        return json.loads((Path(__file__).parent.parent / "eval" / "er_gold.json").read_text())

    def test_gold_set_wellformed_and_sized(self):
        gold = self._gold()
        clusters = gold["clusters"]
        assert len(clusters) >= 20, "brief asks for 20-30 verified clusters"
        for c in clusters:
            assert c["members"], "no empty clusters"
            assert len(c["members"]) >= 2, "gold clusters are multi-member coref cases"

    def test_no_member_appears_in_two_clusters(self):
        """A label belonging to two gold clusters would be a curation bug."""
        seen = {}
        for c in self._gold()["clusters"]:
            for m in c["members"]:
                assert m not in seen, f"{m!r} in both {seen.get(m)!r} and {c['canonical']!r}"
                seen[m] = c["canonical"]

    def test_slug_baseline_below_target(self):
        """The current slug-identity baseline should NOT already meet F1>=0.85 —
        if it did, there'd be nothing for a resolver to improve and the gold set
        would be trivial."""
        from eval.run_er_eval import TARGET_F1, slug_baseline_assignment
        gold_clusters = [c["members"] for c in self._gold()["clusters"]]
        gold = clusters_to_assignment(gold_clusters)
        items = list(gold.keys())
        predicted = slug_baseline_assignment(items)
        _, _, f1 = bcubed(predicted, gold)
        assert f1 < TARGET_F1
