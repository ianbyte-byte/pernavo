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

## 4. Parallelization and Team Orchestration (V2)

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration:

### 4.1 Orchestration
- **Router** acts as the team lead.
- **Spawn Prompting**: Include task-specific details in the spawn prompt as teammates do not inherit conversation history.
- **Plan Approval**: Use `Require plan approval` for complex/risky tasks. The lead reviews and approves/rejects plans autonomously before implementation begins.
- **Wait for Completion**: The lead should wait for teammates to finish tasks before proceeding.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses and actively trying to disprove each other.
- **Parallel Review**: Specialists for Security, Performance, and Test Coverage reviewing the same PR from different lenses.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel on separate pieces.

### 4.3 Sizing and Best Practices
- **Team Size**: 3-5 teammates is a good balance.
- **Task Sizing**: 5-6 tasks per teammate keeps everyone productive.
- **Avoid Conflicts**: Ensure teammates own different sets of files to avoid overwrites.
- **Start with Research**: New teams should start with clear-boundary tasks like review or research.

### 4.4 Coordination
- **Shared Task List**: Decentralized task tracking. Blocked tasks unblock automatically when dependencies are met.
- **Mailbox**: Inter-agent messaging via `message <teammate>` (direct) and `broadcast` (team-wide).
- **Teammate Discovery**: Teammates can read `~/.claude/teams/{team-name}/config.json` to find other members.
- **Cleanup**: The lead must shut down teammates and run `Clean up the team` after completion.

### 4.5 Automated Quality Gates
- `TaskCompleted` hook validates that a handoff report or summary exists in the transcript.
- `TeammateIdle` hook ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
