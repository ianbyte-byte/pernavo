---
name: lcc-swarm
description: Run a comprehensive Swarm workflow using specialized agents: Router, Coder, Reviewer, Tester and optional specialists.
disable-model-invocation: true
---

Run the comprehensive Swarm workflow for this repository. Break complex tasks into specialized stages with clear handoffs or parallel agent teams, leveraging Claude Code's subagent and agent team patterns for context isolation, tool constraint enforcement, and parallel exploration.

## Core Principles

- **Agent Teams**: Use for parallel work, shared task lists, and inter-agent coordination.
- **Context Isolation**: Keep exploration/implementation out of main conversation.
- **Tool Constraints**: Use read-only agents for exploration, write-enabled for implementation.
- **Specialization**: Match tasks to focused system prompts (Router, Coder, etc.).
- **Automated Quality Gates**: Use hooks (`TaskCreated`, `TaskCompleted`, `TeammateIdle`) to enforce rules.

## Full Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Haiku, Read-Only, Team Lead)                 │
│    - Context Discovery: Read .claude/docs/claud_platform_menu.md│
│    - Task Decomposition: Break into subtasks (5-6 per agent) │
│    - Acceptance Criteria: Define done conditions             │
│    - Orchestration: Propose Agent Team or sequential Handoff │
└─────────────────────────────────────────────────────────────┘
    │
    ├───────────────────────┬───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ 2a. Parallel  │   │ 2b. Scientific│   │ 2c. Parallel  │
│ Review        │   │ Debate        │   │ Implementation│
│ (Multi-Lens)  │   │ (Adversarial) │   │ (Component)   │
└───────────────┘   └───────────────┘   └───────────────┘
    │                       │                       │
    └───────────────────────┴───────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 3. Plan Approval (Lead)   │
            │    - Review teammate plans│
            │    - Approve/Reject/Feedbk│
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 4. Execution & Mailbox    │
            │    - Teammates work tasks │
            │    - Inter-agent messaging│
            │    - Self-claiming logic  │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 5. Synthesis & Cleanup    │
            │    - Lead gathers results │
            │    - Shut down teammates  │
            │    - Final Team Cleanup   │
            └───────────────────────────┘
```

## Team Orchestration (V2.2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Shared Task List**: Lead manages tasks; teammates claim and complete. Aim for **5-6 tasks per teammate**.
3. **Plan Approval**: Use `Require plan approval` for implementation. Teammates must wait for Lead's approval before modifying files.
4. **Mailbox**: Teammates use `message <name>` (direct) and `broadcast` (team-wide) to coordinate findings and handoffs.
5. **Wait for Completion**: Lead must wait for all tasks to be finished before final synthesis.
6. **Cleanup**: Lead shuts down teammates one by one, then runs `Clean up the team`.

## Handoff Envelope Schema (For Sequential Handoffs)

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|Architect|Product|SecurityReviewer",
  "summary": {
    "progress": "What was accomplished",
    "remaining": "Outstanding tasks",
    "risks": "Potential blockers",
    "changes": "Key file modifications"
  },
  "acceptance_criteria": [
    "List of verifiable conditions for completion"
  ],
  "next_instructions": "Specific, actionable task list",
  "context": {
    "platform_api_needed": false,
    "session_config_updated": false,
    "test_coverage_required": "minimal|full",
    "risk_level": "low|medium|high"
  }
}
```

## Specialized Agent Integration

When Router identifies specific needs, delegate to specialist agents:

- **lcc-router**: Orchestration & planning (Lead)
- **lcc-coder**: Implementation (supports Plan Approval)
- **lcc-reviewer**: Code review (multi-lens: Security, Perf, etc.)
- **lcc-tester**: Testing & verification (pytest, dotnet watch)
- **lcc-architect**: High-level design & refactoring
- **lcc-debugger**: Complex root cause analysis

## Best Practices

1. **Read-Only Plan Mode**: Use for risky implementation tasks to ensure alignment.
2. **Scientific Debate**: Use 5+ teammates to disprove competing hypotheses.
3. **Task Sizing**: Keep tasks small enough for frequent check-ins but large enough to avoid overhead.
4. **Incremental Cleanup**: Always shut down teammates before cleaning up the team to avoid inconsistent state.

## Project Subagents

Location: `.claude/agents/`

- **lcc-router** - Orchestration & planning
- **lcc-coder** - Implementation
- **lcc-reviewer** - Code review
- **lcc-tester** - Testing & verification
- **lcc-architect**, **lcc-product**, **lcc-security-reviewer**, etc. - Specialists

## Related Resources

- Run `/workflow-index` for full workflow inventory
- See `swarm_docs.md` for detailed V2.2 specifications
- See `.claude/docs/INDEX.md` for project docs navigation
