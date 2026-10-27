# Usage report

## Sub-features

- Read the local Skill usage JSONL
- Write a secret-free aggregate JSON report

## How to get to it (user POV)

After doctor confirms ~/.codex/skill-usage/events.jsonl exists, run the report script. There is no UI.

## Driving it with the shell

```bash
cd /Users/chung/Developer/Code/loongclaude
python3 scripts/skill-usage-report.py \
  --events "${HOME}/.codex/skill-usage/events.jsonl" \
  --output "${TMPDIR:-/tmp}/pernavo-verify/skill-usage.json"
```

## Gotchas

- A missing events file means blocked, not a pass. Do not switch to --db unless the user named that database.
- Do not write the report into docs/audit/. That path is a sample, not the proof location.
- The report is not proof that a skill loaded or that a task completed. It only proves the report command ran.
