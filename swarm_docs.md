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

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration and decentralized coordination:

### 4.1 Orchestration
- **Router** acts as the team lead. One session coordinates work, assigns tasks, and synthesizes results.
- **Spawning**: Use `Spawn X teammates...` prompts. Teammates can reference existing `subagent` types (e.g., `lcc-coder`).
- **Plan Approval**: Use `Require plan approval` for complex/risky tasks. The lead autonomously reviews (approves/rejects) plans before implementation.
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity and allow for reassignment if stuck.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigate competing hypotheses and actively attempt to disprove each other to reach consensus.
- **Parallel Review**: Assign distinct domains (Security, Performance, Test Coverage) to different reviewers to ensure thoroughness.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel on their respective layers.

### 4.3 Coordination & Communication
- **Shared Task List**: Centralized list where teammates self-claim available work. Statuses include pending, in progress, and completed.
- **Direct Messaging**: Teammates communicate via `message <name>`. Messages arrive automatically without polling.
- **Broadcast**: Use `broadcast <message>` for team-wide announcements (e.g., "Architecture updated").
- **Cleanup**: Handled automatically upon session exit. No manual `Clean up the team` tool is required (v2.2).

### 4.4 Automated Quality Gates
- **TaskCreated**: Rejects vague subjects.
- **TaskCompleted**: Ensures evidence (handoff/summary/LGTM) exists in the transcript.
- **TeammateIdle**: Prevents idling if unaddressed errors persist in the transcript.

### 4.5 Best Practices
- **Context**: Teammates load `CLAUDE.md` but not conversation history. Provide task-specific details in the spawn prompt.
- **Size**: Start with 3-5 teammates. Token costs scale linearly with the number of active teammates.
- **Wait**: Instruct the lead to "Wait for teammates to finish" to prevent it from implementing tasks itself.
- **Avoid Conflicts**: Ensure teammates own different sets of files to prevent overwrites.

### 4.6 Limitations
- **Resumption**: `/resume` does not restore in-process teammates (v2.2).
- **Lag**: Task status can sometimes lag; check teammate output if a task appears stuck.
- **Single Team**: One team per session, no nested teams, and the lead is fixed.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
