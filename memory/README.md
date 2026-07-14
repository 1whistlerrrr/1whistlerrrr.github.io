# Memory —— 项目知识库索引

> Claude 的记忆入口，**以项目为中心**组织。
> 每次任务先读本文件定位，再按需深入具体文档，不要一次性全部加载。

## 结构

| 目录 | 作用 | 何时读 |
|------|------|--------|
| `projects/` | **每个项目一个文件夹**，自包含 handoff（工作记忆）+ roadmap + research | 处理某项目时，先读它的 `handoff.md` |
| `guides/` | 长期记忆·操作手册（运维/发布），跨项目通用 | 需要执行运维/发布时 |
| `methodology/` | 长期记忆·可复用方法论 | 需要方法参考时 |

## 目录

### 🟡 projects/ —— 按项目组织（含各自的工作交接）
- [README.md](projects/README.md) —— **项目登记表**：所有项目 + 状态总览（先看这里定位）
- 每个项目文件夹里 `handoff.md` 是当前工作状态，**每次先读**

### 🟢 guides/ —— 操作手册（长期记忆，跨项目）
- [maintenance.md](guides/maintenance.md) —— 博客系统维护指南
- [publish.md](guides/publish.md) —— 文章撰写与提交发布工作流

### 🔵 methodology/ —— 方法论（长期记忆）
- [handoff-vs-summary.md](methodology/handoff-vs-summary.md) —— HANDOFF 与对话总结的区别（写给 AI vs 写给人）

## 维护约定
- 新项目 → `projects/<slug>/` 建文件夹放 `handoff.md`，再到 [projects/README.md](projects/README.md) 加一行
- 跨项目通用的手册/方法论才放 `guides/` `methodology/`；项目专属内容放各自文件夹
- 索引只放"一句话指针"，正文永远在具体文件里
- 项目完成把状态改 ✅ 归档，不要删（留踩坑经验）
