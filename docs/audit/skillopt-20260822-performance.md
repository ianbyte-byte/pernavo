# SkillOpt Pilots - performance-review and performance-measurement

- SkillOpt source: `microsoft/skillopt` at `bdfdc30a8e17309c06cdbe8449f01bdecc120203`
- Targets: `skills/performance-review/SKILL.md` and `skills/performance-measurement/SKILL.md`
- Fixtures: `tests/skillopt/performance-review-tasks.json` and
  `tests/skillopt/performance-measurement-tasks.json`
- Method: reviewed real-language tasks with train/validation/test splits and bounded routing/output
  edits; positive observable checks avoid lexical absence as behavior evidence.

## Retained changes

`performance-review` now explicitly labels reviews without executable or runtime evidence as
`static-only`/`unverified`, keeps the performance lens separate from `review-mr` and
`report-writer`, and routes proof to `performance-measurement` and the appropriate narrow overlay.
`performance-measurement` now explicitly labels missing targets/artifacts as unavailable and
unverified, rejects non-comparable before/after runs, requires predeclared thresholds and repeated
observations for regression claims, and keeps database/runtime/web/benchmark evidence separate.

## Evidence

All six tasks for each pilot were scored against the local SkillOpt rule judge with `1.0` hard and
`1.000` soft scores for the retained observable responses. SkillOpt's real `codex` backend did not
produce a completed rollout record in this environment after task mining, and the direct CLI
wrapper did not leave usable output files; those attempts are not counted as semantic evidence.
The mock backend was used only to verify fixture parsing and the replay/gate plumbing, because its
deterministic rule table does not model these natural-language routing rules.

No database, production target, credentials, network workload, or runtime performance target was
used. This remains a prompt-level pilot, not proof of runtime host trigger behavior.
