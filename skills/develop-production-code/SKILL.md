---
name: develop-production-code
description: >
  Implement or harden retained code intended for a real production system with risk-tiered
  AI-code review, independent oracles, runtime QA, rollback awareness, and proof boundaries.
  Use for production features, fixes, refactors, 原型转生产, AI-generated changes being prepared
  for merge or 上线, and implementation evidence needed for release or readiness claims. Exclude
  read-only analysis or policy discussion, disposable prototypes, trivial edits, MR/PR-only
  review, general SLO design, workflow selection, and agent topology.
---

# Develop Production Code

Use risk, retained ownership, and strength of evidence to decide how AI-assisted code may enter a production system. Do not choose between “read every generated line” and “trust the tests” as universal policies. Understand the system invariants, review retained code in proportion to its consequences, and make independent evidence carry the rest.

## Preserve the ownership contract

- Keep the accountable engineer responsible for requirements, design boundaries, failure behavior, verification, and release evidence. Delegating implementation does not delegate ownership.
- Understand the changed seam, its inputs, state transitions, side effects, dependencies, and rollback path before accepting generated code.
- Treat tests, coverage, complexity limits, linters, and deterministic checkers as evidence, not proof that the requirement or oracle is correct.
- Keep retained production code small and maintainable. Generate abundant disposable tests, probes, simulators, and alternative implementations outside the shipped artifact when they increase confidence.
- Separate implementation confidence from deployment confidence. Never turn a green build, isolated test, or staging run into a production-verified claim.

## Compose with specialized skills

Use this skill as the production implementation and evidence policy, not as a replacement for existing specialists:

1. Let `coding-task-controller` and `unknowns-field-guide` establish the real seam, unknowns, risk path, do-not-do scope, and implementation plan.
2. Use this skill to classify artifacts, choose the code-reading policy, implement the smallest correct change, and assemble evidence.
3. Route reliability architecture, SLOs, resilience, and systemic test strategy to `aviation-grade-engineering` when they are material.
4. Route multi-agent topology to `graph-engineering` only when independent contexts, permissions, or author-verifier separation justify it.
5. Route MR/PR review mechanics to `review-mr`. Do not create a duplicate review process here.

If another domain or repository policy is stricter, follow it.

## Execute the production coding loop

### 1. Establish the change contract

Inspect the actual repository, active runtime path, tests, configuration, data boundaries, and relevant source records. Record:

- observable user or operator outcome;
- changed seam and intended file/module scope;
- invariants that must remain true;
- data, money, permissions, external calls, timing, or state transitions involved;
- failure consequences, reversibility, and blast radius;
- explicit do-not-do scope;
- evidence required for the requested completion state.

Do not implement while a locally unresolvable decision can materially change behavior or data safety. Ask only for that narrow decision.

### 2. Classify every generated artifact

Assign each artifact one class:

| Artifact class | Examples | Default treatment |
|---|---|---|
| Retained production | Application code, migrations, configuration, infrastructure, shipped scripts | Maintain, review, test, and own for its lifetime |
| Retained verification | Committed tests, fixtures, analyzers, CI rules | Review its oracle and maintenance cost; test the checker where practical |
| Disposable verification | One-off probes, fuzz harnesses, differential implementations, generated edge cases | Sandbox it, validate outputs, then discard or keep outside the product |
| Generated evidence | Logs, reports, screenshots, benchmark results | Preserve provenance and verify that the observed surface matches the claim |

Never downgrade code merely because an agent generated it. A migration or temporary repair script that can change real data is production-impacting even if it runs once.

### 3. Assign the highest applicable risk tier

Use [references/risk-evidence-matrix.md](references/risk-evidence-matrix.md) to classify the change. Use the highest tier indicated by consequence, reversibility, reach, observability, and oracle strength:

- **R0 — disposable:** cannot reach production systems, secrets, customer data, or durable state.
- **R1 — routine:** contained, observable, reversible production change with a strong existing oracle.
- **R2 — material:** can affect durable data, money, permissions, external contracts, scheduled or concurrent behavior, or many users.
- **R3 — critical:** safety, regulatory, security-boundary, irreversible, or catastrophic failure potential.

Increase the tier when the active runtime is uncertain, rollback is unproven, tests and implementation share the same weak interpretation, or failure is hard to observe.

### 4. Apply the reading policy

Match reading effort to artifact class and risk:

- **R0:** do not require line-by-line review when execution is sandboxed and outputs are directly checked. Inspect permissions, inputs, and side-effect boundaries first.
- **R1:** inspect the complete retained diff, contracts, error paths, and unfamiliar generated constructs. Confirm that tests exercise the changed behavior.
- **R2:** read all changed production-impacting code and sensitive verification/configuration. Trace data and state transitions end to end. Require a fresh reviewer or independent validation lane for the critical invariants.
- **R3:** require qualified human review of every changed critical line, independently derived acceptance oracles, explicit release authority, and the domain's formal assurance process.

Do not spend review effort uniformly across thousands of generated test cases. Review the generator or oracle, sample concrete cases, inject known faults, and check whether the suite detects them.

### 5. Implement the smallest owned change

- Follow repository conventions and the approved plan; preserve unrelated dirty work.
- Generate or edit in reviewable slices. Re-read the final diff rather than trusting the generation transcript.
- Keep product logic explicit. Avoid speculative abstractions, silent fallbacks, compatibility shims for unshipped shapes, and metrics-only quality work.
- Keep irreversible operations, external writes, migrations, and deployment outside implied authority. Obtain authorization when the task does not already include them.
- Prefer cheap verification code around expensive core code: property tests, mutation tests, differential implementations, fuzz inputs, simulators, fault injection, load probes, and purpose-built diagnostics when relevant.

### 6. Build an evidence stack

Derive acceptance checks from requirements, source records, contracts, invariants, or known examples before using the implementation as the oracle. Then collect only the layers relevant to the risk:

1. **Source/static:** final diff, types, lint, analyzers, dependency and configuration inspection.
2. **Isolated behavior:** focused unit, property, mutation, or regression tests.
3. **Integration:** real database semantics, service contracts, migrations, concurrency, permissions, and failure paths in an isolated environment.
4. **Host/runtime:** build and start the actual application or invoke the normal CLI/API entry point.
5. **Manual surface:** perform the changed user or operator scenario and observe the result.
6. **Release:** rehearse rollback, then use staging, canary, health metrics, or production observation only when the user authorized that scope.

Label the highest layer actually observed. Report blocked or unrun layers explicitly. A transaction-rolled-back database check is not deployment proof; a local host smoke test is not production proof.

### 7. Break correlated confidence

Assume an agent can repeat the same misunderstanding in implementation, tests, and checking tools. Add at least one independent evidence source for R2/R3 changes and whenever the oracle is weak:

- derive expected results from an external specification, source record, historical fixture, or independently calculated example;
- compare against a trusted existing implementation or alternate implementation;
- use property, metamorphic, mutation, fuzz, or fault-injection testing;
- use a fresh reviewer who receives the artifact, requirements, and acceptance criteria rather than the author's intended verdict;
- manually exercise the real surface and inspect externally visible state.

Do not call a checker trustworthy merely because it is deterministic. Demonstrate that it rejects known-bad artifacts and accepts known-good ones.

### 8. Stop at the proven boundary

Finish only when the requested behavior is implemented, changed-file diagnostics are clean, relevant builds and tests pass, the runtime or manual surface required by the selected tier has been observed, and every unverified layer is named. If the artifact has no meaningful runtime or manual surface, record why none applies and exercise the nearest executable driver or consumer instead. If the user asked for deployment or production proof, continue through that authorized surface; otherwise stop at production-ready source and state that deployment remains unverified.

## Return a production evidence packet

Report:

```text
Outcome:
Risk tier and artifact classes:
Critical invariants:
Changed scope / do-not-do scope:
Reading and review performed:
Evidence by layer:
Independent oracle or adversarial check:
Release and rollback status:
Unverified surfaces and residual risk:
```

Keep claims precise. Say “build passed”, “isolated database behavior passed”, “local host exercised”, or “production observed” only when that exact evidence exists.
