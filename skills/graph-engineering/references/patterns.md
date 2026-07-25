# Graph Engineering Patterns

Read this reference when selecting a topology, defining node contracts, or routing a failed verification.

## Contents

- [Topology decision table](#topology-decision-table)
- [Common topologies](#common-topologies)
- [Node contract](#node-contract)
- [Discovery packet](#discovery-packet)
- [Writer packet](#writer-packet)
- [Verification packet](#verification-packet)
- [Repair packet](#repair-packet)
- [Fan-in checklist](#fan-in-checklist)
- [Retry and stop rules](#retry-and-stop-rules)

## Topology decision table

| Signal | Prefer a loop | Prefer a graph |
|---|---|---|
| Responsibility | One coherent job | Distinct specialist responsibilities |
| Context | One clean context is enough | Roles need isolated contexts |
| Work shape | Mostly sequential | Real fan-out followed by fan-in |
| Tools and permissions | Same tools and authority | Different tools, models, or permissions |
| Evaluation | Owner can use objective checks | Fresh independent judgment is material |
| Control flow | Repeat until one exit test passes | Branches, joins, gates, or multiple repair routes |
| Audit need | Final evidence is enough | The chosen path and routing reasons must be inspectable |

Use a loop when the graph column has no material signal. Use a small graph when one strong signal or several moderate signals justify its overhead.

## Common topologies

### Single execution loop

```text
discover -> plan -> execute -> verify ─pass─> finish
             ^                    └─fail─> repair
```

Use for one well-scoped owner and objective validation. Do not spawn agents merely to imitate phases.

### Parallel discovery with one writer

```text
code_trace ─┐
risk_review ├─> root_synthesis -> writer -> verifier
test_trace ─┘                         ^          │
                                      └──fail────┘
```

Use when independent read-only investigations can shorten discovery or expose different evidence. Assign non-overlapping questions and require source paths or commands.

### Fan-out research and synthesis

```text
source_1 ─┐
source_2 ─┼─> merge -> author -> fact_check
source_n ─┘                   └─reject─> author
```

Require every branch to return the same schema. Define duplicate handling, missing-branch behavior, and the merge owner before fan-out.

### Independent opinions with adjudication

```text
analysis_a ─┐
            ├─> adjudicator -> root decision
analysis_b ─┘
```

Keep A and B independent. Give the adjudicator the original objective, both evidence packages, and decision criteria. Ask it to identify consensus, contradictions, unique evidence, and unresolved uncertainty rather than average conclusions.

### Human gate for consequential side effects

```text
prepare -> verify_plan -> human_gate ─approve─> execute -> verify_result
                              └─reject─> stop
```

Use when a destructive action, external write, sensitive disclosure, or material scope expansion requires user authority. Prepare reversible evidence before requesting approval.

## Node contract

```text
Node id:
Responsibility:
Objective:
Inputs:
Allowed tools and permissions:
Allowed files or systems:
Forbidden actions:
Required output schema:
Evidence requirements:
Stop condition:
Timeout or budget:
Failure route:
```

Make the output schema easy to merge. Prefer paths, identifiers, concise findings, and command results over prose narratives.

## Discovery packet

```text
Finding:
Evidence:
Why it matters:
Confidence:
Unknowns:
Recommended next route:
```

## Writer packet

```text
Approved outcome:
Owned files or artifact:
Relevant evidence:
Constraints and forbidden scope:
Acceptance checks:
Expected handoff artifact:
```

## Verification packet

```text
Artifact or commit inspected:
Acceptance criterion:
Check performed:
Expected result:
Observed result:
Verdict: pass | fail | blocked
Failure evidence or blocked reason:
Residual risk:
```

## Repair packet

```text
Failed criterion:
Minimal reproduction:
Expected result:
Observed result:
Relevant artifact or lines:
Required correction:
Check to rerun:
Repair attempt: current / limit
```

Return only failure evidence that the writer needs. Do not send the verifier's private reasoning or broaden the writer's scope.

## Fan-in checklist

Before merging branch results, confirm:

- Every required branch returned or was explicitly marked blocked.
- All branches used the declared output schema.
- Evidence remains traceable after deduplication.
- Contradictions are visible and resolved or escalated.
- The merge did not silently drop an empty, failed, or dissenting branch.
- Downstream nodes receive only the context they need.

## Retry and stop rules

- Define a finite retry limit before the first repair.
- Route the same failure back only when the new packet contains actionable evidence.
- Stop retrying when the same blocker repeats, upstream assumptions are invalid, or new authority is required.
- Invalidate downstream state when an upstream artifact changes materially.
- Stop the graph as soon as the observable success bar is met.
