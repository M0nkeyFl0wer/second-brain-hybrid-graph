"""Post-extraction pipeline stages.

Currently: `resolve` — entity resolution (deduplication) over the typed graph.
The resolver is measured by `eval/run_er_eval.py` (B-Cubed) against
`eval/er_gold.json`.
"""

from .resolve import EntityResolver

__all__ = ["EntityResolver"]
