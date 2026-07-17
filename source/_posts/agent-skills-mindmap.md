---
title: "Agent Skills — AI 编码的生产级工程技能体系"
date: 2026-07-16 17:00:00
tags: [AI, Agent, Skill, 软件工程, 开发效率, Claude Code]
categories: [技术, AI编码]
---

## 概述

[agent-skills](https://github.com/1whilstlerrrr/agent-skills) 是 Addy Osmani 开源的一套面向 AI 编码 agent 的生产级工程技能库。它将资深工程师的完整开发流程编码为 24 个可复用的 Skill + 8 个 Slash Command，覆盖从需求定义到发布上线的全生命周期。

```
  DEFINE          PLAN           BUILD          VERIFY         REVIEW          SHIP
 ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
 │ Idea │ ───▶ │ Spec │ ───▶ │ Code │ ───▶ │ Test │ ───▶ │  QA  │ ───▶ │  Go  │
 │Refine│      │  PRD │      │ Impl │      │Debug │      │ Gate │      │ Live │
 └──────┘      └──────┘      └──────┘      └──────┘      └──────┘      └──────┘
  /spec          /plan          /build        /test         /review       /ship
```

<!-- more -->

---

## 一、思维导图总览

{% markmap %}
- agent-skills
  - 8 Slash Commands（入口层）
    - /spec → 先写 spec 再写代码
    - /plan → 拆分为小任务
    - /build → 逐步实现（/build auto 全自动）
    - /test → TDD 红→绿→重构工作流
    - /review → 五轴代码审查
    - /webperf → Web 性能审计
    - /code-simplify → 简化代码
    - /ship → 预发布检查清单
  - 4 Agent Personas（审查角色）
    - code-reviewer → 五轴代码审查
    - test-engineer → 测试质量评估
    - security-auditor → 安全审计
    - web-performance-auditor → Web 性能审计
  - 24 Skills（能力层）
    - DEFINE（定义）
      - idea-refine → 需求澄清，发散→收敛
      - interview-me → 一问一答式需求访谈
      - spec-driven-development → 先写 spec 再写代码
      - doubt-driven-development → 高正确性场景的对抗审查
    - PLAN（规划）
      - planning-and-task-breakdown → 任务拆解 + 依赖排序
      - api-and-interface-design → API / REST / GraphQL
      - frontend-ui-engineering → 生产级 UI 构建
      - documentation-and-adrs → ADR + 技术文档
    - BUILD（构建）
      - incremental-implementation → 增量实现，一次一小步
      - test-driven-development → 红→绿→重构
      - source-driven-development → 以官方文档为权威
      - context-engineering → Agent 上下文优化
      - using-agent-skills → 元技能：技能发现与调用
    - VERIFY（验证）
      - code-review-and-quality → 多维代码审查
      - browser-testing-with-devtools → DevTools 真实浏览器测试
      - security-and-hardening → 安全加固
      - performance-optimization → 性能优化
      - code-simplification → 清晰度 > 聪明度
      - observability-and-instrumentation → 日志 / 指标 / 追踪
    - SHIP（发布）
      - shipping-and-launch → 预发布检查 + 发布策略
      - ci-cd-and-automation → CI/CD 流水线
      - git-workflow-and-versioning → Git 工作流 + 语义版本
      - deprecation-and-migration → 废弃 + 迁移管理
  - References（参考清单）
    - definition-of-done → 完成的定义
    - testing-patterns → 测试模式
    - security-checklist → 安全检查清单
    - performance-checklist → 性能检查清单
    - accessibility-checklist → 无障碍检查清单
    - observability-checklist → 可观测性检查清单
    - orchestration-patterns → 编排模式
  - Docs（文档）
    - getting-started → 快速上手
    - skill-anatomy → Skill 结构规范
    - comparison → vs Superpowers vs Matt Pocock
    - tool-setup × 8 → 各种工具配置指南
  - Hooks + Evals（钩子与评估）
    - SDD-CACHE → spec 缓存策略
    - SIMPLIFY-IGNORE → 简化忽略规则
    - Evals → 评估框架
{% endmarkmap %}

---

## 二、Skill 的标准结构

每个 Skill 位于 `skills/<skill-name>/SKILL.md`，遵循统一格式：

```
skill-name/
├── SKILL.md              ← 必需：Skill 定义（≤500行）
├── scripts/              ← 可选：可执行脚本
└── supporting-file.md    ← 可选：按需加载的参考资料
```

**SKILL.md 前端元数据**：
- `name`: `lowercase-hyphen-separated`
- `description`: 既说明功能，也说明触发条件（最大 1024 字符）

**六大标准章节**：
1. **Overview** — 一句话概述
2. **When to Use** — 触发条件 + 排除场景
3. **Core Process** — 核心工作流（具名分步，有代码示例）
4. **Common Rationalizations** — "反合理化表"（Agent 常见的偷懒借口 → 为什么不对）
5. **Red Flags** — 违反 Skill 的可观察信号
6. **Verification** — 可验证的退出检查清单

**四大原则**：
- **渐进加载**：只在使用时加载完整内容，平时只有 name + description 驻留在上下文中
- **过程优于知识**：Skill 是工作流，不是参考文档——要步骤，不要 facts
- **具体优于笼统**：`npm test` 明确过 "确保测试通过"
- **证据优于假设**：每个验证项都必须有可检查的产出

---

## 三、对 szxa-next-harness 的启发

结合物资安全管控模块的实战经验，agent-skills 体系在以下方面可以直接借鉴：

### 3.1 可以引入的 Skill

| agent-skills Skill | szxa-next-harness 的对应场景 |
|-------------------|---------------------------|
| `spec-driven-development` | 过程1（需求规格化 → 原型确认） |
| `planning-and-task-breakdown` | 过程3（实施计划 → DAG 生成） |
| `test-driven-development` | 过程4（编码前先写测试） |
| `code-review-and-quality` | backend-code-reviewer / frontend-code-reviewer |
| `incremental-implementation` | 拆分子任务 DAG，逐个实现 |
| `doubt-driven-development` | GAN 循环中的审查机制 |
| `api-and-interface-design` | 详细设计中 §5（API 设计） |

### 3.2 可以引入的机制

1. **反合理化表**：现在 agent 偶尔会"这个太简单了，跳过测试吧"→ 加上 counter-argument
2. **Skill 渐进加载**：现在的 Agent prompt 一次注入太多内容 → 按需加载
3. **验证清单**：每个阶段结束加 checklist，而不是靠人逐条回忆
4. **红牌警告**：定义"如果出现 XX 行为，说明 Agent 偏离了规范"的可观测信号

### 3.3 与现有体系的关系

```
agent-skills                   szxa-next-harness
─────────────                  ─────────────────
/spec                          /skill spec-writer
/plan                          /skill plan-writer
/build                         Agent(backend-coder)
/test                          Skill("backend-test")
/review                        Agent(backend-code-reviewer)
/ship                          Skill("backend-deploy-check")

差异：
agent-skills 是通用框架（所有语言、所有工具）
szxa-next 是特定于 C#/React/Tauri 的定制化落地
```

---

## 四、关键洞察

1. **不是"用 Agent 替代人"，而是"把人的经验编码为 Agent 的工作流"**——Skill 的本质是资深工程师的 SOP 文档化
2. **8 个 Command 是"门面"，24 个 Skill 是"能力"**——Command 只是激活 Skill 的快捷方式
3. **Skill 之间通过名称引用，不重复定义**——`test-driven-development` 被多个 Command 引用
4. **Persona 不调用 Persona**——编排者是用户或 Command，不是 Agent 自己。防止 agent 循环调用失控
5. **渐进加载解决 Token 问题**——平时只占 name + description，使用时才展开
</body>
</html>
