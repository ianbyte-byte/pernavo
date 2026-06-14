# Claude Agent Swarm Guide v2.2

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

## 4. Parallelization and Team Orchestration (V2)

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration:

### 4.1 Architecture
- **Team lead**: The session that creates the team. Coordinates work, assigns tasks, and synthesizes results.
- **Teammates**: Independent Claude Code instances. Each has its own context window and does not inherit the lead's conversation history.
- **Discovery**: Teammates can discover each other by reading `~/.claude/teams/{team-name}/config.json`.
- **Display**: Supports `in-process` (cycle with `Shift+Down`) and `split panes` (requires tmux/iTerm2).

### 4.2 Orchestration
- **Router as Lead**: The Router usually initiates the team.
- **Task Management**: Use the shared task list (`Ctrl+T` to toggle). Aim for 5-6 tasks per teammate.
- **Plan Approval**: Use `Require plan approval` for risky changes. The lead makes approval decisions autonomously.
- **Nudging**: If the lead starts working instead of delegating, use: `Wait for your teammates to complete their tasks before proceeding`.

### 4.3 Communication
- **Mailbox**: Asynchronous messaging system.
- **Direct Messaging**: Use `message <teammate_name>` for targeted coordination (e.g., Coder to Reviewer).
- **Predictability**: Tell the lead what to call each teammate in the spawn instruction for easier referencing.

### 4.4 Advanced Patterns
- **Scientific Debate**: 5+ teammates investigation. Key mechanism: "disprove each other's theories" to avoid anchoring bias.
- **Parallel Review**: Assign distinct "lenses" (Security, Performance, Test Coverage) to prevent overlapping work.
- **Cross-layer coordination**: Assign specialists for frontend, backend, and testing layers.

### 4.5 Team Lifecycle
- **Spawn**: Give teammates enough context in the spawn prompt.
- **Monitor**: Check progress and steer as needed.
- **Shutdown**: Teammates finish current tool calls before exiting.
- **Cleanup**: Lead runs `Clean up the team` only after all teammates are shut down.

### 4.6 Automated Quality Gates
- `TaskCompleted` hook validates that a handoff report or summary exists in the transcript.
- `TeammateIdle` hook ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
