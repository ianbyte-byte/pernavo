---
name: lcc-docs
description: Documentation workflow using lcc-docs-writer (update docs to match current behavior).
disable-model-invocation: true
---

Update documentation to match current code behavior.

## Steps

1) Identify doc gaps (lcc-router)
- Use `lcc-router` to list which docs need updates and what must be added/removed.

2) Write docs (lcc-docs-writer)
- Delegate to `lcc-docs-writer`.
- Require runnable commands and minimal examples.

3) Review (lcc-reviewer)
- Delegate to `lcc-reviewer` focusing on clarity and correctness.
