# Project workflow routing

Classify the user's requested outcome before choosing a general coding approach.

- If the user asks to inspect the current Git diff, review a MR/PR, review changes before commit, or
  审查改动/提交前自查, invoke `change-review` (alias `/review-mr`) and follow that Skill's evidence
  and specialist routing.
- If the user explicitly asks for Open Code Review, OCR, the `ocr` CLI, or an OCR preview/review,
  invoke `/open-code-review`. Do not substitute a generic code review.
- If the user asks to remove dead or duplicated code, decouple modules, or perform behavior-preserving
  codebase slimming, invoke `/codebase-slimming`.
- If none of these conditions match, do not invoke a review or cleanup workflow merely because the
  task involves code.

Keep review, implementation, and behavior verification as separate responsibilities, each in a
different agent, model, or session:

- Implement: `engineering-workflow`. One writer. Do not review your own diff.
- Review: `change-review`. Report findings only. Do not implement, silently edit, approve, merge, or
  deploy from the review session.
- Verify: `test-engineering` (and overlays named by `engineering-workflow`). Behavior evidence is not
  a substitute for diff review, and a review report is not behavior proof.

Stop the implement → review → verify loop when a human or explicit policy says remaining findings
are below the severity bar: no remaining P1; selected P2 only if that policy requires them; P3/nits
optional. Do not loop until the findings list is empty. Same-session "review again" is not an
independent review; any re-review after fixes needs a fresh context. Each finding still needs a
human or explicit policy decision before it is worth fixing.

When a listed Skill is unavailable, report the missing registration instead of silently claiming that
the workflow was used. Preserve unrelated dirty work.
