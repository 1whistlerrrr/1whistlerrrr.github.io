#!/bin/bash

set -e

POSTS_DIR="source/_posts"
TEMPLATE_FILE="${POSTS_DIR}/template.md"
EDITOR="${EDITOR:-vim}"

print_usage() {
  echo "博客内容管理工具"
  echo ""
  echo "用法: ./scripts/blog.sh <命令> [参数]"
  echo ""
  echo "命令:"
  echo "  new <标题> [slug]    创建新文章"
  echo "  list [--all]          列出文章列表"
  echo "  edit <文件名>         编辑文章"
  echo "  delete <文件名>       删除文章"
  echo "  preview               启动本地预览服务器"
  echo "  publish <文件名>      发布文章（提交并推送）"
  echo "  help                  显示帮助信息"
  echo ""
  echo "示例:"
  echo "  ./scripts/blog.sh new \"AI Agent 入门指南\" \"ai-agent-intro\""
  echo "  ./scripts/blog.sh list"
  echo "  ./scripts/blog.sh edit 2026-07-04-ai-agent-intro.md"
  echo "  ./scripts/blog.sh delete 2026-07-04-ai-agent-intro.md"
  echo "  ./scripts/blog.sh preview"
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

  if [ ! -f "${TEMPLATE_FILE}" ]; then
    echo "错误: 模板文件不存在 ${TEMPLATE_FILE}"
    exit 1
  fi

  cp "${TEMPLATE_FILE}" "${FILEPATH}"
  sed -i "" "s/文章标题 - 简明扼要地概括核心内容/${TITLE}/g" "${FILEPATH}"
  sed -i "" "s/2026-07-04/${DATE}/g" "${FILEPATH}"
  sed -i "" "s/10:00:00/${TIME}/g" "${FILEPATH}"

  echo ""
  echo "🎉 文章已创建: ${FILEPATH}"
  echo ""
  echo "📝 下一步操作:"
  echo "  ./scripts/blog.sh edit ${FILENAME}"
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

  git rm "${FILEPATH}"
  
  echo ""
  echo "🗑️  文件已删除: ${FILEPATH}"
  echo ""
  echo "💡  提示: 如果误删，可以使用 git revert 恢复"
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