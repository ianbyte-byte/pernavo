# chung-agent-swarm

A Claude Code–first “Router–Worker” workflow kit:

- Project workflow rules: `CLAUDE.md`
- Claude Code subagents + skills: `.claude/`
- A small Python CLI to validate handoffs and session config: `chung-swarm`

## Quickstart

```bash
python -m pip install -e ".[dev]"
```

Verify the repository has the expected Claude Code workflow files:

```bash
chung-swarm check
```

Validate the session pre-flight file:

```bash
chung-swarm session-config validate
```

Validate a handoff envelope (reads from stdin):

```bash
chung-swarm handoff validate
```

## Run with Claude Code (recommended)

This repo includes Claude Code project subagents and skills:
- Subagents: `.claude/agents/` (lcc-router / lcc-coder / lcc-reviewer / lcc-tester)
- Workflow skill: `.claude/skills/lcc-swarm/` (invoke with `/lcc-swarm`)

In Claude Code:
1) Run `/lcc-swarm` and start with lcc-router to break down the task and produce a handoff JSON
2) Based on `next_role`, delegate to the matching subagent (or let Claude delegate automatically)
3) Iterate Coder → Reviewer → Tester until Reviewer outputs final LGTM

### Available skills

Run `/lcc-workflow-index` in Claude Code to see the full, up-to-date list. Common entry points:
- `/lcc-swarm`: generic Router → Coder → Reviewer → Tester loop
- `/lcc-feature`: requirements → design → implement → review → test
- `/lcc-bugfix`: triage → reproduce → fix → review → verify
- `/lcc-tdd`: red → green → refactor
- `/lcc-simplify`: eliminate redundancy and simplify control flow (behavior-preserving)
- `/lcc-review`: structured review (optional security pass)
- `/lcc-security`: security-focused review + remediation loop
- `/lcc-perf`: measure → optimize → re-measure
- `/lcc-sql-optimize`: SQL optimization based on MySQL index principles (美团技术团队)
- `/lcc-docs`: update documentation to match behavior
- `/lcc-release`: release notes + checklist (no publishing)
- `/lcc-triage`: incident triage playbook

### Available subagents

Core roles:
- lcc-router, lcc-coder, lcc-reviewer, lcc-tester

Specialists:
- lcc-product, lcc-architect, lcc-debugger, lcc-refactorer
- lcc-security-reviewer, lcc-performance-optimizer, lcc-sql-optimizer, lcc-docs-writer
- lcc-release-manager, lcc-incident-triage, lcc-dependency-upgrader
- lcc-git-worktree-manager

### Agent Teams (V2.2)

For parallel work, use `Create an agent team...`:
- **Patterns**: Scientific Debate, Parallel Review, Cross-layer coordination.
- **Shortcuts**: `Shift+Down` (cycle), `Ctrl+T` (tasks), `Enter` (view).
- **Lifecycle**: Wait for completion -> Synthesis -> Shutdown -> Cleanup.

## Structure

- `CLAUDE.md`: Swarm global rules (role boundaries, handoff format)
- `.claude/docs/claud_platform_menu.md`: primary doc-first menu (Claude Platform + Claude Code links)
- `.claude/session_config.json`: per-session pre-flight notes (JSON schema + context window requirements)
- `swarm_docs.md`: workflow guide and extension guidance
- `src/chung_agent_swarm/`: CLI helpers
  - `handoff.py`: handoff schema + parsing/validation
  - `session_config.py`: session_config validation/template
  - `project.py`: repository layout checks

## Handoff protocol

Each handoff must include a JSON object in output:

```json
{
  "type": "handoff",
  "next_role": "Reviewer",
  "summary": "Progress summary",
  "next_instructions": "Actionable tasks for the next agent"
}
```

## Development

Run tests:

```bash
python -m pytest
```
