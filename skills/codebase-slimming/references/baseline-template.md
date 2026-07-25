# Baseline & QA Template

写入：

- `.codebase-slimming/baseline.md`
- `.codebase-slimming/qa-checklist.md`
- `.codebase-slimming/evidence/`

```markdown
# Behavior Baseline

## Build

- Command:
- Environment:
- Result:
- Errors / warnings:
- Duration:
- Evidence path:

## Tests

- Command:
- Passed / failed / skipped:
- Flaky tests:
- Covered critical flows:
- Uncovered critical flows:
- Evidence path:

## API

| API | Method | Input sample | Expected output | Status | Evidence |
|---|---|---|---|---|---|

## UI / Manual

| Page or flow | Steps | Expected | Method | Status |
|---|---|---|---|---|

## Business workflows

| Workflow | Steps | Expected result | Verification |
|---|---|---|---|

## Data behavior

| Scenario | Before | Action | After | Txn / idempotency | Verification |
|---|---|---|---|---|---|

## External systems

| System | Request/response | Timeout/retry/idempotency | Isolation | Evidence |
|---|---|---|---|---|

## Known defects

| Bug | Existing behavior | Tag (PRESERVE_TEMPORARILY / FIX_SEPARATELY / UNCONFIRMED) | Notes |
|---|---|---|---|

## Metrics baseline

- Tool / command / date:
- Production lines:
- Test lines:
- Duplicate candidates:
- Oversized classes:
- High-complexity methods:
- Untested core paths:
```

```markdown
# QA Checklist

| ID | Check | How | Owner | Pass/Fail | Evidence |
|---|---|---|---|---|---|
| Q1 | | | | | |
```
```
