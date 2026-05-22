# Claude Agent Swarm Guide v2.2

## 1. Definition

In a Claude Code workflow, an Agent Swarm is a network of specialized roles coordinated by a Router and linked via a handoff protocol or decentralized Agent Team coordination.

Core capabilities:
- **Handoffs**: One specialist finishes a phase and hands control to the next via structured JSON envelopes.
- **Parallelization**: Multiple specialists work simultaneously in an **Agent Team**, sharing a task list and messaging each other.
- **Shared Context**: All roles rely on `CLAUDE.md`, `.claude/session_config.json`, and project-wide skills/hooks.

## 2. Orchestration Patterns (New in V2.2)

### 2.1 Scientific Debate (Adversarial Investigation)
When the root cause of a bug or the best architectural path is unclear, spawn a team (5+ teammates) to investigate competing hypotheses.
- **Instruction**: "Have them talk to each other to try to disprove each other's theories, like a scientific debate."
- **Outcome**: The theory that survives critical analysis is documented in the final consensus report.

### 2.2 Parallel Review (Distinct Lenses)
Instead of a single reviewer, split review criteria into independent domains.
- **Roles**: Security Reviewer, Performance Optimizer, Test Coverage Validator.
- **Outcome**: Comprehensive audit across multiple dimensions simultaneously.

### 2.3 Cross-Layer Coordination
Separate teammates for frontend, backend, and testing working in parallel on a single feature.

## 3. Team Lifecycle Management

1.  **Discovery & Pre-flight**: Router reads `.claude/docs/claud_platform_menu.md` and defines tasks.
2.  **Spawning**: Lead spawns teammates. Use `Require plan approval before they make any changes` for implementation tasks.
3.  **Planning**: Teammates work in "read-only plan mode" until the Lead approves.
4.  **Implementation**: Teammates self-claim tasks from the shared list. Aim for 5-6 tasks per teammate.
5.  **Coordination**: Lead uses "Wait for your teammates to complete their tasks before proceeding" to synchronize.
6.  **Synthesis**: Lead gathers findings and produces a final summary.
7.  **Shutdown**: Lead asks teammates to shut down.
8.  **Cleanup**: Lead runs "Clean up the team" to remove shared resources.

## 4. Coordination Mechanisms

- **Shared Task List**: Centralized tracking (`Ctrl+T` to toggle).
- **Mailbox**: Direct messaging via `message <name>` and `broadcast`.
- **Teammate Discovery**: Teammates can read `~/.claude/teams/{team-name}/config.json` to find peers.
- **Shortcuts**: `Shift+Down` to cycle, `Enter` to view, `Escape` to interrupt.

## 5. Token Usage & Scaling

- Token usage scales linearly with the number of active teammates.
- Start with **3-5 teammates** for most workflows to balance parallelism and coordination overhead.

## 6. Automated Quality Gates (Hooks)

- **TaskCreated**: Rejects vague subjects (<10 chars) or those containing "TODO".
- **TaskCompleted**: Verifies transcript contains evidence (handoff/report) and rejects "TODO".
- **TeammateIdle**: Prevents idling if "error" is found in transcript without "fixed/resolved".

## 7. Troubleshooting

- **Stuck Tasks**: If a task lags, check the teammate's session or update status manually.
- **Orphaned tmux**: Use `tmux ls` and `tmux kill-session -t <name>` if cleanup fails.
- **No Resumption**: `/resume` does not restore in-process teammates; Lead must re-spawn if session is lost.
