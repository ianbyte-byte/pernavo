---
name: lcc-swarm
description: Run a comprehensive Swarm workflow using specialized agents: Router, Coder, Reviewer, Tester and optional specialists.
disable-model-invocation: true
---

Run the comprehensive Swarm workflow for this repository. Break complex tasks into specialized stages with clear handoffs or parallel agent teams, leveraging Claude Code's subagent and agent team patterns for context isolation, tool constraint enforcement, and parallel exploration.

## Core Principles

- **Agent Teams (V2.2)**: Use for parallel work, shared task lists, and inter-agent coordination.
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
│    - Orchestration: Decision between Single Agent vs Team    │
│    - Acceptance Criteria: Define done conditions             │
└─────────────────────────────────────────────────────────────┘
    │
    ├───────────────────────┬───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ 2a. lcc-     │   │ 2b. lcc-     │   │ 2c. Parallel  │
│ architect     │   │ product       │   │ Agent Team    │
│ (Optional)    │   │ (Optional)    │   │ (Explore/Debate)│
└───────────────┘   └───────────────┘   └───────────────┘
    │                       │                       │
    └───────────────────────┴───────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 3. lcc-coder              │
            │    - Implement changes    │
            │    - Plan approval if team│
            │    - Minimal, testable    │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 4. lcc-reviewer           │
            │    - Security review      │
            │    - Correctness check    │
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
            │    - Synthesis & Cleanup  │
            │    - Document outcome     │
            └───────────────────────────┘
```

## Team Orchestration (V2.2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Shared Task List**: Lead manages tasks; teammates claim and complete.
3. **Context**: Lead passes rich context in spawn prompts.
4. **Patterns**: Scientific Debate, Parallel Review, Cross-layer coordination.
5. **Hooks**: Automated validation via `lcc-quality-gate.sh`.

## Handoff Envelope Schema (V2.2)

```json
{
  "type": "handoff",
  "next_role": "Router|Coder|Reviewer|Tester|...",
  "summary": {
    "progress": "Detailed accomplishment list",
    "remaining": "Outstanding tasks",
    "risks": "Potential blockers",
    "changes": "Key file modifications"
  },
  "acceptance_criteria": [
    "List of verifiable conditions for completion"
  ],
  "next_instructions": "Specific, actionable task list",
  "context": {
    "risk_level": "low|medium|high"
  }
}
```

## Specialized Agent Integration

When Router identifies specific needs, delegate to specialist agents first:

- **lcc-router** - Orchestration & planning
- **lcc-coder** - Implementation
- **lcc-reviewer** - Code review
- **lcc-tester** - Testing & verification
- **lcc-architect**, **lcc-product**, **lcc-security-reviewer**, etc. - Specialists

## Related Resources

- Run `/workflow-index` for full workflow inventory
- See `CLAUDE-1.md` for Swarm Global Rules V2.2
- See `swarm_docs.md` for the comprehensive Swarm Guide V2.2
