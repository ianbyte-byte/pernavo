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

## 3. Handoff protocol (V2.2)

Each handoff must include a JSON object following the **Enhanced Handoff Schema**:

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": {
    "progress": "Detailed summary of what was accomplished",
    "remaining": "What still needs to be done",
    "risks": "Potential blockers, risks, or critical failures",
    "changes": "Summary of files modified or created"
  },
  "next_instructions": "Actionable, concrete task list for the next agent",
  "acceptance_criteria": ["Criterion 1", "Criterion 2"],
  "context": {
    "metadata": "Optional metadata"
  }
}
```

Recommended constraints:
- `summary` MUST be an object with the four mandatory keys: `progress`, `remaining`, `risks`, `changes`.
- `next_instructions` must be actionable (not just “continue”).
- `acceptance_criteria` should be used to define "done" for the next phase.

## 4. Parallelization and Team Orchestration (V2.2)

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration:

### 4.1 Orchestration
- **Router** acts as the team lead.
- Use `Spawn [X] teammates...` prompts to parallelize work.
- **Context Discovery**: Router reads `.claude/docs/claud_platform_menu.md` to identify relevant specifications before routing.
- **Plan Approval**: Use `Require plan approval` for complex/risky tasks. The lead reviews and approves/rejects plans before implementation begins.
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity.
- **Predictable Naming**: Assign clear names (e.g., "frontend-dev") to facilitate direct messaging.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses and actively trying to disprove each other.
- **Parallel Review**: Specialists for Security, Performance, and Test Coverage (coordinate via `message` to avoid duplicate feedback).
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel.

### 4.3 Coordination
- **Shared Task List**: centralized task tracking (`Ctrl+T` to toggle).
- **Mailbox**: inter-agent messaging via `message <teammate>` (direct) and `broadcast` (team-wide).
- **Cleanup**: Handled automatically when the session exits. No manual cleanup tool required.

### 4.4 Limitations
- **Session Resumption**: `/resume` and `/rewind` do not restore in-process teammates.
- **Task Status**: Can sometimes lag; check work manually if a task appears stuck.
- **One Team**: Only one team per session; no nested teams.

### 4.4 Automated Quality Gates
- `TaskCompleted` hook validates that a handoff report or summary exists in the transcript.
- `TeammateIdle` hook ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
