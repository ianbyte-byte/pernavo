---
name: lcc-swarm
description: Run a comprehensive Swarm workflow using specialized agents: Router, Coder, Reviewer, Tester and optional specialists.
disable-model-invocation: true
---

Run the comprehensive Swarm workflow for this repository. Break complex tasks into specialized stages with clear handoffs or parallel agent teams, leveraging Claude Code's subagent and agent team patterns for context isolation, tool constraint enforcement, and parallel exploration.

## Core Principles

- **Agent Teams**: Primary mechanism for parallel work. One lead (Router) coordinates teammates via shared task lists and mailbox.
- **Context Isolation**: Each teammate runs in its own context window. Lead synthesizes final results.
- **Tool Constraints**: Use read-only agents for exploration/review, write-enabled for implementation.
- **Specialization**: Match tasks to focused system prompts (Router, Coder, etc.).
- **Automated Quality Gates**: Use hooks (`TaskCompleted`, `TeammateIdle`) to enforce rules and prevent "TODO" markers.

## Full Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Lead, Haiku, Read-Only)                      │
│    - Context Discovery: Read .claude/docs/claud_platform_menu.md│
│    - Decision: Single Handoff OR Agent Team                 │
│    - Task Decomposition: Break into subtasks (5-6/agent)    │
│    - Acceptance Criteria: Define done conditions             │
└─────────────────────────────────────────────────────────────┘
    │
    ├───────────────────────┬───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ 2a. Parallel  │   │ 2b. Scientific│   │ 2c. Specialist│
│ Implementation│   │     Debate    │   │ (Review/Audit)│
│ (Agent Team)  │   │ (Agent Team)  │   │ (Agent Team)  │
└───────────────┘   └───────────────┘   └───────────────┘
    │                       │                       │
    └───────────────────────┴───────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 3. Team Management        │
            │    - Plan Approval: Lead  │
            │      reviews agent plans  │
            │    - Mailbox: Teammates   │
            │      message each other   │
            │    - Task List: Shared    │
            │      tracking/claiming    │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 4. Verification & Review  │
            │    - lcc-reviewer (Audit) │
            │    - lcc-tester (Run)     │
            │    - Output LGTM if OK    │
            └───────────────────────────┘
                    │               │
              [Issues]         [LGTM]
                    │               │
                    ▼               ▼
            ┌──────────┐    ┌───────────────────┐
            │ lcc-     │    │ 5. lcc-router     │
            │ coder    │    │    (Synthesis)    │
            │ (fix)    │    │    - Shutdown team│
            └──────────┘    │    - Final Report │
                            └───────────────────┘
```

## Team Orchestration (V2.2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Require Plan Approval**: Use for implementation teammates to ensure lead review.
3. **Mailbox**: Teammates use `message <name>` to communicate (e.g., Coder to Reviewer).
4. **Cleanup**: Lead must shut down teammates and run `Clean up the team`.

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

- **Scientific Debate Pattern**: Spawn 5+ teammates to investigate competing hypotheses and actively disprove each other.
- **Parallel Review Pattern**: Assign distinct lenses (Security, Performance, Coverage) to separate reviewers.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists working in parallel.

## Error Handling & Rollback

- **Coder Failure**: Hand back to Router with error details for re-planning.
- **Reviewer Blockers**: Router prioritizes fixes and re-routes to Coder.
- **Task Lag**: If a task is stuck, lead nudges the teammate or updates status manually.

## Best Practices

1. **Task Sizing**: 5-6 tasks per teammate to maximize productivity.
2. **Predictable Naming**: Assign clear names to teammates when spawning.
3. **Teammate Discovery**: Teammates read `~/.claude/teams/{team-name}/config.json` for member info.
4. **Cleanup First**: Shutdown all teammates before running `Clean up the team`.

## Related Resources

- Run `/workflow-index` for full workflow inventory.
- See `swarm_docs.md` for comprehensive v2.2 documentation.
