# Log-S2B: projection table merge（统一投影消费框架的“合表”决策与边界）

---

**id**: `S2B-projection-table-merge`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `architecture/projection table merge (unified outbox/daemon)`
**status**: `draft`          # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Chronicle, Projection, Search, epic/s2, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
**created**: `2026-02-15`
**updated**: `2026-02-15`

---

## Background

合表（table merging）的本质目标不是“数据库更美观”，而是把多条 projection/daemon 的运维与治理能力**收口成一套**：

- 统一消费框架（claim/retry/backoff/stuck reclaim）
- 统一指标与看板（backlog/oldest age/failed/retry scheduled 等）
- 统一失败处理与 DLQ 语义
- 统一重放工具与 runbook

当系统只有 1 个 projection 时，“统一 outbox”往往只是改表名/搬字段，收益有限；当 projection 数量 ≥ 2（例如 Search + Chronicle）时，统一带来的边际收益会显著变大：一次实现、多处复用，运维成本不会线性增长。

## Decision / Outcome（结论区）

**Decision**:

- 将“合表”明确拆成两个可独立交付阶段：
  - Phase 1：统一消费框架（unified consumer framework）
  - Phase 2：表结构合并（table merge）
- 决策顺序固定：先判断是否要统一 daemon/runbook/DLQ/replay（治理能力），再决定是否要统一表（结构层面）。

**Drivers**:

- projection 数量 ≥ 2，重复建设 worker/daemon 能力与运维资产开始拖慢演进
- 需要统一的可观测性口径（指标/告警/排障）与失败治理（DLQ/replay）
- 需要可复用 runbook 与一致工具链，而不是按投影分裂

**Non-goals**:

- 不引入新的队列系统（Kafka/SQS/Redis Stream 等）作为本轮前置
- 不追求跨投影强一致或“全系统单点事务”
- 不把“数据库美观”作为核心目标

**Success criteria（DoD）**:

- Phase 1 完成：新增/迁移一个 projection 时，不再复制 claim/retry/reclaim/DLQ/replay/runbook；核心指标与排障链路复用
- Phase 2 完成：表结构统一后，迁移可回滚；并且不会把 payload 演进变成“垃圾场”
- 两阶段均可验收：能用 checklist 验证、能产出可观测证据、能跑通 replay

## Problem（要解决的真正问题）

当投影表按业务分裂，会自然出现：

- 两套 worker/daemon 逻辑：claim、retry/backoff、stuck reclaim
- 两套 metrics/告警/阈值、两套 runbook
- 两套 failed/DLQ/重放语义（甚至状态字段语义不同）

合表/统一框架的动机：把“队列表/消费者能力”升级为共享基础设施入口。

## Why Now（为什么现在值得做）

- 当 projection 只有 1 条时：收益有限但成本真实存在（payload 治理、索引设计、迁移风险）
- 当 projection ≥ 2 时：共享能力被第二条投影复用，边际收益显著增加（统一 DLQ/metrics/runbook/replay/worker 能力）

## Phase 1：Unified consumer framework（先统一框架，不要求合表）

目标：拿到 70% 运维收益，降低 Phase 2 的一次性风险。

交付件（建议最小集合）：

- 统一调度与并发语义：claim、lease、reclaim、max_attempts/backoff/jitter
- 统一状态机与失败语义：done/failed/retry_scheduled + reason（低基数枚举）
- 统一观测 shared keys：metrics/tracing/logs 对齐（projection/op/attempt/result/reason + trace_id/span_id + correlation_id）
- 统一 DLQ 与 replay：同一套命令/入口对所有 projection 生效
- 统一 runbook：排障流程与阈值不再按投影分裂

验收建议：

- 能对任意 projection 执行 replay（成功/失败都有可解释证据）
- 能用同一套 dashboard/PromQL 看到 backlog/oldest age/retry/failed

## Phase 2：Table merge（结构层面的统一）

### 2.1 风险清单（为什么容易翻车）

- 共享“心脏”故障会扩大影响面（隔离性下降）
- payload 形状不受控会长成 if/else 博物馆
- 索引需求互相打架导致索引膨胀、写入变慢
- 迁移期（并行/双写/回填/回滚）复杂度高

### 2.2 Alternatives（替代方案）

- Alt A：不合表，只共享 `outbox_core`（库/包级复用）
  - 优点：隔离更强、迁移风险低
  - 代价：仍维护两张表（但 Phase 1 的框架收益可先拿到）
- Alt B：逻辑合表（同一张表但按 projection 分区/分桶/优先级）
  - 优点：统一入口同时保留部分隔离
  - 代价：实现复杂，需要明确分区与容量策略
- Alt C：引入消息队列（Kafka/SQS/Redis Stream）
  - 优点：吞吐与弹性最好
  - 代价：运维与系统复杂度显著上升，不适合作为本轮前置

### 2.3 Contract governance（防 payload 垃圾场的硬规则）

三条硬规则（越土越有效）：

- columns = 稳定、低基数、需要过滤/索引/调度的字段
- payload = 高变动、高基数、业务细节（但必须有 `schema_version`）
- 禁止：把需要 Grafana/PromQL 聚合或调度过滤的字段无约束塞进 payload

校验口径：

- consumer 先做 DTO/schema 校验
- deterministic failure（不可恢复）→ 直接 failed + `reason=schema_mismatch|bad_payload`（不重试）
- transient failure（可恢复）→ retry/backoff

### 2.4 Minimal schema（最小可行结构建议）

建议把“必须稳定、可索引、低基数”的字段升列：

- 路由/协议：`projection`、`event_type`、`schema_version`
- 调度：`status`、`available_at`
- 重试：`attempts`、`max_attempts`
- claim：`locked_by`、`locked_at`、`lock_expires_at`（或 lease 语义等价字段）
- 审计/关联：`correlation_id`（可选）、`last_error_reason`（低基数枚举）、`processed_at`

payload：

- `payload`/`payload_json`（JSONB）：只放业务数据与必要上下文

### 2.5 Index policy（索引优先级与约束）

- P0（必须）：驱动调度/claim/reclaim 的索引
  - `status + available_at`
  - `projection + status + available_at`
  - `lock_expires_at`（reclaim）
- P1（建议）：用于观测聚合/排障的索引
  - `projection + event_type`
- 禁止项：为每个 projection 的临时字段随意加索引（需走 schema 提案/评审）

可选约束（以 PG 为例）：

- `attempts >= 0`
- `available_at` 非空（如果调度依赖）
- status 枚举/检查约束（或至少应用层强校验）

## Migration（迁移策略与可验收 checklist）

原则：先统一能力与口径（Phase 1），再统一表结构（Phase 2）。

Migration checklist（建议作为 DoD）：

- 新表 schema + index ready
- 双写窗口定义（开始/结束）
- backfill 脚本可重复执行（幂等）
- replay 工具对新表 failed 生效
- 回滚策略明确：开关/feature flag/切回旧表读
- 容量与隔离策略：projection 限速/优先级/分区（至少留接口）
- 验证：对齐 `processed_total/failed_total/oldest_age_seconds`（旧 vs 新）
- Cutover：停止旧 worker → 切新 worker → 观察窗口 → deprecate 旧表/旧路径

## Notes（定位：它属于哪个模块）

本主题本质上服务的是 Projection 的可治理性与统一消费框架，因此归到 `S2 Projection`（S2B）是合理的；若未来 outbox_core 上升为“通用后台任务平台能力”，再考虑归类到更偏 ops runtime 的范围。


## References

- （docs governance / scripts entrypoint / snapshots）
  - `docs/logs/log-S0B-2A-scripts-snapshots-management.md`
  - `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md`
- （observability v2 / failure drills 自动化与证据包）
  - `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/logs/log-S3A-2A-4B-1A-git-actions.md`