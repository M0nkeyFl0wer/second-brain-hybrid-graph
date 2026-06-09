"""Canonical Pydantic templates for extraction output.

These models ARE the templates for every extraction path. They standardize the
*raw* extraction shape — entity/edge as the model first sees it, BEFORE
id-resolution and enrichment in `Extractor.extract_from_text`. They serve three
purposes at once (per the canonicalization brief):

  1. Schema validation   — field types, ranges, and required fields are checked
                            on every parse, for the urllib backends and the
                            optional Instructor backend alike.
  2. Standardized shape   — deterministic / nlp / llm tiers all return this.
  3. Cardinality limits   — confidence is clamped to [0, 1]; extraction_tier is
                            a closed set.

Design decisions (see the session notes):

* **No hardcoded vocabulary Literal.** `entity_type` / `edge_type` are plain
  strings here, NOT `Literal[...]`. The active ontology (`second_brain.ontology`
  or a `--ontology path.yaml`) is the single source of truth for which types
  exist, and it enforces membership at WRITE time (`graph.add_entity`,
  `bulk_add_entities`, `bulk_add_edges`). Freezing a Literal here would (a) drift
  from `ontology.py` — exactly the staleness that ONTOLOGY.md already shows — and
  (b) reject any custom YAML ontology. Vocabulary belongs to the ontology; shape
  belongs here.

* **Fail-soft, per-item.** `ExtractionResult.from_raw` validates each entity/edge
  independently and drops only the invalid ones, mirroring the pipeline's
  existing "drop edges whose endpoints don't resolve" behavior. One malformed
  edge must not discard a whole chunk's extraction.

* **Confidence is clamped, not rejected.** Local 3B models routinely emit
  out-of-range or non-numeric confidence. Clamping to [0, 1] (rather than raising)
  keeps an otherwise-good entity instead of dropping it on a cosmetic field.

* **Evidence length is NOT enforced here.** ONTOLOGY.md asks for >=10-char
  verbatim evidence on SUPPORTS / CONFLICTS_WITH. Enforcing it as a hard
  field constraint would atomically fail an Instructor result or silently drop
  edges. It is better surfaced as a `warning`-severity ValidationViolation
  (SHACL-vocabulary report) — that is Task 4, out of this session's core scope.

Vocabulary field docs use SKOS terms (prefLabel / altLabel). No rdflib
dependency is taken — the vocabulary is stolen, not imported.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

logger = logging.getLogger(__name__)

# Which extraction tier produced a row. Confidence ladder (per ONTOLOGY.md):
# 0.9 deterministic / 0.7 nlp / 0.5 llm.
ExtractionTier = Literal["deterministic", "nlp", "llm"]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _clamp_confidence(v: Any) -> float:
    """Coerce a model-supplied confidence into [0, 1]. Non-numeric → 0.5."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 0.5
    if f < 0.0:
        return 0.0
    if f > 1.0:
        return 1.0
    return f


class ExtractedEntity(BaseModel):
    """Canonical shape for every entity produced by any extraction tier.

    Accepts both the canonical field names (`name`, `entity_type`) and the raw
    LLM-prompt keys (`label`, `type`) via validation aliases, so the existing
    urllib prompt — which asks for `label`/`type` — validates without a prompt
    rewrite, while Instructor (which drives the schema from the field names) also
    works.
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str = Field(
        validation_alias=AliasChoices("name", "label"),
        min_length=1,
        description="Canonical entity label (SKOS prefLabel)",
    )
    entity_type: str = Field(
        default="concept",
        validation_alias=AliasChoices("entity_type", "type"),
        description=(
            "Ontology NODE_TYPE. Membership is validated against the active "
            "ontology at write time, not frozen as a Literal here."
        ),
    )
    aliases: list[str] = Field(
        default_factory=list,
        description="Alternative surface forms (SKOS altLabel)",
    )
    description: str = Field(
        default="",
        description="One-sentence description grounded in source text",
    )
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="0.9 deterministic / 0.7 nlp / 0.5 llm (clamped to [0,1])",
    )
    evidence: str = Field(
        default="",
        description="Source text span that justifies this extraction",
    )
    extraction_tier: ExtractionTier = "llm"

    @model_validator(mode="before")
    @classmethod
    def _lift_meta_description(cls, data: Any) -> Any:
        """Raw LLM entities carry description under `meta.description`; lift it
        to the top-level field when a top-level description isn't already set."""
        if isinstance(data, dict) and not data.get("description"):
            meta = data.get("meta")
            if isinstance(meta, dict) and meta.get("description"):
                data = {**data, "description": meta["description"]}
        return data

    @field_validator("confidence", mode="before")
    @classmethod
    def _coerce_confidence(cls, v: Any) -> float:
        return _clamp_confidence(v)

    @field_validator("entity_type")
    @classmethod
    def _normalize_type(cls, v: str) -> str:
        # Node types are lower_snake by convention; normalize so the write-time
        # ontology check (which lowercases) sees a consistent form.
        return (v or "concept").strip().lower() or "concept"

    def to_legacy_dict(self) -> dict[str, Any]:
        """The raw extraction dict shape that `Extractor.extract_from_text` and
        `scripts/enrich.py` consume: keys `label`, `type`, `meta.description`,
        `confidence`. Extra canonical fields ride along harmlessly."""
        return {
            "label": self.name,
            "type": self.entity_type,
            "meta": {"description": self.description},
            "description": self.description,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "aliases": list(self.aliases),
            "extraction_tier": self.extraction_tier,
        }


class ExtractedEdge(BaseModel):
    """Canonical shape for every edge produced by any extraction tier."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    source: str = Field(min_length=1, description="Source entity canonical name")
    target: str = Field(min_length=1, description="Target entity canonical name")
    edge_type: str = Field(
        default="ASSOCIATED_WITH",
        validation_alias=AliasChoices("edge_type", "type"),
        description=(
            "Ontology EDGE_TYPE, or the structural fallback ASSOCIATED_WITH. "
            "Membership is validated against the active ontology at write time."
        ),
    )
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence: str = Field(
        default="",
        description="Verbatim source text justifying this relationship",
    )
    extraction_tier: ExtractionTier = "llm"

    @field_validator("confidence", mode="before")
    @classmethod
    def _coerce_confidence(cls, v: Any) -> float:
        return _clamp_confidence(v)

    @field_validator("edge_type")
    @classmethod
    def _normalize_type(cls, v: str) -> str:
        # Edge types are UPPER_SNAKE by convention.
        return (v or "ASSOCIATED_WITH").strip().upper() or "ASSOCIATED_WITH"

    def to_legacy_dict(self) -> dict[str, Any]:
        """Raw extraction edge shape: keys `source`, `target`, `type`,
        `evidence`, `confidence`."""
        return {
            "source": self.source,
            "target": self.target,
            "type": self.edge_type,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "extraction_tier": self.extraction_tier,
        }


class ExtractionResult(BaseModel):
    """Complete validated extraction output for one document or chunk."""

    model_config = ConfigDict(populate_by_name=True)

    entities: list[ExtractedEntity] = Field(default_factory=list)
    edges: list[ExtractedEdge] = Field(default_factory=list)
    source_id: str = Field(default="", description="Document or chunk ID")
    extracted_at: datetime = Field(default_factory=_utcnow)
    # Preserves the fail-loud `_error` contract: a backend failure (timeout,
    # auth, connection) is carried here so the ingest can refuse to declare
    # success on a degraded run rather than silently producing a 0-edge graph.
    error: str | None = Field(default=None)

    @classmethod
    def from_raw(cls, raw: dict[str, Any], source_id: str = "") -> "ExtractionResult":
        """Validate a raw `{entities, edges, _error?}` dict into the canonical
        shape, dropping (and logging) any item that fails validation. This is the
        fail-soft parse boundary used by both urllib extraction backends."""
        if not isinstance(raw, dict):
            return cls(source_id=source_id)

        entities: list[ExtractedEntity] = []
        dropped_e = 0
        for item in raw.get("entities") or []:
            try:
                entities.append(ExtractedEntity.model_validate(item))
            except ValidationError as ex:
                dropped_e += 1
                logger.debug("dropped entity (schema-invalid): %s — %s", item, ex)

        edges: list[ExtractedEdge] = []
        dropped_x = 0
        for item in raw.get("edges") or []:
            try:
                edges.append(ExtractedEdge.model_validate(item))
            except ValidationError as ex:
                dropped_x += 1
                logger.debug("dropped edge (schema-invalid): %s — %s", item, ex)

        if dropped_e or dropped_x:
            logger.info(
                "extraction validation dropped %d entit%s, %d edge%s",
                dropped_e,
                "y" if dropped_e == 1 else "ies",
                dropped_x,
                "" if dropped_x == 1 else "s",
            )

        return cls(
            entities=entities,
            edges=edges,
            source_id=source_id,
            error=raw.get("_error"),
        )

    def to_legacy_dict(self) -> dict[str, Any]:
        """Serialize back to the raw extraction dict shape the functional API
        contract returns: `{entities: [...], edges: [...], _error?: str}`."""
        out: dict[str, Any] = {
            "entities": [e.to_legacy_dict() for e in self.entities],
            "edges": [x.to_legacy_dict() for x in self.edges],
        }
        if self.error:
            out["_error"] = self.error
        return out
