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
  `tests/skillopt/test-engineering-tasks.json` 的 SkillOpt 夹具。
- 安装手册和 README 从 7 项/21 cases 更新为 8 项/24 cases。

## SkillOpt-Sleep

命令：

```bash
uvx --from git+https://github.com/microsoft/skillopt.git skillopt-sleep dry-run \
  --project /Users/chung/Developer/Code/loongclaude \
  --backend mock \
  --target-skill-path skills/test-engineering/SKILL.md \
  --tasks-file tests/skillopt/test-engineering-tasks.json \
  --edit-budget 0 --json
```

结果：读取 3 个 reviewed tasks，`accepted=false`、`gate_action=reject`、`n_accepted_edits=0`，
没有自动改写或采纳。mock backend 只证明夹具和门禁可运行，不产生模型质量分数，也不证明宿主
runtime 触发；因此保留人工编写版本。

## 验证

- `quick_validate.py`：8 个 Skill 均通过。
- `scripts/validate-skills.sh`：8 个 frontmatter、链接、README 条目和触发三元组通过，语料
  共 24 cases。
- `python3 -m unittest discover -s tests -p 'test_*.py'`：61 tests passed。
- `npx --yes skills add . --list`：列出 8 个入口，包含 `test-engineering`。

## 覆盖边界

上述证据最高到 source/installed/static validation。尚未在独立宿主新会话中执行完整 24-case
runtime corpus，因此正文 loaded、executed、target-observed 和真实业务目标环境行为仍
为 `unverified`。测试工具、数据库目标、凭据、CI 和 UAT 仍须按当前仓库和用户授权解析，不能
由 Skill 名称推断。

## 回滚

删除 `skills/test-engineering/`，恢复 `engineering-workflow` 的验证段，移除新增的三条触发
语料和 SkillOpt 夹具，并将 README/AI_INSTALL 的 8/24 恢复为对应发布集合；最后运行
`./scripts/validate-skills.sh`。不删除其他测试或外部来源 Skill。
