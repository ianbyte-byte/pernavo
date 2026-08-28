# Test Matrix

Use this reference after `test-engineering` selects a level or method. Keep the matrix proportional
to the risk and record explicit states for cases that cannot safely run.

## Level and method mapping

| Level | Typical seam | Primary method | Useful secondary method |
|---|---|---|---|
| Unit | public function, class, rule, state transition | white-box | black-box contract examples |
| Integration | service plus database/cache/queue/filesystem | gray-box | black-box boundary assertions |
| API/contract | HTTP or RPC boundary | black-box | gray-box schema, events, logs |
| Functional/system | business workflow across components | black-box | gray-box traces and state checks |
| Regression | changed seam and prior failure | whichever falsifies the risk | combine methods for high-loss paths |
| Acceptance/UAT | business scenario and outcome | black-box | gray-box reconciliation evidence |
| Release smoke | authorized live-like critical path | black-box | gray-box health and audit checks |

## Case categories

Select the categories required by the contract and risk model:

- happy path and alternate valid representations;
- missing, null, malformed, out-of-range, duplicate, and unknown values;
- authentication, authorization, tenant or ownership boundaries;
- not-found, conflict, stale version, invalid transition, retry, and idempotency;
- dependency timeout, partial failure, unavailable service, rollback, and recovery;
- persistence, emitted event, cache invalidation, audit trail, and cleanup;
- pagination, ordering, empty result, payload/batch limits, and safe concurrency;
- business invariants and reconciliation, such as totals, tax, inventory, and ledger consistency.

## .NET selection guidance

Inspect the solution and existing CI before selecting tools. Common choices are examples, not
mandatory dependencies:

- xUnit, NUnit, or MSTest for unit and repository-native test projects;
- ASP.NET Core `WebApplicationFactory` for in-process integration boundaries;
- a disposable container or explicitly configured test service for database and dependency tests;
- Coverlet for coverage evidence and Stryker.NET for mutation evidence when the repository already
  supports them;
- Playwright or the repository's browser runner for black-box UI workflows;
- a repository-approved client or contract fixture for HTTP/API tests.

Do not add a framework only to satisfy a metric. Preserve the repository's runner, fixture lifecycle,
target isolation, and CI conventions.

## Evidence minimum

Every executed case should identify the test level, method, case ID, precondition, fixture, expected
assertions, actual result, command, exit status, revision, target class, and artifact or log path.
Every non-executed case needs a state and reason. Coverage and mutation numbers are supplemental;
the report must state what behavior they do and do not establish.
