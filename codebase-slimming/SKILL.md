---
name: codebase-slimming
description: Structured workflow for reducing duplicated, bloated, AI-generated, temporary-patch, or dangerous code without changing behavior. Use when the user asks to slim a codebase, reduce effective code lines, replace dangerous implementations, remove duplicate logic, or create a staged behavior-preserving cleanup plan with baselines, QA checks, suitability decisions, progress tracking, and rollback criteria.
---

# Codebase Slimming

在功能行为完全不变的前提下，对代码库进行结构化瘦身，减少重复实现、临时补丁、危险抽象、自制框架和不可维护代码。

本 Skill 不追求“看起来行数更少”，而是追求：

1. 行为可验证。
2. 结构更清晰。
3. 重复逻辑更少。
4. 模块边界更稳定。
5. 后续 AI / 人工继续开发时不容易重新失控。

## Core Principles

### 先建立测试和行为基线，再改代码

禁止在没有行为基线的情况下直接重构。

重构前必须先完成：

- 页面 / 接口 / 命令 / 定时任务 / 后台任务清单。
- 关键业务流程清单。
- 现有自动化测试结果。
- 缺失测试的补充方案。
- 可人工验收的 QA 检查清单。
- 当前代码行数、重复逻辑、复杂模块、危险实现的基线统计。

如果没有测试，必须先补行为保护，而不是直接瘦身。

### 先初步分析，不适合就终止

必须先做初步评估。如果判断项目无法有效改善，必须直接终止评估，并说明原因。

常见终止条件：

- 项目无法正常构建或运行，且短时间内无法恢复。
- 关键业务行为无人能解释，也没有可验证数据。
- 没有测试、没有验收清单、没有接口样例，且无法补齐。
- 项目本身规模很小，瘦身收益低于风险。
- 主要问题不是代码冗余，而是需求不清、数据错误、架构方向错误或业务模型错误。
- 用户只要求压缩行数，不接受测试、基线和分阶段验证。
- 需要大范围重写核心业务，但没有足够业务上下文。

终止时必须输出：

```text
评估结论：不建议继续代码瘦身
主要原因：
1. ...
2. ...
3. ...

可替代建议：
1. ...
2. ...
```

### 适合重构时，必须明确承诺缩减目标

如果项目适合重构，必须给出明确、可度量的代码缩减目标。

目标格式：

```text
在功能完全不变、测试和验收清单全部通过的前提下，
将有效代码行数从 X 行缩减到 Y 行，
预计缩减 Z%。
```

注意：

- 目标必须基于初步分析后的证据。
- 不允许在未分析前随意承诺比例。
- 不允许只为了达到目标而删除注释、压缩格式、合并无关逻辑。
- 不允许为了减少行数牺牲可读性、可测试性和模块边界。

### 禁止代码高尔夫式压缩

严禁通过以下方式完成瘦身目标：

- 删除有价值注释。
- 把多行清晰逻辑压缩成一行。
- 使用晦涩语法、炫技写法、过度链式调用。
- 为了减少文件数而合并无关模块。
- 为了减少行数而牺牲命名清晰度。
- 把显式业务规则隐藏到复杂表达式中。
- 用反射、动态调用、字符串拼接等方式绕开类型检查。
- 把重复代码改成更难理解的万能函数。
- 将业务差异强行抽象成难以维护的配置黑盒。

瘦身后的代码必须比原代码更容易阅读，而不是更难。

### 逐步替换危险实现

不要一次性推倒重来。优先采用“包围、验证、替换、删除”的方式：

1. 找到危险实现。
2. 提取其真实行为。
3. 建立测试或验收用例。
4. 用清晰实现替换。
5. 对比旧行为。
6. 删除旧实现。
7. 更新进度记录和防回归规则。

危险实现包括：

- 重复复制的业务逻辑。
- 多套日期 / 金额 / 税率 / 状态转换规则。
- 自制框架。
- 临时补丁堆叠。
- 无边界的工具类。
- 大型 God Class / God Service。
- 跨模块直接访问内部数据。
- 隐式副作用。
- 魔法字符串和魔法状态码。
- 无测试保护的核心流程。
- AI 生成但无人审查的代码。

## Dedicated Progress Folder

所有瘦身过程必须放入独立目录管理。

默认目录：

```text
.codebase-slimming/
```

目录结构：

```text
.codebase-slimming/
  00-intake.md
  01-initial-assessment.md
  02-behavior-baseline.md
  03-code-metrics.md
  04-suitability-decision.md
  05-reduction-target.md
  06-refactor-plan.md
  07-progress-log.md
  08-risk-register.md
  09-qa-checklist.md
  10-regression-report.md
  11-final-report.md

  baselines/
    build-result.txt
    test-result.txt
    api-samples/
    page-snapshots/
    command-outputs/
    database-snapshots/
    scc-before.json
    scc-after.json

  decisions/
    ADR-0001.md
    ADR-0002.md

  guardrails/
    CLAUDE.md
    AGENTS.md
    lint-rules.md
    ci-checks.md
    code-review-checklist.md

  modules/
    module-name-001.md
    module-name-002.md
```

禁止把进度记录散落在聊天、临时文件或代码注释中。

## Workflow

### Phase 0: Intake

先记录项目基本信息。

输出到：

```text
.codebase-slimming/00-intake.md
```

必须包含：

```markdown
# Intake

## Repository

- Name:
- Path:
- Main language:
- Framework:
- Runtime:
- Database:
- Build command:
- Test command:
- Start command:

## Business Scope

- Main product:
- Core users:
- Core workflows:
- Critical modules:

## User Goal

- Why slimming is needed:
- Current pain:
- Expected outcome:

## Hard Constraints

- Must not change:
- Must preserve:
- External integrations:
- Database compatibility:
- API compatibility:
- UI compatibility:
```

### Phase 1: Initial Assessment

先分析，不直接修改代码。

输出到：

```text
.codebase-slimming/01-initial-assessment.md
```

必须检查：

- 项目是否能构建。
- 项目是否能运行。
- 测试是否存在。
- 核心入口是否清晰。
- 模块边界是否清晰。
- 是否存在明显重复实现。
- 是否存在 AI 代码膨胀痕迹。
- 是否存在高风险业务逻辑。
- 是否存在不可替换的历史兼容逻辑。
- 是否有足够样例可以建立行为基线。

建议使用的分析维度：

```text
1. 构建健康度
2. 测试健康度
3. 代码重复度
4. 模块边界
5. 业务规则显式程度
6. 危险实现数量
7. 可验证性
8. 瘦身收益
9. 重构风险
10. 是否适合继续
```

### Phase 2: Code Metrics Baseline

使用工具统计有效代码行数。默认推荐使用 `scc`。

输出到：

```text
.codebase-slimming/03-code-metrics.md
.codebase-slimming/baselines/scc-before.json
```

统计口径：

- 只统计有效代码行。
- 不把删除注释作为瘦身成果。
- 不把空行变化作为瘦身成果。
- 不把格式压缩作为瘦身成果。

记录格式：

```markdown
# Code Metrics Baseline

## Tool

- Tool: scc
- Date:
- Command:

## Before

| Language | Files | Code Lines | Comment Lines | Blank Lines |
|---|---:|---:|---:|---:|
| C# | | | | |
| TypeScript | | | | |
| SQL | | | | |
| Total | | | | |

## Excluded Paths

- bin/
- obj/
- node_modules/
- dist/
- build/
- generated/
- migrations/only-if-generated
```

### Phase 3: Behavior Baseline

正式修改代码前，必须建立行为基线。

输出到：

```text
.codebase-slimming/02-behavior-baseline.md
.codebase-slimming/09-qa-checklist.md
```

行为基线至少包括：

```markdown
# Behavior Baseline

## Build Baseline

- Build command:
- Result:
- Errors:
- Warnings:

## Test Baseline

- Test command:
- Passed:
- Failed:
- Skipped:

## API Baseline

| API | Method | Input Sample | Expected Output | Status |
|---|---|---|---|---|

## UI Baseline

| Page | Main Behavior | Verification Method | Status |
|---|---|---|---|

## Business Workflow Baseline

| Workflow | Steps | Expected Result | Verification Method |
|---|---|---|---|

## Data Baseline

| Scenario | Input Data | Expected Data Change | Verification |
|---|---|---|---|

## Known Existing Bugs

| Bug | Existing Behavior | Must Preserve? | Notes |
|---|---|---|---|
```

原则：

- 已知旧 bug 要记录清楚。
- 不要把旧 bug 当作重构引入的问题。
- 但也不要在瘦身中顺手修业务 bug，除非用户明确要求。
- 代码瘦身默认目标是行为不变。

### Phase 4: Suitability Decision

完成初步分析后，必须做继续 / 终止决策。

输出到：

```text
.codebase-slimming/04-suitability-decision.md
```

模板：

```markdown
# Suitability Decision

## Decision

继续 / 终止

## Summary

一句话说明是否适合代码瘦身。

## Evidence

| Evidence | Observation | Impact |
|---|---|---|

## Main Risks

| Risk | Severity | Mitigation |
|---|---|---|

## Final Judgment

如果继续：

本项目适合进行代码库瘦身，因为：
1. ...
2. ...
3. ...

如果终止：

本项目不适合继续代码库瘦身，因为：
1. ...
2. ...
3. ...

建议改为：
1. ...
2. ...
```

### Phase 5: Reduction Target

只有在判断适合继续后，才能设置缩减目标。

输出到：

```text
.codebase-slimming/05-reduction-target.md
```

模板：

```markdown
# Reduction Target

## Baseline

- Current effective code lines:
- Measurement tool:
- Measurement date:

## Target

在功能完全不变、测试和 QA 检查清单全部通过的前提下，
将有效代码行数从 `X` 行缩减到 `Y` 行，
目标缩减 `Z%`。

## Scope Included

- Module A
- Module B
- Module C

## Scope Excluded

- Generated code
- Third-party code
- Migrations
- Historical archive
- Vendor directory

## Non-Negotiable Rules

1. 不删除有价值注释来制造缩减。
2. 不使用代码高尔夫式压缩。
3. 不降低可读性。
4. 不改变外部 API 行为。
5. 不改变数据库兼容性。
6. 不改变用户可见行为。
7. 不绕过测试。
8. 不隐藏业务规则。
```

### Phase 6: Refactor Plan

输出到：

```text
.codebase-slimming/06-refactor-plan.md
```

重构计划必须按模块拆分，不允许一次性大爆炸修改。

模板：

```markdown
# Refactor Plan

## Strategy

采用分阶段、可回滚、行为保持的瘦身方式。

## Module Plan

| Order | Module | Problem | Action | Expected Reduction | Risk | Baseline Required |
|---:|---|---|---|---:|---|---|
| 1 | | | | | | |
| 2 | | | | | | |

## Refactor Patterns

### Merge Duplicate Logic

适用于：

- 多套日期格式化。
- 多套金额计算。
- 多套状态转换。
- 多套 API 参数组装。
- 多套校验逻辑。

要求：

- 先列出所有重复实现。
- 对比行为差异。
- 抽出统一实现。
- 为差异保留明确配置或策略。
- 删除旧实现。

### Replace Homegrown Framework

适用于：

- 自制路由。
- 自制依赖注入。
- 自制状态管理。
- 自制日期 / 金额 / 权限 / 校验框架。

要求：

- 先确认自制框架的真实行为。
- 只替换无业务差异的部分。
- 对历史兼容行为建立测试。
- 禁止为了“用库”而引入更复杂依赖。

### Extract Actual Behavior Then Rewrite

适用于：

- 已经不可维护的模块。
- 大量补丁叠加的逻辑。
- 无法安全局部修改的危险实现。

要求：

- 先提炼行为。
- 写行为测试。
- 新实现并行验证。
- 通过后替换入口。
- 最后删除旧实现。
```

### Phase 7: Progress Management

每一次瘦身修改都必须记录进度。

输出到：

```text
.codebase-slimming/07-progress-log.md
```

模板：

```markdown
# Progress Log

## Entry Template

### YYYY-MM-DD / Step N

## Target

本次处理的模块：

## Before

- Files:
- Effective code lines:
- Main problems:

## Action

- 合并了：
- 删除了：
- 替换了：
- 保留了：

## After

- Files:
- Effective code lines:
- Reduction:
- Tests:

## Behavior Verification

- Build:
- Unit tests:
- Integration tests:
- Manual QA:
- API checks:

## Risk Notes

- Risk:
- Mitigation:

## Decision

继续 / 回滚 / 暂停
```

### Phase 8: Regression Check

每个阶段结束后必须做回归检查。

输出到：

```text
.codebase-slimming/10-regression-report.md
```

必须检查：

- 构建是否通过。
- 自动化测试是否通过。
- 关键页面是否正常。
- 核心接口是否兼容。
- 数据库读写是否兼容。
- 外部系统调用是否兼容。
- 日志是否仍可追踪。
- 错误处理是否没有被吞掉。
- 性能是否没有明显退化。
- 删除的代码是否确实无引用、无行为损失。

模板：

```markdown
# Regression Report

## Summary

- Date:
- Commit:
- Result:

## Checks

| Check | Result | Evidence |
|---|---|---|
| Build | | |
| Unit Tests | | |
| Integration Tests | | |
| API Compatibility | | |
| UI Behavior | | |
| Database Compatibility | | |
| External Integrations | | |
| Logs / Observability | | |
| Performance Smoke Test | | |

## Failed Checks

| Check | Failure | Fix / Decision |
|---|---|---|

## Conclusion

通过 / 不通过 / 需要回滚
```

### Phase 9: Engineering Guardrails

瘦身完成后，必须添加防止代码重新膨胀的工程护栏。

输出到：

```text
.codebase-slimming/guardrails/
```

至少包括：

```text
CLAUDE.md
AGENTS.md
lint-rules.md
ci-checks.md
code-review-checklist.md
```

护栏必须覆盖：

- 禁止重复实现已有逻辑。
- 新增功能前必须搜索已有模块。
- 新增工具函数前必须证明没有现成实现。
- 禁止无测试修改核心业务。
- 禁止绕开模块边界。
- 禁止为局部修复引入全局副作用。
- 禁止 AI 在没有人工确认的情况下重写核心模块。
- 每次 AI 修改后必须运行构建、测试和关键检查。
- 大型改动必须拆成小 PR / 小提交。
- 删除代码必须说明行为等价证据。

## Required Output Format

每次执行本 Skill，必须按以下顺序输出：

```markdown
# 代码库瘦身执行报告

## 1. 当前阶段

Intake / Initial Assessment / Baseline / Suitability Decision / Refactor / Regression / Final

## 2. 本次结论

继续 / 终止 / 暂停 / 回滚

## 3. 关键发现

1. ...
2. ...
3. ...

## 4. 行为基线状态

- Build:
- Tests:
- API:
- UI:
- Data:

## 5. 代码规模状态

- Before:
- Current:
- Target:
- Reduction:

## 6. 风险

| Risk | Severity | Mitigation |
|---|---|---|

## 7. 下一步

1. ...
2. ...
3. ...
```

## Final Report

完成后输出：

```text
.codebase-slimming/11-final-report.md
```

模板：

```markdown
# Final Codebase Slimming Report

## Summary

在功能行为保持不变的前提下，完成代码库瘦身。

## Target vs Actual

| Metric | Before | Target | Actual |
|---|---:|---:|---:|
| Effective code lines | | | |
| Files | | | |
| Duplicate implementations | | | |
| Dangerous modules | | | |

## Reduction Result

- Target reduction:
- Actual reduction:
- Completion ratio:

## Behavior Verification

| Check | Result |
|---|---|
| Build | |
| Unit Tests | |
| Integration Tests | |
| QA Checklist | |
| API Compatibility | |
| UI Compatibility | |
| Database Compatibility | |

## Major Changes

1. ...
2. ...
3. ...

## Removed / Replaced Dangerous Implementations

| Old Implementation | New Implementation | Reason |
|---|---|---|

## Guardrails Added

1. CLAUDE.md
2. AGENTS.md
3. Lint rules
4. CI checks
5. Code review checklist

## Remaining Risks

| Risk | Recommendation |
|---|---|

## Maintenance Recommendations

1. 新增功能前先搜索已有实现。
2. 每次 AI 修改必须附带测试或验收证据。
3. 每周检查重复逻辑和无用代码。
4. 每个核心模块必须有明确负责人或边界说明。
5. 禁止让 Agent 单独决定架构级变更。
```

## Decision Rules

### Continue

满足以下条件时继续：

- 项目可以构建或可快速恢复构建。
- 核心行为可以被测试或人工验收。
- 重复逻辑明显。
- 危险实现可以逐步替换。
- 用户接受行为基线优先。
- 用户接受不使用代码高尔夫式压缩。
- 预估收益明显高于风险。

### Stop

满足以下条件时停止：

- 无法建立行为基线。
- 无法确认核心业务规则。
- 缩减目标只能靠删除注释或压缩格式完成。
- 重构风险高于收益。
- 用户要求跳过测试直接删代码。
- 项目真正问题不是代码膨胀。
- 代码已经足够小，瘦身没有实际价值。

### Roll Back

满足以下条件时回滚：

- 构建失败且无法快速修复。
- 测试出现非预期回归。
- 核心业务流程行为变化。
- API 兼容性被破坏。
- 数据库读写行为变化。
- 新实现比旧实现更难理解。
- 抽象过度，导致维护成本上升。

## Agent Behavior Rules

AI 可以做：

- 搜索重复代码。
- 生成统计报告。
- 整理行为清单。
- 建议重构方案。
- 编写测试。
- 提交小范围重构补丁。
- 更新进度文件。
- 运行构建和测试。
- 生成最终报告。

AI 不可以做：

- 在无基线情况下直接大规模删除代码。
- 单独决定核心架构替换。
- 隐藏行为差异。
- 为达成行数目标牺牲可读性。
- 删除注释制造成果。
- 把代码压缩成难读形式。
- 一次性重写大模块。
- 忽略测试失败。
- 把已知回归标记为成功。

最终决策必须由工程师确认，Agent 没有最终投票权。

## Quality Bar

瘦身后的代码必须满足：

1. 更少重复。
2. 更少危险实现。
3. 更清晰命名。
4. 更明确模块边界。
5. 更容易测试。
6. 更容易调试。
7. 更容易继续开发。
8. 行为与原系统一致。
9. 代码行数真实减少。
10. 没有代码高尔夫式压缩。

## One-Sentence Rule

代码库瘦身不是把代码写短，而是在行为可验证的前提下，把重复、危险、失控的实现替换成更少、更清晰、更可维护的结构。
