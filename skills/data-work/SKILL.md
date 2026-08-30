---
name: data-work
description: >
  Safely inspect and validate SQL, ORM queries, schemas, execution plans, round trips, locks, and
  test-database data. Use for database debugging, report data checks, SQL scripts, N+1 or query
  performance review, and bounded test-data setup. Resolve an explicitly configured non-production
  target first; default to read-only and require explicit write gates.
---

# Data Work

This is the single database entry point. Separate query-shape review from database execution.

## Route

- **Static query/ORM review:** inspect generated SQL, cardinality, pagination, N+1 shape, plans,
  locks, indexes, and round-trip amplification without connecting to a database. Label evidence
  `static-only` or `estimated-plan`.
- **Test-database validation:** resolve the documented test target, run `preflight`, then the
  narrowest read-only query. Use the repository database runner when available.
- **Write test:** use disposable or transaction-isolated data and require both the tool's write
  flag and the repository write environment gate. State setup and cleanup before execution.

## Guardrails

Never guess a URL, reuse production credentials, scan secret stores, print credentials or sensitive
rows, or retry a failed write automatically. Stop when target, tenant, schema, authentication, or
cleanup state is unknown. Estimated plans and source patterns are not actual runtime evidence.

## Evidence

Report target class, revision, SQL or request shape, query count/round trips, plan source, lock or
cardinality evidence, result summary, cleanup state, and unverified surfaces. Route a confirmed
performance question to `performance-work`; route implementation to `engineering-workflow`. Do not
implement code or schema changes from a static review, and do not silently edit.
