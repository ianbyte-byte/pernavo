# Swarm Global Rules (V2.2)

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 1) Goals
- Organize multi-agent collaboration using a Router–Worker architecture.
- Ensure continuity via a traceable handoff protocol.
- Leverage parallel execution and decentralized coordination via Agent Teams.

## 2) Role boundaries (mandatory)
- **Router**: routing, decomposition, acceptance criteria, and team lead only. No code edits, no test runs.
- **Coder**: implements changes. Must notify Reviewer and Lead when done.
- **Reviewer**: reviews security/correctness/maintainability. Does not edit files.
- **Tester**: runs/designs tests and produces repro steps. No large refactors.

## 3) Handoff protocol (mandatory for sequential work)
Each handoff must include a JSON object in the output:
```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|...",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable task list for the next agent"
}
```

## 4) Agent Teams (Experimental)
Agent teams allow parallel execution and decentralized coordination.

### Orchestration
- **Team Lead**: The main agent session. Responsible for spawning the team, approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows.
- **Shared Task List**: Use it to assign and track work. Teammates can self-claim tasks. Aim for 5-6 tasks per teammate.
- **Plan Approval**: For complex or risky tasks, use `Require plan approval before they make any changes`. The lead reviews plans autonomously.
- **Communication**:
  - `message <teammate>`: Direct message to a specific teammate.
  - `broadcast <message>`: Send to all teammates (use sparingly).

### UI Shortcuts
- `Shift+Down`: Cycle through teammates.
- `Ctrl+T`: Toggle the task list.
- `Enter`: View a teammate's session.
- `Escape`: Interrupt a teammate's turn.

### Display Modes
- `auto` (default): Uses split panes if inside tmux/iTerm2, otherwise in-process.
- `in-process`: All teammates run inside the main terminal.
- `tmux`: Each teammate gets its own pane (requires tmux or iTerm2).

### Parallel Patterns
- **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses and actively disprove each other.
- **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).
- **Cross-layer coordination**: Separate teammates for frontend, backend, and testing.

## 5) Hooks and Quality Gates
Automated checks are enforced via `.claude/hooks/lcc-quality-gate.sh`.
- **TaskCreated**: Rejects subjects < 10 characters or containing "TODO".
- **TaskCompleted**: Verifies that a summary or handoff report exists in the transcript.
- **TeammateIdle**: Ensures no work is left with unaddressed errors without resolution keywords (fixed/resolved/workaround).

## 6) Document-first workflow (mandatory)
Before any code changes for tasks involving platform APIs, prompt optimization, or Claude Code configuration:
- The Router must ensure relevant specs are reviewed first.
- The Coder must update `.claude/session_config.json` with requirements for JSON schema and context window optimization.

## 7) Project Subagents
Located in `.claude/agents/`. Teammates discover each other via `~/.claude/teams/{team-name}/config.json`.
RESPECT!
