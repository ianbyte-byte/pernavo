# Unknowns Field Guide Reference

Use this reference only for pre-change discovery. Planning belongs to
[plan-code-change](../plan-code-change/SKILL.md); implementation, verification, and review belong
to their separate owners.

## Information categories

| Category | Meaning | Example |
|----------|---------|---------|
| Known Knowns | Explicit and confirmed by inspected evidence | Existing endpoint contract and caller |
| Known Unknowns | A known gap that needs evidence or a decision | Source of a state-transition field |
| Unknown Knowns | Likely unstated user criterion | Compatibility or rollback expectation |
| Unknown Unknowns | Hidden historical or downstream constraint | A scheduler or retry path uses the same seam |

## Blindspot pass

**Purpose:** discover pre-change constraints and evidence gaps.

1. Restate the task and named seam in 3–5 sentences.
2. List confirmed facts with source locations.
3. List known gaps and why each can change the result.
4. Probe likely hidden constraints: data grain, state, retries, idempotency, transactions,
   concurrency, permissions, history, consumers, deployment configuration, and observability.
5. Rank P0/P1/P2 and name only the P0 items that block a safe plan.

```markdown
# Discovery Report

## Task and named seam

## Known Knowns
- <fact>: <evidence pointer>

## Known Unknowns
- <question>: <why it matters>

## Unknown Knowns
- <suspected criterion>: <why it may matter>

## Unknown Unknowns / blindspots
- <risk>: <where it could occur>

## Risk ranking
- P0:
- P1:
- P2:

## Discovery handoff
- Confirmed constraints:
- Assumptions or safe defaults:
- Unresolved blockers:
- Evidence locations:
```

## Reverse interview

**Purpose:** ask only for a missing decision that cannot be resolved from local evidence.

For each question, state why it matters, the safe default if one exists, and the risk of that
default. Ask no more than needed to unblock a plan.

```markdown
# Reverse Interview

## Must-confirm questions
### <question>
- Why it matters:
- Evidence already checked:
- Safe default:
- Risk if wrong:

## Minimum safe handoff
<facts and defaults that plan-code-change may use, or the blocking decision>
```
