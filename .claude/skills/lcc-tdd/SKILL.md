---
name: lcc-tdd
description: TDD workflow (red → green → refactor) using project subagents.
disable-model-invocation: true
---

Run a test-driven development loop.

## Steps

1) Plan the tests (lcc-router)
- Use `lcc-router` to define the smallest testable unit and acceptance criteria.

2) Write failing tests (lcc-coder)
- Delegate to `lcc-coder` to add minimal failing tests first.
- Require: clear test names and minimal fixtures.

3) Implement (lcc-coder)
- Continue with `lcc-coder` to implement the minimal code to make tests pass.

4) Refactor (lcc-refactorer)
- Delegate to `lcc-refactorer` to improve structure while preserving behavior.
- Require: test suite stays green.

5) Review + verify (lcc-reviewer → lcc-tester)
- Reviewer checks correctness and maintainability.
- Tester runs the full suite and reports results.
