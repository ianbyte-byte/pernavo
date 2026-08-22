# Project workflow routing

Classify the user's requested outcome before choosing a general coding approach.

- If the user asks to inspect the current Git diff, review a MR/PR, review changes before commit, or
  审查改动/提交前自查, invoke `/review-mr` and follow that Skill's evidence and specialist routing.
- If the user explicitly asks for Open Code Review, OCR, the `ocr` CLI, or an OCR preview/review,
  invoke `/open-code-review`. Do not substitute a generic code review.
- If the user asks to remove dead or duplicated code, decouple modules, or perform behavior-preserving
  codebase slimming, invoke `/codebase-slimming`.
- If none of these conditions match, do not invoke a review or cleanup workflow merely because the
  task involves code.

When a listed Skill is unavailable, report the missing registration instead of silently claiming that
the workflow was used. Preserve unrelated dirty work and keep review, implementation, and behavior
verification as separate responsibilities.
