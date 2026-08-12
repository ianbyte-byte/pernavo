---
name: performance-review
description: >
  Review a code change or code path for hidden performance risks that ordinary correctness review
  can miss, including hot loops, allocations, query shape, I/O, contention, retries, caching,
  serialization, tail latency, and missing observability. Use for 性能审查, 性能问题排查,
  performance review, slow path review, latency regression, or performance blind spots. Start with
  static signals, then route to performance-measurement and the applicable database-performance,
  runtime-performance, web-performance, or benchmark-performance overlay. Do not claim a bottleneck
  from a pattern alone, implement optimizations without authorization, or replace runtime evidence
  with a green build or average latency.
---

# Performance Review

审查的目标是发现“代码看起来正确，但在真实负载下会变慢、放大资源消耗或扩大尾延迟”的风险。
本 Skill 负责发现、分级和路由；它不负责修改代码，也不把静态命中当作已证实的瓶颈。

## 入口流程

1. 固定目标：代码差异/路径、请求或作业、负载规模、SLO/基线、目标环境和不在范围内的表面。
2. 先读调用图和数据流，再看模式。标记循环、集合物化、序列化、外部调用、数据库访问、锁/队列、缓存和重试边界。
3. 按下面的信号表列出疑似风险，保存文件与行号、触发条件、潜在放大因子和最小验证。
4. 路由窄域 Skill；请求“证明/排查/回归”时调用 `performance-measurement`，不要直接下结论。
5. 输出每个 finding 的 `静态信号 → 影响假设 → 需要的证据 → 建议动作`。

## 优先检查的隐藏成本

| 信号 | 常见放大方式 | 最小验证/路由 |
|---|---|---|
| 循环内查询、懒加载、重复远程调用 | N+1、网络往返 × 数据量 | `database-performance`；记录请求内调用次数和总下游耗时 |
| 全量 `ToList`/反序列化/实体图、无界分页 | 内存峰值、GC、响应体和尾延迟随数据增长 | `database-performance` + `runtime-performance`；阶梯负载 |
| 热循环中的 LINQ/临时集合/字符串拼接/正则 | 分配、复制和 CPU 随 N 或字符串长度增长 | `runtime-performance`；allocation/CPU profile |
| `.Result`、`.Wait()`、同步 I/O、串行下游调用 | 线程池饥饿、连接占用、排队 | `runtime-performance`；线程池、队列、trace |
| 锁、全局缓存、单飞失败、共享连接池 | contention、惊群、容量耗尽 | `runtime-performance`；wall/lock/off-CPU profile |
| 无截止时间、无界并发、多层重试、无 jitter | 重试乘法、级联故障、p99 放大 | `performance-measurement`；分离原始请求和 retry 请求 |
| 缓存无容量/TTL/失效策略或 key 高基数 | 命中率低、内存增长、脏读、穿透 | `performance-measurement`；命中率、eviction、大小和一致性 |
| 大 JSON/映射/压缩/日志、重复序列化 | CPU、分配、I/O 和 payload 放大 | `runtime-performance`；按 payload size 分层 |
| 只看平均值、单实例、单次 benchmark | 长尾、热点分片、冷启动和 GC 被隐藏 | `performance-measurement` + `benchmark-performance` |
| Web 只看 load/TTFB/Lighthouse | 主线程长任务、交互延迟、布局偏移漏检 | `web-performance` |

## 分级

- **P1**：已有同负载对比或生产证据显示 SLO/容量受到影响，或明显存在无界放大/资源耗尽路径。
- **P2**：静态信号可信且影响会随输入、并发或下游延迟放大，但还缺关键运行证据。
- **P3**：优化机会或观测缺口，影响依赖场景，不能作为必须修复的瓶颈。

不要因为“复杂度高”“用了循环”就报 P1。必须写出放大变量（N、并发、payload、往返次数、重试层数、锁持有时间等）。

## 证据门槛

性能结论至少要能回答：workload 是什么、何时测、在哪里测、样本量多少、p50/p95/p99 如何变化、资源和错误是否变化、是否存在冷/热状态差异。优先使用 [performance-measurement](../performance-measurement/SKILL.md) 生成 manifest；静态审查可先给“待验证”。

使用 [references/hidden-costs.md](references/hidden-costs.md) 选择语言/框架模式，使用 [references/evidence-contract.md](references/evidence-contract.md) 写结果。需要正式报告时交给 [report-writer](../report-writer/SKILL.md)；需要审查 Git diff 时与 [review-mr](../review-mr/SKILL.md) 组合，保持性能 findings 和行为 QA 分开。

## 输出格式

```markdown
## Performance Review
- Scope / revision / target: ...
- Evidence state: static-only | partial | runtime-observed
- Workload: ...

### Findings
1. [P1/P2/P3] `path:line` — signal and amplification variable
   - Impact hypothesis: ...
   - Required evidence: ...
   - Smallest safe action: ...

### Coverage and limits
- Checked: ...
- Routed overlays: ...
- Not observed / unavailable: ...
```

禁止把“建议使用 profiler/压测”写成“已发现瓶颈”。如果没有可运行目标，明确 `static-only`，不要伪造 runtime evidence。
