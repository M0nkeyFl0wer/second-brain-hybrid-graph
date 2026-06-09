"""
Unit tests for the three-phase extraction pipeline.

Tests cover:
  - Phase 1: deterministic date extraction
  - Phase 2: spaCy NER (person, org->source, location->place)
  - Entity ID generation (deterministic, type-differentiated)
  - Deduplication within a single extraction pass
"""

import pytest


@pytest.fixture
def extractor(ontology, mock_ollama):
    """Extractor instance with mocked Ollama (Phase 3 won't call real LLM)."""
    from second_brain.extract import Extractor

    return Extractor(ontology)


@pytest.mark.skip(
    reason="Phase-1 regex/deterministic extraction was removed "
    "in the 2026-04-08 refactor; extraction is now LLM-only "
    "(extract.py). No deterministic date/structure phase exists."
)
class TestPhase1Deterministic:
    """Test regex-based deterministic extraction (dates, structure)."""

    def test_phase1_dates_iso(self, extractor):
        """ISO date '2024-01-15' should produce an event entity."""
        result = extractor.extract_from_text("Meeting on 2024-01-15 at noon.")
        entities = result["entities"]
        date_entities = [e for e in entities if "2024-01-15" in e["label"]]
        assert len(date_entities) >= 1
        assert (
            date_entities[0]["entity_type"] == "event"
            or date_entities[0]["provenance"] == "deterministic"
        )

    def test_phase1_dates_natural(self, extractor):
        """Natural date 'January 15, 2024' should also be extracted."""
        result = extractor.extract_from_text("Due by January 15, 2024.")
        entities = result["entities"]
        date_entities = [e for e in entities if "January" in e["label"] and "2024" in e["label"]]
        assert len(date_entities) >= 1

    def test_phase1_no_false_positives(self, extractor):
        """Plain text without dates should not produce deterministic entities."""
        result = extractor.extract_from_text("This is normal text about nothing special.")
        # Phase 1 (deterministic) should find nothing; Phase 2 (spaCy) might
        # find entities, so we check that no 'deterministic' provenance entities exist
        deterministic = [e for e in result["entities"] if e["provenance"] == "deterministic"]
        assert len(deterministic) == 0


@pytest.mark.skip(
    reason="Phase-2 spaCy NER was removed in the 2026-04-08 "
    "refactor; extraction is now LLM-only (extract.py). No spaCy "
    "dependency or NER phase exists."
)
class TestPhase2SpaCy:
    """Test spaCy NER extraction with ontology type mapping."""

    def test_phase2_spacy_person(self, extractor):
        """spaCy should extract 'Albert Einstein' as a person entity."""
        result = extractor.extract_from_text("Albert Einstein developed the theory of relativity.")
        entities = result["entities"]
        person_entities = [e for e in entities if e["entity_type"] == "person"]
        labels = [e["label"] for e in person_entities]
        assert any(
            "Einstein" in label for label in labels
        ), f"Expected 'Einstein' in person entities, got: {labels}"

    def test_phase2_spacy_organization(self, extractor):
        """spaCy ORG label should map to 'source' in the PKG ontology."""
        result = extractor.extract_from_text(
            "The United Nations passed a resolution on climate change."
        )
        entities = result["entities"]
        source_entities = [e for e in entities if e["entity_type"] == "source"]
        labels = [e["label"] for e in source_entities]
        assert any(
            "United Nations" in label for label in labels
        ), f"Expected 'United Nations' in source entities, got: {labels}"

    def test_phase2_spacy_location(self, extractor):
        """spaCy GPE label should map to 'place' in the PKG ontology."""
        result = extractor.extract_from_text("I visited Tokyo last summer and it was amazing.")
        entities = result["entities"]
        place_entities = [e for e in entities if e["entity_type"] == "place"]
        labels = [e["label"] for e in place_entities]
        assert any(
            "Tokyo" in label for label in labels
        ), f"Expected 'Tokyo' in place entities, got: {labels}"


class TestEntityIdGeneration:
    """The canonical entity ID is a slug of the label.

    The post-refactor design keys entity identity on the LABEL only (id =
    slugify(label)), not a (label, type, source) hash — so the same concept
    referenced from different documents resolves to the same node, which is
    what lets cross-document edges connect. (The old 3-arg hash contract is
    gone by design.)
    """

    def test_generate_entity_id_deterministic(self):
        """Same label always produces the same ID."""
        from second_brain.extract import generate_entity_id

        assert generate_entity_id("spaced repetition") == generate_entity_id("spaced repetition")

    def test_generate_entity_id_is_slug(self):
        """ID is a lowercased underscore slug of the label."""
        from second_brain.extract import generate_entity_id

        assert generate_entity_id("Spaced Repetition!") == "spaced_repetition"

    def test_generate_entity_id_distinct_labels_differ(self):
        """Different labels produce different IDs."""
        from second_brain.extract import generate_entity_id

        assert generate_entity_id("meditation") != generate_entity_id("mindfulness")


@pytest.mark.skip(
    reason="Cross-mention dedup now happens at the ingest layer "
    "(ingest_obsidian.py 'seen' map), not in extract_from_text, "
    "and this test's mock_ollama fixture patches the 'ollama' "
    "package while the extractor calls urllib /api/generate. "
    "Covered behaviorally by the ingest path."
)
class TestDeduplication:
    """Test entity deduplication within a single extraction."""

    def test_dedup_within_extraction(self, extractor):
        """Text mentioning the same entity twice should deduplicate."""
        text = "Albert Einstein was brilliant. " "Albert Einstein changed physics forever."
        result = extractor.extract_from_text(text)
        # Count entities with 'Einstein' in label
        einstein_entities = [e for e in result["entities"] if "Einstein" in e["label"]]
        # Should be deduplicated to 1
        assert len(einstein_entities) == 1
