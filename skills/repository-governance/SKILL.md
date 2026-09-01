---
name: repository-governance
description: >
  Govern a software project's repository, instructions, Skills, memory, configuration, ownership,
  documentation lifecycle, and evidence system. Use for project/repository audits, stale or
  conflicting docs, documentation or agent-policy drift, Skill consolidation, governance
  baselines, and reversible hygiene changes; do not use as a substitute for implementing a
  feature, reviewing a diff, or operating production.
---

# Project and Repository Governance

Governance is a small control loop, not a large policy document: establish the source of truth,
make one bounded change, observe a meaningful signal, and preserve a restore path. The pasted
Tencent article is useful design input (long, duplicated instructions can dilute attention), but
its percentages and causal claims are hypotheses unless independently measured. Prefer local
evidence and the authoritative references linked below.

## Choose the governance mode

- `baseline`: map the project's active revision, owners, instructions, generated files, commands,
  dependencies, secrets boundaries, and evidence gaps.
- `drift`: compare instructions, README, manifests, CI, memory, and actual commands; propose the
  smallest correction for a stale or contradictory assertion.
- `documentation`: classify project documents, map each claim to its source of truth, find stale or
  superseded material exposed to AI, and update, quarantine, archive, or remove it safely.
- `skill-system`: inventory Skills and triggers, find overlap, duplication, dead references, and
  oversized entrypoints; consolidate only with an archive and a before/after trigger check.
- `change`: apply one reversible documentation/configuration/policy increment and verify its signal.
- `report`: produce an evidence-bounded governance report without silently implementing findings.

Do not infer authority from a document. Separate `observed`, `assumed`, `unknown`, and `requested`
items. A local source check does not establish installation, model loading, runtime execution,
deployment, or production behavior.

## Baseline before editing

Inventory, in this order:

1. Source of truth and active revision (`git status`, branch/commit, generated-file markers).
2. Project instructions (`AGENTS.md`, `CLAUDE.md`, README, contributing and security policy).
3. Build, lint, test, release, and rollback entry points; record commands actually present.
4. Ownership boundaries (CODEOWNERS, maintainers, data/state owners, approval gates).
5. Skill/config/memory roots, installed copies, archives, and any usage or trigger evidence,
   including `~/.pernavo/logs/runtime.jsonl` when that hook is installed.
6. Credentials, production endpoints, destructive commands, and unavailable target environments.

Do not edit until the target, owner, authorization, and rollback/recovery path are explicit. If an
assertion cannot be checked, label it `unknown` rather than filling the gap with a plausible claim.

## Documentation governance

Treat every document visible to an agent as input to the running system. Inventory root
instructions, README files, `docs/`, runbooks, ADRs, plans, reports, examples, generated docs,
Skill references, and archives. For each relevant document establish:

- class: `normative`, `operational`, `reference`, `decision`, `generated`, or `historical`;
- status: `active`, `draft`, `deprecated`, `superseded`, or `archived`;
- owner, applicable scope/version, source of truth, and a semantic revalidation trigger;
- inbound links and AI exposure (root instructions, indexes, Skill links, search/discovery paths).

Do not use file modification time or an old review date alone as proof that content is current.
Verify high-impact claims against code, configuration, manifests, CI, or the owning system. When
sources disagree, do not silently choose the newest prose: record the conflict and the authority
for that claim.

Prevent obsolete documents from influencing AI work:

1. Keep one active canonical document per rule or procedure and update inbound links to it.
2. Mark superseded material at the top with status, reason, date, and `superseded_by`/restore path.
3. Move historical material out of active indexes and normal instruction/reference paths. Archives
   remain evidence, not current guidance.
4. Remove or rewrite executable-looking commands, examples, and prompts that are no longer valid;
   a warning beside a stale example is weaker than deleting it from the active document.
5. Check that active instructions do not link to archived documents except explicitly as history.
6. After a material code/config/workflow change, update coupled docs in the same change or record a
   named owner and tracked gap; never imply undocumented follow-up is complete.

Read [documentation-governance.md](references/documentation-governance.md) for the full audit,
metadata, quarantine, and verification procedure whenever documents can affect agent decisions.

## Instruction and Skill hygiene

Treat an instruction set as an executable interface with a limited context budget:

- Put 2-5 non-negotiable rules first; state the positive action, scope, and exception together.
- Give each rule one canonical home. Replace or merge a matching rule; do not append another
  warning merely because a bad case occurred.
- Resolve tension with explicit scope (`always`, `when`, `only`, `except`) and a precedence order.
- Use tables, numbered steps, and checklists for routing decisions; keep examples compliant with
  the rules they illustrate.
- Keep reference knowledge, schemas, and long examples in linked `references/` files. Load only
  the reference needed for the current mode.
- Set a size/complexity budget for entrypoints. When a change exceeds it, refactor or externalize;
  do not grow the prompt indefinitely. Record what was removed, merged, or archived.
- Keep negative controls: verify that unrelated requests do not route to the Skill, and collision
  cases name the expected composition and prohibited owner.

These are design constraints, not a promise that any model will obey them. Validate behavior with
fresh, recorded trials when runtime routing matters.

## Safe change protocol

Select one reversible increment: correct one stale command, clarify one conflicting rule, merge one
duplicate, add one missing owner, or stage one ablation. For every increment record:

```text
Goal and do-not-do scope:
Observed facts / assumptions / unknowns:
Owner and authorization boundary:
Files and source of truth:
Expected signal and check:
Rollback or restore path:
Evidence layer reached:
```

Preserve credentials, tests, safety controls, and unrelated customizations. Archive retired policy
with reason, date, source revision, and restore path. Avoid mass deletion, broad prompt rewrites,
unbounded automatic appends, and changes that mix implementation with governance.

## Evidence ladder

Report the highest layer actually observed, never a stronger one:

| Layer | Establishes | Does not establish |
|---|---|---|
| static | files, links, frontmatter, manifests, local command shape | installation or runtime use |
| installed | target location and immutable revision | that a host read the file |
| loaded | successful read of the intended Skill/config | instruction following |
| executed | completed trial/command observation | correct routing or deployment |
| target-observed | expected owner loaded and prohibited owner absent | production safety or customer impact |

For Skill changes, use one positive, one negative, and one collision case per owner. Keep raw trial
inputs, revision, terminal result, and loaded-owner evidence together. A test pass is supporting
evidence, not proof of deployment or production behavior.

## Routing and stopping boundaries

- Code or schema implementation -> `engineering-workflow`.
- Diff/MR/PR findings -> `change-review` (findings only, fresh context for re-review).
- Test design or execution -> `test-engineering`.
- Formal report formatting -> `report-writer`.
- Security, data, performance, or browser-specific evidence -> the relevant specialist Skill.

Stop and report when the source/revision is ambiguous, authorization is missing, the rollback path
is unknown for a risky change, or the requested result would require deployment/production writes.
Do not implement from a `change-review` finding list, and do not turn one reversible increment into
a review-fix loop.

## Report contract

```markdown
## Project governance report
- Scope / active revision: ...
- Owner / authority boundary: ...
### Observed
- ...
### Assumptions and unknowns
- ...
### Increment
- Change, expected signal, and rollback: ...
### Evidence
- Highest layer reached; checks and artifacts: ...
### Limits / next gate
- Unverified runtime, target, deployment, or production surfaces: ...
```

## Authoritative references

Read [project-governance-authoritative-sources.md](references/project-governance-authoritative-sources.md)
when selecting controls, explaining the evidence ladder, or reviewing supply-chain/ownership
practice. It maps each recommendation to a primary source and records access dates; do not copy a
standard wholesale into this Skill.
