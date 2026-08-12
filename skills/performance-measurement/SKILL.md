---
name: performance-measurement
description: >
  Design or execute a reproducible performance investigation and evidence pack for a suspected
  bottleneck, latency regression, or capacity risk. Use for 性能测量, 压测方案, profiling plan,
  benchmark evidence, p95/p99 analysis, USE/RED analysis, or runtime proof. Require workload,
  environment, time window, distribution, resource saturation, and before/after comparability.
  Do not infer a bottleneck from source patterns, averages, a single profile, or a green test.
---

# Performance Measurement

把“可能慢”变成可复核证据。先定义问题和负载，再测量；结果要区分 observed、partial、degraded 和 unavailable。

## 流程

1. 记录 revision、目标环境、服务/实例/分片、版本、配置、数据量、请求率、并发、payload、缓存状态和持续时间。
2. 建立基线：同一 workload 至少重复多次；对比 p50/p95/p99、吞吐、错误/超时、CPU、内存/分配、GC、队列/等待、I/O 和下游耗时。
3. 以 USE 检查 CPU、内存、磁盘、网络、线程池、连接池和业务队列的利用率、饱和度、错误；以 RED/SRE 检查流量、错误、延迟、饱和度。
4. 以 trace 定位端到端尾延迟中的下游、重试、排队和串行阶段；记录采样率，不能把“没采样到”当作“没有”。
5. 只改一个变量；用相同负载复测，记录效应大小、误差、回归和未覆盖面。性能改善必须与资源/错误代价一起判断。

## 最小证据包

- `manifest.json`：目标、revision、环境、命令、时间窗、负载和工具版本；不要写 token。
- 延迟分布：请求数、p50/p95/p99、最大值、分组维度和 histogram/bucket 或原始样本摘要。
- 资源证据：USE/RED 指标的原始名称、单位、窗口、实例范围和查询表达式。
- trace/profile：trace ID 或 artifact hash、采样率、采样时长、CPU/allocation/lock/wall 事件选择。
- before/after：相同 workload 的差异、误差和是否达到业务 SLO；不可比时标记 `not-comparable`。

随附脚本 `scripts/performance_evidence.py` 只做本地、无网络、无写入目标源码的证据清单和 manifest 校验；它不是 profiler、压测器或性能结论引擎。

## 结论规则

- **confirmed**：相同/可比负载下重复观察到影响，并有至少一条原因证据（plan、profile、trace、queue/GC/IO 等）。
- **plausible**：静态信号和部分运行数据吻合，但缺少对照、分布或原因证据。
- **unverified**：只有代码模式、计划或工具不可用；只给下一步验证，不给优化批准。
- **regressed**：结果恶化且差异超过预先定义的阈值；报告阈值来源，不能事后挑阈值。

## 参考

- [references/evidence-methods.md](references/evidence-methods.md)：USE、RED、OTel、重试和 Web/服务指标。
- [references/evidence-contract.md](references/evidence-contract.md)：证据状态、字段和报告边界。
