---
name: develop-production-code
description: >
  Implements the smallest retained production-code change from an approved plan with risk-tiered
  reading, artifact discipline, rollback awareness, and an evidence handoff. Use for production
  features, fixes, refactors, or prototype-to-production work. Excludes discovery-only work,
  plan authorship, independent runtime QA, diff findings, approval, deployment, and production
  claims.
---

# Develop Production Code

Implement a bounded, reviewable production change. Retain responsibility for the code and accurate
author evidence, but do not self-approve behavior, replace independent QA, or turn local results
into deployment proof.

## Receive the approved handoff

Require a plan that names the observable outcome, changed seam, constraints, do-not-do scope,
assumptions, rollback or recovery, validation requests, and human-review points. If a material fact
or P0 decision is missing, return it to [unknowns-field-guide](../unknowns-field-guide/SKILL.md) or
[plan-code-change](../plan-code-change/SKILL.md); do not silently expand the task.

## Preserve the implementation contract

- Keep the accountable engineer responsible for requirements, design boundaries, failure behavior,
  and the correctness of the retained code.
- Understand inputs, state transitions, side effects, dependencies, and rollback path before
  editing the relevant seam.
- Treat tests, coverage, complexity limits, linters, and deterministic checkers as evidence, not
  proof that the requirement or oracle is correct.
- Preserve unrelated dirty work and repository conventions. Do not make irreversible operations,
  external writes, migrations, or deployments without explicit authority.

## Classify artifacts and risk

| Artifact class | Examples | Required treatment |
|----------------|----------|--------------------|
| Retained production | Application code, migrations, configuration, shipped scripts | Maintain, read, test, and own for its lifetime |
| Retained verification | Committed tests, fixtures, analyzers, CI rules | Review its oracle and maintenance cost |
| Disposable verification | Probes, fuzz harnesses, differential implementations | Sandbox and discard or keep outside the product |
| Generated evidence | Logs, reports, screenshots, benchmark results | Preserve provenance and actual observation scope |

Use [references/risk-evidence-matrix.md](references/risk-evidence-matrix.md) and the highest
applicable tier: R0 disposable, R1 routine and reversible, R2 material data/permission/external or
state impact, R3 critical/irreversible/security/regulatory impact. Escalate when runtime, rollback,
or oracle strength is uncertain.

Read the retained artifact in proportion to risk: inspect the complete retained diff for R1; trace
changed data and state end-to-end and request an independent lane for critical R2 invariants; require
qualified human review and separately derived acceptance criteria for R3.

## Implement the smallest owned change

1. Edit only the approved seams in reviewable slices.
2. Re-read the final diff and changed contracts; avoid speculative abstractions, silent fallbacks,
   and compatibility shims for unshipped shapes.
3. Add focused author checks or verification artifacts where they exercise the changed contract.
   Prefer independent expected values, fixtures, properties, differential checks, fault injection,
   or trusted source records when the implementation and test could share one misunderstanding.
4. Record only checks actually run, their commands, targets, results, and artifact locations. Name
   failures, skips, and unverified layers.

## Hand off completed work

Provide this author packet to
[verify-change-evidence](../verify-change-evidence/SKILL.md):

```text
Requested outcome and approved plan:
Changed scope / do-not-do scope:
Risk tier, artifact classes, and critical invariants:
Author checks actually run with commands, targets, and results:
Known failures, skipped checks, and proof boundary:
Rollback or recovery status:
Required runtime/manual scenarios and human-review points:
```

The verification owner determines behavior evidence. Route an existing diff to
[review-mr](../review-mr/SKILL.md) for findings; this skill neither reviews nor approves its own
diff. A green author check is not independent QA, deployment evidence, or a production claim.
