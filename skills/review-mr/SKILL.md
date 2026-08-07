---
name: review-mr
description: >
  Review current uncommitted, staged, or branch-versus-base Git diffs with parallel specialists
  and consolidated P1, P2, and P3 findings. Use for review MR, PR, or diff, review my changes,
  审查改动, 提交前自查, multi-agent code review, or /review-mr. Review only: do not trigger for
  implementation, generic code explanation, whole-codebase cleanup, or a named gpt55-fusion
  topology. Always compose code review with sonarqube-review plus the applicable general and domain
  review tools; do not wait for the user to name them and do not emulate SonarQube through a generic
  reviewer.
---

# Review MR

You are the Coordinator. Run a Cloudflare-style multi-agent review on the current change set: classify risk, immediately launch all selected specialist reviewers in parallel when multi-agent tooling is available, deduplicate findings, and write one consolidated P1/P2/P3 report to `docs/audit/<branch>-<YYYYMMDD>-mr-review.md`.

`review-mr` owns findings in an existing diff. It does not execute completed-change behavior QA or
turn tests into acceptance evidence; route that work to
[verify-change-evidence](../verify-change-evidence/SKILL.md). Both may be requested in sequence,
but neither replaces the other or grants approval.

When findings and evidence are ready, route presentation to
[report-writer](../report-writer/SKILL.md) and use its engineering review module. `review-mr` retains
finding and severity ownership; `report-writer` owns purpose-based format selection and artifact
structure.

Before launching specialist reviewers, always route a bounded read-only preflight and evidence
lookup to [sonarqube-review](../sonarqube-review/SKILL.md), even when no configuration signal is
initially visible. Keep its quality-gate and issue results in a separate report section. Do not wait
for the user to request SonarQube explicitly. Do not block the rest of the diff review merely because
SonarQube is unconfigured, unreachable, unauthenticated, stale, or has no analysis for the current
branch; mark that evidence source unavailable, partial, or `baseline-only` as appropriate.

## Mandatory review evidence stack

Every review must attempt all applicable evidence channels without waiting for separate user
prompts:

1. `sonarqube-review` for the existing quality gate, measures, and issues, or a labeled unavailable
   result when no usable analysis can be reached;
2. `code-reviewer` for general correctness and maintainability findings;
3. every domain reviewer selected by the changed paths and risk table below;
4. existing repository tests, linters, type checks, or other deterministic review tools that are
   safe and relevant to the changed surface.

Do not install new analyzers or run a new SonarQube scan implicitly. Do not treat one green tool as
approval. Preserve tool provenance and report SonarQube, specialist findings, and executable checks
as separate evidence sections. If a channel cannot run, mark it degraded with the reason and
continue the remaining channels.

## When Not To Use

- The user is asking a generic code question.
- The user wants a single-domain review; use the matching reviewer lens directly.
- The target is not a git repository.

## Collect Inputs

Run these first, preferably in parallel:

```powershell
git rev-parse --abbrev-ref HEAD
git rev-parse --show-toplevel
git status --porcelain
git diff --stat
git log --oneline main..HEAD 2>$null
```

Then collect the actual diff:

- Uncommitted review: `git diff`
- Staged-only review: `git diff --cached`
- Branch review: `git diff main...HEAD`; if `main` is missing, use the user's base branch or the best discovered upstream base

In the same bounded input pass, collect existing SonarQube signals: project-key files, presence of
the documented environment variables without printing values, exposed SonarQube MCP tools, or
repository instructions that identify the project. Signals accelerate target resolution; their
absence does not skip `sonarqube-review` and does not justify a global server search.

If there is no diff, stop with `无可审查的变更`.

## Risk Classification

Pick the highest applicable level:

| Level | Rule | Reviewers |
|-------|------|-----------|
| `trivial` | Total diff lines <= 50 and all changed files are `docs/**`, `*.md`, non-secret `*.json`, or pure comment blocks | `code-reviewer`, `docs-writer` |
| `lite` | Total diff lines <= 300 and changes span <= 2 first-level domains | `code-reviewer` plus domain-specific reviewers |
| `full` | Everything else, or >= 3 domains, or > 300 lines, or sensitive code paths | all reviewers |

A domain is the first-level directory under the repo root. `*/Sql/*` counts as its own domain regardless of parent.

Sensitive paths always force `full`: tax-control, invoice, voucher, permission, finance, payment, write-off, authentication, authorization, migration, destructive SQL, production config, credentials, and external integration signing/status writeback.

Domain-specific reviewers for `lite`:

- SQL files or migration scripts: `db-reviewer`
- Controllers, services, repositories, DTO/entity boundaries: `architect`
- Tests or missing tests around production changes: `test-engineer`
- UI files: `ui-ux-reviewer`
- Third-party API/integration paths: `api-integration-reviewer`
- Auth, permissions, secrets, external input: `security-reviewer`
- Hot paths, batch jobs, large queries, reports: `performance-reviewer`

## Reviewer Execution

The main advantage of `review-mr` is parallel specialist review. After risk classification, immediately dispatch every selected reviewer as a separate child agent in one parallel wave when multi-agent tooling is available. Keep the Coordinator in the parent thread; the Coordinator does not perform specialist review until child results return.

If the runtime exposes a multi-agent tool, use it. Do not replace parallel dispatch with a single broad review. Sequential reviewer emulation is only a degraded fallback when multi-agent tooling is absent, disabled, or fails after a real attempt.

When running child agents, pass each reviewer:

- repository root
- branch name
- risk level
- changed file/stat summary
- relevant diff, truncated only when necessary
- path to `.claude/ai-workflows/agents/<reviewer>.md` when present
- the instruction to return only P1/P2/P3 findings with file:line, impact, and fix

If any child agent fails or returns empty, mark only that reviewer as degraded and continue aggregating the successful reviewers.

For each reviewer, load the project agent file when present:

```text
.claude/ai-workflows/agents/<reviewer>.md
```

If the project agent file is missing, use the inline fallback role below. Reviewers must only report changed-code issues with evidence, and each finding should include file:line, impact, and the smallest safe fix.

### Inline Fallback Roles

- `code-reviewer`: null/exception/concurrency/state/transaction risks; validation and error returns; logging adequacy; critical branch test coverage.
- `db-reviewer`: N+1, missing indexes, transaction scope, migration rollback plan, destructive SQL, data repair safety.
- `test-engineer`: whether tests reproduce the issue, cover success/failure/edge paths, and capture command, exit code, and key logs.
- `security-reviewer`: auth entry, permission checks, secrets, log redaction, SQL injection, unsafe external input, credential handling.
- `performance-reviewer`: hot loops, allocations, query plans, cache use, batch vs single-record behavior.
- `architect`: module boundaries, DTO/entity/service/repository responsibility split, existing patterns, rollback path, long-term design debt.
- `api-integration-reviewer`: third-party signatures, timestamp/nonce handling, idempotency, status writeback, timeout/retry behavior.
- `ui-ux-reviewer`: viewport coverage, interaction state, accessibility, empty/error/loading states.
- `docs-writer`: README/API/doc/comment accuracy, durable decision records, stale guidance.

## Aggregation

After all reviewer passes return:

1. Deduplicate by changed file and line; note all contributing reviewers.
2. Reclassify severity:
   - P1: correctness bug, security hole, data loss risk, broken contract, missing rollback plan on destructive change.
   - P2: test gap on changed code, observability hole, medium-risk refactor, misleading naming, maintainability issue with real cost.
   - P3: style, minor optimization, doc nit, optional refactor.
3. Downgrade over-rated findings; a typo is never P1.
4. Upgrade only when multiple independent reviewers identify the same concrete risk.
5. Prefer Chinese output in Chinese repositories.

## Report

Use `report-writer` to write the consolidated evidence. Default to
`docs/audit/<branch>-<YYYYMMDD>-mr-review.md` for a repository-native audit trail. When the intended
use requires a spreadsheet, PDF, HTML, Word, or slides, preserve the same basename with the selected
extension and use the corresponding artifact Skill. Use UTC date in the filename and local time in
the body. Create `docs/audit/` if needed. If the file exists, append `-<seq>` starting at 2.

Use this template:

```markdown
# MR Review - <branch> <YYYY-MM-DD HH:mm local>

- 风险等级: <trivial|lite|full>
- 改动行数: <N>（新增 <X> / 删除 <Y>）
- 改动文件: <F>
- 涉及领域: <domain list>
- 调用的 reviewer: <names>
- 模式: 正常 / degraded（缺 <names>）

## P1（必须修复）

1. `<file>:<line>` - <问题>
   - 影响: <concrete consequence>
   - 建议: <fix or follow-up>
   - 来源: <reviewer>[, <reviewer>]

## P2（应该修复）

...

## P3（建议改进）

...

## 各 reviewer 摘要

### code-reviewer
- 命中: <count>
- 关键问题: <one-line summary>

## Coordinator 结论

- 是否建议保留改动: 是 / 否 / 有条件
- 阻塞项: <P1 list, or "无">
- 人工确认点（财务/税控/权限相关）: <list, or "无">

## 后续动作

- [ ] 修复 P1
- [ ] 补充 P2 测试
- [ ] 重新跑 review-mr 验证
```

After writing, report:

```text
MR Review 报告已写入: <absolute path>
风险等级: <level>
P1: <n>  P2: <n>  P3: <n>
阻塞项: <count> 个
是否建议保留: <是/否/有条件>
```

## Error Handling

| Failure | Action |
|---------|--------|
| Not a git repo | Abort with `当前目录不是 git 仓库，review-mr 不可用` |
| Empty diff | Abort with `无可审查的变更` |
| Multi-agent tool unavailable | Mark sequential mode; still run every selected reviewer lens |
| Reviewer returns empty or errors | Mark degraded mode; list missing reviewers in the report; still produce a partial report |
| `docs/audit/` creation fails | Abort with the OS error |
| Report writer unavailable | Use the Markdown fallback template, mark presentation degraded, and do not omit the report |
| Reviewer agent spec missing and no inline fallback applies | Skip that reviewer and mark degraded |

## Boundaries

- Do not post to GitHub/GitLab, approve, merge, push, or publish review results unless explicitly requested.
- Do not edit project-level reviewer agent files during a review.
- Do not add config files for this skill.
- Do not run destructive database operations.
- For finance, tax-control, invoice, payment, write-off, and permission changes, include explicit human confirmation points.
