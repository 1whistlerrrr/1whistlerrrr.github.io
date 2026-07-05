# 博客系统维护指南

## 一、系统概述

本博客系统基于 **Hexo** 框架和 **Butterfly** 主题构建，支持以下核心功能：

- ✅ 自动化文章发布流程
- ✅ 知识图谱（Markmap）可视化
- ✅ 每周AI自动总结与更新
- ✅ 完整的内容CRUD管理
- ✅ 本地搜索与分类导航

---

## 二、文件夹结构

```
private-web/
├── source/
│   ├── _posts/              # 博客文章目录
│   │   ├── template.md      # 文章模板
│   │   └── YYYY-MM-DD-slug.md  # 博客文章
│   ├── knowledge/           # 知识图谱目录
│   │   ├── index.md         # 知识图谱入口页
│   │   ├── ai-agent.md      # AI Agent 知识图谱
│   │   ├── java.md          # Java 知识图谱
│   │   ├── python.md        # Python 知识图谱
│   │   ├── automation.md    # 自动化知识图谱
│   │   └── cloud.md         # 云原生知识图谱
│   ├── about/               # 关于页面
│   ├── projects/            # 项目页面
│   └── css/                 # 自定义样式
├── scripts/
│   ├── blog.sh              # CRUD管理脚本
│   ├── publish.sh           # 发布脚本（兼容保留）
│   ├── publish-guide.md     # 发布指南
│   ├── weekly-summary.js    # 每周总结脚本
│   └── maintenance-guide.md # 维护指南
├── themes/
│   └── butterfly/           # Butterfly主题
├── _config.yml              # Hexo配置
├── _config.butterfly.yml    # Butterfly主题配置
└── .github/workflows/
    ├── pages.yml            # 部署工作流
    └── weekly-summary.yml   # 每周总结工作流
```

---

## 三、内容管理脚本使用

### 3.1 脚本命令

```bash
./scripts/blog.sh <命令> [参数]
```

| 命令 | 描述 | 参数 |
|------|------|------|
| `new` | 创建新文章 | `<标题> [slug]` |
| `list` | 列出文章列表 | `[--all]` |
| `edit` | 编辑文章 | `<文件名>` |
| `delete` | 删除文章 | `<文件名>` |
| `preview` | 本地预览 | 无 |
| `publish` | 发布文章 | `<文件名>` |
| `help` | 显示帮助 | 无 |

### 3.2 使用示例

```bash
# 创建新文章
./scripts/blog.sh new "AI Agent 记忆机制" "ai-agent-memory"

# 列出文章
./scripts/blog.sh list

# 编辑文章
./scripts/blog.sh edit 2026-07-04-ai-agent-memory.md

# 预览效果
./scripts/blog.sh preview

# 发布文章
./scripts/blog.sh publish 2026-07-04-ai-agent-memory.md
```

---

## 四、文章撰写规范

### 4.1 Front-matter 配置

```yaml
---
title: "文章标题"
date: 2026-07-04 10:00:00
tags:
  - AI Agent
categories:
  - AI Agent
keywords: "关键词1, 关键词2"
description: "文章摘要，不超过150字"
top_img: "/img/banner/ai-agent.jpg"
cover: "/img/cover/ai-agent.png"
---
```

**分类规范**：

| 分类名 | 说明 | 知识文件 |
|--------|------|----------|
| AI Agent | 智能代理相关 | knowledge/ai-agent.md |
| Java | Java技术栈 | knowledge/java.md |
| Python | Python技术栈 | knowledge/python.md |
| 自动化 | 自动化工具流 | knowledge/automation.md |
| 云原生 | 云原生技术 | knowledge/cloud.md |

### 4.2 内容结构

参考 `source/_posts/template.md`，建议结构：

1. **摘要** - 一句话定位 + 核心价值 + 适用人群
2. **引言** - 背景 + 动机 + 目标
3. **核心概念** - 定义 + 原理 + 架构
4. **实践指南** - 环境准备 + 代码实现 + 步骤说明
5. **案例分析** - 背景 + 解决方案 + 效果评估
6. **最佳实践** - 技巧 + 优化 + 安全
7. **总结与展望** - 回顾 + 未来方向
8. **参考文献** + **相关资源**

---

## 五、知识图谱管理

### 5.1 知识文件结构

每个知识文件包含：
- **Front-matter**：标题、日期、类型
- **Markmap**：思维导图内容
- **相关文章**：自动更新的相关博客列表

### 5.2 Markmap 语法

```markdown
{% markmap %}
# 主题
## 分支1
- 子节点1
- 子节点2
## 分支2
- 子节点3
{% endmarkmap %}
```

### 5.3 手动更新知识图谱

```bash
# 编辑知识文件
./scripts/blog.sh edit knowledge/ai-agent.md

# 或直接编辑
vim source/knowledge/ai-agent.md
```

---

## 六、自动化流程

### 6.1 每周AI总结

**触发条件**：
- 每周日 12:00 UTC 自动运行
- 可在 GitHub Actions 手动触发

**执行流程**：

```
1. 检出代码
2. 安装依赖
3. 运行 weekly-summary.js
   ├── 扫描最近7天新增文章
   ├── 按分类分组文章
   ├── 调用AI分析文章内容
   ├── 更新对应知识文件的markmap
   └── 更新相关文章列表
4. 检查是否有变更
5. 创建 Pull Request（如有变更）
```

### 6.2 AI配置

在 GitHub 仓库设置中添加以下 Secrets：

| Secret | 说明 | 默认值 |
|--------|------|--------|
| `AI_API_KEY` | AI API密钥 | 必填 |
| `AI_API_BASE` | API基础URL | https://api.openai.com/v1 |
| `AI_MODEL` | 模型名称 | gpt-4o-mini |

### 6.3 部署流程

**触发条件**：推送到 `main` 分支

**执行流程**：

```
1. 检出代码
2. 安装依赖（Node.js 24）
3. 构建站点（hexo clean && hexo generate）
4. 上传产物
5. 部署到 GitHub Pages
```

---

## 七、搜索功能

### 7.1 配置说明

系统使用 `hexo-generator-searchdb` 插件实现本地搜索：

```yaml
# _config.butterfly.yml
search:
  enable: true
  type: local
  local_search:
    enable: true
    preload: true
    trigger: auto
    top_n_per_article: 1
```

### 7.2 搜索索引更新

搜索索引在 `hexo generate` 时自动生成，无需手动操作。

---

## 八、版本控制策略

### 8.1 Git 工作流

```
main（主分支）
├── 直接推送：文章内容、配置修改
└── PR合并：自动化更新、重大变更
```

### 8.2 Commit 规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 新增文章 | `feat: 添加文章《标题》` | `feat: 添加文章《AI Agent 入门指南》` |
| 更新文章 | `update: 更新文章《标题》` | `update: 更新文章《AI Agent 入门指南》` |
| 修复问题 | `fix: 修复文章《标题》中的问题` | `fix: 修复文章《AI Agent 入门指南》中的代码错误` |
| 自动化更新 | `chore: update knowledge graphs` | 由 GitHub Actions 自动生成 |

### 8.3 数据恢复

如果误删文章，可以通过 Git 恢复：

```bash
# 查看最近提交
git log --oneline -10

# 恢复到指定提交
git revert <commit-hash>

# 或重置（谨慎使用）
git reset --hard <commit-hash>
```

---

## 九、维护检查清单

### 9.1 日常维护

- [ ] 检查 GitHub Actions 工作流状态
- [ ] 验证新发布文章是否正常显示
- [ ] 检查搜索功能是否正常
- [ ] 确保知识图谱链接正确

### 9.2 每周检查

- [ ] 查看 weekly-summary 工作流是否成功
- [ ] 审核自动生成的 Pull Request
- [ ] 更新知识图谱内容（如需要）

### 9.3 每月检查

- [ ] 清理无效或过时的文章
- [ ] 检查依赖版本更新
- [ ] 优化文章SEO
- [ ] 备份重要内容

---

## 十、故障排查

### 10.1 部署失败

**常见原因**：
1. Node.js 版本不兼容 → 确认工作流使用 Node.js 24
2. 依赖安装失败 → 检查 package.json 和网络
3. 构建错误 → 检查文章 Markdown 语法

**排查步骤**：
1. 访问 GitHub Actions 日志
2. 查看错误信息
3. 本地运行 `npx hexo clean && npx hexo generate` 验证

### 10.2 知识图谱不更新

**常见原因**：
1. AI_API_KEY 未配置或无效
2. 文章分类与知识文件映射不匹配
3. Markmap 语法错误

**排查步骤**：
1. 检查 GitHub Secrets 配置
2. 验证文章 Front-matter 的 categories 字段
3. 检查知识文件中的 markmap 标签

### 10.3 搜索结果异常

**常见原因**：
1. 搜索索引未重新生成
2. 文章内容格式问题

**排查步骤**：
1. 重新运行 `npx hexo clean && npx hexo generate`
2. 检查 `public/search.xml` 是否生成

---

## 十一、扩展指南

### 11.1 添加新分类

1. 创建知识文件：`source/knowledge/new-category.md`
2. 更新分类映射：`scripts/weekly-summary.js` 中的 `categoryMap`
3. 更新知识入口页：`source/knowledge/index.md`

### 11.2 自定义主题

1. 修改 `source/css/custom.css`
2. 或编辑 `themes/butterfly/source/css/` 中的样式文件

### 11.3 添加新功能

1. 安装 Hexo 插件：`npm install hexo-plugin-name`
2. 在 `_config.yml` 中配置插件
3. 在 `_config.butterfly.yml` 中启用相关功能

---

## 十二、常用命令速查

| 命令 | 说明 |
|------|------|
| `./scripts/blog.sh new "标题" "slug"` | 创建新文章 |
| `./scripts/blog.sh list` | 列出文章 |
| `./scripts/blog.sh preview` | 本地预览 |
| `npx hexo clean` | 清理缓存 |
| `npx hexo generate` | 生成静态文件 |
| `npx hexo server` | 启动服务器 |
| `git add . && git commit && git push` | 提交并推送 |