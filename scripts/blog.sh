#!/bin/bash

set -e

POSTS_DIR="source/_posts"
TEMPLATE_FILE="${POSTS_DIR}/template.md"
EDITOR="${EDITOR:-vim}"

CATEGORIES=(
  "AI Agent"
  "Java"
  "Python"
  "自动化"
  "云原生"
)

TAGS_MAP=(
  "AI Agent"
  "Java"
  "Python"
  "自动化"
  "云原生"
)

CATEGORY_COLORS=(
  "\033[0;34m"
  "\033[0;32m"
  "\033[0;35m"
  "\033[0;36m"
  "\033[0;33m"
)

NC="\033[0m"

print_usage() {
  echo "博客内容管理工具"
  echo ""
  echo "用法: ./scripts/blog.sh <命令> [参数]"
  echo ""
  echo "命令:"
  echo "  new <标题> [slug]          创建新文章（含主题选择）"
  echo "  list [--all]              列出文章列表"
  echo "  edit <文件名>             编辑文章"
  echo "  delete <文件名>           删除文章"
  echo "  upload <文件名> <文章名>  上传附件到文章目录"
  echo "  preview                   启动本地预览服务器"
  echo "  publish <文件名>          发布文章（提交并推送）"
  echo "  help                      显示帮助信息"
  echo ""
  echo "示例:"
  echo "  ./scripts/blog.sh new \"AI Agent 入门指南\" \"ai-agent-intro\""
  echo "  ./scripts/blog.sh list"
  echo "  ./scripts/blog.sh upload image.png 2026-07-05-ai-agent-intro.md"
  echo "  ./scripts/blog.sh preview"
}

select_category() {
  echo ""
  echo "📁 请选择文章主题（分类）:"
  echo ""
  
  for i in "${!CATEGORIES[@]}"; do
    printf "  %d. %s%s%s\n" $((i+1)) "${CATEGORY_COLORS[i]}" "${CATEGORIES[i]}" "$NC"
  done
  
  echo ""
  echo -n "请输入序号 [1-${#CATEGORIES[@]}]: "
  read -r selection
  
  if ! [[ "$selection" =~ ^[0-9]+$ ]] || [ "$selection" -lt 1 ] || [ "$selection" -gt "${#CATEGORIES[@]}" ]; then
    echo "❌ 无效输入，请重新选择"
    select_category
    return
  fi
  
  SELECTED_CATEGORY="${CATEGORIES[$((selection-1))]}"
  SELECTED_TAG="${TAGS_MAP[$((selection-1))]}"
  
  echo ""
  echo "✅ 已选择主题: ${CATEGORY_COLORS[$((selection-1))]}${SELECTED_CATEGORY}${NC}"
}

create_post_content() {
  local title="$1"
  local date="$2"
  local time="$3"
  local category="$4"
  local tag="$5"
  
  cat <<EOF
---
title: "${title}"
date: ${date} ${time}
tags:
  - ${tag}
categories:
  - ${category}
keywords: "${tag}"
description: ""
top_img: ""
cover: ""
---

## 摘要

**一句话定位**：

**核心价值**：

**适用人群**：

---

## 一、引言

### 1.1 背景


### 1.2 动机


### 1.3 目标


---

## 二、核心概念

### 2.1 概念定义


### 2.2 技术原理


### 2.3 架构设计


---

## 三、实践指南

### 3.1 环境准备


### 3.2 代码实现


### 3.3 步骤说明


### 3.4 常见问题


---

## 四、案例分析

### 4.1 案例背景


### 4.2 解决方案


### 4.3 效果评估


---

## 五、最佳实践

### 5.1 技巧与建议


### 5.2 性能优化


### 5.3 安全考虑


---

## 六、总结与展望

### 6.1 核心要点回顾


### 6.2 未来发展方向


---

## 参考文献


## 相关资源


> "引用一句与主题相关的名言，增强文章的深度和感染力。"
EOF
}

cmd_new() {
  if [ -z "$1" ]; then
    echo "错误: 请提供文章标题"
    echo "用法: ./scripts/blog.sh new <标题> [slug]"
    exit 1
  fi

  TITLE="$1"
  SLUG="$2"
  DATE=$(date +%Y-%m-%d)
  TIME=$(date +%H:%M:%S)

  if [ -z "$SLUG" ]; then
    SLUG=$(echo "${TITLE}" | sed -e 's/[^[:alnum:]]/-/g' | sed -e 's/^-*//' -e 's/-*$//' | tr '[:upper:]' '[:lower:]')
    if [ -z "$SLUG" ]; then
      SLUG="post"
    fi
  fi

  FILENAME="${DATE}-${SLUG}.md"
  FILEPATH="${POSTS_DIR}/${FILENAME}"

  if [ -f "${FILEPATH}" ]; then
    echo "错误: 文件已存在 ${FILEPATH}"
    exit 1
  fi

  select_category

  create_post_content "${TITLE}" "${DATE}" "${TIME}" "${SELECTED_CATEGORY}" "${SELECTED_TAG}" > "${FILEPATH}"

  ASSET_FOLDER="${POSTS_DIR}/${FILENAME%.md}"
  mkdir -p "${ASSET_FOLDER}"

  echo ""
  echo "🎉 文章已创建: ${FILEPATH}"
  echo ""
  echo "📁 附件目录: ${ASSET_FOLDER}/"
  echo ""
  echo "📝 下一步操作:"
  echo "  ./scripts/blog.sh edit ${FILENAME}"
  echo "  ./scripts/blog.sh upload <文件> ${FILENAME}"
  echo "  ./scripts/blog.sh preview"
  echo "  ./scripts/blog.sh publish ${FILENAME}"
}

cmd_list() {
  local show_all=false
  if [ "$1" = "--all" ]; then
    show_all=true
  fi

  echo "📋 文章列表:"
  echo "─────────────────────────────────────────────────────"
  
  local count=0
  for file in "${POSTS_DIR}"/*.md; do
    [ -f "$file" ] || continue
    
    local filename=$(basename "$file")
    if [ "$filename" = "template.md" ] && [ "$show_all" = false ]; then
      continue
    fi

    local content=$(cat "$file")
    local title=$(echo "$content" | grep -m 1 "^title:" | sed 's/title:\s*["'\''"]\([^"'\'']*\)["'\''"]/\1/')
    if [ -z "$title" ]; then
      title="$filename"
    fi

    local date=$(echo "$content" | grep -m 1 "^date:" | sed 's/date:\s*//')
    if [ -z "$date" ]; then
      date=$(stat -f "%Sm" "$file" | cut -d' ' -f1-3)
    fi

    local categories=$(echo "$content" | grep -A5 "^categories:" | grep "- " | sed 's/- //' | tr '\n' ', ' | sed 's/, $//')
    local tags=$(echo "$content" | grep -A5 "^tags:" | grep "- " | sed 's/- //' | tr '\n' ', ' | sed 's/, $//')

    printf "%-30s %-20s\n" "$title" "$date"
    if [ -n "$categories" ] || [ -n "$tags" ]; then
      printf "        分类: %-20s 标签: %s\n" "$categories" "$tags"
    fi
    count=$((count + 1))
  done

  echo "─────────────────────────────────────────────────────"
  echo "共 ${count} 篇文章"
}

cmd_edit() {
  if [ -z "$1" ]; then
    echo "错误: 请提供要编辑的文件名"
    echo "用法: ./scripts/blog.sh edit <文件名>"
    exit 1
  fi

  FILEPATH="${POSTS_DIR}/$1"

  if [ ! -f "${FILEPATH}" ]; then
    echo "错误: 文件不存在 ${FILEPATH}"
    exit 1
  fi

  "${EDITOR}" "${FILEPATH}"
  echo ""
  echo "✏️  编辑完成: ${FILEPATH}"
}

cmd_delete() {
  if [ -z "$1" ]; then
    echo "错误: 请提供要删除的文件名"
    echo "用法: ./scripts/blog.sh delete <文件名>"
    exit 1
  fi

  FILEPATH="${POSTS_DIR}/$1"

  if [ ! -f "${FILEPATH}" ]; then
    echo "错误: 文件不存在 ${FILEPATH}"
    exit 1
  fi

  echo -n "⚠️  确认删除 ${FILEPATH} 吗？(y/N): "
  read -r confirm
  if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "取消删除"
    exit 0
  fi

  ASSET_FOLDER="${POSTS_DIR}/${1%.md}"
  if [ -d "${ASSET_FOLDER}" ]; then
    git rm -rf "${ASSET_FOLDER}"
  fi
  
  git rm "${FILEPATH}"
  
  echo ""
  echo "🗑️  文件已删除: ${FILEPATH}"
  echo ""
  echo "💡  提示: 如果误删，可以使用 git revert 恢复"
}

cmd_upload() {
  if [ -z "$1" ] || [ -z "$2" ]; then
    echo "错误: 请提供要上传的文件和目标文章"
    echo "用法: ./scripts/blog.sh upload <文件路径> <文章文件名>"
    exit 1
  fi

  SOURCE_FILE="$1"
  POST_FILE="$2"
  POST_FILEPATH="${POSTS_DIR}/${POST_FILE}"

  if [ ! -f "${SOURCE_FILE}" ]; then
    echo "错误: 源文件不存在 ${SOURCE_FILE}"
    exit 1
  fi

  if [ ! -f "${POST_FILEPATH}" ]; then
    echo "错误: 目标文章不存在 ${POST_FILEPATH}"
    exit 1
  fi

  ASSET_FOLDER="${POSTS_DIR}/${POST_FILE%.md}"
  mkdir -p "${ASSET_FOLDER}"

  FILENAME=$(basename "${SOURCE_FILE}")
  DEST_FILE="${ASSET_FOLDER}/${FILENAME}"

  if [ -f "${DEST_FILE}" ]; then
    echo -n "⚠️  文件已存在，是否覆盖？(y/N): "
    read -r overwrite
    if [ "$overwrite" != "y" ] && [ "$overwrite" != "Y" ]; then
      echo "取消上传"
      exit 0
    fi
  fi

  cp "${SOURCE_FILE}" "${DEST_FILE}"
  git add "${DEST_FILE}"

  echo ""
  echo "📤 文件已上传: ${DEST_FILE}"
  echo ""
  echo "📝 在文章中引用方式:"
  echo "  {% asset_img ${FILENAME} \"图片描述\" %}"
  echo "  ![图片描述](/${POST_FILE%.md}/${FILENAME})"
}

cmd_preview() {
  echo "🚀 启动本地预览服务器..."
  echo ""
  echo "访问: http://localhost:4000/"
  echo "按 Ctrl+C 停止服务器"
  echo ""
  
  npx hexo clean && npx hexo server
}

cmd_publish() {
  if [ -z "$1" ]; then
    echo "错误: 请提供要发布的文件名"
    echo "用法: ./scripts/blog.sh publish <文件名>"
    exit 1
  fi

  FILEPATH="${POSTS_DIR}/$1"

  if [ ! -f "${FILEPATH}" ]; then
    echo "错误: 文件不存在 ${FILEPATH}"
    exit 1
  fi

  local content=$(cat "${FILEPATH}")
  local title=$(echo "$content" | grep -m 1 "^title:" | sed 's/title:\s*["'\''"]\([^"'\'']*\)["'\''"]/\1/')
  if [ -z "$title" ]; then
    title="$1"
  fi

  ASSET_FOLDER="${POSTS_DIR}/${1%.md}"
  if [ -d "${ASSET_FOLDER}" ]; then
    git add "${ASSET_FOLDER}"
  fi

  echo ""
  echo "📦 准备发布文章: ${title}"
  echo ""

  echo "1️⃣  暂存文件..."
  git add "${FILEPATH}"

  echo "2️⃣  提交更改..."
  git commit -m "feat: 添加文章《${title}》"

  echo "3️⃣  推送到远程..."
  git push origin main

  echo ""
  echo "✅ 发布完成！"
  echo ""
  echo "🌐 部署成功后访问: https://1whistlerrrr.github.io"
}

case "$1" in
  new)
    cmd_new "$2" "$3"
    ;;
  list)
    cmd_list "$2"
    ;;
  edit)
    cmd_edit "$2"
    ;;
  delete)
    cmd_delete "$2"
    ;;
  upload)
    cmd_upload "$2" "$3"
    ;;
  preview)
    cmd_preview
    ;;
  publish)
    cmd_publish "$2"
    ;;
  help)
    print_usage
    ;;
  *)
    print_usage
    exit 1
    ;;
esac