---
name: test-engineering
description: >
  Design, execute, or assess software tests across unit, integration, API, functional, system,
  regression, acceptance, and release-smoke levels, while choosing white-box, gray-box, or black-box
  evidence. Use when asked to write, run, plan, or review tests, test strategy, coverage, integration
  tests, API contracts, regression, UAT, smoke tests, or black/white/gray-box testing. Route database
  execution to data-work, performance evidence to performance-work, Web UI QA to qa or qa-only,
  security assessment to `codex-security:*`, and report formatting to report-writer.
---

# Test Engineering

Use one testing entry point to choose the test level, observation method, execution scope, and
evidence needed for the risk. Test levels describe **what** is under test; white-box, gray-box, and
black-box describe **how** the behavior is observed. A task can use more than one level or method.

## Route

Select the narrowest level that can falsify the suspected failure, then widen only when the result
or risk requires it:

- `unit`: one public function, class, service, rule, or state transition; prefer fast isolated tests
  with independent expected values.
- `integration`: two or more modules or a real dependency boundary such as API plus database,
  cache, queue, filesystem, or authorized third-party sandbox.
- `api`: request, response, protocol, validation, authorization, idempotency, error contract, and
  observable side effects at an endpoint or service boundary.
- `functional/system`: a user or business workflow across components and services; include normal,
  failure, recovery, and state-transition paths.
- `regression`: a focused suite proving a change did not break known behavior; select cases from the
  changed seams and prior failures rather than rerunning an unexplained large suite.
- `acceptance/release-smoke`: business acceptance or post-release checks against an authorized
  environment; keep production mutation and approval outside this Skill's authority.

Choose the observation method explicitly:

- `white-box`: source-aware branch, condition, exception, state, coverage, mutation, or architecture
  checks. Do not confuse a coverage percentage with behavior quality.
- `gray-box`: use selected internal facts such as schema, logs, events, query shape, or dependency
  boundaries while asserting externally meaningful behavior.
- `black-box`: use requirements-level inputs, outputs, roles, workflows, and externally visible side
  effects without relying on implementation details.

## Workflow

1. Record the revision, target environment, changed seam, risk, authority, and available test runner.
   Inspect repository scripts and fixtures before choosing a framework or inventing a command.
2. Build a case matrix covering applicable success, validation, boundary, authentication,
   authorization, not-found/conflict, state transition, idempotency, dependency failure, limits,
   side effects, cleanup, and recovery cases. Mark every non-executed case `blocked`, `skipped`, or
   `not-applicable` with a reason.
3. Pick the smallest public seam and independent oracle. For white-box tests, cover meaningful
   branches and failure paths; for gray-box tests, verify the selected internal evidence plus the
   public result; for black-box tests, derive assertions from requirements or a trusted contract.
4. Run in an evidence ladder: unit, integration/API, functional/system, regression, then authorized
   acceptance or release smoke. Stop expansion after a failed gate until the failure is understood.
5. Preserve command, exit status, revision, environment class, fixture identity, timing, result per
   case, artifact paths, cleanup state, and evidence limits. Keep credentials and regulated data out
   of logs.
6. Hand off specialized work without absorbing its authority: `data-work` for configured test
   databases and SQL evidence, `performance-work` for workload and percentile proof, `qa` or
   `qa-only` for browser interaction, `codex-security:*` for security testing, and `report-writer`
   for formal presentation.

## Boundaries

- Use non-production or disposable targets by default. Require explicit authorization and a cleanup
  plan for writes, destructive cases, fault injection, concurrency, or rate-limit tests.
- A passing local test does not prove deployment or production behavior. A coverage number, snapshot,
  mock expectation, or single benchmark does not by itself prove quality or a regression decision.
- Keep test execution separate from implementation and diff review. Route code changes to
  `engineering-workflow` and review-only requests to `change-review`. Verification does not re-open the review loop,
  does not authorize the verifier to edit the writer's tree, and does not self-select P2 or P3.

## API completion gate

Before HTTP or business API tests, write `.pernavo/api-test-matrix.json` with `required_cases`. Do
not claim those tests complete unless `scripts/grade_api_jsonl.py` exits 0. Default install merges a
host Stop hook that runs `scripts/api_test_stop_hook.py`; see
[the API test gate](references/api-test-gate.md).

## Output

```text
Testing scope and authority:
Test levels and observation methods:
Case matrix and expected behavior:
Commands, revision, target class, and results:
Evidence artifacts and cleanup:
Blocked, skipped, and unverified surfaces:
Next gate or handoff:
```

For detailed case categories and stack adapter selection, read
[the test matrix](references/test-matrix.md). For HTTP request/response evidence, read
[`report-writer`'s API test module](../report-writer/references/http-api-test.md). For the JSONL
completion gate, read [the API test gate](references/api-test-gate.md).
