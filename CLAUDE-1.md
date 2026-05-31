# Swarm Global Rules (V2.2)

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
  "next_role": "Router|Coder|Reviewer|Tester|...",
  "summary": {
    "progress": "What was accomplished",
    "remaining": "Outstanding tasks",
    "risks": "Potential blockers",
    "changes": "Key file modifications"
  },
  "acceptance_criteria": ["Criteria 1", "Criteria 2"],
  "next_instructions": "Specific, actionable task list",
  "context": { "platform_api_needed": false, "risk_level": "low" }
}
```

## 4) Handoff content requirements

- Must include: progress summary, next steps, and required context (files/commands/failure reasons)
- Must not include: secrets, tokens, or sensitive information

## 5) Agent teams

Agent teams allow parallel execution and decentralized coordination. Enable via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

- **Team lead**: The main agent session. Responsible for spawning the team, approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows.
  - **Context**: Teammates load project context (CLAUDE.md, etc.) but *not* conversation history. **Always provide rich, task-specific details in the spawn prompt.**
  - **Models**: Default is leader's model. Can be overridden in spawn prompt or `/config`. Sonnet is recommended for balance.
- **Shared task list**: Use it to assign and track work. Teammates can self-claim tasks. Aim for 5-6 tasks per teammate to maximize productivity.
- **Display Modes**:
  - `in-process`: Default. Use `Shift+Down` to cycle.
  - `tmux`: Split-pane mode. Requires tmux or iTerm2.
- **UI Shortcuts**: Use `Shift+Down` to cycle, `Ctrl+T` for task list, `Enter` to view, `Escape` to interrupt.
- **Plan Approval**: Use `Require plan approval before they make any changes` for complex tasks. Lead approves/rejects plans autonomously.
- **Communication**:
  - `message <teammate>`: Direct message.
  - `broadcast <message>`: Team-wide.
- **Cleanup**: Lead must shut down teammates first, then run `Clean up the team`.
- **Token Usage**: Scales linearly with teammates. Use teams for research/review/new features; single sessions for routine tasks.
- **Parallel patterns**:
  - **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses and actively disprove each other.
  - **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).
  - **Cross-layer coordination**: Separate teammates for frontend, backend, and testing.

## 6) Hooks and quality gates

Automated checks are enforced via `.claude/settings.json` and `.claude/hooks/`.

- **TaskCreated**: Rejects subjects < 10 characters or containing "TODO".
- **TaskCompleted**: Verifies handoff report in transcript and rejects "TODO".
- **TeammateIdle**: Ensures no unaddressed errors in transcript.

## 7) Failure handling & Troubleshooting

- **Stuck Tasks**: If a task lags, check the teammate's session and update status manually or nudge them.
- **Slow Shutdown**: Teammates finish current tool calls before exiting.
- **Orphaned Sessions**: Use `tmux ls` and `tmux kill-session -t <name>` if cleanup fails.
- If blocked, the summary must include: failure reason, repro steps, and a recommended fix path.

## 8) Document-first workflow (mandatory)

Before any code changes for tasks involving platform APIs, prompt optimization, model selection, token budgets, context windows, rate limits, structured outputs, or Claude Code configuration:

- The Router must ensure relevant specs are reviewed first.
- The Coder must not start implementation until the session config is updated.

### Instruction to (re)generate the menu doc

In Claude (chat) or Claude Code, run:

> Please visit `https://platform.claude.com/docs/en/home` and its core sub-pages (such as Prompt Engineering, Models, API Reference), extract all the core topics, and generate a Markdown format link menu document for me. The document should be categorized as 'Basic Concepts', 'Development Guidelines', and 'Performance Optimization', and retain the original URLs.

### Session pre-flight: Write requirements into `.claude/session_config.json`.
