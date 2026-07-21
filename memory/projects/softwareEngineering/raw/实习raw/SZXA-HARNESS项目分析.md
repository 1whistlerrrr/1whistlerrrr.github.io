# SZXA-HARNESS 项目开发体系分析

> 分析时间：2026-07-22
> 来源：`/Users/liuchuyao/Downloads/HARNESS/szxa-next-harness/`
> 版本：v3.4.1

---

## 一、整体定位

SZXA-HARNESS 是**数智兴安（szxa）项目的 AI 编排系统**，构建在 Claude Code 之上。它不是简单地"用 AI 写代码"，而是一套完整的工程基础设施：把 feature 从需求到上线的全生命周期，用**过程路由 + 专职 Agent + 对抗审查 + Hook 拦截**自动化执行。

管辖范围：1 个 Tauri 前端（`szxa-next-desktop`）+ 1 个 .NET 后端（`szxa-next-webapi`）+ 1 个 Expo 移动端（`szxa-next-app`）。

---

## 二、完整开发流程（4 个串行过程）

```
需求要点（人脑风暴）
       ↓
  ┌──────────────────────────────────────────┐
  │ 过程1: 需求规格化 → 原型确认             │
  │   spec-writer ⇄ spec-reviewer (GAN)     │
  │   → frontend-coder 建可交互原型           │
  │   → 人类确认 → promote 到 final/         │
  ├──────────────────────────────────────────┤
  │ 过程2: 全栈详细设计                      │
  │   designer ⇄ design-reviewer (GAN)      │
  │   → 人类确认 → promote 到 final/         │
  ├──────────────────────────────────────────┤
  │ 过程3: 实施计划                          │
  │   plan-writer ⇄ plan-reviewer (GAN)     │
  │   → 人类确认（执行产物，不 promote）       │
  ├──────────────────────────────────────────┤
  │ 过程4: 编码 → 审查 → 验证                │
  │   task-planner → backend-coder 先        │
  │   → frontend-coder 后（等 swagger）       │
  │   → code-reviewer 审查 → evaluator 验证  │
  └──────────────────────────────────────────┘
```

**GAN 对抗循环**：Writer 产出 → Reviewer 审查（按 Critical / High / Medium / Low 分级）→ 不满足退出条件则反馈 Writer 修改 → 重新审查，最多 3 轮。退出条件：高优问题全部解决 OR 剩余问题无法在当前阶段解决。

---

## 三、文件体系：每类文件的作用

### 3.1 入口与控制文件

| 文件 | 作用 |
|------|------|
| `CLAUDE.md` | **编排者（Orchestrator）的权威行为指南**。定义角色、过程路由、Agent 清单、任务目录规范、全局约束。每次会话启动时作为系统提示词被平台加载——这是整个 harness 运作的"宪法"，编排者的所有行为由此驱动 |
| `AGENTS.md` | 仅两行，指向 CLAUDE.md。让子 Agent 也能读取相同的规范基线 |
| `init.sh` / `init.bat` | **会话启动门控脚本**。每次会话开始必须执行。检查 3 个子仓库状态 + 插件版本 + manifest 漂移（drift）。`--init` 模式做完整初始化（clone 仓库、同步资产、安装 git hooks） |
| `.claude/current-task` | 编排者维护的一行文本文件（如 `feature-物资安全管控`）。**运行时"当前任务"标识**——traces 按此名隔离写入，UserPromptSubmit hook 每次校验提醒 |
| `.claude/current-iteration` | 一行文本文件（如 `R1`）。**运行时"当前迭代轮次"标识**——所有 Agent 产出按此写入 `iterations/R{n}/` |

### 3.2 Manifest 与同步体系

| 文件 | 作用 |
|------|------|
| `claude-init/harness-manifest.json` | **Harness 资产的权威闭集清单**。定义 5 个 sync_groups（agents、skills、hooks、settings、mcp），每个指定 source → target 的同步策略（copy-dir 或 copy-file）。还包含 assets（开发资产登记）、versioned_files（需统一版本号的文件）。**新增任何 agent/skill/hook/配置必须先登记进这里** |
| `scripts/harness-sync.js` | **Node 同步引擎**。check 模式：校验 manifest 完整性 + 逐文件 SHA256 hash 比对（5 态：ok / missing / drifted / extra / source-missing）+ 检测 resolution-drift。sync 模式：执行 copy 同步 + 生成 `.harness-state.json` 状态锁 |
| `.harness-state.json` | **同步状态锁**。记录最后同步的时间戳、commit hash、每个文件的 SHA256 hash。下次 check 对比此文件即可发现 drift。不在 git 中 |
| `scripts/bump-version.js` | 按 manifest 的 versioned_files 闭集批量更新所有文件中的版本号标记 |
| `scripts/promote.sh` | 编排者在设计层确认后，将 `iterations/R{n}/` 的设计文档复制到 `final/` |
| `scripts/verify-harness.sh` | Harness 自检脚本：6 个场景的端到端验证（self-test、全量 sync+check、drift 检测、source-missing 检测、state lock 验证、hook 自定位） |

### 3.3 Agent 定义（13 个）

位置：`claude-init/agents/*.md`（权威源）→ 同步到 `.claude/agents/`（运行时）

每个 Agent 文件通过 **YAML frontmatter** 声明：模型（opus / sonnet）、工具白名单、maxTurns、memory 模式（project）、worktree 隔离（仅 coder 类 Agent）。

| Agent | 过程 | 作用 |
|-------|------|------|
| `spec-writer` | 过程1 | 将需求要点转化为结构化的需求 spec、产品验收 spec、UI&UX 设计 spec |
| `spec-reviewer` | 过程1 | 审查三份 spec 的完整性和无歧义性，产出结构化审查报告 |
| `designer` | 过程2 | 全栈详细设计（API 契约、数据模型、业务流程、前端组件、ADR） |
| `design-reviewer` | 过程2 | 审查详细设计是否与架构规范一致，字段/接口是否完备 |
| `plan-writer` | 过程3 | 将详细设计转化为精确到文件路径的实施计划（含完整代码，禁占位符） |
| `plan-reviewer` | 过程3 | 审查实施计划的可执行性 |
| `task-planner` | 过程4 | 将实施计划拆解为子任务 DAG + 子任务 spec |
| `backend-coder` | 过程4 | 后端编码，worktree 隔离，.NET 8 + EF Core + PostgreSQL |
| `frontend-coder` | 过程1、4 | 前端编码，worktree 隔离。过程1 建原型，过程4 接真实 API |
| `frontend-coder-app` | 过程1、4 | 移动端编码，Expo + React Native |
| `backend-code-reviewer` | 过程4 | 后端代码多维度审查（安全 / 风格 / 测试 / 错误处理 / 性能） |
| `frontend-code-reviewer` | 过程4 | 前端代码多维度审查（UI&UX 偏差标记为 Critical） |
| `frontend-coder-app-reviewer` | 过程4 | 移动端代码审查 |
| `evaluator` | 过程4 | E2E 分层验证（API 集成测试 + 单元测试覆盖率 + 前端类型检查） |
| `issue-analyzer` | 过程外 | 线上问题归因分析（只分析不改代码，定位到需求/设计/实施三层） |

### 3.4 Skill 体系（20 个）

位置：`claude-init/skills/*/SKILL.md`（权威源）→ 同步到 `.claude/skills/`（运行时）

Skill 是 Agent 的**可复用能力模块**，分两类：

**Standalone Skill**（出现在 `/` 菜单，用户可手动调用）：

| Skill | 作用 |
|-------|------|
| `local-dev` | 本地前后端联调启动 |
| `harness-version` | 查看 harness 版本和资产状态 |
| `harness-update` | 更新 harness 自身（改 agent/skill/hook/配置后的标准流程） |
| `aqm-db` | 查询 AQM 测试环境数据库 |
| `backend-commit` | 后端智能提交（安全检查 + conventional commit） |
| `backend-test` | 后端测试运行器 |
| `复盘` | 读 traces 做合规分析 |

**Agent Skill**（不进菜单，仅通过 Agent frontmatter 预加载）：

| Skill | 作用 |
|-------|------|
| `backend-csharp-unit-testing` | C# 单元测试规范（xUnit + Moq + AAA） |
| `backend-datacenter-etl-dev` | ETL 组件开发模板 |
| `backend-deploy-check` | 后端部署前检查清单 |
| `backend-refactor` | 后端结构化重构工作流 |
| `backend-review` | 后端 5 维度审查 |
| `frontend-unit-testing` | 前端单元测试规范（Vitest + Testing Library） |
| `frontend-feature-development` | 前端功能开发（Mantine 优先） |
| `frontend-component-refactoring` | 大组件拆分重构 |
| `frontend-code-migration` | 跨项目代码迁移 |
| `frontend-generate-component` | 组件生成模板（6 种类型） |
| `frontend-generate-renderer` | GIS 渲染器生成 |
| `frontend-generate-test` | 前端测试文件生成 |
| `frontend-gis-development` | GIS 模块开发（mapbox-gl） |

### 3.5 Hook 体系（5 个）

位置：`claude-init/hooks/`（权威源）→ 同步到 `.claude/hooks/`（运行时）

Hook 在 Agent **外部**运行，模型无法绕过。是将规范从"建议"变成"强制"的关键机制。

| Hook | 触发时机 | 作用 |
|------|----------|------|
| `session-start.sh` | SessionStart | 注入 git 状态（分支、status、最近 5 commits）到初始上下文 |
| `user-prompt-submit.sh` | UserPromptSubmit | 校验 `.claude/current-task` 和 `.claude/current-iteration`，通过 additionalContext 提醒编排者 |
| `pre-edit-guard.sh` | PreToolUse (Edit\|Write) | **编排者职责边界提醒**——拦截编排者直接写产品代码 |
| `trace-writer.sh` | PostToolUse / SubagentStart / SubagentStop | 所有关键工具调用 + Subagent 对话记录到 `doc/{task}/traces/main.jsonl`，只存不解析 |
| `pre-commit` | Git pre-commit | 拦截对 `.claude/` 的手动编辑，强制通过 manifest 同步 |

### 3.6 配置体系

| 文件 | 作用 |
|------|------|
| `claude-init/settings.json` | **权威 settings 模板**。定义 hook matcher/command、权限 allow/deny 列表、11 个启用插件。同步到 `.claude/settings.json` |
| `claude-init/settings.local.json` | 本地配置模板（占位 token）。首次 `--init` 时复制到 `.claude/`，已存在不覆盖 |
| `.claude/settings.local.json` | 机器本地配置（API key、模型映射、base URL），不在 git 中 |
| `claude-init/.mcp.json` | MCP 服务器配置（Playwright），同步到根 `.mcp.json` |

### 3.7 规范与模板

| 目录/文件 | 作用 |
|-----------|------|
| `规范/架构设计文档.md` | 项目架构设计（技术栈、分层、模块划分） |
| `规范/架构约束.md` | **可执行的架构约束**——同时在 Agent Prompt（软约束）和 Hook（硬约束）中编码 |
| `规范/API接口文档生成和测试规范.md` | API 文档格式和契约测试标准 |
| `规范/数据库建模规范.md` | DDL 编写、索引、迁移规范 |
| `规范/UI规范.md` | UI 组件库、布局、交互规范 |
| `规范/测试策略规范.md` | 测试金字塔、覆盖率阈值 |
| `规范/集成测试规范.md` | 集成测试编写和执行规范 |
| `规范/前后端联调流程.md` | 前后端串行依赖约定 |
| `规范/部署检查清单.md` | 上线前逐项检查 |
| `规范/GIT分支管理规范.md` | 分支策略、commit message 规范 |
| `templates/`（17 个） | 需求/设计/计划/审查/验证/任务报告等的**文档骨架**，Agent 按模板填充产出 |
| `需求基线/需求基线管理.md` | 全平台功能成熟度跟踪 |

### 3.8 任务产出目录结构

```
doc/{task-name}/
├── final/                    ← 设计层基线（GAN + 人类确认后 promote）
│   ├── 需求spec.md
│   ├── 产品验收spec.md
│   ├── UI&UX设计spec.md
│   ├── 详细设计spec.md       ← API/数据库/流程/组件设计
│   └── 需求追溯矩阵.md       ← FR→AT→设计→实施→测试 端到端追溯
│
├── iterations/
│   ├── R1/                   ← 第1轮迭代全部产物
│   │   ├── 需求spec.md、产品验收spec.md、UI&UX设计spec.md
│   │   ├── 审查报告-需求.md
│   │   ├── 详细设计spec.md、审查报告-设计.md
│   │   ├── 实施计划.md、审查报告-计划.md
│   │   ├── 任务计划DAG.md、子任务spec/
│   │   ├── 审查报告.md、验证报告.md、最终任务报告.md
│   │   └── 计划进度文档.md   ← 全过程状态台账（支持断点续接）
│   ├── R2/                   ← 修复迭代（递增）
│   └── R3/
└── traces/                   ← 执行 trace（按任务名隔离，不提交 git）
```

**Promote 机制**：Agent 产出**永远写** `iterations/R{n}/`；编排者在设计层确认后用 `promote.sh` 复制到 `final/`。final 只保留设计层产物，执行产物（审查报告、计划、DAG 等）永久留在 iterations 里。

---

## 四、一次完整开发的执行时序

```
 1. 用户提出需求 → Orchestrator 执行 bash init.sh（门控检查）
 2. Orchestrator 创建 .claude/current-task + .claude/current-iteration
 3. SessionStart hook 自动注入 git 状态
 4. UserPromptSubmit hook 校验任务上下文

── 过程1 需求规格化 ──
 5. spec-writer 产出三份 spec → iterations/R1/
 6. spec-reviewer 审查 → 审查报告
 7. GAN 循环（≤3 轮）直到退出条件满足
 8. 人类确认 → promote → final/

── 过程2 详细设计（同理，GAN 循环）──
── 过程3 实施计划（同理，GAN 循环，执行产物不 promote）──

── 过程4 编码→审查→验证 ──
 9. task-planner 拆解子任务 DAG
10. backend-coder（worktree 隔离）编码 → swagger.json
11. frontend-coder（worktree 隔离，等 swagger）接真实 API
12. code-reviewer 多维度审查
13. evaluator 分层验证（API 集成 + 单元测试 + 类型检查）
14. Orchestrator 合并 worktree → 最终任务报告
```

---

## 五、五个核心设计原则

1. **过程固化**：4 过程严格顺序，不可跳转，门控由编排者 + GAN 自动判定
2. **角色拆分**：13 个专职 Agent（Writer + Reviewer 成对），职责窄而深，1 层扁平派发
3. **双重约束**：Agent Prompt（软约束）+ Hook 拦截（硬约束），规范不被绕过
4. **结构化产出**：每阶段产出有固定模板、可校验、可追溯（traces 审计日志）
5. **配置驱动**：Manifest 声明式管理所有资产，SHA256 hash 完整性校验，`init.sh --init` 一键同步，团队环境一致

---

## 六、关于"记忆"机制

项目**不存在** `memory_tool.py`。记忆/状态管理分散在多层：

| 层次 | 机制 | 文件/组件 |
|------|------|-----------|
| 系统提示词 | CLAUDE.md 在会话启动时加载为快照 | `CLAUDE.md` + `AGENTS.md` |
| 资产一致性 | Manifest + SHA256 hash 锁 | `harness-manifest.json` → `.harness-state.json` |
| 会话恢复 | 运行时状态文件 | `.claude/current-task`、`.claude/current-iteration` |
| 上下文注入 | SessionStart hook | `session-start.sh` 注入 git 状态 |
| Agent 记忆 | Subagent frontmatter `memory: project` | Agent 定义文件中声明 |
| 可观测性 | Trace 采集 | `trace-writer.sh` → `doc/{task}/traces/main.jsonl` |
