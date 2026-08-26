# Project Capability Model

Use this model to produce an evidence-backed profile, not a universal maturity contest. Score each
capability independently and preserve unknowns. Do not collapse the result into one aggregate score.

## Maturity scale

| Level | Meaning | Minimum evidence |
|---|---|---|
| `L0 Unknown` | Available evidence cannot establish the current capability. | Named missing surface and why it matters. |
| `L1 Ad hoc` | Work depends mainly on individual knowledge or unrepeated manual steps. | Observed workflow, repository artifact, or reproducible absence of an entry point. |
| `L2 Documented` | The expected path or rule is documented, but enforcement or repeatability is unobserved. | Current, discoverable repository documentation or configuration. |
| `L3 Enforced` | Important invariants are mechanically checked and their result is observable. | Successful authorized check at the claimed environment layer. |
| `L4 Adaptive` | The capability has measured feedback, ownership, and a demonstrated improvement loop. | Versioned trend or recurring evidence plus a recorded correction loop. |

One strong sub-capability does not automatically raise the whole capability. Record mixed evidence
and use the lowest material condition when that condition blocks the requested outcome.

## Eight capabilities

### 1. Legibility

Can a new engineer or agent discover product intent, module ownership, architecture, important
decisions, and the next relevant source of truth without loading a monolithic manual?

Inspect repository maps, architecture and product docs, decision records, generated schemas,
cross-links, ownership, freshness checks, and disagreement between docs and code.

### 2. Reproducible setup

Can an authorized clean environment install dependencies, start the relevant system, load safe
fixtures, and run focused checks through stable entry points?

Inspect pinned dependencies, bootstrap/start/check commands, environment examples, health checks,
fixtures, isolation, and local-to-CI differences. Do not execute network or external writes without
authority.

### 3. Architecture enforceability

Are important dependency directions, data parsing seams, naming or size limits, and reliability
invariants mechanically enforced with useful remediation feedback?

Documentation alone reaches at most `L2`. Prefer structural tests, custom lints, schema validation,
type checks, and error messages that explain the permitted repair path.

### 4. Testing and verification

Can changes be evaluated through stable module interfaces and observable user or system behavior?

Inspect fast checks, module/interface tests, integration and contract tests, end-to-end journeys,
failure and recovery coverage, trusted fixtures, regression reproduction, flake handling, and proof
boundaries. Coverage percentage alone does not establish oracle quality.

### 5. Observability

Can an authorized developer or agent observe failures, state transitions, latency, and critical
journeys using structured logs, metrics, traces, diagnostics, or reproducible artifacts?

Configuration proves availability intent; queries or observed signals prove operation only at the
environment actually inspected.

### 6. Delivery and recovery

Are build, review, release, migration, rollout, rollback, and recovery controls proportionate to the
change risk and demonstrably repeatable?

Inspect CI gates, artifact provenance, risk tiers, feature flags, migration checks, rollback paths,
canaries, and release evidence. Do not infer deployment authority from automation.

### 7. Security and authority

Are secrets, sensitive data, dependencies, network access, write permissions, approvals, and audit
events constrained by deterministic controls rather than reminders alone?

Do not inspect secret values. Record only policy and minimum metadata. A written rule without an
enforced permission or gate reaches at most `L2`.

### 8. Gardening and learning

Does the project detect and correct documentation drift, architecture erosion, flaky tests,
dependency decay, repeated review feedback, technical debt, and agent-harness regressions?

Inspect quality scorecards, debt registers, recurring jobs, incident-to-test or incident-to-rule
links, small repair records, trend evidence, owners, and model/runtime re-evaluation.

## Gap selection

Select one gap, or at most two that cannot be separated, using this order:

1. protected safety, data, permission, and recovery failures;
2. inability to build, start, observe, or verify the requested work;
3. repeated correctness or architecture failures;
4. missing repository knowledge that causes wrong work;
5. delivery friction and recurring manual correction;
6. cost, latency, convenience, and polish.

Prefer an increment that establishes a reusable feedback loop. Do not recommend a capability merely
because a tool is fashionable or absent.
