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

Each handoff must include a JSON object following the **Enhanced Handoff Schema**:

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": {
    "progress": "What was accomplished",
    "remaining": "What still needs to be done",
    "risks": "Potential blockers or side effects",
    "changes": "Brief list of modified files/logic"
  },
  "next_instructions": "Actionable task list for the next agent",
  "acceptance_criteria": ["condition 1"],
  "context": { "platform_api_needed": "false" }
}
```

Recommended constraints:
- `summary` must be structured (V2.2+).
- `next_instructions` must be actionable.
- Use `chung-swarm handoff new` CLI for validation.

## 4. Parallelization and Team Orchestration (V2.2)

V2.2 leverages native Claude Code **Agent Teams** with decentralized coordination:

### 4.1 Orchestration
- **Router** acts as the team lead.
- **Spawning**: Use `Spawn a teammate using the [agent-type] agent type` for role consistency. Provide rich context in the spawn prompt.
- **Plan Approval**: Use `Require plan approval` for implementation. The lead reviews and approves/rejects plans autonomously based on quality criteria (e.g., test coverage, no "TODO" markers).
- **Task Sizing**: Aim for 5-6 tasks per teammate.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses and actively trying to "disprove each other's theories".
- **Parallel Review**: Specialists (Security, Performance, Test Coverage) reviewing in parallel.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists.

### 4.3 Coordination
- **Shared Task List**: Automatic decentralized task tracking.
- **Mailbox**: Inter-agent messaging via `message <teammate>` and `broadcast`.
- **Synchronization**: Use "Wait for your teammates to complete their tasks before proceeding" for lead-driven synthesis.
- **Teammate Discovery**: Teammates can discover others via `~/.claude/teams/{team-name}/config.json`.
- **Cleanup**: Cleanup is automatic upon session exit (v2.1.178+). Explicitly shut down teammates when done.

### 4.4 Automated Quality Gates
- `TaskCompleted` hook validates that a handoff report or summary exists in the transcript.
- `TeammateIdle` hook ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
