# Skills 使用审计（2026-08-28）

## 结论

当天共有 16 个真实用户任务进入统计。会话按 `session_id` 合并续接文件，并排除
SkillOpt 评分器、评测器和只有系统注入文本的会话。

| Skill | 适用任务 | 实际读取 | 漏触发 |
| --- | ---: | ---: | ---: |
| `engineering-workflow` | 12 | 3 | 9 |
| `test-engineering` | 11 | 5 | 6 |
| `data-work` | 9 | 4 | 5 |
| `change-review` | 6 | 0 | 6 |
| `performance-work` | 5 | 0 | 5 |
| `repository-governance` | 1 | 1 | 0 |
| `codebase-slimming` | 1 | 1 | 0 |

适用不是“Skill 名称出现”，而是用户任务文本命中该入口的边界关键词；读取只有在会话
命令证据中发现 `cat`、`sed`、`head` 或 `tail` 明确读取对应 `SKILL.md` 时才计数。报告不把
系统提供的 available-skills 列表、用户显式提名或助手复述当成加载证据。

## 观察

- `engineering-workflow` 的适用面最大，但普通功能、修复、发布和接口开发中只有少数会话
  留下入口正文读取证据。应继续作为普通开发的默认入口，并在触发语料和运行时抽样中重点
  验证，而不是拆出更多实现类 Skill。
- `test-engineering` 在今天新增后已经被真实测试、复现、验收和 Skill 系统治理任务读取；
  早于安装时间的测试任务不能反推其设计失败。它覆盖 unit/integration/API/
  functional/system/regression/UAT/release-smoke，并以 white/gray/black-box 作为观察方法，
  不绑定编程语言；`.NET`、xUnit 等只能作为仓库匹配示例。
- `data-work` 已在 SQL、测试库和报表任务中出现，但仍有 5 个适用任务未留下读取证据，
  说明数据库入口需要在真实任务中持续抽样，而不是再增加 `database-*` 碎片。
- `performance-work` 与 `change-review` 的 0 次读取是明显的运行时漏触发信号。当天确有
  性能、审查和重构请求；这两个入口暂不删除，因为适用任务存在，优先修复触发路径并用
  负向/碰撞样本防止泛化。
- `repository-governance`、`codebase-slimming` 在相应治理和瘦身请求中被读取，当前保留
  有实际依据。

## SkillOpt 迭代

本轮使用仓库锁定的 Microsoft SkillOpt `0.2.0`（commit
`eb8c1e7bcbccdd80f9d422f12018fcd8e84ce19a`）复核 `test-engineering` 的 6 个 reviewed
semantic tasks，覆盖风险驱动层级、三种观察方法、跨语言仓库原生工具、专长路由、生产
破坏测试权限及 `.NET` 仅作示例。validation 和 final hard gate 均为 `1.00`，候选没有
超过基线，因此 `0 skill edits`、`accepted=false`、`gate_action=reject`。按工程化门槛
不强行制造正文 diff；改进保留在更有区分力的评测夹具和本次真实用量观测器。

针对当天漏触发最多的 `engineering-workflow` 又执行了一轮同版本 SkillOpt 回放（3 个
reviewed tasks，Claude Sonnet backend）。baseline/candidate 均为 `1.00`，final held-out
task 无回归但无增益，`accepted=false`、`gate_action=reject`、`0 edits`；因此没有为改变
文件数量而改写入口正文。

## 可复现命令

```bash
python3 scripts/skill-usage-report.py \
  --db /Users/chung/.codex/thread_history_1.sqlite \
  --sessions-root /Users/chung/.codex/sessions/2026/08/28 \
  --date 2026-08-28 --timezone Asia/Shanghai \
  --output docs/audit/skill-usage-20260828.json
```

## 限制

命令读取证据证明了 `SKILL.md` 被读取，不证明模型完全遵循正文，也不证明目标数据库、
浏览器、负载环境或生产行为已经验证。当前报告只覆盖本机 Codex JSONL 会话；未观察到的
执行均标为漏触发或未验证，不据此删除低频专项入口。
