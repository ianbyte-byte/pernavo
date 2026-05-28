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

- **Router**: routing, decomposition, acceptance criteria only. No code edits, no test runs.
- **Coder**: implements changes. Must hand off to Reviewer when done.
- **Reviewer**: reviews security/correctness/maintainability. Does not edit files.
- **Tester**: runs/designs tests and produces repro steps. No large refactors.

## 3) Handoff protocol (mandatory)

Each handoff must include a JSON object in the output:

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|Architect|AiNativeArchitect|Product|SecurityReviewer|Debugger|Refactorer|PerformanceOptimizer|SqlOptimizer|DocsWriter|ReleaseManager|IncidentTriage|DependencyUpgrader|GitWorktreeManager|Simplifier",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable task list for the next agent"
}
```

## 4) Handoff content requirements

- Must include: progress summary, next steps, and required context (files/commands/failure reasons).
- Must not include: secrets, tokens, or sensitive information.

## 5) Agent Teams (V2.2)

Agent teams allow parallel execution and decentralized coordination.

- **Team Lead**: The main agent session. Responsible for spawning the team, assigning tasks, approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows.
- **Enabling**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`.
- **Display Modes**:
  - `in-process`: All teammates run in one terminal. Use `Shift+Down` to cycle.
  - `split panes`: Requires `tmux` or `iTerm2`. Set `teammateMode: "tmux"` or `"auto"` in `settings.json`.
- **UI Shortcuts**:
  - `Shift+Down`: Cycle through teammates (Lead -> Teammate 1 -> ... -> Lead).
  - `Ctrl+T`: Toggle the shared task list.
  - `Enter`: View a teammate's full session output.
  - `Escape`: Interrupt a teammate's current turn.
- **Shared Task List**:
  - Use it to assign and track work. Teammates can self-claim tasks.
  - **Task Dependencies**: Pending tasks with unresolved dependencies cannot be claimed until unblocked.
  - Aim for 5-6 tasks per teammate to maximize productivity.
- **Plan Approval**: For complex or risky tasks, the lead should spawn teammates with `Require plan approval before they make any changes`. The lead reviews and approves/rejects plans autonomously.
- **Communication**:
  - `message <teammate>`: Send a direct message to a specific teammate.
  - `broadcast <message>`: Send to all teammates (use sparingly).
- **Permissions**: Teammates inherit the lead's permission settings (e.g., `--dangerously-skip-permissions`).
- **Cleanup**: The lead must shut down all teammates first, then run `Clean up the team`.
- **Parallel Patterns**:
  - **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses and actively disprove each other.
  - **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).
  - **Cross-layer Coordination**: Separate teammates for frontend, backend, and testing.

## 6) Hooks and Quality Gates

Automated checks are enforced via `.claude/settings.json` and `.claude/hooks/`.

- **TaskCreated**: Rejects subjects < 10 characters or containing "TODO".
- **TaskCompleted**: Verifies that a summary or handoff report exists in the transcript and rejects "TODO" in subjects.
- **TeammateIdle**: Ensures no work is left with unaddressed errors.

## 7) Failure handling

- If blocked, the summary must include: failure reason, repro steps, and a recommended fix path.

## 8) Document-first workflow (mandatory)

Before any code changes for tasks involving platform APIs, prompt optimization, model selection, token budgets, context windows, rate limits, structured outputs, or Claude Code configuration:

- The Router must ensure relevant specs are reviewed first (local docs preferred).
- The Coder must not start implementation until the session config is updated.

### Session Pre-flight (required)

Before `lcc-coder` writes code, it must summarize requirements regarding JSON schemas and context window optimization into `.claude/session_config.json`.
