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

Agent teams allow parallel execution and decentralized coordination. Enable via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

- **Team lead**: The main session. Responsible for spawning, task decomposition, plan approval, and final synthesis. One team per session.
- **Teammates**: Independent sessions with separate context windows. Teammates load `CLAUDE.md`, MCP servers, and skills, but **do not inherit lead conversation history**. Include full context in spawn prompts.
- **Display Modes**:
  - `in-process` (default): Use `Shift+Down` to cycle, `Enter` to view, `Escape` to interrupt, `Ctrl+T` for tasks.
  - `split panes`: Requires `tmux` or iTerm2 (`teammateMode: "tmux"` in `settings.json`).
- **Shared task list**: decentralized tracking. Teammates self-claim or lead assigns. Aim for 5-6 tasks/teammate.
- **Plan Approval**: Use `Require plan approval` for implementation. The lead reviews/approves plans before any changes.
- **Communication**: Use `message <teammate>` (direct) or `broadcast <message>` (all).
- **Cleanup**: Lead must shut down teammates first, then run `Clean up the team`.
- **Parallel patterns**:
  - **Scientific Debate**: 5+ teammates investigate competing hypotheses and challenge each other.
  - **Parallel Review**: Assign distinct lenses (Security, Performance, Coverage).
  - **Cross-layer coordination**: Separate teammates for frontend, backend, and testing.
- **Troubleshooting**:
  - Teammates stop on errors: Check output via `Shift+Down` and message them directly.
  - Orphaned tmux: Run `tmux kill-session -t <name>`.
  - Task lag: Update status manually or nudge the teammate via lead.
- **Limitations**: No session resumption (`/resume`) for in-process teammates; no nested teams.

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
