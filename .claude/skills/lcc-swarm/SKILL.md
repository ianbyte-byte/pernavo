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
- **Automated Quality Gates**: Use hooks (`TaskCompleted`, `TeammateIdle`) to enforce rules.

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

## Team Orchestration (New in V2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Patterns**:
   - **Scientific Debate**: 5+ teammates investigate competing hypotheses and challenge each other via mailbox.
   - **Parallel Review**: Specialists for Security, Performance, and Test Coverage.
   - **Cross-layer coordination**: Frontend, Backend, and Tests specialists.
3. **Lead Responsibilities**:
   - Provide comprehensive spawn prompts (no history inheritance).
   - Enforce task sizing (5-6 tasks per teammate).
   - Use `Require plan approval` for implementation teammates.
   - Wait for teammates to finish before synthesis.
   - Cleanup: shut down teammates first, then `Clean up the team`.
4. **Shared Task List**: Lead manages tasks and dependencies; teammates self-claim.
5. **Mailbox**: Teammates use `message` and `broadcast` to coordinate.
6. **Hooks**: Automated validation via `lcc-quality-gate.sh`.

## Handoff Envelope Schema (Enhanced)

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

When Router identifies specific needs, delegate to specialist agents first:

- **lcc-architect**: Design, architecture, refactoring guidance
- **lcc-product**: Requirements clarification, user story mapping
- **lcc-security-reviewer**: Security audit (can be called after Reviewer)
- **lcc-debugger**: Complex debugging scenarios
- **lcc-refactorer**: Large-scale code reorganization
- **lcc-performance-optimizer**: Performance tuning
- **lcc-simplifier**: Code simplification
- **lcc-docs-writer**: Documentation generation
- **lcc-release-manager**: Release orchestration

## Error Handling & Rollback

- **Coder Failure**: Hand back to Router with error details for re-planning
- **Reviewer Blockers**: Router prioritizes fixes and re-routes to Coder
- **Test Failures**: Include minimal repro steps + suggested fix path
- **Context Drift**: Re-run Router to re-sync with current state

## Best Practices

1. **Prefer Read-Only First**: Use Explore or Router for discovery before Coder
2. **Session Config**: For platform API tasks, always update `.claude/session_config.json` first
3. **Parallel Exploration**: Use multiple read-only agents to research separate areas, then Router synthesizes
4. **Incremental Delivery**: Break into small, reviewable chunks
5. **Model Selection**:
   - Router → Haiku (fast, read-only)
   - Coder/Reviewer/Tester → inherit (balanced capability)

## Project Subagents

Location: `.claude/agents/`

- **lcc-router** - Orchestration & planning
- **lcc-coder** - Implementation
- **lcc-reviewer** - Code review
- **lcc-tester** - Testing & verification
- **lcc-architect**, **lcc-product**, **lcc-security-reviewer**, etc. - Specialists

## Related Resources

- Run `/workflow-index` for full workflow inventory
- See `.claude/docs/claude_code/SUBAGENTS.md` for Claude Code subagent best practices
- See `.claude/docs/INDEX.md` for project docs navigation
