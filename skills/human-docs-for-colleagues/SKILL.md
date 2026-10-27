---
name: human-docs-for-colleagues
description: >
  Write a scannable document a human colleague can act on. Use when the user asks for
  给同事看, 对接文档, 不要太啰嗦, 精简文档, 不知所云, colleague-facing API or integration
  docs, or a one-page handoff. Do not use for agent skills, AGENTS.md, formal evidence
  reports, or production implementation.
---

# Colleague Docs

Own the page a teammate will actually read. Scan time is the budget. If they cannot start
work after one pass, the document failed.

A document you were unwilling to write is a document they will be unwilling to read. Keep
AI-generated filler under half the page; 50% is already generous. Long AI prose that
explains everything explains nothing.

## Route away

| Request | Owner |
|---|---|
| Formal report with evidence states, findings, or sign-off | `report-writer` |
| Agent skill, `AGENTS.md`, `CLAUDE.md`, always-on instructions | `repository-governance` |
| Implement, fix, or change production behavior | `engineering-workflow` |
| Diff / MR review | `change-review` |
| 系统设计, ER, 数据流转, or 状态变更 | `understanding-system` |

Finish this page before those owners. Do not mix a colleague handoff with a report template
or an agent prompt.

## Keep

Only what the reader needs to act:

- conclusion and current status in the first screen
- business rules that change a request or a save
- routes, methods, and request fields
- success / failure contract the caller can assert
- voucher or document types they must send
- per-scenario diffs and the exact validation copy they will see

Lead with the rule, then a short table. One small request body is enough; do not walk a
full JSON tree.

## Cut

Delete on sight:

- module source directories, internal class names, views, migrations, tests
- implementation sequence, internal status fields, snapshot / trace fields
- data-dictionary constants the caller does not send
- CardID, print templates, deploy values — tell them to ask the project owner
- repeated 口径 already stated once
- full JSON walkthroughs, watermark essays, query-string examples for POST bodies

If a line does not change what they type or what they check, remove it.

## Shape

```markdown
# <name> — 对接文档

<one-line status>. Success is **`result == 1`**. Do not use HTTP status.

## 1. 业务
<rules that change a save, as tables or one-line bullets>

## 2. 单据 / 类型
| code | meaning |

## 3. 接口
| method | path | body fields |

## 4. 保存字段
| field | required | note |

## 5. 各场景只记差异
<only what differs; paste exact error text>
```

Adapt section names to the domain. Keep the whole file near one screen. Prefer tables over
paragraphs. Prefer the exact error string over a paraphrase.

## Workflow

1. Name the reader and the action they must take after reading.
2. Read the current code or contract. Do not document a previous draft.
3. List keep vs cut before writing. Cut first.
4. Draft the page. Put the success rule and the status line at the top.
5. Align field names, methods, and error text with the source. One short example per
   distinct body shape.
6. Count: if more than half the page is restatement, hedging, or unused context, delete
   until a colleague can scan and call.

When code changed, update in place. Do not rewrite the page to look complete.

## Done

The page is done when a colleague can pick a route, fill the required fields, and recognize
the failure text — without opening the implementation.
