---
name: coding-task-controller
description: >
  Governs non-trivial coding work by first separating user intent from granted authority, then
  selecting a proportionate fast, default, or deep path. Use for coding-session policy, lifecycle
  selection, authorization boundaries, or handoff compliance. Excludes discovery detail, plan
  authorship, implementation, QA execution, diff findings, approval, and deployment claims.
---

# Coding Task Controller

Select the minimum safe lifecycle path and confirm each required phase has an owner. This is a
governance skill: it does not discover facts, author a plan, write code, execute behavior checks,
or approve the result.

## Establish intent and authority first

Classify the request before selecting a path:

- **Read-only diagnosis or analysis** authorizes inspection and a report only. It is not authority
  to repair code, alter data, retry an external action, deploy, or change historical records.
- **Implementation** authorizes the necessary in-scope discovery, planning, editing, and local
  verification needed to deliver the requested change. It does not grant unrelated external
  writes, migration execution, deployment, publication, account changes, or production-data work.
- **Verification or delivery** authorizes only the named checks or handoff. Do not infer authority
  to repair a failure, approve a release, or operate an unmentioned target environment.

State an ambiguity when it changes the allowed target or side effect. Otherwise, use the safest
in-scope default and preserve the do-not-do boundary.

## Select a path and automatic topology

Choose one path once, then execute its default topology without asking the user to advance each
stage. This does not authorize a new side effect: pause only for a P0 decision with no safe default,
new permission or target authority, sensitive disclosure, or a destructive operation.

| Task type | Path | Default automatic topology | Deterministic reason code |
|-----------|------|----------------------------|---------------------------|
| Trivial copy, comment, wording, or one-seam low-risk edit | `fast` | direct: one accountable owner performs the focused change and proportionate check | `fast-local` |
| Normal existing-code change | `default` | necessary cheap read-only discovery → one writer → independent verifier | `default-standard` plus applicable preflight signals |
| High-risk or uncertain change | `deep` | at most two partitioned read-only investigations in parallel → one writer → independent verifier; add one requested or required review/release gate | `deep-risk` plus applicable preflight signals |
| User requests read-only analysis | analysis-only | discovery or plan only; stop before implementation | `analysis-only` |

For `default`, start cheap read-only discovery only when a deterministic preflight signal is present:
`unknown-repository-or-api`, `multi-file-or-dependency`, `failing-tests`, `security-data-schema-auth`,
`external-side-effect`, or `ui-runtime-surface`. Record every matching code; do not invent a
discovery branch merely to fill a phase. A material plan remains a required handoff, but it may be
created by [plan-code-change](../plan-code-change/SKILL.md) in the root context when that avoids an
unnecessary child startup; the writer does not own or prepare the plan.

`deep` keeps all existing triggers: irreversible or regulated data, permissions, external writes,
batch or historical repair, schema changes, scheduled/idempotent work, cross-record state
transitions, customer-visible outputs, and uncertainty about consequence, active runtime context,
state ownership, rollback, or recovery. Partition its investigations by non-overlapping questions
(for example, runtime/lifecycle and compatibility/risk), cancel an idle or no-longer-needed branch,
and never add a second writer in the same working tree.

Use [graph-engineering](../graph-engineering/SKILL.md) only to realize this topology; it does not
replace lifecycle owners. Its [cost-aware routing reference](../graph-engineering/references/cost-aware-routing.md)
defines capability tiers, bounded context packets, fallback, and stop rules.

Use `deep` for irreversible or regulated data, permissions, external writes, batch or historical
repair, schema changes, scheduled/idempotent work, cross-record state transitions, or
customer-visible outputs. Escalate when consequences, the active runtime context, state ownership,
rollback, or recovery behavior is uncertain. Do not require the full deep sequence for a low-risk
change merely because a skill exists; select only the handoffs needed for the risk.

## Enforce phase ownership

Use only the owners needed by the selected path. The topology chooses contexts and ordering; these
skills retain ownership of their respective artifacts:

1. [unknowns-field-guide](../unknowns-field-guide/SKILL.md) owns active context, inspected facts,
   unknowns, assumptions, lifecycle boundaries, and discovery evidence.
2. [plan-code-change](../plan-code-change/SKILL.md) owns an executable plan, do-not-do scope,
   rollback, validation requests, and human-review points.
3. [develop-production-code](../develop-production-code/SKILL.md) owns the smallest authorized
   production change, in-code failure and recovery behavior, and the author evidence handoff.
4. [verify-change-evidence](../verify-change-evidence/SKILL.md) owns independent observation of
   single and batch flows, failure/recovery behavior, and the highest verified environment layer.
5. [review-mr](../review-mr/SKILL.md) owns diff or MR findings only when a diff review is requested.

Ask the user only for a P0 decision that locally available evidence cannot answer and no safe
default preserves the do-not-do scope, a new permission or target authority, sensitive disclosure,
or destructive operation. Otherwise route the missing work to its owner and report the reason code.

## Audit compliance

For the selected path, report only:

```text
Selected path and rationale:
Intent and authority boundary:
Completed handoffs and artifact locations:
Missing or blocked phase:
Scope/risk escalation:
Evidence by layer (author, independent, target environment):
Unverified surfaces and required human, release, or deployment gate:
```

Do not turn a completed checklist into approval. A green author test, QA packet, or diff review
does not by itself prove deployment or production behavior.
