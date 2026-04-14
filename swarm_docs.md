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
- `.claude/skills/`: Claude Code skills (including the `/lcc-swarm` workflow)
- `.claude/settings.json`: project settings (enables agent teams and hooks)
- `.claude/hooks/`: automated quality gate scripts
- `.claude/session_config.json`: per-session pre-flight notes required by the document-first workflow

### 2.3 Key CLI helpers (optional)
The Python package provides a small CLI to validate workflow artifacts:
- `PYTHONPATH=src python -m chung_agent_swarm.cli check`: verify required files exist
- `PYTHONPATH=src python -m chung_agent_swarm.cli session-config validate`: validate `.claude/session_config.json`
- `PYTHONPATH=src python -m chung_agent_swarm.cli handoff validate`: validate a handoff envelope pasted from output

### 2.4 Running with Claude Code (project configuration)

This repo includes Claude Code project configuration for running the swarm directly:
- `.claude/agents/`: project subagents (YAML frontmatter + system prompt)
- `.claude/skills/lcc-swarm/`: the `/lcc-swarm` workflow skill (manual invocation)

## 3. Handoff protocol

Each handoff must include a JSON object:

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": {
    "progress": "What was accomplished",
    "remaining": "Outstanding tasks",
    "risks": "Potential blockers",
    "changes": "Key file modifications"
  },
  "acceptance_criteria": ["criteria 1", "criteria 2"],
  "next_instructions": "Specific, actionable tasks",
  "context": {
    "risk_level": "low|medium|high"
  }
}
```

Recommended constraints:
- `summary` must include: progress, remaining, risks
- `next_instructions` must be actionable (not just “continue”)

## 4. Parallelization and Team Orchestration (V2.2)

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration:

### 4.1 Orchestration
- **Router** acts as the team lead.
- Use `Create an agent team...` prompts to parallelize work.
- **Plan Approval**: Use `Require plan approval` for complex tasks. The lead reviews and approves/rejects plans before implementation begins.
- **Task Quality**: Automated gate rejects subjects < 10 chars or containing "TODO".
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses and challenging each other.
- **Parallel Review**: Specialists for Security, Performance, and Test Coverage.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel.

### 4.3 Coordination
- **Shared Task List**: decentralized task tracking.
- **Mailbox**: inter-agent messaging via `message <teammate>` (direct) and `broadcast` (team-wide).
- **Cleanup**: The lead must shut down teammates and run `Clean up the team` after completion.

### 4.4 Automated Quality Gates
- `TaskCreated`: Validates task subject length and content.
- `TaskCompleted`: Validates that a summary or keyword (LGTM, verified, etc.) exists in the transcript.
- `TeammateIdle`: Ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
