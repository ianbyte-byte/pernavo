# Routing Decision Guide

## Decision Tree

```
用户请求
├── 明确提到某个子 skill 的领域？
│   ├── 是 → 直接路由到该 skill
│   └── 否 → 继续判断
├── 涉及代码变更？
│   ├── 是 → 变更规模？
│   │   ├── 小改动（单文件） → review-mr
│   │   ├── 中等改动（跨模块） → unknowns-field-guide → 编码 → review-mr
│   │   └── 大改动（架构级） → architecture decision → unknowns-field-guide → graph-engineering
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
        → aviation-grade-engineering（测试策略）
        → 编码实施
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
    → aviation-grade-engineering（确保测试覆盖）
    → 分阶段重构
    → review-mr（每阶段审查）
    → 回归验证
```

### 模式 4: 架构升级
```
架构决策（ADR）→ unknowns-field-guide（风险扫描）
              → graph-engineering（并行实施编排）
              → aviation-grade-engineering（韧性验证）
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
| **Low** | 直接编码 → review-mr |
| **Medium** | + unknowns-field-guide（快速扫描） |
| **High** | + unknowns-field-guide（deep path）+ aviation-grade-engineering（完整测试策略） |
| **Critical** | + 所有相关子 skill + 架构决策 ADR + graph-engineering 编排 |
