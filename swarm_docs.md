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

## 4. Parallelization and Team Orchestration (V2)

V2.1 leverages native Claude Code **Agent Teams** (v2.1.178+) for decentralized coordination:

### 4.1 Orchestration
- **Router** acts as the team lead, spawning teammates via natural language instructions.
- **Subagent Definitions**: Reference subagent types (e.g., `lcc-coder`) when spawning teammates to reuse role definitions.
- **Plan Approval**: Use `Require plan approval` for complex tasks. Teammates work in read-only plan mode until the lead approves.
- **Teammate Discovery**: Agents read `~/.claude/teams/{team-name}/config.json` to find other members.
- **Sizing**: 3-5 teammates with 5-6 tasks each is recommended.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses and "disproving each other's theories."
- **Parallel Review**: Specialists for Security, Performance, and Test Coverage.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel.

### 4.3 Coordination
- **Shared Task List**: All agents can see status and self-claim unassigned, unblocked tasks.
- **Mailbox**: Direct peer-to-peer messaging via `message <name>` and `broadcast`.
- **Cleanup**: Automatic upon session exit. Explicitly shut down teammates via "Ask [name] to shut down" if needed early. Manual cleanup tools are deprecated.

### 4.4 Automated Quality Gates
- `TaskCompleted` hook: Rejects if no handoff/summary/LGTM is in the transcript.
- `TeammateIdle` hook: Rejects if "error" exists without "fixed/resolved/workaround".
- `TaskCreated` hook: Rejects short subjects or "TODO".

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
