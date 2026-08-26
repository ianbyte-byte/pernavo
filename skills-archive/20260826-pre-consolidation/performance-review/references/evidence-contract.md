# Performance evidence contract

## Required fields

| Field | Requirement |
|---|---|
| scope | exact files/path/request/job and excluded surface |
| revision | commit, build or deployed version |
| target | environment, instance/region/shard, CPU quota and runtime |
| workload | request shape, data size, concurrency/rate, cache and warm/cold state |
| window | start/end, timezone, duration, sampling interval and sample count |
| result | count, throughput, p50/p95/p99/max, errors/timeouts/rejections |
| causes | plan/profile/trace/queue/GC/I/O evidence and artifact IDs |
| comparison | baseline, changed variable, threshold and reproducibility |
| limits | unavailable tools, sampling gaps, non-comparable inputs and next evidence |

## State vocabulary

- `observed`: command/tool output or target observation is retained and addressable.
- `partial`: some surfaces were observed; named gaps remain.
- `degraded`: intended tool or environment failed, with the failure captured.
- `unavailable`: no authorized target/tool; no result inferred.
- `unverified`: static hypothesis or third-party/public benchmark only.

Never convert unavailable to pass, an average to a percentile, or a plan to an actual execution. Keep numeric `http_status`/exit code separate from the evidence state.
