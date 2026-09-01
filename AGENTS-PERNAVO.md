# Shared agent guidance

This file contains reusable guidance distilled from repository learning notes.

## Avoid unrequested compatibility

Do not add backward-compatibility layers, legacy fallbacks, dual-write, field aliases, or silent
mitigations unless a real caller, shipped contract, or explicit user request requires them. Do not
preserve obsolete paths in code that has never been deployed. Removing an existing shipped contract
requires evidence and a human decision; this rule does not authorize that.

This preference applies to greenfield or explicitly unconsumed code. It does not authorize deleting
an existing supported API, message, library, data, or configuration contract. Treat unconfirmed
dispatch, reflection, and configuration entry points as unconfirmed until evidence resolves them.

## API and business-test completion

Do not claim HTTP API or business-flow tests complete from HTTP 200, empty-payload errors,
negative-only logs, or the existence of a JSONL file. Complete means every required case in
`.pernavo/api-test-matrix.json` has an explicit passed, failed, blocked, or skipped state; at least
one business-success case passed with side-effect or reconciliation evidence; and the deterministic
grader exits 0. HTTP 200 with `result=-1` is not business success. Probe lines without a case id do
not count. The host Stop hook is the gate; conversational correction in the same session is not. If
all success paths are blocked, or the matrix has no business-success case, the run is incomplete.

## Host runtime evidence

Keep secret-free host runtime evidence under `~/.pernavo/logs`, not in a project tree. Do not write
prompts, commands, tool payloads, credentials, or business JSONL bodies there. A log line is not
proof that a workflow loaded, executed, or completed.
