"""Tests for the Phase-A deterministic entity resolver: pure matchers,
union-find clustering, and an end-to-end check against the gold set (recall up,
precision held, zero must-not-merge violations)."""

import json
from pathlib import Path

from second_brain.pipeline.resolve import (
    EntityResolver,
    initials,
    match_acronym,
    match_normalized,
    match_plural,
    match_surname,
    normalize,
    singular_key,
)


class TestNormalization:
    def test_normalize_strips_case_punct_accents(self):
        assert normalize("U.S. FDA") == "u s fda"  # the period splits U and S
        assert normalize("dominance_theory") == "dominance theory"
        assert normalize("Hill's") == "hills"
        assert normalize("Fédération") == "federation"

    def test_singular_key(self):
        assert singular_key("American Pit Bull Terriers") == "american pit bull terrier"
        assert singular_key("pit bulls") == "pit bull"

    def test_initials_skip_stopwords(self):
        assert initials("American College of Veterinary Internal Medicine") == "acvim"
        assert initials("American Kennel Club") == "akc"


class TestMatchers:
    def test_normalized_equal(self):
        assert match_normalized("Pit Bull", "concept", "pit_bull", "concept")
        assert match_normalized("X", "concept", "Y", "concept") is None

    def test_plural(self):
        assert match_plural("American Pit Bull Terrier", "breed",
                            "American Pit Bull Terriers", "breed")
        # identical-normalized handled by the normalized matcher, not plural
        assert match_plural("pit bull", "concept", "pit_bull", "concept") is None

    def test_acronym_positive(self):
        assert match_acronym("AKC", "organization", "American Kennel Club", "organization")
        assert match_acronym("APBT", "concept", "American Pit Bull Terrier", "breed")

    def test_acronym_guard_blocks_lowercase_collision(self):
        """CDC (org) must NOT match 'canine dilated cardiomyopathy' even though
        its initials spell 'cdc' — the expansion is an all-lowercase common
        phrase, not a proper name."""
        assert initials("canine dilated cardiomyopathy") == "cdc"  # the collision
        assert match_acronym("CDC", "organization",
                             "canine dilated cardiomyopathy", "concept") is None
        assert match_acronym("cdc", "concept",
                             "canine dilated cardiomyopathy", "concept") is None

    def test_surname_requires_person(self):
        assert match_surname("schenkel", "concept", "Rudolf Schenkel", "person")
        assert match_surname("freeman", "concept", "Dr. Lisa Freeman", "person")
        # not a person -> no surname match
        assert match_surname("freeman", "concept", "Dr. Lisa Freeman", "concept") is None


class TestClustering:
    def test_transitive_union(self):
        """akc -> AKC (normalize) and AKC -> American Kennel Club (acronym)
        should yield a single cluster of all three."""
        ents = [
            {"label": "akc", "entity_type": "concept"},
            {"label": "AKC", "entity_type": "organization"},
            {"label": "American Kennel Club", "entity_type": "organization"},
        ]
        result = EntityResolver(ents).resolve()
        big = [c for c in result.clusters if len(c.members) == 3]
        assert len(big) == 1
        assert set(big[0].members) == {"akc", "AKC", "American Kennel Club"}
        assert big[0].canonical == "American Kennel Club"  # most tokens

    def test_distinct_entities_stay_separate(self):
        ents = [
            {"label": "Brucella canis", "entity_type": "concept"},
            {"label": "brucellosis", "entity_type": "concept"},
        ]
        result = EntityResolver(ents).resolve()
        assert all(len(c.members) == 1 for c in result.clusters)


class TestAgainstGold:
    def _gold(self):
        return json.loads((Path(__file__).parent.parent / "eval" / "er_gold.json").read_text())

    def _eval(self):
        from eval.er_metrics import bcubed, clusters_to_assignment
        gold_data = self._gold()
        coref = [c["members"] for c in gold_data["clusters"]]
        contrast = [c["members"] for c in gold_data["contrast"]]
        gold = clusters_to_assignment(coref)
        all_items = sorted(set(gold) | {m for g in contrast for m in g})

        result = EntityResolver(
            [{"label": i, "entity_type": ""} for i in all_items]
        ).resolve()
        predicted = {}
        for cid, c in enumerate(result.clusters):
            for m in c.members:
                predicted[m] = cid

        p, r, f1 = bcubed(predicted, gold)
        from eval.run_er_eval import count_merge_violations
        violations = count_merge_violations(predicted, coref + contrast)
        return p, r, f1, violations

    def test_recall_improves_over_slug_baseline(self):
        from eval.run_er_eval import slug_baseline_assignment
        from eval.er_metrics import bcubed, clusters_to_assignment
        coref = [c["members"] for c in self._gold()["clusters"]]
        gold = clusters_to_assignment(coref)
        _, base_r, base_f1 = bcubed(slug_baseline_assignment(list(gold)), gold)
        _, r, f1, _ = self._eval()
        assert r > base_r and f1 > base_f1

    def test_precision_held_and_no_violations(self):
        p, _, _, violations = self._eval()
        assert p == 1.0, "Phase A must stay high-precision"
        assert violations == [], f"must-not-merge pairs were merged: {violations}"

    def test_f1_in_expected_phase_a_band(self):
        _, _, f1, _ = self._eval()
        assert 0.80 <= f1 < 0.85, f"Phase A expected ~0.808, got {f1:.3f}"
