---
name: runtime-performance
description: >
  Review or diagnose application runtime costs: CPU hot paths, allocation and GC pressure, thread
  pool starvation, blocking, lock contention, queues, connection pools, serialization, I/O, and
  profiler evidence. Use for runtime performance, CPU/memory profiling, GC, thread pool, async
  blocking, allocation hotspot, contention, or .NET/JVM latency. Match the profiler event to the
  hypothesis and keep static, counter, trace, and profile evidence separate.
---

# Runtime Performance

## 静态信号

- 找热路径中的重复分配、复制、装箱、字符串/JSON 转换、正则、集合扩容和大对象；确认它们是否随 N/payload 放大。
- 找同步等待、同步文件/网络 I/O、长锁、无界队列、无限重试和过大的并发；区分 CPU 使用和等待占用。
- 检查缓存容量、eviction、生命周期和高基数 key；命中率不等于低延迟，填充和失效也需测量。
- 检查日志级别、异常作为控制流、重复序列化和诊断开销是否只在高负载出现。

## .NET 证据

- 低侵入先用 `dotnet-counters monitor --process-id <PID>`：CPU、alloc-rate、GC 次数/耗时、线程池队列/线程、异常率；记录 runtime/SDK 和窗口。
- 需要调用栈和事件顺序再用 `dotnet-trace collect --process-id <PID> --duration ...`；报告 trace 文件 hash/大小和分析工具，不要只贴截图。
- ASP.NET Core 请求路径避免 `.Result`/`.Wait()` 和同步 I/O；检查响应缓冲、分页/流式传输、取消令牌、下游并发和中间件重复读取。

## JVM 证据

- async-profiler 按假设选择 CPU、allocation、lock 或 wall-clock/底层采样；一张 CPU 火焰图不能证明锁、内存或 I/O 根因。
- 对同一 workload 记录采样时长、JDK、容器 CPU quota、事件、线程状态和 artifact；检查 native/阻塞/非 safepoint 栈是否被漏掉。

## 输出

分开列出 `CPU / allocation / GC / lock-wait / I/O / queue` 证据；如果只具备一个面，结论最多为 plausible。不要因 CPU 高直接归因于业务方法，先排除 GC/JIT/锁/线程池。

## 来源

- .NET counters: https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-counters
- .NET trace: https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace
- ASP.NET performance: https://learn.microsoft.com/en-us/aspnet/core/performance/performance-best-practices
- async-profiler: https://github.com/async-profiler/async-profiler
- OpenTelemetry JVM attributes: https://opentelemetry.io/docs/specs/semconv/registry/attributes/jvm/
