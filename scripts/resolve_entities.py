"""Resolve (deduplicate) entities in the graph — Phase A: deterministic, dry-run.

Reads entities from the LadybugDB graph, runs the deterministic EntityResolver,
and writes the proposed clustering to a JSON file (the same shape
`eval/run_er_eval.py` scores). It does NOT mutate the graph.

    python -m scripts.resolve_entities                  # -> data/resolution.json
    python -m scripts.resolve_entities --out clusters.json
    python -m scripts.resolve_entities --graph data/graph.lbug --min-cluster 2

Applying merges to the live graph (repoint edges, fold aliases, delete dup
nodes) is destructive on this LadybugDB build and is intentionally NOT
implemented here — it must go through the `ladybug-surgery` skill (Phase D).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from second_brain import config
from second_brain.pipeline import EntityResolver


def _load_entities(graph_dir: Path) -> list[dict]:
    from second_brain.graph import Graph
    g = Graph(graph_dir, read_only=True)
    try:
        return g.query("MATCH (e:Entity) RETURN e.label AS label, e.entity_type AS entity_type")
    finally:
        g.close()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--graph", default=str(config.GRAPH_DIR))
    ap.add_argument("--out", default=str(Path(config.GRAPH_DIR).parent / "resolution.json"))
    ap.add_argument("--min-cluster", type=int, default=2,
                    help="Only report clusters with at least this many members (default 2).")
    ap.add_argument("--apply", action="store_true",
                    help="(Phase D, not implemented) apply merges to the graph.")
    args = ap.parse_args(argv)

    if args.apply:
        print("--apply is not implemented: graph mutation must go through the "
              "ladybug-surgery skill (Phase D). This tool is dry-run only.",
              file=sys.stderr)
        return 2

    entities = _load_entities(Path(args.graph))
    result = EntityResolver(entities).resolve()

    reported = [c for c in result.clusters if len(c.members) >= args.min_cluster]
    Path(args.out).write_text(json.dumps(result.to_eval_dict(), indent=2, ensure_ascii=False))

    print(f"Resolved {len(entities)} entities → {len(result.clusters)} clusters "
          f"({result.merged_count} labels folded).")
    print(f"  {len(reported)} multi-member cluster(s) (>= {args.min_cluster}); "
          f"full clustering written to {args.out}")
    for c in sorted(reported, key=lambda c: -len(c.members))[:15]:
        print(f"    {c.canonical!r}  <-  {c.aliases}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
