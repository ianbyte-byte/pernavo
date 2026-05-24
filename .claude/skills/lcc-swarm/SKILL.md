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
- **Automated Quality Gates**: Enforced via hooks (`TaskCompleted`, `TeammateIdle`).

## Full Workflow (V2.2)

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Haiku, Read-Only)                            │
│    - Context Discovery: Read .claude/docs/claud_platform_menu.md│
│    - Task Decomposition: Break into subtasks (5-6 per agent) │
│    - Orchestration: Propose Subagents or Agent Team          │
│    - Spawning: Use "Require plan approval" for complex tasks │
└─────────────────────────────────────────────────────────────┘
    │
    ├───────────────────────┬───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ 2a. Sequential│   │ 2b. Parallel  │   │ 2c. Patterns  │
│ Handoffs      │   │ Agent Team    │   │ (Debate,      │
│ (Handoff JSON)│   │ (Mailbox)     │   │  Review)      │
└───────────────┘   └───────────────┘   └───────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 3. Implementation (Coder) │
            │    - Plan Approval first  │
            │    - Mailbox notification │
            │    - Update Task List     │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 4. Verification (Reviewer)│
            │    - Specific "lenses"    │
            │    - Mailbox feedback     │
            │    - Output LGTM          │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 5. Testing (Tester)       │
            │    - Run pytest/watch     │
            │    - repro steps in task  │
            └───────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │ 6. lcc-router (Cleanup)   │
            │    - Synthesize findings  │
            │    - Shutdown teammates   │
            │    - Clean up the team    │
            └───────────────────────────┘
```

## Team Orchestration

1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Shared Task List**: Lead manages tasks; teammates claim and complete.
3. **Mailbox**: Teammates use `message` and `broadcast` to coordinate.
4. **Plan Approval**: Lead reviews teammate plans before implementation.
5. **Cleanup**: Lead shuts down teammates before running `Clean up the team`.

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

## Related Resources

- Run `/workflow-index` for full workflow inventory
- See `CLAUDE-1.md` for Swarm Global Rules
- See `swarm_docs.md` for the comprehensive V2.2 guide
