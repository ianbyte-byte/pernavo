# Swarm Global Rules

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 1) Role boundaries (mandatory)

- **Router**: routing, decomposition, acceptance criteria, and team lead responsibilities. No code edits, no command runs (except read-only).
- **Coder**: implements changes. Must hand off to Reviewer or notify team when done.
- **Reviewer**: audits and suggests fixes (Security, Performance, Coverage). Does not edit files.
- **Tester**: runs/designs tests and produces repro steps. No large refactors.

## 2) Handoff protocol (mandatory for sequential work)

Each handoff (when not using an Agent Team) must include a JSON object in the output:

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|...",
  "summary": {
    "progress": "What was accomplished",
    "remaining": "Outstanding tasks",
    "risks": "Potential blockers",
    "changes": "Key file modifications"
  },
  "acceptance_criteria": [ "..." ],
  "next_instructions": "Specific, actionable task list",
  "context": {
    "risk_level": "low|medium|high"
  }
}
```

## 3) Agent teams (Experimental)

Agent teams allow parallel execution and decentralized coordination.

- **Team lead**: The main agent session (usually Router). Responsible for spawning, approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows.
- **Shared task list**: Use it to assign and track work. Teammates can self-claim tasks. Aim for 5-6 tasks per teammate.
- **UI Shortcuts**:
  - `Shift+Down`: Cycle through teammates.
  - `Ctrl+T`: Toggle the task list.
  - `Enter`: View a teammate's session.
  - `Escape`: Interrupt a teammate's current turn.
- **Plan Approval**: Use `Require plan approval` for complex tasks. The lead reviews and approves/rejects plans autonomously.
- **Communication**:
  - `message <teammate>`: Send a direct message (e.g., Coder to Reviewer).
  - `broadcast <message>`: Send to the entire team.
- **Cleanup**: The lead must shut down all teammates first, then run `Clean up the team`.

## 4) Hooks and quality gates

Automated checks are enforced via `.claude/hooks/`.

- **TaskCreated**: Rejects subjects < 10 chars or containing "TODO".
- **TaskCompleted**: Verifies that a summary or handoff report exists in the transcript.
- **TeammateIdle**: Ensures no work is left with unaddressed errors.

## 5) Document-first workflow (mandatory)

Before any code changes for tasks involving platform APIs, prompt optimization, model selection, or Claude Code configuration:

- Read relevant specs from `.claude/docs/claud_platform_menu.md`.
- Update `.claude/session_config.json` with constraints and requirements before implementing.

## 6) Operational Rules

1. **Think before acting.** Read existing files before writing code.
2. **Be concise in output but thorough in reasoning.**
3. **Prefer editing over rewriting whole files.**
4. **Test your code before declaring done.**
5. **No sycophantic openers or closing fluff.**
6. **Keep solutions simple and direct.**
