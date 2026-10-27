---
name: desktop-wireframe
description: >
  Produce a light desktop wireframe sheet in the Feishu desktop wireframe
  prototype layout: a window specimen, a button kit, a component kit, and
  composed desktop windows. Use when the user asks for 桌面端线框原型,
  飞书线框模板, 窗口布局, 常用组件, or a desktop wireframe prototype before
  implementation. Do not use for an annotated stakeholder deck, production UI,
  or uploading a document to Feishu.
---

# Desktop wireframe

Own the sheet a person opens to review desktop structure. Copy the shell.
Replace the sample screens. Keep the kit. Do not implement the product, and
do not edit a Feishu document.

## Route away

| Request | Owner |
|---|---|
| Annotated HTML deck, redlines, clickable mock, 线稿, 设计稿 | `frontend-wireframe` |
| Production page, component, or styling in the real app | `engineering-workflow` |
| Formal findings report | `report-writer` |

Finish the sheet before any production change. Do not start that change in the same pass.

## Collect

Mark a missing fact unavailable. Do not invent a second product.

- Product name and the one job of this review
- Screens. One screen has one job
- Language of the screen copy

If the brief names no product, pick one concrete product and say that you picked it.
If the brief names no screens, draw one window for that product's main job.

## Draw

The sheet is done when this skill's `scripts/check_wireframe.py` prints `PASS` and exits 0.

1. Copy [assets/shell.html](assets/shell.html) to `docs/wireframes/desktop-<slug>-v<n>.html`.
2. Set `<title>` and the `h1` to the product name followed by `桌面端线框原型图`.
3. Keep `[data-board="kit"]`. Keep the headings `窗口布局`, `按钮`, and `常用组件`.
4. Add a control the brief needs and the kit lacks to `[data-column="components"]` first, with a new `data-part`, and only then use it on a screen.
5. Replace `[data-board="screens"]`. One `[data-screen]` window per screen. Build each window from `data-part` values that already exist in the kit. Write the product's real copy, in its language. Name a control by the action.
6. Run this skill's [scripts/check_wireframe.py](scripts/check_wireframe.py) with the HTML path as its only argument.

## Report

```text
Path
Screens (id · job)
Kit parts added
Checker (command · exit · PASS or FAIL line)
Open with: open <path>
```

Do not claim a browser checked the sheet unless a screenshot was taken.
Do not claim the production app matches the sheet.
