# Progress & Plan Template

写入：

- `.codebase-slimming/plan.md`
- `.codebase-slimming/progress.md`
- `.codebase-slimming/modules/<name>.md`（可选）

```markdown
# Plan

## Pilot

- Module:
- Why chosen:
- Why not higher-risk cores:
- Baseline readiness:
- Expected outcome:

## Pilot result

PASS / FAIL

- Regression:
- Readability review:
- Metrics before → after:
- Decision: expand / adjust / stop

## Formal goals (post-pilot)

| Metric | Before | Target | Notes |
|---|---:|---:|---|
| Production LOC | | | |
| Duplicates | | | |
| Oversized classes | | | |
| High-complexity methods | | | |
| Untested core paths | | | |

## Module backlog

| Order | Module | Problem | Action | Risk | Baseline required |
|---:|---|---|---|---|---|
| 1 | | | | | |
```

```markdown
# Progress Log

## YYYY-MM-DD / Batch N

### 范围

- 模块：
- 文件：
- 提交：

### 修改前问题

- ...

### 本次修改

- 合并 / 替换 / 删除 / 保留：

### 指标变化

| Metric | Before | After |
|---|---:|---:|
| Production LOC | | |
| Test LOC | | |
| Duplicates | | |
| Complexity hotspots | | |
| Files | | |

### 验证

- Build：
- Unit tests：
- Integration tests：
- QA：
- API：
- Database：
- Dependency direction：
- Readability：

### 风险

- ...

### 结论

PASS / ROLLBACK / PAUSE
```
```
