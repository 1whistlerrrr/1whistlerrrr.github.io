---
name: performance-testing
version: v1.0.0
description: 【性能测试专家】当用户用 k6、Artillery 开展负载压测、分析性能瓶颈、量化 QPS 与响应时间时启用。请勿用于功能正确性验证。
allowed-tools: []
---

# 性能测试

用压测工具（k6、Artillery、JMeter）验证系统**能否承受预期负载**，定位性能瓶颈，量化 QPS、响应时间、并发上限等指标。

## 执行指令

1. **确定性能指标** — 业务目标：QPS、RT（P95/P99）、最大并发、错误率
2. **设计压测场景** — 基准、负载、压力、峰值、稳定性（阶梯式）
3. **编写压测脚本** — 定义请求、用户数、持续时长、断言阈值
4. **执行并监控** — 压测同时采集 CPU/内存/DB/网络指标
5. **分析瓶颈** — 定位慢查询、连接池、内存泄漏、锁竞争
6. **输出报告** — 指标对比、瓶颈定位、优化建议

## 使用示例

### 用户输入
"用 k6 压测 /api/attendance/list，目标 500 QPS，P95 < 200ms"

### 预期输出
```js
import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {
  scenarios: { load: { executor: 'ramping-vus', stages: [{ duration: '30s', target: 100 }] } },
  thresholds: {
    http_req_duration: ['p(95)<200'],   // 断言 P95 响应时间
    http_req_failed: ['rate<0.01'],     // 断言错误率 < 1%
  },
};
export default function () {
  const res = http.get('http://localhost:5050/api/attendance/list');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(0.1);
}
```

## 故障处理

| 场景 | 应对 |
|------|------|
| 压测结果忽高忽低 | 检查是否有预热不足、JIT、连接池冷启动 |
| 命中率低但延迟高 | 区分瓶颈在 DB/网络/应用，用监控数据定位 |
| 压测机自身成瓶颈 | 分布式压测或降低单机虚拟用户数 |

## 做什么不做什么

### ✅ 做什么
- 压测 API 与核心接口的容量与延迟
- 验证在目标并发下的稳定性
- 对比优化前后效果，量化收益
- 通过阶梯加压找出系统拐点

### ❌ 不做什么
- 没有性能目标时盲目压测（无意义）
- 对生产环境随意高压（先隔离或压测环境）
- 只看工具输出，忽略服务器/DB 侧监控数据
- 压测脚本本身不设断言、不测错误率
