---
name: coding-task-controller
description: >
  Governs non-trivial coding work by selecting a fast, default, or deep risk path and requiring
  phase handoffs. Use for coding-session policy, risk-path selection, handoff compliance, or
  deep-path enforcement. Excludes discovery detail, change-plan authorship, implementation, QA
  execution, diff findings, approval, and deployment claims.
---

# Coding Task Controller

Select the minimum safe lifecycle path and confirm each phase has an owner. This is a governance
skill: it does not discover facts, author a plan, write code, execute behavior checks, or approve
the result.

## Select a path

| Task type | Path | Required handoffs |
|-----------|------|-------------------|
| Trivial copy, comment, wording, or one-seam low-risk edit | `fast` | focused scope → implementation → proportionate verification |
| Normal existing-code change | `default` | discovery → plan → implementation → verification → optional diff review |
| High-risk or uncertain change | `deep` | discovery → plan → implementation → independent verification → diff review → human/release gate |
| User requests read-only analysis | analysis-only | discovery or plan only; stop before implementation |

Use `deep` for money, taxes, inventory, invoicing, contracts, permissions, external writes or
callbacks, batch SQL, schema or historical-data repair, scheduled/idempotent work, state
transitions, and customer-visible documents or reports. Escalate when consequences, active runtime,
or rollback are uncertain.

## Enforce phase ownership

Require these artifacts before advancing:

1. [unknowns-field-guide](../unknowns-field-guide/SKILL.md) owns inspected facts, unknowns,
   assumptions, and discovery evidence.
2. [plan-code-change](../plan-code-change/SKILL.md) owns an executable plan, do-not-do scope,
   rollback, validation requests, and human-review points.
3. [develop-production-code](../develop-production-code/SKILL.md) owns the smallest approved
   production change and the author evidence handoff.
4. [verify-change-evidence](../verify-change-evidence/SKILL.md) owns independent behavior-oriented
   test and runtime evidence.
5. [review-mr](../review-mr/SKILL.md) owns diff or MR findings when a diff review is requested.

Ask the user only for a P0 decision that locally available evidence cannot answer and no safe
default preserves the do-not-do scope. Otherwise route the missing work to its owner.

## Audit compliance

For the selected path, report only:

```text
Selected path and rationale:
Completed handoffs and artifact locations:
Missing or blocked phase:
Scope/risk escalation:
Unverified surfaces and required human or release gate:
```

Do not turn a completed checklist into approval. A green author test, QA packet, or diff review
does not by itself prove deployment or production behavior.
