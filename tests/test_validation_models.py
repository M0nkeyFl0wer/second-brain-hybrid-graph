"""Tests for the SHACL-vocabulary ValidationViolation/Report models, the
check_extraction lint pass, and the graph write-path wiring."""

from second_brain.models import (
    ExtractedEdge,
    ExtractedEntity,
    ExtractionResult,
    ValidationReport,
    ValidationViolation,
    check_extraction,
)
from second_brain.models import validation as v


class TestValidationViolation:
    def test_shacl_dict_keys(self):
        viol = ValidationViolation(
            focus_node="anki",
            result_path="entity_type",
            source_constraint="sh:InConstraintComponent",
            result_message="nope",
            severity="violation",
        )
        d = viol.to_shacl_dict()
        assert d["sh:focusNode"] == "anki"
        assert d["sh:resultPath"] == "entity_type"
        assert d["sh:sourceConstraintComponent"] == "sh:InConstraintComponent"
        assert d["sh:resultSeverity"] == "sh:Violation"

    def test_severity_iri_mapping(self):
        assert v.missing_evidence("a -[SUPPORTS]-> b", "SUPPORTS", 3).to_shacl_dict()[
            "sh:resultSeverity"
        ] == "sh:Warning"


class TestValidationReport:
    def test_conforms_true_when_only_warnings(self):
        report = ValidationReport.from_violations([
            v.missing_evidence("a -[SUPPORTS]-> b", "SUPPORTS", 2),
        ])
        assert report.conforms is True

    def test_conforms_false_with_a_violation(self):
        report = ValidationReport.from_violations([
            v.unknown_edge_type("a -[FOO]-> b", "FOO"),
        ])
        assert report.conforms is False

    def test_shacl_report_shape(self):
        report = ValidationReport.from_violations([v.unknown_entity_type("x", "widget")])
        d = report.to_shacl_dict()
        assert d["sh:conforms"] is False
        assert isinstance(d["sh:result"], list) and len(d["sh:result"]) == 1


class TestCheckExtraction:
    def _ontology(self):
        from second_brain.ontology import Ontology
        return Ontology()

    def test_clean_extraction_conforms(self):
        result = ExtractionResult(
            entities=[ExtractedEntity(name="memory", entity_type="concept")],
            edges=[ExtractedEdge(source="memory", target="sleep", edge_type="SUPPORTS",
                                 evidence="sleep consolidates memory")],
        )
        report = check_extraction(result, self._ontology())
        assert report.conforms is True
        assert report.results == []

    def test_unknown_entity_type_is_violation(self):
        result = ExtractionResult(entities=[ExtractedEntity(name="x", entity_type="widget")])
        report = check_extraction(result, self._ontology())
        assert report.conforms is False
        assert report.results[0].result_path == "entity_type"

    def test_method_tool_implements_requires_conform(self):
        """Live-ontology types the stale brief omitted must lint clean."""
        result = ExtractionResult(
            entities=[
                ExtractedEntity(name="Obsidian", entity_type="tool"),
                ExtractedEntity(name="causal inference", entity_type="method"),
            ],
            edges=[
                ExtractedEdge(source="Obsidian", target="linking", edge_type="IMPLEMENTS",
                              evidence="Obsidian implements bidirectional linking"),
                ExtractedEdge(source="pandas", target="numpy", edge_type="REQUIRES",
                              evidence="pandas requires numpy"),
            ],
        )
        report = check_extraction(result, self._ontology())
        assert report.conforms is True

    def test_short_evidence_on_supports_is_warning_not_violation(self):
        result = ExtractionResult(
            edges=[ExtractedEdge(source="a", target="b", edge_type="SUPPORTS", evidence="x")],
        )
        report = check_extraction(result, self._ontology())
        assert report.conforms is True  # warning only
        assert report.results[0].severity == "warning"
        assert report.results[0].result_path == "evidence"


class TestGraphWiring:
    def test_bulk_add_entities_records_violations(self, graph):
        n = graph.bulk_add_entities([
            {"id": "good", "entity_type": "concept", "label": "Good"},
            {"id": "bad", "entity_type": "widget", "label": "Bad"},
        ])
        assert n == 1  # only the valid one written; count contract unchanged
        assert len(graph.last_violations) == 1
        assert graph.last_violations[0].focus_node == "bad"
        assert graph.last_violations[0].result_path == "entity_type"

    def test_bulk_add_edges_records_violations(self, graph):
        graph.bulk_add_entities([
            {"id": "a", "entity_type": "concept", "label": "A"},
            {"id": "b", "entity_type": "concept", "label": "B"},
        ])
        graph.last_violations = []
        n = graph.bulk_add_edges([
            {"source_id": "a", "target_id": "b", "edge_type": "SUPPORTS"},
            {"source_id": "a", "target_id": "b", "edge_type": "BOGUS"},
        ])
        assert n == 1
        assert len(graph.last_violations) == 1
        assert graph.last_violations[0].result_path == "edge_type"
        assert "BOGUS" in graph.last_violations[0].result_message
