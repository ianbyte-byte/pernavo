---
name: unknowns-field-guide
description: >
  Discovers pre-change facts, unknowns, assumptions, constraints, and evidence around a named
  code or runtime seam. Use for blindspot passes, reverse interviews, first investigation, tracing,
  or risky money, data, permissions, integration, SQL, scheduled, or stateful work. Excludes
  change-plan authorship, implementation notes, production-code changes, post-change QA, diff
  review, approval, and deployment claims.
---

# Unknowns Field Guide

Investigate what must be known before a change can be planned. Produce discovery evidence only;
do not choose the lifecycle path, write an implementation plan, modify code, or report completed
behavior.

## Discovery contract

- Start from the named file, method, endpoint, SQL, field, payload, log line, or issue.
- Inspect code, configuration, tests, schemas, logs, source records, or authorized runtime state
  before treating a claim as fact.
- Separate inspected facts, assumptions, unconfirmed questions, and evidence pointers.
- Ask the user only for a P0 decision that local evidence cannot cheaply answer and has no safe
  default. Never turn a guess into an answer.
- Keep the report proportional: inline for a small seam, durable only when risk or the user needs
  a handoff.

## Perform the discovery pass

1. Restate the requested outcome and named seam without proposing a change.
2. Run a blindspot pass across state transitions, historical compatibility, retries and idempotency,
   transaction and concurrency boundaries, permissions, external consumers, observability, and
   rollback constraints as relevant.
3. Classify each item as Known Known, Known Unknown, Unknown Known, or Unknown Unknown; give each
   an evidence pointer or reason it remains unconfirmed.
4. Rank risks P0/P1/P2. P0 means the unanswered item can materially change behavior or data safety.
5. Use a reverse interview only for remaining decision-changing gaps; provide a safe default and
   concrete risk whenever one exists.
6. End with a discovery handoff: confirmed facts, assumptions/defaults, unresolved blockers,
   do-not-do constraints found, and evidence locations.

Use [REFERENCE.md](REFERENCE.md) for the blindspot and reverse-interview templates.

## Handoff boundary

Hand sufficient discovery to [plan-code-change](../plan-code-change/SKILL.md). If a request is
discovery-only, stop with the report. If new facts invalidate a plan during implementation, return
to discovery; do not rewrite the plan or implementation record here.
