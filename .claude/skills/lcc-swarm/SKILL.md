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
- **Automated Quality Gates**: Use hooks (`TaskCreated`, `TaskCompleted`, `TeammateIdle`) to enforce rules via `lcc-quality-gate.sh`.

## Full Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Haiku, Read-Only)                            │
│    - Context Discovery: Read .claude/docs/claud_platform_menu.md│
│    - Task Decomposition: Break into subtasks (5-6 per team)  │
│    - Acceptance Criteria: Define done conditions             │
│    - Specialist Selection: Choose next role(s)               │
│    - Lead Orchestration: Inform user about UI shortcuts      │
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
            │    - Plan Approval Mode?  │
            │    - Update session_config│
            │      if platform API task │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 4. lcc-reviewer           │
            │    - Security review      │
            │    - Correctness check    │
            │    - Maintainability      │
            │    - Output LGTM if OK    │
            └───────────────────────────┘
                    │               │
              [Issues]         [LGTM]
                    │               │
                    ▼               ▼
            ┌──────────┐    ┌───────────────────┐
            │ lcc-     │    │ 5. lcc-tester     │
            │ coder    │    │    - Run tests    │
            │ (fix)    │    │    - Repro steps  │
            └──────────┘    └───────────────────┘
                    │               │
                    └───────────────┘
                            │
                      [Passing]
                            │
                            ▼
            ┌───────────────────────────┐
            │ 6. lcc-router (Wrap-Up)   │
            │    - Verify acceptance    │
            │    - Summarize outcome    │
            │    - Cleanup Team         │
            └───────────────────────────┘
```

## Team Orchestration (V2.2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **UI Shortcuts**: `Shift+Down` (cycle), `Ctrl+T` (toggle tasks), `Enter` (view), `Escape` (interrupt).
3. **Display Modes**: In-process or Split Panes (requires `tmux` or `it2` CLI).
4. **Task List**: Lead manages; teammates claim (5-6 tasks each).
5. **Mailbox**: Teammates use `message` and `broadcast` to coordinate.
6. **Plan Approval**: Use `Require plan approval` for risky tasks.
7. **Hooks**: Validation via `lcc-quality-gate.sh` (TaskCreated, TaskCompleted, TeammateIdle).
8. **Patterns**: Scientific Debate, Parallel Review, Cross-layer Coordination.

## Handoff Envelope Schema (V2.2)

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|Architect|Product|SecurityReviewer|Debugger|Refactorer",
  "summary": {
    "progress": "What was accomplished",
    "remaining": "Outstanding tasks",
    "risks": "Potential blockers",
    "changes": "Key file modifications (if any)"
  },
  "acceptance_criteria": [
    "Verifiable conditions for completion"
  ],
  "next_instructions": "Specific, actionable task list",
  "context": {
    "platform_api_needed": false,
    "session_config_updated": false,
    "team_active": false,
    "risk_level": "low|medium|high"
  }
}
```

## Specialized Agent Integration

Delegate to specialist agents as needed:
- **lcc-architect**: Design & refactoring guidance
- **lcc-product**: Requirements & user story mapping
- **lcc-security-reviewer**: Security audit pass
- **lcc-debugger**: Complex triage & investigation
- **lcc-refactorer**: Structural code reorganization
- **lcc-performance-optimizer**: Performance measurement & tuning
- **lcc-simplifier**: Code minimalism (behavior-preserving)
- **lcc-docs-writer**: Documentation synchronization
- **lcc-release-manager**: Release orchestration & checklist

## Error Handling & Rollback

- **Coder Failure**: Hand back to Router for re-planning.
- **Reviewer Blockers**: Router prioritizes fixes and re-routes.
- **Test Failures**: Coder fixes based on Repro Steps from Tester.
- **Context Drift**: Router re-syncs state and re-routes.

## Best Practices

1. **Wait for Teammates**: Lead waits for completions before synthesis.
2. **Proactive UI Nudges**: Inform users about `Shift+Down` to monitor progress.
3. **Task Sizing**: 5-6 tasks per teammate avoids bottlenecking.
4. **Subject Quality**: Descriptive subjects >= 10 chars (enforced by hooks).

## Related Resources

- Run `/workflow-index` for full workflow inventory.
- Run `/lcc-workflow-index` for specialized LCC skills.
- See `swarm_docs.md` for advanced orchestration patterns.
