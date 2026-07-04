#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "用法: ./scripts/publish.sh <中文标题> [英文slug]"
  echo "示例: ./scripts/publish.sh \"AI Agent 入门指南\" \"ai-agent-introduction\""
  exit 1
fi

CHINESE_TITLE="$1"
ENGLISH_SLUG="$2"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)

if [ -z "$ENGLISH_SLUG" ]; then
  ENGLISH_SLUG=$(echo "${CHINESE_TITLE}" | sed -e 's/[^[:alnum:]]/-/g' | sed -e 's/^-*//' -e 's/-*$//' | tr '[:upper:]' '[:lower:]')
  if [ -z "$ENGLISH_SLUG" ]; then
    ENGLISH_SLUG="post"
  fi
fi

FILENAME="${DATE}-${ENGLISH_SLUG}.md"
FILEPATH="source/_posts/${FILENAME}"

if [ -f "${FILEPATH}" ]; then
  echo "错误: 文件已存在 ${FILEPATH}"
  exit 1
fi

cp source/_posts/template.md "${FILEPATH}"

sed -i "" "s/文章标题 - 简明扼要地概括核心内容/${CHINESE_TITLE}/g" "${FILEPATH}"
sed -i "" "s/2026-07-04/${DATE}/g" "${FILEPATH}"
sed -i "" "s/10:00:00/${TIME}/g" "${FILEPATH}"

echo ""
echo "🎉 文章已创建: ${FILEPATH}"
echo ""
echo "📝 请编辑文章内容后执行:"
echo "  git add ${FILEPATH}"
echo "  git commit -m \"feat: 添加文章《${CHINESE_TITLE}》\""
echo "  git push origin main"
echo ""
echo "🌐 部署成功后访问: https://1whistlerrrr.github.io"