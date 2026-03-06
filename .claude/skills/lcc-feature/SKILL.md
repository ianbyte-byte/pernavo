---
name: lcc-feature
description: End-to-end feature workflow (requirements → design → implement → review → test) using project subagents.
disable-model-invocation: true
---

Run a full feature workflow in Claude Code using this repository’s subagents and the handoff envelope.

## Steps

1) Requirements (lcc-product)
- Use the `lcc-product` subagent to clarify scope and acceptance criteria.
- Capture the acceptance checklist in your main thread.

2) Design (lcc-architect)
- Use the `lcc-architect` subagent to propose a design, interfaces, and a migration plan.
- Choose a design and capture key decisions.

3) Routing (lcc-router)
- Use the `lcc-router` subagent to turn requirements + design into an execution plan.
- Router must output a handoff JSON pointing to the next role.

4) Implementation (lcc-coder)
- Delegate to `lcc-coder` to implement changes and update/add tests.
- Coder must output a handoff JSON to `Reviewer`.

5) Review (lcc-reviewer)
- Delegate to `lcc-reviewer` for security/correctness/maintainability review.
- If not LGTM, hand off back to `Coder` with a fix list.

6) Verification (lcc-tester)
- Delegate to `lcc-tester` to run tests and provide repro steps for any failures.
- If failing, hand off to `Coder`. If passing, hand off to `Reviewer` for final LGTM.

## Handoff envelope (required)
```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable tasks for the next agent"
}
```
