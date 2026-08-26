# Repository Knowledge Model

Classify material documentation so an agent can discover the right source and a maintainer can see
how it becomes stale. Use existing project terminology where it is unambiguous; this model is for
assessment, not mandatory directory naming.

## Roles

| Role | Examples | Primary question |
|---|---|---|
| Entry map | README, AGENTS.md, contribution index | Where should this task look next? |
| Architecture | architecture map, domain/package layering, ADR | How is the system organized and why? |
| Product | product specs, user journeys, acceptance contracts | What behavior is intended? |
| Execution | active/completed plans, decision and progress logs | What work is underway or was completed? |
| Generated reference | schema, API, CLI, configuration reference | What facts can be reproduced from canonical inputs? |
| Operations | runbook, SLO, recovery and release guide | How is the system observed and operated? |
| Policy | security, reliability, quality and contribution policy | Which decisions or controls govern work? |
| History | incident, migration, deprecation and archived decisions | What past context must remain distinguishable? |

## Authority classes

- `authoritative`: the named approved source for a claim family.
- `derived`: reproducible from an authoritative input and generator.
- `reference`: helps navigation but does not decide conflicts.
- `historical`: records past context and must not be silently rewritten as current truth.
- `unknown`: authority has not been established.

A document may be authoritative for one claim and only a reference for another. Record claim
families rather than labeling an entire large file authoritative by default.

## Maintenance modes

- `human-owned`: product intent, architectural rationale, security policy, SLO targets, retention.
- `generated`: schemas, route tables, CLI/config references with a reproducible generator.
- `hybrid`: generated facts plus reviewed explanations.
- `ephemeral`: short-lived working notes with an expiry or promotion rule.
- `frozen-history`: retained record changed only through an explicit correction/addendum process.
- `unknown`: maintenance mechanism or owner is not established.

## Statuses

- `verified`: the named verification ran successfully at the recorded revision and environment.
- `documented-only`: present and discoverable, but behavior or enforcement is unobserved.
- `confirmed-drift`: a deterministic source or trusted observation contradicts it.
- `suspected-drift`: evidence indicates risk but cannot decide which source is wrong.
- `contradiction`: two candidate authorities disagree.
- `duplicate`: overlapping sources lack a clear precedence or ownership rule.
- `unknown`: insufficient evidence.

## Progressive-disclosure checks

Trace at least one representative path:

```text
task intent → entry map → domain/product index → detailed source → executable check or owner
```

Record dead ends, cycles, duplicated instructions, missing indexes, unbounded entry files, stale
links, and sources that require undisclosed external context. A long document is not automatically a
failure when its audience and selective-loading path are clear.
