# Routing Decision Guide

## Decision Tree

```
用户请求
├── 明确提到某个子 skill 的领域？
│   ├── 是 → 直接路由到该 skill
│   └── 否 → 继续判断
├── 涉及代码变更？
│   ├── 是 → 变更规模？
│   │   ├── 纯文案/注释等平凡改动 → 聚焦修改与验证
│   │   ├── 一般生产改动 → coding-task-controller → unknowns-field-guide → develop-production-code → review-mr
│   │   └── 架构级改动 → architecture decision → coding-task-controller → unknowns-field-guide → develop-production-code
│   │       └── 仅在确需独立上下文或条件路由时加入 graph-engineering
│   └── 否 → 继续判断
├── 涉及系统可靠性？
│   ├── 是 → aviation-grade-engineering
│   └── 否 → 继续判断
├── 涉及发布/部署？
│   ├── 是 → Release Ops 子流程
│   └── 否 → 继续判断
├── 涉及事后复盘/流程改进？
│   ├── 是 → Continuous Improvement 子流程
│   └── 否 → 继续判断
├── 想评估工程实践水平？
│   ├── 是 → 工程健康度检查
│   └── 否 → 直接回答/讨论
```

## Common Routing Patterns

### 模式 1: 新功能开发
```
需求分析 → unknowns-field-guide（风险扫描）
        → develop-production-code（编码与证据边界）
        → aviation-grade-engineering（仅当系统性可靠性属于范围）
        → review-mr（代码审查）
        → Release Ops（发布）
```

### 模式 2: 事故响应
```
事故检测 → 紧急修复
        → aviation-grade-engineering（postmortem 模板）
        → Continuous Improvement（流程改进）
        → aviation-grade-engineering（加强监控/测试）
```

### 模式 3: 代码库重构
```
评估 → codebase-slimming（识别重复/死代码）
    → 分阶段重构
    → review-mr（每阶段审查）
    → aviation-grade-engineering（仅当可靠性或测试策略升级属于范围）
    → 回归验证
```

### 模式 4: 架构升级
```
架构决策（ADR）→ unknowns-field-guide（风险扫描）
              → develop-production-code（生产实现）
              → graph-engineering（仅在需要并行或条件路由时）
              → aviation-grade-engineering（仅在需要韧性验证时）
              → Release Ops（安全发布）
```

### 模式 5: 工程实践评估
```
健康度检查（6 维度评分）
→ 识别短板
→ 路由到对应子 skill
→ 制定改进计划
→ 定期复查
```

## Risk-Based Routing Modifiers

根据任务风险调整路由深度：

| 风险等级 | 路由调整 |
|----------|----------|
| **Low** | 平凡改动走聚焦修改与验证；非平凡改动仍由 controller 分级 |
| **Medium** | coding-task-controller + unknowns-field-guide（default）+ 对应实施 Skill |
| **High** | coding-task-controller + unknowns-field-guide（deep path）+ 对应实施/领域 Skill |
| **Critical** | 在 High 基础上加入 ADR；仅按实际需要加入可靠性或 graph 编排，不强制加载所有 Skill |
