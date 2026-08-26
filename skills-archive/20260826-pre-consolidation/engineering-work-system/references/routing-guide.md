# Routing Decision Guide

Use this guide only for cross-domain routing. A focused request should load its specialist directly.
For normal retained changes, compose lifecycle governance with the cost-aware topology automatically;
do not require the user to authorize each ordinary internal handoff.

## Lifecycle composition

```text
Govern risk → discover facts → plan change → implement → verify behavior → review diff
    coding-task   unknowns       plan-code     develop       verify-change    review-mr
    controller    field-guide    change        production    evidence
                                           code
```

Each arrow is a handoff, not one owner doing all work. Stop at the user-authorized phase. A failed
verification returns to implementation; a missing fact returns to discovery; a requested diff
finding goes to review. Neither verification nor review grants release or production authority.

## Automatic normal-change composition

`coding-task-controller` selects the risk path and authority boundary. `graph-engineering` then
selects an economy, standard, or deep topology using its deterministic reason codes. For the usual
standard case, run only necessary cheap read-only discovery, then one writer and an independent
verifier. For deep work, use at most two non-overlapping read-only investigations, one writer, and
one verifier; add a review only when independently required. This is routing composition, not new
ownership: discovery, planning, implementation, verification, and review retain their focused
owners.

Do not prompt the user between those ordinary handoffs. Pause for a P0 decision without a safe
default, new authority, sensitive disclosure, or destructive operation. When child agents are
unavailable, use the authorized sequential fallback and label it `degraded-sequential`. See
[cost-aware routing](../../graph-engineering/references/cost-aware-routing.md) for limits,
packets, retry, reuse, privacy, and stop gates.

## Common compositions

| Request | Ordered route |
|---------|---------------|
| Normal existing-code change | controller → necessary cheap discovery → `plan-code-change` for a material plan (root context permitted) → one writer → independent verification; add review only when requested |
| High-risk money/data/state change | controller (deep) → discovery → plan → implementation → verification → review → human/release gate |
| Discovery-only question | discovery only |
| Plan-only request after facts are known | plan only |
| Completed-change acceptance evidence | verification only; return failures to implementation |
| Existing-diff findings | `review-mr` with automatic `sonarqube-review` preflight (unavailable results stay labeled evidence); add verification only when behavior evidence is also requested; hand formal report packaging to `report-writer` when a report artifact is required |
| Existing SonarQube project quality evidence | `sonarqube-review` only; do not install scanners or run a new analysis implicitly |
| Formal report from already-collected evidence | `report-writer`; keep finding ownership with the upstream specialist |
| Behavior-preserving cleanup | codebase-slimming → verification as needed → review |
| Reliability improvement | aviation-grade-engineering; add lifecycle owners only for an actual code change |
| Repository capability assessment | project-capability-engineering; route a selected increment through lifecycle owners only when implementation is authorized |
| Repository knowledge gardening | repository-knowledge-gardening; add lifecycle owners only for authorized documentation edits or automation |
| Agent-harness audit | audit-agent-harness; add review only after an actual diff exists |

## Cross-domain advisory playbooks

### Architecture

Compare options, constraints, reversibility, and ADR requirements. Route facts to discovery and an
approved option that changes code through plan, implementation, verification, and any requested
review. Architecture advice does not approve the implementation.

### Release

Identify required evidence, rollback, environment, and release authority. Verification records
observed behavior; the user, CI, or external release gate owns deployment and production claims.

### Continuous Improvement

Use incident observations, DORA signals, and engineering-health scores to identify a focused
owner and measurable follow-up. Route reliability to aviation-grade-engineering, code health to
codebase-slimming, repository-wide foundation gaps to project-capability-engineering, documentation
knowledge drift to repository-knowledge-gardening, and actual retained changes through the lifecycle
above.
