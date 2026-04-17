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

## 5) Agent teams (Experimental)

Agent teams allow parallel execution and decentralized coordination for tasks where parallel exploration adds value.

- **Enablement**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`.
- **Team Lead**: The session that creates the team. Responsible for:
  - Spawning teammates with clear roles and model selection (Sonnet preferred).
  - Task decomposition: Breaking work into 5-6 self-contained tasks per teammate.
  - **Autonomous Plan Approval**: For complex/risky tasks, spawn with `Require plan approval before they make any changes`. The lead approves plans based on criteria (e.g., "include test coverage", "no breaking changes").
  - **Coordination & Synthesis**: Monitoring progress, nudging stuck teammates, and synthesizing final results.
  - **Shutdown & Cleanup**: Shutting down teammates gracefully (`Ask the [Name] teammate to shut down`) before running `Clean up the team`.
- **Teammates**: Independent Claude Code sessions.
  - **Context**: They load `CLAUDE.md`, skills, and MCP servers but NOT the lead's history. Provide task-specific context in the spawn prompt.
  - **Task Claiming**: Teammates can self-claim unassigned, unblocked tasks from the **shared task list**. Use file locking to prevent race conditions.
  - **Messaging**:
    - `message <name>`: Send direct messages for peer coordination (e.g., Coder to Reviewer).
    - `broadcast <message>`: Send to all teammates (use sparingly; costs scale with team size).
- **Advanced Patterns**:
  - **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses. Teammates must talk to each other to try to disprove theories.
  - **Parallel Review**: Assign reviewers distinct domains (Security, Performance, Coverage) for thorough attention.
  - **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel.
- **Limitations**: No session resumption (`/resume`) for in-process teammates; task status can sometimes lag.

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
