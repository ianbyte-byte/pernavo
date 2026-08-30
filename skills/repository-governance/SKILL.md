---
name: repository-governance
description: >
  Improve repository knowledge, agent configuration, memory, and engineering-system hygiene using
  observed evidence. Use for documentation drift, CLAUDE.md or AGENTS.md cleanup, capability
  assessment, skill-system audits, and reversible customization ablations. Keep local facts,
  unknowns, permissions, and production claims separate.
---

# Repository Governance

Inventory before editing: source of truth, active revision, project instructions, build/test entry
points, owner boundaries, generated files, and existing memory/configuration. Treat documentation as
an assertion to verify, not as proof of runtime behavior.

## Safe increments

Choose one reversible increment: fix a stale instruction, add a missing command, consolidate a
duplicate rule, or stage an ablation. Preserve safety controls, credentials, tests, and unrelated
customizations. Do not mass-delete, rewrite prompts, or claim a host loaded a Skill without trace
evidence. Archive retired material with reason, date, and restore path.

## Report

Record observed facts, assumptions, unknowns, proposed change, expected signal, rollback, and the
highest evidence layer reached. Route code changes to `engineering-workflow`, review to
`change-review`, and formal output to `report-writer`. Do not implement from a `change-review`
finding list, and do not turn one reversible increment into a review-fix loop.
