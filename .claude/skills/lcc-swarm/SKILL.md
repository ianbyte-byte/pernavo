---
name: lcc-swarm
description: Run a comprehensive Swarm workflow using specialized agents (Router, Coder, Reviewer, Tester) and parallel Agent Teams.
disable-model-invocation: true
---

Run the comprehensive Swarm workflow for this repository. Break complex tasks into specialized stages with clear handoffs or parallel agent teams, leveraging Claude Code's subagent and agent team patterns for context isolation, tool constraint enforcement, and parallel exploration.

## Core Principles

- **Agent Teams**: Use for parallel work, shared task lists, and inter-agent coordination.
- **Context Isolation**: Keep exploration/implementation out of main conversation.
- **Tool Constraints**: Use read-only agents for exploration, write-enabled for implementation.
- **Specialization**: Match tasks to focused system prompts (Router, Coder, etc.).
- **Automated Quality Gates**: Enforce rules via `TaskCreated`, `TaskCompleted`, and `TeammateIdle` hooks.

## Full Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Haiku, Read-Only, Lead)                      │
│    - Context Discovery: Read .claude/docs/claud_platform_menu.md│
│    - Orchestration: Decide between single subagent or Team   │
│    - Task Decomposition: Break into subtasks in shared list  │
│    - Risk Assessment: Use "Require plan approval" if needed  │
└─────────────────────────────────────────────────────────────┘
    │
    ├───────────────────────┬───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ 2a. Specialist│   │ 2b. Specialist│   │ 2c. Parallel  │
│ (Implementation)  │ (Review/Audit)│   │ Exploration   │
└───────────────┘   └───────────────┘   └───────────────┘
    │                       │                       │
    └───────────────────────┴───────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 3. Lead Wait & Synthesize │
            │    - Wait for all tasks   │
            │    - Review plans if any  │
            │    - Summarize outcomes   │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 4. Cleanup                │
            │    - Shut down teammates  │
            │    - Clean up the team    │
            └───────────────────────────┘
```

## Team Orchestration (V2.2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Shared Task List**: Lead manages tasks; teammates claim and complete.
3. **Plan Approval**: Lead reviews and approves/rejects plans autonomously before implementation begins.
4. **Mailbox**: Teammates use `message <teammate>` to coordinate and hand off work.
5. **Quality Gates**: Automated validation via `lcc-quality-gate.sh`.

## Handoff Envelope Schema (Enhanced)

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|Architect|AiNativeArchitect|Product|SecurityReviewer|Debugger|Refactorer|PerformanceOptimizer|SqlOptimizer|DocsWriter|ReleaseManager|IncidentTriage|DependencyUpgrader|GitWorktreeManager|Simplifier",
  "summary": {
    "progress": "What was accomplished",
    "remaining": "Outstanding tasks",
    "risks": "Potential blockers",
    "changes": "Key file modifications (if any)"
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

Delegation to specialist agents based on Router's plan:
- **lcc-router**: Orchestration & planning
- **lcc-coder**: Implementation
- **lcc-reviewer**: Code review (Security/Perf/Coverage)
- **lcc-tester**: Testing & verification
- **lcc-architect**, **lcc-product**, **lcc-debugger**, etc.: Specialists

## Best Practices

1. **Prefer Read-Only First**: Use Router for discovery before Coder.
2. **Wait for Teammates**: Lead should not proceed until all parallel tasks are complete.
3. **Proactive Cleanup**: Always shut down teammates and clean up the team after the goal is achieved.
4. **UI Shortcuts**: Use `Shift+Down` to monitor teammates and `Ctrl+T` for the task list.

RESPECT!
