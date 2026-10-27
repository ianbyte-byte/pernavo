---
name: understanding-system
description: >
  Write the design document for the current repository. Use when the user runs
  /understanding-system, or asks to 搞清楚一个系统的设计, 系统设计, 表设计, ER,
  实体联系, 数据流转, 状态变更, or 方案. With no narrower question, write the
  complete document and its Excalidraw figures. Do not use for implementation,
  diff review, colleague API handoffs, formal sign-off reports, or opening a database.
---

# Understanding a System

The user runs `/understanding-system`. With no narrower question, write the complete
design document for the repository they have open. Read the source the document will
cite, then read every reference listed below.

## Document

Write `excalidraw/system-design.md` in that repository. Put each figure in the same
`excalidraw/` directory. The document is the deliverable. The reply gives its path.

Write the document in modern written Chinese. Names go in the Excalidraw file.
Sentences go under that figure, in the document. Follow the paragraph shape in the
reference. Every part, column, association, message, status, and reason names a file
that was read. Leave an unread item out of the figure, and name the unread directory
in the last sentence of that section.

Use these sections, in this order:

| Section | Read | Figure |
|---|---|---|
| 结构 | [structure](references/structure.md) | `excalidraw/structure.excalidraw` |
| 表设计 | [table](references/table.md) | none; the columns are a table in the document |
| 关联 | [er](references/er.md) | `excalidraw/er.excalidraw` |
| 数据流转 | [flow](references/flow.md) | `excalidraw/flow.excalidraw` |
| 状态变更 | [state](references/state.md) | `excalidraw/status.excalidraw` |
| 方案 | [choice](references/choice.md) | none; the comparison is a table in the document |
| 重复结构 | [repetition](references/repetition.md) | `excalidraw/repetition.excalidraw` when the source has a repeated block |
| 对齐 | [alignment](references/alignment.md) | none |

Write 重复结构 and 对齐 as one sentence when the source does not show that case. Write
the other six sections from the source. A missing table, relationship, flow, or status
still gets its section, with the unread directory named there.

## Figures

Draw every figure with [excalidraw_scene.py](scripts/excalidraw_scene.py). Run it from
this skill directory:

```bash
python3 scripts/excalidraw_scene.py scene.json -o excalidraw/<figure>.excalidraw
```

`rectangle` is an entity, program, or status. `diamond` is a relationship. Edge text is
`1`, `N`, the data that moves, or the event.

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

`excalidraw/system-design.md` contains 结构, 表设计, 关联, 数据流转, 状态变更, and 方案.
The four required figures exist beside it. A reader can check every sentence against the
cited file.
