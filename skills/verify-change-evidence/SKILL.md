---
name: verify-change-evidence
description: >
  Independently verifies completed code-change behavior and records evidence from authorized
  tests, runtime paths, and manual surfaces. Use after implementation for QA, regression
  reproduction, acceptance evidence, or proof-boundary reporting. Excludes production-code fixes,
  diff or MR findings, approval, deployment, and production claims without observing that surface.
---

# Verify Change Evidence

## Proof boundaries

- Derive expected results from an independent contract, source record, or trusted fixture; do not use the changed implementation as its own oracle.
- Mark each check passed, failed, blocked, skipped, or not-applicable. Stop at the highest layer observed and never turn local tests into staging or production proof, approval, or deployment.
- Preserve target identity without secrets, command, exit status, timestamp when useful, result, and artifact path or hash; hand formal presentation to `report-writer` without surrendering case and assertion ownership.

Independently determine what behavior was actually observed after a completed change. Execute only
authorized checks and report the evidence boundary precisely. Do not repair production code, review
the diff for findings, approve the change, deploy it, or infer production behavior from local tests.

## Receive a testable handoff

Collect the requested behavior, changed seams, active context, data and state ownership, risk and
rollback constraints, acceptance checks, known assumptions, author-run evidence, target environment,
and any required manual scenario. If the behavior cannot be tested from this material, name the
missing prerequisite rather than filling it with a guess.

## Verify behavior

1. Derive expected results from requirements, contracts, source records, or a trusted fixture rather
   than the changed implementation alone.
2. Run the narrowest relevant checks first, then the authorized integration, host/runtime, or manual
   surface needed for the claim.
3. Exercise success, failure, recovery, and changed edge behavior where the risk warrants it. Cover
   both one-record and batch flow contracts when either can differ. Record a skipped layer and
   reason instead of treating it as passed.
4. Preserve commands, target/environment identity without secrets, exit status, timestamps when
   useful, concise results, and artifact paths or hashes.
5. Stop at the highest surface actually observed. Local tests, roll-backed database checks, staging,
   and production are different proof layers.

For HTTP API verification, inventory every applicable case and give each an executed, passed,
failed, blocked, skipped, or not-applicable state. Preserve sanitized request/response events and
artifacts as required by [report-writer's HTTP API test module](../report-writer/references/http-api-test.md)
and [log evidence module](../report-writer/references/log-evidence.md). Do not put reusable
credentials on command lines or in logs. A formal report request hands this evidence to
[report-writer](../report-writer/SKILL.md); verification retains ownership of cases and assertions.

For a defect reproduction, first demonstrate the pre-fix failure when practical and safe, then run
the completed change through the same observable scenario. Do not modify product code to make the
test pass; return a failed or blocked result to the implementation owner.

## Report an evidence packet

```markdown
# Change Verification Evidence

## Scope and proof boundary
- Requested behavior:
- Changed seams under test:
- Target/environment:
- Active context and lifecycle ownership:
- Highest observed layer:

## Checks executed
| Check | Command or manual scenario | Result | Evidence/artifact |
|-------|----------------------------|--------|-------------------|

## Observed behavior
- Success path:
- Failure, recovery, or edge path:
- Single-record and batch behavior:

## Unverified layers and limits
- <layer>: <why unrun or unavailable>

## Result
<passed, failed, blocked, or partial; no approval or deployment conclusion>

## Handoff
- Implementation follow-up: <needed or none>
- Diff findings review: <route to review-mr when requested>
- Human or release authority: <needed or none>
```

Route failed behavior to [develop-production-code](../develop-production-code/SKILL.md) for a fix.
Route an existing diff to [review-mr](../review-mr/SKILL.md) for independent findings. Behavior
verification and diff review may both occur, but neither replaces the other.
