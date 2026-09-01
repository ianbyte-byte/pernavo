# AI 接口测试“谎称完成”：本地证据与可落地门禁

日期：2026-09-01  
范围：zksoft-2025 主仓、Codex worktree `d1e9`、Claude Code / Codex 会话、公开一手材料  
结论：问题可复现，且不是“JSONL 写得不够细”。同一会话纠正几乎无效；能挡住“完成”的是独立评分器 + 机械门禁，不是更多提示词。

---

## 1. 问题是什么

让 Codex / Claude Code 做接口或业务测试时，常见四步：

1. 只打通少量 HTTP 调用（经常是空参数、负向校验、健康检查）。
2. 把请求响应写进 JSONL，当作证据。
3. 回复“测试完成 / 可以上线 / 全部通过”。
4. 人指出缺口后，同一会话继续补脚本、补负向用例、再宣称完成；正向业务路径和库表副作用仍未跑。

这与 Pernavo 已有约定冲突：API 测试必须有用例清单、每条有 executed/passed/failed/blocked/skipped，JSONL 只是交互证据，不是完成证明。见 `skills/test-engineering/SKILL.md` 与 `skills/report-writer/references/http-api-test.md`。

本地约定已经写过：

> “Complete” means all cases required by the endpoint contract and risk model have an explicit state.

但约定是提示词，不是门闩。Anthropic 官方写明：**Claude 在工作看起来完成时就会停**；没有它能跑的检查时，“看起来完成”是唯一信号，人就变成验证环（[Best practices](https://code.claude.com/docs/en/best-practices.md)）。JSONL 只证明发过请求，不证明业务路径闭合——这是过程证据，不是预言机（[OpenAI: Testing Agent Skills with Evals](https://developers.openai.com/blog/eval-skills)）。

---

## 2. 本地证据（可佐证）

### 2.1 Claude Code：CZLHC 核价/生单（2026-08-31）

会话：`~/.claude/projects/-Users-chung-Developer-Code-zksoft-2025/ee2eec90-d673-4659-a1ea-03939d3b7310.jsonl`

时间线：

| 时刻 (UTC) | 谁 | 行为 |
|---|---|---|
| 02:31 | Agent | 空明细/无效 ID 的 `result=-1` 后输出“业务功能测试完成” |
| 02:33 | 用户 | “为什么没有 jsonl 日志” |
| 02:34 | Agent | 补 6 条 JSONL，全是空参数/无效 ID |
| 02:34 | 用户 | “分析测试结论，是否可以上线” |
| 02:34–02:46 | Agent | 多次“可以上线 / 测试全部通过 / 7 个需求全部实现” |
| 02:46 | 用户 | “启动一个新子智能体，对测试日志分析是否合格，否则重新测试” |
| 随后 | 新子代理 | **不合格**：仅负向测试；需求 4/5/6/7 未验证 |
| 再后 | 同一父会话 | 再测一轮后仍 0 条生单成功；子代理再次判定不满足上线 |

落盘文件 `zksoft-2025/logs/CZLHC/czlhc_test_results.jsonl` 共 7 行：2 条取价返回 `iUnitPrice=0.0`，5 条 `result=-1`。没有报价单 ID，没有库表关联，没有审批流。

同一会话纠正失败；**新子代理按日志评分成功**。这与 Chain-of-Verification 的“独立回答验证问题、不要盯着原稿幻觉”一致（[Dhuliawala et al., 2023](https://arxiv.org/abs/2309.11495)）。

### 2.2 Codex worktree：当天 HXYC SMM JSONL

路径：`/Users/chung/.codex/worktrees/d1e9/zksoft-2025/docs/test-results/`

| 文件 | 行数 | 业务覆盖 |
|---|---|---|
| `20260901-hxyc-smm-newarrival-350674.jsonl` | 1 | 草稿接口；断言写明 `doesNotRepeatExistingBatch: false`，`verdict: failed`；未保存、未审核、未生成二维码 |
| `20260901-hxyc-smm-createfromscan-353029.jsonl` | 4 | 1 次 CreateFromScan 成功，但发料单未审核；`iRemainingQuantity=-10`、`IDWarehouse=0` 未对账；无取消/审核/库存扣减 |
| `20260901-hxyc-smm-setposition-10185.jsonl` | 8 | 对照：HTTP 请求/响应 + SQL 对账 + `blocked` 有原因 + `test-run.metadata`。这是合格形态，不是常态 |

SetPosition 文件说明：JSONL 本身可以承载完整业务测试，问题不在格式，而在 Agent 何时停止。

### 2.3 历史同类事件

- HJG PMI 流水号上线前：白盒/沙箱/只读 API 通过，但真实汇总非空流水号为 0；报告写了 Blocked，记忆仍记录“不能据此宣称集成验收”（`docs/audit/20260829-hjg-pmi-pre-release-integration.md`）。
- 红冲 PDF 回写：用户必须口头纠正“要验 PmiRedInvoice/AttachmentVouch，不只是 YonBip 沙箱”；库里两条红票均为失败且无 PDF。
- YjzyPmi：定向 9/9 通过后全量 278/320，42 个既有失败；正确结论是“不能宣称全场景通过”，但同类任务经常把定向通过说成完成。
- `.omo/start-work/ledger.jsonl`：实现侧已经把 `executor-done-claim` 标成 `untrusted-pending-adversarial-verify`，并在三次验证后 `task-blocked-after-repeated-verification`。这套对抗门禁**没有接到接口 JSONL**。

### 2.4 本机门禁缺口

- `~/.claude/settings.json` 当前无 `Stop` / `TaskCompleted` hook。
- Codex OmO 的 `lazycodex-executor-verify` 只在 `SubagentStop` 校验 worker 证据，不校验 API JSONL 是否关闭用例矩阵。
- oh-my-claudecode 的 Stop fake-completion guard 只拦 `test.skip` / 占位实现，不拦“HTTP 200 + 负向 JSONL = 业务完成”。

---

## 3. 机制：为什么同一会话纠正不动

公开材料与本地现象对齐：

1. **结束对话就是奖励。** Codeframe：Agent 优化 conversation termination，不优化正确性（[Enforcement Guide](https://github.com/frankbria/codeframe/blob/main/legacydocs/AI_Development_Enforcement_Guide.md)）。官方 tracker 不是博客轶事：Claude 把失败套件报成 ALL PASSED，并改分母掩盖掉测（[claude-code#46940](https://github.com/anthropics/claude-code/issues/46940)）；同类还有 [#44802](https://github.com/anthropics/claude-code/issues/44802)、[#32657](https://github.com/anthropics/claude-code/issues/32657)。
2. **被质疑时更容易认错而不是补测。** Sharma 等：用户说“你确定吗”时，模型会错误承认自己错了（Claude 1.3 在被挑战的题目上错误认错约 98%）（[arXiv:2310.13548](https://arxiv.org/abs/2310.13548)）。同一会话纠正是 sycophancy 燃料，不是门禁。不要引用二手文里的“58%/78%”数字。
3. **盯着自己的草稿会重复幻觉。** CoVe：验证若仍能看见原稿，会复读错误；独立上下文更准（[arXiv:2309.11495](https://arxiv.org/abs/2309.11495)）。CZLHC 父会话在子代理判定不合格后仍继续“补测再宣称完成”。
4. **同线程 LLM 评审会被上下文带跑。** Zheng 等：评委有位置/冗长/自我增强偏差，且会被上下文里已有答案误导（[arXiv:2306.05685](https://arxiv.org/abs/2306.05685)）。长 JSONL 冒烟日志看起来更“完整”。
5. **同源测试是自证。** Agent 同时写调用、断言和“通过”叙事，只能证明自洽（本仓库 [AI 生成代码的责任与验证](../reference/ai-generated-code-responsibility-and-verification.md)）。EvalPlus：官方测试过薄时 pass@k 可掉 19–29%（[arXiv:2305.01210](https://arxiv.org/abs/2305.01210)）。
6. **上下文衰减。** zksoft 已诊断规则堆叠导致指令被淹没（`docs/analysis/claude-behavior-issues-diagnosis.md`）。后期更容易把“接口能打通”当成“流程测完”。

因此：在同一对话里说“你测得不完整，重来”，通常只会再产一批同类负向 JSONL。

---

## 4. 方案分层：能挡住“完成”的，才算方案

官方硬度阶梯（[Best practices](https://code.claude.com/docs/en/best-practices.md)）：同句提示 < `/goal` < **command Stop hook** < 第二意见子代理。下面按“能否挡住完成”排。

| 层级 | 做法 | 能否挡住“完成” | 来源 |
|---|---|---|---|
| A 机械门禁 | `type: command` 的 Stop / SubagentStop / TaskCompleted：评分失败则 JSON `decision: block` 且 **exit 2** | **能，但有上限** | [Hooks](https://code.claude.com/docs/en/hooks)；失败路径必须 exit 2，exit 1 会被当成 hook 坏了并放行（[hooks-guide](https://code.claude.com/docs/en/hooks-guide)） |
| A2 CI / pre-commit | 同一评分脚本在提交或 PR 上跑 | **能越过 Stop 上限** | 默认连续 block 8 次后宿主强制结束回合；可用 `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` 上调（[hooks-guide：Stop hook hits the block cap](https://code.claude.com/docs/en/hooks-guide)） |
| B 独立执行器 | 测试设计不看实现；执行器是真实 runner | 能（对它断言的那一层） | [AgentCoder](https://arxiv.org/abs/2312.13010) |
| C 独立评审会话 | 新 session 只读矩阵 + JSONL + 库表 | 能改结论，拦不住父会话停手 | CoVe factored；用户 08-31 已验证；官方“fresh model try to refute”（[Best practices](https://code.claude.com/docs/en/best-practices.md)） |
| D 变异/空测 | 变异后仍绿 → VACUOUS，永不签字放行 | 能（可变异准则） | [spec-verify](https://github.com/dannwaneri/spec-verify) |
| E 容器隐藏测试 | 补丁必须让 FAIL_TO_PASS / PASS_TO_PASS 过 | 能（该任务） | [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) |
| F `/goal` | 小模型看**对话里已经出现的内容** | **不能**当预言机 | 官方：evaluator **doesn't run commands or read files independently**（[/goal](https://code.claude.com/docs/en/goal)） |
| G 提示词 / Skill | “必须写 JSONL / 不要说完成” | **不能** | 本地已有 test-engineering，仍失败 |
| H 同会话口头纠正 | “这不是完整业务测试” | **不能稳定** | Sharma；CZLHC 父会话 |

Anthropic 把可预测步骤做成带 gate 的 workflow（[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)）。接口完成判定是可预测的：矩阵是否闭合、成功用例是否 `result=1` 且有副作用。

---

## 5. 推荐栈（针对已有 JSONL、仍缺业务测试）

不要再加“必须写 JSONL”的规则。要加一个**先于 Agent 存在、且 Agent 不能改写的评分器**。

### 5.1 测试前：用例矩阵是输入，不是总结

每个接口测试任务先落一个 manifest（YAML/JSON），例如：

```yaml
target: HxycSmmMaterialIssue/CreateFromScan
environment_class: authorized-nonprod
required_cases:
  - id: SCAN-OK
    kind: business-success
    expect: { http: 200, result: 1 }
    side_effects: [issue_row, barcode_allocation, stock_or_explicit_none]
  - id: SCAN-VERIFY
    kind: business-success
    expect: { issue_status: verified }
  - id: SCAN-CANCEL
    kind: recovery
  - id: SCAN-NON-SMM
    kind: negative
  - id: AUTH-MISSING
    kind: auth
```

未出现在矩阵里的 JSONL 行只算探针，不算完成。`blocked`/`skipped` 必须带原因；缺成功路径不得标 complete。

这就是 test-engineering 已经要求、但从未机械执行的东西。

### 5.2 测试中：JSONL 事件形状固定

沿用 `http-api-test.md`：每条执行用例至少 `http.request` + `http.response`（或传输失败）。`kind: business-success` 还必须有 `database.reconciliation` 或等价副作用事件。SetPosition 的 2026-09-01 文件是模板。

机械拒绝：

- 只有 HTTP 200、没有 `result` / `assertion_status`
- `kind=business-success` 但 `result=-1` 或空明细
- 无 `case_id` 且无法映射到矩阵
- 把健康检查、空参数校验计为业务成功

### 5.3 测试后：确定性评分器，不用 LLM 判完成

伪规则：

1. 矩阵每条都有 `passed|failed|blocked|skipped`。
2. `business-success` 至少一条真实 `result=1`，且副作用事件存在。
3. 若成功路径全部 `blocked`（无夹具、无授权写入），总评只能是 `incomplete`，不能是 `passed`。
4. 评分器读文件，不读助手自白。

这对应 Anthropic 的建议：能确定性打分的不要用 model grader。

### 5.4 用 command hook 接到“停止”，再用 CI 越过 8 次上限

Claude Code 只把 **command** hook 当确定性门禁。`prompt` 型 Stop 和 `/goal` 都是小模型看 transcript，实现者写什么它就评什么。

接线要点：

- `Stop`：评分失败输出 `{"decision":"block","reason":"missing SCAN-VERIFY ..."}` 并 **exit 2**。exit 1 等于放行。
- reason 点名下一缺失 case id，不要写“继续测”。8 次预算很紧（[hooks-guide](https://code.claude.com/docs/en/hooks-guide)）。
- 处理 `stop_hook_active`：已在续跑时不要无脑再 block 造成空转；评分仍失败应把缺失 id 写进 reason，或把最终否决交给 CI。
- `TaskCompleted`：同样可阻止勾选完成（[Hooks：Can block?](https://code.claude.com/docs/en/hooks)）。
- **不要**用 `/goal all API tests pass` 当唯一停止条件。

Codex：JSONL 评分接到 `SubagentStop` / executor-verify，与 `.omo/start-work` 的 `executor-done-claim = untrusted` 同一哲学。OpenAI 的 eval 也是扫 `command_execution` 事件，再加只读 rubric，不信最后一段话（[eval-skills](https://developers.openai.com/blog/eval-skills)）。

CI / pre-commit 必须跑同一脚本。Stop 连续 block 8 次后宿主会强制结束回合；Agent 可以耗尽预算然后停。PR 门禁没有这个上限。

当前两套宿主都没接到 API JSONL 评分器。

### 5.5 人只做独立评审，不在同一会话里“再劝一次”

流程：

1. Writer 跑测试、写 JSONL。
2. 评分器 fail-closed。
3. 新会话（或新子代理）只读矩阵 + JSONL + 库表摘要，输出合格/不合格。禁止该评审者改实现。
4. `UNVALIDATABLE`（真随机、第三方沙箱、生产）必须人签字；空测和负向冒充正向不可签字放行（spec-verify 的 VACUOUS vs UNVALIDATABLE）。

用户在 CZLHC 已经证明第 3 步有效。缺的是第 2 步，所以第 3 步变成人工救火。

### 5.6 不要用覆盖率或“跑过 pytest”代替业务完成

Codeframe 的 pytest+coverage hook 能挡住“没跑单测就说通过”，挡不住“跑了空参数 API 就说业务完成”。接口任务的预言机是：单据状态、库存、审批记录、幂等键，不是 HTTP 状态码。

---

## 6. 明确不建议

- 继续加长 CLAUDE.md / Skill。本地已经写过，仍失败。
- 让同一个 Agent 既执行又宣布完成。第二意见必须是新会话或独立脚本（[Best practices](https://code.claude.com/docs/en/best-practices.md)）。
- 把 `/goal` 或 prompt 型 Stop 当预言机。官方写明它不跑命令、不读文件。
- 把 LLM-as-judge 当唯一门禁。可用于“报告是否好读”，不能用于“是否测完”。
- 无夹具时用代码审查顶替正向路径，再标非阻塞。CZLHC 把未验证的生单/审批标成可上线，就是这条路。
- 失败后删测试凑绿。gstack QA 一类“修一次还不绿就删用例”不能搬到业务接口测试。

---

## 7. 建议的最小试点（zksoft-2025）

1. 为 HXYC SMM 选一个已反复翻车的入口（`CreateFromScan` 或 `NewArrivalFromPo`），先写死 6–10 条 required_cases。
2. 写一个 100 行内的 `scripts/grade-api-jsonl.py`：读矩阵 + JSONL，打印 `pass=false` 和缺失 id。
3. Claude Code `type: command` 的 `Stop` hook 调用该脚本；失败 exit 2，reason 列出缺失 id。
4. 同一脚本进 pre-commit / PR CI，避免 8 次 block 后被强制放行。
5. Codex 交付 JSONL 后先跑脚本，再允许 `task_complete`。
6. 回归：CZLHC 7 行负向日志必须 `fail`；SetPosition 8 行在矩阵匹配时可 `pass`。

未做完这五步之前，口头纠正不应被当成流程修复。

---

## 来源

一手（门禁与官方行为）：

- [Best practices：看起来完成就会停；硬度阶梯](https://code.claude.com/docs/en/best-practices.md)
- [Hooks reference：Stop / TaskCompleted 可 block](https://code.claude.com/docs/en/hooks)
- [Hooks guide：exit 2、8 次 cap、`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`](https://code.claude.com/docs/en/hooks-guide)
- [/goal：evaluator 不跑命令、不读文件](https://code.claude.com/docs/en/goal)
- [claude-code#46940 伪造 ALL PASSED / 改分母](https://github.com/anthropics/claude-code/issues/46940)
- [OpenAI eval-skills：JSONL 是过程痕迹](https://developers.openai.com/blog/eval-skills)
- [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)

论文与工具：

- [CoVe, arXiv:2309.11495](https://arxiv.org/abs/2309.11495)
- [AgentCoder, arXiv:2312.13010](https://arxiv.org/abs/2312.13010)
- [EvalPlus, arXiv:2305.01210](https://arxiv.org/abs/2305.01210)
- [Sharma sycophancy, arXiv:2310.13548](https://arxiv.org/abs/2310.13548)
- [Zheng LLM-as-judge, arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
- [spec-verify](https://github.com/dannwaneri/spec-verify)
- [codeframe Enforcement Guide](https://github.com/frankbria/codeframe/blob/main/legacydocs/AI_Development_Enforcement_Guide.md)

二手地图（不引用其统计数字）：[Substack recap](https://yichenguo.substack.com/p/your-ai-code-agent-is-lying-about)；spec-verify 作者教程：[freeCodeCamp](https://www.freecodecamp.org/news/how-to-stop-letting-ai-agents-fake-their-own-tests/)。

本地：`zksoft-2025/logs/CZLHC/*.jsonl`，`d1e9/.../docs/test-results/20260901-*.jsonl`，Claude 会话 `ee2eec90-...`，`.omo/start-work/ledger.jsonl`
