# SkillOpt-Sleep Consolidation Check - 2026-08-26

## Scope

- Candidate set: 7 default Skills under `skills/`.
- Reviewed task fixtures: `tests/skillopt/*-tasks.json`, 3 rule cases per entry (21 total).
- Transcript source: local Codex history only; no provider prompts were sent.
- SkillOpt source: `microsoft/skillopt` HEAD `0389ace56339988e16ca5ddab36f0978776fe9b0`.

## Commands and observations

The official `skillopt-sleep` CLI was run through `uvx` with Python 3.11 and `--backend mock` for
each entry. All runs parsed the reviewed fixture and completed the local gate without edits or
auto-adoption. The mock backend has no model response, so its baseline/candidate scores are 0.0 or
unchanged partial rule scores; this is a fixture/gate check, not a quality score or runtime trigger
claim.

The `--backend handoff` run for `engineering-workflow` generated a pending prompt packet under a
temporary staging path. It was moved out of the repository without adoption because no human/model
answer was authorized in this task.

The separate npm wrapper `@sofagent/skillopt` was probed, but its published CLI currently fails with
`Cannot find module '../../package.json'`; it was not used as evidence. The Microsoft
`skillopt-sleep` CLI is the reproducible final-iteration path used here.

## Decision

`KEEP` the 7-entry consolidation. No SkillOpt candidate was adopted because the offline backend
cannot produce a non-empty candidate and the gate correctly rejected it. The next optimization
cycle may use a reviewed, redacted task set with an authorized model backend; until then, the
current entries are the human-authored retained version and their activation remains unverified.
