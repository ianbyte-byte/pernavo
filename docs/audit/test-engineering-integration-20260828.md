# Test Engineering Skill 集成审计（2026-08-28）

## 目标

把单元、集成、API、功能/系统、回归、验收和发布冒烟测试，以及 white-box、gray-box、
black-box 三种观察方法，接入当前 Skills 系统的一个可复用入口。避免为每个测试层级创建低
复用的独立 Skill。

## 变更

- 新增 `skills/test-engineering/SKILL.md` 作为统一测试路由和证据契约。
- 新增 `skills/test-engineering/references/test-matrix.md`，按需提供层级/方法映射、案例类别和
  跨语言技术栈适配原则。
- `engineering-workflow` 的独立验证阶段接入 `test-engineering`，并保留 `data-work`、
  `performance-work`、`qa`、`codex-security:*` 和 `report-writer` 的专长边界。
- 增加 `tests/skill-trigger-corpus.tsv` 的正向、负向、碰撞三元组，以及
  `tests/skillopt/test-engineering-tasks.json` 的 SkillOpt 夹具。最终夹具包含 6 个 reviewed
  semantic-rubric tasks，按 train/validation/test 各 2 个切分。
- 安装手册和 README 从 7 项/21 cases 更新为 8 项/24 cases。

## SkillOpt-Sleep 最终迭代

固定来源：Microsoft SkillOpt commit
`eb8c1e7bcbccdd80f9d422f12018fcd8e84ce19a`，SkillOpt `0.2.0`。

原 3-task 关键词夹具的真实 Codex dry-run 得到 `1.0 -> 1.0`、0 edits，无法区分关键词满足与
行为质量。最终夹具改为 6 个语义 rubric，覆盖：

- 风险驱动的测试层级选择；
- white-box、gray-box、black-box 方法与 coverage 证据边界；
- Rust/Cargo repository-native stack 选择；
- `data-work`、`qa`、`performance-work`、`codex-security:*` 与实现/review 路由；
- 未授权生产破坏测试与凭据保护；
- C#、Go、TypeScript 多语言仓库中 .NET 工具只作为对应组件示例。

mock dry-run 读取 6 个任务并正确识别 train/validation/test 切分；它只验证夹具结构，不作为
模型质量证据。

真实 Codex CLI `0.149.1` / `gpt-5.6-sol` 回放曾成功取得部分结果，但本地 CC Switch 的
AIwelink provider 随后对 `/responses` 连续返回 HTTP 503。该次运行包含空响应和伪 0 分，已
中止并排除在采纳依据之外。轻量 Codex 模型也复现相同 503，说明问题不在 Skill 内容。

最终有效命令使用已认证的 Claude Code `2.1.246` / Sonnet，保持同一任务、偏好和编辑预算：

```bash
uvx --from git+https://github.com/microsoft/skillopt.git skillopt-sleep run \
  --project /Users/chung/Developer/Code/loongclaude \
  --backend claude --model sonnet \
  --target-skill-path skills/test-engineering/SKILL.md \
  --tasks-file tests/skillopt/test-engineering-tasks.json \
  --edit-budget 2 --progress \
  --preferences 'Keep test-engineering language- and framework-agnostic. Treat .NET, Python, JavaScript/TypeScript, Java, Go, Rust, and other tools as optional repository-specific examples, never defaults. Preserve routing boundaries and evidence honesty. Prefer concise edits and progressive disclosure.' \
  --json
```

没有使用 `--auto-adopt`。结果：

| 证据 | hard | soft / mixed |
|---|---:|---:|
| validation baseline | 1.00 | soft 0.90 / mixed 0.95 |
| validation candidate | 1.00 | soft 0.90 / mixed 0.95 |
| final test (`te5`, `te6`) | 1.00 | soft 0.95 |

验证任务 mixed score 分别为 repository-native Rust `0.975`、专项路由 `0.925`；最终留出任务
soft score 分别为生产权限 `0.98`、多语言/.NET 示例边界 `0.92`。共使用 21,623 estimated
tokens，6 个任务均无调用错误。

SkillOpt 返回 0 skill edits、0 memory edits，`accepted=false`、`gate_action=reject`，因为候选
与基线同为 `0.95`，没有实质改善。未执行 adopt，也未改写 `test-engineering` 正文；采纳的是更
有区分力的评估夹具，而不是为了产生 diff 强行加入提示词。

## 验证

- `quick_validate.py`：8 个 Skill 均通过。
- `scripts/validate-skills.sh`：8 个 frontmatter、链接、README 条目和触发三元组通过，语料
  共 24 cases。
- `python3 -m unittest discover -s tests -p 'test_*.py'`：61 tests passed。
- `npx --yes skills add . --list`：列出 8 个入口，包含 `test-engineering`。
- SkillOpt：6 个 semantic-rubric tasks；validation 和 final test hard gate 均为 1.00。

## 覆盖边界

上述证据最高到 source/installed/static validation，加上 SkillOpt 隔离模型回放。SkillOpt 分数
是 rubric judge 对生成回答的评估，不等于真实仓库命令、数据库、浏览器、负载或生产环境测试。
尚未在独立宿主新会话中执行完整 24-case runtime corpus，因此正文 loaded、executed、
target-observed 和真实业务目标环境行为仍为 `unverified`。测试工具、数据库目标、凭据、CI 和
UAT 仍须按当前仓库和用户授权解析，不能由 Skill 名称推断。

## 回滚

删除 `skills/test-engineering/`，恢复 `engineering-workflow` 的验证段，移除新增的三条触发
语料和 SkillOpt 夹具，并将 README/AI_INSTALL 的 8/24 恢复为对应发布集合；最后运行
`./scripts/validate-skills.sh`。不删除其他测试或外部来源 Skill。
