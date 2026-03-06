---
name: lcc-sql-optimize
description: SQL optimization workflow based on MySQL index principles (美团技术团队). Analyze slow queries, design proper indexes, and optimize SQL statements.
disable-model-invocation: true
---

Run a SQL optimization workflow based on MySQL index principles.

Reference: https://tech.meituan.com/2014/06/30/mysql-index.html

## Steps

1) Analyze (lcc-sql-optimizer)
- Use `lcc-sql-optimizer` to analyze the slow query(ies)
- Check: query pattern, table schema, existing indexes, execution plan
- Identify bottlenecks: full table scans, missing indexes, improper index order

2) Design & Implement (lcc-sql-optimizer)
- Design proper indexes based on leftmost prefix principle
- Optimize SQL statements: avoid SELECT *, use appropriate JOINs, etc.
- Provide before/after execution plan comparisons

3) Verify (lcc-tester)
- Run tests to verify correctness
- Validate performance improvements
