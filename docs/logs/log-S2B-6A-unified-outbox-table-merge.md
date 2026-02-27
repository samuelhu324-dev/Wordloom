# log-S2B-6A-unified-outbox-table-merge（P4–P6：payload 治理 + 容量/隔离 + 物理合表）

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

**Current status**:

- `2026-02-27`：本 log 仅完成结构落位（`draft`）；Execution Checklist 尚未执行。

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

- `P4`：payload contract 治理（`schema_version` + DTO/schema 校验 + deterministic failure 直接 failed）在 Search + Chronicle 两端都落地，且可审计。
- `P4`：容量/隔离策略（分区/分桶/优先级/限速/claim scope）明确，并写入 runbook。
- `P5`：物理合表（unified outbox table）迁移方案 + Alembic migration + backfill/dual-write/cutover 演练与证据闭环。
- `P6`：合表后的 cleanup（deprecate → 删除旧表/旧路径/旧 flag），按“每步 pre/post 固定回归包 + Evidence + SoT 更新”执行。

## Success Criteria（DoD）

- `P4` 完成：
  - Search + Chronicle 两端 consumer 均在处理前执行 DTO/schema 校验（含 `schema_version`）。
  - deterministic failure（不可恢复）→ 直接 `failed`，并落 `reason`（低基数枚举，例如 `schema_mismatch|bad_payload`）。
  - transient failure（可恢复）→ `retry_scheduled` + backoff。
  - 审计与观测：能按 `projection/op/result/reason` 维度统计，并可从 artifacts 复盘。

- `P5` 完成：
  - unified outbox table 的最小 schema proposal、索引策略、禁止项明确。
  - 能跑通：`alembic migration` → backfill（幂等）→ dual-write window → cutover（含回滚口径）。
  - 验证：固定 write-gate 回归包全绿 + sustained window 指标不退化。

- `P6` 完成：
  - 旧表/旧路径/旧 flag 按切片逐步删除；每一步都有 pre/post 证据与 SoT 入账。

## Plan（draft）

> 注：Plan 只描述“要做什么”（`P*-S*`）；执行记账在 Checklist（`P*-C*-S*`）。

### P4（硬门槛：payload 治理 + 容量/隔离策略）

- P4-S1：定义 payload contract（必须字段：`schema_version`、`projection`、`event_type` 等）与 DTO/schema 校验入口（Search + Chronicle）。
- P4-S2：定义 deterministic vs transient 的 failure taxonomy，并把 deterministic 直接 failed（不重试）。
- P4-S3：定义容量/隔离策略（至少包含：projection 维度限速/claim scope；可选：分区/分桶/优先级）。
- P4-S4：把治理规则与隔离策略写入 runbook，并在 drills 中可验证。

### P5（物理合表：unified outbox table migration）

- P5-S1：最小 schema proposal（列字段 + payload JSONB + 约束）与 index policy（P0/P1 + 禁止项）。
- P5-S2：迁移策略设计：backfill/dual-write/cutover/rollback（含窗口观察与止血开关）。
- P5-S3：实现 Alembic migration（新表 + 索引）与 backfill 工具（幂等）。
- P5-S4：定义并执行演练：pre/post 固定 write-gate 6-pack + sustained window + replay/rollback rehearsal。

### P6（物理合表后的 cleanup）

- P6-S1：制定 deletion ledger（旧表/旧路径/旧 flag）与每项 guard（pre/post drills + Evidence）。
- P6-S2：按最小 risk 顺序执行删除切片（每切片独立 commit/PR + 证据）。

## Execution Checklist（可执行清单 / checked）

### P4（硬门槛：payload 治理 + 容量/隔离策略）

- [ ] `P4-C1-S1`：payload contract（`schema_version`）与 DTO/schema 校验在 Search + Chronicle 两端落地。
- [ ] `P4-C1-S2`：deterministic failure → 直接 failed + `reason`（低基数枚举）；transient → retry/backoff。
- [ ] `P4-C1-S3`：容量/隔离策略落地（至少：projection 维度限速/claim scope），并可在 drills 验证。
- [ ] `P4-C1-S4`：runbook 更新（治理规则 + 隔离策略 + 排障口径）并入账 Evidence。

### P5（物理合表：unified outbox table migration）

- [ ] `P5-C1-S1`：最小 schema proposal + index policy + 禁止项（doc + ADR/notes 如需）。
- [ ] `P5-C1-S2`：迁移方案（backfill/dual-write/cutover/rollback）落地为可执行 checklist。
- [ ] `P5-C1-S3`：Alembic migration（新表 + 索引）+ backfill 工具（幂等）完成。
- [ ] `P5-C1-S4`：pre 固定 write-gate 6-pack + Evidence 入账。
- [ ] `P5-C1-S5`：dual-write window + sustained window（`dual_run/*/window_sustained`）+ Evidence 入账。
- [ ] `P5-C1-S6`：cutover + post 固定 write-gate 6-pack（N≥3，含 jitter）+ Evidence 入账。
- [ ] `P5-C1-S7`：rollback rehearsal（按 runbook）+ Evidence 入账。

### P6（物理合表后的 cleanup）

- [ ] `P6-C1-S1`：deletion ledger（旧表/旧路径/旧 flag）完成（只列清单，不删除）。
- [ ] `P6-C1-S2`：cleanup slice 1（最小风险项）pre/post 固定回归包 + Evidence。
- [ ] `P6-C2-S*`：按 slice 继续推进（每 slice 独立证据）。

## Evidence（证据与 SoT 规则）

- 固定 write-gate 回归包 run↔scenario 映射 SoT：`artifacts/write_gate_runs.latest.json`
- sustained window：优先复用 `drill-dual-run` 既有场景与产物结构。
