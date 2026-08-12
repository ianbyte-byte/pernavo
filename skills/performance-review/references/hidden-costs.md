# Hidden performance costs

这份表用于静态审查生成候选，不代替实测。

## 通用

- 找输入规模、并发、payload、往返次数、重试层数、锁持有时间和缓存 key cardinality；每个 finding 至少绑定一个放大变量。
- 检查是否把 setup、冷启动、编译、缓存填充和 steady state 混在一起。
- 检查是否只报平均值；尾延迟、失败请求、拒绝和排队可能在均值正常时已经恶化。
- 检查日志、指标和 trace 是否产生无界高基数标签（完整 URL、用户 ID、request ID）或重复序列化。

## 访问与数据

- 循环里的 query/HTTP/文件调用通常是 N+1 或串行往返；确认是否能批量化、并行化或缓存，但先检查顺序、限流和一致性。
- `SELECT *`、全实体图、无界 `Include`、无稳定排序分页、客户端过滤/聚合会把数据量成本推到应用端。
- JSON/DTO 映射和压缩可能同时消耗 CPU、分配和网络；按 payload size 分层测量。

## 并发与可靠性

- `.Result`/`.Wait()`、同步 I/O 和长锁持有会把等待转换成线程/连接池占用。
- 无 deadline、无界 semaphore/channel、无容量缓存会让压力转为排队或 OOM。
- 多层 retry、固定 backoff、无 jitter 和不区分可重试错误会放大流量；记录每一层 attempt。

## 来源

- Brendan Gregg, USE Method: https://www.brendangregg.com/usemethod.html
- Brendan Gregg, Methodology: https://www.brendangregg.com/methodology.html
- AWS Builders' Library, timeouts/retries/backoff/jitter: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
- OpenTelemetry semantic conventions: https://opentelemetry.io/docs/specs/semconv/
