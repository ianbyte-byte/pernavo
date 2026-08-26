---
name: performance-work
description: >
  Review and measure hidden performance risks across application, database, runtime, browser, and
  benchmark paths. Use for slow queries, timeout or latency investigations, memory/CPU/GC issues,
  contention, caching, retries, Web Vitals, profiling, load tests, or benchmark regressions.
  Separate static signals from runtime proof and retain workload, environment, percentile, and
  resource evidence.
---

# Performance Work

Start with a static hypothesis, then select the narrowest proof overlay inside this entry point.

## Route by question

- Query shape, N+1, plans, locks, or round trips: use the static portion of `data-work`.
- CPU, allocation, GC, blocking, queues, contention, or I/O: collect a matching runtime profile.
- LCP, INP, CLS, long tasks, resource loading, or layout shifts: collect field/lab Web Vitals.
- Benchmark or capacity claim: define representative workload, warmup, forks/iterations, variance,
  and setup separation before comparing results.
- Suspected bottleneck or regression: run a reproducible measurement with p50/p95/p99, throughput,
  errors/timeouts, resource saturation, cold/hot state, revision, and time window.

## Rules

Do not call a loop, average, green test, single profile, or one-run benchmark a bottleneck. Do not
implement an optimization from a static pattern without authorization. Distinguish `static-only`,
`partial`, `runtime-observed`, and `unavailable`; route code changes to `engineering-workflow`.

## Finding format

```markdown
## Performance Work
- Scope / revision / target: ...
- Evidence state: static-only | partial | runtime-observed
- Workload and window: ...
### Findings
1. [P1/P2/P3] `path:line` - signal and amplification variable
   - Impact hypothesis: ...
   - Required evidence: ...
   - Smallest safe action: ...
### Limits
- Unobserved or unavailable: ...
```
