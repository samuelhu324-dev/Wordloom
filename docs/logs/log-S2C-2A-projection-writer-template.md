# log-S2C-2A-projection-writer-template（Writer Template：统一 enqueue / trace / scope keys）

---

**id**: `S2C-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `projection writer template (unified enqueue for Search+Chronicle)`
**status**: `draft`           # draft | stable | archived
**scope**: `S2C`
**tags**: `EVOLUTION, Projection, Platform, Framework, Outbox, Writer, Search, Chronicle, epic/s2, sub/2`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log**: `docs/logs/log-S2B-3A-unified-consumer-framework.md` # outbox_core baseline
  **previous_log**: `docs/logs/log-S2C-1A-projection-spec-registry-harness.md`
**created**: `2026-03-01`
**updated**: `2026-03-01`

---

## Decision / Outcome（结论区）

**Decision**:

- 本切片交付 Phase 3（Writer Template）：把 “写 outbox（enqueue）” 的共性抽成可复用的模板能力，避免每个 projection 手写 enqueue、scope keys、reason taxonomy 与 trace 注入，从而降低新增/迁移投影的工程成本与语义漂移风险。

**What this unlocks**:

- Search / Chronicle 的写路径统一后，后续的 harness cutover、rebuild/backfill、drills template 会更容易标准化（且改动面可控）。

## Constraints（约束）

- 不改变 artifacts contract：drills 证据结构不变。
- 不引入新的对外入口：现有 stable scripts/workflows 不随意改名；如需迁移，优先 shim。
- 本切片不做 Search harness migration（DB→ES）：只做 writer 侧模板化与写路径切换。

## Scope（本 log 范围）

- `P0`：Writer contract（定义“平台承诺的 enqueue 语义”）
- `P1`：Writer template（实现通用 enqueue repo / helper）
- `P2`：Migrations（把 Search/Chronicle 写路径切到 writer template，事务语义不变）
- `P3`：Evidence（按 S2B 口径补齐最小证据）

## Success Criteria（DoD）

- 代码层面：
  - Search/Chronicle 写 outbox 不再各自拼装 payload / reason / scope keys；统一走同一套 writer API。
  - 事务边界与幂等语义不回退（仍由既有 outbox_core + DB 约束兜底）。

- 证据层面：
  - 若写路径影响 outbox 行为：按 S2B 口径跑最小回归包（N≥3 rounds，或等价的最小稳定性证明）。

## P0（Writer contract｜v1）

> 目标：把 Search / Chronicle 的“写 outbox”统一成同一套入参与字段映射；并约束 reason taxonomy / payload schema 的边界，避免低基数指标被污染。

### Writer inputs → outbox_events（字段映射）

- `projection` (str) → `OutboxEventModel.projection`
  - 例：Search=`search_index_to_elastic`；Chronicle=`chronicle_events_to_entries`
- `entity_type` (str) → `OutboxEventModel.entity_type`
  - 例：Search/Index=`block|book|tag|...`（沿用现有 SearchIndexModel 口径）
  - 例：Chronicle=`chronicle_event`
- `entity_id` (UUID) → `OutboxEventModel.entity_id`
  - Chronicle contract：`entity_id == chronicle_events.id`（consumer 以此回读 SoT）
- `op` (str) → `OutboxEventModel.op`
  - 允许集合（先按现状收敛）：`upsert|delete`
  - Chronicle contract：仅 `upsert`
- `event_version` (int) → `OutboxEventModel.event_version`
  - 用于 claim 顺序稳定性（与 `created_at` 一起排序）
  - Search：沿用 SearchIndexModel.event_version
  - Chronicle：暂用 `0`（维持既有行为；后续如需严格排序再演进）

### Scope keys（claim isolation）

- `library_id` (UUID | None) → `OutboxEventModel.library_id`
  - Search：若可得则写入（用于 allowlist / 隔离 claim）
- `book_id` (UUID | None) → `OutboxEventModel.book_id`
  - Chronicle：写入 `book_id`（用于 book-scoped claim / drills）

### Trace propagation（分布式追踪）

- Writer 必须尝试注入 trace context：
  - `traceparent` → `OutboxEventModel.traceparent`
  - `tracestate` → `OutboxEventModel.tracestate`

### Payload（可选；边界明确）

- `payload` (dict | None) → `OutboxEventModel.payload`
- 约束：必须是 JSON object（表约束已硬 gate）
- 约束：若调用方传入非空 payload，则必须包含 `schema_version: int`
- 约束：payload 只承载“稳定 envelope/路由信息”，不复制大字段/全文/快照；业务 SoT 仍在主表中回读
- Writer 模板行为：当调用方未传 payload 时，writer 会写入 `{}`（避免 `NULL` 触发 DB check constraint）

### Non-goals（writer 不负责写入）

- 不写入：`processed_at/owner/lease_until/processing_started_at/attempts/next_retry_at/error_reason/error`（均由 worker/harness/outbox_core 生命周期负责）

### Reason taxonomy boundary（避免指标基数爆炸）

- Writer **不接受/不写入** `error_reason`（失败原因由 consumer 侧低基数分类产生，供 metrics 聚合）
- 人工操作/审计原因（如 replay）仍允许写入 `last_replayed_reason`（free-text），但该字段不参与 metrics labels

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。同一切片需要“修复后重跑一轮”时才递增。

**Commit / PR 命名**:

- `S2C-2A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P0（Writer contract）

- P0-S1：明确 writer 输入（projection/entity/op/scope/trace/payload）与 outbox 侧字段映射
- P0-S2：明确 reason taxonomy 与 payload schema 边界（不扩大基数）

### P1（Writer template implementation）

- P1-S1：落一个通用 writer repo（enqueue API + 结构化日志）
- P1-S2：对齐 shared keys（run_id/worker_id/projection）与 outbox_metrics labels

### P2（Migrations）

- P2-S1：Chronicle 写路径切到 writer template（保持事务语义不变）
- P2-S2：Search 写路径切到 writer template（保持事务语义不变）

### P3（Evidence）

- P3-S1：跑最小证据包并入账（根据改动影响决定 N≥3）

## Execution Checklist（unchecked）

### P0（Writer contract）

- [x] `P0-C1-S1`：定义 writer 输入与字段映射（projection/entity/op/scope/trace/payload）
- [x] `P0-C1-S2`：约束 reason taxonomy 与 payload schema（保持低基数可聚合）

### P1（Writer template implementation）

- [x] `P1-C1-S1`：实现 writer template（enqueue API + structured logs）
-     Impl: `backend/infra/outbox_unified/writer.py` (`OutboxWriter.enqueue`)
-     Migrate: `backend/infra/search/search_outbox_repository.py` (delegate -> OutboxWriter)
-     Migrate: `backend/infra/storage/chronicle_repository_impl.py` (delegate -> OutboxWriter)
- [x] `P1-C1-S2`：对齐 metrics/shared keys（projection/op/reason；run_id/worker_id）
-     Impl: `backend/infra/outbox_unified/writer.py` (structured logs: event=outbox.enqueue; run_id/worker_id)
-     Impl: `backend/infra/observability/outbox_metrics.py` (`outbox_enqueued_total{projection,op}`)

### P2（Migrations）

- [x] `P2-C1-S1`：Chronicle 写 outbox 切换到 writer template（事务语义不变）
  Confirm: `SQLAlchemyChronicleRepository.save` -> `OutboxWriter.enqueue` (same `AsyncSession`; writer does not commit)
- [x] `P2-C1-S2`：Search 写 outbox 切换到 writer template（事务语义不变）
  Confirm: `PostgresSearchIndexer` -> `SearchOutboxRepository.enqueue` -> `OutboxWriter.enqueue` (same `AsyncSession`; writer does not commit)
  Verify: `py_compile` OK for migration-related modules; static scan confirms production write paths delegate to writer (legacy `backend/scripts/legacy/*` direct inserts are out of scope)

### P3（Evidence）

- [x] `P3-C1-S1`：跑 drills 并入账 evidence（按 S2B 口径补齐最小回归包）

#### Evidence approach & trade-offs（记账）

- 选择：按 “harness 路线” 跑 N≥3 rounds，但对两个投影采用不同证据闭环：
  - `chronicle_events_to_entries`：harness 实际消费（claim/apply/mark）+ DB verify，N≥3 rounds
  - `search_index_to_elastic`：仅验证 writer enqueue（outbox 行写入）+ DB verify，N≥3 rounds
    - 原因：本切片明确 deferred Search harness migration（DB→ES），且 builtin apply 仍为 stub；不把 ES/worker 作为 P3 前置依赖

- Why harness（优点）：
  - 直接覆盖 outbox lifecycle（claim → apply → mark_done/mark_retry/mark_failed → reclaim/sanitize），最贴近本切片的风险面（writer 模板化后 consumer/harness 语义不回退）。
  - 依赖更少：通常只需要 DB（不强依赖 ES / API 服务全量启动），成本/波动更可控。
  - 产物稳定：复用既有 artifacts contract，便于与 S2B 证据节奏对齐。

- Not chosen（为何不做/不作为本切片主证据）：
  - “写路径触发回归”（先制造 SoT 变更再消费）：更接近端到端，但依赖更多组件（API/seed 脚本/可能 ES），容易把本切片范围拉大；如需补强，可作为附加 1 次性验证而非 N≥3 主包。
  - dual-write/sampling/shadow-verify：更偏迁移对账阶段；本切片明确 deferred Search harness migration（DB→ES），不把该类证据纳入 P3 主闭环。

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + run URL + 关键参数。

### P3-C1-S1（N=3 rounds；harness-based + artifacts SoT）

- headSha: `678dec9d507c0fb87da7a6b84a024118eca9bc6f`
- DB: `postgresql://wordloom:wordloom@localhost:5435/wordloom_dev`（devtest-db 5435）
- Runner: `backend/scripts/labs/s2c2a_writer_template_harness_evidence.py`
- Rounds (artifacts):
  - `artifacts/_tmp_s2c2a_p3_round1/_result.json`
  - `artifacts/_tmp_s2c2a_p3_round2/_result.json`
  - `artifacts/_tmp_s2c2a_p3_round3/_result.json`

**What this evidence covers**:

- Chronicle：`SQLAlchemyChronicleRepository.save()` → `OutboxWriter.enqueue()` → harness 消费 `chronicle_events_to_entries` → 生成 `chronicle_entries`（DB verify）
- Search：`SearchOutboxRepository.enqueue()` → `OutboxWriter.enqueue()` → 写入 `outbox_events` pending 行（DB verify；不跑 ES/harness apply）

**Fix discovered during evidence**:

- `outbox_events.payload` 有 `ck_outbox_events_payload_object` 约束要求 payload 为 JSON object；
  证据跑中发现 writer 在 payload 省略时写入 `NULL` 会违反约束；已修复为默认写 `{}`。
