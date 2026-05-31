# Claude Agent Swarm Guide v2.2

## 1. Definition

In a Claude Code workflow, an Agent Swarm can be implemented as a network of specialized roles coordinated by a Router and linked via a handoff protocol that preserves continuity.

Core capabilities:
- Handoffs: one specialist finishes a phase and hands control to the next.
- Parallelization: multiple specialists can be queried in parallel for comparison/verification, then synthesized by Router.
- Shared context: all roles rely on the same project rules and artifacts (`CLAUDE.md`, `CLAUDE-1.md`).

## 2. Reference implementation (this repository)

### 2.1 Architecture: Router–Worker
- **Router**: understands the goal, decomposes tasks, selects agents, defines acceptance criteria.
- **Workers**:
  - **Coder**: implements changes.
  - **Reviewer**: audits and suggests fixes.
  - **Tester**: verifies with tests and repro steps.

### 2.2 Key artifacts
- `CLAUDE.md`: project engineering guidelines.
- `CLAUDE-1.md`: Swarm global rules (handoff schema, team coordination, hooks).
- `.claude/agents/`: Claude Code subagents (Router/Coder/Reviewer/Tester + specialists).
- `.claude/skills/`: Claude Code skills (including the `/swarm` workflow).
- `.claude/settings.json`: project settings (enables agent teams and hooks).
- `.claude/hooks/`: automated quality gate scripts (`lcc-quality-gate.sh`).
- `.claude/session_config.json`: per-session pre-flight notes.

### 2.3 Key CLI helpers
The Python package provides a CLI to validate workflow artifacts:
- `PYTHONPATH=src python -m chung_agent_swarm.cli check`: verify required files exist.
- `PYTHONPATH=src python -m chung_agent_swarm.cli handoff new`: generate a V2.2 handoff envelope.

## 3. Handoff protocol (V2.2)

Each handoff must include the enhanced JSON envelope:

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": {
    "progress": "Detailed accomplishment list",
    "remaining": "Pending tasks",
    "risks": "Potential blockers",
    "changes": "Modified files"
  },
  "acceptance_criteria": ["Criteria 1", "Criteria 2"],
  "next_instructions": "Actionable tasks",
  "context": { "risk_level": "medium" }
}
```

## 4. Team Orchestration (V2.2)

V2.2 leverages native **Agent Teams** for high-concurrency tasks:

### 4.1 Orchestration & Management
- **Router as Lead**: Orchestrates spawning, task assignment, and synthesis.
- **Context Handling**: Teammates do NOT inherit history. The lead must pass explicit context in the spawn prompt.
- **Models**: Default to lead's model. Sonnet is preferred for teammates to ensure balance.
- **Plan Approval**: Mandatory for complex/risky tasks via `Require plan approval`. Lead reviews plans autonomously.
- **Task Sizing**: 5-6 tasks per teammate to maximize productivity without overloading.

### 4.2 Parallel Patterns
- **Scientific Debate**: 5+ teammates investigated competing hypotheses and challenging each other.
- **Parallel Review**: Specialists for Security, Performance, and Test Coverage.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel.

### 4.3 Coordination & Display
- **Task List**: Shared via `Ctrl+T`. Teammates self-claim unblocked tasks.
- **Messaging**: `message <name>` for direct communication; `broadcast` for team-wide updates.
- **Display Mode**: `in-process` (default) or `tmux` (split-panes). Configurable in `settings.json`.
- **Cleanup**: Lead must shut down teammates first, then run `Clean up the team`.

### 4.4 Troubleshooting
- **Stuck Tasks**: Teammates may fail to mark tasks complete. Update manually or nudge the teammate.
- **Orphaned tmux**: If cleanup fails, manually kill sessions via `tmux kill-session`.
- **Slow Shutdown**: Teammates finish current tool calls before exiting.
- **No Resumption**: `/resume` does not restore in-process teammates. Re-spawn if needed.

## 5. Testing & Quality
- **Automated Gates**: `TaskCompleted` verifies handoff reports; `TeammateIdle` prevents exiting with errors.
- **TDD Workflow**: Coder implements → Tester verifies → Reviewer audits → Router synthesizes.
