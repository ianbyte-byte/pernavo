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

## Stack adapter guidance

Testing is language- and framework-agnostic. Inspect the repository's language(s), build system,
test runner, fixtures, dependency services, and existing CI before selecting commands or tools. Use
the native ecosystem and preserve its lifecycle, isolation, reporting, and conventions; do not add a
framework only to satisfy a metric.

Examples are adapters, not requirements:

- a repository-native unit framework and assertion library for the implementation language;
- an in-process harness or service test host for application boundaries;
- disposable containers, emulators, or explicitly configured test services for real dependencies;
- coverage, mutation, property-based, or fuzz tooling when the repository already supports it;
- the repository's approved browser runner for black-box UI workflows;
- an approved HTTP/RPC client or contract fixture for API tests.

For example, a .NET repository might use xUnit, NUnit, or MSTest; ASP.NET Core
`WebApplicationFactory`; and Coverlet or Stryker.NET. A Python repository might use pytest and
pytest fixtures, while a JavaScript/TypeScript repository might use Vitest or Jest with Playwright.
These names illustrate adapter selection only; inspect the repository before choosing among them.

When a concrete example is useful, name the language-specific tool and why it fits the repository;
never infer a language, framework, or dependency from this reference alone.

## Evidence minimum

Every executed case should identify the test level, method, case ID, precondition, fixture, expected
assertions, actual result, command, exit status, revision, target class, and artifact or log path.
Every non-executed case needs a state and reason. Coverage and mutation numbers are supplemental;
the report must state what behavior they do and do not establish.
