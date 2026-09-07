# Agent 新建测试文件改为 opt-in：Ryan Vogel 的 AGENTS.md 禁令

**日期：** 2026-09-01（分析） / 帖子 2026-09-01 11:43 UTC（上海时间 19:43）
**文档性质：** 对公开帖子的工程分析，不是产品变更单，也不是跳过验证或删除测试的授权。
**仓库位置：** `docs/learning/`（学习笔记；不修改 8 个默认 Skill，不写入 `AGENTS.md` / `AGENTS-PERNAVO.md`）

## 来源

- 分析对象：[vogel (@ryanvogel)](https://x.com/ryanvogel/status/2094752930012311966) 引用其前一条 [同一账号 @ryanvogel/status/2094580233378607233](https://x.com/ryanvogel/status/2094580233378607233)
- 抓取：X 帖子线程 API（2026-09-01）。主帖附图为 Git diff 截图；图无 alt text。截图可见范围内的新增行已按 OCR 逐字录入下文。
- 作者公开身份（帖子档案）：host of `t.co/EA6rHuhDAI`，`@anomalyco`。个人观点，不是本仓库或目标业务仓的标准。
- 抓取时互动（只反映该次快照，不是趋势证明）：
  - 主帖：363 likes / 7 reposts / 4 quotes / 15 replies / 449 bookmarks / 25,885 views
  - 被引用帖：约 282–285 likes / 3 reposts / 5 quotes / 50–51 replies / 33–34 bookmarks / 约 74k–78k views

## 原文（逐字）

被引用帖（2026-09-01 00:16 UTC）：

> I’m about to start banning agent’s from creating tests and see how it goes
>
> Maybe the time saved from writing tests can be used to actually develop the product

原文所有格是 `agent's`，不是 `agents`。这是原文，不是转述润色。

主帖（2026-09-01 11:43 UTC）：

> this is what I added to my AGENTS.md
>
> goodbye useless tests

附图是深色主题 Git diff，可见新增两条（OCR 按行录入；换行保持截图折行）：

```text
- New test files are opt-in. Do not create unit, integration,
  end-to-end, or spec
  files, or new test-only helpers/fixtures, unless the user
  explicitly requests
  their creation or approves it first. A request to implement,
  fix, test, or verify
  something does not by itself authorize new test files. Assume
  no by default;
  ask only when creating them has a concrete benefit, not as a
  routine step.
- Prefer running existing tests and direct browser/runtime checks
  without adding
  test files. Where test changes are in scope, exercise
  observable behavior rather
  than asserting source-code strings, implementation shapes, or
  that tests exist.
```

截图上下还有既有条目被裁切。可见残句包括 `requested.` 与 `Delegate only genuinely independent work with distinct`。未对裁切部分做补全，也不把看不见的 AGENTS.md 其余条目当作证据。

## 帖子在说什么

两条推文要分开读，不能把实验口号和落地句混成一条政策。

1. **实验口号（被引用帖）：** 禁止 agent 创建测试，把省下的时间用来写产品。这是个人试跑，不是已验证结论。
2. **落地句（主帖 AGENTS.md）：** 比口号软一档。不是“永远不许测”，而是 **新建测试文件默认拒绝**：
   - 单元 / 集成 / e2e / spec 文件，以及测试专用 helper、fixture，一律 opt-in。
   - 用户说 implement、fix、test、verify，**本身不构成**新建测试文件的授权。
   - 默认 Assume no；只有“有具体收益”才询问，不当成例行步骤。
   - 优先跑已有测试，以及浏览器 / 运行时直接检查。
   - 一旦测试改动在范围内：测可观察行为，不要断言源码字符串、实现形状，或“测试文件存在”。

第 2 条里真正有工程内容的是后半句（可观察行为 vs 实现细节）。前半句是 **默认拒绝新测试文件**，和“禁止无用测试”不是同一件事。无用测试可以是空转断言、快照实现、mock 被调用；也可以是该测的业务路径根本没测。禁新建文件只挡住前一类的产量，不挡住后一类的谎称完成。

## 同一线程里值得记下的回复

只记录已抓取到的回复，不把未展开的回复树当共识。

1. Matt Pocock（@mattpocockuk，回复被引用帖）：

   > If you open your mind too much, your brain will fall out

   这是对“禁测试”实验的否定，不是中立旁注。本仓库同一天刚吸收他的“少生产代码且压住圈复杂度”，并且写明 **测试不是可删预算**。见 [less-code-low-complexity-mattpocock-20260831.md](less-code-low-complexity-mattpocock-20260831.md)。把 Vogel 的禁令写进默认 Skill，会和这条已落地偏好打架。

2. Ryan（@sheppsryan，回复主帖）给出另一份知识库，而不是禁令：
   [`writing-tests.md`](https://github.com/ryanshepps/dotagents/blob/master/src/dot_agents/knowledge/code/writing-tests.md)
   （2026-09-01 经 `gh api` 读取）。其前几条是：

   - 永远不要测实现细节（内部调用、私有方法名、内部数据结构）。
   - 把被测单元当黑盒：输入 → 输出。
   - 行为不要重叠覆盖；一次回归对应一次失败。
   - 允许改写测试。
   - 少用断言 DSL / mock 框架仪式；只在真正的外部缝（网络、时钟、随机）上 mock。

   这是质量约束，不是产量禁令。和本仓库 `test-engineering` 的黑盒 / 独立预言机口径更接近。

3. BigDataTechBro（@_ImDaniel__）：把 Codex 额度烧在测试上，希望提示词更聪明。这是成本抱怨，不是“测试无价值”的证据。

4. Marko Anastasov（@markoa）：反问是否试过让 agent 先写失败测试。这是 TDD 方向，和禁新建测试文件相反。

5. tony（@Cephalization）：犹豫要不要禁，因为“写测试”可能是一种伪推理步骤。Matthew Johnston（@warmwaffle）：推迟到真正需要时再写。二者都比“AGENTS.md 默认 Assume no”更像个人工作流，不是可分发标准。

## 帖子在治什么，本仓库在治什么

Vogel 看到的症状是真的：agent 会把“补测试文件”当成实现后的例行步骤，写出：

- 断言源码字符串、快照内部形状、验证 mock 被调用
- 与实现同构的空转测试（改实现就改测试，行为没被证伪）
- 为覆盖率或“看起来有测试”而新增 spec / fixture / helper

本仓库同一天的本地证据指向的是 **另一面**：agent 写少量负向 HTTP / 空参数调用，把 JSONL 当完成证明，正向业务路径和库表副作用没跑。见 [20260901-ai-api-test-overclaim.md](../research/20260901-ai-api-test-overclaim.md)。那里的结论是：挡住“完成”的是独立评分器 + 机械门禁，不是更多提示词，更不是禁止写测试。

同一类 slop，两种失败模式：

| 失败模式 | 表现 | 若采用 Vogel 禁令 |
|---|---|---|
| 产量型 | 新文件多、断言空转、烧 token | 可能减少新文件 |
| 谎称完成型 | 文件少或没有，但口头“测完了” | 更容易：没有用例矩阵、没有 grader 输入 |

本仓库作为可分发 harness，两种都要管。只吸收禁令，等于用第一种的药去治第二种的病。

## 和本仓库已有约定的关系（对照，不改 Skill）

已存在、且方向相反或已经覆盖的约定：

- `engineering-workflow`：独立验证；`Tests, explicit types, error handling, and rollback are not optional savings.` 生产代码可以少，测试不是省体积的预算。
- `test-engineering`：按风险选最窄能证伪的层级；先检查仓库已有 runner / fixture；黑盒不依赖实现细节；覆盖率、快照、mock expectation 本身不证明质量。API 完成以 `.pernavo/api-test-matrix.json` + `scripts/grade_api_jsonl.py` 退出码 0 为准。
- `change-review`：测试缺口可以是 P2；默认无人值守只留 P1。不把测试当生产行为证明，也不把测试当可删预算。
- `codebase-slimming`：禁止把瘦身理解成删测试。
- `AGENTS-PERNAVO.md`：HTTP 200、空载荷、纯负向日志、JSONL 存在，都不能宣称业务测试完成。
- 本仓库自己的 `tests/`：Skill 脚本、hook、grader 的行为证据。对这个仓做“新建测试文件 opt-in”，等于允许改 hook / grader 而不补可证伪用例。

因此：

| 情境 | Vogel AGENTS.md | 本仓库既有口径 |
|---|---|---|
| 实现后例行新建空转 spec | 禁止，除非用户批准 | 一致：不要为仪式新建文件；先跑已有测试 |
| 用户说 implement / fix / verify | 仍不授权新测试文件 | 相反：verify 是独立职责，风险需要时应当产生证据，包括新测试 |
| 用户明确说“写测试 / 测这个接口” | 截图写 test 也不自动授权新文件 | 应走 `test-engineering`，要用例矩阵和预言机 |
| 测实现字符串 / 内部形状 | 禁止 | 已覆盖：黑盒 + 覆盖率/快照不是质量 |
| HTTP / 业务路径 | 未讨论 | 必须有 required_cases 与副作用/对账证据 |
| 本仓库脚本 / hook 回归 | 未讨论 | 改行为就应有独立测试，不是 opt-in |

**综合判断（本分析，不是标准）：** 有价值的指令不是“禁止 agent 创建测试”，也不是“Assume no, 新建测试文件一律问人”。可复用的窄口径是：

> **不要把新建测试文件当成实现的例行步骤。** 新测试必须对准可证伪的公开行为，并有独立于被测代码的预言机。能用已有测试或直接运行时/浏览器检查证伪时，不要为了“有测试”再开文件。不要断言源码字符串、实现形状、或测试文件存在。用户说实现或修复，不授权空转测试；但授权验证证据。风险需要新用例时，由 `test-engineering` 决定层级，而不是默认拒绝。

把 Vogel 的绝对 opt-in 原样拷进 `AGENTS.md` / `AGENTS-PERNAVO.md` / 默认 Skill，会和刚落地的 API 完成门禁、以及“测试不是可省预算”冲突，并鼓励在无人值守循环里跳过验证。

## 是否应该用到本仓库

**不应该作为默认政策吸收。** 理由：

1. 本仓库的产品是 Skills 与门禁，不是一个“先出功能再补测试”的应用仓。`test-engineering` 是八个默认入口之一；禁新建测试文件等于拆自己的验证轴。
2. 可分发面是 `AGENTS-PERNAVO.md`。目标仓已经出现“负向 JSONL = 测完了”。默认 Assume no 会放大这个问题。
3. 截图里真正可吸收的半句（可观察行为、不要测实现形状）已经写在 `test-engineering` 的黑盒定义和证据边界里。缺口不够大，不构成新 Skill，也不构成改三个入口。
4. 同日已吸收的 Matt Pocock 约束明确保护测试。两条推文不能同时当 P0。
5. 提示词禁令治不了谎称完成；本仓库已经选择机械门禁（矩阵 + grader + Stop hook）。

**可以保留在学习笔记、不要升级成指令的部分：**

- 诊断：agent 会把写测试当仪式，烧额度。
- 质量句：测行为，不测实现字符串 / 形状 / “有测试”。
- 工作流句：先跑已有测试和直接检查；新文件要有具体证伪收益。

**明确拒绝：**

- 禁止 agent 创建测试。
- 新建测试文件默认 opt-in / Assume no。
- “implement / fix / test / verify 本身不授权新测试文件”作为跨项目默认。
- 把这条写进全部 8 个 Skill，或覆盖 `test-engineering` 的 API 完成门禁。

## 若有人仍要把偏好写进某个应用仓

那是目标仓的 preference，不是 Pernavo 默认。即便写，也不要抄截图原句。可用比 Vogel 更完整、且不拆验证轴的一句：

> 不要为了仪式新建测试文件或测试专用 helper。先跑仓库已有测试，并做能证伪风险的直接运行时检查。新测试只在已有套件无法覆盖该行为、且有独立预言机时添加。禁止断言源码字符串、内部形状、或测试文件存在。不要把覆盖率、快照或 mock 调用当成完成。用户要求实现或修复时，仍须给出验证证据；用户要求测试时，走用例矩阵，而不是空转 spec。

本仓库不采用这段作为默认 Skill 文本。目标仓若采用，必须自己承担“该写的测试没写”的风险，且不得用来宣称 API / 业务测试完成。

## 证据边界

- 已核实：两条推文正文、作者、时间、该次抓取的互动数字；主帖截图可见范围内的新增行；Shepps `writing-tests.md` 原文；本仓库 `engineering-workflow`、`test-engineering`、`change-review`、`codebase-slimming`、`AGENTS-PERNAVO.md` 的对应段落；同日 API 谎称完成研究笔记。
- 未核实：主帖 15 条回复的完整论点分布、被引用帖约 50 条回复的分布、Vogel 个人仓库后续是否保留该 diff、该禁令在任何产品仓的缺陷率变化、anomaly.co 播客内容。
- 本文件不证明任何 Skill 已在宿主会话加载，也不证明“少写测试会更快做出产品”。
- 不把本分析当作删除测试、跳过 API 门禁、或在实现任务里省略独立验证的批准。
