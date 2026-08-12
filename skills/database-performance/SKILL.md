---
name: database-performance
description: >
  Audit database and ORM performance risks such as N+1 queries, bad query shape, missing or unused
  indexes, cardinality misestimates, full scans, unstable pagination, over-fetching, client-side
  evaluation, lock waits, and excessive round trips. Use for SQL performance review, slow query,
  EXPLAIN, EF Core performance, query plan, database bottleneck, or ORM latency. Require actual
  execution evidence where possible; do not infer a fix from an index or estimated plan alone.
---

# Database Performance

## 静态审查

- 追踪一次请求/作业的 SQL 次数、循环位置、懒加载和重复参数；优先找 N+1 与串行往返。
- 检查过滤/排序/分页是否在数据库端完成，是否有稳定排序和上界；检查投影是否只取需要的列。
- 检查函数包裹索引列、隐式类型转换、低选择性索引、`SELECT *`、无界 `IN`、大 `Include` 和客户端求值。
- 追踪事务和锁边界：长事务、锁顺序、批量大小、隔离级别、连接池等待、读写混合。
- 以数据分布和选择性理解索引，不以“加索引”作为默认修复；写入成本、缓存、统计信息和维护都要计入。

## 运行验证

- PostgreSQL：对安全的代表性 workload 使用 `EXPLAIN (ANALYZE, BUFFERS, WAL, SETTINGS)`；比较 estimated/actual rows，关注 shared read、临时磁盘、排序/哈希溢出和嵌套循环放大。结合 `pg_stat_statements`、`pg_stat_activity` 的耗时、等待和阻塞。
- MySQL：使用 `EXPLAIN ANALYZE`（版本支持时）和 Performance Schema statement digest；检查实际行数、key、过滤、temporary/filesort、扫描行和慢查询日志。
- EF Core：记录生成 SQL、单请求 SQL 次数与数据库总耗时；对只读查询评估 `AsNoTracking()`，但用实测确认；不要把公开 benchmark 当本项目结论。

## 输出

每个 finding 写 `path:line → query shape → amplification → plan/runtime evidence → smallest safe experiment`。实验必须有回滚/对照，不能在生产无授权地运行 `ANALYZE` 或改变索引。

## 来源

- PostgreSQL EXPLAIN: https://www.postgresql.org/docs/current/using-explain.html
- PostgreSQL monitoring: https://www.postgresql.org/docs/current/monitoring-stats.html
- MySQL optimization: https://dev.mysql.com/doc/refman/8.4/en/optimization.html
- MySQL EXPLAIN: https://dev.mysql.com/doc/refman/8.4/en/using-explain.html
- EF Core performance: https://learn.microsoft.com/en-us/ef/core/performance/
- EF Core efficient querying: https://learn.microsoft.com/en-us/ef/core/performance/efficient-querying
