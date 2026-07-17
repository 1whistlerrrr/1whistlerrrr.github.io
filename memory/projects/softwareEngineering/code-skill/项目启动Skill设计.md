# 项目启动 Skill — 从零到详细设计

> 核心问题：假设没有任何代码，如何启动一个项目？人和 Agent 各自做什么？

---

## 一、人 vs Agent 的分工原则

```
人做：会后悔的决策       → 技术栈、架构、模块边界、业务方向
Agent 做：不会后悔的活    → 脚手架、模板、重复性工作、一致性检查
人审：Agent 做的是否符合意图
```

| 环节 | 人 | Agent | 原因 |
|------|:--:|:--:|------|
| 技术栈选型 | ✅ 决策 | ❌ | .NET vs Java 选了就不能回头 |
| 模块拆分 | ✅ 决策 | ❌ | 影响整个团队分工 |
| 数据库选型 | ✅ 决策 | ❌ | PG vs MySQL vs Mongo 换不了 |
| 脚手架搭建 | ❌ | ✅ | 纯模板，没有任何决策 |
| CI/CD 配置 | ✅ 审 | ✅ 生成 | Agent 生成，人确认 |
| 编码规范文件 | ✅ 审 | ✅ 生成 | EditorConfig、Directory.Build.props |
| 需求 spec 撰写 | ✅ 确认 | ✅ 初稿 | Agent 写初稿，人修正 |
| 详细设计 spec | ✅ 审 | ✅ 初稿 | Agent 按模板填，人调架构决策 |

---

## 二、项目启动的完整流程

### 阶段 0：人做决策（不可代理）

```
人需要明确回答以下 6 个问题：

Q1: 这个项目解决什么业务问题？（一句话）
Q2: 后端用什么语言/框架？
    → .NET 8 + EF Core + PostgreSQL
    → 还是 Java Spring + MySQL
    → 还是 Go + MongoDB
Q3: 前端用什么？
    → React + TypeScript + Mantine
    → 还是 Vue + Element Plus
    → 还是纯后端（无前端）
Q4: 单体还是微服务？
    → 单体（像 szxa-next-webapi）
    → 还是微服务（多个独立部署的服务）
Q5: 数据库用哪个？
    → PostgreSQL（当前项目）
    → 还是 MySQL / MongoDB / SQLite
Q6: 部署在哪？
    → 自建服务器 / 云服务器 / Docker / K8s
```

**这 6 个问题 Agent 不能替人回答——错了要推倒重来。**

### 阶段 1：Agent 搭建脚手架（人看完 Q1~Q6 的答案后触发）

```
Skill: project-init

输入：技术栈选择 + 项目名称
输出：
  1. 目录结构
  2. .sln 解决方案文件
  3. 基础项目文件（.csproj、Program.cs、appsettings.json）
  4. Directory.Build.props（统一版本号）
  5. .gitignore
  6. .editorconfig
  7. docker-compose.yml（数据库）
  8. CI/CD 基础流程
```

**这部分纯机械操作，Agent 可以直接生成。人只需要确认目录结构是否符合预期。**

### 阶段 2：人确认第一个模块 + Agent 搭建框架

```
人：选一个最简单的模块作为"范本模块"
    → 比如"用户登录"、"字典管理"
    → 这个模块会成为后续所有模块的模板

Agent：
  1. 创建第一个 Module（如 UserService.API）
  2. 创建 Module 基类
  3. 实现第一个完整链路：Entity → Repository → Service → Controller
  4. 跑通 swagger、集成测试
  5. 这个模块将成为后面所有模块的"照着写"范本
```

### 阶段 3：后续模块的开发（就是这次物资安全管控的模式）

```
人：
  1. 产出需求 spec + 产品验收 spec + UI/UX spec
  2. 确认后 promote 到 final/
  3. 派发 designer agent 产出详细设计 spec
  4. 确认后派发 backend-coder / frontend-coder

Agent：
  1. 读取 final/ 下的设计 spec
  2. 以阶段 2 的范本模块为参照
  3. 按设计 spec 产出代码
  4. 自检（编译、格式化）
```

---

## 三、启动 Skill 设计

### Skill 1: `project-init`（项目脚手架初始化）

```markdown
## 输入
- 项目名称：{ProjectName}
- 技术栈：.NET 8 / EF Core 8 / PostgreSQL 12
- 前端：React 19 + TypeScript + Mantine 7（可选）
- 部署：Docker / 自建服务器

## 产出清单
1. 根目录 {ProjectName}/
2. src/ 目录下的 .sln 文件
3. 共享项目：{ProjectName}.Shared（ApiResult、ErrorCode、Module 基类）
4. 数据层：{ProjectName}.DAL（AppDbContext、Entity 基类、仓储基类）
5. 第一个模块：UserService.API（作为后续模块的范本）
6. HostAPP（启动项目，加载所有模块）
7. test/ 目录（集成测试基础设施）
8. docker-compose.yml（PostgreSQL + Redis 可选）
9. .gitignore、.editorconfig、Directory.Build.props
10. CI/CD 基础 .github/workflows/ 或 Jenkinsfile

## 执行步骤
1. 创建目录结构
2. 创建 .sln
3. 创建共享项目（所有模块的依赖）
4. 创建第一个模块（范本模块）
5. 创建 HostAPP
6. 创建测试项目
7. 创建 Docker 配置
8. 创建 CI/CD 配置
9. dotnet build 验证
```

### Skill 2: `module-new`（新增业务模块）

```markdown
## 前置条件
- 已有范本模块（如 SafetyTechManagement.API）
- 已有详细设计 spec（路径）
- 项目铁律文档（路径）

## 输入
- 模块名称
- 详细设计 spec 路径（含 DDL、Entity、API、业务流程）

## 产出清单
1. {Module}.API 项目（csproj + Program.cs + Module.cs）
2. Entity（{count} 个）
3. Enum（1 个）
4. ViewModels（{count} 个 DTO 类）
5. Repository（{count} 组接口+实现）
6. Service（1 个）
7. Controller（{count} 个）
8. DDL 追加到 upgrade.sql
9. AppDbContext 修改（DbSet + OnModelCreating）
10. HostAPP.csproj 引用
11. ModulesLoader 注册
12. .sln 注册
13. 单元测试项目（可选）

## 执行顺序
1. 读设计 spec + 范本模块代码
2. 创建枚举 → 实体 → DDL
3. 改 AppDbContext + upgrade.sql
4. 创建 ViewModels
5. 创建 Repository
6. 创建 Service → Controller
7. 创建 Module → Program → csproj
8. 改 HostAPP.csproj → ModulesLoader → sln
9. dotnet build 验证
```

---

## 四、哪些问题需要人判断（Agent 不该碰）

| 决策 | 为什么是人的 | Agent 可以辅助什么 |
|------|------------|-----------------|
| **模块边界** | 影响团队分工，需要业务理解 | 根据需求 spec 给建议 |
| **数据库选型** | 换数据库成本极高 | 列出 PG vs MySQL vs Mongo 对比 |
| **单体 vs 微服务** | 组织架构决定，不是技术问题 | 列出权衡对比表 |
| **API 风格** | RESTful vs RPC vs GraphQL 影响前后端协作 | 给项目现有风格的建议 |
| **是否引入 Redis / MQ** | 加中间件 = 加运维负担 | 列出"什么时候该加"的判断标准 |
| **并发方案选型** | 乐观锁 vs 悲观锁 vs Redis 和业务场景强相关 | 列出各方案 QPS 和适用场景 |
| **索引设计** | 需要知道查询模式 | 分析 spec 中的查询语句建议索引 |
| **FK RESTRICT vs CASCADE** | 业务语义决定 | 列出每种选择的后果 |

## 五、哪些问题 Agent 可以直接做（人不该浪费时间）

| 任务 | Agent 直接做 | 人只需要 |
|------|:--:|------|
| 文件创建（Entity、DTO、Controller 等） | ✅ | 审查关键逻辑 |
| DDL 生成 | ✅ | 审查 FK 关系和索引 |
| AppDbContext 修改 | ✅ | 审查没有和现有冲突 |
| 代码格式化、using 排序 | ✅ | 不需要 |
| 根据 spec 生成单元测试用例 | ✅ | 审查覆盖范围 |
| swagger.json 验证 | ✅ | 不需要 |
| 编译验证 | ✅ | 不需要 |
| 前后端字段对齐检查 | ✅ | 确认没有遗漏 |
| .gitignore、.editorconfig | ✅ | 不需要 |
| CI/CD 模板 | ✅ | 确认脚本路径正确 |

---

## 六、从零到第一个模块跑通的时间线

```
Day 1（人）：
  回答 6 个决策问题 → 确认技术栈

Day 1-2（Agent + 人审）：
  执行 project-init → 脚手架搭建 → dotnet build 通过
  创建范本模块 → 第一个 API 跑通 → swagger 可用
  Docker PostgreSQL 启动 → 集成测试基础设施就绪

Day 3-5（人 + Agent 并行）：
  人：写第一个模块的需求 spec + 详细设计 spec
  Agent：完善 CI/CD、代码规范检查、文档模板

Day 5+（人审 + Agent 执行）：
  完成范本模块的完整实现 → 成为后续模块的"照着写"模板
  后续每个新模块：人产出 design spec → Agent 编码 → 人审查
```

---

## 七、关键原则

```
1. 第一个模块是最重要的——它决定了后面所有模块怎么写
   第一个模块必须由人仔细审查，确认模式正确

2. 铁律写一次，全项目引用——不要每次重新告诉 Agent 规则

3. Agent 的产出质量 = 范本质量 × spec 详细度
   范本好 → Agent 产出好
   spec 模糊 → Agent 自由发挥 → 跑偏

4. 人守住"不可逆决策"，Agent 做"可回滚的活"
   技术栈选错 → 重写    Agent 写的 Controller 不够好 → 删了重来
```
