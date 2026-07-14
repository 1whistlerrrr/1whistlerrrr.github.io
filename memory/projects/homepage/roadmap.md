# 个人主页更新路线图

> 基于需求澄清与现有项目（Hexo + Butterfly 主题）分析，制定的主页更新实施计划。

---

## 一、需求澄清（六维度）

### 1. 网站目标与目标受众

| 维度 | 澄清结果 |
|------|---------|
| **网站定位** | 综合个人门户 — 博客 + 作品集 + 简介三合一，作为个人在线名片 |
| **主要受众** | 同行开发者、潜在雇主/合作者、技术学习者 |
| **核心价值** | 展示 AI Agent + 自动化工具领域的专业能力，分享技术实践，建立个人品牌 |
| **转化目标** | 促成连接 — 阅读文章 / 查看项目 / 联系合作 |

### 2. 设计偏好

| 维度 | 偏好 |
|------|------|
| **整体气质** | 开发者气质，简约大气，有个人特色 |
| **色彩原则** | 不花哨、简单，但背景配色好看，有生命力与呼吸感 |
| **风格基调** | 介于"极简清爽"与"科技深色"之间 — 干净的留白 + 开发者审美的强调色 |
| **设计参考** | Brittany Chiang（极简开发者风格）、Linear/Vercel（呼吸感与渐变背景） |

**色彩方案建议**（待确认）：

```
浅色模式：
  背景：#fafafa → #ffffff（微渐变，呼吸感）
  文字：#1a1a2e（深蓝黑，非纯黑，更柔和）
  强调色：#6366f1（靛蓝紫，开发者气质，有活力但不刺眼）
  辅助色：#10b981（薄荷绿，用于成功/在线状态点缀）
  卡片背景：#ffffff + 轻微阴影
  边框：#e5e7eb

深色模式：
  背景：#0f0f1a → #1a1a2e（深蓝黑渐变，非纯黑，有深度）
  文字：#e4e4e7
  强调色：#818cf8（浅靛蓝，深色背景下更醒目）
  辅助色：#34d399
  卡片背景：#1e1e2e
  边框：#2d2d3f
```

### 3. 内容结构

主页将包含以下板块（按首屏到底部顺序）：

| 板块 | 状态 | 说明 |
|------|------|------|
| **Hero 首屏** | 新建 | 姓名 + 一句话定位 + CTA 按钮，呼吸感渐变背景 |
| **关于我/简介** | 已有，需精简 | 现有 about 页内容丰富，首页只放精华摘要 + 链接 |
| **精选项目/作品集** | 已有占位，需填充 | 3-5 个项目卡片，替换现有"建设中"内容 |
| **知识大纲** | 已有，保留 | 现有 markmap 思维导图，后续与知识图谱联动 |
| **博客文章** | 已有 | 现有文章列表，保留 Butterfly 文章流 |
| **联系方式** | 已有，需强化 | 邮箱 + GitHub，首页底部 + 独立联系区 |

**导航菜单建议**（当前为空，需配置）：

```
首页 | 文章 | 项目 | 知识图谱 | 关于
 /     /archives  /projects  /knowledge  /about
```

### 4. 功能需求

| 功能 | 现状 | 实施方案 |
|------|------|---------|
| **深浅主题切换** | 主题已支持，`darkmode.enable: true` | ✅ 已就绪，仅需配置 `autoChangeMode: 1`（跟随系统） |
| **全站搜索** | 主配置有 search.xml，但主题 `search.use` 为空 | 启用 `local_search`，配置主题 search 字段 |
| **评论系统** | 未配置（`comments.use` 为空） | 启用 **Giscus**（基于 GitHub Discussions，免费、无广告、与 GitHub 生态契合） |
| **订阅功能** | 无 | 添加 **RSS 订阅**（hexo-generator-feed 插件）+ 文章页订阅引导 |

### 5. 参考案例

| 案例 | 借鉴点 |
|------|--------|
| **Brittany Chiang**（brittanychiang.com） | 极简开发者主页、左侧固定导航、深色主题、项目分区 |
| **Linear**（linear.app） | 渐变背景的呼吸感、柔和阴影、开发者审美 |
| **Vercel**（vercel.com） | 黑白高对比 + 强调色点缀、首屏价值主张清晰 |
| **Lee Robinson**（leerob.com） | 博客与项目整合、Next.js 风格的简洁卡片 |

### 6. 技术约束

| 约束 | 说明 |
|------|------|
| **平台** | GitHub Pages 部署，Git 版本控制 |
| **框架** | Hexo（继续使用，迁移成本最低） |
| **主题** | Butterfly（已安装，功能强大，支持深度自定义） |
| **内容格式** | Markdown + Hexo 标签插件（markmap/timeline 等） |
| **构建** | 本地 `hexo generate` → deploy 到 GitHub，或用 GitHub Actions 自动化 |
| **域名** | 当前 `1whistlerrrr.github.io`，可选绑定自定义域名 |

---

## 二、实施路线图

### 阶段 0：准备工作（基础配置补全）

**目标**：补全主题缺失配置，让现有功能正常运转。

| 任务 | 文件 | 具体操作 |
|------|------|---------|
| 配置导航菜单 | `themes/butterfly/_config.yml` | 取消 menu 注释，配置 首页/文章/项目/知识图谱/关于 五项 |
| 配置社交链接 | `themes/butterfly/_config.yml` | social 字段填入 GitHub + Email |
| 配置头像 | `themes/butterfly/_config.yml` | 替换默认 butterfly 图标为个人头像 |
| 启用本地搜索 | `themes/butterfly/_config.yml` | `search.use: local_search` |
| 配置深浅模式 | `themes/butterfly/_config.yml` | `darkmode.autoChangeMode: 1`（跟随系统） |
| 配置站点信息 | `_config.yml` | 确认 title/author/description 准确 |
| 修正侧边栏 GitHub 链接 | `themes/butterfly/_config.yml` | card_author.button.link 改为实际 GitHub 地址 |

### 阶段 1：视觉风格定制（呼吸感开发者主题）

**目标**：建立有个人特色的视觉体系，告别默认主题外观。

| 任务 | 文件 | 具体操作 |
|------|------|---------|
| 自定义主题色 | `themes/butterfly/_config.yml` | 启用 theme_color，配置靛蓝紫强调色方案（见上方色彩建议） |
| 自定义背景 | `themes/butterfly/_config.yml` + `source/css/custom.css` | 浅色：微渐变背景 `linear-gradient(180deg, #fafafa, #ffffff)`；深色：`linear-gradient(180deg, #0f0f1a, #1a1a2e)` |
| 自定义字体 | `themes/butterfly/_config.yml` | 全局字体用系统字体栈；代码字体用 JetBrains Mono / Fira Code |
| 圆角与阴影 | `source/css/custom.css` | 卡片圆角 12px、柔和阴影 `0 4px 20px rgba(0,0,0,0.06)` |
| 首屏样式 | `source/css/custom.css` | Hero 区域渐变背景 + 大字号标题 + 留白 |
| 启用页面过渡 | `themes/butterfly/_config.yml` | `enter_transitions: true`（已启用） |

### 阶段 2：首页内容重构

**目标**：将首页从纯文章流升级为综合门户。

| 任务 | 说明 |
|------|------|
| 创建自定义首页布局 | 在 `themes/butterfly/layout/` 新建 `index_custom.pug` 或用 inject 注入自定义 HTML |
| Hero 首屏 | 姓名、一句话定位（"专注于 AI Agent 与自动化工具的开发者"）、CTA 按钮（查看项目/阅读文章） |
| 精选项目摘要 | 首页中部展示 3 个项目卡片，链接到 /projects/ |
| 知识大纲入口 | 首页展示知识图谱预览卡，链接到 /knowledge/ |
| 最新文章 | 保留 Butterfly 文章流，但限制显示 5 篇 + "查看全部"链接 |
| 联系区 | 首页底部：邮箱 + GitHub 图标 + 一句话引导 |

### 阶段 3：内容填充与优化

| 任务 | 说明 |
|------|------|
| 填充项目作品集 | 替换 `source/projects/index.md` 占位内容，添加 3-5 个真实项目（AI Agent 工具、自动化脚本等），每个含描述/技术栈/链接 |
| 精简关于页 | `source/about/index.md` 现有内容保留，但确保首屏摘要清晰 |
| 知识大纲优化 | `source/knowledge/index.md` 现有 markmap 保留，后续阶段添加知识图谱可视化 |
| 文章封面图 | 为现有文章配置封面图（cover default_cover） |
| 添加 RSS 订阅 | 安装 `hexo-generator-feed` 插件，配置 feed 链接 |

### 阶段 4：功能集成

| 任务 | 配置位置 |
|------|---------|
| 启用 Giscus 评论 | `themes/butterfly/_config.yml` → giscus 字段（需在 giscus.app 配置获取 repo_id/category_id） |
| 订阅引导 | 文章页底部添加 RSS 订阅 + GitHub Follow 引导 |
| SEO 优化 | 启用 `structured_data`、配置 Open Graph、提交 sitemap 到搜索引擎 |
| 访问统计 | 可选启用 Umami（自托管，隐私友好）或 Google Analytics |

### 阶段 5：知识图谱联动（后续规划）

| 任务 | 说明 |
|------|------|
| 知识图谱可视化 | 在现有 markmap 思维导图基础上，引入交互式知识图谱（如 D3.js / Cytoscape.js） |
| 大纲与图谱联动 | 知识大纲作为图谱的入口/索引，点击大纲节点跳转到图谱对应区域 |
| 与博客联动 | 文章自动关联到知识图谱节点，形成"知识-文章"双向链接 |

---

## 三、技术实现要点

### 3.1 首页自定义布局方案

Butterfly 主题支持通过 `inject` 注入自定义内容，无需修改主题核心文件：

```yaml
# themes/butterfly/_config.yml
inject:
  head:
    - <link rel="stylesheet" href="/css/custom.css">
  bottom:
    - <script src="/js/homepage.js"></script>
```

在 `source/css/custom.css` 中编写首页专属样式，在 `source/js/homepage.js` 中处理交互。

### 3.2 呼吸感背景实现

```css
/* source/css/custom.css */
body {
  background: linear-gradient(180deg, #fafafa 0%, #ffffff 100%);
  background-attachment: fixed;
}

[data-theme="dark"] body {
  background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
}

/* 首屏 Hero 渐变光晕 */
.hero-section {
  position: relative;
  overflow: hidden;
}
.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: 50%;
  transform: translateX(-50%);
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
```

### 3.3 Giscus 评论配置步骤

1. 访问 https://giscus.app
2. 填入仓库 `1whistlerrrr/1whistlerrrr.github.io`，启用 Discussions
3. 选择映射方式 `pathname`，分类 `Announcements`
4. 获取生成的 `repo_id` 和 `category_id`
5. 填入主题配置：

```yaml
giscus:
  repo: 1whistlerrrr/1whistlerrrr.github.io
  repo_id: <获取的 repo_id>
  category_id: <获取的 category_id>
  light_theme: light
  dark_theme: dark
```

### 3.4 RSS 订阅配置

```bash
npm install hexo-generator-feed --save
```

```yaml
# _config.yml 添加
feed:
  enable: true
  type: atom
  path: atom.xml
  limit: 20
```

---

## 四、执行优先级与建议

### 推荐执行顺序

```
阶段 0（基础配置）→ 阶段 1（视觉定制）→ 阶段 2（首页重构）→ 阶段 3（内容填充）→ 阶段 4（功能集成）
                                                                      ↓
                                                            阶段 5（知识图谱，长期）
```

### 关键决策点

| 决策 | 建议 | 待确认 |
|------|------|--------|
| 色彩方案 | 采用靛蓝紫强调色（#6366f1） | 是否符合您对"有生命力"的期待？ |
| 首页布局 | 自定义 Hero + 精选项目 + 文章流 | 是否需要加入技能展示区？ |
| 评论系统 | Giscus（基于 GitHub Discussions） | 是否同意用 GitHub 账号评论？ |
| 项目内容 | 需您提供 3-5 个真实项目信息 | 哪些项目想展示？ |
| 知识图谱 | 先保留 markmap，后续迭代 | 知识图谱期望的交互形式？ |

### 下一步行动

1. **确认色彩方案** — 您是否认可靛蓝紫（#6366f1）作为强调色，或有其他偏好？
2. **提供项目信息** — 列出 3-5 个想展示的项目（名称/描述/技术栈/链接）
3. **开始阶段 0** — 我可以立即开始补全基础配置（导航菜单、社交链接、搜索、深浅模式）

---

*路线图制定时间：2026-07-02 | 基于 Hexo + Butterfly 主题 + GitHub Pages 技术栈*
