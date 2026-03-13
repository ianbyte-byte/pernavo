---
name: lcc-bugfix
description: Bugfix workflow (triage → reproduce → fix → review → verify) using project subagents.
disable-model-invocation: true
---

Run a bugfix workflow in Claude Code using subagents.

## Steps

1) Triage (lcc-incident-triage or lcc-router)
- If you have logs/symptoms, use `lcc-incident-triage` to summarize impact, evidence, hypotheses, and mitigations.
- Otherwise, use `lcc-router` to define repro steps and a plan.

2) Reproduce + fix (lcc-debugger)
- Delegate to `lcc-debugger`.
- Encourage using live-reload/watch tools (e.g., `dotnet watch`, `nodemon`, `pytest-watch`) in the background for real-time runtime bug detection and faster iteration.
- Require: minimal repro, root cause with evidence, smallest safe fix, verification commands and results.

3) Review (lcc-reviewer)
- Delegate to `lcc-reviewer`.
- If not LGTM, hand back to `lcc-debugger` or `lcc-coder` with a prioritized fix list.

4) Verify (lcc-tester)
- Delegate to `lcc-tester` to run `python -m pytest` (or repo-equivalent).
- If failing, hand off to `lcc-debugger`.

## Handoff envelope (required)
```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable tasks for the next agent"
}
```
