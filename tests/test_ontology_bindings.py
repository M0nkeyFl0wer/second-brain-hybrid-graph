"""Reference-impl tests for the two ontology<->grader bindings (RFC v3):
competency-question edge coverage and resolution identity criteria.

These are pure, local, deterministic checks over class attributes — no corpus,
no LLM, no graph. They are the design-time half of the RFC.
"""
from types import SimpleNamespace

from second_brain.ontology_kg_common import SecondBrainOntology


def test_edge_type_coverage_finds_the_real_ghost_set():
    """The inverse check flags exactly the five declared-but-unserved DOMAIN
    edge types. This is the set hand-counting got wrong by three in RFC v1/v2
    (missed IMPLEMENTS/REQUIRES, wrongly kept ASSOCIATED_WITH)."""
    cov = SecondBrainOntology().edge_type_coverage()
    assert cov["served"] == {"LEARNED_FROM", "CONFLICTS_WITH", "PRACTICED_IN",
                             "ASKED_ABOUT", "ANSWERS"}
    assert cov["ghost"] == {"INSPIRED_BY", "SUPPORTS", "PART_OF",
                            "IMPLEMENTS", "REQUIRES"}
    # ASSOCIATED_WITH is structural, not a domain edge — excluded from all buckets.
    allbuckets = cov["served"] | cov["discovery"] | cov["ghost"]
    assert "ASSOCIATED_WITH" not in allbuckets


def test_no_undefined_cq_references():
    """Every competency question references only declared types."""
    assert SecondBrainOntology().undefined_cq_references() == {}


def test_identity_key_uses_declared_criterion():
    o = SecondBrainOntology()
    # person -> keyed by label (the shared-universal default)
    person = SimpleNamespace(entity_type="person", label="Donella Meadows",
                             source_url="", properties={})
    assert o.identity_key(person) == ("Donella Meadows",)
    # source -> keyed by URL, NOT its display label (same source cited two ways
    # -> one node)
    src = SimpleNamespace(entity_type="source", label="Thinking in Systems",
                          source_url="https://example.org/tis", properties={})
    assert o.identity_key(src) == ("https://example.org/tis",)


def test_identity_key_none_falls_back_to_label():
    """A type with no declared criterion returns None -> resolver uses label."""
    o = SecondBrainOntology()
    concept = SimpleNamespace(entity_type="concept", label="feedback loops",
                              source_url="", properties={})
    assert o.identity_key(concept) is None
