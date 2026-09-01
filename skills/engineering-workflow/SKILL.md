---
name: engineering-workflow
description: >
  Route non-trivial coding work from intent and authority through discovery, planning, one-writer
  implementation, independent verification, and delivery boundaries. Use for normal feature work,
  bug fixes, refactors, risky data or integration changes, or when choosing the smallest safe
  engineering workflow. Keep deployment, production writes, and approval outside local authority.
---

# Engineering Workflow

Use one entry point for the lifecycle. Select the smallest path before doing work and keep each
artifact owned by one role.

## Select a path

- `fast`: trivial copy, comment, or one-seam low-risk edit; one owner and one focused check.
- `default`: normal code change; cheap discovery when the repository/API, dependencies, tests,
  external effects, or runtime surface are uncertain, then one writer and an independent verifier.
- `deep`: permissions, schema, money/data, batch repair, state transitions, scheduled work,
  external writes, rollback uncertainty, or customer-visible consequences. Use bounded discovery,
  an explicit plan, one writer, independent verification, and a human/release gate.
- `analysis-only`: inspect and report. Do not edit, retry writes, deploy, or alter historical data.

Record path, authority boundary, reason, owner, and evidence layer (`static`, `author`,
`independent`, `target-environment`). Ask only for a decision-changing permission or P0 choice.

## Production surface

Implement the authorized behavior with the least production code. Reuse existing types, functions,
and modules before adding new ones. Do not invent files, helpers, abstractions, compatibility
layers, or fallbacks that the authorized change does not require. When replacing a path, delete the
old one in the same batch if evidence allows.

Do not reduce volume by raising cyclomatic complexity: nested branches, flag-driven god functions,
and compressed control flow are not smaller. Tests, explicit types, error handling, and rollback are
not optional savings. Less production code is a slop control, not proof of fewer bugs.

## Lifecycle

1. Discover active revision, configuration, dependencies, data/state ownership, unknowns, and
   rollback constraints. Mark unavailable context as unconfirmed.
2. Write a reviewable plan with goal, do-not-do scope, affected seams, expected behavior, checks,
   rollback/recovery, and human gates.
3. Implement the smallest authorized change with the least production code that does not raise
   cyclomatic complexity. Keep one writer in a shared working tree. The writer does not review
   their own diff. Invoke `change-review` only when a diff review was requested or a
   human/policy gate requires it, and only in a different agent, model, or session. Implement only
   findings selected by the default policy or by a human; do not self-select P2 or P3.
4. Verify independently against the intended behavior, including success and failure/recovery
   paths when relevant. Use `test-engineering` to select test levels, observation methods, and case
   evidence; overlay `data-work`, `performance-work`, `qa`, or `codex-security:*` only when their
   boundaries apply. The changed code is not the verification oracle. Verification does not replace
   requested diff review and does not re-open the review loop.
5. Report evidence and unverified layers. Local tests never prove deployment or production behavior.

After a requested `change-review` pass, follow the default policy when no human is in the loop:
remaining P1 only; do not self-select P2 or P3. Do not re-review in the writer session. Re-review
after fixes needs a fresh context.

Use a bounded independent subagent for discovery or verification only when the selected path needs
it; do not delegate trivial work or create a second writer. Preserve evidence and stop expansion on
failure.

## Output

```text
Selected path and rationale:
Intent and authority boundary:
Production-code delta and cyclomatic complexity:
Owners and completed artifacts:
Missing or blocked phase:
Evidence by layer:
Unverified surfaces and required human/release gate:
```
