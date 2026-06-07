# Claude Agent Swarm Guide v2.2

## 1. Definition

In a Claude Code workflow, an Agent Swarm can be implemented as a network of specialized roles coordinated by a Router and linked via a handoff protocol that preserves continuity. V2.2 leverages native **Agent Teams** for high-concurrency parallel exploration and implementation.

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

V2.2 leverages native Claude Code **Agent Teams** with decentralized coordination:

### 4.1 Orchestration
- **Router** acts as the team lead. It handles team creation, task decomposition, plan approval, and synthesis.
- **Teammates**: Spawn using specific agent types (e.g., `lcc-coder`, `lcc-reviewer`). They operate in independent context windows.
- **Context Injection**: Teammates do not inherit lead history. Spawn prompts must be self-contained and descriptive.
- **Plan Approval**: Enforce with `Require plan approval` for risky changes. Teammates work in read-only mode until the lead approves.
- **Task Sizing**: 5-6 tasks per teammate. Smaller tasks reduce risk; larger tasks reduce coordination overhead.

### 4.2 Advanced Patterns
- **Scientific Debate**: 5+ teammates. Focus on *anchoring* avoidance. Teammates must actively try to disprove each other's theories to find the true root cause.
- **Parallel Review**: Assign distinct "lenses" (Security, Performance, Test Coverage) to ensure thorough multi-dimensional auditing.
- **Cross-layer Coordination**: Horizontal split by stack layers (Frontend, Backend, DB, Tests) or vertical split by feature modules.

### 4.3 Coordination Mechanics
- **Shared Task List**: The source of truth for work status. Supports dependencies (blocking/unblocking).
- **Mailbox**: Enables direct peer-to-peer communication. Coder can message Reviewer directly without lead intervention.
- **Shutdown & Cleanup**:
  - Sequential: Shut down teammates first (`Ask... to shut down`).
  - Final: Lead runs `Clean up the team` only after all teammates have exited.
- **Display Modes**: Use `in-process` (default) or `split-panes` (requires tmux/iTerm2).

### 4.4 Automated Quality Gates
- `TaskCompleted` hook validates that a handoff report or summary exists in the transcript.
- `TeammateIdle` hook ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
