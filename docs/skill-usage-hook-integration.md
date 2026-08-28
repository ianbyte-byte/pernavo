# Cross-Agent Skill Usage Logging

Codex and Claude Code now send Hook payloads to the same append-only JSONL file:

```text
~/.codex/skill-usage/events.jsonl
```

The logger is [scripts/skill-usage-hook.py](../scripts/skill-usage-hook.py). It is intentionally
best-effort: malformed input, an unavailable log directory, or a transient write failure returns a
successful hook response so development is never blocked.

Each event uses schema `pernavo.skill_usage_event.v1` and records only routing/evidence metadata:
source (`codex` or `claude`), hook event, event kind, status, session, cwd, tool name, normalized
Skill name, and optional prompt length/hash. Raw prompts, commands, tool responses, credentials, and
database rows are never written. The file and parent directory are restricted to the current user;
append writes use an advisory process lock on Unix.

Configured events:

- `UserPromptSubmit`: prompt submitted
- `PreToolUse` / `PostToolUse`: Skill invocation, Skill file read, or observed tool
- `Stop`: session stop observation

The same logger command is installed in `/Users/chung/.codex/hooks.json` and
`/Users/chung/.claude/settings.json`. The Claude configuration uses the standard settings Hook API;
the Codex configuration uses its `hooks.json` command hooks. Existing Mem0 and OMC hooks remain
unchanged.

Use the existing analyzer against the unified log in a later audit by adding an input adapter for
`pernavo.skill_usage_event.v1`; do not infer loading from a Skill name mention alone. A
`skill_file_read` event is the strongest local evidence that a `SKILL.md` was read, while
`skill_invoked` only records a Skill-tool invocation.

The current adapter is available directly:

```bash
python3 scripts/skill-usage-report.py \
  --events ~/.codex/skill-usage/events.jsonl \
  --date 2026-08-28 --timezone Asia/Shanghai \
  --output docs/audit/skill-events.json
```
