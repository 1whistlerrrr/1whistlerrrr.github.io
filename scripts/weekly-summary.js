const fs = require('fs');
const path = require('path');

const POSTS_DIR = path.join(__dirname, '../source/_posts');
const KNOWLEDGE_DIR = path.join(__dirname, '../source/knowledge');
const AI_API_KEY = process.env.AI_API_KEY;
const AI_API_BASE = process.env.AI_API_BASE || 'https://api.openai.com/v1';
const AI_MODEL = process.env.AI_MODEL || 'gpt-4o-mini';

const CATEGORY_MAP = {
  'AI Agent': { dir: 'ai-agent', label: 'AI Agent', emoji: '🧠' },
  'Java': { dir: 'java', label: 'Java', emoji: '☕' },
  'Python': { dir: 'python', label: 'Python', emoji: '🐍' },
  '自动化': { dir: 'automation', label: '自动化', emoji: '🔄' },
  '云原生': { dir: 'cloud', label: '云原生', emoji: '☁️' }
};

const CATEGORY_DESCRIPTIONS = {
  'AI Agent': '智能代理核心技术与应用',
  'Java': 'Java技术栈与微服务架构',
  'Python': 'Python技术栈与AI开发',
  '自动化': '自动化工具流与CI/CD',
  '云原生': '容器化与云服务技术'
};

async function fetchAIResponse(prompt) {
  if (!AI_API_KEY) {
    console.log('[WARN] AI_API_KEY not set, skipping AI analysis');
    return null;
  }

  try {
    const response = await fetch(`${AI_API_BASE}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${AI_API_KEY}`
      },
      body: JSON.stringify({
        model: AI_MODEL,
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.3,
        max_tokens: 2000
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.choices[0].message.content;
  } catch (error) {
    console.error('[ERROR] AI API call failed:', error.message);
    return null;
  }
}

function parseYAMLList(frontMatter, key) {
  const lines = frontMatter.split('\n');
  const result = [];
  let inList = false;
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    if (trimmed.startsWith(`${key}:`)) {
      inList = true;
      if (trimmed.includes('-')) {
        const item = trimmed.match(/- \s*(.+)/);
        if (item) result.push(item[1].trim());
      }
    } else if (inList && trimmed.startsWith('- ')) {
      result.push(trimmed.substring(2).trim());
    } else if (inList && !trimmed.startsWith('-') && trimmed !== '') {
      break;
    }
  }
  
  return result;
}

function getAllPosts() {
  const posts = [];
  const files = fs.readdirSync(POSTS_DIR);

  files.forEach(file => {
    if (file.endsWith('.md') && file !== 'template.md') {
      const filePath = path.join(POSTS_DIR, file);
      const content = fs.readFileSync(filePath, 'utf8');
      const frontMatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
      let title = file.replace('.md', '');
      let categories = [];
      let tags = [];

      if (frontMatterMatch) {
        const frontMatter = frontMatterMatch[1];
        const titleMatch = frontMatter.match(/title:\s*["']([^"']+)["']/);
        
        if (titleMatch) title = titleMatch[1];
        categories = parseYAMLList(frontMatter, 'categories');
        tags = parseYAMLList(frontMatter, 'tags');
      }

      posts.push({
        file,
        title,
        categories,
        tags,
        content: content.substring(0, 500)
      });
    }
  });

  return posts.sort((a, b) => b.file.localeCompare(a.file));
}

function getRecentPosts(days = 7) {
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - days);

  const posts = [];
  const files = fs.readdirSync(POSTS_DIR);

  files.forEach(file => {
    if (file.endsWith('.md') && file !== 'template.md') {
      const filePath = path.join(POSTS_DIR, file);
      const stats = fs.statSync(filePath);
      if (stats.mtime > cutoffDate) {
        const content = fs.readFileSync(filePath, 'utf8');
        const frontMatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
        let title = file.replace('.md', '');
        let categories = [];
        let tags = [];

        if (frontMatterMatch) {
          const frontMatter = frontMatterMatch[1];
          const titleMatch = frontMatter.match(/title:\s*["']([^"']+)["']/);
          
          if (titleMatch) title = titleMatch[1];
          categories = parseYAMLList(frontMatter, 'categories');
          tags = parseYAMLList(frontMatter, 'tags');
        }

        posts.push({
          file,
          title,
          categories,
          tags,
          content: content.substring(0, 500),
          date: stats.mtime
        });
      }
    }
  });

  return posts.sort((a, b) => b.date - a.date);
}

function extractMarkmap(content) {
  const match = content.match(/{% markmap %}\n([\s\S]*?)\n{% endmarkmap %}/);
  return match ? match[1] : null;
}

function replaceMarkmap(content, newMarkmap) {
  return content.replace(/{% markmap %}\n([\s\S]*?)\n{% endmarkmap %}/, `{% markmap %}\n${newMarkmap}\n{% endmarkmap %}`);
}

async function updateKnowledgeFile(category, posts) {
  const categoryInfo = CATEGORY_MAP[category];
  if (!categoryInfo) return;

  const filePath = path.join(KNOWLEDGE_DIR, categoryInfo.dir, 'index.md');
  if (!fs.existsSync(filePath)) return;

  const content = fs.readFileSync(filePath, 'utf8');
  const existingMarkmap = extractMarkmap(content);

  if (!existingMarkmap) {
    console.log(`[INFO] No markmap found in ${categoryInfo.dir}/index.md`);
    return;
  }

  const prompt = `
你是一个技术博客知识图谱维护助手。请根据以下本周新增的博客文章，更新现有的思维导图（markmap）。

现有思维导图内容：
${existingMarkmap}

本周新增文章：
${posts.map(p => `- ${p.title} (标签: ${p.tags.join(', ')})`).join('\n')}

要求：
1. 只更新思维导图的内容，不改变其他部分
2. 将新增文章的核心知识点添加到合适的分支下
3. 保持思维导图结构清晰，层级不超过4层
4. 如果文章内容与现有分支不匹配，可以新增分支
5. 输出格式为纯Markdown列表，不要包含{% markmap %}标签
6. 优化分支名称，使其更具概括性

输出示例格式：
# AI Agent
## 基础概念
- 智能代理定义
- Agent 架构模式
## 核心技术
- 大语言模型
  - GPT
  - LLaMA
`;

  const newMarkmap = await fetchAIResponse(prompt);
  if (!newMarkmap) return;

  const updatedContent = replaceMarkmap(content, newMarkmap.trim());
  fs.writeFileSync(filePath, updatedContent, 'utf8');
  console.log(`[SUCCESS] Updated ${categoryInfo.dir}/index.md markmap`);
}

function updateKnowledgeIndex(posts) {
  const filePath = path.join(KNOWLEDGE_DIR, 'index.md');
  if (!fs.existsSync(filePath)) return;

  const content = fs.readFileSync(filePath, 'utf8');

  const categoryStats = {};
  Object.keys(CATEGORY_MAP).forEach(cat => {
    categoryStats[cat] = 0;
  });

  posts.forEach(post => {
    post.categories.forEach(cat => {
      if (categoryStats[cat] !== undefined) {
        categoryStats[cat]++;
      }
    });
  });

  let tableRows = '';
  Object.keys(CATEGORY_MAP).forEach(cat => {
    const info = CATEGORY_MAP[cat];
    const count = categoryStats[cat];
    const desc = CATEGORY_DESCRIPTIONS[cat];
    tableRows += `| [${info.emoji} ${cat}](/knowledge/${info.dir}/) | ${desc} | ${count} |\n`;
  });

  const newTable = `## 📁 知识分类\n\n| 分类 | 描述 | 文章数 |\n|------|------|--------|\n${tableRows}`;
  const updatedContent = content.replace(/## 📁 知识分类\n[\s\S]*?\n---/, `${newTable}\n---`);
  
  fs.writeFileSync(filePath, updatedContent, 'utf8');
  console.log('[SUCCESS] Updated knowledge index with category stats');
}

function getPermalink(file) {
  const dateMatch = file.match(/^(\d{4})-(\d{2})-(\d{2})-.+\.md$/);
  if (dateMatch) {
    const [, year, month, day] = dateMatch;
    const title = file.replace('.md', '');
    return `/${year}/${month}/${day}/${title}/`;
  }
  
  const filePath = path.join(POSTS_DIR, file);
  const stats = fs.statSync(filePath);
  const date = new Date(stats.birthtime || stats.mtime);
  const year = date.getFullYear().toString();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const title = file.replace('.md', '');
  
  return `/${year}/${month}/${day}/${title}/`;
}

function updateRelatedPosts(posts) {
  const directories = fs.readdirSync(KNOWLEDGE_DIR, { withFileTypes: true });
  
  directories.forEach(dir => {
    if (dir.isDirectory()) {
      const filePath = path.join(KNOWLEDGE_DIR, dir.name, 'index.md');
      if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        
        let displayCategory = null;
        for (const [cat, info] of Object.entries(CATEGORY_MAP)) {
          if (info.dir === dir.name) {
            displayCategory = cat;
            break;
          }
        }
        
        if (!displayCategory) {
          displayCategory = dir.name;
        }
        
        const relatedPosts = posts.filter(p => p.categories.includes(displayCategory));
        
        let relatedSection = '## 📚 相关文章\n\n';
        if (relatedPosts.length > 0) {
          relatedSection += relatedPosts.map(p => {
            const permalink = getPermalink(p.file);
            return `- [${p.title}](${permalink})`;
          }).join('\n');
        } else {
          relatedSection += '暂无相关文章';
        }
        
        content = content.replace(/## 📚 相关文章\n[\s\S]*?$/, relatedSection);
        fs.writeFileSync(filePath, content, 'utf8');
      }
    }
  });

  console.log('[SUCCESS] Updated related posts sections');
}

async function main() {
  console.log('[INFO] Starting weekly summary generation...');
  
  const allPosts = getAllPosts();
  console.log(`[INFO] Found ${allPosts.length} total posts`);
  
  updateKnowledgeIndex(allPosts);
  
  updateRelatedPosts(allPosts);
  
  const recentPosts = getRecentPosts(7);
  if (recentPosts.length > 0) {
    console.log(`[INFO] Found ${recentPosts.length} recent posts:`);
    recentPosts.forEach(p => console.log(`  - ${p.title} (分类: ${p.categories.join(', ')})`));

    const categoryPosts = {};
    recentPosts.forEach(post => {
      post.categories.forEach(cat => {
        if (!categoryPosts[cat]) categoryPosts[cat] = [];
        categoryPosts[cat].push(post);
      });
    });

    for (const [category, catPosts] of Object.entries(categoryPosts)) {
      console.log(`[INFO] Processing category: ${category}`);
      await updateKnowledgeFile(category, catPosts);
    }
  } else {
    console.log('[INFO] No recent posts found for AI analysis');
  }
  
  console.log('[INFO] Weekly summary generation completed');
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  getAllPosts,
  getRecentPosts,
  updateKnowledgeFile,
  updateKnowledgeIndex,
  updateRelatedPosts
};