# Host runtime log (`~/.pernavo`)

Default install merges a best-effort command hook that appends to:

```text
~/.pernavo/logs/runtime.jsonl
```

The installing agent copies [scripts/pernavo-runtime-hook.py](../scripts/pernavo-runtime-hook.py) to
`$HOME/.pernavo/hooks/runtime-hook.py` so the command path survives the temporary checkout. The
logger never blocks the host. It records routing and completion-claim metadata for evolving Skills
and the API-test Stop gate. Raw prompts, commands, tool responses, credentials, and JSONL bodies are
not written.

## Layout

```text
~/.pernavo/
  hooks/runtime-hook.py
  logs/runtime.jsonl
```

Directory mode `0700`, log and hook file mode `0600`. Override the home with `PERNAVO_HOME` and the
log path with `PERNAVO_RUNTIME_LOG`. Set `PERNAVO_RUNTIME_SOURCE=claude` or `codex` in the hook
command.

## Schema

Each line is `pernavo.runtime_event.v1`: source, hook event, kind, status, session, cwd, tool name,
normalized Skill name, optional prompt length/hash. Stop / TaskCompleted / SubagentStop also record
`claims_complete` and `matrix_present` as booleans and `last_message_length` without the message
text.

Kinds include `prompt_submitted`, `skill_invoked`, `skill_file_read`, `session_started`,
`session_stop`, `task_completed`, `subagent_stop`, and `hook_observed`.

## Host events

| Host | Events |
|---|---|
| Claude Code | `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `TaskCompleted` |
| Codex | `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop` |

Merge into existing hook arrays. Do not replace Mem0, skill-usage, or the API-test Stop gate.

## Read

```bash
python3 scripts/skill-usage-report.py \
  --events ~/.pernavo/logs/runtime.jsonl \
  --date 2026-09-01 --timezone Asia/Shanghai \
  --output docs/audit/runtime-events.json
```

This is local evolution evidence. It does not prove a Skill was `target-observed` in a new session.
The optional Codex logger `~/.codex/skill-usage/events.jsonl` is unchanged and is not part of default
install.
