# Swarm Global Rules

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 1) Goals

- Organize multi-agent collaboration using a Router–Worker architecture
- Ensure continuity via a traceable handoff protocol

## 2) Role boundaries (mandatory)

- Router: routing, decomposition, acceptance criteria only. No code edits, no test runs.
- Coder: implements changes. Must hand off to Reviewer when done.
- Reviewer: reviews security/correctness/maintainability. Does not edit files.
- Tester: runs/designs tests and produces repro steps. No large refactors.

## 3) Handoff protocol (mandatory)

Each handoff must include a JSON object in the output:

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable task list for the next agent"
}
```

## 4) Handoff content requirements

- Must include: progress summary, next steps, and required context (files/commands/failure reasons)
- Must not include: secrets, tokens, or sensitive information

## 5) Agent teams (V2.2)

Agent teams allow parallel execution and decentralized coordination.

- **Team lead**: The main agent session. Responsible for spawning the team, approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows.
- **Shared task list**: Use it to assign and track work. Teammates can self-claim tasks. Aim for 5-6 tasks per teammate to maximize productivity.
- **UI Shortcuts**:
  - `Shift+Down`: Cycle through teammates.
  - `Ctrl+T`: Toggle the task list.
  - `Enter`: View a teammate's session.
  - `Escape`: Interrupt a teammate's turn.
- **Display Modes**: Configurable via `teammateMode` in `settings.json` (`auto`, `in-process`, `tmux`).
- **Plan Approval**: For complex or risky tasks, the lead should spawn teammates with `Require plan approval before they make any changes`. The lead reviews and approves/rejects plans autonomously.
- **Discovery**: Teammates can discover others via reading `~/.claude/teams/{team-name}/config.json`.
- **Communication**:
  - `message <teammate>`: Send a direct message to a specific teammate.
  - `broadcast <message>`: Send to all teammates (use sparingly).
- **Coordination Commands**:
  - `Wait for your teammates to complete their tasks before proceeding`: Synchronizes the lead with the team.
  - `Clean up the team`: Removes shared resources after shutting down teammates.
- **Parallel patterns**:
  - **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses and actively "disprove each other's theories".
  - **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).
  - **Cross-layer coordination**: Separate teammates for frontend, backend, and testing.

## 6) Hooks and quality gates

Automated checks are enforced via `.claude/settings.json` and `.claude/hooks/`.

- **TaskCreated**: Fires when a task is being created. Rejects subjects < 10 characters or containing "TODO".
- **TaskCompleted**: Fires when a task is closed. Verifies that a summary or handoff report exists in the transcript and rejects "TODO" in subjects.
- **TeammateIdle**: Fires before a teammate stops. Ensures no work is left with unaddressed errors.

## 7) Failure handling

- If blocked, the summary must include: failure reason, repro steps, and a recommended fix path

## 8) Document-first workflow (mandatory)

Before any code changes for tasks involving platform APIs or Claude Code configuration:

- The Router must ensure relevant specs are reviewed first.
- The Coder must not start implementation until the session config is updated.

### Document index (project)

- Primary: `.claude/docs/claud_platform_menu.md`

### Session pre-flight (required)

Before `lcc-coder` writes code, it must summarize requirements into `.claude/session_config.json`.
