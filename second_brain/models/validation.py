"""Structured validation output using SHACL report vocabulary — no pyshacl.

When the writer rejects an entity/edge (unknown type) or a lint pass finds a
missing/short evidence quote, it emits a `ValidationViolation` whose field names
mirror SHACL's ValidationResult (`sh:focusNode`, `sh:resultPath`,
`sh:sourceConstraintComponent`, `sh:resultMessage`, `sh:resultSeverity`). The
rejection log is therefore machine-readable by anyone who knows SHACL, with NO
pyshacl dependency. The Python validation logic is unchanged — only the output
format is standardized.

We steal the SHACL *report shape*, not the SHACL engine. See
https://www.w3.org/TR/shacl/#validation-report.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:  # avoid a runtime import cycle / hard dep on the ontology here
    from .extraction import ExtractionResult

Severity = Literal["violation", "warning", "info"]

# SHACL severity IRIs, for `to_shacl_dict()`.
_SEVERITY_IRI = {
    "violation": "sh:Violation",
    "warning": "sh:Warning",
    "info": "sh:Info",
}

# Minimum verbatim-evidence length (ONTOLOGY.md): edges should justify
# themselves with a >=10-char source quote. A shortfall is a warning, not a
# hard rejection — the edge still writes.
MIN_EVIDENCE_LEN = 10
# Edge types for which evidence matters most (belief-structure assertions).
_EVIDENCE_CRITICAL = frozenset({"SUPPORTS", "CONFLICTS_WITH"})


class ValidationViolation(BaseModel):
    """One SHACL-vocabulary validation result."""

    model_config = ConfigDict(str_strip_whitespace=True)

    focus_node: str = Field(description="sh:focusNode — the entity or edge ID that failed")
    result_path: str = Field(description="sh:resultPath — the property that failed")
    source_constraint: str = Field(
        description="sh:sourceConstraintComponent — which constraint was violated"
    )
    result_message: str = Field(description="sh:resultMessage — human-readable explanation")
    severity: Severity = "violation"

    def to_shacl_dict(self) -> dict[str, str]:
        """Emit with the actual `sh:`-prefixed keys, for a machine-readable log."""
        return {
            "sh:focusNode": self.focus_node,
            "sh:resultPath": self.result_path,
            "sh:sourceConstraintComponent": self.source_constraint,
            "sh:resultMessage": self.result_message,
            "sh:resultSeverity": _SEVERITY_IRI[self.severity],
        }


class ValidationReport(BaseModel):
    """SHACL ValidationReport: `sh:conforms` + the list of `sh:result`s."""

    conforms: bool = Field(description="sh:conforms — true iff there are no violation-severity results")
    results: list[ValidationViolation] = Field(default_factory=list)

    @classmethod
    def from_violations(cls, violations: list[ValidationViolation]) -> "ValidationReport":
        conforms = not any(v.severity == "violation" for v in violations)
        return cls(conforms=conforms, results=list(violations))

    def to_shacl_dict(self) -> dict[str, Any]:
        return {
            "sh:conforms": self.conforms,
            "sh:result": [v.to_shacl_dict() for v in self.results],
        }


# --------------------------------------------------------------------------- #
# Builders — turn a rejection into a violation. The write path / lint pass call
# these so the rejection vocabulary lives in one place.
# --------------------------------------------------------------------------- #


def unknown_entity_type(entity_id: str, entity_type: str) -> ValidationViolation:
    return ValidationViolation(
        focus_node=entity_id or "<unknown>",
        result_path="entity_type",
        source_constraint="sh:InConstraintComponent",
        result_message=f"entity_type '{entity_type}' is not in the ontology NODE_TYPES",
        severity="violation",
    )


def unknown_edge_type(edge_key: str, edge_type: str) -> ValidationViolation:
    return ValidationViolation(
        focus_node=edge_key,
        result_path="edge_type",
        source_constraint="sh:InConstraintComponent",
        result_message=f"edge_type '{edge_type}' is not in the ontology EDGE_TYPES",
        severity="violation",
    )


def grade_violation(
    edge_key: str, edge_type: str, src_type: str, tgt_type: str
) -> ValidationViolation:
    """Edge rejected because its endpoint types violate the ontology's
    domain/range (grade locality, EDGE_DOMAIN_RANGE)."""
    return ValidationViolation(
        focus_node=edge_key,
        result_path="edge_type",
        source_constraint="sh:ClassConstraintComponent",
        result_message=(
            f"grade violation: {edge_type} does not accept "
            f"{src_type or '<unknown>'} -> {tgt_type or '<unknown>'} "
            f"(not in ontology EDGE_DOMAIN_RANGE)"
        ),
        severity="violation",
    )


def missing_evidence(edge_key: str, edge_type: str, length: int) -> ValidationViolation:
    return ValidationViolation(
        focus_node=edge_key,
        result_path="evidence",
        source_constraint="sh:MinLengthConstraintComponent",
        result_message=(
            f"{edge_type} evidence is {length} chars; "
            f">={MIN_EVIDENCE_LEN} expected for a verbatim source quote"
        ),
        severity="warning",
    )


def edge_key(source: str, edge_type: str, target: str) -> str:
    """Canonical focus-node string for an edge: `source -[TYPE]-> target`."""
    return f"{source} -[{edge_type}]-> {target}"


def check_extraction(result: "ExtractionResult", ontology: Any) -> ValidationReport:
    """Lint an ExtractionResult against an ontology, returning a SHACL report.

    Checks (no graph writes):
      - entity_type ∈ NODE_TYPES                         → violation
      - edge_type ∈ EDGE_TYPES ∪ structural fallback     → violation
      - evidence length on belief-structure edges        → warning

    Pure and side-effect-free — use it as a pre-write lint or a post-extraction
    quality gate.
    """
    violations: list[ValidationViolation] = []

    node_types = set(getattr(ontology, "NODE_TYPES", set()) or set())
    for ent in result.entities:
        # mirror the write-time check, which lowercases
        if ent.entity_type.lower() not in node_types:
            violations.append(unknown_entity_type(ent.name, ent.entity_type))

    for edge in result.edges:
        key = edge_key(edge.source, edge.edge_type, edge.target)
        if not ontology.validate_edge_type(edge.edge_type):
            violations.append(unknown_edge_type(key, edge.edge_type))
        if edge.edge_type in _EVIDENCE_CRITICAL and len(edge.evidence.strip()) < MIN_EVIDENCE_LEN:
            violations.append(missing_evidence(key, edge.edge_type, len(edge.evidence.strip())))

    return ValidationReport.from_violations(violations)
