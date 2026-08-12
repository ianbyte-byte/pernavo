# 隐藏性能问题：公开一手资料研究

> 研究日期：2026-08-12（Asia/Shanghai）
>
> 目的：把普通代码审查容易遗漏的性能风险转成可路由、可测量、可复核的 Skills 规则。

## 结论

1. **方法先于指标。** USE 要求按资源检查 utilization、saturation、errors；Google SRE 的四类信号是 latency、traffic、errors、saturation。只看 CPU 或平均耗时会漏掉排队、失败和尾延迟。
2. **性能结论必须带上下文。** workload、数据量、并发、缓存状态、目标环境、时间窗、样本分布和 revision 缺一不可；公开 benchmark 不能替代本项目数据和网络条件。
3. **静态发现只是候选。** N+1、无界物化、同步阻塞、重试放大、长任务和高基数标签都能从代码中发现，但是否成为瓶颈要靠 query plan、trace、counter、profile 或对照基准验证。
4. **要和问题匹配工具。** CPU profile 不能单独证明 allocation、锁或 I/O 根因；JMH 需要 warmup、measurement、fork、结果消费和误差；数据库需要实际执行计划与运行统计；Web 需要 LCP/INP/CLS 的 field/lab 分布。
5. **尾延迟和重试会互相放大。** 记录 p50/p95/p99、原始请求与 retry attempt、各层 deadline/backoff/jitter，并检查多层 retry 的乘法效果。

## 公开来源与 Skill 映射

| 来源 | 可执行规则 | 采用位置 |
|---|---|---|
| [Gregg USE Method](https://www.brendangregg.com/usemethod.html) | 每个资源记录利用率、饱和度、错误及时间窗/维度 | `performance-measurement` |
| [Gregg Methodology](https://www.brendangregg.com/methodology.html) | 先定义问题/负载，再选 USE、CPU profile、off-CPU 或 benchmark；避免指标 fishing | `performance-review`, `performance-measurement` |
| [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/) | 关联 traces、metrics、logs；保留 trace 时间和上下文 | `performance-measurement` |
| [OpenTelemetry metrics data model](https://opentelemetry.io/docs/specs/otel/metrics/data-model/) | 延迟保留 histogram/分位数，限制高基数属性，保存 query/window/aggregation | `performance-measurement` |
| [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/) | 使用稳定的服务、路由、状态、数据库维度，避免完整 URL/ID 聚合 | `performance-review`, `runtime-performance` |
| [Google SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/) | 用 latency/traffic/errors/saturation 解释用户影响和容量风险 | `performance-measurement` |
| [AWS Builders' Library](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/) | 记录 deadline、attempt、backoff、jitter；检查多层 retry 放大 | `performance-review`, `performance-measurement` |
| [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) | 对代表 workload 比较 estimated/actual rows、buffers、WAL、设置和节点耗时 | `database-performance` |
| [PostgreSQL monitoring](https://www.postgresql.org/docs/current/monitoring-stats.html) | 结合 `pg_stat_statements`、活动、等待和阻塞 | `database-performance` |
| [MySQL optimization](https://dev.mysql.com/doc/refman/8.4/en/optimization.html) | 检查实际计划、扫描、temporary/filesort、digest 和慢查询 | `database-performance` |
| [.NET counters/trace](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters) / [trace](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace) | 先 counters，再按需 trace；关联 CPU、分配、GC、线程池和异常 | `runtime-performance` |
| [ASP.NET performance practices](https://learn.microsoft.com/en-us/aspnet/core/performance/performance-best-practices) | 避免同步阻塞/IO、过度缓冲；使用取消、分页、流式传输和有界并发 | `runtime-performance` |
| [EF Core performance](https://learn.microsoft.com/en-us/ef/core/performance/) | 检查 SQL、round trips、N+1、投影、跟踪和真实数据量 | `database-performance` |
| [JMH](https://github.com/openjdk/jmh#how-to-run) | warmup、measurement、fork、结果消费、分布/误差和 setup 分离 | `benchmark-performance` |
| [async-profiler](https://github.com/async-profiler/async-profiler#usage) | 按假设选择 CPU/allocation/lock/wall 事件，不以单张 CPU 图证明根因 | `runtime-performance` |
| [MDN Performance](https://developer.mozilla.org/en-US/docs/Web/Performance) / [Long Tasks](https://developer.mozilla.org/en-US/docs/Web/API/Long_Tasks_API) | 拆 navigation/resource/mark/measure；记录 >50ms 长任务及归因 | `web-performance` |
| [web.dev Web Vitals](https://web.dev/articles/vitals) / [LCP](https://web.dev/articles/lcp) / [CLS](https://web.dev/articles/cls) | field/lab 分开；记录 LCP、INP、CLS p75；LCP 拆 TTFB/发现/下载/渲染，CLS 覆盖整个生命周期 | `web-performance` |

## 证据边界

这些来源支持的是方法、工具使用和应记录的信号，不支持“某种模式必然慢”或“本仓库已观察到瓶颈”。本套 Skills 因此把结果分为 `confirmed`、`plausible`、`unverified` 和 `regressed`，并要求把命令、环境、时间窗及 artifact 指针写入证据。不存在授权目标或工具时只能输出静态假设和下一步验证。
