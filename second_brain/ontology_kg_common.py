"""SecondBrainOntology — kg-common Ontology ABC subclass for open-second-brain.

The original `second_brain.ontology` module exposes the type sets as
module-level frozensets and helper functions (`normalize_node_type`,
`validate_edge`, `slugify`, `extraction_prompt_fragment`,
`node_type_prompt_fragment`). At some point an `Ontology` class was
referenced from 11 callsites but the class itself disappeared from
`ontology.py` — leaving every script and the test suite in a
broken-import state.

This module ships the class as a kg-common Ontology subclass so:

  - All 11 broken-import callsites work again (via the
    `from .ontology_kg_common import SecondBrainOntology as Ontology`
    alias appended to `second_brain/ontology.py`).
  - The shared-substrate Ontology ABC is adopted — this project subclasses
    `kg_common.ontology.Ontology`, proving the ABC is reusable across
    infrastructure-type knowledge graphs.

Module-level constants (`NODE_TYPES`, `EDGE_TYPES`, `EDGE_DOMAIN_RANGE`,
`TYPE_ALIASES`) stay in `second_brain/ontology.py` for `scripts/enrich.py`
and any other importer of `slugify` / `validate_edge` (module-level
functions kept there for backward compat).
"""
from __future__ import annotations

from itertools import product

from kg_common.ontology.base import Ontology

from second_brain.ontology import (
    EDGE_TYPES as _EDGE_TYPES,
    NODE_TYPES as _NODE_TYPES,
    TYPE_ALIASES as _TYPE_ALIASES,
)


# Edge domain/range — converted from the original `(domain_set, range_set)`
# tuple form to kg-common's `list[(src, tgt)]` cartesian form. Only the
# *constrained* edges go in the map; unconstrained ones (where both sides
# accept any NODE_TYPE) are omitted so the base class's `validate_grade`
# returns True by default (faster + clearer than enumerating a 10x10 table).
_PRACTICE_SRC = {"practice", "method", "tool"}
_IMPLEMENTS_SRC = {"tool", "method"}

_EDGE_DOMAIN_RANGE: dict[str, list[tuple[str, str]]] = {
    "PRACTICED_IN": list(product(_PRACTICE_SRC, _NODE_TYPES)),
    "ASKED_ABOUT":  list(product({"question"}, _NODE_TYPES)),
    "ANSWERS":      list(product(_NODE_TYPES, {"question"})),
    "IMPLEMENTS":   list(product(_IMPLEMENTS_SRC, _NODE_TYPES)),
}


class SecondBrainOntology(Ontology):
    """Ontology for open-second-brain — triplet-first entity/edge schema.

    Inherits the kg-common ABC surface (`validate_entity_type`,
    `validate_edge_type`, `validate_grade`, `entity_field_schema`,
    `edge_field_schema`, `schema_ddl`, `extraction_prompt_fragment`).
    Field schemas use kg-common defaults (which include the bi-temporal
    trio); the open-second-brain writer (`second_brain/graph.py`) maintains
    its own custom DDL with FLOAT[768] embedding columns and hypergraph
    EdgeNode/CommunityMeta tables, so `schema_ddl()` is informational here
    — the live writer doesn't consume it yet.

    Constructor accepts an optional `path` argument that the legacy class
    used to parse an `ONTOLOGY.md` file. The types are now declared
    statically via the frozensets above; the path is accepted for
    backward compatibility with `tests/conftest.py` (which does
    `Ontology(str(ONTOLOGY_md_path))`) but is otherwise ignored.
    """

    NODE_TYPES = _NODE_TYPES
    EDGE_TYPES = _EDGE_TYPES
    EDGE_DOMAIN_RANGE = _EDGE_DOMAIN_RANGE
    TYPE_ALIASES = _TYPE_ALIASES
    VERSION = "second-brain-1.0"

    def __init__(self, path: str | None = None) -> None:
        self._source_path = path

    def extraction_prompt_fragment(self) -> str:
        """Project-specific extraction prompt — keeps the evidence-quote
        requirement and the deterministic/NLP/LLM confidence ladder that
        the legacy `extraction_prompt_fragment()` in
        `second_brain/ontology.py` enforced. Re-declared here so callers
        that pass the ontology object (rather than importing the module
        function) get the same text."""
        edge_lines = []
        for etype in sorted(self.EDGE_TYPES):
            pairs = self.EDGE_DOMAIN_RANGE.get(etype)
            if pairs is None:
                edge_lines.append(f"    - {etype} (any → any)")
            else:
                sources = sorted({s for s, _ in pairs})
                targets = sorted({t for _, t in pairs})
                edge_lines.append(
                    f"    - {etype} (source: {sources} → target: {targets})"
                )
        return "\n".join([
            "Edge types (all require verbatim evidence quote):",
            *edge_lines,
            "",
            "Rules:",
            "  - Every edge MUST have evidence (exact quote from text, min 10 chars)",
            "  - Confidence: 0.9 deterministic / 0.7 NLP / 0.5 LLM",
            "  - Use exact entity labels from text, don't invent names",
            "  - Extract CONFLICTS_WITH and SUPPORTS when beliefs contrast/reinforce",
        ])
