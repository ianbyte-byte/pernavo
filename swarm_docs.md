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

## 4. Parallelization and Team Orchestration

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration.

### 4.1 Subagents vs Agent Teams
Choose the right tool for the job:
- **Subagents**: Best for sequential tasks, quick research, or verification within a single session. Lower token cost.
- **Agent Teams**: Best for parallel exploration, complex debugging, or multi-perspective reviews where teammates need to communicate directly. Higher token cost.

### 4.2 Orchestration
- **Router** acts as the team lead.
- **Plan Approval**: Use `Require plan approval` for complex tasks. The lead reviews and approves/rejects plans before implementation begins.
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity.
- **Mailbox**: Direct inter-agent communication via `message <teammate>` and `broadcast`.

### 4.3 Orchestration Patterns
- **Scientific Debate**: 5+ teammates investigate competing hypotheses and actively try to disprove each other. Converges on more robust root causes.
- **Parallel Review**: Assign distinct "lenses" (Security, Performance, Test Coverage) to separate reviewers.
- **Cross-layer Coordination**: Separate teammates for Frontend, Backend, and Testing.

### 4.4 Best Practices & Troubleshooting
- **Context**: Teammates load project context but NOT conversation history. Include task-specific details in the spawn prompt.
- **File Conflicts**: Assign distinct file sets to teammates to avoid overwrites.
- **Waiting**: If the lead starts doing work instead of waiting, use: `Wait for your teammates to complete their tasks before proceeding`.
- **Cleanup**: Always shut down teammates before running `Clean up the team`.
- **Stuck Tasks**: If task status lags, manually update it or nudge the teammate via the mailbox.

## 5. Automated Quality Gates
Enforced via `.claude/hooks/lcc-quality-gate.sh`:
- `TaskCreated`: Rejects subjects < 10 chars or containing "TODO".
- `TaskCompleted`: Ensures a handoff report or summary exists in the transcript.
- `TeammateIdle`: Prevents going idle with unaddressed errors.

## 6. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
