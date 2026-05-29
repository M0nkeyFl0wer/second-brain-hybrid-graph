"""Phase 5.2 parity test — open-second-brain against kg-common HEAD.

Three things pinned:

1. The legacy `Ontology` name resolves again (was broken across 11
   callsites after the class was removed from `second_brain/ontology.py`;
   now re-aliased to `SecondBrainOntology` at the bottom of that file).
2. SecondBrainOntology satisfies the kg-common Ontology ABC surface —
   every method the writer calls returns a sensible value.
3. The bi-temporal opt-in value for SecondBrainOntology is locked.
   Currently True (inherits DEFAULT_EDGE_FIELDS from the vendored
   `second_brain.ontology_base`, no override).

The base ABC was vendored from kg-common into `second_brain.ontology_base`
to drop the private dependency, so conformance is now checked against the
vendored base (no external package required).
"""
from __future__ import annotations

import pytest


# ----------------------------------------------------------------------
# Broken-import repair: Ontology resolves from second_brain.ontology
# ----------------------------------------------------------------------


def test_legacy_ontology_import_resolves():
    """The 11 callsites that do `from second_brain.ontology import Ontology`
    were broken because the class had been removed. The bottom-of-file
    alias points the name at SecondBrainOntology now."""
    from second_brain.ontology import Ontology
    from second_brain.ontology_kg_common import SecondBrainOntology

    assert Ontology is SecondBrainOntology


def test_legacy_ontology_constructs_with_no_args():
    """Most callsites do `Ontology()` — no path arg."""
    from second_brain.ontology import Ontology

    ont = Ontology()
    assert ont is not None
    assert len(ont.NODE_TYPES) == 10
    assert len(ont.EDGE_TYPES) == 10


def test_legacy_ontology_constructs_with_path_arg():
    """tests/conftest.py does `Ontology(str(dst))` with an ONTOLOGY.md
    path. The legacy class parsed the markdown; the new class accepts
    the path for backward compat and ignores it (types are static)."""
    from second_brain.ontology import Ontology

    ont = Ontology("/nonexistent/ONTOLOGY.md")
    assert ont is not None
    assert ont.NODE_TYPES  # still populated from static frozensets


# ----------------------------------------------------------------------
# ABC conformance — every method the writer calls returns sanely
# ----------------------------------------------------------------------


def test_second_brain_ontology_satisfies_abc():
    from second_brain.ontology_base import Ontology as AbcOntology
    from second_brain.ontology_kg_common import SecondBrainOntology

    ont = SecondBrainOntology()
    assert isinstance(ont, AbcOntology)

    # NODE_TYPES + EDGE_TYPES are the project's frozensets, not empty defaults
    assert "concept" in ont.NODE_TYPES
    assert "LEARNED_FROM" in ont.EDGE_TYPES

    # validate_entity_type — accept known, reject garbage
    assert ont.validate_entity_type("concept") is True
    assert ont.validate_entity_type("NOT_A_REAL_TYPE_XYZ") is False

    # validate_edge_type — same shape
    assert ont.validate_edge_type("LEARNED_FROM") is True
    assert ont.validate_edge_type("NOT_AN_EDGE_TYPE_XYZ") is False

    # validate_grade — constrained edge
    assert ont.validate_grade("PRACTICED_IN", "practice", "project") is True
    assert ont.validate_grade("ASKED_ABOUT", "question", "concept") is True
    # Unconstrained edge: no entry in EDGE_DOMAIN_RANGE → base returns True
    assert ont.validate_grade("LEARNED_FROM", "concept", "source") is True
    # Domain violation on constrained edge
    assert ont.validate_grade("ASKED_ABOUT", "concept", "question") is False

    # extraction_prompt_fragment — non-empty + mentions a real edge type
    frag = ont.extraction_prompt_fragment()
    assert isinstance(frag, str)
    assert "LEARNED_FROM" in frag
    assert "evidence" in frag.lower()  # rules block preserved

    # schema_ddl — returns a non-empty list of DDL strings (informational
    # here; the live writer uses its own custom DDL).
    ddl = ont.schema_ddl()
    assert isinstance(ddl, list) and len(ddl) > 0


# ----------------------------------------------------------------------
# Lock-in: bi-temporal opt-in value
# ----------------------------------------------------------------------


def test_second_brain_temporal_optin_value_locked():
    """SecondBrainOntology does not override edge_field_schema(), so it
    inherits DEFAULT_EDGE_FIELDS from kg_common.ontology.base. Those
    defaults include the bi-temporal trio.

    If this assertion fails, kg-common's default has been changed and
    every open-second-brain edge has silently flipped opt-in status.
    Investigate before updating this test."""
    from second_brain.ontology_kg_common import SecondBrainOntology

    fields = SecondBrainOntology().edge_field_schema()
    assert "valid_at_ms" in fields
    assert "invalid_at_ms" in fields
    assert "expired_at_ms" in fields


# ----------------------------------------------------------------------
# Type aliases — legacy normalization still works on the new class
# ----------------------------------------------------------------------


def test_type_aliases_normalize_via_abc():
    """The frozensets and TYPE_ALIASES come from second_brain/ontology.py
    via re-export; the base class's normalize_node_type uses them."""
    from second_brain.ontology_kg_common import SecondBrainOntology

    ont = SecondBrainOntology()
    assert ont.normalize_node_type("idea") == "concept"
    assert ont.normalize_node_type("people") == "person"
    assert ont.normalize_node_type("software") == "tool"
    assert ont.normalize_node_type("NOT_A_THING") is None
