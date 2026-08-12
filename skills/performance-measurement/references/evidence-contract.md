# Performance evidence contract

| Field | Requirement |
|---|---|
| scope | exact path/request/job and excluded surface |
| revision | commit, build or deployed version |
| target | environment, instance/region/shard, CPU quota and runtime |
| workload | request shape, data size, concurrency/rate, cache and warm/cold state |
| window | start/end, timezone, duration, sampling interval and sample count |
| result | count, throughput, p50/p95/p99/max, errors/timeouts/rejections |
| causes | plan/profile/trace/queue/GC/I/O evidence and artifact IDs |
| comparison | baseline, changed variable, threshold and reproducibility |
| limits | unavailable tools, sampling gaps, non-comparable inputs and next evidence |

Evidence states are `observed`, `partial`, `degraded`, `unavailable`, and `unverified`. Never convert unavailable to pass, an average to a percentile, or a plan to actual execution. Keep exit codes and HTTP status numeric; keep evidence state semantic.
