# 如何编写高效的 Agent Skill

> 基于物资安全管控模块（24 API、8 表、3000+ 行代码）的实战经验
> 核心问题：Agent 拿到设计 spec 后，如何不跑偏、一次编译通过？

---

## 一、Skill 的本质

**不是告诉 Agent "做什么"，而是告诉它 "照着谁做"**。

```
❌ 错误写法：
  "创建一个物资安全管控模块，包含 8 张表、24 个 API"

✅ 正确写法：
  "以 SafetyTechManagement.API 为范本
   照着这 14 个具体文件写
   按详细设计 spec §3~§6
   禁止做的事：7 条
   必须改的文件：4 个
   不要自行发挥"
```

Agent 的核心能力是**模式匹配 + 模仿**。Skill 的唯一工作：**帮 Agent 找到正确的模仿对象**。

---

## 二、Skill 必须包含的 6 个部分

### 第 1 部分：项目铁律（一次性写，全模块复用）

```markdown
## 项目铁律（违反 → 编译失败 / CR 打回）
1. ApiResult<T> 统一响应，HTTP 200，Code=0 成功
2. 错误码复用 ErrorCode，禁止新增
3. 仅 GET/POST，RPC 风格，PascalCase 方法名
4. 所有实体带 long ProjectId，仓储继承 DirectKeyRepositoryBase<T, AppDbContext>
5. 每模块 1 个 Service，内部 #region 分子域
6. 无 EF Migration，DDL 追加 upgrade.sql
7. 禁止 is_deleted，用归档表
8. FK 与 DDL 同名（HasConstraintName）
9. 枚举序列化规则见 AccessCore/Shared/Json.cs:34
10. FilterQL 用于模糊搜索（CONTAINS），query 参数用于精确筛选
11. lock 内不能 await（C# 编译器限制）
```

**写一次，后面所有模块直接引用，不重复。**

### 第 2 部分：照着谁写 — 范本文件精确路径

```markdown
## 每个你要创建的文件 → 对应的范本

| 你要创建 | 照着这个写 |
|---------|-----------|
| Module.cs | SafetyTechManagement.API/SafetyTechManagementModule.cs |
| Program.cs | SafetyTechManagement.API/Program.cs |
| Controller | SafetyTechManagement.API/Controllers/HazardousProjectController.cs |
| Service | SafetyTechManagement.API/Business/Services/SafetyTechManagementService.cs |
| Repository | SafetyTechManagement.API/Repository/HazardousProjectRepository.cs |
| IDbInfrastructure | SafetyTechManagement.API/Repository/IDbInfrastructure.cs |
| Entity | DataCenter.DAL.Core/SafetyTechManagement/Entities/HazardousProjectEntity.cs |
| CurrentUserContext | SafetyTechManagement.API/Business/Services/CurrentUserContext.cs |
| ExcelExportService | SafetyTechManagement.API/Business/Services/ExcelExportService.cs |
| .csproj | SafetyTechManagement.API/SafetyTechManagement.API.csproj |
| appsettings.json | SafetyTechManagement.API/appsettings.json |
```

**不要只描述模式，直接给路径。让 Agent 自己读。**

### 第 3 部分：必须修改的现有文件（最容易漏）

```markdown
## 需要修改的现有文件（忘了就编译失败）

| 文件 | 修改内容 | 位置 |
|------|---------|------|
| AppDbContext.cs | 添加 8 个 DbSet | SafetyTechManagement 的 DbSet 后面 |
| AppDbContext.cs | 添加 OnModelCreating 配置 | SafetyTechManagement 配置后面 |
| HostAPP.csproj | 添加 ProjectReference | SafetyTechManagement 引用的下一行 |
| ModulesLoader.cs | using + _modules 列表 | SafetyTechManagementModule 后面 |
| upgrade.sql | 追加 8 表 DDL | 文件末尾 |
| szxa-next-webapi.sln | dotnet sln add | 命令行操作 |
```

**这是最容易漏的 6 处——显式列出来。**

### 第 4 部分：必须读的基础设施文件

```markdown
## 不需要创建，但必须知道它们怎么工作

| 类 | 位置 | 知道什么就够了 |
|----|------|--------------|
| Json.cs | AccessCore/Shared/Json.cs | 枚举是 camelCase 字符串，不是数字 |
| PagedQuery.cs | FrontQL/Extensions/PagedQuery.cs | allowNoPaging 参数含义 |
| Module 基类 | SZXA.WebAPI.Shared | ConfigureServices 已经做了什么 |
| DirectKeyRepositoryBase | DataCenter.DAL.Core.Abstractions | 3 个抽象方法怎么写 |
| DataFilterContext | DataCenter.DAL.Core.Abstractions | ProjectId + Timezone 怎么取 |
```

### 第 5 部分：设计 spec 到代码的映射（让 Agent 知道哪里找什么）

```markdown
## 设计 spec 章节 → 代码文件映射

| spec 章节 | 产出代码 |
|----------|---------|
| §3.2 表结构 | Entity 字段定义 |
| §3.4 DDL | upgrade.sql 追加内容（直接复制） |
| §4.1 枚举 | MaterialSafetyEnums.cs |
| §4.2 实体类 | 8 个 Entity 文件（直接复制代码块） |
| §4.3 AppDbContext | DbSet + OnModelCreating |
| §5.2~5.6 每个接口 | Controller 方法签名 + ViewModels + Service 方法 |
| §6 业务流程 | Service 方法内部实现逻辑 |
```

**关键：告诉 Agent spec 里大部分代码块可以直接用，不用重新设计。**

### 第 6 部分：禁止事项 & 常见错误

```markdown
## 不要做的事（踩过的坑）

1. ❌ 不要自行设计筛选方式 → 严格按 spec §5 的 query 参数/FilterQL 分工
2. ❌ 不要新增 ErrorCode → 复用 InvalidArguments(1000)/DuplicateData(1002)/NotFound(404)
3. ❌ 不要在 Service 直接注入 AppDbContext → 用 IDbInfrastructure + Npgsql 原生 SQL
4. ❌ 不要用 EF ExecuteUpdateAsync 做原子扣减 → 用 Npgsql 原生 UPDATE WHERE
5. ❌ 不要只加 ModulesLoader 忘了 csproj → 两个都要改
6. ❌ 不要只加 csproj 忘了 sln → dotnet sln add
7. ❌ JSON 归档表的 Id 不要用 IdGen.NewId() → 用原流水 ID
```

---

## 三、Skill 模板

```markdown
## 任务：创建 {模块名} 模块后端代码

### 权威来源
- 设计 spec：{路径}

### 项目铁律（引用外部文件，不重复）
{引用铁律清单}

### 照着这些文件写
{范本文件表}

### 必须修改的现有文件
{6 处修改清单}

### 执行顺序
1. 先读设计 spec §3~§6
2. 创建枚举 → 实体 → DDL
3. 修改 AppDbContext → upgrade.sql
4. 创建 ViewModels
5. 创建 Repository
6. 创建 Service → Controller
7. 创建 Module → Program → csproj
8. 修改 HostAPP.csproj → ModulesLoader → sln

### 验证
- dotnet build {Module}.API 0 错误
- 检查 6 个必须修改的现有文件都已改
```

---

## 四、本次实战的 7 个 bug 及如何通过 Skill 预防

| 问题 | 根因 | Skill 中如何预防 |
|------|------|----------------|
| FilterQL 替代 query 参数 | Agent 自行发挥 | 铁律 10 + 设计 spec 映射表 |
| `SortDirection` 找不到 | 少 `using FrontQL;` | 范本文件表（看 Service 的 using） |
| HostAPP 找不到模块 | 漏 csproj 引用 | 第 3 部分：必须修改的现有文件 |
| `lock` 内 `await` 编译错误 | C# 知识盲区 | 铁律 11 |
| DDL 没追加 | Agent 没意识到 DDL 是产出 | 第 5 部分：spec 章节→代码映射 |
| DTO 类型 doc 写 `number` | 不知道全局枚举序列化规则 | 第 4 部分：读 Json.cs |
| `allowNoPaging: false` 导致接口报错 | 不理解参数含义 | 第 4 部分：读 PagedQuery.cs |

---

## 五、Skill 质量自检清单

写完一个 Skill 后，逐项核对：

```
□ 铁律清单是否完整（11 条）
□ 范本文件表是否精确到文件路径
□ 必须修改的现有文件是否列出全部 6 处
□ 设计 spec → 代码的映射表是否有
□ 禁止事项是否列了容易犯的错
□ 执行顺序是否明确（先建什么后改什么）
□ 验证命令是否给出（dotnet build 哪个项目）
□ 是否有"不要自行发挥"的明确警告
```

---

## 六、Skill 复用策略

```
skill/backend-module-base.md      ← 铁律 11 条（所有后端模块 skill 引用）
skill/backend-module-模板.md       ← 上面的完整模板（新模块改模块名即可）
skill/backend-module-MaterialSafety.md ← 具体模块 skill（引用模板 + 设计 spec 路径）
```

**不要每次重新写铁律和范本路径。建一个基础 Skill，新模块只写差异部分。**
