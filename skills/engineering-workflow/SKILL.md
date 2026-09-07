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
`independent`, `target-environment`). A request to implement or fix authorizes that scoped local
work. Reuse prior authorization; prepare the concrete result before any still-required release
approval. Resolve routine choices from context and ask only when an answer materially changes the
outcome. Ask asynchronously when supported and continue independent work; silence does not approve
a consequential decision. If a Skill guideline blocks requested work, cite its exact file and rule,
explain the conflict, and apply explicit user instructions within host and tool constraints.

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
2. For `default` or `deep`, record the goal, affected behavior, checks, recovery, and any unresolved
   decision. A short in-session plan is enough unless risk or repository policy needs an artifact;
   `fast` needs only the intended edit and focused check.
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

For `default` and `deep`, delegate independent verification when the host supports it. Parallelize
bounded read-only discovery with writer work when they are independent and it saves time or improves
coverage. Give each agent its scope, inputs, expected artifact, and stopping condition. Keep one
writer; do not delegate trivial work. If an independent role is unavailable, finish authorized
preparation and report the verification gap without claiming independence.

## Continue long tasks

Treat corrections, added constraints, and status questions as steering; keep the original objective
unless the user replaces or cancels it. After answering a side question, resume remaining work.
At a context transition, retain the active goal, accepted constraints, completed checks, failed
approaches and their causes, open decisions, and artifact references in supported session notes.
Retrieve earlier messages or tool results when a missing detail matters, then confirm the current
revision before reusing old test results. Do not repeat completed work merely because context was
compacted. Native notes and history search require actual host support; do not invent tools or
enable experimental configuration as part of an ordinary coding task.

## Output

Lead with the delivered behavior, relevant check results, and any remaining blocker. Use concise
paragraphs for a small change. For substantial work, include path, owners, production-code delta and
cyclomatic complexity, evidence layer, and remaining release gates. Keep detailed evidence in linked
artifacts; do not turn this checklist into mandatory headings for every reply.
