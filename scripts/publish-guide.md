# 博客文章提交工作流程

## 一、文章撰写流程

### 1.1 使用自动化脚本新建文章

```bash
# 用法
./scripts/publish.sh <中文标题> [英文slug]

# 示例
./scripts/publish.sh "AI Agent 入门指南" "ai-agent-introduction"
```

脚本会自动创建文件 `source/_posts/YYYY-MM-DD-英文slug.md`，并替换模板中的标题和日期。

### 1.2 手动创建文章（备用）

在 `source/_posts/` 目录下创建新文件，文件名格式为：

```
YYYY-MM-DD-英文slug.md
```

示例：`2026-07-04-ai-agent-memory-mechanism.md`

### 1.3 使用模板

参考 `source/_posts/template.md` 文件，按照模板结构撰写文章。

### 1.4 Front-matter 配置

文章开头必须包含以下配置：

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

**必填项**：
- `title`：文章标题
- `date`：发布日期（格式：YYYY-MM-DD HH:MM:SS）
- `tags`：标签列表（最多4个）
- `categories`：分类列表

**可选项**：
- `keywords`：SEO关键词
- `description`：文章摘要
- `top_img`：顶部横幅图片
- `cover`：封面图片

### 1.5 文章内容规范

**格式要求**：
- 使用 Markdown 语法
- 代码块使用 ```python 或 ```bash 标识语言
- 引用使用 > 符号
- 列表使用 - 或 1. 格式

**内容结构**（建议）：
1. 摘要（一句话定位 + 核心价值 + 适用人群）
2. 引言（背景 + 动机 + 目标）
3. 核心概念（定义 + 原理 + 架构）
4. 实践指南（环境准备 + 代码实现 + 步骤说明）
5. 案例分析（背景 + 解决方案 + 效果评估）
6. 最佳实践（技巧 + 优化 + 安全）
7. 总结与展望（回顾 + 未来方向）
8. 参考文献 + 相关资源

---

## 二、本地预览

### 2.1 启动本地服务器

```bash
cd /Volumes/macos/IDEAProject/private-web
npx hexo clean && npx hexo server
```

访问 **http://localhost:4000/** 查看效果。

### 2.2 验证检查清单

- [ ] 文章标题正确显示
- [ ] 标签和分类正确显示
- [ ] 代码高亮正常
- [ ] 图片加载正常
- [ ] 移动端适配正常
- [ ] 无语法错误

---

## 三、提交到 GitHub

### 3.1 暂存文件

```bash
git add source/_posts/YYYY-MM-DD-英文slug.md
```

### 3.2 提交更改

```bash
git commit -m "feat: 添加文章《文章标题》"
```

**Commit 消息规范**：
- 新增文章：`feat: 添加文章《标题》`
- 更新文章：`update: 更新文章《标题》`
- 修复问题：`fix: 修复文章《标题》中的问题`

### 3.3 推送到远程

```bash
git push origin main
```

---

## 四、自动部署

### 4.1 GitHub Actions 工作流

推送后，GitHub Actions 会自动执行以下流程：

1. **检出代码**：从 main 分支拉取最新代码
2. **安装依赖**：使用 npm ci 安装依赖（Node.js 24）
3. **构建站点**：执行 hexo clean && hexo generate
4. **上传产物**：将 public 目录上传为 artifact
5. **部署到 Pages**：使用 actions/deploy-pages@v4 部署

### 4.2 查看部署状态

访问 **https://github.com/1whistlerrrr/1whistlerrrr.github.io/actions** 查看工作流状态。

- ✅ 绿色：部署成功
- ❌ 红色：部署失败，查看日志排查问题

### 4.3 访问网站

部署成功后，访问 **https://1whistlerrrr.github.io** 查看新文章。

---

## 五、常用命令速查

| 命令 | 说明 |
|------|------|
| `./scripts/publish.sh "标题" "slug"` | 使用脚本创建新文章 |
| `npx hexo new "文章标题"` | 创建新文章（自动生成日期） |
| `npx hexo generate` | 生成静态文件 |
| `npx hexo server` | 启动本地服务器 |
| `npx hexo clean` | 清理缓存 |
| `npx hexo deploy` | 部署到远程（需配置） |

---

## 六、注意事项

1. **图片资源**：将图片放在 `source/img/` 目录下，使用相对路径引用
2. **标签管理**：保持标签数量在 4 个以内，避免过度细分
3. **分类管理**：使用统一的分类体系（如 AI Agent、自动化、工具等）
4. **SEO 优化**：设置合适的 keywords 和 description
5. **代码质量**：确保代码示例可以正常运行
6. **内容原创**：确保文章内容为原创或获得授权
7. **文件名**：使用英文 slug，避免中文文件名

---

## 七、自动化脚本详解

### 7.1 脚本功能

- 自动生成符合规范的文件名
- 自动替换模板中的标题和日期
- 支持自定义英文 slug
- 防止重复创建文件

### 7.2 脚本位置

```
scripts/publish.sh
```

### 7.3 使用示例

```bash
# 创建文章，自动生成slug
./scripts/publish.sh "AI Agent 记忆机制详解"

# 创建文章，指定自定义slug
./scripts/publish.sh "AI Agent 记忆机制详解" "ai-agent-memory-mechanism"

# 脚本输出示例
🎉 文章已创建: source/_posts/2026-07-04-ai-agent-memory-mechanism.md

📝 请编辑文章内容后执行:
  git add source/_posts/2026-07-04-ai-agent-memory-mechanism.md
  git commit -m "feat: 添加文章《AI Agent 记忆机制详解》"
  git push origin main

🌐 部署成功后访问: https://1whistlerrrr.github.io
```

---

## 八、完整工作流流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    博客文章发布工作流                        │
├─────────────────────────────────────────────────────────────┤
│  1. 撰写文章                                                │
│     └── ./scripts/publish.sh "标题" "slug"                 │
│           ↓                                                │
│  2. 编辑内容                                                │
│     └── 按照 template.md 模板填充内容                       │
│           ↓                                                │
│  3. 本地预览                                                │
│     └── npx hexo clean && npx hexo server                 │
│           ↓                                                │
│  4. 检查验证                                                │
│     └── 标题/标签/代码/图片/移动端                          │
│           ↓                                                │
│  5. 提交代码                                                │
│     └── git add → git commit → git push                   │
│           ↓                                                │
│  6. 自动部署 (GitHub Actions)                               │
│     ├── 检出代码                                            │
│     ├── 安装依赖                                            │
│     ├── 构建站点                                            │
│     └── 部署到 Pages                                       │
│           ↓                                                │
│  7. 访问网站                                                │
│     └── https://1whistlerrrr.github.io                    │
└─────────────────────────────────────────────────────────────┘
```