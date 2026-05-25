---
name: lcc-swarm
description: Run a comprehensive Swarm workflow (V2.2) using specialized agents: Router, Coder, Reviewer, Tester and optional specialists.
disable-model-invocation: true
---

Run the comprehensive Swarm workflow for this repository. Break complex tasks into specialized stages with clear handoffs or parallel agent teams, leveraging Claude Code's subagent and agent team patterns for context isolation, tool constraint enforcement, and parallel exploration.

## Core Principles

- **Agent Teams (V2.2)**: Use for parallel work, shared task lists, and inter-agent coordination.
- **Orchestration Patterns**: Scientific Debate, Parallel Review, and Cross-Layer Coordination.
- **Plan Approval**: Use `Require plan approval` for implementation to enforce quality before changes.
- **Task Sizing**: Aim for 5-6 tasks per teammate to keep everyone productive.
- **Automated Quality Gates**: Use hooks (`TaskCreated`, `TaskCompleted`, `TeammateIdle`) to enforce rules.

## Full Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Team Lead, Haiku, Read-Only)                 │
│    - Context Discovery: Read docs/specs                      │
│    - Team Selection: Spawn teammates or use subagents       │
│    - Task Decomposition: Populate shared task list          │
│    - Acceptance Criteria: Define done conditions             │
└─────────────────────────────────────────────────────────────┘
    │
    ├───────────────────────┬───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ 2a. Specialist│   │ 2b. Parallel  │   │ 2c. Competing │
│ Exploration   │   │ Code Review   │   │ Hypotheses    │
│ (Architect,   │   │ (Security,    │   │ (Scientific   │
│ Product, etc.)│   │ Perf, etc.)   │   │ Debate)       │
└───────────────┘   └───────────────┘   └───────────────┘
    │                       │                       │
    └───────────────────────┴───────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 3. lcc-coder (Teammate)   │
            │    - **Plan Approval**    │
            │    - Implement changes    │
            │    - Self-claim tasks     │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 4. lcc-reviewer (Teammate)│
            │    - Parallel review      │
            │    - Output LGTM          │
            │    - Message Coder        │
            └───────────────────────────┘
                    │               │
              [Issues]         [LGTM]
                    │               │
                    ▼               ▼
            ┌──────────┐    ┌───────────────────┐
            │ lcc-     │    │ 5. lcc-tester     │
            │ coder    │    │    - Run tests    │
            │ (fix)    │    │    - Self-claim   │
            └──────────┘    └───────────────────┘
                    │               │
                    └───────────────┘
                            │
                      [Passing]
                            │
                            ▼
            ┌───────────────────────────┐
            │ 6. lcc-router (Synthesis) │
            │    - Verify acceptance    │
            │    - Cleanup Team         │
            │    - Summarize outcome    │
            └───────────────────────────┘
```

## Team Orchestration (V2.2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Shared Task List**: Lead manages tasks; teammates claim and complete.
3. **Mailbox**: Teammates use `message` and `broadcast` to coordinate.
4. **Hooks**: Automated validation via `lcc-quality-gate.sh`.
5. **Lifecycle**: Spawn -> Plan Approval -> Execution -> Synthesis -> Cleanup.

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

## Best Practices

1. **Prefer Agent Teams**: Use for parallel work and coordination.
2. **Require Plan Approval**: Essential for complex implementation tasks.
3. **Scientific Debate**: Use 5+ teammates for investigative work.
4. **Partition by File**: Avoid merge conflicts by assigning separate files to teammates.
5. **Wait for Completion**: The Lead should explicitly wait for teammates before synthesizing.

## Related Resources

- Run `/workflow-index` for full workflow inventory
- See `swarm_docs.md` for in-depth V2.2 guidance.
- See `.claude/docs/INDEX.md` for project docs navigation.
