# Regression Template

写入：`.codebase-slimming/progress.md` 的批次验证段，或独立证据目录 `evidence/tests/`。

```markdown
# Regression Report

## Summary

- Date:
- Commit / batch:
- Scope:
- Result: PASS / FAIL / ROLLBACK

## Checks

| Check | Result | Evidence |
|---|---|---|
| Build | | |
| Unit tests | | |
| Integration tests | | |
| API compatibility | | |
| UI behavior | | |
| Database behavior | | |
| External integrations | | |
| Idempotency / transactions | | |
| AuthZ / permissions | | |
| Logs / audit | | |
| Performance smoke | | |
| No silent error swallowing | | |
| Deleted code has no call sites | | |
| No new cross-module coupling | | |
| Readability not worse | | |

## Failed checks

| Check | Failure | Fix or rollback |
|---|---|---|

## Rollback triggers observed

- [ ] Unexpected test failures
- [ ] Behavior / contract change
- [ ] Harder-to-read abstraction
- [ ] Boolean-flag god method
- [ ] Unproven dead-code deletion

## Conclusion

通过 / 不通过 / 需要回滚
```
```
