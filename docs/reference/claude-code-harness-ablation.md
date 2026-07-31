# Claude Code Harness 消融：事实核验与安全实践边界

> 核验日期：2026-07-31（Asia/Shanghai）
> 输入材料：`Claude Code之父：每半年清空一次claude.md、skills和hooks，模型自己会想办法.md`
> 结论性质：公开资料核验 + 可证伪的工程实践建议，不是 Anthropic 官方政策

## 结论摘要

“定期重测旧提示词与 Harness 是否仍有边际价值”有官方资料支持的工程动机：Claude Code
官方文档明确说明不同扩展层的加载成本、建议按反复出现的失败逐步增加配置，并提供
`--bare` 与 `--safe-mode` 进行非破坏性排障。但“每六个月全部删除”不是找到的官方规范，
也不能推导出安全、权限、合规 Hooks 可以关闭。

因此，本文采用的可执行结论是：**周期是复核触发器，不是删除授权；先影子消融、后逐项决策；
安全控制默认不可消融。**

## 证据等级

- `已核实`：当前一手资料直接支持。
- `部分核实`：一手资料支持核心方向，但不支持原文的数字、版本、范围或因果强度。
- `未独立核实`：只在访谈整理/标题中出现，未取得可检索的一手逐字内容或其他一手证据。
- `工程推论`：基于已核实机制提出的实践，需由真实任务实验验证。

## 逐项核验

| 主张 | 结论 | 一手证据与边界 |
| --- | --- | --- |
| Boris Cherny 是 Claude Code 的创造者/负责人 | 已核实 | Anthropic 活动页称其为 “inventor of Claude Code” 与 Head of Claude Code。该身份不自动证明访谈中的每个数字。[Anthropic webinar](https://www.anthropic.com/webinars/claude-code-service-delivery) |
| 可替换或追加 system prompt | 已核实 | CLI 文档列出 `--system-prompt[-file]` 与 `--append-system-prompt[-file]`；同时警告替换会丢失默认工具、安全与编码指导，使用者需自行负责。[CLI reference](https://code.claude.com/docs/en/cli-usage) |
| `CLAUDE_CODE_SIMPLE=1` 可用于极简实验 | 部分核实（命令/变量已核实） | 当前文档把 `--bare` 定义为极简模式并说明其设置 `CLAUDE_CODE_SIMPLE`；它跳过部分自动发现和后台能力，不等于“移除几乎全部系统提示词”。[CLI reference](https://code.claude.com/docs/en/cli-usage) |
| 可一次禁用所有自定义层排障 | 已核实 | `--safe-mode` 会禁用 CLAUDE.md、Skills、Plugins、Hooks、MCP、自定义 Agents 等；权限与部分托管策略仍工作。它是排障入口，不是生产安全证明。[CLI reference](https://code.claude.com/docs/en/cli-usage) |
| 扩展会增加上下文成本和噪声 | 已核实 | 官方文档说明 CLAUDE.md 每次加载、Skill 描述常驻、错误或重叠描述会漏触发/错触发，并建议 CLAUDE.md 控制在 200 行内。[Extend Claude Code](https://code.claude.com/docs/en/features-overview) |
| 只在模型反复犯错后增加配置 | 已核实 | 官方文档建议在约定或命令连续出错、重复粘贴流程等可观察触发出现后，再增加 CLAUDE.md、Skill 或 Hook。[Extend Claude Code](https://code.claude.com/docs/en/features-overview) |
| “每六个月清空 CLAUDE.md、Skills、Hooks” | 未独立核实 | 未在当前官方文档找到这一固定周期或全量删除建议。可将其作为访谈中的经验假说，不能写成强制政策。 |
| “删掉 Claude Code 80%+ 系统提示词” | 部分核实（仅标题级） | YouTube 的公开视频标题为 “We Cut 80% of Claude Code’s Prompt”。标题只支持“80% prompt”这一发布表述；本次无法取得可检索字幕，不能确认 system-prompt 范围、具体版本、消融方法或删除后的保留内容。[Y Combinator video](https://www.youtube.com/watch?v=qyPCVqFUyDo) |
| Dynamic Workflows 可协调大规模并行 Agent | 已核实（高层） | Anthropic 的 Opus 4.8 发布页称该预览功能可运行数百个并行 subagents 并处理大规模迁移；“Opus 5”、数千/数万 Agent、函数式 Agent 代数等细节未由该页面支持。[Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8) |
| Loop 是会话内重复，Routine 在云端持续运行 | 已核实 | `/loop` 依赖当前会话，重复 `/loop` 任务默认 7 天后过期；Routines 在 Anthropic 托管基础设施上按计划、API 或 GitHub 事件运行。[Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)；[Routines](https://code.claude.com/docs/en/routines) |
| 模型可无额外机制连续运行数周/月 | 未独立核实 | 当前官方材料提供 `/goal`、`/loop`、后台会话与 Routines 等明确持续机制；不能据此证明裸模型会自行连续运行数月。[/goal](https://code.claude.com/docs/en/goal) |
| 三层机制已使提示词注入难以演示 | 部分核实 | Anthropic 系统卡公开讨论 prompt-injection safeguards 与评测，但本次材料不能确认访谈所述的精确三层架构、神经元解释或任意部署的安全保证。[Claude Opus 4.8 System Card](https://www-cdn.anthropic.com/0b4915911bb0d19eca5b5ee635c80fef830a37ea/Claude%20Opus%204.8%20System%20Card.pdf) |
| Bun Zig→Rust、Electron→Swift、OpenCV 绘画的数字与细节 | 未独立核实 | 未找到能逐项支持 11 天、14–15 天、代码规模、生产替换或 Agent 数量的一手公开材料；保留为访谈案例，不升级为事实。 |

## 为什么不能直接“全删”

官方文档把不同层分成不同职责：CLAUDE.md 提供常驻约定，Skills 提供按需知识与流程，Hooks
提供确定性事件执行。文档还明确指出，必须强制的护栏应放在 Hook 中；提示词中的“不要做”只是请求，
而 PreToolUse Hook 才是执行层阻断。[Extend Claude Code](https://code.claude.com/docs/en/features-overview)

因此，全量删除会把以下变量同时改变：

1. 模型可见上下文；
2. Skill 路由候选；
3. 工具与权限执行控制；
4. 外部连接与自动化；
5. 观测与审计。

这种实验无法归因，还可能产生静默安全回归。`--safe-mode`/`--bare` 可用于受限环境中的整体对照，
但不能代替逐项实验，也不能授权对真实配置做删除。

## 可执行工程协议

1. **盘点**：区分 always-on、on-demand、deterministic enforcement 与 integration；记录来源、作用域、优先级和负责人，不复制秘密值。
2. **保护**：安全、权限、合规、数据边界、破坏性命令阻断、审计日志默认 `KEEP`，不进入关闭实验。
3. **固定基线**：锁定模型、CLI 版本、工具、权限、代码 revision 与真实任务集。
4. **单元消融**：A 为当前 Harness，B 只隐藏一个连贯单元；使用新上下文、相同任务与独立 oracle。
5. **覆盖边界**：路由类必须有 positive / negative / collision；高后果边界必须有 safety canary。
6. **证据决策**：输出 `KEEP / COMPRESS / MOVE / MERGE / RETIRE / INCONCLUSIVE`；速度与 token 仅作次要指标。
7. **另行授权变更**：审计默认只读；真正修改前需明确写范围、可恢复快照、单项变更和回归验证。
8. **重新开始条件**：模型、runtime、权限或工具集合变化后，不把旧试验与新结果混为一组。

这套协议把访谈里的“敢于删除”改写为可证伪的工程动作：只有在相同任务、相同权限、独立验证下，
缺失该单元仍不劣且不削弱安全边界，才有资格建议退休。

## 来源访问限制

- 微信/InfoQ 页面与 YouTube 正文在本次自动化访问中未能提供可检索逐字稿；YouTube oEmbed 仅确认视频标题与发布者为 Y Combinator。
- 产品与 CLI 状态会变化；上表是 2026-07-31 的当前资料快照，执行前应重新检查官方 CLI 与文档。
- 访谈内部案例、具体数字和未公开产品状态，没有其他一手材料时均保持“未独立核实”。
