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

### 4.1 Orchestration
- **Router** acts as the team lead.
- Use `Create an agent team...` prompts to parallelize work.
- **Plan Approval**: Use `Require plan approval` for complex or risky tasks. The teammate works in read-only plan mode until the lead reviews and approves/rejects the approach.
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity. Avoid tasks that are too small (high overhead) or too large (delayed check-ins).
- **Wait for Completion**: The lead should explicitly wait for teammates to complete their tasks before proceeding with synthesis or implementation.

### 4.2 Patterns
- **Scientific Debate**: Spawn 5+ teammates to investigate different hypotheses. Have them talk to each other to try to disprove each other's theories, converging on a root cause.
- **Parallel Review**: Split review criteria into independent domains (e.g., Security, Performance, Test Coverage) assigned to different teammates.
- **Cross-layer coordination**: Teammates each own a separate piece (e.g., Frontend, Backend, Tests) that can be explored/implemented in parallel.

### 4.3 Coordination
- **Shared Task List**: Decentralized task tracking where teammates can self-claim unassigned, unblocked tasks.
- **Mailbox**: Inter-agent messaging via `message <teammate>` (direct) and `broadcast` (team-wide).
- **Display Modes**:
  - `in-process` (default): Cycle through teammates with Shift+Down.
  - `split-panes`: Requires tmux or iTerm2. See everyone's output at once.
- **Shutdown & Cleanup**:
  - Gracefully shut down teammates first (`Ask the [teammate] to shut down`).
  - Once all teammates are closed, the lead runs `Clean up the team`.

### 4.4 Automated Quality Gates
- `TaskCreated`: Validates task subjects (e.g., reject subjects < 10 characters or containing "TODO").
- `TaskCompleted`: Validates that a handoff report or summary exists in the transcript.
- `TeammateIdle`: Ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified

## 6. Limitations (Experimental)
- No session resumption with in-process teammates.
- Task status can sometimes lag.
- One team per session; no nested teams.
- Lead is fixed to the session that created the team.
