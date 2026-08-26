# Skill 系统收敛记录（2026-08-26）

## 目标

让 Codex 日常开发优先命中少量可复用入口，而不是在 26 个细分 Skill 中选择低频或外部工具
包装。默认发现目录从 26 项收敛为 7 项；旧实现保存在
`skills-archive/20260826-pre-consolidation/`，可按名称恢复。

## 证据

来源为本机 `/Users/chung/.codex/thread_history_1.sqlite` 的 `userMessage` 行，未计入助手或
系统提示回显。可用以下命令复现聚合报告：

```bash
python3 scripts/skill-usage-report.py \
  --db /Users/chung/.codex/thread_history_1.sqlite \
  --output docs/audit/skill-usage-20260826.json
```

| 用户意图路由 | 去重消息数 | 默认入口 |
|---|---:|---|
| 数据库/SQL/报表 | 87 | `data-work` |
| 代码实现/修复 | 56 | `engineering-workflow` |
| 审查/验证 | 52 | `change-review` |
| 部署/交付/Git | 40 | `engineering-workflow` |
| 记忆/文档/Skills 治理 | 40 | `repository-governance` |
| 性能/超时/资源 | 34 | `performance-work` |

显式旧名称出现最多的是 `codebase-slimming`（21）、`review-mr`（21）、`open-code-review`
（20）、数据库与性能系列（各 10-15 次）。性能系列在历史中还会被系统提示反复回显，因此
报告只将用户消息作为触发证据。

## 默认入口与归档映射

| 默认入口 | 收敛的旧 Skill | 保留的职责 |
|---|---|---|
| `engineering-workflow` | coding-task-controller, engineering-work-system, graph-engineering, unknowns-field-guide, plan-code-change, develop-production-code, verify-change-evidence | 路径选择、发现、计划、单写作者、独立验证、权限边界 |
| `data-work` | database-testing, database-performance | SQL/ORM 静态审查与明确测试库验证 |
| `performance-work` | performance-review, performance-measurement, runtime-performance, web-performance, benchmark-performance | 静态假设、运行时证据、Web Vitals、基准方法 |
| `change-review` | review-mr, open-code-review, sonarqube-review | diff/MR findings；外部质量工具仅在实际可用时报告 |
| `repository-governance` | audit-agent-harness, aviation-grade-engineering, project-capability-engineering, repository-knowledge-gardening | 记忆、文档、配置、能力与可逆治理增量 |
| `codebase-slimming` | 保留 | 基线、试点、行为保持的瘦身批次 |
| `report-writer` | 保留 | 基于证据的正式报告 |

`exa-search`、`pplx-cli`、`gpt55-fusion` 等外部/显式 opt-in 工具不再占用默认发现名额；完整
正文仍在归档中，需恢复时先确认目标工具、授权和安装状态。

## 运行规则

1. 普通开发从 `engineering-workflow` 开始；只有问题明确属于数据库、性能、审查、治理、瘦身
   或报告时才切换入口。
2. 入口正文负责路由和边界，细节按需读取归档参考；不以“Skill 存在”强制创建子 Agent。
   非 trivial 任务最多一个写入者，必要时使用独立只读发现/验证上下文。
3. 静态、已加载、已执行、目标环境证据分开记录；未观察到的运行时行为标记为
   `unverified`。
4. 每次 SkillOpt 迭代只接受有任务夹具、正/负/碰撞触发、可复现报告和人工 adoption 的变更。

## 回滚

从 `skills-archive/20260826-pre-consolidation/<name>/` 恢复指定目录，更新
`tests/skill-trigger-corpus.tsv` 和 README/安装清单，并重新运行
`./scripts/validate-skills.sh`。不要使用通配删除或 `remove --all`。
