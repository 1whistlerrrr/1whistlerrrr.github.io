---
title: 思维导图
date: 2024-01-01 10:00:00
type: "mindmap"
---

## 🌐 思维导图集合

将树形结构的知识笔记转化为可交互的思维导图，支持缩放、折叠、搜索。

---

## 📁 导图列表

{% mindmap_list %}
{% endmindmap_list %}

---

## 📖 使用说明

1. 将树形文本（使用 `├─` `└─` `│` 字符）放入 `source/raw_mindmap/` 目录
2. 运行 `python scripts/convert_mindmap.py` 转换为 markmap 格式
3. 推送到 GitHub 后，GitHub Actions 会自动转换并部署

> 转换脚本：`scripts/convert_mindmap.py`
