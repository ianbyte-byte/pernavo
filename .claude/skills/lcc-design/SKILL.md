---
name: lcc-design
description: Design workflow (requirements → architecture → execution plan) using lcc-product and lcc-architect.
disable-model-invocation: true
---

Run a design-first workflow without implementing code yet.

## Steps

1) Requirements (lcc-product)
- Delegate to `lcc-product` to produce an acceptance checklist and edge cases.

2) Architecture (lcc-architect)
- Delegate to `lcc-architect` to propose a design, interfaces, invariants, and migration plan.

3) Execution plan (lcc-router)
- Delegate to `lcc-router` to turn the design into an actionable plan and choose the next specialist.
