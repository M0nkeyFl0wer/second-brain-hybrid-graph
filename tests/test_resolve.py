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
        # not a person -> no surname match (this guards Montreal ↔ City of Montreal)
        assert match_surname("freeman", "concept", "Dr. Lisa Freeman", "concept") is None


class TestPhaseBMatchers:
    def test_acronym_subsequence(self):
        from second_brain.pipeline.resolve import match_acronym_subsequence
        # FDA is a subsequence of initials("U.S. Food and Drug Administration")="usfda"
        assert match_acronym_subsequence("FDA", "organization",
                                         "U.S. Food and Drug Administration", "organization")
        # but NOT of "FDA Center for Veterinary Medicine (CVM)" (no 'd' after 'f')
        assert match_acronym_subsequence("FDA", "organization",
                                         "FDA Center for Veterinary Medicine (CVM)",
                                         "organization") is None

    def test_legal_suffix(self):
        from second_brain.pipeline.resolve import match_legal_suffix
        assert match_legal_suffix("Hill's Pet Nutrition", "organization",
                                  "Hill's Pet Nutrition Inc.", "organization")
        # real-word difference is NOT a legal suffix
        assert match_legal_suffix("Hill's", "organization",
                                  "Hill's Pet Nutrition", "organization") is None

    def test_singularizer_keeps_latin_is_us(self):
        from second_brain.pipeline.resolve import _singularize
        assert _singularize("basis") == "basis"
        assert _singularize("canis") == "canis"
        assert _singularize("terriers") == "terrier"


class TestEmbeddingTier:
    def test_merges_near_same_type_not_far_or_incompatible(self):
        ents = [
            {"label": "Alsatian", "entity_type": "breed"},
            {"label": "German Shepherd", "entity_type": "breed"},
            {"label": "goldfish", "entity_type": "breed"},
            {"label": "Calgary", "entity_type": "location"},
        ]
        embs = {
            "Alsatian": [1.0, 0.0, 0.0],
            "German Shepherd": [0.99, 0.01, 0.0],   # near Alsatian, same type -> merge
            "goldfish": [0.0, 1.0, 0.0],            # far -> stays separate
            "Calgary": [0.98, 0.0, 0.0],            # near Alsatian but type location (distinct, specific)
        }
        result = EntityResolver(ents, embeddings=embs, embedding_threshold=0.92).resolve()
        groups = {frozenset(c.members) for c in result.clusters}
        assert frozenset({"Alsatian", "German Shepherd"}) in groups
        assert frozenset({"goldfish"}) in groups
        # breed vs location are distinct specific types -> never embedding-merged
        assert frozenset({"Calgary"}) in groups


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

    def _embeddings(self):
        path = Path(__file__).parent.parent / "eval" / "er_gold_embeddings.json"
        return json.loads(path.read_text()) if path.exists() else None

    def _eval(self, use_embeddings: bool):
        from eval.run_er_eval import (
            bcubed_pr_f1,
            clusters_to_assignment,
            count_merge_violations,
        )
        gold_data = self._gold()
        coref = [c["members"] for c in gold_data["clusters"]]
        contrast = [c["members"] for c in gold_data["contrast"]]
        types = gold_data["types"]
        gold = clusters_to_assignment(coref)
        all_items = sorted(set(gold) | {m for g in contrast for m in g})

        embeddings = self._embeddings() if use_embeddings else None
        result = EntityResolver(
            [{"label": i, "entity_type": types.get(i, "")} for i in all_items],
            embeddings=embeddings,
        ).resolve()
        predicted = {}
        for cid, c in enumerate(result.clusters):
            for m in c.members:
                predicted[m] = cid

        p, r, f1 = bcubed_pr_f1(gold, predicted)
        violations = count_merge_violations(predicted, coref + contrast)
        return p, r, f1, violations

    def test_recall_improves_over_slug_baseline(self):
        from eval.run_er_eval import (
            bcubed_pr_f1,
            clusters_to_assignment,
            slug_baseline_assignment,
        )
        coref = [c["members"] for c in self._gold()["clusters"]]
        gold = clusters_to_assignment(coref)
        _, base_r, base_f1 = bcubed_pr_f1(gold, slug_baseline_assignment(list(gold)))
        _, r, f1, _ = self._eval(use_embeddings=False)
        assert r > base_r and f1 > base_f1

    def test_deterministic_floor_high_precision(self):
        """Deterministic-only: high precision, no violations, ~0.83 band."""
        p, _, f1, violations = self._eval(use_embeddings=False)
        assert p == 1.0
        assert violations == []
        assert 0.80 <= f1 < 0.85

    def test_full_resolver_meets_target(self):
        """Deterministic + embedding tier (gold sidecar vectors @ DEDUP_THRESHOLD)
        clears F1 0.85 with precision held and zero must-not-merge violations."""
        if self._embeddings() is None:
            import pytest
            pytest.skip("gold embedding sidecar not present")
        p, _, f1, violations = self._eval(use_embeddings=True)
        assert p == 1.0, "embedding tier must not cost precision at the 0.92 cliff"
        assert violations == [], f"must-not-merge pairs were merged: {violations}"
        assert f1 >= 0.85, f"expected >= 0.85 (got {f1:.3f})"
