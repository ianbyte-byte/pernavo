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
| Agent-harness audit | `audit-agent-harness` |
| Agent execution topology | `graph-engineering` |

For a normal code change, route only the phases requested or required by risk:

```text
coding-task-controller → unknowns-field-guide → plan-code-change
→ develop-production-code → verify-change-evidence → review-mr
```

Use a phase only when its input exists. `review-mr` is optional unless a diff review is requested;
verification and diff review are distinct independent surfaces. Add reliability, topology, security,
or domain overlays only when their own triggers are present.

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
  code health, or process owners; do not implement the remedies here.

Use [references/routing-guide.md](references/routing-guide.md) for composition examples. Return the
task classification, ordered owners, phase inputs/outputs, and any missing authority or evidence.
