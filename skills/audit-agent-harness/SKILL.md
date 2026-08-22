---
name: audit-agent-harness
description: >
  Audit and simplify AI coding-agent customization through reversible ablation of CLAUDE.md,
  AGENTS.md, rules, Skills, Hooks, system prompts, agents, plugins, MCP configuration, and other
  harness layers. Use after a model or agent-runtime upgrade, during periodic harness hygiene,
  when instructions may be stale, conflicting, noisy, or duplicated, or when deciding what to
  keep, compress, move, merge, or retire. Treat bulk-delete requests as an audit plus an explicit
  approval gate. Do not use for production-code slimming, MR/PR-only review, ordinary prompt
  writing, secret rotation, or permission-policy redesign.
---

# Audit Agent Harness

## Ablation evidence boundary

- Pin model, runtime, permission mode, revision, fixtures, and evaluation window before comparing a unit; changing a pinned variable starts a new comparison.
- Protected controls stay active unless explicit authority and independent evidence justify change. Use positive, negative, and collision probes for routing units; token savings or a happy path is not evidence that a unit is safe to remove.
- Inventory only authorized scopes, record minimum metadata, and stage human-reviewable proposals; do not mutate the harness during inventory or expose credential values.

Determine whether each customization still improves observable behavior on the current model and
runtime. Treat cadence such as “every six months” as a reminder to remeasure, not as evidence that
deletion is safe.

## Preserve the control plane

Classify every unit before testing it:

| Class | Examples | Default treatment |
| --- | --- | --- |
| Protected | permission enforcement, destructive-command blockers, compliance, data boundaries, secret handling, audit logging | Keep active; inspect but do not ablate |
| Behavioral | coding conventions, workflow instructions, role prompts, reusable knowledge | Eligible for controlled ablation |
| Routing | Skill descriptions, agent selection, tool or workflow dispatch | Eligible only with positive, negative, and collision probes |
| Convenience | formatting, status display, repeated boilerplate, optional integrations | Prefer early audit candidates |

Never let token savings, speed, or a successful happy path compensate for a protected-control
failure. Do not read or copy credential values while inventorying settings. Record only the minimum
metadata needed to identify a unit.

## Run the audit

### 1. Freeze the question

Write one decision question per candidate, for example:

```text
Does rule-unit R7 improve invoice-state diagnosis on model M and runtime V without increasing
false routing or unsafe actions?
```

Pin the model ID, runtime version, permission mode, built-in tools, working-tree revision, test
fixtures, and evaluation window. If any pinned variable changes, start a new comparison rather
than combining results.

### 2. Inventory without mutating

Inspect only scopes the user placed in bounds. Default to the current project; do not inspect user,
organization, or managed configuration unless the user explicitly includes that scope. List broader
layers as uninspected when they may affect the result. Distinguish included scopes instead of
flattening precedence. For each unit record:

- stable ID, source, scope, owner, and load/trigger behavior;
- intended outcome and observable failure it prevents;
- dependencies, duplicates, conflicts, and stale copies;
- class: `protected | behavioral | routing | convenience`;
- current evidence and last review date, if known.

Do not infer that an instruction is useless because it is old, long, rarely triggered, or duplicated.
Defense in depth and rare high-consequence cases require explicit evaluation.

### 3. Build the fixed task suite

Use real, representative tasks with independent oracles. Include:

- positive cases where the candidate should help;
- negative cases where it should stay out of the way;
- collision cases where another rule, Skill, or tool owns the task;
- safety canaries for every affected boundary;
- at least one difficult task that historically exposed the claimed failure.

Pre-register primary outcomes. Prefer task correctness, gate adherence, wrong/missed routing,
unnecessary corrections, and reproducible runtime evidence. Treat latency and token use as secondary
metrics. Do not score prose similarity or the model's self-report that a Skill was used.

### 4. Compare one coherent unit

Run fresh, independent contexts:

```text
A: current harness
B: identical harness with one candidate unit withheld
```

Keep task inputs and permissions identical, vary order when practical, and repeat stochastic cases.
Withhold one unit at a time; a whole file may count as one unit only when its lines form one coherent
policy. Record issued trials, completed trials, failures, timeouts, and missing evidence separately.

Prefer a temporary copied configuration, explicit runtime override, or isolated worktree/sandbox.
Where the current Claude Code version documents `--safe-mode` or `--bare`, use whole-stack modes only
for read-only troubleshooting or an independently permission-constrained sandbox. They disable or
skip customizations and therefore cannot prove that removing local safety hooks is safe. Do not
invent equivalent flags for other runtimes; check their current documentation first.

### 5. Decide by marginal evidence

Assign one decision per unit:

| Decision | Evidence bar |
| --- | --- |
| `KEEP` | Prevents a reproduced failure or enforces a required boundary |
| `COMPRESS` | Same behavior survives a smaller formulation across the fixed suite |
| `MOVE` | Content is useful but belongs in a more selective surface, such as always-on to on-demand or instruction to deterministic hook |
| `MERGE` | Two units have the same owner, trigger, and outcome without weakening independent defenses |
| `RETIRE` | Withholding is non-inferior across relevant tasks and creates no safety, routing, or recovery regression |
| `INCONCLUSIVE` | Evidence is sparse, confounded, or inconsistent; keep current behavior pending another test |

Prefer `INCONCLUSIVE` to a deletion justified by absence of failures. State the tested model/runtime
and do not generalize beyond them.

### 6. Separate audit from mutation

The audit is read-only by default. Before applying a recommendation:

1. obtain explicit scope and write authorization;
2. preserve unrelated dirty work and create a recoverable snapshot or patch;
3. change one approved unit;
4. rerun the fixed suite and normal repository validators;
5. restore immediately on a protected-control, correctness, or routing regression;
6. record the decision, evidence, reviewer, and next review trigger.

Never interpret “audit,” “clean up,” or a periodic cadence as authorization to bulk-delete user or
organization configuration. Do not commit, push, deploy, rotate secrets, or alter managed policy
unless the user separately requests that action.

## Keep the evidence reusable

Use [references/experiment-template.md](references/experiment-template.md) for the artifact layout,
inventory fields, task corpus, result records, and decision log. Keep the result in the response by
default. When artifact writing is authorized, use the target repository's existing audit area; if
none exists, use `.agent-harness-audit/` and keep secret values out of it.

Report structural validation, isolated task results, installed runtime state, and production behavior
as separate evidence levels. A green Markdown validator does not prove routing, and an isolated
ablation does not prove organization-wide safety.

## Compose with neighboring Skills

- Use `codebase-slimming` for production source-code cleanup; this Skill owns agent customization.
- Use `engineering-work-system` only when the user needs cross-domain assessment or routing.
- Use `graph-engineering` only when the experiment needs independent contexts or explicit topology.
- Use `review-mr` after an authorized mutation creates an actual diff that needs review.
- Follow a more specific security or compliance Skill whenever protected controls are in scope.
