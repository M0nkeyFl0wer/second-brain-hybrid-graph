"""Pydantic models — the canonical, validated templates for pipeline output.

`extraction` holds the standardized shape every extraction tier (deterministic,
nlp, llm) and every backend (urllib Ollama, urllib OpenAI-compatible, optional
Instructor) produces. Importing this package pulls in pydantic only — no
Instructor, no openai SDK — so the core stays import-clean.
"""

from .extraction import ExtractedEdge, ExtractedEntity, ExtractionResult
from .validation import (
    ValidationReport,
    ValidationViolation,
    check_extraction,
)

__all__ = [
    "ExtractedEntity",
    "ExtractedEdge",
    "ExtractionResult",
    "ValidationViolation",
    "ValidationReport",
    "check_extraction",
]
