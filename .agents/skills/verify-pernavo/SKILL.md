---
name: verify-pernavo
description: >
  Re-run Pernavo catalog validation before claiming a skill-system edit is valid.
  Use in /Users/chung/Developer/Code/loongclaude after changing skills/, the
  trigger corpus, README skill entries, or scripts/validate-skills.sh. Do not
  use in other repositories, for application behavior, or as a diff review.
---

# Verify Pernavo

Use only when the working tree is `/Users/chung/Developer/Code/loongclaude`.
This repository has no running app. The surface is the catalog validator and
the usage report. Do not apply `verify-change` here.

Evidence directory: `${TMPDIR:-/tmp}/pernavo-verify/`. Create it before a drive.
Cleanup never deletes that directory.

## Launch

Short-lived commands. No server and no second instance.

```bash
cd /Users/chung/Developer/Code/loongclaude
mkdir -p "${TMPDIR:-/tmp}/pernavo-verify"
```

## Doctor

Read-only. Run this before the first drive and again after a failed drive.

```bash
test -f scripts/validate-skills.sh
test -f tests/skill-trigger-corpus.tsv
test -d skills/engineering-workflow
test -s "${HOME}/.codex/skill-usage/events.jsonl"
python3 .agents/skills/verify-pernavo/doctor.py
```

The events file is required only for the usage-report feature. If it is
missing, catalog validation can still run. Mark usage-report `blocked` and
name the missing file. Do not point the report at a different database.

## Drive

From the repository root. One command per feature. Do not start a second
validator in parallel, because `npx skills add . --list` uses this checkout.

Catalog validation:

```bash
./scripts/validate-skills.sh
```

Usage report, only after doctor sees the events file. Write the JSON into the
evidence directory, not into `docs/`.

```bash
python3 scripts/skill-usage-report.py \
  --events "${HOME}/.codex/skill-usage/events.jsonl" \
  --output "${TMPDIR:-/tmp}/pernavo-verify/skill-usage.json"
```

## Evidence

Save stdout, stderr, and the exit code. A passing catalog run prints
`PASS: 11 skills validated and listed; corpus has 33 cases.` and exits 0.
`Skill is valid!` without that PASS line is not success. A usage report is
successful only when the process exits 0 and the output JSON exists.

Bad catalog input: set `PERNAVO_SKILL_VALIDATOR` to a path that is not a file.
The command must exit non-zero and name that path. Do not leave the variable
set. Do not edit `skills/` to manufacture a failure.

## Cleanup

The validator deletes its own temporary Skills CLI listing. Do not kill
processes by name. Leave `${TMPDIR:-/tmp}/pernavo-verify/` in place.

## Features

Read [features/README.md](features/README.md) and drive every feature that
doctor can reach. One passing feature does not cover the other.
