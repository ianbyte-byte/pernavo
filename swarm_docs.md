# Claude Agent Swarm Guide v2.2

## 1. Definition

In a Claude Code workflow, an Agent Swarm is implemented as a network of specialized roles coordinated by a Router and linked via a handoff protocol or a shared task list (Agent Teams) that preserves continuity.

Core capabilities:
- **Handoffs**: Sequential flow where one specialist finishes a phase and hands control to the next.
- **Agent Teams**: Parallel execution where multiple specialists work together via a shared task list and inter-agent messaging.
- **Shared context**: All roles rely on the same project rules (e.g., `CLAUDE.md`) and session artifacts.

## 2. Reference Implementation

### 2.1 Architecture: Router–Worker (Agent Teams)
- **Router (Team Lead)**: Understands the goal, breaks it into tasks, spawns teammates, approves plans, and synthesizes results.
- **Workers (Teammates)**:
  - **Coder**: Implements changes.
  - **Reviewer**: Audits for security, performance, and correctness.
  - **Tester**: Verifies with tests and repro steps.
  - **Specialists**: Architect, SecurityReviewer, Debugger, etc.

### 2.2 Key Artifacts
- `CLAUDE.md`: Global rules and role boundaries.
- `.claude/agents/`: Subagent definitions used as teammate templates.
- `.claude/skills/`: Custom workflows (e.g., `/lcc-swarm`).
- `.claude/settings.json`: Enables `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- `.claude/hooks/`: Automated quality gates (`TaskCreated`, `TaskCompleted`, `TeammateIdle`).
- `.claude/session_config.json`: Per-session pre-flight requirements.

## 3. Orchestration Patterns (V2.2)

### 3.1 Scientific Debate
- **Purpose**: Investigate root causes or explore complex designs when the answer is unclear.
- **Execution**: Spawn 5+ teammates with competing hypotheses. Instruct them to "talk to each other to try to disprove each other's theories."
- **Benefit**: Fights "anchoring bias" where an agent stops at the first plausible explanation.

### 3.2 Parallel Code Review
- **Purpose**: Thoroughly audit a PR or module from multiple angles simultaneously.
- **Execution**: Spawn specialists for Security, Performance, and Test Coverage.
- **Benefit**: Ensures deep focus on specific domains without one aspect overshadowing others.

### 3.3 Cross-Layer Coordination
- **Purpose**: Implement features that span multiple layers (Frontend, Backend, Tests).
- **Execution**: Assign each layer to a different teammate.
- **Constraint**: Partition work by file to avoid merge conflicts.

## 4. Team Lifecycle Management

1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json`.
2. **Spawn**: The Lead (Router) creates the team. Use `Require plan approval` for implementation.
3. **Plan Approval**: Teammates work in read-only mode until the Lead approves their approach.
4. **Execution**: Teammates self-claim tasks from the shared list. They communicate via `message <name>` or `broadcast`.
5. **Monitor & Steer**: The Lead (or User) cycles through teammates (Shift+Down) to redirect if they get stuck.
6. **Synthesis**: The Lead waits for completion (`Wait for your teammates to finish`) and summarizes findings.
7. **Cleanup**: Lead shuts down teammates and runs `Clean up the team`.

## 5. Troubleshooting & Best Practices

- **Context Inheritance**: Teammates load `CLAUDE.md` but NOT the lead's conversation history. Provide rich context in the spawn prompt.
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity and allow re-assignment.
- **Stuck Tasks**: If a teammate fails to mark a task as complete, update it manually or nudge them.
- **Teammate Mode**: Use `teammateMode: "auto"` (default). Split-panes require `tmux` or `iTerm2`.
- **Orphaned Sessions**: If cleanup fails, use `tmux ls` and `tmux kill-session -t <name>` to manually clear resources.

## 6. Testing guidance

Suggested scenario:
- Scaffold a new service or refactor a module using a team of 3 (Architect, Coder, Tester).

Expected loop:
- Architect plans → Lead approves → Coder implements → Tester verifies → Lead synthesizes.
