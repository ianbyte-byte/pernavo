---
name: lcc-deps
description: Dependency upgrade workflow using lcc-dependency-upgrader with review and verification.
disable-model-invocation: true
---

Upgrade dependencies safely.

## Steps

1) Plan (lcc-router)
- Use `lcc-router` to define upgrade scope, constraints, and risk tolerance.

2) Upgrade (lcc-dependency-upgrader)
- Delegate to `lcc-dependency-upgrader`.
- Require: minimal-step upgrade plan, changes applied, and test results.

3) Review + verify (lcc-reviewer → lcc-tester)
- Reviewer checks for risk, config correctness, and dependency pinning rationale.
- Tester runs the full suite and reports results.
