# Swarm Global Rules (V2.2)

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 1) Goals

- Organize multi-agent collaboration using a Router–Worker architecture
- Ensure continuity via a traceable handoff protocol (sequential) or shared task list (teams)

## 2) Role boundaries (mandatory)

- **Router**: Orchestration, decomposition, acceptance criteria, and team leadership. No code edits.
- **Coder**: Implements changes. Supports "read-only plan mode". Must notify Reviewer/Lead when done.
- **Reviewer**: Reviews security/correctness/maintainability. Does not edit files.
- **Tester**: Runs/designs tests and produces repro steps. No large refactors.

## 3) Handoff protocol (mandatory for sequential)

Each sequential handoff must include a JSON object in the output:

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|Architect|Product|SecurityReviewer",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable task list for the next agent"
}
```

## 4) Agent teams (Experimental - V2.2)

Agent teams allow parallel execution and decentralized coordination.

- **Team lead**: The main agent session (Router). Responsible for spawning the team, approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows.
- **Shared task list**: Use it to assign and track work. Teammates self-claim tasks.
- **Task Sizing**: Aim for **5-6 tasks per teammate** to maximize productivity.
- **Plan Approval**: For risky tasks, spawn teammates with `Require plan approval before they make any changes`. The lead reviews and approves/rejects plans.
- **Communication**:
  - `message <teammate>`: Send a direct message to a specific teammate.
  - `broadcast <message>`: Send to all teammates (use sparingly).
- **Cleanup Sequence**:
  1. Lead asks each teammate to shut down.
  2. Once all are closed, lead runs `Clean up the team`.
- **Parallel patterns**:
  - **Scientific Debate**: 5+ teammates investigate competing hypotheses and challenge each other.
  - **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Coverage).
  - **Cross-layer coordination**: Separate teammates for frontend, backend, and testing.

## 5) Hooks and quality gates

Automated checks are enforced via `.claude/settings.json` and `.claude/hooks/`.

- **TaskCreated**: Rejects subjects < 10 characters or containing "TODO".
- **TaskCompleted**: Verifies that a handoff report or summary exists in the transcript.
- **TeammateIdle**: Ensures no work is left in a pending state with unaddressed errors.

## 6) Document-first workflow (mandatory)

Before any tasks involving platform APIs, prompt optimization, model selection, token budgets, context windows, rate limits, structured outputs, or Claude Code configuration:

- The Router must ensure relevant specs are reviewed first (local docs preferred).
- The Coder must not start implementation until the session config is updated.
- Update `.claude/session_config.json` with requirements summary and spec links.

## 7) Failure handling

- If blocked, the summary must include: failure reason, repro steps, and a recommended fix path.
- In teams, notify the lead or broadcast to the team if a critical blocker is found.
