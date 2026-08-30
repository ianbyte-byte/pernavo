---
name: change-review
description: >
  Review an existing Git diff, merge request, or pull request for correctness, security, data,
  performance, and maintainability findings. Use when asked to review changes, check code before
  commit, review an MR/PR, /review-mr, or 审查改动/提交前自查. Report findings only; do not silently edit,
  implement fixes, approve, merge, deploy, or treat tests as proof of production behavior.
---

# Change Review

Fix the review target first: working tree, staged diff, or explicit base/revision. Read the complete
diff and affected callers, then inspect high-risk boundaries (auth, data, transactions, external
calls, concurrency, resource amplification, and rollback).

This Skill owns findings on an existing diff. It is not the writer and not the behavior verifier.
Do not implement, patch, or silently edit reported issues in the review session. Hand only
human- or policy-selected fixes to `engineering-workflow` in a different agent, model, or session.
Route behavior evidence to `test-engineering`.

## Review contract

Order findings by severity and include file/line, trigger, impact, and a concrete fix direction.
Separate correctness findings from performance hypotheses and from unavailable SonarQube or target
environment evidence. A green build is supporting evidence, not approval.

- P1: correctness, security, data loss, broken contract, or missing rollback on a destructive change.
- P2: real maintainability or test-gap cost that a human or explicit policy may still defer.
- P3: style, nits, optional refactors. Never promote a nit to P1.

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
### Loop
- Stop recommendation: continue (remaining P1, or policy-selected P2) | stop (no remaining P1; nits optional)
- Re-review: fresh context required after fixes | not applicable
```

One review pass reports the current diff. Do not re-review the same findings in this session, and do
not loop until the findings list is empty; later passes tend to restate prior items or promote style
preferences into defects. Stop when there is no remaining P1 unless a human or explicit policy still
requires selected P2 work. P3/nits are optional. When no P1 remains, say the review loop should stop
even if P2/P3 items exist. When no actionable finding exists, say so and name remaining test or
environment gaps.

A re-review after fixes must start in a fresh context (different agent, model, or session) against
the new revision. Same-session "review again" is not an independent review.

If an external reviewer or quality gate is unavailable, record it as unavailable instead of simulating it.
