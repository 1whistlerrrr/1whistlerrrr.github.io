#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "用法: ./scripts/publish.sh <文章标题>"
  exit 1
fi

TITLE="$1"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
TITLE_SLUG=$(echo "${TITLE}" | iconv -t ascii//TRANSLIT | sed -r 's/[^a-zA-Z0-9]+/-/g' | sed 's/^-//;s/-$//' | tr '[:upper:]' '[:lower:]')
FILENAME="${DATE}-${TITLE_SLUG}.md"
FILEPATH="source/_posts/${FILENAME}"

if [ -f "${FILEPATH}" ]; then
  echo "错误: 文件已存在 ${FILEPATH}"
  exit 1
fi

cp source/_posts/template.md "${FILEPATH}"

sed -i.bak "s/文章标题 - 简明扼要地概括核心内容/${TITLE}/g" "${FILEPATH}"
sed -i.bak "s/2026-07-04/${DATE}/g" "${FILEPATH}"
sed -i.bak "s/10:00:00/${TIME}/g" "${FILEPATH}"

rm "${FILEPATH}.bak"

echo ""
echo "🎉 文章已创建: ${FILEPATH}"
echo ""
echo "📝 请编辑文章内容后执行:"
echo "  git add ${FILEPATH}"
echo "  git commit -m \"feat: 添加文章《${TITLE}》\""
echo "  git push origin main"
echo ""
echo "🌐 部署成功后访问: https://1whistlerrrr.github.io"
