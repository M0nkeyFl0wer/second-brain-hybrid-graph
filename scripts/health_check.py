"""
Health check script for open-second-brain — graph observability.

Run manually: python scripts/health_check.py
Run via timer: systemd timer every 15 min

Checks:
1. Graph: total entities, total edges, type distribution, orphan count
2. Write queue: pending writes in graph_queue.jsonl
3. Write log: rejection rate from write_log.jsonl (if exists)
4. Last enrichment: time since last run
5. WAL health: check for orphaned WAL files

Thresholds:
- Orphan entities > 50: WARNING
- Connected % < 95%: WARNING
- Rejection rate > 20%: CRITICAL
- Queue depth > 1000: WARNING
- Last enrichment > 24h: WARNING
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from second_brain.graph import Graph
from second_brain.ontology_yaml import load_ontology
from second_brain import config

DATA_DIR = config.GRAPH_DIR.parent
GRAPH_DIR = config.GRAPH_DIR
QUEUE_PATH = DATA_DIR / "graph_queue.jsonl"
WRITE_LOG = DATA_DIR / "write_log.jsonl"
LAST_RUN_FILE = DATA_DIR / "enrichment_last_run.txt"

THRESHOLDS = {
    "orphan_entities": {"warning": 50, "critical": 500},
    "connected_pct": {"warning": 95, "critical": 90},
    "rejection_rate": {"warning": 0.15, "critical": 0.20},
    "queue_depth": {"warning": 1000, "critical": 5000},
    "hours_since_enrichment": {"warning": 24, "critical": 72},
}


def status_icon(ok, warn):
    if ok:
        return "ok"
    return "warn" if warn else "crit"


def check_graph():
    """Check graph health using the current Graph API."""
    try:
        ontology = load_ontology()
        g = Graph(graph_dir=GRAPH_DIR, ontology=ontology)
        entity_count = g.entity_count()
        edge_count = g.edge_count()
        doc_count = g.document_count()
        type_dist = g.type_distribution()
        edge_dist = g.edge_type_distribution()

        # Count orphans (entities that don't participate in any
        # RELATES_TO edge). LadybugDB doesn't support WHERE NOT
        # exists(path) so we do it in Python.
        connected = set()
        for r in g.query(
            "MATCH (a:Entity)-[e:RELATES_TO]->(b:Entity) " "RETURN a.id AS src, b.id AS tgt"
        ):
            connected.add(r["src"])
            connected.add(r["tgt"])
        orphans = entity_count - len(connected)

        connected_pct = (
            ((entity_count - orphans) / entity_count * 100) if entity_count > 0 else 100.0
        )
        g.close()

        issues = []
        if orphans > THRESHOLDS["orphan_entities"]["critical"]:
            issues.append(f"{orphans} orphan entities (critical)")
        elif orphans > THRESHOLDS["orphan_entities"]["warning"]:
            issues.append(f"{orphans} orphan entities (warning)")

        if connected_pct < THRESHOLDS["connected_pct"]["critical"]:
            issues.append(f"Only {connected_pct:.1f}% connected (critical)")
        elif connected_pct < THRESHOLDS["connected_pct"]["warning"]:
            issues.append(f"Only {connected_pct:.1f}% connected (warning)")

        status = "ok" if not issues else ("warning" if len(issues) < 2 else "critical")
        return {
            "status": status,
            "total_entities": entity_count,
            "total_edges": edge_count,
            "total_documents": doc_count,
            "entity_types": dict(sorted(type_dist.items(), key=lambda x: -x[1])),
            "edge_types": dict(sorted(edge_dist.items(), key=lambda x: -x[1])),
            "orphan_entities": orphans,
            "connected_pct": round(connected_pct, 1),
            "issues": issues,
        }
    except Exception as ex:
        return {"status": "error", "error": str(ex)}


def check_queue():
    """Check write queue depth."""
    try:
        if not QUEUE_PATH.exists():
            return {"status": "ok", "depth": 0}

        with open(QUEUE_PATH) as f:
            depth = sum(1 for _ in f)

        issues = []
        if depth > THRESHOLDS["queue_depth"]["critical"]:
            issues.append(f"Queue depth {depth} (critical)")
        elif depth > THRESHOLDS["queue_depth"]["warning"]:
            issues.append(f"Queue depth {depth} (warning)")

        status = "ok" if not issues else ("warning" if len(issues) < 2 else "critical")
        return {"status": status, "depth": depth, "issues": issues}
    except Exception as ex:
        return {"status": "error", "error": str(ex)}


def check_rejection_rate():
    """Check write_log.jsonl rejection rate."""
    try:
        if not WRITE_LOG.exists():
            return {"status": "ok", "rate": 0.0}

        total = 0
        rejected = 0
        with open(WRITE_LOG) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    total += 1
                    if entry.get("type"):
                        rejected += 1
                except json.JSONDecodeError:
                    continue

        rate = rejected / total if total > 0 else 0.0

        issues = []
        if rate > THRESHOLDS["rejection_rate"]["critical"]:
            issues.append(f"Rejection rate {rate:.0%} (critical)")
        elif rate > THRESHOLDS["rejection_rate"]["warning"]:
            issues.append(f"Rejection rate {rate:.0%} (warning)")

        status = "ok" if not issues else ("warning" if len(issues) < 2 else "critical")
        return {
            "status": status,
            "rate": round(rate, 4),
            "total_records": total,
            "rejected_records": rejected,
            "issues": issues,
        }
    except Exception as ex:
        return {"status": "error", "error": str(ex)}


def check_last_enrichment():
    """Check time since last enrichment run."""
    try:
        if not LAST_RUN_FILE.exists():
            return {"status": "warning", "hours_since": None, "issues": ["Never run"]}

        with open(LAST_RUN_FILE) as f:
            last_run = datetime.fromisoformat(f.read().strip())

        hours_since = (datetime.now(timezone.utc) - last_run).total_seconds() / 3600

        issues = []
        if hours_since > THRESHOLDS["hours_since_enrichment"]["critical"]:
            issues.append(f"Last enrichment {hours_since:.1f}h ago (critical)")
        elif hours_since > THRESHOLDS["hours_since_enrichment"]["warning"]:
            issues.append(f"Last enrichment {hours_since:.1f}h ago (warning)")

        status = "ok" if not issues else ("warning" if len(issues) < 2 else "critical")
        return {
            "status": status,
            "hours_since": round(hours_since, 1),
            "last_run": last_run.isoformat(),
            "issues": issues,
        }
    except Exception as ex:
        return {"status": "error", "error": str(ex)}


def check_wal_health():
    """Check for orphaned WAL files."""
    issues = []
    wal = GRAPH_DIR.with_suffix(".wal")
    shadow = GRAPH_DIR.with_suffix(".shadow")
    orphan_marker = DATA_DIR / ".builder-running"

    if wal.exists() and orphan_marker.exists():
        issues.append(f"Orphaned WAL detected: {wal.name}")

    if shadow.exists() and orphan_marker.exists():
        issues.append(f"Orphaned shadow detected: {shadow.name}")

    return {
        "status": "ok" if not issues else "critical",
        "issues": issues,
    }


def main():
    """Run all health checks and print report."""
    print("=" * 60)
    print(" open-second-brain Health Check")
    print(f" {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)

    checks = {
        "Graph": check_graph(),
        "Write Queue": check_queue(),
        "Rejection Rate": check_rejection_rate(),
        "Last Enrichment": check_last_enrichment(),
        "WAL Health": check_wal_health(),
    }

    all_ok = True
    any_critical = False

    for name, result in checks.items():
        status = result.get("status", "error")
        icon = status_icon(status == "ok", status != "critical")
        print(f"\n[{icon}] {name}: {status.upper()}")
        print(f"   {json.dumps(result, indent=2, default=str)}")

        if status != "ok":
            all_ok = False
        if status == "critical":
            any_critical = True

    print("\n" + "=" * 60)
    if any_critical:
        print("CRITICAL ISSUES DETECTED -- manual intervention required")
        sys.exit(2)
    elif not all_ok:
        print("WARNINGS DETECTED -- monitor closely")
        sys.exit(1)
    else:
        print("All systems healthy")
        sys.exit(0)


if __name__ == "__main__":
    main()
