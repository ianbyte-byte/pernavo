# Agent Teams (Claude Code)

Upstream:
- Agent teams: https://code.claude.com/docs/en/agent-teams

## What agent teams are

Agent teams let you coordinate multiple Claude Code instances working together in parallel.

Key differences from subagents:
- Subagents: work within a single session, report results back to parent
- Agent teams: coordinate across separate sessions, with direct inter-agent communication

## Enable agent teams

Agent teams are experimental and disabled by default. Enable them by adding:
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to your `settings.json`
- Or set as an environment variable

## How to use

After enabling, tell Claude to create an agent team and describe the task and team structure you want in natural language.

Example:
> I'm designing a CLI tool that helps developers track TODO comments across their codebase. Create an agent team with 3 specialists to work on this.

## Advanced Patterns

- **Scientific Debate**: Spawn 5+ agent teammates to investigate different hypotheses. Have them talk to each other to try to disprove each other's theories.
- **Parallel Review**: Spawn reviewers with distinct lenses (Security, Performance, Test Coverage).

## Architecture

Component roles:
- **Team Lead**: Your main Claude Code session that creates the team, spawns teammates, assigns tasks, and synthesizes results
- **Teammates**: Separate Claude Code instances with their own context windows, working independently on assigned tasks
- **Task List**: Shared work items with dependency tracking. Tasks auto-unblock when dependencies complete
- **Mailbox**: Messaging system enabling direct communication between agents—not just reporting to the lead

## Hooks

Agent team hooks:
- `TeammateIdle`: runs when a teammate is about to go idle. Exit with code 2 to send feedback and keep the teammate working
- `TaskCompleted`: runs when a task is being marked complete. Exit with code 2 to prevent completion and send feedback

## Display modes

### In-process mode (default)
- Works in any terminal, including VS Code integrated terminal
- Use `Shift+Down` to cycle through teammates (wraps to lead)
- Press `Enter` to view a teammate's session, `Escape` to interrupt
- Press `Ctrl+T` to toggle the task list

### Split-pane mode
- Each teammate gets its own terminal pane
- Requires **tmux** or **iTerm2**
- Not supported in: VS Code's integrated terminal, Windows Terminal, Ghostty
- Click into a teammate's pane to interact directly

## Configuration

Set `teammateMode` in your `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": 1
  },
  "teammateMode": "auto"
}
```

`teammateMode` options:
- `"auto"` (default): Uses split panes if already in a tmux session, otherwise falls back to in-process
- `"tmux"`: Enables split panes, auto-detects tmux or iTerm2
- `"in-process"`: Forces in-process mode

## Limitations

Known limitations:
- Session resumption
- Task coordination
- Shutdown behavior

## Project-specific guidance

`CLAUDE.md` works normally: teammates read `CLAUDE.md` files from their working directory. Use this to provide project-specific guidance to all teammates.

## When to use

Use agent teams for:
- Sustained parallelism
- Tasks that exceed your context window
- Multi-agent collaboration with direct communication

Use subagents for:
- Multi-step workflows (sequence of subagents)
- Research or verification within your session
- Tasks that don't need inter-agent coordination
