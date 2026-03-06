---
name: lcc-perf
description: Performance workflow (measure → optimize → re-measure) using lcc-performance-optimizer.
disable-model-invocation: true
---

Run a performance optimization loop.

## Steps

1) Define the metric (lcc-router)
- Use `lcc-router` to define the target metric and acceptable regression thresholds.

2) Optimize (lcc-performance-optimizer)
- Delegate to `lcc-performance-optimizer`.
- Require: baseline measurement, change summary, and post-change measurement.

3) Review + verify (lcc-reviewer → lcc-tester)
- Reviewer checks correctness and maintainability of the optimization.
- Tester runs relevant tests and reports results.
