#!/usr/bin/env bash
# PreToolUse DENY gate for open-second-brain.
# From the kg-common verification harness (docs/harness-verification/).
#
# Blocks a gated tool call unless its required proof exists and re-verifies.
# Emits a PreToolUse decision JSON on stdout; a "deny" blocks the tool even
# under --dangerously-skip-permissions. The decision rides the JSON, never the
# exit code, so any internal error fails OPEN (allow), never wedging a tool call.
#
# Fail-open by default: ships with an EMPTY gate policy
# (scripts/hooks/harness-gate-policy.json == []), so nothing is blocked until a
# real gate rule is added. See scripts/hooks/README.md for how to wire a gate
# (e.g. a B-Cubed threshold on the entity-resolution eval).
#
# NOTE: kg_common is editable-installed in this project's .venv; the PYTHONPATH
# export below is a fallback to the sibling checkout.
set -uo pipefail

payload="$(cat)"

export PYTHONPATH="${KG_COMMON_PATH:-/home/user/Projects/kg-common}${PYTHONPATH:+:$PYTHONPATH}"
: "${KG_HARNESS_GATE_POLICY:=${CLAUDE_PROJECT_DIR:-.}/scripts/hooks/harness-gate-policy.json}"
export KG_HARNESS_GATE_POLICY

PY="${KG_HARNESS_PYTHON:-}"
if [ -z "$PY" ]; then
  for c in "${CLAUDE_PROJECT_DIR:-.}/.venv/bin/python" "./.venv/bin/python" "python3"; do
    if [ -x "$c" ] || command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
  done
fi

if [ -n "$PY" ] && out="$(printf '%s' "$payload" | "$PY" -m kg_common.verify.deny_gate 2>/dev/null)"; then
  printf '%s\n' "$out"
  exit 0
fi

# Fail-open: could not run the gate -> do not block; let normal permission flow proceed.
exit 0
