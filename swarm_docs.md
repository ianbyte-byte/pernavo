# Claude Agent Swarm Guide v2.2

## 1. Definition

In a Claude Code workflow, an Agent Swarm can be implemented as a network of specialized roles coordinated by a Router and linked via a handoff protocol that preserves continuity.

Core capabilities:
- **Handoffs**: one specialist finishes a phase and hands control to the next.
- **Parallelization**: multiple specialists can be queried in parallel for comparison/verification, then synthesized by Router (or an integrator).
- **Agent Teams**: decentralized coordination using a shared task list and inter-agent messaging.
- **Shared context**: all roles rely on the same project rules and artifacts (e.g., `CLAUDE.md`, `.claude/session_config.json`).

## 2. Reference implementation (this repository)

### 2.1 Architecture: Router–Worker (Lead–Teammate)
- **Router (Lead)**: Understands the goal, decomposes tasks, selects the next agent(s), defines acceptance criteria, approves plans, and synthesizes findings.
- **Workers (Teammates)**:
  - **Coder**: Implements changes.
  - **Reviewer**: Audits and suggests fixes.
  - **Tester**: Verifies with tests and repro steps.
  - **Specialists**: Focus on specific domains (Security, Perf, Docs, etc.).

### 2.2 Key artifacts
- `CLAUDE.md`: Global rules (role boundaries, handoff schema, agent teams, hooks).
- `.claude/agents/`: Claude Code subagents (Router/Coder/Reviewer/Tester + specialists).
- `.claude/skills/`: Claude Code skills (including the `/lcc-swarm` workflow).
- `.claude/settings.json`: Project settings (enables agent teams and hooks).
- `.claude/hooks/`: Automated quality gate scripts (`lcc-quality-gate.sh`).
- `.claude/session_config.json`: Per-session pre-flight notes required by the document-first workflow.

## 3. Handoff protocol (Sequential)

Each handoff must include a JSON object (the "Handoff Envelope"):

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

## 4. Team Orchestration (V2.2)

V2.2 leverages native Claude Code **Agent Teams** for advanced parallel orchestration:

### 4.1 Orchestration
- **Router** acts as the team lead.
- **Plan Approval**: Use `Require plan approval before they make any changes` for complex tasks. The lead reviews and approves/rejects plans autonomously before implementation begins.
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity. Use explicit dependencies in the shared task list.
- **Lifecycle**: Lead must "Wait for teammates to complete their tasks", synthesize findings, ask teammates to shut down, and then run `Clean up the team`.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigating competing hypotheses and challenging each other to disprove theories.
- **Parallel Review**: Specialists with distinct lenses (Security, Performance, Test Coverage) reviewing the same code simultaneously.
- **Cross-layer Coordination**: Frontend, Backend, and Tests specialists working in parallel on their respective layers.

### 4.3 Coordination
- **Shared Task List**: Centralized, decentralized task tracking and self-claiming.
- **Mailbox**: Inter-agent messaging via `message <teammate>` (direct) and `broadcast` (team-wide).
- **UI Shortcuts**: Use `Shift+Down` to cycle, `Ctrl+T` for tasks, `Enter` to view, and `Escape` to interrupt.

### 4.4 Automated Quality Gates
- `TaskCreated`: Rejects short or vague subjects.
- `TaskCompleted`: Validates that a handoff report or summary exists in the transcript.
- `TeammateIdle`: Ensures teammates don't go idle with unaddressed errors.

## 5. Best Practices

- **Document-First**: Always update `.claude/session_config.json` before implementation for tasks involving platform APIs.
- **Context Discovery**: Router should read `.claude/docs/claud_platform_menu.md` first.
- **Intent-Driven Minimalism**: Write only necessary code and prefer simple solutions.
- **Monitor and Steer**: Use `Shift+Down` to check on teammates regularly.

RESPECT!
