# log-S2C-3A-projection-rebuild-backfill-template（Rebuild/Backfill Template + Drills Automation）

---

**id**: `S2C-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `projection rebuild/backfill template + catalog-driven drills automation`
**status**: `draft`           # draft | stable | archived
**scope**: `S2C`
**tags**: `EVOLUTION, Projection, Platform, Framework, Outbox, Rebuild, Backfill, Drills, Catalog, epic/s2, sub/3`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log**: `docs/logs/log-S2B-3A-unified-consumer-framework.md` # outbox_core baseline
  **previous_log**: `docs/logs/log-S2C-2A-projection-writer-template.md`
**created**: `2026-03-01`
**updated**: `2026-03-01`

---

## Decision / Outcome（结论区）

**Decision**:

- 本切片交付 Phase 4（Rebuild/Backfill Template）+ Phase 5 的一个最小子集（Drills/Catalog Automation）：
  - 为“读侧投影表”提供可复制的 rebuild runner 模板（bookkeeping + metrics + runbook 口径统一）。
  - 为“证据跑法”提供可复制的 catalog 驱动入口（让场景能被 Actions runner 统一解析/运行/打包 evidence）。

**Why now**:

- Phase 3（Writer Template）已把 enqueue 语义统一；接下来最容易在迁移/故障时出事故的是“重建/回填/证据链”不一致。
- 统一 rebuild/backfill 与 drills 模板，可以把“新增第 3 条投影”的运维成本降到平台可复制的最低形态。

## Constraints（约束）

- 不改变 artifacts contract：drills 证据结构不变（`_result.json` / snapshot bundle 为 SoT）。
- 不引入新的对外入口：现有 stable scripts/workflows 不随意改名；如需迁移，优先 shim。
- 本切片不做 Search harness migration（DB→ES）：Search 的消费迁移仍按 S2C Phase 6（deferred）单独切片交付。

## Scope（本 log 范围）

- `P0`：Rebuild/Backfill contract（明确平台承诺：参数、幂等、bookkeeping、可观测性、失败语义）
- `P1`：Rebuild template（通用 runner：projection 选择 + status 记账 + metrics + dry-run）
- `P2`：Drills/Catalog automation（把关键“模板证据场景”纳入 catalog；为 Actions runner 提供稳定入口）
- `P3`：Evidence（按 S2B 口径补齐最小证据：N≥3 或等价稳定性证明）

## Success Criteria（DoD）

- 代码层面：
  - 至少 Chronicle（DB→DB）具备可复制的 rebuild runner（不依赖业务 API；DB-only 运行）。
  - rebuild 的 bookkeeping 与 metrics 口径统一（run_id/worker_id/projection）。
  - 关键证据场景能以 catalog 方式被 runner 解析并运行（CI 可复用）。

- 证据层面：
  - 至少 1 个 rebuild smoke / verify 场景能产出 artifacts；若涉及 worker 行为或一致性风险，补齐 N≥3 rounds。

## P0（Rebuild/Backfill contract｜v1）

> 目标：把 rebuild/backfill 从“脚本碎片”升级为“平台契约”，并避免在新增投影时语义漂移。

### Rebuild（读侧表重建）

- 输入（v1 最小集合）：
  - `projection`（必填）：例如 `chronicle_events_to_entries`
  - `--truncate`（可选）：是否清空读侧表再重建（注意与 `--emit-outbox` 组合时应清 outbox backlog，而非清读侧表）
  - `--emit-outbox`（可选）：将 rebuild 写入 outbox，由 harness 投影路径完成 materialize（用于验证 worker path）
  - `--limit / --since / --event-id`（可选）：用于小窗演练与风险隔离（不同投影可实现不同子集，但必须显式）

- 输出（bookkeeping + observability + evidence）：
  - **bookkeeping（DB 低基数）**：必须 upsert `projection_status`（1 行/投影），记录开始/结束、耗时、success/error。
  - **structured logs（可带 run_id/worker_id）**：必须输出 `run_id`、`worker_id`、`projection`、处理计数、关键 flags（truncate/emit_outbox/limit）。
  - **metrics（低基数）**：只允许以 `projection` 作为 label（避免 run_id/worker_id 进入 metrics）；至少输出：
    - `projection_rebuild_duration_seconds{projection}`
    - `projection_rebuild_last_finished_timestamp_seconds{projection}`
    - `projection_rebuild_last_success{projection}`
  - **evidence（artifacts / snapshot bundle）**：若用于 drills/CI，必须把关键 run 参数与结果写入 `_result.json` 或 snapshot bundle（以 artifacts 为 SoT）。

- 失败语义（v1）：
  - rebuild 失败必须可归因（低基数 reason taxonomy），建议：
    - `bad_payload` / `schema_mismatch`（payload contract）
    - `missing_entity`（SoT/outbox 指向缺失）
    - `db_constraint`（DB 约束）
    - `unexpected`（未分类异常）
  - 细节（stacktrace / offending ids）进入日志或 artifacts；`projection_status.last_rebuild_error` 只存短字符串摘要。

### Backfill（回填 outbox / 数据修复）

- 非目标（v1）：不在本切片强制实现所有 backfill 类型；但要把模板接口定下来，避免后续脚本散落。

### Non-goals / Risk Boundaries（平台不负责/风险边界）

- 不在 v1 强制统一所有 rebuild 的“数据源扫描策略”（全表扫描 vs 增量窗口），但要求每个 rebuild 脚本显式声明其扫描边界。
- 不把 `run_id/worker_id` 写入 metrics label；避免高基数污染监控。
- 不保证 rebuild 过程对线上业务无影响：
  - 需要运维层面通过 `--limit/--since`、低峰运行、限速/分批 commit 等方式控制风险。
- 不在本切片重写 Search 消费迁移（DB→ES）；Search 的 worker/harness 迁移仍在 Phase 6。

## Numbering（编号约定）

- `S<n>`：Step（步骤）。
- `C<n>`：Cycle（循环轮次）。同一切片需要“修复后重跑一轮”时才递增。

**Commit / PR 命名**:

- `S2C-3A/P<phase>-C<cycle>-S<step>: <summary>`

## Plan（draft）

### P0（Contract）

- P0-S1：明确 rebuild/backfill 的最小入参、bookkeeping、失败语义与观测口径
- P0-S2：明确“平台负责/不负责”（Non-goals）：不重写业务 SoT；只统一投影运维契约

### P1（Rebuild template implementation）

- P1-S1：落通用 rebuild runner（projection 选择 + status 记账 + metrics）
- P1-S2：以 Chronicle 为 reference：把 legacy rebuild 脚本形态收敛到 template（保留 stable entrypoint 或做 shim）

### P2（Drills/Catalog automation）

- P2-S1：将“Writer Template harness evidence（DB-only）”纳入 catalog（CI runner 可解析/运行）
- P2-S2：新增 1 个 rebuild smoke 场景并纳入 catalog（面向 Phase 4）
- P2-S3（可选）：新增/复用一个 workflow 入口，让 verify/rebuild 也能走 reusable-labs-scenario-runner

### P3（Evidence）

- P3-S1：按 S2B 口径跑最小证据包并入账（必要时 N≥3）

## Execution Checklist（unchecked）

### P0（Contract）

- [x] `P0-C1-S1`：定义 rebuild/backfill 最小接口与 bookkeeping/metrics 口径
- [x] `P0-C1-S2`：明确 Non-goals 与风险边界（避免 scope 膨胀）

### P1（Rebuild template implementation）

- [x] `P1-C1-S1`：实现通用 rebuild runner（DB-only 可跑）
- [x] `P1-C1-S2`：Chronicle rebuild 迁移到 template（入口稳定；必要时 shim）

### P2（Drills/Catalog automation）

- [x] `P2-C1-S1`：writer template evidence 纳入 catalog（Actions runner 可复用）
- [x] `P2-C1-S2`：rebuild smoke 场景纳入 catalog
- [x] `P2-C1-S3`：CI workflow（可选）

### P3（Evidence）

- [ ] `P3-C1-S1`：跑最小证据包并入账（N≥3 或等价稳定性证明）

## Evidence（预留）

- Evidence 以 artifacts 为事实源；本 log 记录：headSha + run URL + 关键参数。
- 本切片完成后，在此追加至少一条 rebuild/backfill 或 catalog-automation 相关的证据记录。

## Execution Notes（变更记账）

- `P2-C1-S1`（catalog 接入）已在 commit `81e09f93` 完成：新增 writer evidence scenario 并通过 guardrails。
- `P1-C1-S1/S2`（rebuild runner template + Chronicle 收敛）在 commit `652339cc` 完成：
  - 新增：`backend/infra/projection_framework/rebuild_template.py`
  - 迁移：`backend/scripts/legacy/rebuild_chronicle_entries.py` 统一使用 runner（status + metrics），保持现有 flags/行为
  - stable 入口保持：`backend/scripts/ops/rebuild_chronicle_entries.py` 仍作为 shim
- `P2-C1-S3`（workflow 入口）：新增一个 workflow_dispatch 入口复用 `reusable-labs-scenario-runner.yml`（见 `.github/workflows/drill-labs-scenario.yml`）
- `P2-C1-S2`（rebuild smoke）：新增 Chronicle rebuild smoke 场景 `verify/chronicle/rebuild_entries_smoke`，runner 为 `backend/scripts/labs/s2c3a_rebuild_chronicle_entries_smoke.py`（DB-only；产物 `_result.json` 为 SoT）
