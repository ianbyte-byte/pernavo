---
name: repository-knowledge-gardening
description: >
  Assesses repository-local project knowledge and designs continuous improvements for short agent
  maps, structured documentation, architecture and product records, executable plans, generated
  references, ownership, freshness, cross-links, and documentation drift. Use for documentation
  inventory, repository knowledge maps, docs-as-system-of-record design, stale or contradictory
  documentation audits, post-change documentation synchronization planning, or recurring
  documentation gardening design. Excludes one-off copyediting, ordinary README wording fixes,
  agent-rule ablation, production-code cleanup, implementation of documentation changes,
  deployment, and claims that unobserved code or runtime behavior is documented correctly.
---

# Repository Knowledge Gardening

Make repository-local knowledge discoverable, versioned, progressively disclosed, and verifiable
for humans and coding agents. Produce a documentation inventory, drift assessment, and one focused
gardening increment. This V1 is read-only: do not edit the assessed repository, create or delete
documents, install documentation tools, open pull requests, schedule jobs, or operate external
systems.

The design is informed by OpenAI's
[Harness engineering](https://openai.com/index/harness-engineering/) account: use a small map rather
than a monolithic agent manual, treat structured repository knowledge as a system of record, enforce
freshness and cross-links mechanically, and garden drift in small recurring changes. Apply these as
principles, not as proof that one directory layout or autonomy level fits every project. See
[harness principles](references/harness-principles.md).

## Interface

### Inputs

- The repository and documentation scope to inspect.
- The requested outcome: inventory, drift audit, agent legibility, post-change synchronization, or
  recurring gardening design.
- Any named source-of-truth, ownership, environment, security, compliance, or historical constraints.

Inspect only authorized repository-local sources. Knowledge in external docs, chat, tickets, live
systems, or people's heads is unobserved unless the user authorizes and exposes it. Record the gap;
do not copy sensitive content or silently treat the repository as complete.

### Output

Return one completed [knowledge gardening report](templates/knowledge-gardening-report.md) with:

1. repository revision, dirty state, inspected scope, and proof boundary;
2. a documentation inventory classified by role, authority, maintenance mode, owner, and status;
3. the entry map and progressive-disclosure path an agent or new engineer can follow;
4. confirmed drift, suspected drift, contradictions, duplicates, and unknowns;
5. deterministic verification opportunities and checks that remain semantic or human-owned;
6. one smallest reversible gardening increment with an observable acceptance condition;
7. handoffs for implementation, independent verification, review, and any human decision.

Do not output a generic documentation tree, rewrite proposal, or freshness score without evidence.

## Assessment workflow

1. **Freeze scope and authority.** Record the repository revision, dirty state, target docs, allowed
   reads, unavailable sources, and whether the request is inventory, drift, synchronization, or
   recurring-gardening design.
2. **Find current entry points.** Inspect existing agent guidance, README, architecture and product
   docs, decision records, plans, generated references, operations guides, quality/security policy,
   and documentation tooling. Extend the established structure rather than imposing a template.
3. **Build the inventory.** Apply the roles, authority classes, maintenance modes, and statuses in
   [the knowledge model](references/knowledge-model.md). Record the canonical or candidate source of
   truth for each material claim family.
4. **Trace progressive disclosure.** Determine whether a short stable map leads to deeper indexed
   sources without forcing every task to load an encyclopedia. Treat a large agent instruction file
   as a drift risk, not an automatic defect.
5. **Detect drift.** Classify each finding as `confirmed-drift`, `suspected-drift`, `contradiction`,
   `duplicate`, or `unknown`. A missing file or broken reference can be confirmed; semantic mismatch
   usually requires a trusted contract, test, runtime observation, or human decision.
6. **Select verification.** Use [documentation oracles](references/documentation-oracles.md) to
   separate deterministic link, structure, command, code-reference, and generated-artifact checks
   from semantic and operational claims.
7. **Choose one increment.** Prefer a small improvement that makes future drift observable: an index,
   ownership field, source declaration, executable check, generated reference, or bounded correction.
   When a critical rule repeatedly escapes documentation, recommend promotion to a lint, test, schema,
   permission, or tool rather than adding more prose.
8. **Route, do not absorb.** Send authorized edits through the normal change lifecycle. Scheduling,
   pull-request creation, merging, deployment, and external publication require their own runtime and
   authority.

## Knowledge-system invariants

- A top-level agent file should primarily map tasks to deeper sources; do not make it the default
  encyclopedia. Do not enforce an arbitrary line count when the project has a justified exception.
- Repository-local, versioned artifacts are preferable for knowledge needed during agent execution,
  but external authoritative systems must be referenced rather than silently copied or downgraded.
- Generated documentation must name its canonical input and generator. Human-maintained decisions
  must not be overwritten from implementation alone.
- Active plans, completed plans, debt, historical records, and generated references must remain
  distinguishable; do not rewrite history to resemble the current implementation.
- Every material freshness claim must name an observable basis such as a successful generator run,
  command execution, schema comparison, reviewed decision, or target-runtime observation.
- A document's presence proves availability, not correctness, enforcement, adoption, or production
  behavior.

## Drift and safety rules

- Never infer that implementation behavior is the intended product contract merely because it is
  current code.
- Do not delete or archive historical, compatibility, security, compliance, incident, or decision
  records without explicit authority and an identified retention rule.
- Preserve unrelated dirty documentation work and report overlapping files before proposing edits.
- Do not read secret values, include sensitive external content in reports, or execute documented
  commands that require network, credentials, writes, migrations, or production access without
  separate authority.
- An unreachable external URL is an observation at a time and environment, not proof that the source
  is obsolete.
- If code, tests, docs, generated artifacts, and runtime evidence disagree, report the contradiction
  and required owner decision; do not choose the convenient source silently.

## Ownership and composition

| Need | Owner |
|---|---|
| Repository-wide capability baseline and gap priority | `project-capability-engineering` |
| Missing code, data, runtime, or historical facts | `unknowns-field-guide` |
| Risk path and lifecycle handoffs for retained edits | `coding-task-controller` |
| Executable documentation-change plan | `plan-code-change` |
| Independent command, generated-artifact, or observed-behavior evidence | `verify-change-evidence` |
| Findings on a completed documentation diff | `review-mr` |
| Reliability policy, SLO, runbook, and incident-learning substance | `aviation-grade-engineering` |
| AGENTS.md, Skills, Hooks, prompt, and agent-runtime effectiveness audit | `audit-agent-harness` |
| Behavior-preserving production-source cleanup | `codebase-slimming` |
| Cross-domain routing | `engineering-work-system` |

This Skill owns the repository knowledge model and gardening assessment. It does not own the
correctness of business policy, architecture decisions, SLO targets, security policy, production
behavior, or external knowledge systems.

## Stop and hand off

Stop and name the missing prerequisite when:

- the repository, active documentation set, or requested claim family cannot be identified;
- deciding which source is authoritative requires an unresolved product, architecture, security,
  compliance, retention, or historical decision;
- the only way to validate a claim is an unauthorized external read or side effect;
- a proposed correction overlaps unrelated dirty work and cannot be isolated safely;
- available evidence cannot distinguish stale documentation from stale implementation.

The report is not a documentation correction, accepted architecture decision, release approval,
runtime verification, scheduled automation, or production-health claim.
