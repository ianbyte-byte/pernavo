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

Each handoff must include a JSON object using the **Enhanced Handoff Schema**:

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": {
    "progress": "Detailed summary of what was completed",
    "remaining": "What remains to be done",
    "risks": "Any blockers, risks, or technical debt introduced",
    "changes": "Brief list of file changes"
  },
  "next_instructions": "Actionable tasks for the next agent",
  "acceptance_criteria": ["criteria 1", "criteria 2"],
  "context": {
    "platform_api_needed": false,
    "risk_level": "low"
  }
}
```

Recommended constraints:
- `summary` mapping must contain all 4 keys: `progress`, `remaining`, `risks`, `changes`.
- `next_instructions` must be actionable (not just “continue”).

## 4. Parallelization and Team Orchestration (V2.2)

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration:

### 4.1 Orchestration
- **Router** acts as the team lead.
- **Display Mode**: Use `teammateMode: auto` to enable split panes in compatible terminals.
- **Spawning**: Use subagent types for consistent behavior.
  - Command: `Spawn a teammate using the [type] agent type`.
- **Plan Approval**: Mandatory for implementation/refactoring tasks.
  - Use: `Require plan approval before they make any changes`.
  - Lead reviews plans in read-only mode.
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity.
- **Wait for Teammates**: If the lead starts implementing itself, use: `Wait for your teammates to complete their tasks before proceeding`.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses.
  - Key instruction: "Have them talk to each other to try to disprove each other's theories".
- **Parallel Review**: Specialists for Security, Performance, and Test Coverage.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel.

### 4.3 Coordination
- **Shared Task List**: Decentralized task tracking and self-claiming.
- **Mailbox**: Direct inter-agent messaging via `message <teammate>`.
- **Discovery**: Teammates can read `~/.claude/teams/{team-name}/config.json` to find other members.
- **Cleanup**: Automatic upon lead session exit. Manual cleanup tools are no longer required.

### 4.4 Automated Quality Gates
- `TaskCompleted` hook validates that a handoff report or summary exists in the transcript.
- `TeammateIdle` hook ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
