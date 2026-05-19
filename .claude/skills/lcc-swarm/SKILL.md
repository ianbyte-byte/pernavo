---
name: lcc-swarm
description: Run a comprehensive Swarm workflow using specialized agents (Router, Coder, Reviewer, Tester) or Agent Teams for parallel collaboration.
disable-model-invocation: true
---

Run the comprehensive Swarm workflow for this repository. Break complex tasks into specialized stages with clear handoffs or parallel agent teams, leveraging Claude Code's subagent and agent team patterns for context isolation, tool constraint enforcement, and parallel exploration.

## Core Principles

- **Agent Teams**: Preferred for complex tasks requiring parallel exploration, multi-perspective reviews, or adversarial debugging (Scientific Debate).
- **Context Isolation**: Each teammate operates in its own context window, inheriting project rules but not lead conversation history.
- **Shared Task List**: Lead decomposes work; teammates self-claim or are assigned. Aim for 5-6 tasks per teammate.
- **Direct Communication**: Cycle teammates with `Shift+Down`. Use `message <teammate>` for coordination.
- **Automated Quality Gates**: Use hooks (`TaskCreated`, `TaskCompleted`, `TeammateIdle`) to enforce rules.

## Full Workflow

```
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. lcc-router (Haiku, Read-Only)                            │
│    - Context Discovery: Read .claude/docs/claud_platform_menu.md│
│    - Orchestration Choice: Single Handoff vs. Agent Team     │
│    - Task Decomposition: Break into subtasks                 │
│    - Acceptance Criteria: Define done conditions             │
└─────────────────────────────────────────────────────────────┘
    │
    ├──────────────────────────────────────────────────────┐
    │                                                      │
    ▼                                                      ▼
[Single Handoff Path]                            [Agent Team Path]
    │                                                      │
┌──────────────────────┐              ┌──────────────────────────────────────────┐
│ 2. Specialized Agent │              │ 2. Create Agent Team                     │
│    (lcc-coder, etc.) │              │    - Spawn lcc-coder, lcc-reviewer, etc. │
│    - Sequential work │              │    - Require Plan Approval (if risky)    │
└──────────────────────┘              │    - Shared Task List Coordination       │
    │                                 └──────────────────────────────────────────┘
    ▼                                                      │
┌──────────────────────┐                                   ▼
│ 3. Handoff to Next   │              ┌──────────────────────────────────────────┐
│    - JSON Envelope   │              │ 3. Lead Synthesis & Cleanup              │
│    - Summary/Instruct│              │    - Wait for teammates to finish        │
└──────────────────────┘              │    - Synthesis results                   │
                                      │    - Shutdown teammates & Cleanup         │
                                      └──────────────────────────────────────────┘
```

## Team Orchestration (V2.2)

For complex tasks, the Router will propose an **Agent Team**:
1. **Enable Teams**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
2. **Display Mode**: Set `teammateMode: auto` in `settings.json`.
3. **Plan Approval**: Use `Require plan approval` to ensure architectural alignment.
4. **Coordination**: Lead uses "Wait for your teammates to complete their tasks before proceeding".
5. **Shortcuts**: `Shift+Down` (cycle), `Ctrl+T` (tasks), `Enter` (view), `Escape` (interrupt).

## Handoff Envelope Schema (V2.2)

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
    "risk_level": "low|medium|high"
  }
}
```

## Patterns

- **Scientific Debate**: Competing hypotheses investigating the same issue.
- **Parallel Review**: Security, Performance, and Coverage reviews in parallel.
- **Cross-layer coordination**: Frontend, Backend, and Tests specialists.

## Best Practices

1. **Prefer Read-Only First**: Use Router or Explore for discovery before Coder.
2. **Predictable Spawning**: Use "Spawn a teammate using the lcc-[agent-type] agent type".
3. **Graceful Lifecycle**: Shutdown all teammates before "Clean up the team".
4. **Task Sizing**: 5-6 units of work per teammate to maximize efficiency.
