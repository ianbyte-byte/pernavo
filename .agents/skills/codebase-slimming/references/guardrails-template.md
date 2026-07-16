# Guardrails Template

写入：`.codebase-slimming/guardrails/`，并按项目同步到 `CLAUDE.md` / `AGENTS.md` / CI / lint / PR 模板。

```markdown
# Coding rules (post-slimming)

## Before adding code

Search existing implementations first for:

- utilities, date/money/tax helpers
- state transitions and validators
- API clients and data access
- error types, DTOs, auth checks, logging wrappers

Do not copy-paste a second implementation.

## AI change constraints

1. State which existing code will be reused.
2. State any new abstraction and why it is not a god method.
3. State any new cross-module dependency.
4. Run relevant tests; attach behavior evidence.
5. Do not rewrite core modules without human approval.
6. Do not ignore failing tests or paper over root causes.
7. Do not hide business rules in metaprogramming/config black boxes.

## Review checklist

- [ ] Behavior unchanged or intentional change approved
- [ ] No golf (comment/test deletion, line-packing, obscure syntax)
- [ ] Duplication reduced without wrong abstraction
- [ ] Module boundaries respected
- [ ] Tests or QA evidence attached
- [ ] Deletion justified with no-behavior-loss proof

## CI checks (add gradually)

- build, unit, integration
- format / static analysis
- duplication and complexity budgets (where tooling exists)
- dependency direction / architecture tests
- API contract and migration checks
- block generated/vendor dumps and deprecated deps

Keep gates tight enough to prevent re-bloat, loose enough for normal delivery.
```

```markdown
# Final report skeleton

# Codebase Slimming Final Report

## 结论

COMPLETED / PARTIAL / STOPPED

## 目标完成情况

| 指标 | 修改前 | 目标 | 实际 |
|---|---:|---:|---:|
| 生产代码行数 | | | |
| 测试代码行数 | | | |
| 重复实现数量 | | | |
| 超大类数量 | | | |
| 高复杂度方法数量 | | | |
| 无测试核心路径 | | | |

## 行为验证

| 检查项 | 结果 | 证据 |
|---|---|---|
| Build | | |
| Unit Tests | | |
| Integration Tests | | |
| API Compatibility | | |
| UI Behavior | | |
| Database Behavior | | |
| External Integrations | | |
| Performance | | |

## 主要改进

1. ...

## 替换的危险实现

| 原实现 | 新实现 | 行为证据 |
|---|---|---|

## 未完成项

| 项目 | 原因 | 建议 |
|---|---|---|

## 新增护栏

1. ...

## 剩余风险

1. ...
```
```