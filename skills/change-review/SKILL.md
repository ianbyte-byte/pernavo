---
name: change-review
description: >
  Review an existing Git diff, merge request, or pull request for correctness, security, data,
  performance, and maintainability findings. Use when asked to review changes or check code before
  commit. Report findings only; do not silently edit, approve, merge, deploy, or treat tests as proof
  of production behavior.
---

# Change Review

Fix the review target first: working tree, staged diff, or explicit base/revision. Read the complete
diff and affected callers, then inspect high-risk boundaries (auth, data, transactions, external
calls, concurrency, resource amplification, and rollback).

## Review contract

Order findings by severity and include file/line, trigger, impact, and a concrete fix direction.
Separate correctness findings from performance hypotheses and from unavailable SonarQube or target
environment evidence. A green build is supporting evidence, not approval.

```markdown
## Change Review
- Scope / revision: ...
- Evidence: diff | tests | static-only | target-observed
### Findings
1. [P1/P2/P3] `path:line` - concise title
   - Trigger and impact: ...
   - Evidence: ...
   - Suggested correction: ...
### Limits
- Unverified target, deployment, or external checks: ...
```

When no actionable finding exists, say so and name remaining test or environment gaps. If an
external reviewer or quality gate is unavailable, record it as unavailable instead of simulating it.
