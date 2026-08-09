# VS Code 单模块调试配置流程

## 背景

SZxA 后端 (`szxa-next-webapi/`) 是 .NET 8 模块化单体架构。HostAPP 启动全部模块会因 MassTransit SQL Transport 权限、RabbitMQ 等问题崩溃，因此本地调试需要只启动单个 API 模块。

## 完整流程

### 1. 创建 launch.json 调试配置

用 VS Code 打开 `szxa-next-webapi/` 文件夹（不是上级目录），在 `.vscode/launch.json` 中添加：

```json
{
    "name": "Launch: AttendanceManagement.API (单模块)",
    "type": "coreclr",
    "request": "launch",
    "preLaunchTask": "build-AttendanceManagement",
    "program": "${workspaceFolder}/AttendanceManagement.API/bin/Debug/net8.0/AttendanceManagement.API.dll",
    "args": ["--urls", "http://localhost:5050"],
    "cwd": "${workspaceFolder}/AttendanceManagement.API",
    "stopAtEntry": false,
    "env": {
        "ASPNETCORE_ENVIRONMENT": "Development"
    },
    "console": "integratedTerminal",
    "justMyCode": false
}
```

**关键点**：
- `program` 指向编译后的 DLL，不能用 `dotnet run`（调试器 attach 不上子进程）
- `cwd` 设为模块目录（`appsettings.json` 所在位置）
- `justMyCode: false` 允许进入框架/共享库源码调试

### 2. 创建单模块 build task

整个 solution 编译可能因无关模块的编译错误失败。在 `.vscode/tasks.json` 中创建针对性 task：

```json
{
    "label": "build-AttendanceManagement",
    "command": "dotnet",
    "type": "process",
    "args": [
        "build",
        "${workspaceFolder}/AttendanceManagement.API/AttendanceManagement.API.csproj"
    ],
    "problemMatcher": "$msCompile"
}
```

调试其他模块时仿照创建对应的 task 和 launch config，改模块路径和端口即可。

### 3. 创建模块的 appsettings.json

模块目录下默认没有 `appsettings.json`（配置在 HostAPP/ 里），需手动创建。

**必须包含 `FileStorage` 节**，否则 DI 容器初始化失败（见下方排错记录第3条）。

```json
{
  "Logging": { "LogLevel": { "Default": "Information" } },
  "ConnectionStrings": {
    "PostgreSQL": "Host={host};Port={port};Database={db};Username=aqm_db_user;Password=SzXa#aqm@13579!;Pooling=true;ConnectionLifetime=0;Tcp Keepalive=true;"
  },
  "Usm3Auth": {
    "TokenEndpoint": "https://zndt.msdi.cn/oauth2/token",
    "SysId": "eddd95a3-5d79-4d48-a43f-755c27aa398a",
    "TenantId": "C36BE9E3-61E6-9548-6349-5464BC5BEAF5",
    "Authorization": "Basic c3dvcmQ6c3dvcmRfc2VjcmV0"
  },
  "ExceptionWebhook": { "Enabled": false },
  "FileStorage": {
    "Provider": "Local",
    "Local": { "RootPath": "./uploads" }
  }
}
```

### 4. 模块代码：注册 FileStorage 服务

在模块的 `*Module.cs` 中调用 `AddFileStorage()`。HostAPP 在 `ModulesLoader` 里统一注册，单模块跑需各自补上：

```csharp
using static SZXA.WebAPI.Shared.FileStorage.Extensions.FileStorageServiceExtensions;

public override void ConfigureServices(WebApplicationBuilder builder) {
    base.ConfigureServices(builder);
    builder.Services.AddFileStorage(builder.Configuration);  // 单模块独立运行需要
    // ... 其他服务注册
}
```

### 5. 数据库连接

| 环境 | Host | Port | Database |
|------|------|------|----------|
| Prod | 10.226.6.40 | 8086 | aqm_db |
| Test | 10.226.6.48 | 8086 | aqm_db_test |

### 6. 端口占用处理

```bash
lsof -ti:5050 | xargs kill -9 2>/dev/null
```

### 7. 调用接口验证

```bash
curl --noproxy '*' -s -X POST \
  "http://localhost:5050/api/AttendanceRecord/List" \
  -H "token: <token>" \
  -H "ProjectId: <projectId>" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

- `--noproxy '*'` 必须加，否则走本地代理 127.0.0.1:7897 → 502
- `token` header 不是 `Authorization: Bearer`
- `ProjectId` header 必传

---

## 排错记录

### 问题1：`dotnet run` 断点不生效

**现象**：F5 启动成功但断点永远不命中。

**根因**：`"program": "dotnet"` + `"args": ["run", ...]` → 调试器 attach 到 `dotnet` 父进程，`dotnet run` 会 fork 子进程跑实际应用，子进程不在调试器管控范围内。

**修复**：改为直接启动编译好的 DLL（`"program": "...bin/Debug/net8.0/AttendanceManagement.API.dll"`），coreclr 调试器能正确托管整个进程。

---

### 问题2：`preLaunchTask: build` 编译失败

**现象**：4 个 `CS0121` 错误：`string.Split` 调用具有二义性。

**根因**：`tasks.json` 中的 `build` task 编译整个 `szxa-next-webapi.sln`。`DatacenterAPP/Datacenter/SmartPreShiftMeeting/Extractor/MeetingParticipantRecordsExtractor.cs` 中有 `string.Split` 调用在 .NET 8 下 ambiguous（`Split(char[]?, StringSplitOptions)` vs `Split(string?, StringSplitOptions)`），这是代码本身的问题，和 Attendance 模块无关。

**修复**：创建仅编译目标模块的 task `build-AttendanceManagement`，不改动 DatacenterAPP 的代码。

---

### 问题3：CLR/System.AggregateException — `IStorageProvider` 无法解析

**现象**：
```
System.AggregateException: 'Some services are not able to be constructed'
  inner: Unable to resolve service for type 'IStorageProvider'
         while attempting to activate 'FileService'.
```

**根因链**：
1. `FileService` 有 `[Service(ServiceScope.Scoped)]` 属性
2. `ServiceFactory.RegisterService()` 自动扫描带 `[Service]` 的类并注册到 DI 容器
3. `FileService` 的构造函数依赖 `IStorageProvider`
4. `IStorageProvider` 通过 `FileStorageServiceExtensions.AddFileStorage()` 注册，不走 `[Service]` 扫描
5. HostAPP 的 `ModulesLoader.ConfigureServices()` 调用了 `AddFileStorage()`
6. 基类 `Module.ConfigureServices()` **没有**调用 `AddFileStorage()`
7. 单模块运行时只有基类逻辑，`IStorageProvider` 从未注册

**修复**：
- `appsettings.json` 添加 `FileStorage` 配置节（默认 Local provider，`./uploads` 目录）
- 模块 `ConfigureServices()` 中加一行 `builder.Services.AddFileStorage(builder.Configuration)`

**关键架构知识点**：
- `[Service]` 属性标注的类会被 `ServiceFactory.RegisterService()` 自动扫描注册（包括其首个非 System 接口）
- 部分基础设施服务（如 `IStorageProvider`）不走 `[Service]` 扫描，需通过扩展方法手动注册
- `FileStorageOptions` 所有属性都有默认值，`Provider` 默认 `"Local"`，`RootPath` 默认 `"./uploads"`
- 基类 `Module.ConfigureServices()` 提供通用基础设施（DB 上下文、AccessCore、异常处理等），但不包含 `AddFileStorage()`

---

## 调试其他模块的 checklist

换模块调试时，保证以下 4 项：

1. `.vscode/tasks.json` — 新建 `build-{ModuleName}` task
2. `.vscode/launch.json` — 复制单模块配置，改模块路径、端口、task 名
3. `{Module}.API/appsettings.json` — 含 DB、Usm3Auth、FileStorage 三个节
4. `{Module}Module.cs` — `ConfigureServices()` 中调了 `builder.Services.AddFileStorage(builder.Configuration)`
