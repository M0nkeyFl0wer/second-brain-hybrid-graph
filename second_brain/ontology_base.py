"""Ontology base class — vendored from kg-common (MIT, M0nkeyFl0wer) so this
repo is self-contained with no private dependency. Defines the Ontology ABC:
NODE_TYPES / EDGE_TYPES / EDGE_DOMAIN_RANGE + validation (validate_grade etc.).
Subclass it (see second_brain/ontology.py) or load from YAML (ontology_yaml.py).
"""

from __future__ import annotations

from pathlib import Path

# LadybugDB SQL-ish type → Python default value used when the field is missing
# from a caller's kwargs. Project ontologies override via entity_field_schema()
# and friends to add project-specific columns.
DEFAULT_ENTITY_FIELDS: dict[str, tuple[str, object]] = {
    "id": ("STRING", ""),
    "entity_type": ("STRING", ""),
    "label": ("STRING", ""),
    "description": ("STRING", ""),
    "confidence": ("DOUBLE", 0.5),
    "provenance": ("STRING", "unknown"),
    "properties": ("STRING", "{}"),
    "created_at": ("INT64", 0),
    "updated_at": ("INT64", 0),
}

DEFAULT_DOCUMENT_FIELDS: dict[str, tuple[str, object]] = {
    "id": ("STRING", ""),
    "title": ("STRING", ""),
    "path": ("STRING", ""),
    "doc_type": ("STRING", ""),
    "excerpt": ("STRING", ""),
    "ingested_at": ("INT64", 0),
}

DEFAULT_CHUNK_FIELDS: dict[str, tuple[str, object]] = {
    "id": ("STRING", ""),
    "doc_id": ("STRING", ""),
    "text": ("STRING", ""),
    "chunk_index": ("INT64", 0),
    "word_count": ("INT64", 0),
    "created_at": ("INT64", 0),
}

DEFAULT_EDGE_FIELDS: dict[str, tuple[str, object]] = {
    "edge_type": ("STRING", ""),
    "weight": ("DOUBLE", 1.0),
    "confidence": ("DOUBLE", 0.5),
    "source_url": ("STRING", ""),
    "evidence": ("STRING", ""),
    "provenance": ("STRING", "unknown"),
    "properties": ("STRING", "{}"),
    "created_at": ("INT64", 0),
    "updated_at": ("INT64", 0),
    # Bi-temporal fields. INT64 ms-since-epoch, sentinel 0 = null/unset.
    # Graphiti uses TIMESTAMP nullable; kg-common uses INT64 ms with sentinel
    # to stay consistent with created_at/updated_at and sidestep Lady's
    # naive-datetime read-back (Graphiti issue #893). See PLAN_TEMPORAL.md §2.
    "valid_at_ms": ("INT64", 0),
    "invalid_at_ms": ("INT64", 0),
    "expired_at_ms": ("INT64", 0),
}


class Ontology:
    NODE_TYPES: frozenset[str] = frozenset()
    EDGE_TYPES: frozenset[str] = frozenset()
    EDGE_DOMAIN_RANGE: dict[str, list[tuple[str, str]]] = {}
    TYPE_ALIASES: dict[str, str] = {}
    # Synonym map for edge types — same shape as TYPE_ALIASES but for edges.
    # `{"FRIENDS_WITH": "KNOWS", "BECAME_LEADER_OF": "ELECTED"}` declares
    # that the two LHS terms are semantically equivalent to their RHS
    # canonical forms. The writer normalizes inputs through
    # `canonical_edge_type` before validate / contradiction / write, so
    # consumers can ingest with whatever vocabulary their LLM extractor
    # emits without polluting the graph with synonym clutter.
    # Phase-1 dedup is structural (identity); aliases are how a project
    # opts into "same fact expressed differently" without invoking LLM
    # judgment in the write path.
    EDGE_TYPE_ALIASES: dict[str, str] = {}
    VERSION: str = "0.0.0"

    # ------------------------------------------------------------------
    # Schema surface — labels, primary keys, rel-table names
    #
    # The shared GraphWriter consumes these so seabrick (kind/canonical_name,
    # EDGE rel-table, doc_id/chunk_id PKs) can use the same code as
    # election_oracle (entity_type/label, RELATES_TO, id PKs).
    # ------------------------------------------------------------------

    ENTITY_LABEL: str = "Entity"
    ENTITY_PK: str = "id"
    ENTITY_TYPE_FIELD: str = "entity_type"
    ENTITY_LABEL_FIELD: str = "label"

    # Whether `GraphWriter.add_entity` runs the dedup gate before MERGE.
    # Phase-1 dedup is O(n) per call (iterates entity labels); for projects
    # doing bulk seeds with thousands of entities this becomes O(n²) and
    # unacceptable. Default True (correctness over speed) so existing tests
    # pass; bulk-write consumers flip to False until Phase 2 lands the
    # indexed `normalized_label` column. See PLAN_TEMPORAL.md §3.3.
    DEDUP_AT_WRITE: bool = True

    DOCUMENT_LABEL: str = "Document"
    DOCUMENT_PK: str = "id"

    CHUNK_LABEL: str = "Chunk"
    CHUNK_PK: str = "id"
    CHUNK_DOC_FK: str = "doc_id"

    EDGE_REL_TABLE: str = "RELATES_TO"
    EDGE_TYPE_FIELD: str = "edge_type"

    CHUNK_OF_REL: str = "CHUNK_OF"
    MENTIONED_IN_REL: str = "MENTIONED_IN"

    # ------------------------------------------------------------------
    # Phase 2 — normalization + prompt hooks
    # ------------------------------------------------------------------

    def normalize_node_type(self, t: str | None) -> str | None:
        """Map a raw LLM-produced type to a canonical NODE_TYPES member.

        Default: consult TYPE_ALIASES, fall back to lowercased exact match.
        """
        if not t:
            return None
        alias = self.TYPE_ALIASES.get(t) or self.TYPE_ALIASES.get(t.lower())
        candidate = alias or t.lower()
        if candidate in self.NODE_TYPES:
            return candidate
        return None

    def validate_edge(
        self, src_type: str, etype: str, tgt_type: str
    ) -> tuple[bool, str]:
        """Ontology-level validation for an edge.

        Default: checks edge type membership + grade locality via
        EDGE_DOMAIN_RANGE. Returns (ok, reason).
        """
        if etype not in self.EDGE_TYPES:
            return False, f"unknown edge type: {etype}"
        domain_range = self.EDGE_DOMAIN_RANGE.get(etype)
        if domain_range is None:
            return True, ""
        if (src_type, tgt_type) in domain_range:
            return True, ""
        return (
            False,
            f"grade violation: {etype} does not accept {src_type} -> {tgt_type}",
        )

    def extraction_prompt_fragment(self) -> str:
        """LLM-facing type list for extraction prompts. Subclass to customize."""
        nodes = ", ".join(sorted(self.NODE_TYPES))
        edges = ", ".join(sorted(self.EDGE_TYPES))
        return (
            f"Allowed node types: {nodes}\n"
            f"Allowed edge types: {edges}\n"
        )

    @classmethod
    def from_markdown(cls, path: Path) -> "Ontology":
        raise NotImplementedError("Phase 2")

    # ------------------------------------------------------------------
    # Phase 1 — writer surface
    # ------------------------------------------------------------------

    def validate_entity_type(self, t: str) -> bool:
        """True iff `t` is in NODE_TYPES. No alias lookup — caller should
        normalize first via `normalize_node_type`."""
        return t in self.NODE_TYPES

    def canonical_edge_type(self, t: str) -> str:
        """Resolve `t` through `EDGE_TYPE_ALIASES` to its canonical form.

        Lookup order: exact match → uppercased exact match → identity.
        Symmetric with TYPE_ALIASES' lowercase fallback, mirrored for
        edge-type convention (UPPER_SNAKE). Idempotent: passing a
        canonical form returns it unchanged.
        """
        if not t:
            return t
        alias = (
            self.EDGE_TYPE_ALIASES.get(t)
            or self.EDGE_TYPE_ALIASES.get(t.upper())
        )
        return alias or t

    @property
    def entity_type_names(self) -> list:
        """Sorted list of declared entity-type names. Convenience accessor over
        NODE_TYPES, used by status/validation/dashboard tooling."""
        return sorted(self.NODE_TYPES)

    @property
    def edge_type_names(self) -> list:
        """Sorted list of declared edge-type names (convenience over EDGE_TYPES)."""
        return sorted(self.EDGE_TYPES)

    # Structural edges are graph-mechanics relationships (e.g. wikilinks,
    # untyped-extraction fallback) that exist independent of any domain
    # ontology. They must always validate, or ingest silently drops every
    # wikilink/tag edge and every extracted edge whose type the LLM omitted
    # (extract.py defaults those to ASSOCIATED_WITH).
    STRUCTURAL_EDGE_TYPES = frozenset({"ASSOCIATED_WITH"})

    def validate_edge_type(self, t: str) -> bool:
        return t in self.EDGE_TYPES or t in self.STRUCTURAL_EDGE_TYPES

    def validate_grade(self, edge: str, src_type: str, tgt_type: str) -> bool:
        """True if (src_type, tgt_type) appears in EDGE_DOMAIN_RANGE[edge],
        or the edge has no domain/range constraint declared."""
        dr = self.EDGE_DOMAIN_RANGE.get(edge)
        if dr is None:
            return True
        return (src_type, tgt_type) in dr

    def entity_field_schema(self) -> dict[str, tuple[str, object]]:
        """Field set for the Entity node table. Override to add project fields."""
        return dict(DEFAULT_ENTITY_FIELDS)

    def document_field_schema(self) -> dict[str, tuple[str, object]]:
        return dict(DEFAULT_DOCUMENT_FIELDS)

    def chunk_field_schema(self) -> dict[str, tuple[str, object]]:
        return dict(DEFAULT_CHUNK_FIELDS)

    def edge_field_schema(self) -> dict[str, tuple[str, object]]:
        """Field set for the RELATES_TO edge. `edge_type` is part of the MERGE
        key and always required."""
        return dict(DEFAULT_EDGE_FIELDS)

    def entity_on_match_fields(self) -> list[str]:
        """Fields refreshed on a MERGE's ON MATCH branch.

        Default: empty — entity fields are write-once. Seabrick overrides with
        `["embedding", "embedded_at"]` so re-runs pick up new embeddings
        without a full graph rebuild.
        """
        return []

    def edge_write_mode(self) -> str:
        """How edges are written: `"merge"` (dedup by src/tgt/edge_type) or
        `"create"` (parallel edges allowed).

        Default `"merge"` is the correctness-preferred behavior. Seabrick's
        baseline graph was written with CREATE and has 78 parallel duplicate
        edges whose collapse would fail count-parity tests; it overrides to
        `"create"` for Phase 1 migration. A future stage_6 dedup pass should
        let it flip back.
        """
        return "merge"

    def schema_ddl(self) -> list[str]:
        """Return the full list of CREATE TABLE statements for this ontology.

        Default schema: Entity + Document + Chunk nodes, RELATES_TO +
        MENTIONED_IN + CHUNK_OF edges. Labels / PKs / rel-table names come from
        the class-level constants so projects can rename without overriding
        this method.
        """
        ddl: list[str] = []

        ent_cols = ", ".join(
            f"{n} {t}" for n, (t, _) in self.entity_field_schema().items()
        )
        ddl.append(
            f"CREATE NODE TABLE IF NOT EXISTS {self.ENTITY_LABEL} "
            f"({ent_cols}, PRIMARY KEY ({self.ENTITY_PK}))"
        )

        doc_cols = ", ".join(
            f"{n} {t}" for n, (t, _) in self.document_field_schema().items()
        )
        ddl.append(
            f"CREATE NODE TABLE IF NOT EXISTS {self.DOCUMENT_LABEL} "
            f"({doc_cols}, PRIMARY KEY ({self.DOCUMENT_PK}))"
        )

        chk_cols = ", ".join(
            f"{n} {t}" for n, (t, _) in self.chunk_field_schema().items()
        )
        ddl.append(
            f"CREATE NODE TABLE IF NOT EXISTS {self.CHUNK_LABEL} "
            f"({chk_cols}, PRIMARY KEY ({self.CHUNK_PK}))"
        )

        edge_cols = ", ".join(
            f"{n} {t}" for n, (t, _) in self.edge_field_schema().items()
        )
        ddl.append(
            f"CREATE REL TABLE IF NOT EXISTS {self.EDGE_REL_TABLE} "
            f"(FROM {self.ENTITY_LABEL} TO {self.ENTITY_LABEL}, "
            f"{edge_cols}, MANY_MANY)"
        )

        ddl.append(
            f"CREATE REL TABLE IF NOT EXISTS {self.MENTIONED_IN_REL} "
            f"(FROM {self.ENTITY_LABEL} TO {self.DOCUMENT_LABEL}, "
            "mention_count INT64, first_mention_offset INT64, "
            "created_at INT64, MANY_MANY)"
        )
        ddl.append(
            f"CREATE REL TABLE IF NOT EXISTS {self.CHUNK_OF_REL} "
            f"(FROM {self.CHUNK_LABEL} TO {self.DOCUMENT_LABEL}, MANY_ONE)"
        )
        return ddl

    def trust_weight(self, doc_type: str) -> float:
        """Per-project source-trust lookup. Default: 1.0 for all types."""
        return 1.0
