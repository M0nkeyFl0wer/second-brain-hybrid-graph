"""Pydantic models for entity-resolution output.

A resolver groups entity labels that refer to the same real-world thing into
clusters. The canonical label is the cluster's `skos:prefLabel`; the rest become
`skos:altLabel` aliases — the same SKOS framing the extraction models use, so a
resolved cluster feeds straight back into `ExtractedEntity.aliases`.

`ResolutionResult.to_eval_dict()` emits the exact `{clusters: [{canonical,
members}]}` shape that `eval/run_er_eval.py` scores, so resolve → score is one
hop with no glue.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ResolutionMatch(BaseModel):
    """One accepted pairwise match, with the rule that fired as evidence."""

    model_config = ConfigDict(str_strip_whitespace=True)

    left: str
    right: str
    rule: str = Field(
        description="Which matcher fired (normalized-equal, plural, acronym, surname, ...)"
    )
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: str = Field(default="", description="Human-readable why")


class ResolutionCluster(BaseModel):
    """A set of labels judged to be the same entity."""

    canonical: str = Field(description="skos:prefLabel — the chosen canonical label")
    members: list[str] = Field(description="All labels in the cluster (incl. canonical)")

    @property
    def aliases(self) -> list[str]:
        """skos:altLabel — members other than the canonical."""
        return [m for m in self.members if m != self.canonical]


class ResolutionResult(BaseModel):
    """Full resolver output: the clustering + the matches that produced it."""

    clusters: list[ResolutionCluster] = Field(default_factory=list)
    matches: list[ResolutionMatch] = Field(default_factory=list)

    def to_eval_dict(self) -> dict[str, Any]:
        """The `{clusters: [{canonical, members}]}` shape run_er_eval consumes."""
        return {
            "clusters": [
                {"canonical": c.canonical, "members": list(c.members)} for c in self.clusters
            ]
        }

    @property
    def merged_count(self) -> int:
        """How many labels were folded away (members - clusters)."""
        return sum(len(c.members) for c in self.clusters) - len(self.clusters)
