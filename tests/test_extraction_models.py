"""Tests for the canonical Pydantic extraction templates and their integration
at the extract.py parse boundary.

Covers:
  - Field validation + coercion (confidence clamp, type normalization)
  - Raw-LLM key acceptance via validation aliases (label/type)
  - meta.description lift
  - Fail-soft per-item validation in ExtractionResult.from_raw
  - Legacy-dict round-trip keys the downstream pipeline consumes
  - extract_triplets_from_text still returns the legacy dict contract after
    routing through the model (urllib mocked; no live LLM)
"""
import json
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from second_brain.models import ExtractedEdge, ExtractedEntity, ExtractionResult


class TestExtractedEntity:
    def test_accepts_raw_llm_keys(self):
        """The urllib prompt emits {label, type}; the model must accept them."""
        e = ExtractedEntity.model_validate({"label": "spaced repetition", "type": "Concept"})
        assert e.name == "spaced repetition"
        assert e.entity_type == "concept"  # normalized lower

    def test_accepts_canonical_keys(self):
        e = ExtractedEntity.model_validate({"name": "Anki", "entity_type": "tool"})
        assert e.name == "Anki"
        assert e.entity_type == "tool"

    def test_confidence_clamped_not_rejected(self):
        assert ExtractedEntity(name="x", confidence=5).confidence == 1.0
        assert ExtractedEntity(name="x", confidence=-2).confidence == 0.0
        assert ExtractedEntity(name="x", confidence="0.7").confidence == pytest.approx(0.7)
        # Non-numeric falls back to default rather than raising.
        assert ExtractedEntity(name="x", confidence="high").confidence == 0.5

    def test_empty_name_rejected(self):
        with pytest.raises(ValidationError):
            ExtractedEntity(name="")

    def test_meta_description_lifted(self):
        e = ExtractedEntity.model_validate(
            {"label": "flow", "type": "concept", "meta": {"description": "a focused state"}}
        )
        assert e.description == "a focused state"

    def test_method_and_tool_types_allowed(self):
        """Live ontology has method/tool — the model must NOT freeze them out
        (the stale-Literal regression we explicitly avoided)."""
        for t in ("method", "tool"):
            assert ExtractedEntity(name="x", entity_type=t).entity_type == t

    def test_legacy_dict_keys(self):
        e = ExtractedEntity(name="X", entity_type="concept", description="d", confidence=0.8)
        d = e.to_legacy_dict()
        assert d["label"] == "X"
        assert d["type"] == "concept"
        assert d["meta"]["description"] == "d"
        assert d["confidence"] == 0.8


class TestExtractedEdge:
    def test_accepts_raw_keys_and_normalizes_type(self):
        x = ExtractedEdge.model_validate(
            {"source": "a", "target": "b", "type": "supports", "evidence": "because reasons"}
        )
        assert x.edge_type == "SUPPORTS"  # upper-normalized
        assert x.source == "a" and x.target == "b"

    def test_implements_requires_allowed(self):
        """Live ontology edge types absent from the stale brief."""
        for t in ("IMPLEMENTS", "REQUIRES"):
            assert ExtractedEdge(source="a", target="b", edge_type=t).edge_type == t

    def test_missing_endpoint_rejected(self):
        with pytest.raises(ValidationError):
            ExtractedEdge(source="", target="b")

    def test_legacy_dict_keys(self):
        x = ExtractedEdge(source="a", target="b", edge_type="LEARNED_FROM", evidence="q", confidence=0.5)
        d = x.to_legacy_dict()
        assert d == {
            "source": "a", "target": "b", "type": "LEARNED_FROM",
            "evidence": "q", "confidence": 0.5, "extraction_tier": "llm",
        }


class TestExtractionResultFromRaw:
    def test_drops_invalid_items_keeps_valid(self):
        raw = {
            "entities": [
                {"label": "good", "type": "concept"},
                {"label": "", "type": "concept"},          # invalid: empty name
                {"type": "concept"},                         # invalid: no name
            ],
            "edges": [
                {"source": "a", "target": "b", "type": "SUPPORTS", "evidence": "x"},
                {"source": "a", "type": "SUPPORTS"},         # invalid: no target
            ],
        }
        result = ExtractionResult.from_raw(raw, source_id="doc1")
        assert len(result.entities) == 1
        assert result.entities[0].name == "good"
        assert len(result.edges) == 1
        assert result.source_id == "doc1"

    def test_preserves_error_contract(self):
        result = ExtractionResult.from_raw({"entities": [], "edges": [], "_error": "timeout"})
        assert result.error == "timeout"
        assert result.to_legacy_dict()["_error"] == "timeout"

    def test_legacy_roundtrip_shape(self):
        raw = {"entities": [{"label": "x", "type": "concept"}],
               "edges": [{"source": "x", "target": "y", "type": "PART_OF", "evidence": "ev"}]}
        out = ExtractionResult.from_raw(raw).to_legacy_dict()
        assert set(out.keys()) == {"entities", "edges"}
        assert out["entities"][0]["label"] == "x"
        assert out["edges"][0]["type"] == "PART_OF"

    def test_non_dict_input_is_safe(self):
        assert ExtractionResult.from_raw(None).entities == []


class TestExtractParseBoundary:
    """extract_triplets_from_text must still return the legacy dict contract
    after validating through the model. urllib is mocked — no live LLM."""

    def _fake_urlopen(self, payload_text):
        class _Resp:
            def __enter__(self_):
                return self_
            def __exit__(self_, *a):
                return False
            def read(self_):
                return json.dumps({"response": payload_text}).encode()
        return lambda *a, **k: _Resp()

    def test_returns_validated_legacy_dict(self):
        from second_brain import extract
        llm_json = json.dumps({
            "entities": [{"label": "memory", "type": "concept"}],
            "edges": [{"source": "memory", "target": "sleep", "type": "supports",
                       "evidence": "sleep consolidates memory", "confidence": 9}],
        })
        with patch.object(extract.urllib.request, "urlopen", self._fake_urlopen(llm_json)):
            out = extract.extract_triplets_from_text(
                "Sleep consolidates memory over time, studies show.",
                edge_types=["SUPPORTS"],
            )
        assert out["entities"][0]["label"] == "memory"
        # confidence 9 was clamped to 1.0 by the model, edge type upper-normalized
        assert out["edges"][0]["confidence"] == 1.0
        assert out["edges"][0]["type"] == "SUPPORTS"

    def test_malformed_json_returns_empty_legacy_shape(self):
        from second_brain import extract
        with patch.object(extract.urllib.request, "urlopen",
                          self._fake_urlopen("not json at all")):
            out = extract.extract_triplets_from_text("some text here that is long enough",
                                                     edge_types=["SUPPORTS"])
        assert out == {"entities": [], "edges": []}
