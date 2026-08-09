---
name: e2e-testing
version: v1.0.0
description: 【端到端测试专家】当用户编写 Playwright 等 E2E 用例、验证用户业务流程、搭建 E2E 回归集时启用。请勿用于单元/集成级别的细节验证。
allowed-tools: []
---

# 端到端测试 (E2E)

从**用户视角**验证完整业务流程：打开页面 → 操作 → 提交 → 结果，走通前端 + 后端 + 数据库整条链路。典型工具：Playwright。

## 执行指令

1. **梳理核心用户路径** — 挑出高价值业务流程（登录、下单、提交、导出）
2. **搭建 E2E 环境** — 测试环境、测试账号、可重置的数据状态
3. **编写场景用例** — 以用户操作描述，绑定稳定选择器（data-testid 优先）
4. **执行测试** — 运行浏览器自动化，截图/录屏留证
5. **分析失败** — 区分真实 Bug / 用例脆弱 / 环境问题
6. **固化回归集** — 核心路径纳入 CI，非核心放低频

## 使用示例

### 用户输入
"写登录 → 进入项目 → 新增记录的 E2E 用例"

### 预期输出
```ts
test('用户登录并新增一条考勤记录', async ({ page }) => {
  await page.goto('/login');
  await page.getByTestId('username').fill('admin');
  await page.getByTestId('password').fill('****');
  await page.getByRole('button', { name: '登录' }).click();
  await page.getByTestId('project-item').first().click();
  await page.getByTestId('attendance-add').click();
  await expect(page.getByText('新增成功')).toBeVisible();
});
```

## 故障处理

| 场景 | 应对 |
|------|------|
| 用例偶发失败 | 优先用 data-testid 定位，检查异步等待是否充分 |
| UI 文案变更挂用例 | 选择器脱离文案，断言归到数据属性 |
| 环境数据不可重置 | 提供种子/重置脚本，每个用例独立数据 |

## 做什么不做什么

### ✅ 做什么
- 验证核心业务流程端到端可用
- 回归关键用户路径，防发布事故
- 跨端验证（Web 浏览器 / 桌面应用）
- 用数据属性选择器定位元素（抗 UI 改动）

### ❌ 不做什么
- 覆盖所有细节（细节回归交给单测/集成测试）
- 用文案/位置选择器导致用例脆弱
- 跑全量 E2E 作为每次提交门禁（太慢）
- 依赖固定数据而无法重置运行环境
