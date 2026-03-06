---
name: lcc-debug
description: Debug workflow (repro → isolate → fix → verify) using lcc-debugger with review and testing.
disable-model-invocation: true
---

Run a debugging workflow.

## Steps

1) Route (lcc-router)
- Use `lcc-router` to define expected behavior and a minimal reproduction plan.

2) Debug and fix (lcc-debugger)
- Delegate to `lcc-debugger`.
- Require: exact repro commands, root cause evidence, smallest safe fix, and verification results.

3) Review (lcc-reviewer)
- Delegate to `lcc-reviewer` for correctness and maintainability review.

4) Verify (lcc-tester)
- Delegate to `lcc-tester` to run tests and report results.
