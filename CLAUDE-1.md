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

## 5) Agent Teams & Swarm Orchestration (V2.2)

Agent teams (v2.1.32+) allow parallel execution and decentralized coordination. Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

- **Roles & Setup**:
  - **Team lead**: The main agent session. Coordinates work, assigns tasks, and synthesizes results.
  - **Teammates**: Independent Claude instances with their own context windows. Discoverable via `~/.claude/teams/{team-name}/config.json`.
  - **Display Modes**: Configure `teammateMode` in `settings.json` (`auto`, `in-process`, `tmux`).
- **Coordination**:
  - **Shared task list**: Decentralized task tracking. Aim for 5-6 tasks per teammate.
  - **Wait Command**: Use "Wait for your teammates to complete their tasks before proceeding" if the lead starts work prematurely.
  - **Plan Approval**: Use `Require plan approval` for complex tasks. Lead approves/rejects plans in read-only mode.
- **Communication**:
  - `message <teammate>`: Direct inter-agent messaging.
  - `broadcast <message>`: Team-wide notification (use sparingly).
- **UI Shortcuts**: `Shift+Down` (cycle), `Ctrl+T` (toggle tasks), `Enter` (view), `Escape` (interrupt).
- **Parallel patterns**:
  - **Scientific Debate**: 5+ teammates investigating competing hypotheses. Instruction: "try to disprove each other's theories".
  - **Parallel Review**: Specialists for Security, Performance, and Test Coverage.
  - **Cross-layer coordination**: Frontend, Backend, and Tests specialists.
- **Cleanup**: Lead must shut down teammates by name first, then run `Clean up the team`.
- **Limitations**:
  - One team at a time. No nested teams.
  - No session resumption (`/resume`) for in-process teammates.
  - Shutdown can be slow (waits for current tool call).

## 6) Hooks and quality gates

Automated checks are enforced via `.claude/settings.json` and `.claude/hooks/`.

- **TaskCreated**: Fires when a task is being created. Rejects subjects < 10 characters or containing "TODO".
- **TaskCompleted**: Fires when a task is closed. Verifies that a summary or handoff report exists in the transcript and rejects "TODO" in subjects.
- **TeammateIdle**: Fires before a teammate stops. Ensures no work is left with unaddressed errors.

## 7) Failure handling

- If blocked, the summary must include: failure reason, repro steps, and a recommended fix path

## 8) Document-first workflow (mandatory for platform/API/prompt/limits + Claude Code configuration)

Before any code changes for tasks involving platform APIs, prompt optimization, model selection, token budgets, context windows, rate limits, structured outputs, or Claude Code configuration (subagents/skills/hooks/permissions):

- The Router must ensure relevant specs are reviewed first (local docs preferred).
- The Coder must not start implementation until the session config is updated (see below).

### Document index (project)

- Primary: `.claude/docs/claud_platform_menu.md`

### Instruction to (re)generate the menu doc

In Claude (chat) or Claude Code, run:

> Please visit `https://platform.claude.com/docs/en/home` and its core sub-pages (such as Prompt Engineering, Models, API Reference), extract all the core topics, and generate a Markdown format link menu document for me. The document should be categorized as 'Basic Concepts', 'Development Guidelines', and 'Performance Optimization', and retain the original URLs.

### “Read the book first, then do the work” starter instruction

When starting a development task, use:

> Based on the best practices outlined in the relevant specifications linked in `.claude/docs/claud_platform_menu.md`, please perform the following tasks: [your requirements].

### Session pre-flight (required)

Before `lcc-coder` writes code, it must summarize requirements from the relevant specs regarding:

- JSON schema definition (structured outputs / tool input schemas)
- Context window optimization (token budgets, long context, caching/compaction strategies)

and write them into:

- `.claude/session_config.json`
