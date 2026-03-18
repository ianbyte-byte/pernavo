# Claude Agent Swarm Guide v2.2

## 1. Definition

In a Claude Code workflow, an Agent Swarm can be implemented as a network of specialized roles coordinated by a Router and linked via a handoff protocol that preserves continuity.

Core capabilities:
- Handoffs: one specialist finishes a phase and hands control to the next
- Parallelization: multiple specialists can be queried in parallel for comparison/verification, then synthesized by Router (or an integrator)
- Shared context: all roles rely on the same project rules and artifacts (for example `CLAUDE.md` + `.claude/session_config.json`)

## 2. Reference implementation (this repository)

### 2.1 Architecture: Router–Worker
- Router: understands the goal, decomposes tasks, selects the next agent, defines acceptance criteria
- Workers:
  - Coder: implements changes
  - Reviewer: audits and suggests fixes
  - Tester: verifies with tests and repro steps

### 2.2 Key artifacts
- `CLAUDE.md`: global rules (role boundaries, handoff schema, agent teams, hooks)
- `.claude/agents/`: Claude Code subagents (Router/Coder/Reviewer/Tester + specialists)
- `.claude/skills/`: Claude Code skills (including the `/swarm` workflow)
- `.claude/settings.json`: project settings (enables agent teams and hooks)
- `.claude/hooks/`: automated quality gate scripts
- `.claude/session_config.json`: per-session pre-flight notes required by the document-first workflow

### 2.3 Key CLI helpers (optional)
The Python package provides a small CLI to validate workflow artifacts:
- `chung-swarm check`: verify required files exist
- `chung-swarm session-config validate`: validate `.claude/session_config.json`
- `chung-swarm handoff validate`: validate a handoff envelope pasted from output

### 2.3 Running with Claude Code (project configuration)

This repo includes Claude Code project configuration for running the swarm directly:
- `.claude/agents/`: project subagents (YAML frontmatter + system prompt)
- `.claude/skills/swarm/`: the `/swarm` workflow skill (manual invocation)

## 3. Handoff protocol

Each handoff must include a JSON object:

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": "Progress summary",
  "next_instructions": "Actionable tasks for the next agent"
}
```

Recommended constraints:
- `summary` must include: done, todo, risks/blockers
- `next_instructions` must be actionable (not just “continue”)

## 4. Parallelization and Team Orchestration (V2)

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration:

### 4.1 Comparison: Subagents vs Agent Teams

| Feature | Subagents | Agent Teams |
| :--- | :--- | :--- |
| **Context** | Own context window; results return to caller | Own context window; fully independent |
| **Communication** | Report results back to main agent only | Teammates message each other directly |
| **Coordination** | Main agent manages all work | Shared task list with self-coordination |
| **Best for** | Focused tasks where only result matters | Complex work requiring collaboration |
| **Token cost** | Lower (summarized back to main) | Higher (each is a separate instance) |

### 4.2 Orchestration
- **Router** acts as the team lead.
- **Enablement**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- **Plan Approval**: Use `Require plan approval` for complex tasks. The lead reviews and approves/rejects plans autonomously while the teammate stays in read-only mode.
- **Display Mode**: Choose between `in-process` (Shift+Down to cycle) and `split-pane` (requires tmux/iTerm2).

### 4.3 Patterns
- **Scientific Debate**: 5+ teammates investigate competing hypotheses and actively disprove each other. Use for root cause analysis or architectural trade-offs.
- **Parallel Review**: Assign reviewers with distinct lenses (Security, Performance, Test Coverage).
- **Cross-layer coordination**: Separate teammates for frontend, backend, and testing working on a single feature.

### 4.4 Coordination & Best Practices
- **Shared Task List**: All agents see task status and claim work. Task claiming uses file locking.
- **Task Sizing**: Aim for 5-6 tasks per teammate to maximize productivity.
- **Context**: Teammates load `CLAUDE.md`, MCP servers, and skills, but NOT conversation history. Include task-specific details in the spawn prompt.
- **Direct Messaging**: Use `message <teammate>` (direct) and `broadcast` (team-wide). Teammates can discover each other via `~/.claude/teams/{team-name}/config.json`.
- **Wait for Completion**: The lead should wait for teammates to finish tasks before proceeding to avoid implementation race conditions.
- **Cleanup**: The lead must shut down teammates and run `Clean up the team` after completion.

### 4.5 Automated Quality Gates
- `TaskCompleted` hook validates that a handoff report or summary exists in the transcript.
- `TeammateIdle` hook ensures teammates don't go idle with unaddressed errors (exit code 2 sends feedback).

### 4.6 Troubleshooting
- **Teammates not appearing**: Check `Shift+Down` in in-process mode or verify `tmux`/`it2` for split-pane.
- **Orphaned tmux sessions**: Use `tmux ls` and `tmux kill-session -t <name>`.
- **Lagging task status**: If a task appears stuck, nudged the teammate or update status manually.
- **Lead shuts down early**: Tell the lead to wait for teammates.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
