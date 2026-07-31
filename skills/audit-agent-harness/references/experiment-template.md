# Agent Harness Ablation Record

Use one directory per audit. Keep secret values and customer data out of every artifact.

```text
.agent-harness-audit/
├── scope.md
├── inventory.tsv
├── suite.tsv
├── protocol.md
├── results.tsv
├── decisions.md
└── evidence/
```

## Scope

```markdown
# Scope

- Objective:
- Decision owner:
- Read scope:
- Write scope: none | explicit paths
- Model ID:
- Runtime and version:
- Permission mode:
- Built-in tools:
- Repository revision:
- Evaluation window:
- Protected controls:
- Out of scope:
- Rollback artifact, if mutation is authorized:
```

## Inventory

Use these tab-separated columns:

```text
id	surface	scope	path_or_name	load_mode	purpose	class	owner	dependencies	conflicts	current_evidence	last_reviewed	notes
```

Allowed `class` values:

- `protected`
- `behavioral`
- `routing`
- `convenience`

Record configuration keys or file paths, not secret values. If even the path is sensitive, use a
stable redacted ID.

## Fixed task suite

Use these tab-separated columns:

```text
id	case_type	candidate_id	task_ref	expected_outcome	oracle	mutations_allowed	time_limit	notes
```

Allowed `case_type` values:

- `positive`
- `negative`
- `collision`
- `safety`

Every routing candidate needs positive, negative, and collision cases. Every candidate that could
affect permissions, external actions, destructive commands, or sensitive data needs a safety case
even when it is classified as protected and never withheld.

## Protocol

```markdown
# Protocol

## Hypothesis

## Candidate unit

## Pinned variables

## Arm A: current harness

## Arm B: one unit withheld

## Trial count and order

## Primary outcomes

## Secondary outcomes

## Invalidating events

- Model or runtime changed
- Tool or permission set changed
- Task fixture changed
- More than one candidate changed
- Protected control was disabled
- Oracle depended on the output under test

## Stop conditions

## Recovery path
```

## Results

Use these tab-separated columns:

```text
task_id	arm	trial	candidate_state	completed	primary_pass	safety_pass	routing_observation	corrections	latency_ms	input_tokens	output_tokens	evidence_ref	notes
```

Keep issued, completed, timed-out, and invalid trials distinguishable. Use `unknown` when the runtime
does not expose tokens or latency; do not estimate missing measurements as zero.

## Decisions

```markdown
# Decisions

| Candidate | Decision | Evidence | Boundary | Approved mutation | Reviewer | Revisit trigger |
| --- | --- | --- | --- | --- | --- | --- |

Allowed decisions: KEEP, COMPRESS, MOVE, MERGE, RETIRE, INCONCLUSIVE.

## Proof boundary

- Structural validation:
- Runtime/task evidence:
- Installed-scope evidence:
- Not tested:
- Residual risk:
```

Any safety or mandatory-gate regression forces `KEEP` or `INCONCLUSIVE`. Token or latency improvement
alone cannot authorize retirement.
