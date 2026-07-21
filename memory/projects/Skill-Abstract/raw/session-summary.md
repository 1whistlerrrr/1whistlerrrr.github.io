# 对话总结 — Claude Code 工作流优化全链路

**日期**: 2026-07-21 | **总轮次**: 76 轮 | **方法**: ACORN 五步法

---

## 结论

这是一个从"怎么省 token"开始，一路深入到"Agent 上下文架构对比 + Harness 迭代自动化"的完整探索。核心产出包括：一个对话总结 Skill、一套 Harness 迭代工作流方案、五轮 /last30days 深度调研。

---

## 主题聚类

### 一、Token 节省 & 上下文管理

**决策:**
- 压縮策略采用 50% 手动 compact + 80% 自动安全网
- 子代理隔离作为对抗上下文膨胀的首要手段
- 模型路由：Haiku 做轻活、Sonnet 做日常、Opus 做架构

**发现:**
- `/compact` 在 50% 时压比 80% 时效好得多——上下文质量从 25% 窗口填充率就开始退化
- Caveman 风格输出可节省 60-75% 输出 token
- TokenWar (RTK+context-mode+claude-mem+caveman+ponytail) 五合一栈压缩不同缓冲区，叠加生效
- tokensave 建代码知识图谱 → 88% 检索节省（SQLite 存 `.tokensave/tokensave.db`）

**关键工具清单:**
- `tokensave` — 代码知识图谱，预建索引。brew install，项目内 `tokensave init`
- `cclog` — JSONL → Markdown 导出
- `ccspan` — Token/成本 TUI 分析
- `cclens` — SQLite 全文搜索历史会话

---

### 二、对话记录 & 记忆工具链

**决策:**
- 选用 claw-diary 做每日/每周自动总结（Hook 驱动，零外部 API）
- Vinod vs Wendkeep 对比结论：Vinod 极轻量被动观察，Wendkeep 完整归档+知识图谱+成本追踪
- 最终用户倾向轻量方案 → claw-diary 最匹配

**发现:**
- Claude Code 原生已自动写 `~/.claude/projects/` JSONL（完整转录）
- Auto Memory 自动记笔记 + Auto Dream 每 24h 后台整理
- Wendkeep 308 会话 / $4,836 生产案例

**claw-diary 架构解析:**
```
PreToolUse → claw-diary collect before
PostToolUse → claw-diary collect after
SessionStart → claw-diary collect session-start
Stop → claw-diary collect session-stop
         ↓
~/.claw-diary/events/YYYY-MM-DD.jsonl
         ↓
/diary → claw-diary summarize today → LLM 读 JSONL 写摘要
```

---

### 三、Skills & 总结方法论

**决策:**
- 创建 `/summarize` Skill，采用 ACORN 五步法：
  - A (Atomic) — 拆为原子单元
  - C (Cluster) — 按决策 > 新信息 > 可执行性聚类
  - O (Order) — 结论 → 决策 → 发现 → 待办
  - R (Refine) — 新手 / 速读者 / 专家三重审查
  - N (Name) — 标题体现结果，不是话题

**产出:**
- `~/.claude/skills/summarize.md`
- `Skill-Abstract/summarize.md` (GitHub Pages)

**调用方式:**
- `/summarize` — 默认总结
- `/summarize:weekly` — 周报
- `/summarize:decisions` — 仅提取决策
- `/summarize:standup` — 站会格式
- `/summarize:eli5` — 零基础解释

---

### 四、Agent 上下文架构对比

**五大平台系统性对比:**

| 维度 | Claude Code | Trae (字节) | WorkBuddy | Grok Build | Cursor/Copilot/Codex |
|------|-----------|------------|-----------|------------|---------------------|
| Hook完备性 | 4/4 (25+事件) | IDE原生 | Harness控制 | 2/4 | 0-4/4 |
| 记忆架构 | Auto Memory+Auto Dream | 双轨20条+SQLite | GEM 10策略模板 | Markdown MEMORY.md | 各不同 |
| 独特优势 | 自动化程度最高 | 中文最强+IDE原生 | 哲学一致性+透明 | Arena多代理+开源 | 各有所长 |

**WorkBuddy GEM 架构核心:**
- Gene: 10个 ~50 token 策略模板（SIGNALS+STRATEGY+CONSTRAINTS）
- Executive: 调度路由 + 注意力控制
- Memory: 晶体化索引 + 双节点蒸馏(任务完成+22:00日压缩)
- 核心哲学: "不放程序性记忆进长期记忆" + "显式外化 Markdown"

**Grok Build 独特价值:**
- Arena Mode: 8并行代理选最优
- 4代理辩论架构(Grok 4.20): 幻觉率从~12%降到~4.2%
- $2/$6 per M token (最便宜)
- Apache 2.0 开源

---

### 五、Harness 迭代自动化

**决策:**
- 选用 "纠正 → Stop hook 捕获 → 回流到 CLAUDE.md" 模式
- 配合 Self-Learning Skills 做推广门控（3条件：验证通过 + 命名失败模式 + 至少一个排除的死路）

**2026 社区共识模式:**
```
会话执行 → 纠正/失败被检测 → 捕获为候选 → 验证/推广门 → 进化 CLAUDE.md → 下次会话受益
```

**关键原则:**
- 证明, 不信任 — Agent 必须提供遵循规则的证据
- 推广门 — 只有被验证的经验才成为永久规则
- 编译, 不只加载 — 把被动文本转为主动执行检查
- 闭环 — 纠正必须自动回流进规则

---

## 待办

- [ ] 注册 Stop hook 脚本(捕获纠正 → 追加 HARRNESS_FEEDBACK.md)
- [ ] 每周审核 HARRNESS_FEEDBACK.md → 精选条目写入 CLAUDE.md
- [ ] 评估安装 claw-diary 或 Wendkeep 做全自动采集
- [ ] 将 summarize Skill 注册为正式可用(/summarize 命令)
