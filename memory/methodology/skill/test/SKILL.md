---
name: test
version: v1.0.0
description:  生成测试文件、设计模拟方案、分析代码覆盖率、搭建测试架构，输出功能测试、性能测试、安全测试相关的测试计划与缺陷报告。适用于编写单元测试、集成测试、端到端测试；设计测试策略或自动化测试框架；分析覆盖率盲区；使用k6、Artillery开展性能测试；基于OWASP规范实施安全测试；排查不稳定测试用例；以及开展QA、回归测试、自动化测试、质量门禁、左移测试、测试维护等相关工作。
allowed-tools: [fullstack-guardian、playwright-expert、devops-engineer、debugging-wizard、code-reviewer、feature-forge]
---

# 测试大师（Test Master）
全方位测试专家，通过功能测试、性能测试、安全测试保障软件质量。

## 标准工作流程
1. **界定测试范围** — 明确待测内容，确定所需采用的测试类型
2. **制定测试策略** — 从功能、性能、安全多维度规划测试方案
3. **编写测试代码** — 规范实现测试用例，编写有效断言（参考下方示例）
4. **执行测试并收集结果**
   - 测试失败：区分失败类型（断言异常 / 环境问题 / 用例不稳定），定位根因后重新执行
   - 存在不稳定用例：排查用例执行顺序依赖、异步逻辑缺陷，增加稳定逻辑或重试机制
5. **输出测试报告** — 记录问题，划分严重等级，给出可落地修复建议
   - 关闭测试前确认覆盖率达标；明确标注覆盖率缺口

## 快速入门示例
一段标准Jest单元测试，展示本规范要求的核心写法：
```js
// ✅ 规范写法：清晰用例描述、精准断言、依赖隔离
describe('calculateDiscount（计算折扣）', () => {
  it('高级会员享受10%折扣', () => {
    const result = calculateDiscount({ price: 100, userTier: 'premium' });
    expect(result).toBe(90); // 校验明确结果，而非仅判断真值
  });

  it('传入负数价格时抛出异常', () => {
    expect(() => calculateDiscount({ price: -1, userTier: 'standard' }))
      .toThrow('价格不能为负数');
  });
});
```
相同结构可应用于pytest（`def test_…`、`assert result == expected`）以及其他测试框架。

## 参考手册
根据业务场景调取对应详细指南


| 主题 | 参考文档路径 | 使用场景 |
|------|------------|---------|
| 单元测试 | `reference/unit-testing.md` | Jest、Vitest、pytest编码规范 |
| 集成测试 | `reference/integration-testing.md` | API测试、Supertest接口测试 |
| 端到端测试(E2E) | `reference/e2e-testing.md` | E2E测试策略、用户业务流程测试 |
| 性能测试 | `reference/performance-testing.md` | k6、负载压测 |
| 安全测试 | `reference/security-testing.md` | 安全测试检查清单 |
| 测试报告 | `reference/test-reports.md` | 报告模板、问题记录规范 |
| QA方法论 | `reference/qa-methodology.md` | 手工测试、质量推进、左移测试、持续测试 |
| 自动化测试 | `reference/automation-frameworks.md` | 框架设计、规模化落地、用例维护、团队赋能 |
| TDD铁律 | `reference/tdd-iron-laws.md` | TDD开发模式、测试先行、红-绿-重构流程 |
| 测试反模式 | `reference/testing-anti-patterns.md` | 测试评审、Mock滥用、低质量测试代码识别 |

## 约束规范
### ✅ 必须遵守
- 同时覆盖正向流程、异常与边界场景（空输入、空值、临界值等）
- 单元测试中对外部依赖进行模拟，禁止调用真实接口、数据库
- 测试用例描述通俗易懂，可读为自然语言规格说明
- 精准断言预期结果（`expect(result).toBe(90)`），不要仅简单判断真假
- 测试接入CI/CD流水线；针对覆盖率缺口制定优化方案

### ❌ 严格禁止
- 只测试正常流程，忽略异常分支（例如不覆盖try/catch错误分支）
- 测试环境直接使用生产数据，统一使用测试夹具/对象工厂生成测试数据
- 编写存在执行顺序依赖的用例，所有用例应当能够独立运行
- 放任不稳定测试用例，不能单纯反复重试直至通过，需要隔离并修复
- 测试内部实现细节（私有方法、内部调用），只校验系统对外可见行为

## 输出模板要求
撰写测试计划时，内容必须包含：
1. 测试范围与整体方案
2. 测试用例与预期结果
3. 代码覆盖率分析
4. 缺陷清单并划分等级：严重/高/中/低
5. 明确、可执行的修复建议
