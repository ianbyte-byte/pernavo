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

- **Team lead**: The main agent session. Responsible for spawning the team, assigning predictable names (e.g., `coder-1`), approving plans, and final synthesis.
- **Teammates**: Independent agents with their own context windows. Inherit lead's permissions at spawn. conversation history does not carry over.
- **Subagent Roles**: Reference subagent types (e.g., `lcc-coder`) when spawning to reuse specialized system prompts.
- **Shared task list**: Decentralized coordination. Teammates self-claim unblocked tasks. Aim for 5-6 tasks per teammate.
- **Plan Approval**: Lead reviews teammate plans before implementation. Approve if they meet criteria (tests, no breaks) or reject with feedback.
- **Communication**:
  - `message <teammate>`: Direct inter-agent communication.
  - `broadcast <message>`: Team-wide updates (use sparingly).
- **Shortcuts (UI)**:
  - `Shift+Down`: Cycle through teammates.
  - `Ctrl+T`: Toggle shared task list.
  - `Enter`: View teammate session.
  - `Escape`: Interrupt teammate.
- **Orchestration Sequence**: Wait for task completion -> shutdown teammates -> perform final synthesis -> `Clean up the team`.
- **Parallel patterns**:
  - **Scientific Debate**: 5+ teammates investigating competing hypotheses and challenging each other.
  - **Parallel Review**: Specialists (Security, Perf, Coverage) with distinct lenses.
  - **Parallel Implementation**: Teammates owning separate modules or layers.

## 6) Limitations & Troubleshooting

- **Session Resumption**: `/resume` and `/rewind` do not restore in-process teammates. If lead loses track, tell it to spawn new ones.
- **Task Status Lag**: Teammates may fail to mark tasks complete. Lead should nudge them or update manually.
- **Shutdown**: Graceful but can be slow as agents finish tool calls.
- **Cleanup**: Always run from Lead. Orphaned tmux sessions: `tmux kill-session -t <name>`.

## 7) Hooks and quality gates

Automated checks via `.claude/settings.json` and `.claude/hooks/`.

- **TaskCreated**: Reject subjects < 10 chars or containing "TODO".
- **TaskCompleted**: Verify handoff/summary/LGTM exists in transcript.
- **TeammateIdle**: Prevent idling with unaddressed errors.

## 8) Failure handling

- If blocked, the summary must include: failure reason, repro steps, and a recommended fix path

## 9) Document-first workflow (mandatory for platform/API/prompt/limits + Claude Code configuration)

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
