---
name: engineering-work-system
description: >
  Route or assess work across multiple engineering domains and choose specialist Skills.
  Use only when the user asks which process or Skill to use, wants a cross-domain engineering
  workflow or health assessment, or needs architecture, release, incident, DORA, and
  continuous-improvement orchestration. Prefer the direct specialist for a clear reliability,
  review, slimming, discovery, production-coding, or agent-topology task. Do not trigger for
  ordinary implementation.
---

# Engineering Work System

工程工作系统的顶层编排器。根据当前任务类型，路由到最合适的子 skill，确保工程实践覆盖完整、不重叠、不遗漏。

核心理念：**不是一个 skill 做所有事，而是一组 skill 各司其职，由编排器统一调度。**

## Overview

本 skill 是工程工作系统的入口。它不直接执行具体工程实践，而是：
1. 识别当前任务的类型和风险等级
2. 路由到一个或多个子 skill
3. 确保各 skill 之间的协作不冲突、不遗漏
4. 在子 skill 未覆盖的领域提供补充指导

## When to Use

- 不确定该用哪个工程 skill 时
- 需要跨多个工程维度的综合建议时
- 想建立或评估团队的完整工程实践体系时
- 需要编排多个 skill 协同工作时

## Routing Table

根据任务类型路由到对应子 skill：

| 任务类型 | 触发场景 | 路由目标 | 优先级 |
|----------|----------|----------|--------|
| **可靠性工程** | 提升系统可靠性、SRE、可观测性、韧性设计、测试策略 | [aviation-grade-engineering](../aviation-grade-engineering/SKILL.md) | Primary |
| **代码审查** | MR/PR 审查、代码质量检查、安全审查 | [review-mr](../review-mr/SKILL.md) | Primary |
| **代码库治理** | 减少重复、代码瘦身、可维护性提升 | [codebase-slimming](../codebase-slimming/SKILL.md) | Primary |
| **编码前风险发现** | 非平凡任务实施前的 unknowns 发现、风险评估 | [unknowns-field-guide](../unknowns-field-guide/SKILL.md) | Primary |
| **任务治理** | 编码任务分级、流程合规、风险路由 | [coding-task-controller](../coding-task-controller/SKILL.md) | Primary |
| **生产编码** | 将功能、修复、重构或 AI 生成代码落入真实生产系统 | [develop-production-code](../develop-production-code/SKILL.md) | Primary |
| **多 Agent 编排** | 需要并行专家协作、审计路由、复杂工作流 | [graph-engineering](../graph-engineering/SKILL.md) | Primary |
| **架构决策** | 技术选型、系统设计、ADR、权衡分析 | 内置（见 Architecture Decision 子流程） | Primary |
| **发布管理** | CI/CD 优化、发布策略、回滚、feature flags | 内置（见 Release Ops 子流程） | Primary |
| **持续改进** | DORA metrics、团队复盘、流程优化 | 内置（见 Continuous Improvement 子流程） | Primary |

## Workflow

### Step 1: 任务分类

收到用户请求后，先分类任务类型：

1. **单一维度任务** — 明确属于某个子 skill 的领域 → 直接路由
2. **跨维度任务** — 涉及多个子 skill → 按依赖顺序编排
3. **评估型任务** — 用户想评估当前工程实践水平 → 执行工程健康度检查

### Step 2: 路由执行

**单一维度**：直接调用对应子 skill，不做额外干预。

**跨维度**：确定执行顺序和依赖关系。常见组合：
- 新功能开发：`unknowns-field-guide` → `develop-production-code` → `review-mr`；仅在可靠性工程属于任务范围时加入 `aviation-grade-engineering`
- 事故响应：`aviation-grade-engineering`（postmortem）→ `continuous improvement`（流程改进）
- 代码库重构：`codebase-slimming` → `review-mr`；仅在系统性可靠性或测试策略升级属于任务范围时加入 `aviation-grade-engineering`
- 架构升级：`architecture decision` → `unknowns-field-guide` → `graph-engineering`（并行实施）

**评估型**：执行下面的工程健康度检查。

### Step 3: 工程健康度检查（评估型任务）

对以下 6 个维度打分（1-5），生成雷达图式报告：

| 维度 | 评估内容 | 对应 skill |
|------|----------|-----------|
| **测试防御** | 测试金字塔完整度、覆盖率、自动化程度 | aviation-grade-engineering |
| **可观测性** | 日志、指标、追踪、告警、SLO | aviation-grade-engineering |
| **韧性设计** | 断路器、重试、降级、幂等、舱壁隔离 | aviation-grade-engineering |
| **发布质量** | CI/CD 门禁、发布策略、回滚能力 | Release Ops 子流程 |
| **代码健康** | 重复度、复杂度、可维护性 | codebase-slimming + review-mr |
| **学习闭环** | Postmortem 文化、DORA metrics、流程改进 | Continuous Improvement 子流程 |

输出格式：
1. 各维度评分 + 简要说明
2. 最大短板（最需要改进的 1-2 个维度）
3. 推荐路由到哪些子 skill
4. Quick wins（本周能做的事）

---

## 内置子流程

以下领域没有独立 skill，由编排器直接覆盖：

### Architecture Decision（架构决策）

当任务涉及技术选型或系统设计时：

1. **明确决策范围** — 什么需要决策？约束条件是什么？
2. **收集选项** — 至少 2-3 个候选方案
3. **权衡分析** — 对每个方案评估：
   - 复杂度 vs. 收益
   - 团队熟悉度
   - 长期维护成本
   - 可逆性（单向门 vs. 双向门）
4. **记录 ADR** — 用以下格式记录决策：

```markdown
# ADR-NNN: [标题]

## Status
Proposed / Accepted / Deprecated / Superseded

## Context
什么情况下需要做这个决策？

## Decision
选择了什么方案？

## Consequences
- 正面影响：
- 负面影响：
- 风险：
- 后续行动：
```

5. **关联风险** — 如果决策涉及高风险模块，路由到 `unknowns-field-guide` 做进一步风险扫描

### Release Ops（发布管理）

当任务涉及发布流程优化时：

1. **评估当前发布流程**：
   - 发布频率？（daily/weekly/monthly/ad-hoc）
   - 发布成功率？
   - 回滚时间？
   - 是否有 feature flags？

2. **推荐发布策略**（按成熟度递进）：

| 阶段 | 策略 | 适用场景 |
|------|------|----------|
| Level 1 | 手动发布 + checklist | 早期项目、小团队 |
| Level 2 | CI 自动化 + 手动触发部署 | 成长期项目 |
| Level 3 | CD + 自动部署到 staging + 手动生产 | 中等风险项目 |
| Level 4 | CD + Canary/蓝绿 + Feature Flags | 高风险/高可用项目 |
| Level 5 | CD + 自动回滚 + 混沌验证 | 关键业务系统 |

3. **质量门禁设计**：
   - Pre-merge: lint + build + unit tests + integration tests + static analysis
   - Pre-deploy: smoke tests + contract tests + security scan
   - Post-deploy: health checks + canary metrics + synthetic monitoring

4. **回滚预案**：
   - 每次发布前必须有回滚计划
   - 回滚时间目标 < 5 分钟
   - 数据库变更必须可逆（forward-only 变更需要 migration plan）

### Continuous Improvement（持续改进）

当任务涉及团队流程优化或事后复盘时：

1. **DORA Metrics 追踪**：

| 指标 | 定义 | Elite 目标 |
|------|------|-----------|
| 部署频率 | 代码成功部署到生产的频率 | On-demand (多次/天) |
| 变更 Lead Time | 从 commit 到生产的时间 | < 1 小时 |
| 变更失败率 | 导致故障的部署占比 | 0-15% |
| 恢复时间 (MTTR) | 从故障发现到恢复的时间 | < 1 小时 |

2. **Postmortem 闭环**：
   - 事故 → Blameless Postmortem（路由到 `aviation-grade-engineering` 的 postmortem 模板）
   - Action items → 追踪到完成
   - 模式识别 → 同类事故重复出现？说明系统性问题
   - 反馈到测试/监控 → 防止复发

3. **定期回顾节奏**：

| 频率 | 活动 | 参与者 |
|------|------|--------|
| 每次事故 | Blameless Postmortem | 相关工程师 |
| 每两周 | 工程回顾（DORA 指标 review） | 团队 |
| 每月 | 技术债务盘点 + 优先级排序 | Tech Lead + 团队 |
| 每季度 | 工程实践全面评估（用健康度检查） | 团队 + 管理层 |

---

## Rules

- **编排器不替代子 skill** — 如果任务明确属于某个子 skill 的领域，直接路由，不要重新发明轮子
- **先分类再行动** — 永远先确定任务类型，再决定路由
- **跨维度任务注意依赖** — 确定执行顺序，不要并行执行有依赖关系的 skill
- **评估型任务要量化** — 健康度检查必须给出具体评分，不要模糊建议
- **保持轻量** — 编排器本身不应成为负担，简单任务直接路由即可
- **ADR 必须记录** — 架构决策如果不记录，等于没做

## Output Format

根据任务类型输出不同格式：

**路由型**：
1. 任务分类结果
2. 推荐路由（1 个或多个子 skill）
3. 执行顺序（如果是跨维度）
4. 简要说明为什么这样路由

**评估型**：
1. 6 维度评分雷达图（文字描述）
2. 最大短板 + 改进建议
3. 推荐路由
4. Quick wins

**决策型**：
1. ADR 文档（按模板格式）
2. 关联风险（是否需要路由到 unknowns-field-guide）

## When Not To Use

- 任务明确属于某个子 skill 的领域 → 直接用那个子 skill，不需要编排器
- 纯代码实现任务 → 直接写代码
- 用户只是想聊天工程理念 → 直接讨论

## References

- 路由决策指南: [references/routing-guide.md](references/routing-guide.md)

## Related Skills

- [aviation-grade-engineering](../aviation-grade-engineering/SKILL.md) — 可靠性工程
- [review-mr](../review-mr/SKILL.md) — 代码审查
- [codebase-slimming](../codebase-slimming/SKILL.md) — 代码库治理
- [unknowns-field-guide](../unknowns-field-guide/SKILL.md) — 编码前风险发现
- [coding-task-controller](../coding-task-controller/SKILL.md) — 任务治理
- [develop-production-code](../develop-production-code/SKILL.md) — 生产编码与证据边界
- [graph-engineering](../graph-engineering/SKILL.md) — 多 Agent 编排
