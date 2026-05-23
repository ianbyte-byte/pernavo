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

## 4. Parallelization and Team Orchestration (V2.2)

V2.2 leverages native Claude Code **Agent Teams** with advanced orchestration and parallel exploration:

### 4.1 Orchestration
- **Router** acts as the team lead and orchestrates the lifecycle.
- **Enabling**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
- **Display Modes**:
  - `in-process`: Default, cycles via `Shift+Down`.
  - `split panes`: Requires tmux or iTerm2, set via `teammateMode: "tmux"`.
- **UI Shortcuts**:
  - `Shift+Down`: Cycle through teammates.
  - `Ctrl+T`: Toggle the shared task list.
  - `Enter`: View a teammate's full session.
  - `Escape`: Interrupt a teammate's current turn.
- **Plan Approval**: For risky tasks, use `Require plan approval before they make any changes`. The lead reviews plans autonomously.
- **Task Sizing**: Aim for **5-6 tasks per teammate**. If tasks are too few, ask the lead to split them further.

### 4.2 Patterns
- **Scientific Debate**: 5+ teammates investigate competing hypotheses. Key: "Have them talk to each other to try to disprove each other's theories".
- **Parallel Review**: Split review criteria into independent domains (Security, Performance, Test Coverage).
- **Cross-layer coordination**: Separate teammates own frontend, backend, and tests simultaneously.

### 4.3 Coordination
- **Context Isolation**: Teammates load `CLAUDE.md` but **do not inherit the lead's conversation history**. Spawn prompts must be self-contained.
- **Shared Task List**: Automatic dependency management. Tasks unblock as dependencies complete.
- **Mailbox**: Direct messaging via `message <teammate>` and `broadcast`.
- **Wait for Completion**: If the lead starts working instead of delegating, use: "Wait for your teammates to complete their tasks before proceeding".
- **Cleanup**: 1. Shut down all teammates. 2. Lead runs `Clean up the team`.

### 4.4 Automated Quality Gates
- `TaskCompleted` hook validates that a handoff report or summary exists in the transcript.
- `TeammateIdle` hook ensures teammates don't go idle with unaddressed errors.

## 5. Testing guidance

Suggested scenario:
- From an empty directory, scaffold a FastAPI project with unit tests

Expected loop:
- Coder generates code → Tester runs tests → Reviewer outputs LGTM or a fix list → iterate until verified
