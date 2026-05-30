# Claude Agent Swarm Guide v2.2

## 1. Definition

In a Claude Code workflow, an Agent Swarm is implemented as a network of specialized roles coordinated by a Router, leveraging **Agent Teams** for parallel execution and direct peer communication.

## 2. Architecture (V2.2)

### 2.1 Router–Worker Lead Model
- **Router (Lead)**: Understands the goal, decomposes tasks into a **Shared Task List**, selects teammates, defines acceptance criteria, approves plans, and synthesizes results.
- **Teammates (Workers)**:
  - **Coder**: Implements changes. Uses `message` to notify reviewers.
  - **Reviewer**: Audits changes. Supports **Parallel Review** (Security, Perf, Coverage).
  - **Tester**: Verifies with tests. Shares logs via `message`.

### 2.2 Orchestration Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses. Teammates actively try to disprove each other's theories to find the root cause.
- **Parallel Review**: Assign reviewers with distinct lenses. Coder receives consolidated feedback.
- **Cross-layer Coordination**: Separate teammates for frontend, backend, and infrastructure/tests.

### 2.3 Coordination Mechanics
- **Mailbox**: Direct messaging via `message <name>` (peer-to-peer) and `broadcast <msg>` (team-wide).
- **Plan Approval**: Lead uses `Require plan approval` for implementation teammates. Lead reviews and approves/rejects plans.
- **Task List**: Decentralized task tracking. Teammates self-claim unassigned, unblocked tasks.
- **Cleanup**: Lead MUST shut down teammates before running `Clean up the team`.

## 3. Global Rules & Hooks

- `CLAUDE.md`: Global rules (role boundaries, handoff schema, team patterns).
- `.claude/settings.json`: Configuration (enables agent teams, `teammateMode: "auto"`, and hooks).
- `.claude/hooks/lcc-quality-gate.sh`: Automated validation for task creation, completion, and teammate idle states.

## 4. Handoff Protocol (Legacy/Single-Agent)

For single-agent handoffs, use the JSON envelope:

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": "Progress summary",
  "next_instructions": "Actionable tasks"
}
```

## 5. Deployment Guidelines

- **Haiku for Router**: Fast, cost-effective planning.
- **Sonnet for Teammates**: High-capability implementation and review.
- **Small Tasks**: 5-6 tasks per teammate to maximize productivity.
- **Wait Directive**: Tell the lead "Wait for your teammates to complete their tasks before proceeding".
