# 少生产代码且压住圈复杂度：Matt Pocock 的 slop 约束

**日期：** 2026-09-01（落地） / 帖子 2026-08-31 19:00 UTC
**文档性质：** 对公开帖子的工程分析，以及已吸收进三个默认 Skill 的窄口径偏好。
**仓库位置：** `docs/learning/`（来源与边界）；落地见
`skills/engineering-workflow`、`skills/change-review`、`skills/codebase-slimming`。

## 来源

- 分析对象：[Matt Pocock (@mattpocockuk)](https://x.com/mattpocockuk/status/2094500508224409852)
- 抓取：X API `get_posts_by_id`（2026-09-01）。独立帖，无引用链。
- 作者公开身份：Total TypeScript / AI Hero；前 Vercel。个人观点。
- 抓取时互动（只反映该次快照，不是趋势证明）：2,289 likes / 63 retweets / 277 replies /
  35 quotes / 740 bookmarks / 143,753 impressions。

## 原文（逐字）

> Starting to wonder if the smartest way to reduce slop is just to produce less code
>
> Force code review to continually reduce code while ALSO keeping cyclomatic complexity low
>
> Less code means less code to maintain, fewer bugs

## 帖子在说什么

三条主张应分开读：

1. **供给侧：** 减 slop 靠少写代码，而不是写完再滤。
2. **评审双约束：** 评审要持续压代码体积，同时压住圈复杂度。
3. **因果口号：** 更少代码 → 更少维护、更少 bug。

第 1、2 条对 agent 默认多写（未请求文件、helper、抽象、兼容层）是有效偏好。第 3 条是相关常见、定律不成立：压缩后的控制流可以更难测、更难审。

“持续减少”有三种读法。本仓库只吸收第一种：

| 读法 | 本仓库态度 |
|---|---|
| 评审习惯：每次问“这批生产路径能否更少” | 吸收 |
| 门禁：功能 PR 也必须净减少 | 拒绝 |
| 独立瘦身批次 | 已由 `codebase-slimming` 覆盖，且必须有行为基线 |

公开引用里出现过 “do this with the least amount of lines of code changed”。那是有害的字面化：最少 diff 行数会惩罚补测试、抽端口、写明确类型。正确口径是最少能完成授权行为的**生产路径**，不是最少字符。

## 为什么写入 Skill，而不是只做学习笔记

`engineering-workflow` 已有 smallest authorized change，但没有可检查的生产表面积约束。
`change-review` 看正确性 / 安全 / 数据，几乎不看净增量与复杂度。缺口在实现和评审轴。
这是 preference（何时少做什么），不是新能力，因此不新增第九个 Skill，也不写入
`data-work` / `test-engineering` / `performance-work` / `report-writer` 的万能附录。

与 [未请求兼容层笔记](no-unrequested-compat-philschmid-20260830.md) 同类：限制 agent 扩面。
Philipp 那条当时只保存分析；本条按明确要求落到三个入口。

## 已吸收 / 已拒绝

吸收：

1. 实现默认最少生产代码：复用先于新增；不发明文件、helper、抽象、兼容层。
2. 评审同时看净生产增量和圈复杂度；用压缩换行数算失败。
3. 对象限于生产代码；测试、明确类型、错误处理、有价值注释不是可删预算。

拒绝：

1. “更少代码 = 更少 bug”当验收标准。
2. 每张 PR 必须净减少。
3. 把最少行数写进全部 8 个默认 Skill。
4. 用这条覆盖 `codebase-slimming` 的证据阶梯。

## Skill 映射

| 入口 | 落地 |
|---|---|
| `engineering-workflow` | `Production surface`：least production code；替换时有证据则删旧路径；禁止用圈复杂度换体积 |
| `change-review` | 未请求生产表面是范围问题，不是 nit；压缩控制流是失败的减少；“再短几行”不得升 P1 |
| `codebase-slimming` | 体积与圈复杂度双约束；体积下降而复杂度上升不算成功；COMPLETED 含该条件 |

严重度仍服从默认政策：无人值守时只留 P1。未请求的新行为 / 隐藏路径可以是范围或正确性（P1）；
“偏长但授权范围内”是 P2/P3，不会在默认循环里自动改写。这是有意的，避免把偏好升级成阻断。

## 证据边界

- 已核实：推文正文、作者、时间、该次抓取的互动数字；本仓库三个 Skill 的对应段落。
- 未核实：277 条回复的论点分布、Matt 个人仓库是否用同一句、圈复杂度工具在任意目标仓库可用。
- 本文件不证明任何 Skill 已在宿主会话加载，也不证明目标仓库的 bug 数量会下降。
- 不把本分析当作无基线删除代码或跳过测试的批准。
