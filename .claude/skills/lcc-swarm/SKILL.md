---
name: lcc-swarm
description: Run a Swarm workflow in Claude Code using Router/Coder/Reviewer/Tester roles.
disable-model-invocation: true
---

Run the Swarm workflow conventions for this repository: break complex tasks into routing, implementation, review, and testing stages, connected by a handoff JSON envelope.

## Workflow

1. Start with lcc-router
   - Have Router break down the task, define acceptance criteria, and output a handoff JSON pointing to the next role

2. Follow Router's handoff and delegate to lcc-coder
   - Coder implements and edits files, then outputs a handoff JSON to lcc-reviewer

3. Delegate to lcc-reviewer
   - Reviewer does not edit files; review and recommendations only. If acceptable, output LGTM and hand off to lcc-tester. If not, hand off back to lcc-coder.

4. Delegate to lcc-tester
   - Tester runs tests and provides repro steps. If failing, hand off to lcc-coder to fix. If passing, hand off to lcc-reviewer or lcc-router to wrap up.

## Handoff envelope (required)

Each handoff must include JSON:

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable task list for the next agent"
}
```

## Notes

- Project subagents live in `.claude/agents/`: lcc-router / lcc-coder / lcc-reviewer / lcc-tester
- For parallel research, run multiple read-only agents (e.g., Explore or lcc-router) on separate areas, then have Router synthesize and proceed to implementation.
- For a complete index of workflows, run `/workflow-index`.
