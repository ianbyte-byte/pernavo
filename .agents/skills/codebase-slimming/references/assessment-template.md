# Assessment Template

写入：`.codebase-slimming/assessment.md`

```markdown
# Codebase Slimming Assessment

## Intake

- Repository:
- Path:
- Main language / framework:
- Runtime / database:
- Build command:
- Test command:
- Start command:
- Core workflows:
- Hard constraints (API / DB / UI / external):

## Mode

- Project mode: small / medium / large
- Production code lines (approx):
- Measurement tool / date:

## Scan Findings

### Health

| Check | Result | Notes |
|---|---|---|
| Build | | |
| Run | | |
| Tests exist | | |
| Tests stable | | |

### Problem Hotspots

| Area | Type (dup / dead / god / patch / framework / AI-slop) | Evidence | Risk |
|---|---|---|---|

### Metrics Snapshot

| Bucket | Files | Code lines | Notes |
|---|---:|---:|---|
| Production | | | |
| Test | | | |
| Generated | | | |
| Third-party | | | |

## Decision

`CONTINUE` / `PILOT_ONLY` / `STOP`

### Rationale

1. ...
2. ...
3. ...

### Main Risks

| Risk | Severity | Mitigation |
|---|---|---|

## Goals

### Range goal (after Scan/Decide only)

```text
在行为不变前提下，预计生产代码可缩减 A%～B%。
依据：
- 重复占比：
- 无效兼容层：
- 死代码候选：
- 自制框架可替换规模：
```

### Formal goal (only after Pilot passes)

```text
- 生产代码减少不少于 …%
- 重复实现减少不少于 …%
- 超大类减少不少于 …%
- 高复杂度方法减少不少于 …%
- 无测试核心路径从 N 降到 M 以内
- 不新增跨模块反向依赖
```

## If STOP

```markdown
## 结论
不建议继续代码库瘦身。

## 主要原因
1. ...

## 更适合的处理方式
1. ...
```
```
