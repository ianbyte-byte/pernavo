# Claude Agent Swarm Guide v2.2

## 1. Definition

In a Claude Code workflow, an Agent Swarm can be implemented as a network of specialized roles coordinated by a Router and linked via a handoff protocol that preserves continuity.

Core capabilities:
- **Handoffs**: One specialist finishes a phase and hands control to the next.
- **Parallelization**: Multiple specialists work together via Agent Teams, coordinated by a Lead.
- **Shared Context**: All roles rely on the same project rules (`CLAUDE.md`) and artifacts.

## 2. Reference Implementation

### 2.1 Architecture: Lead–Teammate (Agent Teams)
- **Team Lead**: Understands the goal, decomposes tasks, assigns work, approves plans, and synthesizes results.
- **Teammates**: Specialized sessions (Coder, Reviewer, Tester, etc.) that operate independently but coordinate through shared resources.

### 2.2 Key Artifacts
- `CLAUDE.md`: Global rules, role boundaries, handoff schema, and Agent Team protocols.
- `.claude/agents/`: Claude Code subagent definitions (YAML + system prompt).
- `.claude/skills/`: Claude Code workflow skills (e.g., `/lcc-swarm`).
- `.claude/settings.json`: Enables experimental features and automated hooks.
- `.claude/hooks/`: Automated quality gate scripts (e.g., `lcc-quality-gate.sh`).
- `.claude/session_config.json`: Per-session pre-flight notes for Document-First workflows.

## 3. Handoff Protocol

Each handoff (when not using Agent Teams) must include a JSON object:

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": "Progress summary",
  "next_instructions": "Actionable tasks for the next agent"
}
```

Recommended constraints:
- `summary` must include: done, todo, risks/blockers.
- `next_instructions` must be actionable (not just “continue”).

## 4. Parallelization and Team Orchestration (V2.2)

V2.2 fully leverages native Claude Code **Agent Teams**:

### 4.1 Team Mechanics
- **Enabling**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`.
- **Starting**: Ask the Lead to "Create an agent team...".
- **Plan Approval**: Use `Require plan approval` for implementation teammates. The Lead reviews and approves plans before write access is granted.
- **Task Management**: Use the shared task list (`Ctrl+T`). Aim for 5-6 tasks per teammate.
- **Messaging**: Use `message <teammate>` for direct talk and `broadcast` for team-wide updates.
- **Cleanup**: Lead must shut down teammates and run `Clean up the team`.

### 4.2 Display Modes
- **In-process**: Default. Cycle with `Shift+Down`.
- **Split Panes**: Requires `tmux` or `iTerm2`. Recommended for complex orchestration.

### 4.3 Orchestration Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses, actively trying to disprove each other to find the root cause.
- **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).
- **Cross-layer Coordination**: Frontend, Backend, and Tests specialists working in parallel on their respective layers.

## 5. Automated Quality Gates

Enforced via hooks in `.claude/hooks/`:
- `TaskCreated`: Validates subject length and quality.
- `TaskCompleted`: Verifies that a handoff report or summary exists in the transcript.
- `TeammateIdle`: Prevents teammates from stopping if unaddressed errors exist.

## 6. Document-First Workflow

Required for platform/API/prompt/limits tasks:
1. **Discover**: Read `.claude/docs/claud_platform_menu.md`.
2. **Pre-flight**: Coder updates `.claude/session_config.json` with spec summaries.
3. **Execute**: Implementation starts only after pre-flight is complete.

## 7. Troubleshooting

- **Orphaned Sessions**: Use `tmux ls` and `tmux kill-session -t <name>` to clean up.
- **Task Status Lag**: If a task seems stuck, check the teammate's session (`Enter`) and update manually or nudge.
- **Lead Premature Shutdown**: If the Lead tries to finish before tasks are done, tell it to "Wait for teammates to finish".
