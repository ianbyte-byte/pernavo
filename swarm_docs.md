# Claude Agent Swarm Guide v2.2

## 1. Definition
In a Claude Code workflow, an Agent Swarm is a network of specialized roles coordinated by a Router and linked via a handoff protocol (sequential) or an Agent Team (parallel).

## 2. Architecture: Router–Worker
- **Router (Team Lead)**: Understands the goal, decomposes tasks, selects agents, defines acceptance criteria, approves plans, and manages the team lifecycle.
- **Workers (Teammates)**: Specialized agents (Coder, Reviewer, Tester, Architect, etc.) that execute assigned tasks.

## 3. Parallelization and Team Orchestration (V2.2)
Agent Teams leverage native Claude Code capabilities for multi-agent collaboration.

### 4.1 Orchestration Lifecycle
1. **Enablement**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.
2. **Team Creation**: Router proposes `Create an agent team...` with specific roles and models (prefer Sonnet).
3. **Task Assignment**: Lead creates tasks in the shared list; teammates self-claim or are assigned.
4. **Plan Approval**: For complex work, use `Require plan approval`. Teammates wait in read-only mode until the lead approves their plan.
5. **Messaging**: Teammates coordinate via `message <name>` or `broadcast`.
6. **Synthesis**: Lead summarizes all findings once tasks are completed.
7. **Shutdown & Cleanup**: Lead shuts down teammates individually, then runs `Clean up the team`.

### 4.2 Display Modes
- **In-process**: Works in any terminal. Use `Shift+Down` to cycle.
- **Split Panes**: Requires `tmux` or `iTerm2`. Set `teammateMode: "tmux"` in settings to force.

### 4.3 Advanced Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses. Explicitly instruct them to "disprove each other's theories".
- **Parallel Review**: Specialists for Security, Performance, and Test Coverage auditing a single PR/Module.
- **Cross-layer Coordination**: Frontend, Backend, and Tests specialists working on a single feature.

## 4. Handoff Protocol (Sequential)
For sequential work, each handoff MUST include a JSON envelope:
```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": {
    "progress": "string",
    "remaining": "string",
    "risks": "string",
    "changes": "string"
  },
  "acceptance_criteria": ["string"],
  "next_instructions": "string"
}
```

## 5. Automated Quality Gates
Enforced via `.claude/hooks/lcc-quality-gate.sh`:
- **TaskCreated**: Rejects vague subjects.
- **TaskCompleted**: Ensures evidence of verification (handoff/report/LGTM) exists in the transcript.
- **TeammateIdle**: Prevents idling if errors are left unaddressed.

## 6. Troubleshooting
- **Teammates not appearing**: Ensure `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Use `Shift+Down` to check for hidden sessions.
- **Task status lag**: If a task is stuck, check the teammate's session or update the status manually.
- **Orphaned sessions**: Use `tmux ls` and `tmux kill-session -t <name>` if cleanup fails.

RESPECT!
