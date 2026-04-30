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
  "summary": {
    "progress": "What was accomplished",
    "remaining": "Outstanding tasks",
    "risks": "Potential blockers",
    "changes": "Key file modifications"
  },
  "acceptance_criteria": [
    "List of verifiable conditions"
  ],
  "next_instructions": "Specific, actionable task list"
}
```

## 4. Team Orchestration (V2.2)

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration:

### 4.1 Display Modes and Terminal Requirements
Agent teams support two display modes:
- **In-process**: All teammates run inside the main terminal. Use `Shift+Down` to cycle. Works everywhere.
- **Split panes**: Each teammate gets its own pane. Requires **tmux** or **iTerm2** (with Python API and `it2` CLI).
- Configuration: Set `"teammateMode": "in-process" | "split-panes" | "auto"` in `~/.claude/settings.json`.

### 4.2 Advanced Orchestration Patterns
- **Scientific Debate**: 5+ teammates investigate competing hypotheses, using `message` to challenge each other. Prevents "anchoring bias".
- **Parallel Review**: Specialists for Security, Performance, and Coverage provide thorough attention simultaneously.
- **Parallel Implementation**: Teammates own separate modules or files to avoid conflicts.

### 4.3 Coordination & Communication
- **Shared Task List**: Centralized tracking for the whole team.
- **Mailbox**: Inter-agent messaging via `message <teammate>` (direct) and `broadcast` (team-wide).
- **Plan Approval**: Mandatory for complex tasks. Lead reviews plans before implementation.
- **Team Discovery**: Teammates can read `~/.claude/teams/{team-name}/config.json` to discover other members.

### 4.4 Lifecycle Management
- **Spawn Prompt**: Must be rich and self-contained (teammates don't inherit lead's history).
- **Cleanup Sequence**: 1) Wait for tasks, 2) Synthesis, 3) Shut down teammates, 4) `Clean up the team`.

### 4.5 Troubleshooting
- **Orphaned tmux sessions**: Use `tmux ls` and `tmux kill-session -t <name>` to clean up if the lead exits prematurely.
- **Stuck Tasks**: If task status lags, check teammate output or update status manually via the lead.

### 4.6 Automated Quality Gates
- `TaskCreated`: Rejects subjects < 10 chars or containing "TODO".
- `TaskCompleted`: Ensures a handoff report/summary exists in the transcript.
- `TeammateIdle`: Prevents going idle with unaddressed errors.

## 5. Testing guidance

Suggested loop:
Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
