---
name: lcc-security
description: Security review workflow using lcc-security-reviewer with remediation guidance.
disable-model-invocation: true
---

Run a security-focused review on a change or feature.

## Steps

1) Security review (lcc-security-reviewer)
- Delegate to `lcc-security-reviewer`.
- Require: threat model, prioritized findings, and a verification plan.

2) Remediation (lcc-coder)
- If findings require code changes, hand off to `lcc-coder` with concrete remediation tasks.

3) Verify (lcc-tester)
- Delegate to `lcc-tester` to run tests and provide evidence that fixes work.
