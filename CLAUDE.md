# Swarm Global Rules (V2.2)

## 1) Goals

- Organize multi-agent collaboration using a Router–Worker architecture
- Ensure continuity via a traceable handoff protocol
- Leverage Agent Teams for parallel and adversarial exploration

## 2) Role boundaries (mandatory)

- Router: Team Lead. Routing, decomposition, plan approval, synthesis, and cleanup. No code edits.
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

- **Team lead**: The main agent session. Responsible for spawning the team, approving plans, synthesis, and cleanup.
- **Teammates**: Independent agents with their own context windows. They do NOT inherit lead's history.
- **Configuration**: `teammateMode` ("auto", "in-process", "tmux") in `.claude/settings.json` or `~/.claude.json`.
- **Shared task list**: Use it to assign and track work. Teammates can self-claim tasks. Aim for 5-6 tasks per teammate to maximize productivity.
  - *User/Human Lead*: Use `Shift+Down` to cycle teammates, `Ctrl+T` to toggle task list, `Enter` to view teammate, and `Escape` to interrupt.
- **Plan Approval**: For complex/risky tasks, spawn teammates with `Require plan approval before they make any changes`.
  - Lead approves/rejects plans autonomously based on criteria (e.g., "must include tests").
- **Communication (Mailbox)**:
  - `message <teammate>`: Send a direct message.
  - `broadcast <message>`: Send to all teammates simultaneously.
- **Orchestration Patterns**:
  - **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses and actively disprove each other.
  - **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).
  - **Cross-layer coordination**: Separate teammates for frontend, backend, and testing.
- **Cleanup (Mandatory)**: Lead must: 1. Wait for completion. 2. Perform final synthesis. 3. Shut down teammates. 4. Run `Clean up the team`.
- **Known Limitations**:
  - `/resume` and `/rewind` do not restore in-process teammates.
  - Task status can lag; nudge teammates if they appear stuck.
  - Shutdown is sequential and may be slow.

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
