# Agent 提示信息清单 — 保证详细设计→编码不跑偏

> 基于物资安全管控模块的实战经验，总结 Agent 需要哪些信息才能正确产出代码

---

## 一、两类信息：技术基础设施 + 项目约定

```
Agent 拿到一个详细设计 spec，要写出能编译通过的代码
需要两类信息：

┌── 技术信息（通用，每个项目差不多）
│   ├── 框架版本（.NET 8 / EF Core 8 / PostgreSQL 12）
│   ├── 包依赖（Npgsql / xUnit / Moq / NodaTime）
│   └── 语言特性（C# 12 / nullable enable）
│
└── 项目信息（特定于 szxa-next-webapi，必须从现有代码学）
    ├── 分层结构（Module → Controller → Service → Repository → Entity）
    ├── 命名空间约定
    ├── 代码模式（[ScopedService]、DirectKeyRepositoryBase）
    ├── 需要修改的现有文件（AppDbContext、ModulesLoader、HostAPP.csproj）
    └── 禁止事项（不新增 ErrorCode、不用 EF Migration、不用 is_deleted）
```

---

## 二、本次物资安全管控实际参考的文件清单

### 设计文档（业务逻辑的来源）

| 文件 | 提供了什么 | Agent 用在哪 |
|------|----------|------------|
| `doc/feature-物资安全管控/final/详细设计spec.md` | 8 表 DDL、8 Entity 定义、24 API 签名、DTO 字段、业务流程、ADR | **全部编码的核心来源** |
| `doc/feature-物资安全管控/final/需求spec.md` | FR 编号、验收标准 | 理解业务意图，不直接编码 |
| `doc/feature-物资安全管控/final/产品验收spec.md` | AT 场景 | 测试用例设计 |

### 项目规范文件（什么是能做 / 不能做的）

| 文件 | 提供了什么 | Agent 用在哪 |
|------|----------|------------|
| `规范/架构约束.md` | C-001~C-012 约束表 | 检查自己的代码是否违规 |
| `规范/数据库建模规范.md` | snake_case、3NF、FK 强制、COMMENT 必须 | DDL 和 Entity 设计 |
| `规范/集成测试规范.md` | Testcontainers、Trait、断言规范 | 测试文件结构 |
| `CLAUDE.md` | Agent 清单、过程路由 | Orchestrator 派发 Agent |

### 现有代码（模式从哪里抄）

| 文件 | 提供了什么 | Agent 用在哪 |
|------|----------|------------|
| `SafetyTechManagement.API/SafetyTechManagementModule.cs` | Module 注册模式 | MaterialSafetyModule.cs |
| `SafetyTechManagement.API/Program.cs` | `ModuleRunner.Run(...)` | Program.cs |
| `SafetyTechManagement.API/Repository/HazardousProjectRepository.cs` | 仓储三抽象方法 | 8 个仓储实现 |
| `SafetyTechManagement.API/Repository/IDbInfrastructure.cs` | 事务 + 连接字符串接口 | 复制到本模块 |
| `SafetyTechManagement.API/Business/Services/SafetyTechManagementService.cs` | Service 注入、#region 分子域、PagingFetch | MaterialSafetyService.cs |
| `SafetyTechManagement.API/Business/Services/CurrentUserContext.cs` | 用户上下文 | 复制到本模块 |
| `SafetyTechManagement.API/Controllers/HazardousProjectController.cs` | Controller 模式、Route、[ApiPermission] | 5 个 Controller |
| `DataCenter.DAL.Core/Shared/AppDbContext.cs` | DbSet 注册、OnModelCreating 风格 | 添加 8 个 DbSet + 配置 |
| `DataCenter.DAL.Core/SafetyTechManagement/Entities/HazardousProjectEntity.cs` | Entity 格式 | 8 个 Entity |
| `HostAPP/HostAPP.csproj` | 项目引用格式 | 添加 MaterialSafety.API 引用 |
| `HostAPP/ModulesLoader.cs` | 模块注册格式 | 添加 MaterialSafetyModule |
| `AccessCore/Shared/Json.cs` | `JsonStringEnumConverter(CamelCase)` | 理解枚举序列化规则 |
| `FrontQL/Extensions/PagedQuery.cs` | PagingFetch 参数 | allowNoPaging 等参数用法 |

### 基础设施类（不需要读源码，但需要知道存在）

| 类/接口 | 位置 | 用途 |
|---------|------|------|
| `Module` 基类 | `SZXA.WebAPI.Shared.ModularMonolith` | 继承后 override `ConfigureServices` |
| `ModuleRunner` | `SZXA.WebAPI.Shared.ModularMonolith` | `Program.cs` 唯一调用 |
| `DirectKeyRepositoryBase<T,TDbContext>` | `DataCenter.DAL.Core.Abstractions` | 仓储继承 + 3 抽象方法 |
| `ApiResult<T>` / `ApiResult` | `DataCenter.DAL.Core.Shared.Models` | 所有 Controller 返回类型 |
| `ErrorCode` 枚举 | `DataCenter.DAL.Core.Shared.Enums` | 只能复用，不能新增 |
| `IdGen.NewId()` | `Utility.IdGen` | Entity 主键默认值 |
| `[ScopedService]` | `SZXA.WebAPI.Shared.Attributes` | DI 自动注册 |
| `PagingFetchRequestOption` | `FrontQL.Models` | List 接口请求体 |
| `PagingFetch()` | `FrontQL.Extensions` | IQueryable 分页扩展 |
| `IDataFilterContextAccessor` | `DataCenter.DAL.Core.Abstractions` | 取 `ProjectId` + `Timezone` |

---

## 三、Agent prompt 模板

### 技术信息（必须注入的部分）

```markdown
## 技术栈
- 后端：.NET 8 + EF Core 8 + PostgreSQL 12
- 语言：C# 12，ImplicitUsings enable，Nullable enable
- 测试：xUnit + Moq + FluentAssertions + Testcontainers
- 包：Npgsql（原生 SQL）、NodaTime（时区）、ClosedXML（Excel）

## 必须遵守的全局约束
1. 所有 API 返回 `ApiResult<T>`，HTTP 200，Code=0 成功
2. 错误码复用 `ErrorCode` 枚举，禁止新增
3. 仅 GET/POST，RPC 风格，PascalCase 方法名
4. 所有业务实体自带 `long ProjectId`
5. 每模块 1 个 Service，`#region` 分子域
6. 无 EF Migration，DDL 追加 `upgrade.sql`
7. 禁止 `is_deleted`，用归档表
8. FK 与 DDL 同名（`HasConstraintName`）
9. 枚举序列化为 camelCase（全局 `JsonStringEnumConverter(CamelCase)`）
10. FilterQL 用于模糊搜索，query 参数用于精确筛选
```

### 项目信息（必须让 Agent 读的文件列表）

```markdown
## 必须读取的参考文件（按顺序）

### 1. 设计文档
- {详细设计spec路径} — 全部代码的权威来源

### 2. 范本模块（照着抄模式）
- SafetyTechManagement.API/SafetyTechManagementModule.cs
- SafetyTechManagement.API/Program.cs
- SafetyTechManagement.API/Controllers/HazardousProjectController.cs
- SafetyTechManagement.API/Business/Services/SafetyTechManagementService.cs（前 200 行看注入模式）
- SafetyTechManagement.API/Repository/HazardousProjectRepository.cs
- SafetyTechManagement.API/Repository/IDbInfrastructure.cs
- DataCenter.DAL.Core/SafetyTechManagement/Entities/HazardousProjectEntity.cs

### 3. 需要修改的现有文件（必须找到准确位置再插入）
- DataCenter.DAL.Core/Shared/AppDbContext.cs
- HostAPP/HostAPP.csproj
- HostAPP/ModulesLoader.cs
- DataCenter.DAL.Core/scripts/upgrade.sql

### 4. 约束参考
- AccessCore/Shared/Json.cs（枚举序列化规则）
- FrontQL/Extensions/PagedQuery.cs（PagingFetch 参数含义）
```

---

## 四、本次碰到的问题 & 根因

| 问题 | 根因 | Agent 缺少什么信息 |
|------|------|------------------|
| FilterQL vs query 参数混用 | 擅自修改 spec 规定的参数位置 | 没有强调"设计 spec 是唯一的权威，不要自行发挥" |
| `lock` 内 `await` 编译错误 | C# 语言规则 | 通用知识，不需要额外提示 |
| `SortDirection` 找不到 | 缺少 `using FrontQL;` | 提示 Agent 检查范本 Service 的 using 列表 |
| HostAPP 找不到 MaterialSafety | 漏加 `.csproj` 引用 | 应该提示"新模块需要改 3 处：csproj + ModulesLoader + sln" |
| DTO 类型 vs 实际序列化不一致 | 不知道全局 `JsonStringEnumConverter` 规则 | 提示读 `AccessCore/Shared/Json.cs` |
| `upgrade.sql` 追加 DDL 漏掉 | 没明确说 DDL 也是产出之一 | 提示"设计 spec §3.4 的 DDL 必须追加到 upgrade.sql" |
| 多字节字符 Edit 工具失败 | 工具本身问题 | 备用方案：Python 脚本写入 |
