#!/usr/bin/env bash
# Phase-0 hook-firing instrument for open-second-brain.
# From the kg-common verification harness (docs/harness-verification/).
#
# Observe-only: appends ONE event for the tool call on stdin, then ALWAYS exits 0.
# A non-zero PreToolUse hook DENIES the tool it was only meant to observe, so this
# must never propagate failure. It answers "did the hook fire at all?" before any
# enforcement is trusted.
#
# NOTE: kg_common is editable-installed in this project's .venv (pip install -e
# ../kg-common), so `python -m kg_common.verify.eventlog` works directly. The
# PYTHONPATH export below is a belt-and-suspenders fallback to the sibling
# checkout for environments where the editable install is absent.
set -uo pipefail

payload="$(cat)"

export PYTHONPATH="${KG_COMMON_PATH:-$HOME/Projects/kg-common}${PYTHONPATH:+:$PYTHONPATH}"

PY="${KG_HARNESS_PYTHON:-}"
if [ -z "$PY" ]; then
  for c in "${CLAUDE_PROJECT_DIR:-.}/.venv/bin/python" "./.venv/bin/python" "python3"; do
    if [ -x "$c" ] || command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
  done
fi

if [ -n "$PY" ] && printf '%s' "$payload" | "$PY" -m kg_common.verify.eventlog 2>/dev/null; then
  exit 0
fi

# Fallback: guarantee the "it fired" record even if python/import was unavailable.
log="${KG_HARNESS_EVENTLOG:-${CLAUDE_PROJECT_DIR:-.}/.harness/events.jsonl}"
mkdir -p "$(dirname "$log")" 2>/dev/null || true
printf '{"event":"hook_fired","source":"shell-fallback","ts_ms":%s}\n' \
  "$(date +%s%3N 2>/dev/null || echo 0)" >> "$log" 2>/dev/null || true
exit 0
