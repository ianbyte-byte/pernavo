# AI Agent Skills 精确职责拆分：公开一手资料研究

> 研究日期：2026-07-31（Asia/Shanghai）
>
> 研究对象：本地 AI Agent Skills 的职责、触发、编排、验证与状态边界
>
> 结论性质：下文责任矩阵是对公开一手资料的工程综合，不是 Agent Skills 标准条款，也没有经过本仓库运行时对照试验证明。
> 链接核验：交付时已检查 7 组来源的 Markdown/HTTPS 语法；研究过程中读取了所引官方页面与固定提交源码，但未对全部深链另做穷举 HTTP 状态探测，滚动文档及未来可达性仍可能变化。

## 结论摘要

1. **开放格式只统一“怎么打包”，没有统一“怎么触发”。** Agent Skills 规范规定 `SKILL.md`、`name`、`description`、正文及可选资源；其中 `allowed-tools` 仍标为实验性且客户端支持可能不同。[S3]
2. **发现信息不等于已加载指令。** OpenAI Codex、Anthropic 与 OpenCode 都展示了相同的大方向：先暴露名称/描述，选中后才加载正文，再按需读引用或运行脚本；但各产品的扫描位置、上下文预算、显式调用和隐式选择机制不同。[S1][S4][S6]
3. **Skill 是可复用工作流说明，不是硬权限边界。** 项目常驻规则应放在 `AGENTS.md`；强制阻断、参数改写、权限和外部能力分别属于 hook/plugin、permission、脚本/tool 与 MCP。OpenCode 的 command、agent、skill、MCP、plugin 是不同扩展面，不应靠一个大 Skill 模拟全部。[S2][S6][S7]
4. **最稳妥的拆分单位是“一个决策所有者 + 一种主要产物”。** 路由、未知项发现、实现、编排、QA、代码审查、专业约束和状态/证据各自回答不同问题；作者不应同时给自己的产物最终批准。[S5]
5. **任务状态、长期记忆和运行证据必须三分。** 任务状态用于恢复当前工作；长期记忆用于跨任务召回且可能过时；运行证据用于证明某次命令、测试、部署或观察实际发生。三者不能互相冒充。[S2][S4][S7]

## 一、证据基线与边界

### 1. Metadata、正文与资源是三层，不是一个整体触发器

- OpenAI Codex 官方文档说明：初始只给模型 skill 的名称与描述，决定使用后才读完整 `SKILL.md`；隐式选择依赖 `description`，因此描述应写清范围和边界。Codex 当前源码也把可见目录渲染成“名称 + 描述 + 定位信息”，并要求选中后完整读取正文。[S1]
- Anthropic 把渐进披露明确分成 metadata、instructions、resources/code；脚本可以执行而不把源码全部塞进上下文，适合稳定、可重复的操作。[S4]
- 开放规范把 `description` 定义为“做什么 + 何时使用”，正文定义为激活后的指令；额外资源按需读取。该规范没有规定统一的关键词 Hook、分类器、召回算法或路由优先级。[S3]

因此，本地设计应把 `description` 当作**候选发现契约**，把正文当作**执行契约**。不能因为正文写了 “MUST trigger” 就认为宿主一定会发现它；正文尚未加载时，那句话可能根本不可见。

### 2. Instruction、显式入口、角色、能力和强制门禁应分面

OpenCode 的固定提交文档给出清楚的产品内区分：[skill](https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/skills.mdx#L6-L7) 是按需加载的复用指令；[command](https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/commands.mdx#L6-L35) 是用户通过 `/name` 执行的提示模板；[agent](https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/agents.mdx#L6-L39) 是带独立提示、模型、工具权限和 primary/subagent 模式的角色；[MCP](https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/mcp-servers.mdx#L6-L20) 提供外部工具；[plugin hook](https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/plugins.mdx#L67-L100) 是事件驱动的程序化扩展。

据此建议：

- “始终适用”的仓库约束放 `AGENTS.md`，不要依赖 Skill 被召回后才生效。[S2]
- “用户明确启动某流程”优先用 command；“任务相关时复用方法”用 Skill；“换一个上下文/权限/模型完成工作”用 agent。
- “调用外部系统”用 MCP/tool；“每次工具执行前都必须检查”用 permission 或 hook。Skill 可以解释门禁，但不能替代门禁。
- 脚本只有在被工具实际执行时才是程序化检查；写在 Markdown 中的伪代码仍只是模型指令。[S4]

### 3. 触发 API 不可跨产品外推

OpenAI Codex 文档说其客户端可按 `description` 隐式选择；Anthropic 文档描述 Claude 的匹配行为；OpenCode 当前官方文档则把允许的 Skills 放入 `skill` tool 描述，模型再按名称调用工具。[S1][S4][S6] Oh My OpenAgent（OMO）在固定提交中还额外实现了 IntentGate：先以正则检测特定关键词，再把模式提示注入用户消息；其中组合模式可以再要求模型加载某个 Skill。[S7]

这些是**不同宿主的实现事实**，不能归纳为“所有 Agent 都支持关键词字段”或“写了关键词就必然触发”。需要可证明触发时，应测试实际宿主的可见目录、工具调用或 hook 事件，而不是检查模型是否口头说“已启用”。

## 二、推荐责任矩阵

| 层 | 只负责回答 | 主要产物 / 权限 | 建议触发或调用 | 明确不负责 | 依据 |
|---|---|---|---|---|---|
| **A. entry/router** | “这是什么任务，下一步交给谁？” | 路由决定、所需 Skill/agent 的最小集合；默认只读 | 通用工程请求、用户显式点名入口 | 不复制实现规则、测试步骤、审查清单；不宣称完成 | Metadata 是有限的发现面；技能过多会竞争注意力。[S1][S5] |
| **B. unknown discovery** | “哪些事实、约束、所有者或证据仍未知？” | 只读调查、未知项清单、假设与阻塞项、证据定位 | 目标/边界含混，或需要源码/文档/运行环境调查时由 router 调用 | 不改代码、不替用户作高影响选择、不给发布批准 | OpenCode 将 explore/scout 定义为只读代码库/外部资料调查角色。[S6] |
| **C. implementation policy** | “已知目标下，如何安全地产生最小正确改动？” | 写权限；风险分层、实现步骤、回退点、向 QA 的交接 | 明确要求 build/fix/change/harden 时 | 不决定 agent 拓扑；不审核自己的 diff；不把本地测试说成生产证明 | Skill 正文适合程序化工作流；作者与审阅者应职责分离。[S3][S5] |
| **D. topology/orchestration** | “复杂工作怎样拆图、分配、同步和恢复？” | 任务 DAG、所有权、并发/工作树规则、handoff、状态转换 | 多模块、多 agent、依赖链或长任务；简单任务不启用 | 不承载语言/框架实现政策，不替 worker 写实现，不给 QA 结论 | OpenCode 区分 primary/subagent；OMO 将编排与 Boulder 状态单列。[S6][S7] |
| **E. testing/QA** | “行为是否在指定场景下实际通过？” | 独立执行测试/场景；记录命令、环境、结果和 artifact；原则上只读或仅改测试夹具 | 实现完成、缺陷复现、发布前验收 | 不替作者修生产代码；不把覆盖率/状态字段当充分证明；不做综合 diff 审批 | Anthropic 要求正向、负向、含混与共存评测，并把机器可验证中间产物视为客观证据。[S4][S5] |
| **F. code/diff review** | “这个差异引入了哪些具体缺陷或剩余风险？” | 只读 diff + 上下文；按严重度给出可定位 finding，核对测试缺口 | 作者与 QA 之后的独立 pass | 不直接编辑、不复述整套 QA、不因“看起来合理”批准 | Anthropic 明确要求 Skill 作者不能做自己的 reviewer；OpenCode 示例 reviewer agent 禁写。[S5][S6] |
| **G. reliability/security/integration overlays** | “这个特定领域有哪些额外不变量、威胁、依赖和工具？” | 窄域规则、威胁检查、确定性脚本、MCP/tool 依赖；可叠加到 C/E/F | 只有命中特定技术或风险信号时 | 不成为通用入口，不复制 C 的完整生命周期，不静默扩大数据/网络权限 | Skill 的脚本、网络、MCP、凭据和越界文件访问都需要单独风险审查。[S4][S5][S6] |
| **H1. task state** | “当前工作到哪、由谁、在哪个 session/worktree、能否恢复？” | 结构化计划/任务/session/status/时间戳与 evidence 指针 | 编排生命周期事件自动更新 | 不保存长期经验，不把 `completed` 当测试或部署证据 | OMO Boulder 类型只记录 plan、session、task、status、time、worktree 等控制面字段。[S7] |
| **H2. long-term semantic memory** | “哪些跨任务事实、偏好、决策和经验值得以后召回？” | 带来源、日期、适用范围和陈旧性说明的可检索记忆 | 任务结束后的受控提炼；新任务先验证易漂移事实 | 不保存活跃任务锁/计时器；不取代 `AGENTS.md` 强规则；不证明当前运行状态 | Codex 官方称 memory 是跨聊天 recall layer，并明确要求强制团队规则仍放 `AGENTS.md`。[S2] |
| **H3. runtime evidence** | “本次运行实际发生了什么？” | 命令/参数、时间、目标环境、退出码、日志或 artifact hash、测试/部署/观察结果 | tool/hook/CI/QA 实际执行时写入，task state 只保存指针 | 不从计划、模型叙述、旧记忆或单一 status 推断 | Anthropic 区分模型指令与脚本输出，并建议用脚本验证结构化中间产物。[S4] |

### 推荐组合顺序

```text
entry/router
  ├─ 事实不足 → unknown discovery → 回到 router
  └─ 目标明确 → [必要时 topology] → implementation policy + 0..N 专业 overlay
                                      → testing/QA → code/diff review → 人或外部门禁

task state：贯穿当前流程，只保存控制面状态与 evidence 指针
semantic memory：流程结束后提炼，下一次使用前按漂移风险复核
runtime evidence：由实际执行面产生，不能由上述两类状态补写成“已证明”
```

## 三、反重叠规则

1. **一个 Skill 只有一个主语义。** `description` 首句写“动作 + 对象”，随后写正向触发和排除项，例如：`Review an existing code diff ... Use after implementation. Do not use to write or test the change.` OpenAI 要求明确“何时应/不应触发”；开放规范只保证 `description` 可作为发现信息，不保证负向句的算法语义。[S1][S3]
2. **Router 只组合，不吞并叶子。** Router 可以返回 `implementation + sql-safety + QA`，但不能把三者正文复制进自己；否则任何工程请求都会让宽描述与叶子描述竞争。
3. **每个决策只有一个批准者。** C 拥有实现，E 拥有行为执行证据，F 拥有 diff finding；最终发布由人、CI 或外部门禁拥有。C 不自证，E 不替代 F，F 不伪造 E。
4. **常驻规则与按需知识分开。** 仓库不可违反的命令、文件边界和安全要求放 `AGENTS.md`/权限层；仅某类任务需要的方法放 Skill。[S2]
5. **说明与执行分开。** “必须阻止危险命令”若只写进 Skill，召回失败时就失效；应由 hook/permission 实施，Skill 只解释原因和恢复路径。OMO 自身文档也把 instruction context 与 enforcement 区分开。[S7]
6. **专业 Skill 采用 overlay，不复制主流程。** 安全、可靠性、数据库、浏览器或第三方集成只添加自己的不变量、工具和验收，不再定义一套通用“探索→实现→测试→审查”。
7. **状态、记忆、证据采用不同 schema 和写入者。** 状态记录 `running/completed`；记忆记录“已知/偏好/经验 + 来源/日期”；证据记录实际执行。任何 `PASS` 必须可追到 evidence，而非只追到状态或模型文本。
8. **同名和近义 Skill 必须做碰撞测试。** 至少覆盖应触发、不应触发、含混边界以及与相邻 Skill 共存的 3–5 个代表用例；在实际使用的模型/宿主上运行，而不是只做 YAML 检查。[S5]

## 四、落地时的最小验收

对每个新增或拆分后的 Skill，保留一张短表即可：

| 项目 | 必填内容 |
|---|---|
| 主责任 | 只写一个决策问题和一个主要产物 |
| 正向触发 | 3–5 个真实请求；记录宿主是否实际加载正文 |
| 负向/含混 | 与最邻近两个 Skill 的不触发和移交用例 |
| 组合边界 | 可同时加载哪些 overlay；哪些必须互斥 |
| 权限面 | Skill 指令、脚本、tool/MCP、hook/permission 分别列出 |
| 证据面 | 触发事件、加载记录、命令结果和 artifact 路径；不得只记录模型自述 |
| 独立复核 | 作者、QA、reviewer 身份分开；未覆盖项显式列出 |

## 五、来源与逐项限制

### S1. OpenAI Codex Skills（官方文档 + 固定提交源码）

- [Build skills（官方滚动文档）](https://developers.openai.com/codex/skills/)；[可见目录、触发说明与渐进加载源码](https://github.com/openai/codex/blob/f0c30e528a54bdf0fa9a4d52ff74b34383434811/codex-rs/core-skills/src/render.rs#L18-L63)；[Skill 根目录发现源码](https://github.com/openai/codex/blob/f0c30e528a54bdf0fa9a4d52ff74b34383434811/codex-rs/core-skills/src/loader.rs#L260-L289)。源码修订：`openai/codex@f0c30e528a54bdf0fa9a4d52ff74b34383434811`（访问日 `main`）。
- **支持：** `name`/`description` 的发现作用、正文后加载、Codex 的扫描范围与上下文预算。
- **限制：** 文档是滚动页面，没有在页面上给出固定版本；固定提交只证明该版 Codex 实现，不能代表 Claude、OpenCode 或其他客户端。

### S2. OpenAI Codex AGENTS 与 Memories（官方文档 + 固定提交源码）

- [AGENTS.md 官方文档](https://developers.openai.com/codex/guides/agents-md/)；[项目指令发现与拼接源码](https://github.com/openai/codex/blob/f0c30e528a54bdf0fa9a4d52ff74b34383434811/codex-rs/core/src/agents_md.rs#L1-L16)；[Memories 官方文档](https://learn.chatgpt.com/docs/customization/memories)。源码修订同 S1。
- **支持：** `AGENTS.md` 是任务开始时的分层项目指令；memory 用于跨聊天召回，且不应成为必须规则的唯一载体。
- **限制：** 只描述 OpenAI 产品；memory 召回不保证实时性或事实仍然有效，也不是运行证据系统。

### S3. Agent Skills 开放规范（固定提交）

- [Specification](https://github.com/agentskills/agentskills/blob/38a2ff82958afee88dadf4831509e6f7e9d8ef4e/docs/specification.mdx#L6-L32)；[正文与渐进披露](https://github.com/agentskills/agentskills/blob/38a2ff82958afee88dadf4831509e6f7e9d8ef4e/docs/specification.mdx#L176-L222)。修订：`agentskills/agentskills@38a2ff82958afee88dadf4831509e6f7e9d8ef4e`。
- **支持：** 目录格式、frontmatter 字段、正文/脚本/引用与渐进披露建议。
- **限制：** 规范没有定义统一的自动触发 API；`allowed-tools` 明确是实验字段且实现可能不同。参考校验库自身也标注为演示用途，不能当生产运行时证明。

### S4. Anthropic Agent Skills 架构与作者指南（官方滚动文档）

- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)；[Skill authoring best practices：脚本与可验证中间产物](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#advanced-skills-with-executable-code)。
- **支持：** metadata/正文/资源的三层披露；指令适合灵活判断，脚本适合可靠重复操作；结构化计划可先由脚本验证再执行。
- **限制：** Claude API、Claude Code 与 claude.ai 的安装/执行面不同；Anthropic 的匹配描述不能外推成所有宿主的算法。

### S5. Anthropic Skills 企业治理（官方滚动文档）

- [Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)。
- **支持：** 触发准确性、隔离、共存、指令遵循和输出质量评测；正向/负向/含混用例；作者与 reviewer 职责分离；安全审查脚本、网络、MCP、凭据和文件范围。
- **限制：** 是 Anthropic 的治理建议，不是跨行业标准；“3–5 个用例”等数量是起点，不能替代高风险领域自身验证。

### S6. OpenCode 扩展面（固定提交官方源码文档）

- [Skills](https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/skills.mdx#L6-L45)、[Commands](https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/commands.mdx#L6-L35)、[Agents](https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/agents.mdx#L6-L39)、[MCP](https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/mcp-servers.mdx#L6-L20)、[Plugins/hooks](https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/plugins.mdx#L54-L100)。修订：`anomalyco/opencode@da59457ca4ff55aca0147d4ddb33c495dc72be31`（访问日 `dev`）。
- **支持：** OpenCode 内各扩展面的职责和调用差异，以及 Skill 目录/工具可见性。
- **限制：** 这是 OpenCode 产品模型，不是开放规范；`dev` 快照可能继续变化，V2 beta 文档未用作稳定结论。

### S7. Oh My OpenAgent / Oh My OpenCode（固定提交源码）

- [仓库对 IntentGate 的定义](https://github.com/code-yeongyu/oh-my-openagent/blob/9dfe44185a09051f0a82d7cc78ee52a61a369411/AGENTS.md#L398-L398)；[关键词匹配与过滤](https://github.com/code-yeongyu/oh-my-openagent/blob/9dfe44185a09051f0a82d7cc78ee52a61a369411/packages/omo-opencode/src/hooks/keyword-detector/detector.ts#L14-L70)；[chat.message 注入](https://github.com/code-yeongyu/oh-my-openagent/blob/9dfe44185a09051f0a82d7cc78ee52a61a369411/packages/omo-opencode/src/hooks/keyword-detector/hook.ts#L55-L96)；[组合关键词路由到 Skill](https://github.com/code-yeongyu/oh-my-openagent/blob/9dfe44185a09051f0a82d7cc78ee52a61a369411/packages/omo-opencode/src/hooks/keyword-detector/constants.ts#L13-L24)；[Skill 发现与正文加载](https://github.com/code-yeongyu/oh-my-openagent/blob/9dfe44185a09051f0a82d7cc78ee52a61a369411/packages/omo-opencode/src/tools/skill/tools.ts#L76-L180)；[Boulder 状态类型](https://github.com/code-yeongyu/oh-my-openagent/blob/9dfe44185a09051f0a82d7cc78ee52a61a369411/packages/boulder-state/src/types.ts#L1-L64)。修订：`code-yeongyu/oh-my-openagent@9dfe44185a09051f0a82d7cc78ee52a61a369411`（访问日 `dev`；包名仍处于 `oh-my-opencode` / `oh-my-openagent` 迁移期）。
- **支持：** IntentGate 是程序化关键词 Hook，Skill loader 是另一层；Boulder 保存当前工作控制状态；说明性 `AGENTS.md` 与权限/hook enforcement 分离。
- **限制：** 这是一个插件在单一提交的实现样本，不证明关键词路由优于模型选择，也不证明本仓库已安装、已启用或运行相同版本；源码里的状态字段不等于测试/部署成功证据。

## 最终边界

本研究能支持的是：**用 metadata 做候选发现，用 Skill 正文做任务流程，用脚本/tool/MCP 做能力，用 hook/permission 做强制门禁，用 agent/topology 做上下文与所有权隔离，用 QA/review 产生相对独立判断，并把 task state、semantic memory、runtime evidence 分开存储。**

本研究不能支持的是：某组名称必然自动触发、某个关键词在所有宿主有效、责任矩阵天然提升成功率，或任何 `completed` / `PASS` 文本已经证明真实环境结果。上述主张都需要在目标客户端、模型、安装集合和真实工作流上另做运行时评测。

[S1]: https://developers.openai.com/codex/skills/
[S2]: https://developers.openai.com/codex/guides/agents-md/
[S3]: https://github.com/agentskills/agentskills/blob/38a2ff82958afee88dadf4831509e6f7e9d8ef4e/docs/specification.mdx
[S4]: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
[S5]: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise
[S6]: https://github.com/anomalyco/opencode/blob/da59457ca4ff55aca0147d4ddb33c495dc72be31/packages/web/src/content/docs/skills.mdx
[S7]: https://github.com/code-yeongyu/oh-my-openagent/blob/9dfe44185a09051f0a82d7cc78ee52a61a369411/AGENTS.md#L398
