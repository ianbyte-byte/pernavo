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

## 4. Parallelization and Team Orchestration (V2.2)

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration:

### 4.1 Orchestration & Shortcuts
- **Router** acts as the team lead.
- **Shortcuts**: Use `Shift+Down` to cycle teammates, `Ctrl+T` to toggle tasks, and `Enter` to view sessions.
- **Display Modes**: Supports `in-process` (default) and `split-panes` (requires `tmux` or `iTerm2`).
- **Teammate Discovery**: Teammates can discover each other via `~/.claude/teams/{team-name}/config.json`.
- **Plan Approval**: Use `Require plan approval` for complex tasks. The lead acts as the authority, rejecting plans with "TODO" markers or missing tests.
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigate competing hypotheses and actively disprove each other's theories to avoid anchoring bias.
- **Parallel Review**: Specialists with distinct lenses (Security, Performance, Test Coverage) coordinate via the mailbox to avoid duplication.
- **Cross-layer coordination**: Independent teammates for frontend, backend, and testing working in parallel.

### 4.3 Coordination & Lifecycle
- **Shared Task List**: Decentralized task tracking with dependency support.
- **Mailbox**: Inter-agent messaging via `message <teammate>` (direct) and `broadcast` (team-wide).
- **Mandatory Lifecycle**:
  1. Wait for completion (`Wait for your teammates to finish before proceeding`).
  2. Final Synthesis of findings/code.
  3. Shutdown teammates (`Ask <teammate> to shut down`).
  4. Lead runs `Clean up the team`.

### 4.4 Troubleshooting
- **Orphaned Sessions**: Use `tmux ls` and `tmux kill-session -t <name>` if cleanup fails.
- **Resumption**: `/resume` does not restore in-process teammates; spawn new ones if needed.

### 4.4 Automated Quality Gates
- `TaskCompleted` hook validates that a handoff report or summary exists in the transcript.
- `TeammateIdle` hook ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
