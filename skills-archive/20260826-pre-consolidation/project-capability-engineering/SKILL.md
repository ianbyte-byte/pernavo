---
name: project-capability-engineering
description: >
  Assesses repository-local engineering capabilities for greenfield, existing, and legacy
  projects: project legibility, reproducible setup, architecture enforcement, testing and
  verification, observability, delivery and recovery, security guardrails, and continuous
  learning. Use when making a repository agent-ready, establishing an evidence-based project
  quality baseline, diagnosing cross-cutting project-capability gaps, or selecting the next
  reversible engineering-foundation improvement. Excludes one-off feature or bug work, ordinary
  QA or diff review, production deployment, agent-customization ablation, reliability-only work,
  behavior-preserving source cleanup, and implementation of the recommended improvement.
---

# Project Capability Engineering

## Assessment evidence boundary

- This V1 is read-only: record revision, dirty state, inspected and uninspected scopes, and unknown runtime/external evidence; do not implement the recommended increment or install tools.
- Score each capability from observed evidence, not documentation or configuration alone. Choose one highest-leverage reversible increment with an observable acceptance check, rollback, and owners.
- A score or baseline is not proof of production health, release readiness, or deployment.

Assess how well a repository enables humans and coding agents to understand, change, verify, ship,
and continuously improve the project. Produce an evidence-based baseline and one focused capability
increment. This V1 is read-only: do not implement the increment, edit the assessed repository,
install tools, change permissions, deploy, or operate an external environment.

## Interface

### Inputs

- The repository or project scope to assess.
- The requested outcome, such as agent readiness, a greenfield foundation, legacy-project
  improvement, or a general engineering-capability baseline.
- Any named environment, risk, compliance, delivery, or authority constraints.

When a decision-changing fact is missing, inspect the authorized repository first. Mark unavailable
runtime, organization, production, or external-system evidence as unknown; do not substitute a
nearby environment or infer behavior from configuration alone.

### Output

Return one completed [capability increment](templates/capability-increment.md) containing:

1. project profile and risk overlays;
2. an eight-capability evidence scorecard;
3. facts, unknowns, confidence, and the highest observed evidence layer;
4. the one highest-leverage gap, or at most two inseparable gaps;
5. one reversible target increment with an observable acceptance condition;
6. explicit do-not-do scope, verification needs, and lifecycle handoff owners.

Do not return a context-free best-practices checklist or one aggregate quality score.

## Assessment workflow

1. **Confirm scope and authority.** Assessment authorizes read-only inspection and reporting only.
   Record the repository revision, dirty state, inspected environment, and uninspected surfaces.
2. **Classify the project.** Use [project profiles](references/project-profiles.md) to classify it as
   greenfield, healthy existing, legacy, or unknown. Add high-risk overlays independently.
3. **Inspect real entry points.** Prefer existing build files, scripts, CI, tests, architecture and
   product docs, schemas, lint rules, observability configuration, release controls, and recent
   repository evidence over stated intentions.
4. **Score by evidence.** Apply the eight capabilities and L0-L4 scale in
   [the capability model](references/capability-model.md). A document proves that a practice is
   documented, not enforced; a configured check proves neither a successful run nor target behavior.
5. **Find the limiting capability.** Identify the smallest capability gap that blocks reliable work
   or causes repeated human correction. Prefer leverage, consequence reduction, and short feedback
   loops over broad cleanup or ideal-state completeness.
6. **Define one increment.** State the current condition, target condition, invariant, observable
   acceptance check, rollback, and evidence still required. For legacy projects, establish a baseline
   and non-regression ratchet rather than demanding immediate zero debt.
7. **Route, do not absorb.** Hand actual changes through the repository's normal lifecycle. Keep
   discovery, planning, implementation, verification, review, reliability, cleanup, and agent-harness
   ownership with their focused Skills.

## Evidence rules

- Use `L0 Unknown` when evidence is unavailable. Never reward missing evidence.
- Attach a path, command result, configuration location, or explicit unavailable-surface reason to
  every material conclusion.
- Report confidence as `low`, `medium`, or `high`; confidence never upgrades the evidence layer.
- Separate repository-static, local-execution, CI, staging, production, and organization-process
  observations. Stop claims at the highest layer actually observed.
- Record contradictory evidence instead of averaging it away.
- Do not infer architectural conformance, test health, operational reliability, security, or release
  readiness from the presence of a document or tool configuration.

## Selection rules

- For a **greenfield** project, recommend the smallest useful foundation; avoid empty policy files,
  speculative infrastructure, and constraints without a demonstrated invariant.
- For a **healthy existing** project, extend the established golden path instead of creating a
  competing tool, document hierarchy, or workflow.
- For a **legacy** project, characterize behavior first, preserve compatibility, prevent new debt,
  and tighten one measurable budget gradually. Do not propose a big-bang rewrite.
- For a **high-risk overlay**, require stronger independent evidence and human or release gates; do
  not treat automation throughput as a reason to weaken controls.

## Ownership and composition

| Need after assessment | Owner |
|---|---|
| Missing active-context or lifecycle facts | `unknowns-field-guide` |
| Risk path and required handoffs | `coding-task-controller` |
| Executable retained-change plan | `plan-code-change` |
| Smallest authorized implementation | `develop-production-code` |
| Independent completed-change behavior evidence | `verify-change-evidence` |
| Existing-diff findings | `review-mr` |
| SLO, resilience, observability, or incident program | `aviation-grade-engineering` |
| Repository documentation inventory, drift, and gardening design | `repository-knowledge-gardening` |
| Behavior-preserving source cleanup | `codebase-slimming` |
| AGENTS.md, Skills, Hooks, prompts, or agent-runtime customization audit | `audit-agent-harness` |
| Cross-domain routing | `engineering-work-system` |

The capability assessment may recommend these owners but does not perform their work. If the user
also authorizes implementation, route the selected increment through the normal lifecycle without
making the user approve each ordinary internal handoff. Preserve any required human, security,
release, or production gate.

## Stop and hand off

Stop the assessment and name the missing prerequisite when:

- the repository or intended target cannot be identified;
- a P0 business, data, permission, compliance, or compatibility decision has no safe default;
- assessing the requested capability requires unavailable credentials or unauthorized external
  access;
- existing evidence is too weak to select one improvement without inventing project behavior.

An assessment is not approval, implementation evidence, deployment evidence, or a production-health
claim.
