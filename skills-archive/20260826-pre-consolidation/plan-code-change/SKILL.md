---
name: plan-code-change
description: >
  Produces executable, reviewable plans for code changes after enough discovery has established
  the seam, facts, unknowns, and constraints. Use for a requested implementation plan, scoped
  change design, rollback plan, or reviewable pre-change handoff. Excludes discovery-only work,
  production-code implementation, QA execution, diff review, approval, and deployment claims.
---

# Plan Code Change

## Evidence and plan boundaries

- Reject or return a handoff with missing seam, facts, unknowns, constraints, do-not-do scope, or evidence boundary; never invent facts or silently resolve a P0 decision.
- Every atomic step names one owner seam, observable expected behavior, validation request, rollback/recovery, and human-review point where applicable. A plan is not implementation, QA, approval, or deployment evidence.

Turn confirmed discovery into one plan another engineer can review and execute. Do not inspect for
new facts, write production code, run QA, approve a result, or claim a deployment outcome.

## Entry gate

Accept a handoff only when it identifies:

- the requested outcome and inspected seam;
- facts, unresolved unknowns, and assumptions or safe defaults;
- explicit constraints and do-not-do boundaries; and
- the required completion or evidence boundary.

If these are missing, return the exact discovery gap to
[unknowns-field-guide](../unknowns-field-guide/SKILL.md). Do not invent facts or silently resolve
a P0 decision.

## Produce the plan

Make the primary artifact sufficient for a reviewer to approve, reject, or return for discovery.

```markdown
# Change Plan: <short name>

## Goal
<observable outcome and success condition>

## Do-not-do scope
<explicit non-goals and excluded files, behaviors, data, or authority>

## Assumptions and open decisions
- <fact, assumption, safe default, or blocker>: <evidence and consequence>

## Affected scope
- Files/modules:
- Interfaces/data/configuration:
- Tests or executable consumers:

## Atomic steps
1. <smallest change>
   - Owner seam: <file/module/interface>
   - Expected behavior: <observable result>
   - Validation to request: <focused command or surface>

## Validation and evidence handoff
| Step | Check or observable surface | Expected result | Evidence owner |
|------|-----------------------------|-----------------|----------------|

## Rollback or recovery
<revert, backup, feature-flag, migration, or why no rollback applies>

## Human-review points
- <role or authority>: <decision or invariant to confirm>
```

Split steps until each names one owned seam, an expected behavior, and a validation request.
Identify irreversible writes, external calls, migrations, permission changes, and state transitions
explicitly. For a no-change or read-only request, plan only the authorized analysis outcome.

## Handoff

- Hand the approved plan and its assumptions to
  [develop-production-code](../develop-production-code/SKILL.md) for the smallest owned change.
- Hand a completed-change test matrix and proof boundary to
  [verify-change-evidence](../verify-change-evidence/SKILL.md) for independent behavior evidence.
- Hand a completed diff to [review-mr](../review-mr/SKILL.md) for findings, not approval.

Do not merge these phases unless the user explicitly asks for a multi-phase task; then identify
one owner for each phase and keep the plan artifact separate from execution evidence.
