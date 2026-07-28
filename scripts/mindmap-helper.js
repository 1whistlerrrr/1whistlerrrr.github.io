/**
 * Hexo Tag Plugin: mindmap_list
 * 读取 source/mindmap/source/ 下所有 markmap 导图文件并生成链接列表。
 *
 * 用法：在任意 .md 页面中写 {% mindmap_list %}
 */
const fs = require('fs');
const path = require('path');

hexo.extend.tag.register('mindmap_list', function (args) {
  const sourceDir = path.join(hexo.source_dir, 'mindmap', 'source');
  const mindmapBaseUrl = '/mindmap/source/';

  let files = [];
  try {
    files = fs.readdirSync(sourceDir)
      .filter(f => f.endsWith('.md'))
      .sort();
  } catch (e) {
    return '<p><em>暂无思维导图。请将树形文本放入 source/raw_mindmap/ 并运行转换脚本。</em></p>';
  }

  if (files.length === 0) {
    return '<p><em>暂无思维导图。请将树形文本放入 source/raw_mindmap/ 并运行转换脚本。</em></p>';
  }

  let html = '<ul class="mindmap-list">\n';
  for (const file of files) {
    const name = file.replace(/\.md$/, '');
    let title = name;
    try {
      const content = fs.readFileSync(path.join(sourceDir, file), 'utf-8');
      const match = content.match(/^---\s*\ntitle:\s*(.+?)\s*\n---/);
      if (match) {
        title = match[1].replace(/['"]/g, '');
      }
    } catch (e) {
      // fallback to filename
    }
    const url = mindmapBaseUrl + name + '.html';
    html += `  <li><a href="${url}">🧠 ${title}</a></li>\n`;
  }
  html += '</ul>';
  return html;
}, { async: false });
