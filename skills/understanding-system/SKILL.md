---
name: understanding-system
description: >
  Write the design document for the current repository. Use when the user runs
  /understanding-system, or asks to 搞清楚一个系统的设计, 系统设计, 表设计, ER,
  实体联系, 数据流转, 状态变更, or 方案. With no narrower question, write
  .pernavo/system-design.md and put each figure in a Mermaid block. Cite every
  path from scripts/coverage.py. Do not use for implementation, diff review,
  colleague API handoffs, formal sign-off reports, or opening a database.
---

# Understanding a System

The user runs `/understanding-system`. With no narrower question, write the complete
design document for the repository they have open.

## Read

From this skill's directory, run [`coverage.py`](scripts/coverage.py):

`python3 scripts/coverage.py list <repository>`

Read every printed path before writing. A directory name does not stand in for those files.
Then read every reference listed below.

## Document

Write `.pernavo/system-design.md` in that repository. The document is the deliverable.
The reply gives its path.

Write the document in modern written Chinese. Put each figure in a `mermaid` fence
inside its section, so the Markdown preview shows the drawing. Names go in the
figure. Sentences go under that figure. Follow the paragraph shape in the reference.
Every part, column, association, message, status, and reason names a printed path
that was read. Cite every printed path in the document.

Use these sections, in this order:

| Section | Read | Figure |
|---|---|---|
| 结构 | [structure](references/structure.md) | `flowchart` of the runnable parts |
| 表设计 | [table](references/table.md) | one Markdown column table per relation |
| 关联 | [er](references/er.md) | `flowchart` with one diamond per relationship |
| 数据流转 | [flow](references/flow.md) | one `flowchart` per stored-data operation; the edge text is the data |
| 状态变更 | [state](references/state.md) | one `stateDiagram-v2` per stored status column |
| 方案 | [choice](references/choice.md) | a Markdown table of the alternatives |
| 重复结构 | [repetition](references/repetition.md) | `flowchart` when the source has a repeated block |
| 对齐 | [alignment](references/alignment.md) | none |

Write 重复结构 and 对齐 as one sentence when the source does not show that case. Write
the other six sections from the printed files. When those files do not define a table,
relationship, flow, or status, say that in the section. Do not stop after one operation,
one table, or one status column.

## A narrower question

When the user names one section, write that section and its figure from the printed paths
that define it. `/understanding-system` alone means the complete document.

## Other owners

- Change code: `engineering-workflow`.
- Open a database or run SQL: `data-work`.
- 给同事看 or 对接文档: `human-docs-for-colleagues`.
- A formal report of findings: `report-writer`.
- A diff or MR review: `change-review`.

## Done

`.pernavo/system-design.md` contains 结构, 表设计, 关联, 数据流转, 状态变更, and 方案.
The figures are Mermaid fences in that file. A reader can check every sentence against
the cited file.

From this skill's directory, run:

`python3 scripts/coverage.py check <repository> <repository>/.pernavo/system-design.md`

Exit 0 prints `PASS: cited N of N`. Exit 2 prints `FAIL: missing K of N` and each missing
path. Read each missing file, cite it, and run the check again. The document is done only
when the check exits 0. Exit 1 means the checker itself failed.
