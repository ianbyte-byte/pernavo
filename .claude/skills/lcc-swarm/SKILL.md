---
name: lcc-swarm
description: Run a comprehensive Swarm workflow (v2.2) using specialized agents: Router, Coder, Reviewer, Tester and optional specialists.
disable-model-invocation: true
---

Run the comprehensive Swarm workflow for this repository. Break complex tasks into specialized stages with clear handoffs or parallel agent teams, leveraging Claude Code's subagent and agent team patterns for context isolation, tool constraint enforcement, and parallel exploration.

## Core Principles

- **Agent Teams**: Use for parallel work, shared task lists, and inter-agent coordination.
- **Scientific Debate**: Use competing hypotheses to find root causes.
- **Parallel Review**: Specialists for Security, Performance, and Test Coverage.
- **Context Isolation**: Keep exploration/implementation out of main conversation.
- **Tool Constraints**: Use read-only agents for exploration, write-enabled for implementation.
- **Automated Quality Gates**: Use hooks (`TaskCompleted`, `TeammateIdle`) to enforce rules.

## Full Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Haiku, Read-Only, v2.2)                      │
│    - Context Discovery: Read .claude/docs/claud_platform_menu.md│
│    - Orchestration: Single subagent OR Agent Team           │
│    - Patterns: Scientific Debate, Parallel Review           │
│    - Task Decomposition: Shared Task List (5-6 per agent)   │
└─────────────────────────────────────────────────────────────┘
    │
    ├───────────────────────┬───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ 2a. lcc-     │   │ 2b. lcc-     │   │ 2c. Parallel  │
│ architect     │   │ product       │   │ Exploration   │
│ (Optional)    │   │ (Optional)    │   │ (Team)        │
└───────────────┘   └───────────────┘   └───────────────┘
    │                       │                       │
    └───────────────────────┴───────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 3. lcc-coder              │
            │    - Implement changes    │
            │    - Plan Approval if req │
            │    - Direct Messaging     │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 4. lcc-reviewer           │
            │    - Parallel domain-focus│
            │    - Direct peer-feedback │
            │    - Output LGTM if OK    │
            └───────────────────────────┘
                    │               │
              [Issues]         [LGTM]
                    │               │
                    ▼               ▼
            ┌──────────┐    ┌───────────────────┐
            │ lcc-     │    │ 5. lcc-tester     │
            │ coder    │    │    - Run tests    │
            │ (fix)    │    │    - Share logs   │
            └──────────┘    └───────────────────┘
                    │               │
                    └───────────────┘
                            │
                      [Passing]
                            │
                            ▼
            ┌───────────────────────────┐
            │ 6. lcc-router (Wrap-Up)   │
            │    - Synthesis of team    │
            │    - Cleanup (Shutdown)   │
            └───────────────────────────┘
```

## Team Orchestration (V2.2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Wait for Teammates**: Lead waits for completion before starting its own work.
2. **Mailbox**: Teammates use `message` and `broadcast` for direct peer coordination.
3. **Task Status**: Update the shared task list immediately to unblock dependencies.
4. **Cleanup**: Lead shuts down teammates first, then runs `Clean up the team`.

## Handoff Envelope Schema (Enhanced)

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|Architect|Product|...",
  "summary": {
    "progress": "What was accomplished",
    "remaining": "Outstanding tasks",
    "risks": "Potential blockers",
    "changes": "Key file modifications"
  },
  "acceptance_criteria": [
    "Verifiable conditions"
  ],
  "next_instructions": "Actionable task list",
  "context": {
    "risk_level": "low|medium|high"
  }
}
```

## Specialized Agent Integration

When Router identifies specific needs, delegate to specialist agents first:

- **lcc-architect**: Design, architecture, refactoring guidance
- **lcc-product**: Requirements clarification
- **lcc-security-reviewer**: Security audit
- **lcc-debugger**: Complex debugging (Debate leader)
- **lcc-refactorer**: Large-scale code reorganization
- **lcc-performance-optimizer**: Performance tuning

## Best Practices

1. **Wait for Teammates**: Always ask the lead to wait for teammates to finish.
2. **Direct Messaging**: Coder → Reviewer notifications speed up the loop.
3. **Scientific Debate**: Use 5+ teammates for investigation.
4. **Cleanup**: Never skip the lead-driven cleanup.

## Related Resources

- Run `/workflow-index` for full workflow inventory
- See `CLAUDE.md` and `swarm_docs.md` for global rules and architecture.
