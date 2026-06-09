"""Load an ontology from a YAML file — make the schema a config, not a constant.

The built-in `SecondBrainOntology` is the default. But a knowledge-graph
template should let you bring your own ontology: entity types, edge types,
and per-edge domain/range that drive both extraction (the LLM prompt) and
validation (grade_locality). This loader reads a YAML schema and produces a
kg-common `Ontology` instance the rest of the pipeline consumes unchanged.

YAML shape (see examples/good-dog-corpus/ontology.yaml):

    version: "..."
    entity_types:
      - id: breed
        description: "..."
      - id: person
    edge_types:
      - id: mentions
        direction: "publication -> *"     # src -> tgt; * = any entity type
      - id: located_in
        direction: "organization -> place"

`direction` encodes domain/range. "*" on either side expands to all entity
types (i.e. unconstrained on that side). Edges with "* -> *" impose no
grade_locality constraint (omitted from EDGE_DOMAIN_RANGE so validate_grade
passes by default).
"""

from __future__ import annotations

from itertools import product
from pathlib import Path

import yaml

from second_brain.ontology_base import Ontology


class YamlOntology(Ontology):
    """An Ontology whose type sets + domain/range come from a YAML file."""

    def __init__(self, path: str | Path) -> None:
        self._source_path = str(path)
        doc = yaml.safe_load(Path(path).read_text())

        ents = [e["id"] for e in doc.get("entity_types", []) if e.get("id")]
        edges = [e["id"] for e in doc.get("edge_types", []) if e.get("id")]

        self.NODE_TYPES = frozenset(ents)
        self.EDGE_TYPES = frozenset(edges)
        self.VERSION = doc.get("version", "yaml-ontology")

        # Parse `direction: "src -> tgt"` into EDGE_DOMAIN_RANGE. "*" expands
        # to all entity types. Fully-unconstrained edges (* -> *) are omitted
        # so the base validate_grade returns True for them.
        dr: dict[str, list[tuple[str, str]]] = {}
        for e in doc.get("edge_types", []):
            eid = e.get("id")
            if not eid:
                continue
            # `same_type: true` restricts domain/range to the diagonal
            # (src type == tgt type) — the SKOS-altLabel / entity-resolution
            # constraint that an alias never crosses an entity type. Takes
            # precedence over a "* -> *" direction (which would otherwise mean
            # unconstrained).
            if e.get("same_type"):
                dr[eid] = [(t, t) for t in sorted(self.NODE_TYPES)]
                continue
            direction = (e.get("direction") or "").strip()
            if "->" not in direction:
                continue
            left, right = (s.strip() for s in direction.split("->", 1))
            srcs = ents if left == "*" else [s.strip() for s in left.split("|")]
            tgts = ents if right == "*" else [t.strip() for t in right.split("|")]
            if left == "*" and right == "*":
                continue  # no constraint
            # keep only pairs over declared entity types
            pairs = [
                (s, t)
                for s, t in product(srcs, tgts)
                if s in self.NODE_TYPES and t in self.NODE_TYPES
            ]
            if pairs:
                dr[eid] = pairs
        self.EDGE_DOMAIN_RANGE = dr

        # Alias map (optional): {surface_form: canonical}
        self.TYPE_ALIASES = {}
        for a in doc.get("aliases", []) or []:
            if isinstance(a, dict) and a.get("from") and a.get("to"):
                self.TYPE_ALIASES[a["from"]] = a["to"]

    # The pipeline calls this for rejection telemetry; YAML ontologies don't
    # track rejections, so return an empty tally rather than 500-ing callers.
    def get_rejection_counts(self) -> dict:
        return {}


def load_ontology(path: str | Path | None = None):
    """Return a YamlOntology(path), or the built-in default when path is None.

    The default is the hardcoded SecondBrainOntology — so existing behavior is
    unchanged when no --ontology is given. Pass a YAML path to override.
    """
    if path:
        return YamlOntology(path)
    from second_brain.ontology import Ontology as DefaultOntology

    return DefaultOntology()
