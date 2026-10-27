---
name: understanding-system
description: >
  Write the design document for the current repository. Use when the user runs
  /understanding-system, or asks to 搞清楚一个系统的设计, 系统设计, 表设计, ER,
  实体联系, 数据流转, 状态变更, or 方案. With no narrower question, write
  .pernavo/system-design.md and put each figure in a Mermaid block. Do not use for
  implementation, diff review, colleague API handoffs, formal sign-off reports,
  or opening a database.
---

# Understanding a System

The user runs `/understanding-system`. With no narrower question, write the complete
design document for the repository they have open. Read the source the document will
cite, then read every reference listed below.

## Document

Write `.pernavo/system-design.md` in that repository. The document is the deliverable.
The reply gives its path.

Write the document in modern written Chinese. Put each figure in a `mermaid` fence
inside its section, so the Markdown preview shows the drawing. Names go in the
figure. Sentences go under that figure. Follow the paragraph shape in the reference.
Every part, column, association, message, status, and reason names a file that was
read. Leave an unread item out of the figure, and name the unread directory in the
last sentence of that section.

Use these sections, in this order:

| Section | Read | Figure |
|---|---|---|
| 结构 | [structure](references/structure.md) | `flowchart` of the runnable parts |
| 表设计 | [table](references/table.md) | a Markdown table of columns |
| 关联 | [er](references/er.md) | `flowchart` with rectangles and diamonds |
| 数据流转 | [flow](references/flow.md) | `flowchart`; the edge text is the data |
| 状态变更 | [state](references/state.md) | `stateDiagram-v2` |
| 方案 | [choice](references/choice.md) | a Markdown table of the alternatives |
| 重复结构 | [repetition](references/repetition.md) | `flowchart` when the source has a repeated block |
| 对齐 | [alignment](references/alignment.md) | none |

Write 重复结构 and 对齐 as one sentence when the source does not show that case. Write
the other six sections from the source. A missing table, relationship, flow, or status
still gets its section, with the unread directory named there.

## A narrower question

When the user names one section, write that section and its figure. `/understanding-system`
alone means the complete document.

## Other owners

- Change code: `engineering-workflow`.
- Open a database or run SQL: `data-work`.
- 给同事看 or 对接文档: `human-docs-for-colleagues`.
- A formal report of findings: `report-writer`.
- A diff or MR review: `change-review`.

## Done

`.pernavo/system-design.md` contains 结构, 表设计, 关联, 数据流转, 状态变更, and 方案.
The four figures are Mermaid fences in that file. A reader can check every sentence
against the cited file.
