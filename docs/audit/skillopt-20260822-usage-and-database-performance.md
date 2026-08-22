# SkillOpt Usage-Guided Iteration - database-performance

- SkillOpt source: `microsoft/skillopt` at `bdfdc30a8e17309c06cdbe8449f01bdecc120203`
- Usage source: local `/Users/chung/.codex/thread_history_1.sqlite`, queried on 2026-08-22
- Target: `skills/database-performance/SKILL.md`
- Fixture: `tests/skillopt/database-performance-tasks.json`

## Usage signal

The query counted exact repository skill names in persisted `agentMessage` and `userMessage`
items, not injected skill-catalog snapshots. Among repository skills, the highest observed counts
were `database-testing` (20 agent-message rows), `database-performance` (16),
`performance-measurement` (11), `review-mr` (8), and `performance-review` (7). The count is a
prioritization signal, not a measure of task quality or successful completion.

## Retained candidate

The database-performance skill now labels source-only analysis `static-only`/`unverified`, requires
query-count and data-volume evidence for N+1 claims, routes read-only review away from
`database-testing`, distinguishes estimated from actual plan evidence, and separates database
findings from reproducible `performance-measurement` comparisons. Schema changes remain authorized,
reversible, and target-scoped.

## Gate evidence

Six reviewed real-language tasks were split into 3 train, 2 validation, and 1 test cases. The six
retained observable responses each scored `1.0` hard and `1.000` soft under the local SkillOpt rule
judge. Checks use positive observable outcomes rather than lexical absence as proof of behavior.
SkillOpt mock replay was used only for fixture parsing and gate plumbing; its deterministic rule
table does not model these database-performance semantics.

No database connection, schema change, production target, or credential access was used. This is a
prompt-level iteration, not proof of runtime host trigger behavior. The repository-wide validator
remains the routing gate.
