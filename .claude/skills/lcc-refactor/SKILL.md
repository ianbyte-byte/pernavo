---
name: lcc-refactor
description: Refactoring workflow (identify → refactor → verify) using lcc-refactorer with review and testing.
disable-model-invocation: true
---

Run a safe refactoring workflow.

## Steps

1) Scope (lcc-router)
- Use `lcc-router` to define what must stay the same (behavior and interfaces).

2) Refactor (lcc-refactorer)
- Delegate to `lcc-refactorer`.
- Require: incremental changes, tests stay green, and a before/after summary.

3) Review + verify (lcc-reviewer → lcc-tester)
- Reviewer focuses on readability, layering, and risk.
- Tester runs the full suite.
