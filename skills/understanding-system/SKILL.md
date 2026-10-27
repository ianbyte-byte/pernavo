---
name: understanding-system
description: >
  Explain an existing system's design from source that was read. Use when the user asks to
  搞清楚一个系统的设计, 系统设计, 表设计, ER, 实体联系, 数据流转, 状态变更, or how the
  running parts, tables, and status of a codebase fit together. Draw each figure as an
  Excalidraw file. Do not use for implementation, diff review, colleague API handoffs, formal
  sign-off reports, or opening a database.
---

# Understanding a System

Explain a system that already exists. Read the source the page will cite, then open the one
reference that matches the question. A second question gets a second figure and its own
reference. Each figure has one caption and one paragraph.

When the user names no question, read only [structure](references/structure.md). Stop after
the runnable parts and one operation.

## Which page

| The user wants | Read |
|---|---|
| What the running parts are, or how one operation proceeds | [structure](references/structure.md) |
| A repeated block and the one exception | [repetition](references/repetition.md) |
| Why this design or this parameter was chosen | [choice](references/choice.md) |
| Where two sides disagree, and what aligns them | [alignment](references/alignment.md) |
| The columns of one table | [table](references/table.md) |
| How entities are associated (ER) | [er](references/er.md) |
| Which data moves from which program to which program | [flow](references/flow.md) |
| How one record's status changes | [state](references/state.md) |

## The figure

Draw every figure with [excalidraw_scene.py](scripts/excalidraw_scene.py). Write a scene
JSON whose nodes are the names from the source, then run the script
from this skill directory:

```bash
python3 scripts/excalidraw_scene.py scene.json -o excalidraw/<figure>.excalidraw
```

`rectangle` is an entity, program, or status. `diamond` is a relationship. Edge text is `1`,
`N`, the data that moves, or the event. Save the file in the repository being explained, under
`excalidraw/`. The reply keeps the paragraph and the file path. Open the file in Excalidraw.

## The page

Write modern written Chinese when the user writes Chinese. Write ordinary technical English
when the user writes English. Follow the paragraph shape in the reference. Names go in the
Excalidraw file. Sentences go under the figure, in the reply.

Every part, column, association, message, and status names a file that was read. Leave an
unread item out of the figure and say which directory is still unread, in the last sentence
of that paragraph.

Leave the paragraphs in the reply. The Excalidraw file is the figure, so write that file even
when the prose stays in the reply. Do not also write a Markdown design document unless the
user asks to keep one.

## Other owners

- Change code: `engineering-workflow`.
- Open a database or run SQL: `data-work`.
- 给同事看 or 对接文档: `human-docs-for-colleagues`.
- A formal report of findings: `report-writer`.
- A diff or MR review: `change-review`.

## Done

Each figure answers one question. A reader can check every sentence against the cited file.
