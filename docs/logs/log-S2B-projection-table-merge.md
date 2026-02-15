# Log-S2B: projection table merge（统一投影消费框架的“合表”决策与边界）

---

**id**: `S2B-projection-table-merge`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `architecture/projection table merge (unified outbox/daemon)`
**status**: `draft`          # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Chronicle, Search, epic/s2, sub/0`
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

## 1) 合表要解决的真正问题是什么？

**draft**:

你已经会遇到的分裂症状：

- 两套 worker/daemon 逻辑：claim、retry/backoff、stuck reclaim
- 两套 metrics/告警/阈值、两套 runbook
- 两套 failed/DLQ/重放方式（甚至状态字段语义不同）

合表的核心动机：把“队列表”从按业务/投影分裂，变成一个共享基础设施入口。

**stable**:

一句话：合表是在增加共享基础设施，换取统一与可治理性，但会牺牲一定隔离性。

**archived**:

## 2) 为什么 projection ≥ 2 时收益会翻倍？

**draft**:

在只有一个 projection 时：
- 统一 outbox 的收益不明显
- 但要真实付出：payload 治理、索引设计、迁移风险、兼容策略

当你有 Search + Chronicle（或更多）以后：

- 统一 DLQ：failed 入口与重放命令一致
- 统一 runbook：排障流程/阈值/处理策略可以复用
- 统一 metrics：一套全系统 backlog/oldest age/failed/retry 看板
- 统一 worker 能力：retry/backoff/jitter、stuck reclaim、graceful shutdown、health/readiness

**stable**:

翻倍来自“共享能力被第二个投影复用”：第二条 projection 让前期一次性成本开始摊薄。

**archived**:

## 3) 合表的触发点/契机（什么时候开始变得合理）

**draft**:

满足下面任意 2 条，合表就开始变得合理：

- projection 数量 ≥ 2
- 你在复制同一套 daemon 运维机制（retry/stuck/DLQ/replay）
- 你需要统一的事件处理可观测性与治理（指标、告警、排障口径）
- 你要做跨投影的一致工具：一个 replay 工具覆盖任意 projection 的 failed 事件

**stable**:

触发点通常不是“想优化表结构”，而是“运维/治理能力重复建设”开始拖慢迭代。

**archived**:

## 4) 为什么合表容易翻车（风险清单）

**draft**:

合表的失败模式会从“某个投影坏了”升级成“共享心脏坏了全家遭殃”。常见翻车点：

1) **payload 变垃圾场**
- 每个 projection 临时塞字段、命名/类型不一致
- consumer 变成 if/else 博物馆
- 排障与演进成本指数增长

2) **索引需求互相打架**
- 不同 projection 对检索/过滤字段的索引需求不同
- 合表后索引膨胀、写入变慢、维护成本上升

3) **隔离性下降**
- 某个 projection 高吞吐/大 payload 会拖累其他投影

4) **迁移与兼容复杂度**
- 旧表/新表并行期、双写/回填、回滚策略

**stable**:

最大坑通常不是“迁移脚本”，而是“协议治理”：你是否愿意把 payload 当协议（contract）来管理。

**archived**:

## 5) 合表 vs 不合表：边界与决策法

**draft**:

适合合表（偏平台化）：

- 你想让**一个 daemon**处理所有 projection（按 projection/event_type 路由）
- 你想让**一套 DLQ/replay 工具链**覆盖全投影
- 你愿意承诺 **payload 协议治理**（schema_version/event_type 校验）

暂时别合表（偏隔离优先）：

- 某个 projection payload 很重、吞吐很高（会拖累其它投影）
- 还没准备好 schema/版本治理（合表会大概率长成垃圾场）
- 你更怕“全家遭殃”，宁愿多维护一套 worker

**stable**:

最稳的决策法：先判断“你要不要统一 daemon/runbook/DLQ/replay”，再决定“要不要统一表”。不要反过来。

**archived**:

## 6) 合表的最小可行结构（建议，不绑定具体实现）

**draft**:

如果决定合表，建议把“必须稳定、可索引、低基数”的字段**升列**，把“高频变动/高基数/大对象”留在 payload（JSON）里。

建议列（示意）：

- 标识与路由
  - `id`（event id）
  - `projection`（低基数枚举：search/chronicle/…）
  - `event_type`（低基数枚举）
  - `schema_version`（用于 payload 协议演进）

- 调度与幂等
  - `status`（pending/processing/done/failed 等）
  - `attempts` / `max_attempts`
  - `available_at`（下一次可重试时间）
  - `dedupe_key`（可选：去重/幂等）

- claim（并发控制）
  - `claim_batch_id`（可选：批次标识）
  - `locked_by` / `locked_at` / `lock_expires_at`

- 可观测性与审计
  - `correlation_id`（可选：跨模块串联）
  - `last_error_reason`（低基数枚举，便于统计）
  - `last_error_detail`（可选：短文本/截断）

- 时间戳
  - `created_at` / `updated_at` / `processed_at`

payload 建议：
- `payload_json` / `payload`（JSONB）：只放业务数据与必要上下文
- 禁止把“需要索引/过滤”的高频字段无约束塞进 payload（否则索引灾难）

索引建议（示意）：
- `status + available_at`（调度）
- `projection + status + available_at`（按投影调度）
- `lock_expires_at`（stuck reclaim）
- `projection + event_type`（路由/观测聚合）

**stable**:

最低要求：`projection/event_type/schema_version` 必须像协议字段一样被治理；consumer 先做 DTO 校验，确定性错误直接 failed（不重试），避免“无限重试吞资源”。

**archived**:

## 7) 迁移策略（建议）

**draft**:

- 先统一“运维能力与口径”（runbook/metrics/DLQ/replay），再做合表（减少一次性风险）。
- 如果必须合表：
  - 明确迁移期策略（并行/双写/回填/回滚）
  - 明确兼容窗口与 deprecation plan
  - 为每个 projection 制定容量与隔离策略（例如分片、限速、优先级队列/分区）

**stable**:

先统一能力，再统一表结构，是更稳的演进路径。

**archived**:

## References

- （docs governance / scripts entrypoint / snapshots）
  - `docs/logs/log-S0B-2A-scripts-snapshots-management.md`
  - `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md`
- （observability v2 / failure drills 自动化与证据包）
  - `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/logs/log-S3A-2A-4B-1A-git-actions.md`


//////////

你这份 log 已经很“像样”了：动机、收益、风险、边界、最小结构、迁移策略都齐了。接下来要做的是把它从“解释型文章”收口成“可执行的工程文档”（让未来的你/队友能按它做事、做完能验收、出事能回滚）。下面是我建议你可以立刻改的点（按收益从高到低）。 

log-S2B-projection-table-merge

1) 先补一个“结论区”，让它像 log，而不是随笔

你现在正文里 draft/stable 来回切换，读者要自己总结“你到底决定了啥”。建议在最前面加一个 Decision / Outcome 小节（哪怕先是 “TBD”），格式类似：

Decision：本轮合表范围（Search + Chronicle 的 outbox 表 → unified_outbox）

Status：draft / accepted / implemented / deprecated

Drivers（驱动因素）：projection≥2、重复建设运维能力、统一 DLQ/metrics/runbook/replay

Non-goals（不做什么）：不改业务事件模型、不引入新队列系统（Kafka/SQS）、不做跨投影强一致

Success criteria（验收）：见第 6 点的可验收清单

这样你以后翻 log，30 秒就能知道“当时决定了啥 & 做没做完”。

2) 把“合表”拆成两个可独立交付的决策：先统一“框架”，再统一“表”

你已经在文里写了黄金句：先判断要不要统一 daemon/runbook/DLQ/replay，再决定要不要统一表。
建议把它显式升格成两阶段：

Phase 1：Unified consumer framework（不合表也能做）

统一 claim / retry/backoff / reclaim / DLQ 语义

统一 metrics/tracing/logs shared keys

统一 replay 工具与 runbook

Phase 2：Table merge（结构层面的统一）

统一 schema / indexes / migration plan

原因很现实：Phase 1 做完，你已经拿到了 70% 运维收益；Phase 2 才是把“重复成本”进一步压平。

3) 加一个“替代方案”小节，让决策更硬

现在你有“合/不合”的边界，但缺少典型替代方案对比。建议补 3 个常见替代项，避免未来有人问“为什么不那样做”：

Alt A：不合表，只共享 outbox_core（库/包级复用）
代价：两张表；收益：隔离更强，迁移风险低。

Alt B：逻辑合表（同一张表但按 projection 分区/分桶/优先级）
代价：实现复杂；收益：统一入口但保留隔离。

Alt C：上真正队列（Kafka/SQS/Redis stream）
代价：运维/成本/复杂度高；收益：吞吐与弹性最好。

每个替代方案给一句“为什么这轮不选”。

4) “协议治理”建议再写具体一点：哪些字段是 Contract，怎么防垃圾场

你已经指出最大坑是“payload 治理”。建议你加三条“硬规则”，越土越有效：

列字段（columns）= 稳定、低基数、需要过滤/索引

payload = 高变动、高基数、业务细节（但要有 schema_version）

禁止：把“需要被 Grafana/PromQL 聚合”的东西塞 payload（否则你迟早写 JSONB 索引写到怀疑人生）

并补一个最小校验口径：

consumer 先做 DTO/schema 校验

deterministic failure（不可恢复）→ 直接 failed + reason=bad_payload / schema_mismatch

transient failure（可恢复）→ retry/backoff

这部分写清楚，合表才不会长成“if/else 博物馆”。

5) 索引建议加上“优先级”和“约束”，避免索引无限膨胀

你现在写了索引示意，很好，但建议补两类信息：

P0（必须）：驱动调度/claim/reclaim 的索引（否则 worker 性能会直接炸）

P1（建议）：用于观测聚合的索引

禁止项：不要为每个 projection 的临时字段加索引（要走 schema 提案流程）

另外可以补一条约束（如果你用 PG）：

status 枚举/检查约束（或者至少应用层强校验）

attempts >=0、available_at not null（按你实现定）

6) 把“迁移策略”落成一张可验收 checklist

你现在迁移策略写得偏原则。建议加一个 Migration checklist（这会直接帮你少掉头发）：

 新表 schema + index ready

 双写窗口定义（什么时候开始/结束）

 backfill 脚本可重复执行（幂等）

 replay 工具能对新表 failed 生效

 回滚策略：开关/feature flag/切回旧表读

 容量与隔离策略：projection 限速/优先级/分区（至少留接口）

 验证：对齐 processed_total、failed_total、oldest_age_seconds（旧 vs 新）

 Cutover：停止旧 worker → 切新 worker → 观察窗口 → 清理旧表（deprecate）

7) 结构细节：你现在的 draft/stable/archived 可以简化

当前每节都有三段（draft/stable/archived），读起来像“多时间线写作”。更实用的方式：

正文只保留 当前有效 内容

历史版本放到：

git diff（天然审计）

或 docs/legacy（如果你真的要保留）

如果你非常想保留状态机：建议只在顶部保留 status（draft/stable/archived），不要每节都写三份。

8) “合表算什么模块”这件事：建议你就归到 S2 Projection

你这份 log 是 “统一投影消费框架 + outbox/daemon 的共享基础设施”，本质上服务的是 Projection 的可治理性，所以放 S2 Projection是合理的（你文件名也已经是 S2B）。
如果未来你把 outbox_core 抽成更通用的 runtime 平台能力（给任何后台任务用，不只 projection），那才更像 S4 Ops Runtime。

如果你愿意把它再压缩一刀：我会建议你把 “1) 合表要解决的真正问题是什么？” 和 “2) 为什么 projection ≥2 时收益会翻倍？” 合并成一段“Problem statement + Why now”，避免重复铺垫。整体会更锋利。

你现在这份已经能开干了；把上面第 1、2、6 做完，它就会从“讲得通”变成“跑得起来、交付得了”。