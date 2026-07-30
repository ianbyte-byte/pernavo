---
name: aviation-grade-engineering
description: >
  Design systemic software reliability with risk-driven assurance, SLOs and error budgets,
  observability, resilience patterns such as retries and circuit breakers, layered test and
  CI gates, and blameless postmortems. Use for reliability programs, production stability,
  incident reduction, 航空级可靠性, SRE, 可观测性, 韧性设计, or 质量门禁. Do not trigger for an
  ordinary feature or bug fix, one diff review, or production-code implementation unless
  reliability engineering is the primary task.
---

# Aviation-Grade Engineering

航空软件实现极高可靠性，不是靠"避免所有故障"，而是靠系统性的预防、纵深防御、严格验证、韧性设计、可观测性和从失败中学习。本 skill 将这些原则转化为实用的、风险驱动的软件工程实践——不是完整的 DO-178C 认证（对大多数项目成本过高），而是其背后的工程思维。

## Overview

可靠性不是靠"多测几次"或"快速修 bug"堆出来的，而是靠系统性的工程过程、防御纵深和持续学习。本 skill 帮助团队在有限资源下，将航空级工程思维落地到日常软件开发中。

核心洞察：**飞机不是"不出故障"，而是"出了故障还能飞"。** 软件系统也一样——关键不是追求零 bug，而是设计出能优雅降级的系统。

## When to Use

- 用户想提升系统可靠性或减少线上事故
- 为服务设定 SLO、Error Budget 或可观测性体系
- 设计韧性模式（断路器、重试、优雅降级）
- 建立或改进 CI/CD 质量门禁
- 事故后进行 Postmortem 复盘
- 规划测试策略升级（单元 → 集成 → E2E 金字塔）
- 对高影响模块做风险评估（医疗数据、支付、认证）
- 任何关于"如何让软件更可靠"的讨论

## Core Principles

1. **Risk-Driven Rigor（风险驱动）** — 不是所有代码都需要相同 rigor。高影响模块（医疗数据、支付、安全、数据一致性）用最高验证标准，低风险内部工具快速迭代。
2. **Defense in Depth（纵深防御）** — 多层独立保护。没有单一故障点能导致灾难。
3. **Resilience Over Perfection（韧性优于完美）** — 系统一定会出错。设计优雅降级，而非追求零 bug。"飞机一台引擎故障不会坠机——靠剩余引擎继续飞。"
4. **Observable by Default（默认可观测）** — 看不到就无法修复。结构化日志、指标、分布式追踪不是生产服务的可选项。
5. **Learn Systematically（系统性学习）** — 每次事故都是学习机会。Blameless postmortem 找系统性问题，不找个人替罪羊。

## Workflow

### Step 1: Risk Assessment（风险评估）

- 识别范围内的系统/模块
- 使用 Risk Matrix 分类风险等级（见 [risk-matrix-template.md](references/risk-matrix-template.md)）
- 优先处理高风险区域

对每个模块回答：
- 如果这个模块失败会发生什么？（数据丢失？用户影响？收入损失？）
- 谁受影响？（患者？所有用户？内部员工？）
- 故障可逆吗？（能回滚吗？数据会永久损坏吗？）
- 有合规要求吗？（HIPAA？PCI-DSS？GDPR？）
- 代码变更频率？（稳定核心 vs. 频繁变更）

### Step 2: Test Strategy Design（测试策略）

应用测试金字塔：

| 层级 | 覆盖目标 | 工具建议 |
|------|----------|----------|
| **单元测试** | 高风险逻辑 80%+ 覆盖率；复杂算法用属性测试（FsCheck, Hypothesis） | xUnit, pytest, FsCheck |
| **集成测试** | 真实依赖（Testcontainers）；验证存储过程、API 契约、数据一致性 | Testcontainers, tSQLt |
| **E2E 测试** | 仅覆盖关键用户旅程（登录 → 核心流程 → 输出） | Playwright, Cypress |
| **静态分析** | SAST、lint、类型检查作为 CI 门禁 | SonarQube, Roslyn analyzers |

- 建立需求-测试可追溯性（即使只是 Markdown + Git + 测试链接的轻量方式）
- 高风险模块做更正式的设计和验证

### Step 3: Observability Setup（可观测性建设）

- 为关键服务定义 SLO（见 [slo-checklist.md](references/slo-checklist.md)）
- 实现结构化日志 + 指标 + 分布式追踪（推荐 OpenTelemetry）
- 基于 SLO 消耗速率告警，不仅仅是"服务 down"
- 为已知故障模式编写 runbook

关键指标维度：
- **Availability**: 例如 99.95%（30 天滚动）
- **Latency P50/P99**: 例如 < 200ms / < 2s
- **Error rate**: 例如 < 0.1%
- **Throughput**: 最低可接受吞吐量

### Step 4: Resilience Patterns（韧性模式）

- **断路器**: 故障时快速失败，避免级联崩溃（.NET: Polly; Java: resilience4j）
- **重试 + 退避**: 指数退避 + 抖动，避免重试风暴
- **幂等性**: 所有状态变更操作必须幂等
- **优雅降级**: 哪些功能可以不可用而不导致整个系统崩溃？
- **舱壁隔离**: 将故障限制在起源模块内

### Step 5: CI/CD Quality Gates（质量门禁）

- **Branch protection**: lint + build + 单元测试 + 集成测试 + 静态分析全部通过才能合并
- **发布策略**: Feature Flags + Canary/蓝绿部署 + 即时回滚
- **Infrastructure as Code**: 保证环境一致性
- **Pre-commit hooks**: 强制格式化和基础检查

### Step 6: Incident Response & Learning（事故响应与学习）

- 每次事故后（即使小故障）进行 blameless postmortem（见 [postmortem-template.md](references/postmortem-template.md)）
- 追踪 DORA metrics：部署频率、变更失败率、MTTR、lead time
- 将学习反馈到测试覆盖和监控中

## Rules

- **NEVER** 对非受监管项目推荐完整 DO-178C/IEC 62304 认证——成本过高，不实际
- **ALWAYS** 在开处方前先做风险评估
- **ALWAYS** 建议渐进式采用——不要试图一次实施所有东西
- 优先使用成熟工具和模式（Polly, OpenTelemetry, Testcontainers），而非自建
- **混沌工程**需要可观测性和回滚能力作为前提——永远不要向不可观测的系统注入故障
- AI 辅助代码生成可以，但**关键逻辑上永远不要跳过 review 和测试**
- Postmortem 必须是 blameless 的——聚焦系统性问题，不聚焦个人

## Output Format

完成评估或规划后，输出应包含：

1. **Risk Classification** — 哪些模块是高/中/低风险
2. **Priority Actions** — 按影响排序的 top 3-5 具体下一步
3. **Quick Wins** — 本周就能做的事
4. **Long-term Roadmap** — 分阶段采用计划
5. **Tool Recommendations** — 匹配项目技术栈的具体工具

## When Not To Use

- 纯前端 UI 样式调整（用常规 code review 即可）
- 原型/一次性脚本（overhead 不值得）
- 用户只是想讨论工程理念而非制定具体计划

## References

- 风险评估矩阵: [references/risk-matrix-template.md](references/risk-matrix-template.md)
- SLO 定义清单: [references/slo-checklist.md](references/slo-checklist.md)
- Blameless Postmortem 模板: [references/postmortem-template.md](references/postmortem-template.md)

## Related Skills

- [review-mr](../review-mr/SKILL.md) — 代码审查（质量门禁的一部分）
- [codebase-slimming](../codebase-slimming/SKILL.md) — 代码库瘦身（提升可维护性）
- [unknowns-field-guide](../unknowns-field-guide/SKILL.md) — 编码前发现未知风险
