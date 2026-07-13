# HANDOFF —— AI Solo 开发者工具链调研 —— 2026-07-13

> **目标读者：新 Claude Code 会话。** 读完并在 2 分钟内理解：我们在做什么、做到了哪、下一步是什么。

---

## 一、要做的决策

为 solo 开发者确定 AI 辅助全栈工具链——编码、审查、测试、MCP、Skills 市场。

用户角色：个人研发者，主力用 Claude Code，日常在 `/Users/liuchuyao/Downloads/Github/1whilstlerrrrr/` 下做 Hexo 博客项目。

---

## 二、最重要的 3 个结论

1. **AI 能独立完成项目，但安全是最大盲区。** AI 代码的漏洞率约为人工的 2 倍，87% 的 PR 有至少一个漏洞。任何 solo AI 开发流程必须包含独立审查层。
2. **代码审查必须跨厂商多模型。** 单模型审查自己的代码只能发现 3.8% 的 bug。最低标准：生成 agent 和审查 agent 用不同模型。
3. **MCP 从 3 个开始，不是 20 个。** 每多一个 MCP 服务器就多吃工具配额和上下文窗口。三件套 Filesystem + GitHub + Context7 覆盖 80% 日常场景。

---

## 三、已完成的调研

| 主题 | 核心发现 | 原始数据路径 |
|------|---------|-------------|
| Token 高效信息搜集 | HTML→MD 是最高杠杆；RustBrowser 75-98% 节省；Agentic Compilation O(1) | `~/Documents/Last30Days/token-efficient-web-scraping-ai-agent-data-collection-low-cost-raw-v3.md` |
| AI 能否独立完成项目 | 能，但有代价。经济优势 95-98% 成本降低。安全是最大盲区 | `~/Documents/Last30Days/ai-coding-agent-solo-developer-build-entire-project-alone-one-person-startup-raw-v3.md` |
| Ralph vs AGENT-11 vs OpenClaw 对比 | 三个不同抽象层级，可叠加。从 AGENT-11 起步 | 无独立 raw file（从已有数据直接对比） |
| 代码审查 + 测试工具 | Buddhi-Review 单模型漏掉 96.2% bug。推荐 Qodo + QE Fleet + 防作弊 | `~/Documents/Last30Days/ai-code-review-agent-automated-pr-review-testing-test-generation-quality-raw-v3.md` |
| Solo 开发者工具全景 | 按类别整理了 AI/非 AI 工具，含预算分层推荐 | 无独立 raw file（从已有数据直接回答） |
| MCP 服务器 | 三件套 + Playwright + 数据库。Context7 F 级 schema 但该装还装 | `~/Documents/Last30Days/best-mcp-servers-model-context-protocol-ai-agent-developer-tools-raw-v3.md` |
| Agent Skills 市场 + AI SE 最大问题 | AgentSkillsHub 117K+ 索引。大项目怕系统级推理缺失，小项目怕运维纪律跟不上 | `~/Documents/Last30Days/agent-skills-marketplace-registry-skill-md-ai-coding-tools-raw-v3.md` |
| 应对 AI Brain Fry + 审查方法 | 风险分级、跨厂商审查、维度拆分、系统模型持久化 | 无独立 raw file（从已有数据直接回答） |
| 对话保存和总结方法 | HANDOFF vs 博客总结的区别、各自模板、CLAUDE.md + memory 配置 | 无独立 raw file |

---

## 四、当前状态

- [ ] **待解决**：X/Twitter 源不可用——没有配置浏览器 cookie 或 API key。修复：`FROM_BROWSER=auto` 追加到 `~/.config/last30days/.env` 并运行 setup
- [ ] **待解决**：YouTube 源不可用——没有 yt-dlp。修复：`brew install yt-dlp`
- [ ] **待解决**：GitHub 搜索未认证——无 `gh` CLI 或 token。修复：`brew install gh && gh auth login`
- [ ] **待解决**：Reddit 频繁 403 导致 partial 结果。修复：运行 `"${LAST30DAYS_PYTHON}" "${SKILL_DIR}/scripts/last30days.py" doctor`
- [ ] **待解决**：`.env` 权限警告。修复：`chmod 600 ~/.config/last30days/.env`
- [ ] **待验证**：所有工具推荐均基于社区讨论，未实际测试
- [x] **已完成**：Git SSH → HTTPS 修复（`git config --global url."https://github.com/".insteadOf git@github.com:`）
- [x] **已完成**：last30days setup（`SETUP_COMPLETE=true` 已写入）
- [x] **已完成**：Python 3.13.0 预检通过
- [x] **已完成**：博客总结已写（`2026-07-13-ai-solo-developer-toolchain-research.md`）
- [x] **已完成**：HANDOFF 拆分完成

---

## 五、下一步（按优先级）

| 优先级 | 行动 | 命令/方法 |
|--------|------|----------|
| **1** | 修复 `.env` 权限 | `chmod 600 ~/.config/last30days/.env` |
| **2** | 安装 yt-dlp 解锁 YouTube 源 | `brew install yt-dlp` |
| **3** | 如果继续横向调研 | 跑 `/last30days "solo founder stack deployment hosting 2026"` 或 `/last30days "prompt engineering techniques for AI coding agents 2026"` |
| **4** | 如果纵向实践 | 在真实项目中搭建 Qodo PR-Agent + Agentic QE Fleet + Make No Mistakes 组合 |
| **5** | 改善调研质量（可选） | 配置 X/Twitter 认证（`FROM_BROWSER=auto`）+ 认证 `gh` CLI |

---

## 六、踩过的坑

| 坑 | 现象 | 正确做法 |
|----|------|---------|
| 跳过 last30days Step 0.55/0.75 | 产出 bland 的 4-bullet 摘要 | 每次都跑 pre-research WebSearch → 解析 subreddits → JSON plan → tmpfile → `--plan "$QUERY_PLAN_FILE"` |
| 用 `bash -lc '...'` 包装命令 | 搜索词中的 apostrophe 提前终止单引号 | 直接跑 heredoc block |
| 内联 `--plan '$JSON'` | 中文字符、apostrophe、`$` 破坏 shell | `mktemp` → `cat >| "$FILE" <<'PLAN_EOF'` → `--plan "$FILE"` |
| WebSearch-only 代替 engine | 缺失 Reddit 社区评论 + HN 讨论 | 先跑 engine → 再跑 2-3 个 WebSearch 补充 |
| 跳过 Step 2.5 | WebSearch 来源无法追溯 | 定位 `[last30days] Saved output` 日志路径 → 追加 `## WebSearch Supplemental Results` |
| 静默跑 `setup --allow-browser-cookies` | 未经授权读取浏览器 cookie | 先检查 `BROWSER_CONSENT=true`，不在则 AskUserQuestion |
| GitHub SSH 认证 | `git@github.com: Permission denied` | `git config --global url."https://github.com/".insteadOf git@github.com:`（已修复） |

---

## 七、关键路径

| 文件/目录 | 路径 |
|----------|------|
| 本 HANDOFF | `/Users/liuchuyao/Downloads/Github/1whilstlerrrrr/1whistlerrrr.github.io/source/_posts/HANDOFF.md` |
| 博客总结 | `/Users/liuchuyao/Downloads/Github/1whilstlerrrrr/1whistlerrrr.github.io/source/_posts/2026-07-13-ai-solo-developer-toolchain-research.md` |
| 调研数据目录 | `/Users/liuchuyao/Documents/Last30Days/` |
| last30days SKILL.md | `~/.claude/plugins/cache/last30days-skill/last30days/3.13.0/skills/last30days/SKILL.md` |
| last30days engine | `~/.claude/plugins/cache/last30days-skill/last30days/3.13.0/skills/last30days/scripts/last30days.py` |
| last30days 配置 | `~/.config/last30days/.env` |
| 项目根目录 | `/Users/liuchuyao/Downloads/Github/1whilstlerrrrr/1whistlerrrr.github.io/` |
| Python | `python3.13`（系统自带，已通过预检） |

---

## 新会话快速启动

告诉 Claude：

> "先读 `/Users/liuchuyao/Downloads/Github/1whilstlerrrrr/1whistlerrrr.github.io/source/_posts/HANDOFF.md` 了解上下文。我们在做 AI solo 开发者工具链的调研。读完告诉我你理解的现状和推荐下一步。"
