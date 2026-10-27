# Project workflow routing

Classify the user's requested outcome before choosing a general coding approach.

- If the user asks to inspect the current Git diff, review a MR/PR, review changes before commit, or
  审查改动/提交前自查, invoke `change-review` (alias `/review-mr`) and follow that Skill's evidence
  and specialist routing.
- If the user explicitly asks for Open Code Review, OCR, the `ocr` CLI, or an OCR preview/review,
  invoke `/open-code-review`. Do not substitute a generic code review. If that Skill is unregistered,
  report the missing registration; do not implement suggested fixes.
- If the user asks to remove dead or duplicated code, decouple modules, or perform behavior-preserving
  codebase slimming, invoke `/codebase-slimming`.
- If the user asks for 线稿, wireframe, UI blueprint, clickable mock, 设计稿, or a presentable
  multi-screen HTML prototype before implementation, invoke `frontend-wireframe`. Do not implement
  the production UI in the same pass.
- If the user asks for 给同事看, 对接文档, 不要太啰嗦, 精简文档, or a one-page human handoff,
  invoke `human-docs-for-colleagues`. Do not use `report-writer` or an agent-instruction template.
- If the user runs `/understanding-system`, or asks to understand an existing system's design,
  搞清楚一个系统的设计, 系统设计, 表设计, ER, 实体联系, 数据流转, or 状态变更, invoke
  `understanding-system`. With no narrower question, write `.pernavo/system-design.md` with
  Mermaid figures. Do not implement the system, open a database, or write a colleague handoff in
  that pass.
- If none of these conditions match, do not invoke a review or cleanup workflow merely because the
  task involves code.

Keep review, implementation, and behavior verification as separate responsibilities, each in a
different agent, model, or session:

- Implement: `engineering-workflow`. One writer. Do not review your own diff.
- Review: `change-review`. Findings only. Do not implement, silently edit, approve, merge, or deploy.
- Verify: `test-engineering`. Behavior evidence is not diff review, and a review report is not proof.

Default policy, including agent-only sessions with no human in the loop: remaining P1 only; do not
self-select P2 or P3. A human or explicit policy may still require selected P2. Re-review after
fixes needs a fresh context.

When a listed Skill is unavailable, report the missing registration instead of silently claiming that
the workflow was used. Preserve unrelated dirty work.
