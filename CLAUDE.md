# CLAUDE.md —— 1whistlerrrr.github.io

## 项目信息
- Hexo 静态博客
- 文章路径：`source/_posts/`
- 命名格式：`YYYY-MM-DD-title-slug.md`
- Frontmatter 必须包含：`title`、`date`、`tags`

## 记忆库（每次启动先读索引）
项目知识以**项目为中心**组织在 `memory/`：
- **必须先读** [`memory/README.md`](memory/README.md) —— 顶层索引
- **当前任务** 看 [`memory/projects/README.md`](memory/projects/README.md) 项目登记表，进对应项目文件夹读 `handoff.md`；有待解决项优先处理
- **跨项目手册/方法论** 按需读 `memory/guides/`、`memory/methodology/`
- 新项目：`memory/projects/<slug>/` 建文件夹放 `handoff.md`，再在项目登记表加一行

## 上次调研的可用工具
- `last30days` skill（v3.13.0）已安装在 `~/.claude/plugins/cache/last30days-skill/last30days/3.13.0/skills/last30days/`
- 可用源：Reddit、HackerNews、GitHub、Polymarket、Web
- 不可用：X/Twitter（未配认证）、YouTube（未装 yt-dlp）
- 调研原始数据在 `~/Documents/Last30Days/`

## last30days 使用约定（来自踩过的坑）
- ⚠️ Python 预检每次都要跑（解析 `LAST30DAYS_PYTHON`，系统有 python3.13）
- ⚠️ 必须跑完整协议：Step 0.45 预检 → Step 0.55 解析 subreddits → Step 0.75 生成 JSON plan → 写 tmpfile → `--plan "$QUERY_PLAN_FILE"`
- ⚠️ 不要用 `bash -lc '...'` 包装 engine 命令
- ⚠️ Plan JSON 通过 tmpfile 传递，不要内联
- ⚠️ 先跑 engine 再跑 WebSearch 补充，不要反过来
- ⚠️ Engine 跑完后把 WebSearch 结果追加到 raw file（Step 2.5）

## 输出约定
- `memory/projects/*/handoff.md` 用表格、复选框、绝对路径——写给 AI 看
- 博客文章用叙事结构、有观点、可发布——写给人看
- 两类文件不同，不要混淆格式
