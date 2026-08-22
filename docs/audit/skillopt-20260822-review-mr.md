# SkillOpt Usage-Guided Iteration - review-mr

- SkillOpt source: `microsoft/skillopt` at `bdfdc30a8e17309c06cdbe8449f01bdecc120203`
- Usage source: local `/Users/chung/.codex/thread_history_1.sqlite`, queried on 2026-08-22
- Target: `skills/review-mr/SKILL.md`
- Fixture: `tests/skillopt/review-mr-tasks.json`

## Usage signal

Across persisted user and agent message items, exact repository skill-name mentions ranked
`database-performance` 32, `database-testing` 31, `review-mr` 30, `performance-measurement` 25,
`codebase-slimming` 24, and `performance-review` 21. Catalog snapshots were excluded; these are
prioritization counts, not success rates.

## Retained candidate

`review-mr` now has explicit boundaries for empty diffs, degraded SonarQube evidence, finding
contracts, reviewer provenance, completed-change QA, deployment claims, and report presentation.
It remains the owner of findings and severity while `verify-change-evidence` owns behavior proof
and `report-writer` owns presentation.

## Gate evidence

Six reviewed real-language tasks were split into 3 train, 2 validation, and 1 test cases. The six
retained observable responses each scored `1.0` hard and `1.000` soft under the local SkillOpt rule
judge. Checks use positive outcomes; lexical absence is not used as behavior evidence.

No repository review was approved, merged, pushed, or deployed by this iteration. The changes are
prompt-level improvements and do not prove runtime host trigger behavior.
