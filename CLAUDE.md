# CLAUDE.md - Swarm Global Rules (V2.2)

## First Principle: Intent-Driven Minimalism
- **Code is Liability:** Never write a line of code that doesn't need to exist. Prefer reusing existing patterns over creating new abstractions.
- **Truth over Assumption:** The codebase and the execution environment are the only sources of truth. Always verify assumptions by reading files or running tests before proposing changes.
- **Solve the Problem, Not the Ticket:** Understand the "why" behind a request. If a requested change contradicts system integrity or introduces unnecessary complexity, propose a simpler alternative.
- **Atomic & Reversible:** Every intervention should be as small as possible and easy to roll back.

## 1) Goals
- Organize multi-agent collaboration using a Router–Worker architecture.
- Ensure continuity via a traceable handoff protocol.

## 2) Role boundaries (mandatory)
- **Router**: routing, decomposition, acceptance criteria only. No code edits, no test runs.
- **Coder**: implements changes. Must hand off to Reviewer when done.
- **Reviewer**: reviews security/correctness/maintainability. Does not edit files.
- **Tester**: runs/designs tests and produces repro steps. No large refactors.

## 3) Handoff protocol (mandatory)
Each handoff must include a JSON object in the output using the following schema:
```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|Architect|...",
  "summary": {
    "progress": "string",
    "remaining": "string",
    "risks": "string",
    "changes": "string"
  },
  "acceptance_criteria": ["string"],
  "next_instructions": "string",
  "context": {
    "platform_api_needed": boolean,
    "risk_level": "low|medium|high"
  }
}
```

## 4) Agent Teams (Experimental)
Agent teams allow parallel execution and decentralized coordination.

- **Enablement**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `.claude/settings.json`.
- **Team Lead**: The main agent session. Responsible for spawning the team, approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows. Discovered via `~/.claude/teams/{team-name}/config.json`.
- **Display Modes**:
  - `in-process`: Default. Use `Shift+Down` to cycle.
  - `tmux` / `split-pane`: Each teammate in its own pane. Configure `teammateMode` in settings.
- **UI Shortcuts**:
  - `Shift+Down`: Cycle through teammates.
  - `Ctrl+T`: Toggle the shared task list.
  - `Enter`: View a teammate's session.
  - `Escape`: Interrupt a teammate's current turn.
- **Plan Approval**: Use `Require plan approval before they make any changes` for complex tasks. The lead reviews and approves/rejects plans autonomously.
- **Communication**:
  - `message <teammate>`: Direct message to a specific teammate.
  - `broadcast <message>`: Message to all teammates.
- **Cleanup**: Lead must ask teammates to shut down first, then run `Clean up the team`.
- **Patterns**:
  - **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses and disprove each other.
  - **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).

## 5) Hooks and Quality Gates
Automated checks are enforced via `.claude/hooks/lcc-quality-gate.sh`.
- **TaskCreated**: Rejects short subjects or those containing "TODO".
- **TaskCompleted**: Verifies handoff report exists in transcript; rejects "TODO".
- **TeammateIdle**: Ensures no unaddressed errors remain before idling.

## 6) Document-first workflow (mandatory)
Before any code changes for tasks involving platform APIs, prompt optimization, or Claude Code configuration:
- The **Router** must ensure relevant specs (e.g., `.claude/docs/claud_platform_menu.md`) are reviewed.
- The **Coder** must write requirements into `.claude/session_config.json` before implementing.

RESPECT!
