# Verification harness hooks

Project-local wiring of the **kg-common verification harness**
(`kg_common.verify.*`) into open-second-brain. These are the same two hooks
re-wilding-ssi runs; activation lives in `.claude/settings.json`, the scripts
live here (version-controlled).

| File | Phase | What it does |
|---|---|---|
| `harness-eventlog.sh` | Phase 0 (observe) | Appends one `hook_fired` event per action-tool call to `.harness/events.jsonl`. **Always allows** — answers "did the hook fire?" |
| `harness-deny-gate.sh` | Phase 1 (enforce) | Blocks a gated tool call unless its required proof re-verifies. **Fail-open**: with the empty policy below it blocks nothing. |
| `harness-gate-policy.json` | — | The deny-gate rules. Ships as `[]` (nothing gated). |

Both are registered on the `Write\|Edit\|MultiEdit\|Bash` matcher in
`.claude/settings.json`. `kg_common` is editable-installed in `.venv`
(`pip install -e ../kg-common`); the `PYTHONPATH` export in each script is a
fallback to the sibling checkout.

## Confirming the eventlog fires

```bash
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"ls"}}' \
  | scripts/hooks/harness-eventlog.sh ; echo "exit=$?"   # must be 0
tail -n1 .harness/events.jsonl                            # one JSON line
```

## Adding a real gate (Phase 1)

Edit `harness-gate-policy.json` to a list of rules. A rule matches when its
`tool` equals the tool name AND any `command_contains` / `file_path_contains`
substring is present; on a match the gate requires
`<proof_dir>/<slug>/<require_check>.json` to exist and re-verify, else it
DENIES. Set `KG_HARNESS_TASK` to the current task slug.

Example — gate a graph commit on the entity-resolution B-Cubed threshold:

```json
[
  { "tool": "Bash", "command_contains": "GRAPH_COMMIT", "require_check": "bcubed" }
]
```

Produce the proof with a gate before the gated action:

```bash
python -m kg_common.verify.gates bcubed --gold eval/er_gold.json --threshold 0.85
```

See `kg-common/docs/harness-verification/WIRING.md` for the full contract.
