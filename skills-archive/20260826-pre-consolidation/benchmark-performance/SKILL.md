---
name: benchmark-performance
description: >
  Create, review, or interpret a reliable performance benchmark. Use for benchmark design, JMH,
  BenchmarkDotNet, warmup, forks, variance, microbenchmark, regression threshold, or comparing
  implementations. Require representative workload, setup separation, result consumption, repeatable
  environment, distribution, and allocation/GC context. Do not trust a single run or public benchmark
  that does not match the target workload.
---

# Benchmark Performance

## 必查项

- workload：固定输入规模、数据分布、payload、并发/吞吐和真实依赖；记录冷/热状态。
- setup：把 fixture/对象构造/数据库填充与 steady-state 操作分开；除非端到端问题，否则不要在被测方法里生成大输入。
- JVM/JMH：有 warmup、measurement iterations、多个 fork、JDK/VM 参数；计算结果要返回或交给 `Blackhole`，防止编译器消除。
- 统计：不要只报告平均值；至少保存 count、p50/p95/p99 或样本/误差，关注 GC、分配和 outlier。
- 运行环境：CPU quota、频率/容器限制、OS、runtime/JIT、依赖版本和并行噪声；比较前确认相同。
- 回归：预先定义阈值、方向和样本量；对照基线，解释 variance，避免为了过线反复挑样本。

## 结果边界

微基准不能证明端到端、网络、数据库或生产容量；公开 benchmark 不能替代本项目数据量、网络延迟和部署环境。无法复现时输出 `unverified` 和缺口。

## 来源

- OpenJDK JMH README: https://github.com/openjdk/jmh#how-to-run
- JMH samples: https://github.com/openjdk/jmh/tree/master/jmh-samples
- async-profiler: https://github.com/async-profiler/async-profiler#usage
- EF Core benchmark caution: https://learn.microsoft.com/en-us/ef/core/performance/
