# 未请求的向后兼容：Philipp Schmid 的 AGENTS.md 禁令

**日期：** 2026-09-01（分析） / 帖子 2026-08-30 19:55 UTC（上海时间 2026-08-31 03:55）
**文档性质：** 对公开帖子的工程分析，不是产品变更单，也不是对已部署契约的删除授权。
**仓库位置：** `docs/learning/`（学习笔记；不修改 8 个默认 Skill）

## 来源

- 分析对象：[Philipp Schmid (@_philschmid)](https://x.com/_philschmid/status/2094152154382528996) 引用 [Robin Ebers (@robinebers)](https://x.com/robinebers/status/2093734599956590738)
- 抓取：`https://api.fxtwitter.com/_philschmid/status/2094152154382528996`（HTTP 200）。未登录补读同一帖可见回复 3 条；其余约 18 条被登录墙挡住。未把未看见的回复当作证据。
- 作者公开身份（帖子档案）：Agents & Gemini API, MTS @GoogleDeepMind；此前 Hugging Face Tech Lead。个人观点。
- 抓取时互动（只反映该次快照，不是趋势证明）：Philipp 帖 527 likes / 16 retweets / 21 replies / 430 bookmarks / 36,004 views；被引用的 Robin 帖 5,682 likes / 201 retweets / 125 replies / 47 quotes / 220,414 views。

## 原文（逐字）

Robin Ebers（2026-08-29 16:16 UTC）：

> my favorite AI slop must be coding agents adding backward compatibility and legacy fallbacks for an app that isn't even deployed yet

Philipp Schmid（引用上帖）：

> "Do not preserve backward compatibility. Remove obsolete paths. Do not compatibility layers, fallbacks, or mitigations. " > AGENTS.md

括号里的句子缺动词（应为 Do not **add** compatibility layers…）。这是原文，不是转述润色。

## 帖子在说什么

Robin 指出一类可复现的 agent 行为：在**还没有真实调用方、甚至应用尚未部署**时，仍然主动加入：

- 旧字段别名、双写、`if legacy` 分支
- deprecated wrapper、`Compat` / `V1` / `Fallback` 层
- “以防万一”的默认值、静默吞错、mitigation 开关

Philipp 的回应不是再讲段子，而是把禁令写进 **`AGENTS.md`**：把“不要发明兼容层”从一次性 prompt 变成仓库常驻偏好。这是 preference skill / 项目指令，不是新模型能力。

适用场景被 Robin 限定得很窄：**isn't even deployed yet**。Philipp 的句子写得更绝对（Do not preserve backward compatibility / Remove obsolete paths），没有在推文里复述“仅限未上线”。分析时必须把这两层分开，不能把引用对象的限定条件悄悄删掉。

## 未登录可见回复（同一帖补记）

未登录阅读同一条 Philipp 帖：这是一条独立引用推文（standalone quote tweet），作者没有自回复。可见回复如下，其余被登录墙挡住。不编造额外回复，也不把未看见的回复树当作证据。

1. Wags（@wagsify，8 月 31 日）：

> Thats not nearly enough!

另附一张深色主题 agent-guide 截图。图无 alt text。未对整图做逐字 OCR；可见范围内大致写的是 Direct prohibition：agents 甚至不得提议 backward compatibility、legacy migration、dual-read/write、version bridges、adapters、deprecation periods 或 fallback paths，并指向 CLAUDE.md。该次快照：14 likes / 752 views。

2. tryingEveryThing（@tryingET，8 月 30 日）：

> better: "This is an alpha version. Do introduce braking changes where it simplifies things."

原文拼写是 braking（应为 breaking）。该次快照：5 likes / 598 views。

3. GoldMagikarp（@GoldMagikarp42）：

> Someday this is going to bite someone and cause an outage. Their project will ship and someone will forget to remove the "this is not a shipping product, do not add fallbacks, do not preserve legacy". Proving that software engineering will continue to be hard for a while.

该次快照：2 likes / 157 views。可见界面未给出日期，此处不补。

**本文综合建议（不是推文主张）：** 比 Philipp 更强的禁令（连 adapters / deprecation window 都不许提议）会把绿场 slop 控制压成对生产不安全的绝对句。“alpha，引入 breaking changes”是有时限的 preference。GoldMagikarp 指出的是生命周期漏洞：这条 AGENTS.md 必须过期或按绿场 / 已上线划界，否则会变成下一颗被遗忘的地雷。这支持既有结论：应吸收“禁止未请求的兼容”，而不是吸收“永远不要保留向后兼容”。

## 为什么 agent 会这样写

训练语料和公开工程实践大量来自**已上线系统**：迁移窗口、双写、JSON 别名、功能开关。模型把“不要破坏已有调用方”内化成默认谨慎。在没有部署、没有外部消费者、没有数据文件的任务里，这套谨慎会变成假风险控制：

1. **虚构调用方。** 为尚不存在的 v1 客户端保留 v1。
2. **把不确定写成兼容。** 需求没说清时，用 fallback 同时实现几种猜测。
3. **用 mitigation 代替提问。** 吞掉错误或提供默认，避免与用户确认。
4. **制造以后必须删除的表面积。** 未上线时加的兼容层，上线后会被误当成真实契约。

这与“AI slop”的其他形态同类：未请求的抽象、未请求的 DI、未请求的重试、未请求的 feature flag。共同点是 **agent 在扩大决策空间，而不是完成被授权的那一个变化轴。**

## 和本仓库已有约定的关系（对照，不改 Skill）

本仓库 `skills/codebase-slimming` 与 `docs/learning/code-aesthetics-through-slimming-and-decoupling.md` 对兼容层的态度**更严、也更窄**：

- 瘦身目标包括移除**无效**兼容分支，但前提是**外部行为、接口契约、数据兼容性不变**。
- 删除需要无行为损失证据；静态零引用不够。
- 兼容代码应标注状态：`ACTIVE_COMPATIBILITY` / `DEPRECATION_WINDOW` / `UNCONFIRMED` / `REMOVABLE`。
- 序列化内部重命名不得偷改线缆字段。

因此：

| 情境 | Robin/Philipp 禁令 | 本仓库瘦身/审美论文 |
|---|---|---|
| 绿场、尚未部署、无外部调用方 | 应禁止**发明**兼容层 | 一致：不要为假想消费者增加开关万能函数 |
| 已部署 API / 消息 / 库 / 数据 | 推文字面“不要保留向后兼容”会过宽 | 必须走证据阶梯；ACTIVE 兼容不是 slop |
| 删除旧路径 | “Remove obsolete paths” | 只有 REMOVABLE + 回退时才能删 |
| 未确认入口（调度、反射、配置） | 推文未讨论 | 标 UNCONFIRMED，禁止当死代码删 |

**综合判断（本分析，不是标准）：** 有价值的指令不是“永远不要兼容”，而是：

> **禁止未请求的兼容。** 没有真实调用方、没有迁移窗口、用户没有要求保留旧路径时，不要添加 compatibility / fallback / mitigation。已存在且被支持的契约，不得用这条 AGENTS.md 当作删除授权。

把 Philipp 的绝对句原样拷进所有项目，会和本仓库的删除证据阶梯冲突，并鼓励在生产系统上“顺便清掉旧字段”。

## 可操作的 AGENTS.md 形状（建议文案，供人工决定是否采用）

绿场或明确无外部消费者时，可用比 Philipp 原文更完整的一句：

```text
Do not add backward-compatibility layers, legacy fallbacks, dual-write,
field aliases, or silent mitigations unless a real caller, shipped contract,
or explicit user request requires them. Do not preserve obsolete paths in
code that has never been deployed. Removing an existing shipped contract
requires evidence and a human decision; this rule does not authorize that.
```

不要把该句写进本 PR 的 `CLAUDE.md` 或 Skill；本任务只保存分析。若以后要落地，应作为目标应用仓库的 preference，并与 `codebase-slimming` 的证据阶梯并存，而不是替换它。

## 给评审 / 实现 / 编排的读法

- **实现（ian-implementer / engineering-workflow）：** 绿场任务默认一条路径。出现 `Compat`、`Legacy`、`fallback`、双字段、`obsolete` 注释时，先问是否有真实调用方。
- **评审（ian-reviewer / change-review）：** 把“未请求的兼容层”标成独立发现，不要和“删除已上线字段”混成一条。已部署契约上的删除仍是数据/接口风险，默认 P1。
- **瘦身（codebase-slimming）：** “Remove obsolete paths” 不能跳过 Scan/Baseline。无效兼容是候选，不是授权。
- **Harness：** 这是 preference skill（何时不做什么），要用 description/AGENTS 触发，而不是再做一个“anti-compat” Skill。Skill 膨胀本身也是 Philipp 在其他文章里反对的。

## 与近期其他公开讨论的相邻点

- Kenton Varda / Sol：评审会不断找到问题；停止条件应是严重度与收益递减，而不是清单为空。未请求兼容层适合作为**默认 P1 风格债务的反例**：绿场上它是真实缺陷；生产契约上“清掉兼容”可能是误报。
- Philipp 自己的 skill 写作建议（philschmid.de/agent-skills-tips）：capability vs preference；description 写清何时用。本禁令是 preference：编码风格与范围，不是新工具。

以上相邻点只用于定位，不把那些文章的数据算进本帖证据。

## 证据边界

- 已核实：两条推文正文、作者、时间、引用关系、该次抓取的互动数字；未登录可见的 3 条回复正文与其快照互动数字；Philipp 无自回复、本帖为独立 quote tweet。
- 未核实：登录墙后约 18 条回复的论点分布、Philipp 个人仓库里实际 AGENTS.md 全文、他是否在所有项目使用同一句。Wags 截图无 alt text，未对整图逐字 OCR。
- 本文件不证明任何 Skill 已加载或任何目标仓库已改行为。
- 不把本分析当作对已部署系统删除兼容层的批准。

## 结论

Robin 描述的 slop 是真的：agent 常把生产迁移习惯搬到尚未存在的系统上。Philipp 把它写成 AGENTS.md 常驻禁令，是正确的**偏好落地方式**。对本仓库，应吸收的是“禁止未请求的兼容”，而不是吸收“不要保留向后兼容 / 删掉过时路径”的无条件版本。后者已经由 `codebase-slimming` 的证据阶梯覆盖；无条件删除会破坏该阶梯。
