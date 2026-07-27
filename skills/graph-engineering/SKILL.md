---
name: graph-engineering
description: Design and execute explicit graph-shaped agent workflows with specialized nodes, bounded routing, fan-out/fan-in, clean handoffs, single-writer ownership, and independent verification. Use when the user asks for Graph Engineering, agent graphs, multi-agent orchestration, parallel specialist work, author-review separation, or auditable routing, or when no more specific workflow skill owns the orchestration and the task genuinely needs independent contexts, different tools or permissions, parallel discovery, conditional branches, or a bounded repair loop. Let an explicitly named or more task-specific workflow skill own its prescribed topology, using this skill only for justified surrounding stages. Do not use for trivial work or a single well-scoped discover-execute-verify loop.
---

# Graph Engineering Topology

Design the lightest reliable execution topology the task justifies. Compose reliable agent loops into an explicit graph only when the work needs one. Treat the topology as contracts, not as an excuse to spawn more agents.

## Model the execution topology

At any scale, define the same topology contract: objective, success bar, nodes, edges, state, ownership, and limits. Then require verification and exit evidence from the real artifact or runtime surface. Section 2 defines the contract in detail; scale its ceremony to the task's risk.

Use this canonical lifecycle as the default shape:

```text
intake -> discover -> decide -> execute -> verify
                                             ├─pass─> finish
                                             └─fail─> repair -> verify
```

Keep it as one loop unless isolated specialists, real parallelism, permission boundaries, conditional routing, or independent judgment materially improve the result.

## Preserve these invariants

- Obey the user, repository instructions, safety rules, and tool permissions at every node.
- Keep one write-capable owner per working tree. Run parallel writers only in independent worktrees with an explicit merge owner.
- Keep discovery, implementation, and verification evidence-backed. Do not accept a node's confidence as proof.
- Give an independent verifier the artifact and acceptance criteria, not the author's hidden reasoning or intended verdict.
- Pass only the minimum task-local context. Remove secrets, credentials, customer data, and unrelated private configuration before using external agents or models.
- Keep the root agent responsible for topology, arbitration, scope, and the final claim.

## Compose with other skills

Treat this skill as a topology layer, not as a replacement for domain, safety, or task-specific workflows. Apply matching instructions in this order unless higher-priority runtime rules say otherwise:

1. Follow the user's explicitly named skill or workflow.
2. Follow safety, compliance, and domain-governance skills that define mandatory gates.
3. Follow the most task-specific workflow skill that owns the requested operation.
4. Use this skill to connect otherwise unowned stages and decide whether they need a loop, graph, or degraded path.

In a complete engineering work system, governance selects the risk path, this skill owns only execution topology and routing, task-specific skills own domain execution, and fresh verification supplies the exit evidence. Keep those responsibilities separate instead of building one monolithic workflow skill.

When `coding-task-controller` is active, let it choose the coding risk path, required discovery, and validation gates. Represent those phases as separate nodes only when this skill's graph test is satisfied.

When a specific orchestration skill such as `review-mr` or `gpt55-fusion` matches, use its prescribed reviewers, agents, and routing. Do not wrap it in duplicate reviewers or judges. Add upstream discovery or downstream delivery nodes only when the task requires them and the specific skill does not already own them.

If two skills appear to own the same node, prefer the more specific skill and keep one owner. Ask the user only when explicit skill requests conflict and materially change the result.

## 1. Decide whether a graph earns its cost

Start with one loop. Promote the task to a graph only when at least one graph capability materially improves the outcome:

- Distinct specialties need separate contexts, tools, models, or permissions.
- Independent work can fan out in parallel and later fan in through a defined merge.
- Author and verifier must be separated to avoid self-approval.
- Conditional routing, a human gate, or an auditable repair path must be explicit.

Keep a loop when one owner can perform the work sequentially, the context remains clean, and no independent branch changes the decision. A sequence of boxes is not automatically a graph.

State the choice in one sentence before orchestration:

```text
Topology: graph - two read-only investigations can run independently, then one writer and a fresh verifier need explicit routing.
```

or:

```text
Topology: loop - this is one localized task with no useful fan-out, permission split, or independent review requirement.
```

If the choice is uncertain, read [references/patterns.md](references/patterns.md) and use its decision table.

## 2. Define the graph contract

Define the graph before starting child nodes. Record:

1. **Objective** - Name the observable user outcome, not an activity.
2. **Success bar** - Specify the evidence that permits the graph to stop.
3. **Nodes** - Give each node one responsibility, bounded inputs, an output schema, permissions, and a stop condition.
4. **Edges** - Define success, failure, fan-out, fan-in, retry, escalation, and human-confirmation routes up front.
5. **State** - Pass compact evidence packets instead of complete transcripts.
6. **Ownership** - Name the only writer for every shared artifact or working tree.
7. **Limits** - Set concurrency, retry, time, cost, and side-effect boundaries appropriate to the task.

Represent the planned path compactly:

```text
discover_a ─┐
            ├─> synthesize -> implement -> verify ─pass─> finish
discover_b ─┘                              └─fail─> repair -> verify
```

Use planning or task-tracking tools when available. Keep graph nodes atomic and ensure exactly one execution node owns each mutable surface.

## 3. Select nodes from available capabilities

Inspect the current agent catalog and tools before choosing implementations. Treat `explorer`, `writer`, and `verifier` as role labels, not guaranteed tool or agent names.

- Choose the lightest capable role allowed by local routing rules.
- Use read-only nodes for discovery, alternatives, risk analysis, and review.
- Use one write-capable node for implementation in a shared working tree.
- Use independent worktrees when the graph truly requires parallel writes.
- Keep two opinion nodes independent. Do not give either the other's conclusion before fan-in.
- Use a separate adjudicator only when conflicting evidence cannot be resolved directly by the root agent.

If child-agent support is unavailable, run the task as a single loop or a clearly labeled degraded sequential workflow. Do not claim independent contexts or fan-out that did not occur.

## 4. Execute and route by evidence

1. Start independent read-only nodes in parallel when their outputs do not depend on each other.
2. Give every node the objective, allowed scope, forbidden scope, expected output, required evidence, and exact stop condition.
3. Wait for the required branches, then inspect their raw evidence before synthesizing. Resolve contradictions instead of averaging them.
4. Send the writer only the approved decision, relevant evidence, scope, ownership, and acceptance checks.
5. Inspect the resulting artifact or diff in the root context before verification.
6. Send the verifier the artifact, user-visible acceptance criteria, and applicable validation surface. Keep the verifier read-only.
7. Route a failure back to the owning writer as a minimal failure packet: reproduction, expected result, observed result, relevant artifact, and required check.
8. Re-run only the affected validation after a repair. Use a declared retry cap, defaulting to two repair rounds when no stronger local rule exists.
9. Escalate to the user only when the next route requires new authority, a destructive action, sensitive disclosure, or a product decision that evidence cannot resolve.

Do not restart the whole graph when one node fails. Resume from the latest valid state unless upstream evidence is stale or invalidated.

## 5. Keep handoffs structured

Use this minimum state packet between nodes:

```text
Objective:
Current node:
Allowed scope:
Forbidden scope:
Inputs and evidence:
Decision or artifact:
Validation already run:
Open risks or contradictions:
Next route and stop condition:
```

Keep facts traceable to files, commands, logs, URLs, or user statements. Label inferences and unresolved assumptions. Read [references/patterns.md](references/patterns.md) for fuller node and failure packet templates.

## 6. Verify on the real surface

Match verification to the artifact:

- Code or configuration: inspect the diff, run focused diagnostics, build, and tests, then exercise the changed behavior when possible.
- CLI: run the command through its normal entry point and inspect exit status and output.
- Service or API: exercise the live local surface with a minimal request.
- Document or analysis: check source traceability, required coverage, internal consistency, and rendering or delivery format.
- Workflow or skill: validate its structure, then forward-test it in a fresh context with a realistic prompt and no leaked expected answer.

Distinguish a product failure from a blocked validation environment. Never convert an unrun check into a passing claim.

## 7. Finish with an auditable result

Stop immediately when the success bar is satisfied and no requested work remains. Report:

```text
Topology: loop | graph | degraded
Path executed: node -> node -> node
Result: observable outcome
Validation: commands, checks, or reviewer evidence
Unverified: checks not run and why
Residual risk: remaining risk or none
```

Do not report internal orchestration detail that does not help the user verify the outcome.
