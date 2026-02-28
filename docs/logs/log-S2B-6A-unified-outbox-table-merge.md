# log-S2B-6A-unified-outbox-table-merge（P0–P2：payload 治理 + 容量/隔离 + 物理合表；对应 parent P4–P6）

---

**id**: `S2B-6A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `unified outbox table merge (Phase 2: hard gates + physical migration)`
**status**: `draft`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Chronicle, Search, Projection, TableMerge, epic/s2, sub/6`
**links**: ``
  **adr**: `docs/adr/adr-S2B-projection-table-merge.md`
  **runbook**: `docs/runbook/run-S2B-projection-table-merge.md`
  **sibling_log**: `docs/logs/log-S2B-4A-table-merge-migration.md` # Chronicle-first closure (completed)
  **sibling_log2**: `docs/logs/log-S2B-5A-table-merge-migration-v2.md` # Search closure (completed)
  **parent_log**: `docs/logs/log-S2B-projection-table-merge.md`
**created**: `2026-02-27`
**updated**: `2026-02-27`

---

## Decision / Outcome（结论区）

**Decision**:

- 将 S2B 总 log 的 `P4–P6`（payload 治理 / 容量隔离 / 物理合表迁移 + cleanup）独立为本子 log（`S2B-6A`），以便像 `S2B-5A` 一样用“Plan（draft）→ Execution Checklist（checked）→ Evidence”把后续高风险迁移做成可审计闭环。
- 本 log 的定位：**进入物理合表前的硬门槛 + 物理合表迁移本身 + 合表后的 cleanup**。

**Phase mapping（与 parent log 的对应关系）**:

> 说明：为避免编号跨 log 串联，本 log 的 `P0/P1/P2/...` **从 0 重新计数**。

- parent `P4`（payload 治理 + 容量/隔离）→ 本 log `P0`
- parent `P5`（物理合表迁移）→ 本 log `P1`
- parent `P6`（合表后 cleanup）→ 本 log `P2`

**Current status**:

- `2026-02-27`：`P0-C1` 已完成（含 drills/evidence），见 Evidence 区块（headSha + run URLs）。

## Numbering（编号约定）

> 目标：复用 `S2B-5A` 的 Step/Cycle/Commit 命名法，保证“可复盘、可审计、可对齐 headSha”。

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。同一切片需要“修复后重跑一轮”时才递增。
- 组合写法：`S1S2`（一次提交覆盖多个步骤）。

**Commit / PR 命名**:

- `S2B-6A/P<phase>-C<cycle>-S<step>: <summary>`

**Commit → Push → Evidence 顺序**:

- 所有需要 drills 的切片：先 commit+push，再跑 drills，再把 run URL 与 `headSha` 入账。

## Constraints（约束）

- 不引入第二套入口：仍以 `docs/runbook/run-S2B-projection-table-merge.md` + workflows（`drill-write-gate` / `drill-dual-run` / `drill-verify` / `drill-failures`）为唯一入口。
- Evidence 以 artifacts（summary/logs/traces/zip）为事实源；log 只记录“可复现 run URL + 关键参数 + headSha”。
- 物理合表不允许在 payload 治理缺失时“先上车后补票”（避免共享 outbox 变成垃圾场）。

## Scope（本 log 范围）

- `P0`：payload contract 治理（`schema_version` + DTO/schema 校验 + deterministic failure 直接 failed）在 Search + Chronicle 两端都落地，且可审计。
- `P0`：容量/隔离策略（分区/分桶/优先级/限速/claim scope）明确，并写入 runbook。
- `P1`：物理合表（unified outbox table）迁移方案 + Alembic migration + backfill/dual-write/cutover 演练与证据闭环。
- `P2`：合表后的 cleanup（deprecate → 删除旧表/旧路径/旧 flag），按“每步 pre/post 固定回归包 + Evidence + SoT 更新”执行。

## Success Criteria（DoD）

- `P0` 完成：
  - Search + Chronicle 两端 consumer 均在处理前执行 DTO/schema 校验（含 `schema_version`）。
  - deterministic failure（不可恢复）→ 直接 `failed`，并落 `reason`（低基数枚举，例如 `schema_mismatch|bad_payload`）。
  - transient failure（可恢复）→ `retry_scheduled` + backoff。
  - 审计与观测：能按 `projection/op/result/reason` 维度统计，并可从 artifacts 复盘。

- `P1` 完成：
  - unified outbox table 的最小 schema proposal、索引策略、禁止项明确。
  - 能跑通：`alembic migration` → backfill（幂等）→ dual-write window → cutover（含回滚口径）。
  - 验证：固定 write-gate 回归包全绿 + sustained window 指标不退化。

- `P2` 完成：
  - 旧表/旧路径/旧 flag 按切片逐步删除；每一步都有 pre/post 证据与 SoT 入账。

## Plan（draft）

> 注：Plan 只描述“要做什么”（`P*-S*`）；执行记账在 Checklist（`P*-C*-S*`）。

### P0（硬门槛：payload 治理 + 容量/隔离策略）

- P0-S1：定义 payload contract（必须字段：`schema_version`、`projection`、`event_type` 等）与 DTO/schema 校验入口（Search + Chronicle）。
- P0-S2：定义 deterministic vs transient 的 failure taxonomy，并把 deterministic 直接 failed（不重试）。
- P0-S3：定义容量/隔离策略（至少包含：projection 维度限速/claim scope；可选：分区/分桶/优先级）。
- P0-S4：把治理规则与隔离策略写入 runbook，并在 drills 中可验证。

### P1（物理合表：unified outbox table migration）

- P1-S1：最小 schema proposal（列字段 + payload JSONB + 约束）与 index policy（P0/P1 + 禁止项）。
- P1-S2：迁移策略设计：backfill/dual-write/cutover/rollback（含窗口观察与止血开关）。
- P1-S3：实现 Alembic migration（新表 + 索引）与 backfill 工具（幂等）。
- P1-S4：定义并执行演练：pre/post 固定 write-gate 6-pack + sustained window + replay/rollback rehearsal。

#### P1-C1-S1 draft：unified outbox table（最小 schema + index policy + 禁止项）

> 目标：把 `search_outbox_events` + `chronicle_outbox_events` 合并为一张表时，不牺牲 P0 的 hard gates（payload contract / deterministic reasons / isolation），并保持 worker 侧 claim/retry/lease 语义不变。

**Proposed table name**：`outbox_events`（或 `unified_outbox_events`；最终以 migration 命名为准）

**Required columns（最小闭环；对齐 outbox_core 语义）**：

- `id UUID PK`（默认 `uuid4()`）
- `projection TEXT NOT NULL`：队列/投影标识（例如：`search_index_to_elastic` / `chronicle_events_to_entries`）
- `entity_type VARCHAR(50) NOT NULL`
- `entity_id UUID NOT NULL`
- `op VARCHAR(20) NOT NULL`（例如：`upsert` / `delete`）
- `event_version BIGINT NOT NULL DEFAULT 0`

- `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- `processed_at TIMESTAMPTZ NULL`

- `status VARCHAR(20) NOT NULL DEFAULT 'pending'`（建议 CHECK：`pending|processing|done|failed`）
- `owner VARCHAR(120) NULL`
- `lease_until TIMESTAMPTZ NULL`
- `processing_started_at TIMESTAMPTZ NULL`

- `attempts INT NOT NULL DEFAULT 0`
- `next_retry_at TIMESTAMPTZ NULL`

- `error_reason VARCHAR(80) NULL`（低基数枚举；用于聚合/审计）
- `error TEXT NULL`（仅用于排障；由 sanitize 逻辑裁剪）

- `traceparent VARCHAR(512) NULL`
- `tracestate TEXT NULL`

- `replay_count INT NOT NULL DEFAULT 0`
- `last_replayed_at TIMESTAMPTZ NULL`
- `last_replayed_by VARCHAR(120) NULL`
- `last_replayed_reason TEXT NULL`

**Payload / contract columns（用于 P0 hard gate 延伸到统一表）**：

- `payload JSONB NULL`
  - 约束（建议 CHECK / 运行时校验）：
    - `payload IS NULL OR jsonb_typeof(payload) = 'object'`
    - 若非 NULL：必须包含 `schema_version INT`（v1 先要求 `=1`）
  - 语义：
    - Chronicle：可存放 envelope 最小快照（`schema_version/provenance/source/actor_kind/correlation_id`）或其它 consumer 必需字段。
    - Search：默认 `NULL`（不允许把 `text/snippet` 这类大字段塞进 outbox payload）。

**Scope / isolation columns（最小可操作；避免 claim 阶段 join）**：

- `library_id UUID NULL`（Search claim allowlist / canary；与现有 `search_outbox_events.library_id` 对齐）
- `book_id UUID NULL`（Chronicle claim allowlist；替代当前 worker 用子查询做隔离）

**Index policy（服务 claim/retry/reclaim/审计）**：

- `idx_outbox_entity`：(`projection`, `entity_type`, `entity_id`)
- `idx_outbox_processed`：(`projection`, `processed_at`)
- `idx_outbox_claim`：(`projection`, `status`, `next_retry_at`, `lease_until`, `event_version`)
- `idx_outbox_processing_started`：(`projection`, `status`, `processing_started_at`)
- `idx_outbox_error_reason`：(`projection`, `status`, `error_reason`)
- `idx_outbox_scope_library_claim`：(`projection`, `library_id`, `status`, `next_retry_at`, `lease_until`, `event_version`)（可选：如果 library_id 会常用）
- `idx_outbox_scope_book_claim`：(`projection`, `book_id`, `status`, `next_retry_at`, `lease_until`, `event_version`)（可选：如果 book_id 会常用）

**禁止项（hard no / 防止 unified outbox 变垃圾场）**：

- 禁止把高基数/动态字符串写入 `error_reason`（必须是低基数枚举，例如：`es_429|es_5xx|bad_payload|schema_mismatch|unknown_exception`）。
- 禁止把投影大字段塞进 `payload`（例如 Search 的 `text/snippet`，或任何可从 SoT 重建的大对象）。
- 禁止把包含敏感信息/大段 payload dump 的内容写入 `error`（只保留裁剪后的摘要；全文靠 artifacts/logs）。
- 禁止在统一表引入“按 projection 分叉的重复列地狱”（除 `library_id/book_id` 这类 scope key 外，其他投影字段优先放 `payload` 并受 schema_version 约束）。

#### P1-C1-S2 draft：迁移策略（new table → backfill → dual-write window → cutover → rollback）

> 目标：把“统一 outbox 表”的落地拆成可执行、可回滚、可审计的步骤；每一步都有明确的 guard（pre/post drills + Evidence + 止血开关）。

**基本原则（必须满足）**：

- 不停机迁移：任何时刻都必须可回滚到“旧表读写路径”。
- 读写解耦：写路径（enqueue）与读路径（worker claim）分别受控，避免一次改动影响过大。
- 双写先于切读：先确保“新表数据齐全且可追平”，再切 worker 读源。
- 一切以 projection 为单位：Search/Chronicle 两条队列可以分开切，但切换顺序必须可审计。

**需要的最小开关（实现约束；P1-C1-S3 代码落地）**：

- `OUTBOX_UNIFIED_WRITE_ENABLED`：enqueue 是否双写到新表（按 projection 维度；默认 false）。
- `OUTBOX_UNIFIED_READ_ENABLED`：worker claim 是否从新表读（按 projection 维度；默认 false）。
- `OUTBOX_UNIFIED_BACKFILL_ENABLED`：是否允许 backfill job 运行（默认 false；防误触）。

> 注：命名可调整，但必须具备“三段式开关”的能力：`write` / `read` / `backfill`。

**执行 checklist（最小版）**：

1) **Create new table（只加不改，风险最低）**
   - Action：Alembic 创建 `outbox_events` + indexes（按 `P1-C1-S1` 的 index policy）。
   - Guard：
     - 仅 DDL：不改任何生产读写路径。
     - `OUTBOX_UNIFIED_*` 全部保持 `false`。

2) **Backfill（旧表 → 新表；幂等）**
   - Action：实现并运行 backfill job：
     - 从 `search_outbox_events` 复制到新表（`projection='search_index_to_elastic'`；带 `library_id`）。
     - 从 `chronicle_outbox_events` 复制到新表（`projection='chronicle_events_to_entries'`；`book_id` 若可从 SoT 获取则填充，否则先允许 NULL）。
     - 必须幂等：用 `INSERT ... ON CONFLICT (id) DO NOTHING` / 或者等价 upsert 策略。
   - Guard：
     - Backfill 只写新表，不影响旧 worker。
     - Backfill 只处理“未终态”优先（`processed_at IS NULL` 或 `status in ('pending','processing')`）；终态可按需补齐用于审计。
     - Backfill 产物：输出计数（按 projection/status）+ 采样对账（row count / max(event_version)）。

3) **Enable dual-write window（先双写，仍旧表读）**
   - Action：打开 `OUTBOX_UNIFIED_WRITE_ENABLED=true`（先一条 projection，再另一条），让 enqueue 同时写旧表+新表。
   - Guard：
     - Worker 仍从旧表 claim（`OUTBOX_UNIFIED_READ_ENABLED=false`）。
     - 观察窗口：至少覆盖一个 dual-run/sustained window（见下）。
     - 止血：随时把 `OUTBOX_UNIFIED_WRITE_ENABLED=false` 关闭双写（回到旧行为）。

4) **Cutover read（切 worker 读新表；写仍双写）**
   - Action：打开 `OUTBOX_UNIFIED_READ_ENABLED=true`（按 projection 分批），worker 从新表 claim。
   - Guard：
     - 写保持双写：确保切读期间旧表仍在同步，方便回滚。
     - Cutover 前必须满足：
       - Backfill 已追平（新表 pending/processing 与旧表对齐到可接受误差）。
       - 新表上的 stuck/reclaim/metrics 维度齐全（projection/op/status/reason）。
     - Cutover 后观察：错误率、claim latency、stuck event 数量、attempts 分布。

5) **Rollback（演练与真实回滚口径一致）**
   - Action（回滚路径）：
     - `OUTBOX_UNIFIED_READ_ENABLED=false`（worker 改回旧表读）。
     - 保持 `OUTBOX_UNIFIED_WRITE_ENABLED=true` 一段窗口，避免切换期间丢事件；确认稳定后再决定是否关闭双写。
   - Guard：
     - 任何回滚必须记录：时间窗、开关状态、headSha、drill runs。

**每个阶段的 pre/post drills（Evidence 口径）**：

- 阶段 1（DDL）后：不强制跑完整 6-pack，但至少跑一次 `verify`（确保 worker 未受影响）。
- 阶段 2（Backfill）后：
  - `drill-write-gate` 固定 6-pack（更新 SoT：`artifacts/write_gate_runs.latest.json`）。
  - 关键 verify：Search paging stability / shared_keys / Chronicle entries。
- 阶段 3（dual-write window）期间：
  - `drill-dual-run` sustained window（`dual_run/*/window_sustained`）
  - 观察：错误率、积压（pending）趋势、claim/reclaim 指标。
- 阶段 4（cutover）后：
  - `drill-write-gate` 固定 6-pack（N≥3，含 jitter）
  - `drill-failures`（确保 deterministic reasons 仍为低基数且不重试）。
- 阶段 5（rollback rehearsal）：
  - 按 runbook 走“切回旧表读”的完整流程，并入账 Evidence。

### P2（物理合表后的 cleanup）

- P2-S1：制定 deletion ledger（旧表/旧路径/旧 flag）与每项 guard（pre/post drills + Evidence）。
- P2-S2：按最小 risk 顺序执行删除切片（每切片独立 commit/PR + 证据）。

## Execution Checklist（可执行清单 / checked）

### P0（硬门槛：payload 治理 + 容量/隔离策略）

- [x] `P0-C1-S1`：payload contract（`schema_version`）与 DTO/schema 校验在 Search + Chronicle 两端落地。
- [x] `P0-C1-S2`：deterministic failure → 直接 failed + `reason`（低基数枚举）；transient → retry/backoff。
- [x] `P0-C1-S3`：容量/隔离策略落地（至少：projection 维度限速/claim scope），并可在 drills 验证。
- [x] `P0-C1-S4`：runbook 更新（治理规则 + 隔离策略 + 排障口径）并入账 Evidence。

### P1（物理合表：unified outbox table migration）

- [x] `P1-C1-S1`：最小 schema proposal + index policy + 禁止项（doc + ADR/notes 如需）。
- [x] `P1-C1-S2`：迁移方案（backfill/dual-write/cutover/rollback）落地为可执行 checklist。
- [x] `P1-C1-S3`：Alembic migration（新表 + 索引）+ backfill 工具（幂等）完成。
- [x] `P1-C1-S4`：pre 固定 write-gate 6-pack + Evidence 入账。
- [x] `P1-C1-S5`：dual-write window + sustained window（`dual_run/*/window_sustained`）+ Evidence 入账。
- [x] `P1-C1-S6`：cutover + post 固定 write-gate 6-pack（N≥3，含 jitter）+ Evidence 入账。
- [x] `P1-C1-S7`：rollback rehearsal（按 runbook）+ Evidence 入账。

### P2（物理合表后的 cleanup）

- [x] `P2-C1-S1`：deletion ledger（旧表/旧路径/旧 flag）完成（只列清单，不删除）。
- [x] `P2-C1-S2`：cleanup slice 1（最小风险项）pre/post 固定回归包 + Evidence。
- [ ] `P2-C2-S*`：按 slice 继续推进（每 slice 独立证据）。

## Evidence（证据与 SoT 规则）

- 固定 write-gate 回归包 run↔scenario 映射 SoT：`artifacts/write_gate_runs.latest.json`
- sustained window：优先复用 `drill-dual-run` 既有场景与产物结构。

### P0-C1（payload contract + deterministic reasons + claim isolation）

- headSha: `5ccdc94e8dfcef35436566325dd5911b1a0c3042`

- Drill: drill-shadow-verify-entries | scenario_id: `verify/chronicle/entries` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22483614487 | status/conclusion: completed / success

- suite（write-gate 固定 6-pack；SoT: `artifacts/write_gate_runs.latest.json`）：
  - Drill: drill-write-gate | scenario_id: `shadow_verify_search_index_write_gate` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22483606613 | status/conclusion: completed / success
  - Drill: drill-write-gate | scenario_id: `shadow_verify_search_index_paging_stability` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22483608122 | status/conclusion: completed / success
  - Drill: drill-write-gate | scenario_id: `shadow_verify_shared_keys` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22483609521 | status/conclusion: completed / success
  - Drill: drill-write-gate | scenario_id: `shadow_verify_dual_run_window` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22483610634 | status/conclusion: completed / success
  - Drill: drill-write-gate | scenario_id: `shadow_verify_canary_dual_write` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22483611846 | status/conclusion: completed / success
  - Drill: drill-write-gate | scenario_id: `shadow_verify_dual_write_sampling` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22483613009 | status/conclusion: completed / success

### P1-C1-S1（doc-only：schema/index policy/prohibitions draft）

- headSha: `1209ca6994e504336fcb2aea348e045cf2cdfa1f`
- Notes: doc-only（无 drills）。

### P1-C1-S2（doc-only：migration checklist draft）

- headSha: `f6ea0cc0f2b89fccf7c44f3150b7ec038180136a`
- Notes: doc-only（无 drills）。

### P1-C1-S3（code landing：alembic migration + idempotent backfill tool）

- headSha: `825a20458c44afc146e341f72ac0a77d0b290d37`
- Notes: code-only（drills 在 `P1-C1-S4` 执行）。

### P1-C1-S4（pre：write-gate 固定 6-pack）

- headSha: `52cf85a2e781fbdb2b49a4b65b6653c8a036b200`
- suite（write-gate 固定 6-pack；SoT: `artifacts/write_gate_runs.latest.json`）：
  - Drill: drill-write-gate | scenario_id: `shadow_verify_search_index_write_gate` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22484696973 | status/conclusion: completed / success
  - Drill: drill-write-gate | scenario_id: `shadow_verify_search_index_paging_stability` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22484698130 | status/conclusion: completed / success
  - Drill: drill-write-gate | scenario_id: `shadow_verify_shared_keys` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22484699165 | status/conclusion: completed / success
  - Drill: drill-write-gate | scenario_id: `shadow_verify_dual_run_window` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22484700145 | status/conclusion: completed / success
  - Drill: drill-write-gate | scenario_id: `shadow_verify_canary_dual_write` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22484701213 | status/conclusion: completed / success
  - Drill: drill-write-gate | scenario_id: `shadow_verify_dual_write_sampling` | Run URL: https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22484702323 | status/conclusion: completed / success

### P1-C1-S5（dual-write window：本地证据）

- headSha: `34c534e3de525cf2dcd59f87a24e2d5ee3dd27de`
- Local env:
  - `DATABASE_URL=postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_dev`
  - `ELASTIC_URL=http://127.0.0.1:19200`
  - `OUTBOX_UNIFIED_WRITE_ENABLED=search_index_to_elastic`
  - `OUTBOX_UNIFIED_READ_ENABLED=`（空，仍旧表读）

- canary dual-write（默认 cleanup）：
  - artifacts: `artifacts/_local_s2b6a/P1-C1-S5/shadow_verify_canary_dual_write/20260227-203341/_result.json`
- sustained window（旧表读 + 双写开启）：
  - artifacts: `artifacts/_local_s2b6a/P1-C1-S5/shadow_verify_dual_run_window/20260227-203409/_result.json`
  - worker log: `artifacts/_local_s2b6a/P1-C1-S5/shadow_verify_dual_run_window/20260227-203409/worker.log`

### P1-C1-S6（cutover + post write-gate 6-pack：本地 N=3 rounds）

- headSha: `34c534e3de525cf2dcd59f87a24e2d5ee3dd27de`
- Local env:
  - `DATABASE_URL=postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_dev`
  - `ELASTIC_URL=http://127.0.0.1:19200`
  - `OUTBOX_UNIFIED_WRITE_ENABLED=search_index_to_elastic`
  - `OUTBOX_UNIFIED_READ_ENABLED=search_index_to_elastic`（切到 unified 表读）

- suite root（round1–round3，每轮 6 个 `_result.json`）：
  - `artifacts/_local_s2b6a/P1-C1-S6/20260227-203711/round1/`
  - `artifacts/_local_s2b6a/P1-C1-S6/20260227-203711/round2/`
  - `artifacts/_local_s2b6a/P1-C1-S6/20260227-203711/round3/`

### P1-C1-S7（rollback rehearsal：本地证据）

回滚口径：worker 切回旧表读（`OUTBOX_UNIFIED_READ_ENABLED=`），写保持双写（`OUTBOX_UNIFIED_WRITE_ENABLED=search_index_to_elastic`）。

- headSha: `34c534e3de525cf2dcd59f87a24e2d5ee3dd27de`
- Local env:
  - `DATABASE_URL=postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_dev`
  - `ELASTIC_URL=http://127.0.0.1:19200`
  - `OUTBOX_UNIFIED_WRITE_ENABLED=search_index_to_elastic`
  - `OUTBOX_UNIFIED_READ_ENABLED=`（空，回滚到旧表读）

- sustained window（回滚读旧表 + 双写开启）：
  - artifacts: `artifacts/_local_s2b6a/P1-C1-S7/20260227-204657/window_sustained/_result.json`

### P2-C1-S1（doc-only：deletion ledger（旧表/旧路径/旧 flag）；只列清单不删除）

- headSha: `34c534e3de525cf2dcd59f87a24e2d5ee3dd27de`

> 目标：把 cleanup 变成可切片推进的“删除账本”，每项都有明确的 **删除前条件**、**pre/post guards**、**回滚口径**；避免一次性大清理不可控。

Ledger（按最小风险顺序建议；仅列清单）：

| Item | 类别 | 删除对象 | 触发条件（删除前必须满足） | Guards（pre/post 固定回归包） | 回滚口径 |
|---|---|---|---|---|---|
| L1 | DB | `search_outbox_events`（旧表） + 相关 alembic revisions | Search projection 在生产已满足：`OUTBOX_UNIFIED_WRITE_ENABLED` 常开、`OUTBOX_UNIFIED_READ_ENABLED` 常开；旧表 backlog=0（pending/processing=0）；且观察窗内无回滚事件（例如 7d） | pre: write-gate 6-pack（N≥3）+ window sustained；post: 同上 + failures drill（reason 低基数） | 仍保留 unified 表；回滚不再依赖旧表（因此 drop 前必须确认无需再靠旧表回滚） |
| L2 | DB | `chronicle_outbox_events`（旧表） + 相关 alembic revisions | Chronicle projection 同样满足：write/read 常开；旧表 backlog=0；观察窗内无回滚 | pre/post 同上（对 Chronicle 另需 entries 相关 verify） | 同 L1 |
| L3 | ORM | `backend/infra/database/models/search_outbox_models.py`（SearchOutboxEventModel） | L1 完成且代码写路径不再写旧表、worker 不再读旧表 | pre/post write-gate 6-pack（含 window） | 若需要回滚，应通过 unified outbox 的开关/代码路径回滚（不再依赖旧表模型） |
| L4 | ORM | `backend/infra/database/models/chronicle_outbox_models.py`（ChronicleOutboxEventModel）与 [backend/infra/database/models/__init__.py](backend/infra/database/models/__init__.py) 的 export | L2 完成且 Chronicle 写路径/worker 已完全不依赖旧表 | pre/post：Chronicle verify + window sustained | 同上 |
| L5 | Write path | [backend/infra/search/search_outbox_repository.py](backend/infra/search/search_outbox_repository.py)：停止写旧表（仅写 unified） | L1 进入“待删”阶段（至少已切读 unified 并验证稳定） | pre/post write-gate 6-pack（N≥3） | 若发生异常，回滚通过开关或临时恢复双写（需要保留迁移 PR 的 revert 口径） |
| L6 | Write path | [backend/infra/storage/chronicle_repository_impl.py](backend/infra/storage/chronicle_repository_impl.py)：停止写 `chronicle_outbox_events`（仅写 unified） | L2 进入“待删”阶段 | pre/post：Chronicle verify + write-gate | 同上 |
| L7 | Worker runtime | [backend/scripts/search_outbox_worker_impl.py](backend/scripts/search_outbox_worker_impl.py)：移除 legacy/unified 的运行时分叉（固定读 unified + projection filter） | L1/L3/L5 完成后 | pre/post window sustained（严格 parity） | 临时回滚到旧 worker 需通过代码回滚（因此此项应在 drop table 之后再做） |
| L8 | Worker runtime | [backend/scripts/chronicle_outbox_worker.py](backend/scripts/chronicle_outbox_worker.py) shim + [backend/scripts/legacy/chronicle_outbox_worker.py](backend/scripts/legacy/chronicle_outbox_worker.py)：移除 legacy 实现与 shim（以统一实现替代） | L2/L4/L6 完成后 | pre/post：Chronicle window + entries verify | 同上 |
| L9 | Ops / replay | [backend/scripts/search_outbox_replay_failed.py](backend/scripts/search_outbox_replay_failed.py)、[backend/scripts/ops/search_outbox_replay_failed.py](backend/scripts/ops/search_outbox_replay_failed.py)、legacy 对应脚本：改为统一 outbox 重放（projection 过滤）或移除旧入口 | L1 完成且失败重放仅针对 unified outbox | pre/post：failures drill（replay/audit 字段） | 若回滚需要 replay，确保 unified replay 工具可用 |
| L10 | Ops / replay | Chronicle replay 同上：`chronicle_outbox_replay_failed.py`（stable + legacy） | L2 完成 | pre/post：Chronicle failures drill | 同上 |
| L11 | Drills / labs | `backend/scripts/legacy/*` 中直接写旧表的插入/排障脚本（如 labs_009_insert_*、ops_labs_005_*） | L1/L2 完成且 runbook 不再依赖旧表脚本 | pre/post：不强制（脚本仅用于历史/排障）；但需确保 runbook 入口仍可用 | 若仍需保留历史排障材料，可迁移为“读 unified + projection”版本 |
| L12 | Docs / env | `backend/.env.test.example`、runbook 中旧表/旧脚本的描述与命令 | 对应 L* 项完成后逐步同步文档 | 无（文档变更） | N/A |

Slice 建议（对应 Checklist 的 P2-C1-S2 / P2-C2-S*）：

1) Slice A（最小风险）：先“停止写旧表”（L5/L6），但先不 drop 表；保留回滚余地。
2) Slice B：worker 固定读 unified（L7/L8 的核心逻辑），并跑一轮 N≥3 回归包。
3) Slice C：drop legacy tables（L1/L2）+ 删除 legacy ORM（L3/L4）。
4) Slice D：收尾清理 legacy scripts/docs（L9–L12）。

### P2-C1-S2（Slice A：unified-write => unified-only enqueue；pre/post 本地 N=3 rounds）

- pre headSha: `ba8f282b7b4d8bb7544ff9a4b595007b0ad6f343`
- post headSha: `18afcfa2`（`S2B-6A/P2-C1-S2: slice A unified-write => unified-only enqueue`）

- Local env:
  - `DATABASE_URL=postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_dev`
  - `ELASTIC_URL=http://127.0.0.1:19200`
  - `OUTBOX_UNIFIED_WRITE_ENABLED=search_index_to_elastic,chronicle_events_to_entries`
  - `OUTBOX_UNIFIED_READ_ENABLED=search_index_to_elastic,chronicle_events_to_entries`

- pre suite root（round1–round3，每轮 6 个 `_result.json`）：
  - `artifacts/_local_s2b6a/P2-C1-S2/20260227-213405/pre/round1/`
  - `artifacts/_local_s2b6a/P2-C1-S2/20260227-213405/pre/round2/`
  - `artifacts/_local_s2b6a/P2-C1-S2/20260227-213405/pre/round3/`

- post suite root（round1–round3，每轮 6 个 `_result.json`）：
  - `artifacts/_local_s2b6a/P2-C1-S2/20260228-105240/post/round1/`
  - `artifacts/_local_s2b6a/P2-C1-S2/20260228-105240/post/round2/`
  - `artifacts/_local_s2b6a/P2-C1-S2/20260228-105240/post/round3/`

- Notes:
  - Slice A 口径：当 unified write enabled 时，写路径仅写 `outbox_events`，不再写 legacy outbox tables。
  - post：补跑 `round3/sampling_cleanup` 以补齐缺失 `_result.json`（`remaining_legacy_outbox_rows: 0` / `ok: true`）。
