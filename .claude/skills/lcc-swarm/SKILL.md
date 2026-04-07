---
name: lcc-swarm
description: Run a comprehensive Swarm workflow using specialized agents: Router, Coder, Reviewer, Tester and optional specialists.
disable-model-invocation: true
---

Run the comprehensive Swarm workflow for this repository (V2.2). Break complex tasks into specialized stages with clear handoffs or parallel agent teams, leveraging Claude Code's subagent and agent team patterns for context isolation, tool constraint enforcement, and parallel exploration.

## Core Principles

- **Agent Teams**: Use for parallel work, shared task lists, and inter-agent coordination.
- **Context Isolation**: Keep exploration/implementation out of main conversation.
- **Tool Constraints**: Use read-only agents for exploration, write-enabled for implementation.
- **Specialization**: Match tasks to focused system prompts (Router, Coder, etc.).
- **Automated Quality Gates**: Use hooks (`TaskCreated`, `TaskCompleted`, `TeammateIdle`) to enforce rules.
- **Plan Approval**: Use `Require plan approval` for implementation teammates.

## Full Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Haiku, Read-Only)                            │
│    - Context Discovery: Read .claude/docs/claud_platform_menu.md│
│    - Task Decomposition: Break into subtasks                 │
│    - Acceptance Criteria: Define done conditions             │
│    - Risk Assessment: Identify blockers/rollback path        │
│    - Specialist Selection: Choose next role(s)               │
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
            │    - Minimal, testable    │
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
            │    - Document changes     │
            └───────────────────────────┘
```

## Team Orchestration (V2.2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Shared Task List**: Lead manages tasks; teammates claim and complete.
3. **Mailbox**: Teammates use `message` and `broadcast` to coordinate.
4. **Hooks**: Automated validation via `lcc-quality-gate.sh`.
5. **UI Shortcuts**:
   - `Shift+Down`: Cycle through teammates
   - `Ctrl+T`: Toggle task list
   - `Enter`: View teammate session
   - `Escape`: Interrupt teammate
6. **Task Sizing**: 5-6 tasks per teammate is optimal.

## Advanced Orchestration Patterns

- **Parallel Code Review**: Different reviewers for Security, Performance, and Coverage.
- **Scientific Debate**: Adversarial exploration of debugging hypotheses.

## Handoff Envelope Schema

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|Architect|Product|SecurityReviewer|Debugger|Refactorer|...",
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

- **lcc-router**: Orchestration & planning
- **lcc-coder**: Implementation
- **lcc-reviewer**: Code review
- **lcc-tester**: Testing & verification
- **lcc-architect**: Design, architecture, refactoring guidance
- **lcc-ai-native-architect**: Model-Centric architectural patterns
- **lcc-product**: Requirements clarification
- **lcc-security-reviewer**: Security audit
- **lcc-debugger**: Complex debugging scenarios
- **lcc-refactorer**: Large-scale code reorganization
- **lcc-performance-optimizer**: Performance tuning
- **lcc-sql-optimizer**: SQL/Database optimization
- **lcc-docs-writer**: Documentation generation
- **lcc-release-manager**: Release orchestration
- **lcc-incident-triage**: Incident analysis
- **lcc-dependency-upgrader**: Dependency management
- **lcc-git-worktree-manager**: Parallel session management via worktrees
- **lcc-simplifier**: Code simplification

## Error Handling & Rollback

- **Coder Failure**: Hand back to Router with error details for re-planning.
- **Reviewer Blockers**: Router prioritizes fixes and re-routes to Coder.
- **Test Failures**: Include minimal repro steps + suggested fix path.
- **Context Drift**: Re-run Router to re-sync with current state.
- **Teammate Stalled**: Lead can nudge or spawn replacement.

## Best Practices

1. **Prefer Read-Only First**: Use Explore or Router for discovery before Coder.
2. **Session Config**: For platform API tasks, always update `.claude/session_config.json` first.
3. **Parallel Exploration**: Use multiple read-only agents to research separate areas.
4. **Incremental Delivery**: Break into small, reviewable chunks.
5. **Cleanup**: Shut down teammates before final team cleanup.
6. **Plan Approval**: Lead reviews plans for test coverage and absence of TODOs.
