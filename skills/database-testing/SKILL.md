---
name: database-testing
description: >
  Connect to an explicitly configured SQLite, PostgreSQL, MySQL, or Microsoft SQL Server test database to inspect schema,
  run bounded SQL checks, create test scripts, and validate application data behavior. Use when an AI
  needs to connect to a test database, write or run a SQL validation script, query a configured
  database, seed or clean test data, or reproduce a data issue. Default to read-only execution;
  require explicit write gates and never target production.
---

# Database Testing

Use `scripts/database_runner.py` for database access. It accepts a URL supplied directly or by an
environment-variable name; prefer the latter so credentials never enter a shell history, a source
file, or tool output.

## Workflow

1. Locate the application's documented test connection and confirm its database, tenant, and data
   ownership. Do not guess a URL, reuse a production credential, or scan secret stores.
2. Run `preflight` before connecting. It redacts the target and refuses likely production targets.
3. Inspect schema and execute the smallest read-only query that tests the claim. Save reusable SQL
   in the repository's existing test or tooling location, not in this Skill directory.
4. For a write test, use disposable or transaction-isolated test data. Require both `--allow-write`
   and `DATABASE_TESTING_ALLOW_WRITE=1`; state the setup and cleanup SQL before execution.
5. Report the target class, SQL file or query purpose, result summary, cleanup state, and what was
   not verified. Never print a connection URL, password, token, or result columns that contain
   secrets or unnecessary personal data.

## Runner

Set a test-only connection in the current process:

```bash
export APP_TEST_DATABASE_URL='postgresql://test_user:password@127.0.0.1:5432/app_test'
python3 skills/database-testing/scripts/database_runner.py preflight --url-env APP_TEST_DATABASE_URL
python3 skills/database-testing/scripts/database_runner.py run --url-env APP_TEST_DATABASE_URL --file tests/sql/account-count.sql
```

For a local SQLite database, use an absolute URL and a read query:

```bash
python3 skills/database-testing/scripts/database_runner.py run \
  --url 'sqlite:////absolute/path/to/app-test.db' \
  --sql 'SELECT count(*) AS account_count FROM accounts'
```

The runner supports `sqlite`, `postgresql`/`postgres`, `mysql`, and `mssql`/`sqlserver` URLs.
PostgreSQL requires a locally installed `psql`; MySQL requires `mysql`; SQL Server requires
`sqlcmd`. It has no network or driver dependency of its own. It sets a maximum timeout and emits a
structured result without echoing credentials.

For SQL Server, supply the database in the URL path and use the TCP port when needed:

```bash
export APP_TEST_DATABASE_URL='mssql://test_user:password@127.0.0.1:1433/app_test'
python3 skills/database-testing/scripts/database_runner.py preflight --url-env APP_TEST_DATABASE_URL
python3 skills/database-testing/scripts/database_runner.py run --url-env APP_TEST_DATABASE_URL --sql 'SELECT TOP (10) id FROM dbo.accounts ORDER BY id'
```

## Write Tests

Use explicit setup and cleanup files. Do not use destructive DDL, broad deletes, or unbounded
updates unless the user has specifically authorized them for the identified disposable target.

```bash
DATABASE_TESTING_ALLOW_WRITE=1 \
python3 skills/database-testing/scripts/database_runner.py run \
  --url-env APP_TEST_DATABASE_URL \
  --file tests/sql/seed-test-account.sql \
  --mode write --allow-write
```

The runner rejects a target whose host or database name looks like production. That is a guardrail,
not proof of safety: confirm the target yourself. It intentionally has no bypass flag.

## SQL Guidance

- Use parameterized queries in application scripts; use deterministic literal fixtures only in isolated SQL test files.
- Start with a narrow projection, `LIMIT`, and an exact tenant/test-fixture predicate.
- Make cleanup idempotent and scoped to a unique test prefix or generated identifier.
- Inspect table/column names before writing mutations. For PostgreSQL use `information_schema` or `\d`; for MySQL use `information_schema`; for SQL Server use `sys.tables`, `sys.columns`, or `INFORMATION_SCHEMA`; for SQLite query `sqlite_master` and `PRAGMA table_info`.
- Treat data returned by a test database as potentially sensitive. Aggregate or redact it in the final report.

## Failure Handling

Stop on connection, authentication, target-identification, or SQL errors. Do not retry writes automatically. If a write fails after partial execution, inspect the transaction/cleanup state and report it before attempting any remediation.
