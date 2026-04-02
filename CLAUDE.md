# Swarm Global Rules

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

## 5) Agent teams (Experimental)

Agent teams allow parallel execution and decentralized coordination.

- **Team lead**: The main agent session. Responsible for spawning the team, approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows. Inherit lead's permissions.
- **Discovery**: Teammates can discover other team members by reading the configuration file at `~/.claude/teams/{team-name}/config.json`.
- **Display Modes**:
  - `in-process`: Default. Teammates run in the main terminal.
  - `split panes`: Each teammate in its own pane (requires `tmux` or iTerm2).
  - Set via `teammateMode` in `.claude/settings.json`. Note: Split panes are not supported in VS Code, Windows Terminal, or Ghostty.
- **UI Shortcuts (Human/User only)**:
  - `Shift+Down`: Cycle through teammates and lead.
  - `Ctrl+T`: Toggle shared task list.
  - `Enter`: View teammate's session.
  - `Escape`: Interrupt teammate's turn.
- **Shared task list**: Use it to assign and track work. Teammates can self-claim tasks. Aim for 5-6 tasks per teammate to maximize productivity.
- **Plan Approval**: For complex or risky tasks (e.g., refactors), the lead should spawn teammates with `Require plan approval before they make any changes`. The lead reviews and approves/rejects plans autonomously.
- **Communication**:
  - `message <teammate>`: Send a direct message to a specific teammate (e.g., Coder to Reviewer).
  - `broadcast <message>`: Send to all teammates (use sparingly).
- **Cleanup**: One team per session. Once the task is complete, the lead must explicitly wait for teammates to finish, shut them down, and then run `Clean up the team`.
- **Parallel patterns**:
  - **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses and actively disprove each other.
  - **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).
  - **Cross-layer coordination**: Separate teammates for frontend, backend, and testing.

## 6) Hooks and quality gates

Automated checks are enforced via `.claude/settings.json` and `.claude/hooks/`.

- **TaskCompleted**: Fires when a task is closed. Used to verify completion criteria.
- **TeammateIdle**: Fires before a teammate stops. Used to ensure no work is left in a pending state.

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
