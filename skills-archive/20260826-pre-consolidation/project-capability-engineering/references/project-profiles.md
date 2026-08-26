# Project Profiles and Ratchets

Classify the project from inspected evidence. If the evidence is mixed or the active path is
unknown, use `unknown` and list what would distinguish the profiles.

## Greenfield

Signals include a new or small codebase, few compatibility obligations, and architecture or
delivery choices that remain reversible.

Recommend a minimum foundation around real work: a short repository map, one reproducible start
path, one combined check path, the first important module interface, one executable invariant,
focused tests, basic structured diagnostics, CI, and explicit authority limits. Avoid speculative
platforms, empty documents, and controls whose invariant has not been identified.

## Healthy existing

Signals include a working golden path, maintained tests and CI, discoverable conventions, and
localized rather than systemic gaps.

Extend the project's existing tools and information hierarchy. Prefer one missing constraint,
feedback signal, or recurring maintenance check. Do not create a competing formatter, test runner,
documentation tree, or release workflow merely to normalize the project to a template.

## Legacy

Signals include fragile or unreproducible builds, sparse behavior evidence, hidden compatibility,
dynamic or implicit dependencies, contradictory documentation, broad debt, or high regression
uncertainty.

Use this ratchet:

1. record a reproducible baseline and known defects;
2. identify one bounded pilot seam outside the highest-risk core;
3. add characterization evidence before structural change;
4. prevent new or changed code from increasing the measured debt;
5. establish one mechanical invariant or verification path;
6. validate behavior and rollback before expanding;
7. lower the accepted debt budget gradually.

Never recommend a big-bang rewrite, immediate zero-warning gate, mass renaming, inferred dead-code
deletion, or replacement of a working build path without compatibility evidence.

## High-risk overlays

Apply one or more overlays independently of project age when the scope involves money, identity,
permissions, regulated or sensitive data, irreversible migration, safety-critical behavior,
cross-record state transitions, or broad external effects.

Require separately derived acceptance criteria, stronger failure and recovery evidence, narrow
permissions, auditability, and an explicit qualified-human or release gate. Throughput and easy code
generation never justify weakening these controls.

## Unknown profile

Use `unknown` when the active application, build path, deployment ownership, compatibility surface,
or repository role cannot be established. Return a bounded discovery request rather than choosing a
template by directory size, age, language, or test count alone.
