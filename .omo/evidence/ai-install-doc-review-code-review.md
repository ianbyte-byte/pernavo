# Code quality review — AI installation documentation

## Scope and evidence inspected

- Goal: review `AI_INSTALL.md` and the README link only against the repository's 14 Skills, local harness, examples, `scripts/agentctl.py`, and `scripts/validate-skills.sh`.
- Changed documentation reviewed: `/Users/chung/Developer/Code/loongclaude/AI_INSTALL.md`, `/Users/chung/Developer/Code/loongclaude/README.md`.
- Repository facts verified: 14 `skills/*/SKILL.md` files; the named Phase 1 examples; command implementation; validation script; relevant tests.
- CLI contract verified against `npx --yes skills@1.5.21 --version` and `--help`. The document correctly warns that CLI behavior may drift.

## Validation run

- PASS — `python3 scripts/agentctl.py doctor --config harness/examples/agentctl.json --json`
- PASS — `python3 scripts/agentctl.py explain --config harness/examples/agentctl.json --event harness/examples/event.json --json`
- PASS — `python3 scripts/agentctl.py memory search --config harness/examples/agentctl.json --query canonical --json`
- PASS — `python3 -m unittest discover -s tests -v` (15 tests)
- PASS — `./scripts/validate-skills.sh` (14 Skills, 42 corpus cases)
- PASS — `git diff --check -- AI_INSTALL.md README.md`

## Skill-perspective check

Ran the required `omo:programming` and `omo:remove-ai-slops` perspectives before judging maintainability and tests.

- `programming`: no brittle prompt/prose tests, implementation-mirroring tests, untyped escape hatch, needless abstraction, or unjustified boundary parsing introduced by these documentation changes. The existing `agentctl` parser is a required file-input boundary, not needless production normalization.
- `remove-ai-slops`: no deletion-only, tautological, or implementation-constant-mirroring tests were added. The existing harness tests exercise observable CLI behavior and malformed input; no tests merely pin the new prose. The documentation itself does not add needless production data extraction or parsing.

## Findings

### CRITICAL

None.

### HIGH

1. **The documented update command cannot preserve the authorized target-Agent boundary.**

   `/Users/chung/Developer/Code/loongclaude/AI_INSTALL.md:254`–`/Users/chung/Developer/Code/loongclaude/AI_INSTALL.md:278` instructs an update with `skills update --global --yes <14 names>` after a conflict check limited to Codex at `/Users/chung/Developer/Code/loongclaude/AI_INSTALL.md:141`–`/Users/chung/Developer/Code/loongclaude/AI_INSTALL.md:156`. The verified 1.5.21 `skills update --help` exposes only `--global`, `--project`, and `--yes`; it has no `--agent` option. Therefore this command cannot be shown to update only the authorized `codex` target and can affect matching global installations for other agents. This contradicts the contract's no-scope-expansion rule at `/Users/chung/Developer/Code/loongclaude/AI_INSTALL.md:14`–`/Users/chung/Developer/Code/loongclaude/AI_INSTALL.md:24` and fails the requested targeted-agent acceptance criterion.

   Required fix: make the update section fail closed for 1.5.21 when more than the authorized agent is present, or replace it with a documented per-agent process whose scope is verifiable. Do not present the current update command as a targeted Codex update. Re-check the current CLI help at execution time as already required by the guide.

### MEDIUM

None.

### LOW

None.

## Positive review notes

- The README link is valid and directs AI installers to the authority document: `/Users/chung/Developer/Code/loongclaude/README.md:7`.
- The guide clearly defines source/installed/loaded/executed proof limits, local versus remote source checks, conflict STOP rules, install/rollback commands, host reload, runtime evidence limitations, Phase 1 Harness and canonical JSONL-memory boundary, and a final report template.
- Its stated 14-Skill set matches the repository and its validator output.
- The Phase 1 read-only claim matches the inspected command implementation and passed non-mutation test; it does not claim hook, model, MCP, or tool execution proof.

## Decision

- `codeQualityStatus`: **BLOCK**
- `recommendation`: **REQUEST_CHANGES**
- `blockers`:
  - Correct the global-update procedure so it cannot update Skills outside the user-authorized target agent/scope under CLI 1.5.21.
