---
name: szxa-api-test
version: 1.0.0
description: 独立运行 SZXA 单个API模块并连接指定数据库进行接口测试。当用户说「测试考勤接口」「运行attendance」「调一下XX接口看看返回」时启用。不可用于跑所有单元测试或启动完整HostAPP。
allowed-tools: [Bash, Read, Write, Edit]
---

# 执行指令

你是 SZXA 后端接口测试助手。任务：只启动需要的那个 API 模块，连指定数据库，调接口，看返回。

## 步骤

### 1. 确认环境

- `git branch --show-current` 确认分支
- 检查 `模块.API/appsettings.json` 是否存在、ConnectionStrings 指向哪个库

### 2. 数据库切换

| 用户说 | Host | Database |
|--------|------|----------|
| prod / 40 / 生产 | 10.226.6.40:8086 | aqm_db |
| test / 48 / 测试 | 10.226.6.48:8086 | aqm_db_test |

修改 `appsettings.json` 中 `PostgreSQL` 连接串的 Host 和 Database。

### 3. 启动

```bash
lsof -ti:5050 | xargs kill -9 2>/dev/null
dotnet run --project /Users/liuchuyao/Downloads/HARNESS/szxa-next-harness/szxa-next-webapi/模块.API/模块.API.csproj --urls "http://localhost:5050"
```

等待 `Application started`。

### 4. 调接口

**认证**: 从 `token` header 读，不是 `Authorization: Bearer`。token 和 projectId 向用户要。

```bash
curl --noproxy '*' -s -X POST \
  "http://localhost:5050/api/xxx" \
  -H "token: <token>" \
  -H "ProjectId: <projectId>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

`--noproxy '*'` 必须加。

### 5. 停服务

```bash
lsof -ti:5050 | xargs kill -9 2>/dev/null
```

## 常见问题

| 症状 | 原因 | 解决 |
|------|------|------|
| 401 | 用了 Bearer 不是 token header | 换 `-H "token: xxx"` |
| 502/无响应 | 走了代理 127.0.0.1:7897 | 加 `--noproxy '*'` |
| 启动崩溃 | 跑了 HostAPP 而非单模块 | 不要跑 HostAPP |

## 为什么跑单模块不跑 HostAPP

HostAPP 启动全部模块 → MassTransit 迁移无权限 + 视频平台健康检查外网不可达 → 进程崩溃。
