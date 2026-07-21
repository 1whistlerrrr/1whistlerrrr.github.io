# 个人主页构建资料调研报告

> 本文档为构建个人主页项目的前期资料汇总，涵盖设计案例、功能模块、技术方案、设计最佳实践、内容组织建议与部署维护方案六个维度，旨在为后续实际开发提供全面参考。

---

## 目录

1. [设计优秀的个人主页案例](#一设计优秀的个人主页案例)
2. [常用功能模块类型及实现方式](#二常用功能模块类型及实现方式)
3. [主流搭建技术方案调研](#三主流搭建技术方案调研)
4. [设计最佳实践](#四设计最佳实践)
5. [内容组织建议](#五内容组织建议)
6. [部署与维护方案](#六部署与维护方案)
7. [综合选型建议](#七综合选型建议)

---

## 一、设计优秀的个人主页案例

以下案例覆盖设计师、开发者、艺术家、内容创作者、建筑师等不同行业背景，体现多样的设计风格与功能侧重。

| # | 名称 | 行业背景 | 设计亮点 | 案例链接 |
|---|------|---------|---------|---------|
| 1 | **Brittany Chiang** | 前端开发者 | 极简单页设计，深色主题，左侧固定导航，技能与项目分区清晰，交互流畅 | brittanychiang.com |
| 2 | **Lee Robinson** | 开发者 / Vercel 布道师 | 黑白高对比，首屏即展示价值主张，博客与项目整合，强调内容可读性 | leeroo.com |
| 3 | **Alice Lee** | 独立设计师 / 插画师 | 色彩丰富鲜明，首屏铺满插画与壁画作品，极强的视觉冲击力，鼓励滚动探索 | alicelee.me |
| 4 | **Kristina Smolyar** | 模特 / 内容创作者 | 首屏背景视频自动播放，品牌合作 logo 滚动展示，内置联系表单，移动端体验佳 | kristinasmolyar.com |
| 5 | **Rafael Varona** | 插画师 / 动画师 | 鲜艳色彩主导，GIF 与图标交替按钮，每个项目独立详情页，作品自身说话 | rafaelvarona.com |
| 6 | **T Sakhi** | 建筑师 / 室内设计师 | 抽象视觉风格，故事优先于图库，每个项目附客户/地点/面积/承包商等关键信息 | tsakhi.com |
| 7 | **Dalya Baron** | 学术研究者 | 一页式入口 + 四页锚点（简历/研究/科普/个人），简洁克制，适合学术展示 | 个人学术站 |
| 8 | **Tony Gines** | 创意人 | 极简单页，左侧分类 + 社交链接，右侧交互式头像跟随鼠标，以简胜繁 | 个人站 |

### 案例共性总结

- **首屏即定位**：访客在 3 秒内明确"你是谁、做什么、能提供什么价值"。
- **作品为王**：创作者类站点让作品自身说话，文字极简；技术类站点则用项目卡片 + 案例研究讲清过程。
- **导航一致**：顶部或侧边固定导航，确保随时可跳转。
- **明确行动召唤**：每个案例都在显眼位置放置"联系我 / 查看作品 / 预约咨询"按钮。

> 参考来源：[Webflow 23 portfolio examples](https://webflow.com/blog/design-portfolio-examples)、[HubSpot 25 portfolio examples](https://blog.hubspot.com/website/examples-of-squarespace-websites)、[mandywebdesign 13 personal website examples](https://www.mandywebdesign.com/mandy/personal-website-examples/)

---

## 二、常用功能模块类型及实现方式

一个标准的个人主页通常由以下核心模块构成，可按需组合为单页（One-Page）或多页（Multi-Page）布局。

### 2.1 核心模块清单

| 模块 | 作用 | 关键内容 | 实现方式 |
|------|------|---------|---------|
| **头部 Header / 导航 Nav** | 品牌识别 + 站点导航 | 姓名/Logo、主导航菜单、移动端汉堡菜单 | `<header>` + `<nav>` 语义化标签；sticky 定位；响应式折叠 |
| **英雄区 Hero** | 首屏第一印象，3 秒抓住访客 | 姓名、职位/头衔、一句话价值主张、CTA 按钮、头像/背景图/视频 | 全屏 `<section>`，`<h1>` 标题，按钮锚点跳转；可加渐变/动画 |
| **关于我 About** | 建立个人连接与信任 | 个人故事、背景经历、价值观、照片、个性色彩 | `<section id="about">` + `<h2>`，图文混排，可链接到详细简历页 |
| **技能展示 Skills** | 快速扫描技术能力 | 技术栈、工具、语言、熟练度（可选进度条） | 技能卡片网格、`<ul>` 列表、标签云；建议分组分类 |
| **作品集 Portfolio / Projects** | 核心模块，证明能力 | 3-5 个最佳项目，含截图、描述、技术栈、链接、成果 | `<article>` + `<figure>` + `<figcaption>`；网格/卡片布局；点击进入案例详情页 |
| **经历/简历 Experience** | 展示职业轨迹 | 工作经历、教育背景、证书奖项 | 时间线（Timeline）布局；可提供 PDF 简历下载 |
| **博客 Blog** | 展示思考与持续输出 | 文章列表、分类、标签 | 文章卡片列表；Markdown 内容管理；分页/归档 |
| **推荐信 Testimonials** | 社会证明（可选） | 客户/同事评价、合作 logo | 引用块 + 头像；滚动轮播 |
| **联系 Contact** | 转化入口 | 联系表单、邮箱、社交链接、预约日历 | `<form>` 表单（接 Netlify Forms / Formspree）；社交图标链接 |
| **底部 Footer** | 版权与补充信息 | 版权声明、备案号、次要导航、社交链接 | `<footer>` + 版权年份自动更新 |

### 2.2 单页 vs 多页布局

- **单页布局（One-Page）**：所有模块在同一页面通过锚点平滑滚动串联。适合内容精简、强调快速浏览的开发者/设计师作品集。行业标准做法。
- **多页布局（Multi-Page）**：首页 + 独立的关于/作品集/博客/联系页。适合内容较多、需要深度案例研究的站点。SEO 表现更佳（每页可独立优化）。

### 2.3 推荐的页面结构骨架

```
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>姓名 - 职位 | 个人主页</title>
  <meta name="description" content="一句话价值主张">
</head>
<body>
  <header><nav>...</nav></header>
  <main>
    <section id="hero">...</section>
    <section id="about">...</section>
    <section id="skills">...</section>
    <section id="projects">...</section>
    <section id="contact">...</section>
  </main>
  <footer>...</footer>
</body>
</html>
```

> 参考来源：[CSDN 个人作品集网站设计](https://blog.csdn.net/2501_93104808/article/details/151968747)、[priygop Portfolio Structure](https://priygop.com/courses/html/html-project-portfolio-website)、[0xMinds portfolio prompts](https://0xminds.com/es/blog/guides/build-portfolio-website-ai-prompts-guide)

---

## 三、主流搭建技术方案调研

### 3.1 静态网站生成器（SSG）对比

静态网站生成器是 2025 年个人主页/博客的主流方案，核心优势：**快、便宜、免服务器、安全**。

| 生成器 | 语言 | GitHub Stars | 构建速度 | 学习曲线 | 适用场景 |
|--------|------|-------------|---------|---------|---------|
| **Astro** | JS | 50k+ | 快 | 中等 | 内容型站点首选，零 JS 默认，岛屿架构，框架无关（可混用 React/Vue/Svelte） |
| **Hugo** | Go | 80k+ | 极快（10000 页 <3 秒） | 中等 | 大型站点、追求极致构建速度，主题生态丰富 |
| **Next.js** | JS/React | 131k+ | 中等 | 较陡 | React 生态，需 SSR/ISR 等动态能力时选 |
| **Hexo** | JS | 40k+ | 中等（1000 页约 45 秒） | 低 | 中文社区成熟，博客传统选择 |
| **Gatsby** | JS/React | 55k+ | 慢（大型项目数分钟） | 较陡 | React + GraphQL，插件丰富但构建慢，2025 年热度下降 |
| **Jekyll** | Ruby | 49k+ | 慢 | 低 | GitHub Pages 原生支持，老牌选择 |
| **Eleventy (11ty)** | JS | 18k+ | 快 | 低 | 极简主义，最大控制权，无前端框架强绑定 |

#### 选型建议

- **内容型个人主页/博客**：首选 **Astro**（性能最佳，Lighthouse 满分，零 JS 默认）或 **Hugo**（构建最快，适合长期大量内容）。
- **已有 Hexo 基础**：当前项目为 Hexo，可继续使用，中文文档与主题生态成熟，迁移成本低。
- **需要复杂交互/React 生态**：选 **Next.js**（静态导出模式）。
- **极简追求**：选 **Eleventy**。

### 3.2 网站模板平台对比

| 平台 | 类型 | 优势 | 劣势 | 适用人群 |
|------|------|------|------|---------|
| **GitHub Pages** | 免费静态托管 | 完全免费、自动 HTTPS、Git 工作流、支持自定义域名 | 仅静态、无服务端、构建管线偏简单（Jekyll 导向） | 开发者、技术型用户 |
| **WordPress + Elementor** | CMS + 可视化构建器 | 完全控制权、插件生态庞大、可视化拖拽、SEO 插件丰富 | 需自备主机、维护成本高、性能需优化 | 非技术用户、需后台管理 |
| **Squarespace** | 一体化 SaaS | 模板精美、全托管、零维护 | 月费较高、定制受限、数据导出难 | 创作者、设计师、小企业 |
| **Webflow** | 可视化开发平台 | 设计自由度高、生成干净代码、CMS 功能 | 学习曲线、付费、免费版受限 | 专业设计师 |
| **Notion + Super/Potion** | Notion 转站点 | 写作体验极佳、零构建 | 定制有限、性能一般 | 内容创作者、快速上线 |
| **Wix / Framer** | SaaS 构建器 | 拖拽简单、模板多 | 免费版带广告、迁移困难 | 初学者 |

### 3.3 前端技术栈选择

| 层级 | 主流选择 | 说明 |
|------|---------|------|
| **核心三件** | HTML5 + CSS3 + JavaScript (ES6+) | 语义化标签、Flexbox/Grid 布局、原生 JS 已足够强大 |
| **CSS 方案** | Tailwind CSS / 原生 CSS / Sass/SCSS | Tailwind 是 2025 最流行，原子化、一致性高；SCSS 适合传统项目 |
| **UI 组件库** | shadcn/ui、Radix、Headless UI、daisyUI | 个人主页通常无需重型组件库，轻量 Headless 组件即可 |
| **动画库** | Framer Motion、GSAP、AOS、CSS 动画 | 微交互提升质感，但切忌过度 |
| **图标** | Lucide、Heroicons、Font Awesome | 推荐 Lucide（轻量、tree-shaking） |
| **字体** | Google Fonts、Fontsource（自托管） | 自托管字体性能与隐私更佳 |
| **框架（可选）** | React / Vue / Svelte / Astro 组件 | 仅在需要交互组件时引入，Astro 可零 JS |

#### 当前项目技术栈

当前项目为 **Hexo** 博客（基于 `source/_posts` 结构判断）。Hexo 使用 Node.js，模板语言灵活（EJS/Pug/Nunjucks），主题生态丰富，适合继续作为内容发布平台。若要构建独立的个人主页作品集模块，可：
- 方案 A：在 Hexo 中新增自定义页面 + 主题定制（迁移成本最低）
- 方案 B：另起 Astro 项目做作品集主页，博客保留 Hexo（性能最优）
- 方案 C：整体迁移到 Astro（统一技术栈，长期最优）

> 参考来源：[2025博客框架选择指南](https://juejin.cn/post/7578714735307849754)、[12 Best Static Site Generators 2025](https://www.jekyllpad.com/blog/best-static-site-generators)、[Static Site Generators Comparison 2025](https://www.apatero.com/blog/static-site-generators-comparison-jamstack-2025)、[IONOS Best SSG](https://www.ionos.co.uk/digitalguide/websites/website-creation/the-best-static-site-generators/)

---

## 四、设计最佳实践

### 4.1 色彩搭配

| 原则 | 说明 |
|------|------|
| **60-30-10 法则** | 主色 60%（背景）、辅色 30%（区块/卡片）、强调色 10%（按钮/链接/CTA） |
| **品牌一致性** | 主品牌色统一用于标题、按钮、关键视觉元素；辅色用于背景/页脚；强调色仅用于需注意的元素 |
| **对比度优先** | 文字与背景对比度需满足 WCAG AA（4.5:1），浅灰文字配白底虽现代但可读性差 |
| **情绪传达** | 蓝色=信任/专业、绿色=成长/健康、橙/红=活力/行动、黑白=极简/高级 |
| **深色模式** | 2025 趋势，提供深浅主题切换；深色背景配高对比文字，避免纯黑纯白 |
| **限制色板** | 全站不超过 3-4 种主色，避免彩虹化；艺术家/插画师例外可用鲜艳色彩表达个性 |

### 4.2 排版原则

| 原则 | 建议 |
|------|------|
| **字体数量** | 全站最多 2 种字体（1 种标题 + 1 种正文），保持一致性 |
| **基准字号** | 正文 16px 起步，确保跨屏可读性 |
| **行高** | 长文正文 1.5-1.6 倍行高，提升扫描舒适度 |
| **阅读宽度** | 单栏正文 `max-width: 65-75ch`（约 720px），避免过宽导致换行疲劳 |
| **层级分明** | H1 > H2 > H3 字号梯度明显，粗体用于强调，常规/细体用于长文 |
| **字体选择** | 避免时髦但难读的字体；优先可读性高、响应式、契合品牌个性的字体 |
| **段后留白** | `margin-bottom: 1.2em` 左右，避免文字粘连 |
| **中文排版** | 中英文混排时注意字体回退栈，`font-family: "字体", -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif` |

### 4.3 响应式设计要点

| 要点 | 实践 |
|------|------|
| **移动优先** | 从最小屏幕（320px）开始设计，逐步增强到平板/桌面。Google 移动优先索引，移动体验直接影响 SEO |
| **相对单位** | 使用 `rem`/`em`/`%`/`vw`/`vh` 而非固定 `px`，让布局自适应 |
| **断点设置** | 常用断点：移动 <768px、平板 768-1024px、桌面 >1024px；用 `min-width` 媒体查询渐进增强 |
| **触摸目标** | 按钮/链接最小可点击区域 44×44px，防止误触 |
| **图片响应式** | `<img>` 加 `max-width: 100%; height: auto;`；使用 `<picture>` + `srcset` 按设备提供不同尺寸 |
| **导航适配** | 小屏自动折叠为汉堡菜单；大屏展开为水平/侧边导航 |
| **真实设备测试** | 浏览器模拟器之外，务必在真实手机/平板上测试性能与可用性 |
| **性能预算** | 移动端首屏加载 <3 秒；图片压缩、懒加载（`loading="lazy"`）、CSS/JS 压缩 |

### 4.4 2025 设计趋势

- **大胆排版与个性色彩**：大字号、富有表现力的字体、鲜艳色块
- **微交互与动效**：自定义光标、滚动动画、过渡效果（克制使用）
- **叙事化设计**：展示"你怎么工作、你相信什么"，强调情感连接与真实感
- **极简 + 留白**：白空间让视觉呼吸，聚焦关键内容
- **可持续与包容设计**：关注无障碍访问（A11y）、环保设计、真实而非过度打磨

> 参考来源：[Web Design Best Practices 2026](https://wbcomdesigns.com/web-design-best-practices-every-site-must-follow/)、[10 Essential Website Design Best Practices 2025](https://www.superhub.biz/10-essential-website-design-best-practices-for-2025)、[How to Design a Website 2025](https://elementor.com/blog/how-to-design-a-website/)

---

## 五、内容组织建议

### 5.1 个人简介撰写技巧

#### 核心公式：身份 + 价值 + 证明 + 个性

| 要素 | 说明 | 示例 |
|------|------|------|
| **身份（Who）** | 不止姓名职位，要表明你为谁解决什么问题 | 弱："我是一个设计师" → 强："我帮助初创公司通过视觉故事建立难忘第一印象" |
| **价值主张（What）** | 你解决什么问题、创造什么价值 | "我把复杂数据转化为 FinTech 团队可执行的洞察" |
| **证明（Why trust）** | 经验、成果、客户、认证 | "10 年经验，服务过 50+ 客户，项目平均提升转化率 30%" |
| **个性（Voice）** | 注入个人色彩，避免模板化套话 | "白天是严谨的数据分析师，晚上是狂热的桌游设计师" |

#### 叙事弧线（Context → Challenge → Action → Impact）

1. **背景**：你做什么、为谁做
2. **挑战**：你遇到了什么问题
3. **行动**：你采取了什么做法
4. **影响**：可量化的成果

#### 撰写清单

- [ ] 首屏一句话价值主张（3 秒内传达你是谁、做什么）
- [ ] 简介核心 1-3 句在首屏可见，详情链接到"关于"页
- [ ] 自然融入专业关键词，利于 SEO 与访客理解
- [ ] 加入一张真实照片，提升可信度与人情味
- [ ] 多版本适配：网站"客厅版"（详细）、LinkedIn"正装版"（专业）、社交"聚会版"（简短）
- [ ] 展示 E-E-A-T 信号：经验、专业、权威、可信（Google 重视）

### 5.2 作品集呈现方式

#### 核心原则：质量 > 数量

- 展示 **3-5 个最佳项目**，而非堆砌全部作品。招聘者平均只花 6 秒浏览作品集。
- 每个项目都能代表你的最高水平，宁缺毋滥。

#### 项目卡片要素

| 要素 | 说明 |
|------|------|
| **高质量视觉** | 截图/动图/视频，首图决定是否点击 |
| **项目名称** | 简洁有力 |
| **你的角色** | 明确你在项目中的核心贡献 |
| **关键成果** | 量化数据（如"提升转化率 40%"、"节省每周 10 小时"） |
| **技术栈/工具** | 用到的技能标签 |
| **链接** | 在线 Demo + 源码（GitHub） |
| **案例研究** | 点击进入详情页，讲述问题→方案→过程→成果的完整故事 |

#### 呈现布局

- **网格卡片**：最常见，3 列（桌面）/1 列（移动），每卡含图 + 标题 + 简述 + 链接
- **列表式**：适合博客型项目展示，图文左右交替
- **全屏轮播**：适合视觉作品（摄影/插画），冲击力强
- **分类筛选**：按技术/类型/年份筛选，适合项目较多的站点

#### 更新策略

- 每完成一个新项目即更新，并标注日期
- 访客会自然构建你的成长时间线
- 定期回顾，移除过时或不再代表当前水平的作品

### 5.3 个人品牌塑造方法

| 维度 | 建议 |
|------|------|
| **定位聚焦** | 选 1-2 个目标角色或核心服务（如"初级 UX 设计师"或"初创品牌识别设计"），"什么都能做"= 记不住 |
| **视觉一致** | 全站色彩、字体、头像、语气跨平台一致；社交头像与网站照片呼应 |
| **语气调性** | 与品牌个性匹配：专业严谨 / 友好热情 / 创意活泼，保持一贯 |
| **价值输出** | 通过博客/案例研究持续输出专业见解，建立领域权威 |
| **行动召唤** | 明确告诉访客下一步：查看简历 / 联系我 / 预约咨询 / 关注 GitHub |
| **多渠道矩阵** | 个人网站为"枢纽"（你真正拥有的数字资产），社交平台为"分支"，互相导流 |
| **真实性** | AI 时代，真实的人类故事与个性比完美模板更有价值，避免套话 |

> 参考来源：[How to Write an Effective About Me Page](https://careerservices.syr.edu/blog/2024/08/20/how-to-write-an-effective-about-me-page-examples-included/)、[How to Write a Personal Bio 2026](https://elementor.com/blog/how-to-write-a-personal-bio/)、[个人主页文字内容写作技巧](https://js.zx.zbj.com/baike/36455.html)、[How to Write About Your Story](https://fastcopywriting.ai/write-about-your/)

---

## 六、部署与维护方案

### 6.1 域名选择

| 项 | 建议 |
|----|------|
| **顶级域名** | 首选 `.com`（全球通用、易记）；个人站点也流行 `.me`/`.dev`/`.io`/`.xyz` |
| **域名形式** | `yourname.com` 最佳（个人品牌）；`yourname.dev` 适合开发者 |
| **费用** | 标准域名约 ¥70-140/年（$10-20），部分平台首年优惠 |
| **注册商** | Cloudflare Registrar（成本价）、Namecheap、阿里云/腾讯云（国内备案需） |
| **国内备案** | 若服务器在中国大陆需 ICP 备案；使用 GitHub Pages/Vercel/Netlify 等境外托管则无需备案 |
| **DNS** | 推荐 Cloudflare DNS（免费、快、附带 CDN 与安全防护） |

### 6.2 托管服务对比

| 平台 | 免费子域名 | 自定义域名+HTTPS | Git 部署+预览 | 免费额度 | 最佳场景 |
|------|-----------|-----------------|--------------|---------|---------|
| **GitHub Pages** | username.github.io | ✅ 自动 | 基础（无预览部署） | 无明确带宽上限但非商用 | 超简单静态站、文档、个人项目 |
| **Netlify** | site.netlify.app | ✅ 免费 SSL | ✅ 完整 Git + 预览部署 | 构建分钟/带宽有限额 | 静态站 + 表单 + 简单 Serverless |
| **Vercel** | project.vercel.app | ✅ 免费 SSL | ✅ 优秀预览，Next.js 最优 | 免费档有带宽/构建限制 | Next.js / 现代前端框架 |
| **Cloudflare Pages** | project.pages.dev | ✅ 免费 SSL | ✅ Git + 预览 | 边缘 CDN 大方，构建/Workers 有限 | 极致性能、边缘计算 |

#### 各平台特点

- **GitHub Pages**：零成本、可靠、与 Git 工作流无缝，但无构建预览、无 Serverless。最适合纯静态个人主页。
- **Netlify**：功能均衡，部署预览、内置表单、简单 Functions、易配重定向。最适合需要表单收集的个人站。
- **Vercel**：Next.js 官方平台，预览部署体验最佳，边缘函数。最适合用 Next.js/Astro 的项目。
- **Cloudflare Pages**：全球边缘 CDN 性能最强，Workers 集成。最适合追求极致加载速度。

### 6.3 SEO 优化基础

#### 技术 SEO 清单

| 项 | 做法 |
|----|------|
| **HTTPS** | 全站强制 HTTPS（免费托管平台均自动提供 Let's Encrypt 证书） |
| **Title 标签** | 每页独立、≤60 字符，核心关键词前置，如"姓名 - 前端开发者 \| 个人作品集" |
| **Meta Description** | 150-160 字符，含关键词 2-3 次，动词 + 数字增强吸引力，附 CTA |
| **语义化 HTML** | 用 `<header>/<nav>/<main>/<section>/<article>/<footer>` 替代 `<div>`，利于爬虫理解 |
| **标题层级** | 每页一个 `<h1>`，`<h2>`-`<h3>` 递进，不跳级 |
| **Canonical 标签** | 多 URL 指向同内容时用 `<link rel="canonical">` 指定权威版本，避免重复内容惩罚 |
| **XML Sitemap** | 生成 sitemap.xml 并提交到 Google Search Console / Bing Webmaster |
| **robots.txt** | 允许爬取，屏蔽不需索引的路径 |
| **URL 结构** | 短、语义化、扁平层级，如 `/projects/project-name` 而非 `/2025/articles/id=889` |
| **Open Graph** | `og:title/og:description/og:image` 控制社交分享预览 |
| **Twitter Cards** | `twitter:card` 等标签优化 Twitter 分享 |
| **结构化数据** | JSON-LD 格式添加 `Person`/`WebSite`/`Article` schema，获取富结果 |
| **移动友好** | 移动优先索引，确保移动端可用性；`<meta name="viewport">` 必备 |
| **Core Web Vitals** | LCP <2.5s、INP <200ms、CLS <0.1；影响排名 |
| **图片优化** | 压缩、WebP 格式、`alt` 文本、`loading="lazy"`、描述性文件名 |
| **内链** | 相关页面互相链接，消除孤岛页面 |
| **E-E-A-T** | 简介明确展示经验/专业/权威/可信信号，附作者署名、更新日期 |

#### 推荐工具

- **Google Search Console**：索引状态、搜索表现、Core Web Vitals
- **Google Analytics 4**：流量分析
- **Lighthouse**：Chrome 内置，审计性能/SEO/无障碍
- **Rich Results Test**：验证结构化数据
- **Screaming Frog / Ahrefs Webmaster**：技术 SEO 审计

### 6.4 维护建议

- **内容更新**：每完成新项目/新文章即更新；至少每季度回顾一次
- **依赖更新**：定期更新框架与依赖（`npm update`），关注安全公告
- **备份**：Git 仓库本身即备份；内容用 Markdown 编写，可移植性强
- **监控**：配置 Search Console 邮件提醒；定期检查死链（404）
- **性能复查**：定期跑 Lighthouse，保持评分 90+

> 参考来源：[Best Free Static Website Hosting 2025](https://congero.com.au/blog/comparisons/best-free-static-website-hosting-2025-with-custom-subdomain/)、[DevPortfolio 多平台部署指南](https://blog.csdn.net/gitblog_00944/article/details/153221846)、[How to Host Your Portfolio Online for Free](https://www.resumly.ai/blog/how-to-host-your-portfolio-online-for-free)、[SEO Meta Tags Guide 2025](https://sheikhshadi.com/blogs/seo-meta-tags-and-metadata/)、[How To Optimize Website SEO Checklist](https://rankyak.com/blog/how-to-optimize-website-seo)

---

## 七、综合选型建议

> **平台决策**：本项目确定以 **GitHub** 为核心平台，采用 GitHub Pages 部署、Git 版本控制、仓库结构管理内容组织。以下建议均围绕 GitHub 工作流展开。

### GitHub 优先工作流

基于当前项目为 Hexo 博客、目标是构建个人主页、且确定使用 GitHub 生态的背景，推荐方案如下：

#### 推荐方案：Hexo + GitHub Pages（最小改动，快速上线）

| 维度 | 方案 |
|------|------|
| **技术栈** | 继续用 Hexo，新增自定义页面 + 主题定制 |
| **版本控制** | Git，仓库托管于 GitHub，分支策略管理内容与主题 |
| **部署** | GitHub Pages（`username.github.io` 仓库或 `gh-pages` 分支） |
| **自动化** | GitHub Actions 自动构建部署（push 即发布） |
| **域名** | 默认 `username.github.io`，可绑定自定义域名 `yourname.com` |
| **HTTPS** | GitHub Pages 自动提供 Let's Encrypt 证书 |
| **适用** | 在现有博客基础上增加作品集/个人介绍页，迁移成本最低 |

#### 进阶方案：Astro + GitHub Pages（性能最优，长期演进）

| 维度 | 方案 |
|------|------|
| **技术栈** | Astro（零 JS 默认，Lighthouse 满分），内容用 Markdown 管理 |
| **版本控制** | Git + GitHub，同上 |
| **部署** | GitHub Pages（通过 GitHub Actions 构建 Astro 并部署） |
| **自动化** | GitHub Actions 工作流：install → build → deploy to Pages |
| **适用** | 愿意投入重构，追求极致性能与可扩展性，仍留在 GitHub 生态 |

> 注：Astro 官方提供 `@astrojs/github-pages` 适配器，部署到 GitHub Pages 一键配置。Cloudflare Pages/Vercel 虽性能更优，但若坚持 GitHub 优先，GitHub Pages 完全够用且零额外账号。

### GitHub 仓库结构建议

个人主页项目推荐如下仓库组织方式：

```
yourname.github.io/          # 仓库名（启用 GitHub Pages 的用户站点）
├── source/                  # 源内容（Hexo: source/_posts 等）
├── themes/                  # 主题文件
├── public/                  # 构建产物（.gitignore 忽略，由 CI 生成）
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions 自动部署工作流
├── _config.yml              # Hexo 配置
├── package.json
└── README.md
```

- **用户站点**：仓库名为 `<username>.github.io`，访问地址 `https://<username>.github.io`
- **项目站点**：任意仓库名，访问地址 `https://<username>.github.io/<repo>`
- **分支策略**：`main` 存源码，`gh-pages` 存构建产物（或用 Actions 直接部署）

### GitHub Actions 自动部署示例

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install
      - run: npm run build        # Hexo: hexo generate / Astro: astro build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./public          # 或 ./dist（Astro）
      - id: deployment
        uses: actions/deploy-pages@v4
```

### 自定义域名配置（可选）

1. 域名注册商处添加 CNAME 记录指向 `yourname.github.io`
2. 仓库 Settings → Pages → Custom domain 填入 `yourname.com`
3. 勾选 Enforce HTTPS（GitHub 自动签发证书）
4. 仓库根目录添加 `CNAME` 文件，内容为自定义域名

### 通用建议

1. **内容先行**：无论选哪种技术方案，先写好个人简介、整理 3-5 个代表作
2. **移动优先**：设计从 320px 开始，确保移动端体验
3. **首屏至上**：3 秒内传达"我是谁、做什么、能提供什么"
4. **Git 习惯**：小步提交、清晰 commit message、用分支管理大改动
5. **持续更新**：个人主页是活资产，push 即更新，定期回顾作品与内容
6. **数据自有**：GitHub 仓库是你真正拥有的数字资产，社交平台算法随时变

---

*文档生成时间：2026-07-02 | 基于公开网络资料整理，供个人主页项目构建参考。*
