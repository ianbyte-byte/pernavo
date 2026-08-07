---
name: engineering-work-system
description: >
  Routes cross-domain engineering work and assesses engineering-system health across specialist
  Skills. Use when choosing a workflow, coordinating architecture, release, incident, DORA, or
  continuous-improvement work, or assessing engineering practices. Excludes ordinary focused
  implementation, discovery, planning, QA, diff review, approval, and deployment execution.
---

# Engineering Work System

Act as a cross-domain router and health assessor. Select specialists and their order; do not absorb
their discovery, plan, implementation, verification, review, or release authority.

## Route focused work directly

| Need | Owner |
|------|-------|
| Task-risk governance and required handoffs | `coding-task-controller` |
| Pre-change facts, blindspots, and assumptions | `unknowns-field-guide` |
| Executable plan after discovery | `plan-code-change` |
| Smallest retained production change | `develop-production-code` |
| Independent completed-change behavior evidence | `verify-change-evidence` |
| Diff or MR findings | `review-mr` |
| Reliability, SLO, resilience, incident learning | `aviation-grade-engineering` |
| Behavior-preserving cleanup | `codebase-slimming` |
| Repository capability baseline and next foundation increment | `project-capability-engineering` |
| Repository knowledge inventory, documentation drift, and gardening | `repository-knowledge-gardening` |
| Agent-harness audit | `audit-agent-harness` |
| Agent execution topology | `graph-engineering` |

For a normal code change, automatically compose the controller's risk/authority choice with the
topology layer; do not make the user advance phase by phase. The controller selects `fast`,
`default`, `deep`, or analysis-only. `graph-engineering` realizes the selected cost-aware topology
without taking ownership from lifecycle specialists:

```text
fast:    controller → one accountable implementation owner → proportionate check
default: controller → necessary cheap read-only discovery → one writer → independent verifier
deep:    controller → at most two partitioned read-only investigations → one writer
         → independent verifier → one required review or release gate
```

Use a phase only when its input exists. A material plan is always owned by `plan-code-change`; it
may run in the root context to avoid an unnecessary child startup, but the writer does not prepare
or own it. `review-mr` is optional unless requested or required; verification and diff review are
distinct independent surfaces. Add reliability, topology, security, or domain overlays only when
their own triggers are present.

The default topology is one cheap read-only discovery only for material preflight signals, then one
writer and one independent verifier. Deep work may use no more than two non-overlapping read-only
investigations in parallel. `graph-engineering` owns its reason codes, budgets, child/fallback,
reuse, retry, and stop policy in [cost-aware routing](../graph-engineering/references/cost-aware-routing.md);
this skill does not duplicate those controls. Pause only for a P0 decision with no safe default, new
authority, sensitive disclosure, or destructive operation. If child support is unavailable, report
`degraded-sequential` and continue only with the authorized sequential route.

## Assess cross-domain health

When asked to assess a team or engineering system, score testing defense, observability, resilience,
release quality, code health, and learning loop from 1–5. Identify the one or two largest gaps,
route each gap to a focused owner, and propose a small measurable next step. Do not claim that a
score proves runtime or production health.

## Advisory compatibility playbooks

Architecture, Release, and Continuous Improvement remain compatibility playbooks for a request
that spans domains. They are advisory routing aids, not three new Skills and not substitutes for a
focused specialist.

- **Architecture:** compare options, constraints, reversibility, and ADR needs; route pre-change
  facts to discovery and any resulting code change through the normal lifecycle.
- **Release:** identify readiness, rollback, and authorized deployment gates; route completed-change
  behavior evidence to verification and leave release/production authority to the user, CI, or
  external gate.
- **Continuous Improvement:** connect incidents, DORA observations, and action items to reliability,
  code health, repository capability, or process owners; do not implement the remedies here.

Use [references/routing-guide.md](references/routing-guide.md) for composition examples. Return the
task classification, ordered owners, phase inputs/outputs, and any missing authority or evidence.
