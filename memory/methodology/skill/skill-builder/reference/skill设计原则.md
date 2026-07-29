# 核心设计原则
官方强调了 Skill 设计的三大核心原则，理解它们是构建高效 Skill 的前提。
## 原则一：渐进式披露 (Progressive Disclosure)
这是 Skill 最精妙的设计，旨在最大化能力、最小化 Token 消耗。它分为三层：

第一层 (YAML Frontmatter) : 永远加载在系统提示中，只包含最核心的名称和描述，让 Agent 知道“何时”该用你。
第二层 (SKILL.md 主体) : 当 Agent 认为 Skill 与当前任务相关时才会加载，包含完整的指令和工作流。
第三层 (链接文件) : references/ 或 scripts/ 目录中的文件，只有在 Skill 指令引导 Claude去读取时才会被加载。
> 落地启示：不要把所有文档塞进 SKILL.md，厚重资料放入 references，实现上下文轻量化。
## 原则二：可组合性 (Composability)
Agent 可以同时加载多个 Skill。这意味着你的 Skill 需要像一个行为良好的微服务，专注于做好一件事，并能与其他 Skill 协同工作，而不是假设自己是系统中唯一的能力。
例如：
一个“日志查询” Skill 可以和一个“代码审查” Skill 组合，实现从问题分析到代码定位修复的自动化闭环。

## 原则三：可移植性 (Portability)
一次创建，处处运行。一个标准的 Skill 能够在所有支持的环境中（如 Claude.ai 网页版、Claude Code 开发环境，以及通过 API 调用）无需修改即可一致地工作，前提是目标环境满足其依赖项（如特定的系统软件包或网络访问）。
简单来说，Skill 是连接“用户意图”和“底层工具”的智能胶水层。它教会Agent不仅“能做什么”，更重要的是“应该如何一步步地、高质量地完成”。


# skill.md 格式样例
## 
## Good: 具体且可操作，包含触发短语
---
name: your-skill-name
description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

## Good: 包含用户可能提及的任务
---
name: your-skill-name
description: Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".
---

## Bad: 过于模糊
description: Helps with projects


# 封装 Skill 前提：
满足下面特征，优先封装 Skill：
高频重复的多步骤工作流
需要固定标准、统一输出风格（周报、文档、评审清单）
需要串联调用多个工具 / 多轮 API 交互
隐性领域知识需要固化，避免每次对话重复说明