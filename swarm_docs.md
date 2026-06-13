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

V2.1 leverages native Claude Code **Agent Teams** with advanced orchestration:

### 4.1 Orchestration
- **Router** acts as the team lead.
- Use `Create an agent team...` prompts to parallelize work.
- **Plan Approval**: Use `Require plan approval` for complex tasks. The lead reviews and approves/rejects plans before implementation begins.
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses and challenging each other.
- **Parallel Review**: Specialists for Security, Performance, and Test Coverage.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel.

### 4.3 Coordination
- **Teammate Discovery**: Teammates can discover each other by reading `~/.claude/teams/{team-name}/config.json`.
- **Shared Task List**: decentralized task tracking.
- **Mailbox**: inter-agent messaging via `message <teammate>` (direct) and `broadcast` (team-wide).
- **Cleanup**: The lead must shut down teammates and run `Clean up the team` after completion.

### 4.4 Best Practices
- **Give teammates enough context**: Teammates don't inherit conversation history. Provide task-specific details in the spawn prompt.
- **Appropriate team size**: Start with 3-5 teammates.
- **Size tasks appropriately**: Aim for 5-6 tasks per teammate to keep everyone productive.
- **Wait for teammates to finish**: Use `Wait for your teammates to complete their tasks before proceeding` to prevent the lead from over-implementing.
- **Avoid file conflicts**: Ensure each teammate owns a different set of files.

### 4.5 Limitations
- **No session resumption**: `/resume` does not restore in-process teammates.
- **Task status lag**: Teammates may fail to mark tasks as completed. Update manually or nudge if stuck.
- **Slow shutdown**: Teammates finish current requests before exiting.

### 4.6 Automated Quality Gates
- `TaskCompleted` hook validates that a handoff report or summary exists in the transcript.
- `TeammateIdle` hook ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
