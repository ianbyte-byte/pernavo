---
name: lcc-review
description: Structured code review workflow using lcc-reviewer (and optionally lcc-security-reviewer).
disable-model-invocation: true
---

Run a structured review.

## Steps

1) Primary review (lcc-reviewer)
- Delegate to `lcc-reviewer`.
- Require prioritized findings (Critical / High / Medium / Low) and concrete fixes.

2) Optional security pass (lcc-security-reviewer)
- If the change touches auth, permissions, input handling, file paths, network calls, or secrets, also delegate to `lcc-security-reviewer`.

3) Close the loop
- If changes are required, hand off to `lcc-coder` (or `lcc-debugger`) with an actionable fix list.
- If acceptable, require `LGTM` from `lcc-reviewer` and hand off to `lcc-tester` for verification.
