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

## 3) Handoff protocol (V2.2 Mandatory)

Each handoff must include a JSON object in the output following the Enhanced Handoff Schema:

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|...",
  "summary": {
    "progress": "Detailed summary of what was accomplished",
    "remaining": "What still needs to be done",
    "risks": "Potential blockers, risks, or critical failures",
    "changes": "Summary of files modified or created"
  },
  "next_instructions": "Actionable, concrete task list for the next agent",
  "acceptance_criteria": ["Criterion 1", "Criterion 2"],
  "context": {
    "metadata": "Optional key-value pairs for additional context"
  }
}
```

## 4) Handoff content requirements

- **Summary Object**: The `summary` field MUST be an object containing `progress`, `remaining`, `risks`, and `changes` as string values.
- **Actionability**: `next_instructions` must be specific (e.g., "Run `npm test` and fix failures in `Auth.js`" instead of "Continue working").
- **Acceptance Criteria**: Provide clear list of goals that must be met before the next handoff.
- **Safety**: Must not include secrets, tokens, or sensitive information.

## 5) Agent teams (Experimental)

Agent teams allow parallel execution and decentralized coordination.

- **Team lead**: The main agent session. Responsible for spawning the team, approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows. Teammates do NOT inherit the lead's conversation history; provide enough context in the spawn prompt.
- **Naming**: Use predictable names for teammates (e.g., "security-reviewer") to facilitate direct messaging.
- **Shared task list**: Use it to assign and track work. Teammates can self-claim tasks. Aim for 5-6 tasks per teammate to maximize productivity.
- **UI Shortcuts**:
  - `Up/Down Arrows`: Select a teammate in the agent panel.
  - `Shift+Down`: Cycle through teammates (legacy shortcut).
  - `Enter`: Open the selected teammate's transcript and message it directly.
  - `Ctrl+T`: Toggle the shared task list.
  - `Escape`: Interrupt the selected teammate's current turn.
- **Plan Approval**: For complex or risky tasks, spawn teammates with `Require plan approval before they make any changes`. The lead reviews and approves/rejects plans autonomously.
- **Communication**:
  - `message <teammate>`: Send a direct message to a specific teammate.
  - `broadcast <message>`: Send to all teammates.
- **Cleanup**: Shared directories are removed automatically when the session ends. No separate cleanup step required.
- **Parallel patterns**:
  - **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses and actively disprove each other.
  - **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).
  - **Cross-layer coordination**: Separate teammates for frontend, backend, and testing.
- **Limitations**:
  - **Session Resumption**: `/resume` and `/rewind` do NOT restore in-process teammates.
  - **Task Lag**: Task status can lag; update manually or nudge teammates if they appear stuck.

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
