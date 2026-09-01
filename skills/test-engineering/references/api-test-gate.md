# API test completion gate

JSONL is process evidence. The completion oracle is `scripts/grade_api_jsonl.py` against a
pre-declared matrix. Prompt-only rules and same-session correction are not the gate.

## Matrix

Write `.pernavo/api-test-matrix.json` before claiming HTTP or business API tests complete:

```json
{
  "schema_version": "pernavo.api_test_matrix.v1",
  "jsonl": "logs/api-test.jsonl",
  "required_cases": [
    {
      "id": "create-valid",
      "kind": "business-success",
      "expect": {"http": 200, "result": 1}
    },
    {
      "id": "empty-id",
      "kind": "validation",
      "expect": {"http": 200, "result": -1}
    }
  ]
}
```

`business-success` needs `result=1` and side-effect or `database.reconciliation` evidence. HTTP 200
with `result=-1` cannot pass that kind. Every required case needs an explicit
`passed` / `failed` / `blocked` / `skipped` state; blocked and skipped need a reason. Probe lines
without `case_id` do not count. If the matrix has no business-success case, or none passed, the
grade is `incomplete`.

Examples: `examples/api-test-gate/czlhc-negative` must fail; `examples/api-test-gate/setposition-pass`
must pass.

```bash
python3 scripts/grade_api_jsonl.py --matrix .pernavo/api-test-matrix.json
```

Use `--hook` when a command hook should exit 2 on failure. Do not log secrets from JSONL.

## Host Stop hook

Default install follows [AI_INSTALL.md](../../../AI_INSTALL.md): an installing agent reads the host
JSON and merges `scripts/api_test_stop_hook.py` into Claude `Stop` / `TaskCompleted`, Codex
`Stop` / `SubagentStop`, Cursor `stop` / `subagentStop`, and Grok `Stop` / `SubagentStop`. It does
not replace existing hooks. After editing, verify with `scripts/install_api_test_gate.py --check`
and the optional `--cursor-hooks` / `--grok-hooks` paths. Do not `--apply` against default host
paths.

The adapter allows ordinary turns. It grades when Stop claims completion and a matrix or API/JSONL
context is present, or when `TaskCompleted` sees a matrix. Failure prints
`{"decision":"block","reason":"..."}` and exits 2. The reason names the next missing case id.
A leftover matrix does not block a Stop that does not claim tests are done.
