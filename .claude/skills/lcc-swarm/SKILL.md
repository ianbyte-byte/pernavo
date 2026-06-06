---
name: lcc-swarm
description: Run a comprehensive Swarm workflow using specialized agents: Router, Coder, Reviewer, Tester and optional specialists.
disable-model-invocation: true
---

Run the comprehensive Swarm workflow for this repository. Break complex tasks into specialized stages with clear handoffs or parallel agent teams, leveraging Claude Code's subagent and agent team patterns for context isolation, tool constraint enforcement, and parallel exploration.

## Core Principles

- **Agent Teams**: Use for parallel work, shared task lists, and inter-agent coordination. Ideal for research, review, and complex debugging.
- **Context Isolation**: Keep exploration/implementation out of main conversation.
- **Tool Constraints**: Use read-only agents for exploration, write-enabled for implementation.
- **Specialization**: Match tasks to focused system prompts (Router, Coder, etc.).
- **Automated Quality Gates**: Use hooks (`TaskCompleted`, `TeammateIdle`, `TaskCreated`) to enforce rules.

## Full Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Haiku, Read-Only)                            │
│    - Context Discovery: Read .claude/docs/claud_platform_menu.md│
│    - Task Decomposition: Break into subtasks (5-6 per agent) │
│    - Acceptance Criteria: Define done conditions             │
│    - Specialist Selection: Choose next role(s) or Team      │
└─────────────────────────────────────────────────────────────┘
    │
    ├───────────────────────┬───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────────┐
│ 2a. lcc-     │   │ 2b. lcc-     │   │ 2c. Agent Team    │
│ architect     │   │ product       │   │ (Parallel Work)   │
│ (Optional)    │   │ (Optional)    │   │ (Sonnet Teammates)│
└───────────────┘   └───────────────┘   └───────────────────┘
    │                       │                       │
    └───────────────────────┴──────────┬────────────┘
                                       │
                                       ▼
            ┌──────────────────────────────────────────┐
            │ 3. Implementation (lcc-coder)            │
            │    - Plan Approval (if risky)            │
            │    - Implement changes                   │
            │    - Message team via Mailbox            │
            └──────────────────────────────────────────┘
                                       │
                                       ▼
            ┌──────────────────────────────────────────┐
            │ 4. Review (lcc-reviewer)                 │
            │    - Security/Perf/Coverage focus        │
            │    - Coordinate via message/broadcast    │
            │    - Output LGTM if OK                   │
            └──────────────────────────────────────────┘
                    │               │
              [Issues]         [LGTM]
                    │               │
                    ▼               ▼
            ┌──────────┐    ┌───────────────────┐
            │ lcc-     │    │ 5. Verification   │
            │ coder    │    │    (lcc-tester)   │
            │ (fix)    │    │    - Run tests    │
            │          │    │    - Share logs   │
            └──────────┘    └───────────────────┘
                    │               │
                    └───────────────┘
                            │
                      [Passing]
                            │
                            ▼
            ┌──────────────────────────────────────────┐
            │ 6. lcc-router (Wrap-Up)                  │
            │    - Verify acceptance                   │
            │    - Synthesize results                  │
            │    - Cleanup Team                        │
            └──────────────────────────────────────────┘
```

## Team Orchestration (V2.2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Shared Task List**: Lead manages tasks; teammates claim and complete.
3. **Mailbox**: Teammates use `message` and `broadcast` to coordinate.
4. **Hooks**: Automated validation via `lcc-quality-gate.sh`.
5. **Lifecycle**: Lead waits for teammates, synthesizes, shuts down teammates, and cleans up.

## Patterns for Agent Teams

- **Scientific Debate**: Multiple investigators testing competing hypotheses to find root causes.
- **Parallel Code Review**: Different reviewers for Security, Performance, and Coverage.
- **Cross-Layer Coordination**: Simultaneous work on Frontend, Backend, and Tests.

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

1. **Rich Context**: Spawn prompts MUST include task-specific details as teammates don't inherit history.
2. **Team Sizing**: 3-5 teammates is optimal. Use Sonnet for implementation/review.
3. **Task Sizing**: 5-6 tasks per teammate to keep everyone productive.
4. **Avoid Conflicts**: Partition tasks by file sets to prevent concurrent edits.
5. **Plan Approval**: Use for risky tasks to review approach before execution.
6. **Wait & Synthesize**: Lead should wait for all tasks to finish before summarizing.

## Project Subagents

Location: `.claude/agents/`

- **lcc-router** - Orchestration & planning
- **lcc-coder** - Implementation
- **lcc-reviewer** - Code review
- **lcc-tester** - Testing & verification
- **Specialists**: architect, product, security-reviewer, debugger, etc.

## Related Resources

- Run `/workflow-index` for full workflow inventory
- See `.claude/docs/claude_code/AGENT_TEAMS.md` for team coordination details
- See `.claude/docs/INDEX.md` for project docs navigation
