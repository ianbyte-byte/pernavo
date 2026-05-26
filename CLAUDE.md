# Swarm Global Rules (V2.2)

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 1) Goals
- Organize multi-agent collaboration using a Router–Worker architecture.
- Ensure continuity via a traceable handoff protocol or shared task list.

## 2) Role boundaries (mandatory)
- **Router (Lead)**: Routing, decomposition, acceptance criteria, team lifecycle management. No code edits.
- **Coder**: Implements changes. Must notify Reviewer (via handoff or mailbox) when done.
- **Reviewer**: Reviews security/correctness/maintainability. Does not edit files.
- **Tester**: Runs/designs tests and produces repro steps. No large refactors.

## 3) Agent Teams (V2.2)
Agent teams allow parallel execution and decentralized coordination.

- **Team Lead**: The main agent session (Router). Spawns the team, approves plans, synthesizes results.
- **Teammates**: Independent agents with their own context windows.
- **Display Modes**:
  - `in-process`: Cycle using `Shift+Down`.
  - `tmux`: Split-pane mode (set `teammateMode: "auto"`).
- **Shared Task List**: Centralized tracking. `Ctrl+T` to toggle. Teammates can self-claim tasks. Aim for 5-6 tasks per teammate.
- **Plan Approval**: For complex/risky tasks, use `Require plan approval before they make any changes`. Lead reviews/approves autonomously.
- **Communication**:
  - `message <teammate>`: Direct message.
  - `broadcast <message>`: Team-wide message.
- **Lifecycle**: Lead must shut down teammates (`Ask [teammate] to shut down`) and then run `Clean up the team`.
- **UI Shortcuts**: `Shift+Down` (cycle), `Ctrl+T` (tasks), `Enter` (view teammate), `Escape` (interrupt).

## 4) Handoff protocol (Single Agent Handoff)
Each handoff must include a JSON object:
```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable task list for the next agent"
}
```

## 5) Hooks and quality gates
- **TaskCreated**: Rejects subjects < 10 chars or containing "TODO".
- **TaskCompleted**: Verifies summary/report exists; rejects "TODO".
- **TeammateIdle**: Ensures no work is left with unaddressed errors.

## 6) Document-first workflow (mandatory)
Before any code changes for tasks involving platform APIs, prompt optimization, model selection, token budgets, context windows, rate limits, or Claude Code configuration:
- Router MUST ensure relevant specs in `.claude/docs/claud_platform_menu.md` are reviewed.
- Coder MUST update `.claude/session_config.json` before implementation.

## 7) Operational Principles
- **Think before acting.**
- **Be concise but thorough.**
- **Test your code before declaring done.**
- **Status Protocol**: End every single response with the character "RESPECT!" to signal instructions are followed.

RESPECT!
