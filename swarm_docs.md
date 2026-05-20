# Claude Agent Swarm Guide v2.2

## 1. Definition

An Agent Swarm is a network of specialized roles coordinated by a Router/Lead and linked via a shared task list and messaging protocol.

## 2. Architecture: Router–Worker

- **Router (Lead)**: Understands goals, decomposes tasks, manages the team, and synthesizes results.
- **Workers (Teammates)**:
  - **Coder**: Implements changes.
  - **Reviewer**: Audits for security, performance, and correctness.
  - **Tester**: Verifies with tests and repro steps.
  - **Specialists**: Architect, Product, Debugger, etc.

## 3. Team Orchestration (Native Agent Teams)

Agent teams (v2.2) leverage native Claude Code capabilities for parallel work.

### 4.1 Orchestration
- **Enable**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- **Spawning**: Give teammates specific context and objectives in the spawn prompt.
- **Plan Approval**: Use `Require plan approval` for complex tasks. The lead must approve plans before implementation begins.
- **Wait for Completion**: The lead should wait for teammates to finish before synthesis.

### 4.2 Patterns
- **Scientific Debate**: Multiple teammates investigate competing hypotheses and challenge each other's theories to find the root cause.
- **Parallel Review**: Specialists with distinct lenses (Security, Performance, Coverage) review the same PR/module simultaneously.
- **Cross-layer Coordination**: Separate teammates for frontend, backend, and testing.

### 4.3 Coordination
- **Shared Task List**: Decentralized task tracking. Aim for 5-6 tasks per teammate.
- **Mailbox**: Inter-agent messaging via `message <teammate>` (direct) and `broadcast` (team-wide).
- **Cleanup**: The lead must shut down teammates and run `Clean up the team` after completion.

## 4. Automated Quality Gates (Hooks)

- **TaskCreated**: Validates task subjects.
- **TaskCompleted**: Ensures handoff/summary existence.
- **TeammateIdle**: Prevents idling with unaddressed errors.

## 5. Handoff Protocol (Sequential)

For non-team (sequential) workflows, use the JSON handoff envelope to preserve continuity across role transitions.

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": { "progress": "...", "remaining": "...", "risks": "..." },
  "next_instructions": "..."
}
```

## 6. Best Practices

- **Give Context**: Teammates don't inherit history; provide everything needed in the spawn prompt.
- **Avoid Conflicts**: Assign distinct file sets to different teammates.
- **Size Tasks**: Keep tasks small enough for frequent check-ins but large enough to be a meaningful unit of work.
- **Monitor and Steer**: Don't let teammates run unattended for too long.
- **Cleanup**: Always clean up team resources to avoid inconsistent state.
