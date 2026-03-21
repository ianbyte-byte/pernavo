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

## 5) Agent teams (Experimental V2.2)

Agent teams allow parallel execution and decentralized coordination.

- **Enablement**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`.
- **Display Modes**:
  - `in-process`: All teammates in one terminal (default).
  - `split-panes`: Requires `tmux` or `iTerm2`. Set `teammateMode: "tmux"` in `settings.json`.
- **Shortcuts**:
  - `Shift+Down`: Cycle through teammates and lead.
  - `Ctrl+T`: Toggle shared task list.
  - `Enter`: View a teammate's session.
  - `Escape`: Interrupt a teammate's current turn.
- **Team Lead**: The main session. Responsible for spawning, task assignment, plan approval, synthesis, and cleanup.
- **Teammates**: Independent agents. Discovery via `~/.claude/teams/{team-name}/config.json`.
- **Permissions**: Teammates inherit the lead's permission settings at spawn time.
- **Shared Task List**: decentralized tracking. Teammates self-claim tasks. Aim for 5-6 tasks per teammate.
- **Plan Approval**: Use `Require plan approval before they make any changes` for complex tasks.
  - Lead approves plans autonomously based on criteria (e.g., "no TODOs", "include tests").
  - Teammates stay in read-only plan mode until approved.
- **Communication**:
  - `message <teammate>`: Direct message between agents.
  - `broadcast <message>`: Team-wide announcement (scales cost).
- **Mandatory Lifecycle**:
  1. Lead waits for all teammates to finish.
  2. Lead performs final synthesis.
  3. Lead shuts down all teammates (`Ask <teammate> to shut down`).
  4. Lead runs `Clean up the team`.
- **Parallel Patterns**:
  - **Scientific Debate**: 5+ teammates investigate competing hypotheses and challenge each other's theories to avoid anchoring bias.
  - **Parallel Review**: Specialists with distinct lenses (Security, Performance, Test Coverage).
  - **Cross-layer coordination**: Independent teammates for frontend, backend, and testing.

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
