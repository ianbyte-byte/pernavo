---
name: unknowns-field-guide
description: >
  Discover hidden constraints before any non-trivial code change. Use for explicit blindspot
  or unknown discovery, first investigation or tracing, facts versus assumptions,
  fast/default/deep paths, and risky money, data, permissions, integrations, SQL, scheduled,
  or stateful work. The coding-task-controller selects risk; this Skill owns discovery before
  task-specific implementation. A dedicated planning Skill owns a plan-only request unless the
  user explicitly asks for this discovery workflow. Exclude MR-only or post-change review,
  production-acceptance policy, and unrelated explanation.
---

# Unknowns Field Guide

The biggest risk in AI coding is not that the model cannot write code. It is that hidden constraints were never discovered. Prompts, specs, and rules are maps; the real codebase, data, business rules, and runtime behavior are the territory.

Use this skill to scale discovery to the task's risk. It should prevent blind implementation, not create process theater.

## Operating contract

- Start from the user's named seam: file, method, endpoint, SQL, field, payload, log line, or issue.
- Inspect real code or runtime evidence before treating a statement as fact.
- Ask the user only for P0 decisions that cannot be discovered locally and have no safe default.
- Keep artifacts proportional: inline notes for small work; files only when the task is large, risky, or the user asked for durable handoff.
- Continue implementation after the required unknowns are resolved or explicitly defaulted.

## Core principles

1. **Discover unknowns first.** Never jump from request to implementation.
2. **Separate facts from guesses.** Mark every claim as known, assumed, or unconfirmed.
3. **Prefer evidence over questions.** Read code, logs, docs, tests, schemas, or runtime state before interrupting the user.
4. **Plan, record, review.** Plan before coding, record meaningful deviations while coding, review after coding.
5. **State the do-not-do scope.** Prevent silent scope creep.

## Workflow selection

| Path | Steps | When |
|------|-------|------|
| `fast_path` | blindspot-pass → implementation-plan → post-implementation-review | Copy, log, local UI, comment-only, or single-seam low-risk edits |
| `default` | blindspot-pass → optional reverse-interview → implementation-plan → implementation-notes when deviations occur → post-implementation-review | Most non-trivial coding tasks |
| `deep_path` | blindspot-pass → reverse-interview if P0/P1 unknowns remain → implementation-plan → implementation-notes → post-implementation-review | Required for high-risk domains |

### Deep path triggers

Use `deep_path` if any are true: amounts, taxes, inventory, invoicing, receipts, write-offs, contracts, external API push/re-push/status callback/third-party sync, batch SQL repair/deletes/schema changes on real data, scheduled tasks, idempotency, repeated execution, state machine transitions, permissions, historical data repair, customer-visible documents or reports.

If unsure after inspecting the seam, use `deep_path`. If the user explicitly says "先分析", "先定位问题", or "不要改", stop after the analysis or plan artifact.

For a plan-only request, let the dedicated planning Skill own the task. Compose this Skill only
when the user explicitly requests blindspot or unknown discovery, or when work proceeds toward
implementation and the discovery gate becomes mandatory.

## Quality gates

**Before coding**: blindspot-pass done; P0 unknowns resolved, safely defaulted, or explicitly carried as risk; do-not-do scope explicit.

**During coding**: new P0 unknowns pause implementation; deviations get recorded; scope expansion requires a reason and validation.

**After coding**: summarize behavior change, validation results, remaining risks, and reviewer checks.

## Anti-patterns (forbidden)

- Implementing directly on the user's first message.
- Designing without inspecting the real codebase.
- Producing only the implementation, never the "do-not-do" scope.
- Plan ≠ actual implementation with no recorded reason.
- Reporting "done" without validation, risks, and open questions.
- Treating unconfirmed user assumptions as facts.
- Adding fallback code that masks the root cause without explaining why it is correct.
- Silently expanding the file scope during coding.

## Sub-workflows

1. **blindspot-pass** — find unknown unknowns before coding. See [REFERENCE.md §1](REFERENCE.md#1-blindspot-pass).
2. **reverse-interview** — interview the user for missing critical info. See [REFERENCE.md §2](REFERENCE.md#2-reverse-interview).
3. **implementation-plan** — verifiable, auditable, rollback-able plan. See [REFERENCE.md §3](REFERENCE.md#3-implementation-plan).
4. **implementation-notes** — track execution, deviations, new findings. Required for `deep_path`; optional for small `default` tasks with no deviation. See [REFERENCE.md §4](REFERENCE.md#4-implementation-notes).
5. **post-implementation-review** — explain changes, risks, validation, quiz. See [REFERENCE.md §5](REFERENCE.md#5-post-implementation-review).

Full templates and example outputs: [REFERENCE.md](REFERENCE.md).

## Controller prompt (bootstrap a coding session)

```text
You are a rigorous software development assistant.

For any non-trivial coding task, you must NOT jump straight to implementation.
Run the unknowns-field-guide workflow first, scaled to task risk.

Default path: blindspot-pass → reverse-interview only for unresolved P0/P1
questions → implementation-plan → implementation-notes when work is risky
or deviates from plan → post-implementation-review.

If the task involves money, inventory, invoicing, contracts, historical data,
external APIs, batch SQL, state machines, or scheduled tasks, you MUST use
deep_path.

Output rules:
- Distinguish facts, guesses, assumptions, and unconfirmed questions.
- Always state the "do-not-do" scope.
- Every implementation step must have a validation method.
- On new P0 unknowns, pause and resolve or record a safe default before continuing.
- At the end, output: change summary, validation results, remaining risks,
  reviewer checklist, and a comprehension quiz.

Forbidden: modifying code without investigating it; implementing without a
plan; asking questions that local evidence can answer; silently expanding
scope; writing guesses as facts; reporting "done" without risks and validation.
```

## Quick-start checklist

```text
[ ] Classify task: trivial / normal / risky
[ ] Pick path: fast_path / default / deep_path
[ ] blindspot-pass → produce inline or durable report
[ ] If unresolved P0/P1 unknowns remain → reverse-interview or record safe defaults
[ ] implementation-plan → include do-not-do scope and validation
[ ] Implement, keeping notes current when risk, deviations, or new findings require it
[ ] post-implementation-review → summarize validation, risks, checklist, quiz
[ ] Hand off: plan + notes + review
```
