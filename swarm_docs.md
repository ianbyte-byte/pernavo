# Claude Agent Swarm Guide v2.1

## 1. Definition

In a Claude Code workflow, an Agent Swarm can be implemented as a network of specialized roles coordinated by a Router and linked via a handoff protocol that preserves continuity.

Core capabilities:
- Handoffs: one specialist finishes a phase and hands control to the next
- Parallelization: multiple specialists can be queried in parallel for comparison/verification, then synthesized by Router (or an integrator)
- Shared context: all roles rely on the same project rules and artifacts (for example `CLAUDE.md` + `.claude/session_config.json`)

## 2. Reference implementation (this repository)

### 2.1 Architecture: Router–Worker
- Router: understands the goal, decomposes tasks, selects the next agent, defines acceptance criteria
- Workers:
  - Coder: implements changes
  - Reviewer: audits and suggests fixes
  - Tester: verifies with tests and repro steps

### 2.2 Key artifacts
- `CLAUDE.md`: global rules (role boundaries, handoff schema, agent teams, hooks)
- `.claude/agents/`: Claude Code subagents (Router/Coder/Reviewer/Tester + specialists)
- `.claude/skills/`: Claude Code skills (including the `/swarm` workflow)
- `.claude/settings.json`: project settings (enables agent teams and hooks)
- `.claude/hooks/`: automated quality gate scripts
- `.claude/session_config.json`: per-session pre-flight notes required by the document-first workflow

### 2.3 Key CLI helpers (optional)
The Python package provides a small CLI to validate workflow artifacts:
- `chung-swarm check`: verify required files exist
- `chung-swarm session-config validate`: validate `.claude/session_config.json`
- `chung-swarm handoff validate`: validate a handoff envelope pasted from output

### 2.3 Running with Claude Code (project configuration)

This repo includes Claude Code project configuration for running the swarm directly:
- `.claude/agents/`: project subagents (YAML frontmatter + system prompt)
- `.claude/skills/swarm/`: the `/swarm` workflow skill (manual invocation)

## 3. Handoff protocol

Each handoff must include a JSON object:

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": "Progress summary",
  "next_instructions": "Actionable tasks for the next agent"
}
```

Recommended constraints:
- `summary` must include: done, todo, risks/blockers
- `next_instructions` must be actionable (not just “continue”)

## 4. Parallelization and Team Orchestration (V2.2)

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration and best practices from official documentation:

### 4.1 Orchestration
- **Router** acts as the team lead.
- Use `Create an agent team...` prompts to parallelize work.
- **Plan Approval**: Use `Require plan approval` for complex or risky tasks. The lead reviews and approves/rejects plans autonomously before implementation begins.
- **Task Sizing**: Aim for 5-6 tasks per teammate to keep everyone productive without excessive context switching.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses and actively challenging/disproving each other's theories.
- **Parallel Review**: Specialists for Security, Performance, and Test Coverage reviewing the same changes through distinct lenses.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel on independent components.

### 4.3 Coordination
- **Shared Task List**: decentralized task tracking (pending, in progress, completed).
- **Avoid File Conflicts**: Break work so each teammate owns a different set of files.
- **Wait for Finished**: The lead must wait for teammates to complete tasks before proceeding with final synthesis or implementation.
- **Mailbox**: inter-agent messaging via `message <teammate>` (direct) and `broadcast` (team-wide).
- **Cleanup**: The lead must ask teammates to shut down first, then run `Clean up the team` after completion.

### 4.4 Automated Quality Gates
- `TaskCreated`: Validates task subjects (minimum 10 characters, no "TODO").
- `TaskCompleted`: Validates that a handoff report, summary, or "LGTM" exists in the transcript.
- `TeammateIdle`: Ensures teammates don't go idle with unaddressed errors in the transcript.

### 4.5 Best Practices & Troubleshooting
- **Context**: Include task-specific details and specs in the spawn prompt. Teammates load project context (CLAUDE.md) but not the lead's conversation history.
- **Task Lag**: If a task appears stuck, check the teammate's session (Shift+Down) or nudge them.
- **Premature Shutdown**: If the lead tries to clean up before work is done, tell it to keep going.
- **Orphaned Sessions**: If tmux sessions persist, use `tmux kill-session -t <session-name>`.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
