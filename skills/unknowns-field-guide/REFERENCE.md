# Unknowns Field Guide — Reference

Detailed procedures, prompt templates, and output formats for each sub-workflow. Keep routing logic in [SKILL.md](SKILL.md); keep reusable operational templates here.

---

## Unknown categories

Before any step, classify information into one of four buckets. Do this consistently across the whole workflow.

| Category | Definition | Examples |
|----------|------------|----------|
| **Known Knowns** | Already explicit and confirmed | Goal, named files, stated interface constraints, stated business rules |
| **Known Unknowns** | Aware of a gap; needs confirmation | Field source unclear, state boundaries unclear, historical compatibility unclear, schema changes unclear |
| **Unknown Knowns** | User has criteria they didn't state; only visible once a proposal is on the table | Code style preference, business term preference, what fallback code to keep, internal notes customer shouldn't see |
| **Unknown Unknowns** | Hidden pitfalls, alternatives, latent constraints, history | Old snapshot blocks new schema, re-push merges multiple tickets, status callback only updates first row, an unrelated scheduler also depends on this code |

A good workflow converts the unknowns that can change the implementation into Known Knowns before coding. It does not need to exhaust every possible question.

## Artifact scale

Use the smallest durable surface that still preserves reviewability:

| Task size | Artifact style |
|-----------|----------------|
| Small localized edit | Inline blindspot summary, inline plan, final review in the response |
| Medium task touching multiple files | Inline blindspot summary plus structured plan; notes only for deviations or new findings |
| Deep-path task | Structured blindspot report, plan, implementation notes, and post-implementation review |
| User asks for read-only analysis | Stop after the requested analysis or plan; do not implement |

---

## 1. blindspot-pass

**Purpose**: Discover unknown unknowns before coding.

**Use when**:
- Task touches business flow, historical data, state machines, integrations, batch fixes, scheduled tasks, finance, inventory, or invoicing.
- User gave only a goal; full boundaries are missing.
- Modifying existing code, not isolated new files.

**Inputs**:
- `task_description` — what the user asked
- `known_files_or_modules` — paths/classes/methods named by user
- `user_constraints` — explicit constraints and non-goals
- `existing_docs_optional` — any docs the user pointed to

**Procedure**:

1. **Restate the task** in 3–5 sentences. Do not start implementing.
2. **List Known Knowns** — only facts confirmed by the user or visible in inspected evidence.
3. **List Known Unknowns** — gaps you noticed that need confirmation.
4. **List Unknown Knowns** — likely criteria the user has but hasn't said.
5. **Find Unknown Unknowns** — actively probe for: historical snapshot drift, idempotency, retry/merge behavior, state rollback, concurrent writes, transaction boundaries, permission scope, log/seam gaps, downstream consumers.
6. **Mark risk priority** P0/P1/P2. P0 blocks implementation only when it cannot be discovered locally and has no safe default.

**Output format (markdown)**:

```markdown
# Blindspot Report

## 1. Task Restatement
<3–5 sentences>

## 2. Known Knowns
- <fact>: <evidence pointer>

## 3. Known Unknowns
- <question>: <why it matters>

## 4. Unknown Knowns (suspected criteria)
- <criterion>: <why you think it matters>

## 5. Unknown Unknowns (potential blindspots)
- <risk>: <where in code/data it could bite>

## 6. P0 / P1 / P2 Risk Ranking
- P0 — must resolve before coding: ...
- P1 — should resolve or document safe default: ...
- P2 — nice to resolve: ...

## 7. Pre-implementation must-confirms
- ...
```

**Success criteria**:
- Never produces implementation code.
- Surfaces at least 5 candidate blindspots across categories.
- Distinguishes facts from guesses from unconfirmed questions.
- Marks P0 only for risks that can change the implementation or corrupt behavior/data.

**Prompt template**:

```text
Run blindspot-pass. Do not write code.

Task:
{{task_description}}

Known files/modules:
{{known_files_or_modules}}

Constraints:
{{user_constraints}}

Optional docs:
{{existing_docs_optional}}

Output:
1. Task restatement
2. Known Knowns
3. Known Unknowns
4. Unknown Knowns
5. Unknown Unknowns
6. P0/P1/P2 ranking
7. Pre-implementation must-confirms
```

---

## 2. reverse-interview

**Purpose**: Interview the user only for gaps that change implementation direction and cannot be resolved from local evidence.

**Use when**:
- blindspot-pass surfaced P0/P1 unknowns.
- The request is short but the blast radius is large.
- Multiple viable paths exist and the choice depends on business criteria.

**Inputs**:
- `blindspot_report` — output from step 1
- `task_description`

**Procedure**:

1. **Compress questions** — only ask things that would change the implementation.
2. **Order by impact** — architecture, data, integration, state, historical compatibility come first.
3. **Provide a default assumption** for every question when a safe default exists.
4. **Mark the risk** of proceeding on the default.
5. **Proceed without asking** when code, docs, tests, logs, schemas, or runtime state can answer the question cheaply.

**Output format (markdown)**:

```markdown
# Reverse Interview

## Must-confirm questions
### Q1. <question>
- Why it matters: <impact on design>
- Default assumption: <what we'd do if you don't answer>
- Risk if default is wrong: <concrete consequence>

### Q2. ...

## Minimum safe plan if no answers
<smallest change that preserves invariants, or "blocked" if no safe default exists>
```

**Success criteria**:
- Maximum 7 questions.
- Each question explains why it matters.
- Each question has a default assumption and a stated risk when a safe default exists.
- No question repeats what the user already answered.
- No question asks for information that local evidence can provide.

**Prompt template**:

```text
Run reverse-interview.

Task:
{{task_description}}

Blindspot report:
{{blindspot_report}}

For each question include:
- Question
- Why it matters
- Default assumption
- Risk if default is wrong
```

---

## 3. implementation-plan

**Purpose**: Produce an executable, auditable, rollback-able plan after unknowns are processed.

**Use when**:
- blindspot-pass completed.
- P0 unknowns are confirmed (or have safe defaults).
- About to start modifying code.

**Inputs**:
- `task_description`
- `confirmed_assumptions` — answers from reverse-interview, plus any defaults the user accepted
- `code_findings` — relevant code seams you actually inspected
- `constraints` — explicit do-not-do boundaries

**Procedure**:

1. **Define the goal** — what this change achieves, and what it explicitly does not.
2. **Scope the change** — list files, classes, interfaces, tables, configs, tests, or explicitly say "none" for irrelevant categories.
3. **Split into smallest verifiable units** — never lump everything into one step.
4. **Design validation per step** — every step has a check; prefer the narrowest command or manual surface that exercises the changed behavior.
5. **Design rollback** — for any data, integration, or batch change, write the rollback or backup plan.
6. **Mark human-review points** — anything requiring business sign-off, SQL review, state-flow review, or external behavior review.

**Output format (markdown)**:

```markdown
# Implementation Plan

## 1. Goal
<what success looks like>

## 2. Do-not-do scope
<explicit non-goals to prevent scope creep>

## 3. Key assumptions
<defaults or confirmed answers that drive the plan>

## 4. Affected scope
- Files:
- Classes/Interfaces:
- Tables/Views:
- Configs:
- Tests:

## 5. Implementation steps
### Step 1. <name>
- Files: ...
- Change: ...
- Validation: ...

### Step 2. ...

## 6. Validation plan
| Step | Validation command / check | Expected result |
|------|---------------------------|-----------------|

## 7. Rollback / backup plan
<what to back up, restore, or revert>

## 8. Human-review points
- <business owner / DBA / on-call / etc.>: <what they must confirm>
```

**Success criteria**:
- Every step is independently verifiable.
- "Do-not-do" scope is explicit and not aspirational.
- Rollback or backup exists for any non-trivial data change.
- Human-review points are named (not just "ask the team").
- Plan alone is enough for a reviewer to approve or reject.

**Prompt template**:

```text
Run implementation-plan. Do not write code yet.

Task:
{{task_description}}

Confirmed assumptions:
{{confirmed_assumptions}}

Code findings:
{{code_findings}}

Constraints:
{{constraints}}

Output:
1. Goal
2. Do-not-do scope
3. Key assumptions
4. Affected scope
5. Implementation steps
6. Validation plan
7. Rollback / backup plan
8. Human-review points
```

---

## 4. implementation-notes

**Purpose**: Capture execution-time reality — deviations, new findings, edge cases, validations — while the work is in progress.

**Use when**:
- `deep_path` is active.
- The task has more than 3 implementation steps.
- Code touches legacy logic, historical data, integrations, or state transitions.
- Actual implementation deviates from the plan or discovers new P0/P1 unknowns.

**Inputs**:
- `implementation_plan`
- `current_diff`
- `new_findings`

**Output file**: `implementation-notes.md` when a durable artifact is warranted. For small default-path work, inline notes are acceptable if there were no deviations and no new high-risk findings.

**Procedure**:

1. **Initialize or open** `implementation-notes.md`, or keep inline notes for a small no-deviation task.
2. **Record each completed step** with files, intent, and validation method.
3. **Record deviations from plan** — what changed, why, what risk it introduces.
4. **Record new findings** — newly discovered unknowns, historical-compat issues, edge cases.
5. **Record human-review items** — anything that cannot be auto-verified.

**Output template**:

```markdown
# Implementation Notes

## Task
{{task_summary}}

## Original Plan
{{plan_summary}}

## Changes Made
- {{file}}: {{change_summary}}

## Deviations From Plan
- {{deviation}}
  - Reason: {{reason}}
  - Risk: {{risk}}

## New Findings
- {{finding}}

## Edge Cases Considered
- {{edge_case}}

## Validation Performed
- {{validation_item}}: {{result}}

## Needs Human Review
- {{review_item}}

## Remaining Risks
- {{risk_item}}
```

**Success criteria**:
- Any deviation is recorded with reason and risk.
- Anything not auto-verifiable enters the human-review list.
- A reviewer reading only `implementation-notes.md` can understand why each change was made.

**Prompt template**:

```text
Run implementation-notes. Update implementation-notes.md.

Record:
1. Changes made (file + summary)
2. Deviations from plan
3. Reason for deviation
4. New edge cases found
5. Validations performed
6. Items needing human review
7. Remaining risks
```

---

## 5. post-implementation-review

**Purpose**: Produce a reviewer-ready artifact explaining the change, its risks, validation, and a comprehension quiz.

**Use when**:
- Code changes are complete.
- About to commit, merge, hand off, or send to a reviewer.

**Inputs**:
- `final_diff`
- `implementation_notes`
- `test_results`
- `task_description`

**Procedure**:

1. **Explain the change** in both business and technical language.
2. **Verify against original goals** — for each stated goal, say whether it was met.
3. **Expose remaining risks** — what's uncovered, untested, or human-dependent.
4. **Generate a reviewer checklist** — concrete, checkable items.
5. **Generate a quiz** — 3–7 questions for normal work, 5–10 for deep-path work, to verify the developer or AI actually understood the change.

**Output format (markdown)**:

```markdown
# Post-Implementation Review

## 1. Change Summary
<plain-language summary>

## 2. Business Impact
<what changes for users / business / operations>

## 3. Technical Implementation
<how the code achieves it; key files and decisions>

## 4. Validation Results
| Check | Result | Notes |
|-------|--------|-------|

## 5. Uncovered Risks
- <risk>: <why it remains open>

## 6. Reviewer Checklist
- [ ] Goal X verified
- [ ] Do-not-do scope honored
- [ ] <domain> invariants respected
- [ ] Rollback path understood
- [ ] ...

## 7. Comprehension Quiz
1. <question>
2. ...
```

**Success criteria**:
- Does not just repeat the diff.
- Explains *why* each change was made.
- States explicitly what was *not* done.
- Contains a concrete, clickable reviewer checklist.
- Contains quiz questions proportional to the task risk that a real developer should be able to answer.

**Prompt template**:

```text
Run post-implementation-review.

Task:
{{task_description}}

Final diff:
{{final_diff}}

Implementation notes:
{{implementation_notes}}

Test results:
{{test_results}}

Output:
1. Change summary
2. Business impact
3. Technical implementation
4. Validation results
5. Uncovered risks
6. Reviewer checklist
7. Comprehension quiz
```

---

## End-to-end example (compressed)

```text
User: "Fix tax-control re-push merging multiple invoices into one."

Step 1 — blindspot-pass:
  P0: confirm whether the third-party endpoint has a de-merge call.
  P0: confirm whether historical snapshot already has merged tickets.
  P1: confirm idempotency window.
  → Output: 6 blindspots, 2 P0s.

Step 2 — reverse-interview:
  Q1. Is de-merge available? Default: assume no → block re-push when merged.
  Q2. Are merged tickets allowed historically? Default: preserve as-is.
  → Output: 2 confirmed-or-defaulted questions.

Step 3 — implementation-plan:
  Goal: block re-push when snapshot shows merged ticket.
  Do-not-do: don't touch historical snapshots, don't change DTO surface.
  Steps: 4 (inspect snapshot shape → guard in service → unit test → integration test).
  Rollback: revert guard flag, no data change.
  Human-review: business sign-off before guard is enabled in prod.

Step 4 — implementation-notes (during coding):
  - File: ImTaxControlService.cs — added guard before push.
  - Deviation: had to inspect two extra snapshot columns. Reason: original plan assumed one.
  - Validation: unit + integration both green.

Step 5 — post-implementation-review:
  Summary, impact, validation table, 4 risks, 8-item checklist, 6 quiz Qs.
```

---

## Routing cheat sheet

```text
Trivial change (copy/log/UI tweak)        → fast_path
Normal coding task                        → default
Finance / tax / invoicing / contracts
  / external API / batch SQL
  / scheduled task / state machine
  / customer-visible artifact             → deep_path
```
