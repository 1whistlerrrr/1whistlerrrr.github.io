# CLAUDE.md —— 1whistlerrrr.github.io

## 项目信息
- Hexo 静态博客
- 文章路径：`source/_posts/`
- 命名格式：`YYYY-MM-DD-title-slug.md`
- Frontmatter 必须包含：`title`、`date`、`tags`

## 上下文加载（每次启动自动执行）
**必须先读取** `source/_posts/HANDOFF.md` 了解当前任务状态。
如果 HANDOFF.md 中的 `## 四、当前状态` 有待解决项，优先处理。

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
- HANDOFF.md 用表格、复选框、绝对路径——写给 AI 看
- 博客文章用叙事结构、有观点、可发布——写给人看
- 两个文件不同，不要混淆格式
