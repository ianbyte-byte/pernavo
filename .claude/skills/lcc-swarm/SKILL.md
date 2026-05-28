---
name: lcc-swarm
description: Run a comprehensive Swarm workflow using specialized agents: Router, Coder, Reviewer, Tester and optional specialists.
disable-model-invocation: true
---

Run the comprehensive Swarm workflow for this repository. Break complex tasks into specialized stages with clear handoffs or parallel agent teams, leveraging Claude Code's subagent and agent team patterns for context isolation, tool constraint enforcement, and parallel exploration.

## Core Principles (V2.2)

- **Agent Teams**: Use for parallel work, shared task lists, and inter-agent coordination.
- **Context Isolation**: Keep exploration/implementation out of main conversation.
- **Tool Constraints**: Use read-only agents for exploration, write-enabled for implementation.
- **Specialization**: Match tasks to focused system prompts (Router, Coder, etc.).
- **Automated Quality Gates**: Use hooks (`TaskCompleted`, `TeammateIdle`) to enforce rules.

## Full Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Haiku, Read-Only, Team Lead)                 │
│    - Context Discovery: Read .claude/docs/claud_platform_menu.md│
│    - Task Decomposition: Break into subtasks in shared list  │
│    - Team Spawning: Propose Agent Team for parallel work     │
│    - Plan Approval: Review and approve teammate plans        │
└─────────────────────────────────────────────────────────────┘
    │
    ├───────────────────────┬───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ 2a. lcc-     │   │ 2b. lcc-     │   │ 2c. Parallel  │
│ architect     │   │ product       │   │ Exploration   │
│ (Optional)    │   │ (Optional)    │   │ (Explore)     │
└───────────────┘   └───────────────┘   └───────────────┘
    │                       │                       │
    └───────────────────────┴───────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 3. lcc-coder              │
            │    - Implement changes    │
            │    - Plan approval if req │
            │    - Update session_config│
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 4. lcc-reviewer           │
            │    - Domain-specific review│
            │    - Actionable fixes     │
            │    - Output LGTM if OK    │
            └───────────────────────────┘
                    │               │
              [Issues]         [LGTM]
                    │               │
                    ▼               ▼
            ┌──────────┐    ┌───────────────────┐
            │ lcc-     │    │ 5. lcc-tester     │
            │ coder    │    │    - Run tests    │
            │ (fix)    │    │    - Shared logs  │
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
            │    - Team Cleanup         │
            └───────────────────────────┘
```

## Team Orchestration

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Shared Task List**: `Ctrl+T` to toggle. Teammates claim and complete.
3. **Mailbox**: `message <teammate>` and `broadcast` for sync.
4. **Shortcuts**: `Shift+Down` (cycle), `Enter` (view), `Escape` (interrupt).
5. **Hooks**: Automated validation via `lcc-quality-gate.sh`.

## Handoff Envelope Schema (Enhanced)

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|Architect|AiNativeArchitect|Product|SecurityReviewer|Debugger|Refactorer|PerformanceOptimizer|SqlOptimizer|DocsWriter|ReleaseManager|IncidentTriage|DependencyUpgrader|GitWorktreeManager|Simplifier",
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
    "risk_level": "low|medium|high"
  }
}
```

## Specialized Agent Integration

- **lcc-router** - Orchestration & planning (Lead)
- **lcc-coder** - Implementation
- **lcc-reviewer** - Code review
- **lcc-tester** - Testing & verification
- **Specialists**: architect, product, security-reviewer, debugger, refactorer, etc.

## Best Practices

1. **Lead Synthesis**: Lead should wait for all teammates before final summary.
2. **Plan Approval**: Use for all high-risk refactors.
3. **Minimal Tasks**: Break large features into 5-6 tasks per teammate.
4. **Cleanup**: Always clean up the team via the Lead after completion.
