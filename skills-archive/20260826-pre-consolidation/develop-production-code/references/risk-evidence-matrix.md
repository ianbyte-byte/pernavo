# Production risk and evidence matrix

Read this reference when classifying a production change, selecting the minimum verification stack, or deciding how much AI-generated code must be read.

## Classify by the highest consequence

Evaluate every factor and choose the highest resulting tier. Do not average risks down.

| Factor | R0 — disposable | R1 — routine | R2 — material | R3 — critical |
|---|---|---|---|---|
| Reach | Isolated sandbox | One bounded component | Multiple users/systems | Safety or enterprise-wide boundary |
| Durable state | None | Reversible local state | Shared/customer/financial state | Irreversible or regulated state |
| Security | No credentials or trust boundary | Existing low-privilege path | Permissions, secrets, authentication, external ingress | Privilege boundary or catastrophic exposure |
| Reversibility | Delete the artifact | Fast rollback with known path | Repair or migration required | Rollback cannot restore the loss |
| Observability | Output directly visible | Existing logs/tests expose failure | Delayed or partial detection | Silent failure or harm before detection |
| Oracle | Direct expected output | Mature contract and regression tests | Ambiguous rules or coupled tests | Formal, safety, legal, or independently governed requirement |

Default R2 examples include money, tax, inventory, invoices, permissions, historical repair, durable migrations, external API writes, scheduled tasks, idempotency, concurrency, state machines, and customer-visible reports. Raise any of them to R3 when failure becomes irreversible, regulated, safety-relevant, or catastrophic.

## Minimum evidence gates

Apply repository- and domain-specific gates when they are stricter.

| Gate | R0 | R1 | R2 | R3 |
|---|---|---|---|---|
| Boundary check | Prove sandbox/no production access | Inspect changed seam | Trace data, state, permissions, and side effects | Formal hazard/assurance boundary |
| Code reading | Inputs, permissions, output sampling | Complete retained diff | All changed production-impacting code | Qualified line-by-line critical review |
| Static checks | Relevant syntax/type check | Build, lint/type/analyzers | Add security/config/dependency checks as relevant | Domain-mandated static evidence |
| Behavior tests | Direct output check | Focused regression plus integration where relevant | Requirement-derived integration and failure-path tests | Independent, traceable assurance suite |
| Correlation break | Optional | Add when oracle is weak | Required independent oracle or reviewer | Independent implementation/verification authority |
| Runtime QA | Exercise disposable tool | Exercise normal entry point | Exercise real scenario in isolated/staging host | Controlled staging, fault scenarios, formal acceptance |
| Release evidence | Not applicable | Record rollback path if released | Rehearse rollback; canary/monitor if released | Explicit authorization, staged release, monitored acceptance |

Release gates describe the evidence required **if release is in scope**. They do not authorize deployment, production writes, or access to sensitive systems.

## Match failure modes to evidence

| Failure mode | Stronger evidence |
|---|---|
| Wrong business meaning | Source-record examples, executable acceptance scenarios, independently calculated results |
| Boundary or contract mismatch | Contract tests against the real parser, database, API, queue, or file format |
| Concurrency or allocation race | Atomicity inspection, stress/interleaving tests, real database transaction behavior |
| Security or permission error | Threat model, least-privilege inspection, negative authorization tests, SAST/DAST where relevant |
| Migration or repair damage | Read-only profiling, representative copy, rollback/forward-repair rehearsal, row-count and invariant reconciliation |
| Performance or resource exhaustion | Representative benchmark/load test with explicit baseline and limits |
| Operational invisibility | Structured logs, metrics, traces, alerts, runbook and failure injection |
| Maintainability collapse | Focused review, analyzers, complexity trend, mutation resistance; never one metric alone |

## Test the verification system

Use one or more of these techniques when implementation and tests were generated from the same prompt or model:

1. Seed a known fault and confirm that the suite fails.
2. Mutate operators, conditions, boundaries, or state transitions and measure survivors.
3. Generate cases from an independent source of truth rather than from implementation structure.
4. Compare two implementations that do not share the same algorithm or prompt context.
5. Check properties that must hold for broad input classes, not only remembered examples.
6. Give a fresh reviewer only the requirements, artifact, and acceptance surface.

More generated tests are useful only when they increase failure-detection power. Test count and line coverage are not substitutes for an independent oracle.
