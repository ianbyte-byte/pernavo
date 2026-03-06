---
name: lcc-triage
description: Incident and bug triage workflow using lcc-incident-triage and lcc-debugger.
disable-model-invocation: true
---

Triage an incident or production issue.

## Steps

1) Triage (lcc-incident-triage)
- Delegate to `lcc-incident-triage`.
- Provide logs, timestamps, symptoms, and recent changes if available.

2) Decide path (lcc-router)
- Use `lcc-router` to decide whether to focus on mitigation, rollback, or a fix.

3) Fix/verify (lcc-debugger → lcc-reviewer → lcc-tester)
- Debugger produces minimal repro and a fix.
- Reviewer provides LGTM or fix requests.
- Tester verifies with tests and repro steps.
