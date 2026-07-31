# Routing Decision Guide

Use this guide only for cross-domain routing. A focused request should load its specialist directly.

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

## Common compositions

| Request | Ordered route |
|---------|---------------|
| Normal existing-code change | controller → discovery → plan → implementation → verification; add review only when requested |
| High-risk money/data/state change | controller (deep) → discovery → plan → implementation → verification → review → human/release gate |
| Discovery-only question | discovery only |
| Plan-only request after facts are known | plan only |
| Completed-change acceptance evidence | verification only; return failures to implementation |
| Existing-diff findings | review only; add verification only when behavior evidence is also requested |
| Behavior-preserving cleanup | codebase-slimming → verification as needed → review |
| Reliability improvement | aviation-grade-engineering; add lifecycle owners only for an actual code change |
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
codebase-slimming, and actual code changes through the lifecycle above.
