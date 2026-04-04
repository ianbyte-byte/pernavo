# Claude Agent Swarm Guide v2.2

## 1. Definition
In a Claude Code workflow, an Agent Swarm can be implemented as a network of specialized roles coordinated by a Router and linked via a handoff protocol that preserves continuity.

Core capabilities:
- **Handoffs**: One specialist finishes a phase and hands control to the next.
- **Parallelization**: Multiple specialists can be queried in parallel for comparison/verification, then synthesized by Router.
- **Shared Context**: All roles rely on the same project rules (`CLAUDE.md`) and session notes (`.claude/session_config.json`).

## 2. Reference Implementation
### 2.1 Architecture: Router–Worker
- **Router**: Goal understanding, task decomposition, specialist selection, and acceptance criteria.
- **Workers**:
  - **Coder**: Implements changes.
  - **Reviewer**: Audits security/correctness/maintainability.
  - **Tester**: Verifies with tests and repro steps.

### 2.2 Orchestration Patterns (New in V2.2)
- **Scientific Debate**: Spawn 5+ teammates to investigate competing hypotheses. Teammates must actively try to disprove each other. Consensus is documented by the lead.
- **Parallel Review**: Assign distinct domains (Security, Performance, Coverage) to multiple reviewers to ensure thorough attention without domain overlap.
- **Cross-layer Coordination**: Separate teammates for Frontend, Backend, and Tests, working simultaneously on a single feature.

## 3. Team Orchestration & Coordination
### 3.1 Setup
- Enable via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- Use `Create an agent team...` in your prompt.
- Set `teammateMode` (in-process or split panes) in your global config.

### 3.2 Lead Responsibilities
- **Task Management**: Decompose goals into a shared task list (aim for 5-6 tasks per teammate).
- **Plan Approval**: Use `Require plan approval` for complex/risky tasks. Review and approve/reject teammate plans before implementation.
- **Communication**: Use `message <teammate>` (direct) and `broadcast <message>` (team-wide).
- **Cleanup**: Shut down all teammates first, then run `Clean up the team`.

### 3.3 Troubleshooting
- **Orphaned tmux sessions**: If split-pane sessions persist, list them with `tmux ls` and kill with `tmux kill-session -t <session-name>`.
- **Task status lag**: If a task appears stuck, nudge the teammate or update the status manually.
- **Session Resumption**: `/resume` does not restore in-process teammates. If resuming, tell the lead to spawn new teammates.

## 4. Automated Quality Gates
Automated checks are enforced via `.claude/hooks/lcc-quality-gate.sh`.
- **TaskCreated**: Rejects subjects < 10 chars or with "TODO".
- **TaskCompleted**: Ensures a summary or handoff report exists in the transcript.
- **TeammateIdle**: Ensures no unaddressed errors exist before a teammate stops.

## 5. Handoff Protocol
Each handoff must include a JSON object:
```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": "Progress summary (done/todo/risks)",
  "next_instructions": "Actionable tasks for the next agent"
}
```

## 6. Testing Guidance
- Coder implementation → Reviewer audit → Tester verification (prefer `python -m pytest`).
- Loop until Reviewer outputs final **LGTM**.
