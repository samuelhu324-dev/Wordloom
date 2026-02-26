# Log-S2B-4A: table merge migration （Phase 2：schema/migration/backfill/rollback）

---

**id**: `S2B-4A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `table merge migration (Phase 2: projection table merge)`
**status**: `draft`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Chronicle, Projection, TableMerge, epic/s2, sub/4`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: `docs/adr/adr-S2B-projection-table-merge.md`
  **runbook**: `docs/runbook/run-S2B-projection-table-merge.md`
  **phase1_log**: `docs/logs/log-S2B-3A-unified-consumer-framework.md`
  **parent_log**: `docs/logs/log-S2B-projection-table-merge.md`
**created**: `2026-02-24`
**updated**: `2026-02-26`

---

## Decision / Outcome（结论区）

**Decision**:

- 前置条件：`S2B-3A`（unified consumer framework / outbox_core）已收敛出“固定 write-gate 回归包（6 scenarios）”与可审计证据链，因此开始推进 Phase 2：table merge migration。
- 本 log 只记录 Phase 2 的 schema/migration/backfill/rollback/cutover；Phase 1 的框架演进仍以 `S2B-3A` 为 SoT（仅引用，不沿用其内部 Phase 编号）。

**Numbering（编号约定）**:

- 本 log 内的 `P0/P1/P2/...` 是 Phase 2 的本地切片编号（reset 计数），不与 `S2B-3A` 的 `P0/P1/P2` 连续或对齐。

**Constraints（约束）**:

- 入口不分叉：仍以 `docs/runbook/run-S2B-projection-table-merge.md` + `drill-write-gate` + `backend/scripts/cli.py` 为单入口。
- 验收与排障仍以 artifacts（summary/logs/traces/zip）与 shared keys 为事实源。

## Scope（本 log 范围）

- Chronicle-first：优先推进 Chronicle 的 projection table merge 迁移闭环（shadow → dual-run → cutover → cleanup）。
- Search 的 table merge 如进入执行，必须在本 log 明确切片与证据；否则不默认扩张范围。

## Success Criteria（DoD）

- Schema/index ready：新表（或新结构）具备可运行的索引策略，不阻塞 claim/reclaim/verify。
- Migration 过程可回滚：读开关、写开关、回填脚本均具备“可重复执行 + 可停止/回退”的操作路径。
- Evidence 可审计：
  - cutover 前：固定 write-gate 回归包（6 scenarios）持续全绿
  - cutover 后：同一回归包持续全绿，并且出现问题时可从 artifacts 定位原因。

## Plan（draft）

> 注：延续 Step/Cycle 命名法；每个切片都必须闭环：Implementation → Regression（固定 write-gate 回归包）→ Evidence。

- P0（门槛确认 / baseline）
  - P0-S1：跑一轮固定 write-gate 回归包（Phase 2 baseline）
  - P0-S2：更新 artifacts 映射 + 在本 log 入账 Evidence（run URL + conclusion + baseline 结论）

- P1（schema/index 准备，不触碰入口；保持可回滚）
  - P1-S1：形成最小 schema/index 提案（包含 rollback/开关点清单）
  - P1-S2：落地 migration（只加结构/索引/开关，不做 cutover）
  - P1-S3：跑固定 write-gate 回归包
  - P1-S4：Evidence 入账

- P2（migration/backfill 演练）
  - P2-S1：定义 backfill 幂等脚本与窗口（可重复执行 + 可停止/回退）
  - P2-S2：演练 backfill（dry-run/小窗口）
  - P2-S3：跑固定 write-gate 回归包
  - P2-S4：Evidence 入账

- P3（cutover + 窗口观察）
  - P3-S1：按 runbook 推进 cutover（可回退路径明确）
  - P3-S2：跑固定 write-gate 回归包
  - P3-S3：Evidence 入账 + 窗口内异常处置记录

- P4（cleanup ledger）
  - P4-S1：记录 stub/deprecate window 与清理计划（不提前删旧路径）

- P5（real cutover + deprecate window）
  - P5-S1：推进真实 cutover（将默认读/写路径切到新表；保留回滚路径）
  - P5-S2：跑固定 write-gate 回归包（pre/post）
  - P5-S3：进入 deprecate window（观察窗口 + 证据入账；不做最终删除）

> Cycle 约定：若同一组步骤需要重复一轮（回归重跑/补证据/修正后再跑），在 step 前加 cycle，例如 `P1-C2-S3`；若多个 step 一起提交，可合并写成 `P1-C2-S1S2`。

## Execution Checklist（可执行清单 / checked）

### P0（baseline）

- [x] `P0-C1-S1S2`：固定 write-gate 回归包 baseline 已完成，并已在 Evidence 入账（6/6 success）。

### P1-C1（schema/index 提案 + 回滚清单；no DB change）

- [x] `P1-C1-S1S2`：schema/index proposal（draft）+ rollback/开关点 checklist（不改 DB、不改入口）。
- [x] `P1-C1-S3S4`：跑固定 write-gate 回归包 + Evidence 入账（证明“只有文档/清单变更也不破坏回归链路”）。

### P1-C2（schema/index migration；DB change，no cutover/backfill）

- [x] `P1-C2-S1S2`：落地 schema/index migration（Chronicle-first：为 `chronicle_entries` 补齐 envelope 列/索引；不做 cutover/backfill）。
- [x] `P1-C2-S3S4`：跑固定 write-gate 回归包 + Evidence 入账。

### P2-C1（migration/backfill 演练准备；no cutover）

- [x] `P2-C1-S1S2`：补齐 backfill/重建路径对新列的写入（重建工具 + worker materialize 均写满 envelope 列，避免默认值掩盖数据）。
- [x] `P2-C1-S3S4`：跑固定 write-gate 回归包 + Evidence 入账。

### P2-C2（migration/backfill 演练；no cutover）

- [x] `P2-C2-S1S2`：演练 backfill（dry-run/小窗口；CI drill-verify）。
- [x] `P2-C2-S3S4`：跑固定 write-gate 回归包 + Evidence 入账。

### P3-C1（cutover + 窗口观察）

- [x] `P3-C1-S1S2`：Chronicle read switch rehearsal（`MERGED_READ_ENABLED=0/1` smoke；CI drill-verify）。
- [x] `P3-C1-S3S4`：跑固定 write-gate 回归包 + Evidence 入账。

### P3-C2（cutover + 窗口观察）

- [x] `P3-C2-S1S2`：Search read switch rehearsal（`SEARCH_MERGED_READ_ENABLED=0/1` provider smoke；CI drill-verify）。
- [x] `P3-C2-S3S4`：Search write cutover window（sustained window；CI drill-dual-run；scenario=`dual_run/search/window_sustained`）。
- [x] `P3-C2-S5S6`：跑固定 write-gate 回归包 + Evidence 入账。

### P4-C1（cleanup ledger；no deletion yet）

- [x] `P4-C1-S1S2`：记录 stub/deprecate window 与清理计划（不提前删旧路径；回滚优先）。
- [x] `P4-C1-S3S4`：跑固定 write-gate 回归包 + Evidence 入账（doc-only regression）。

### P4-C2（first real cleanup：delete legacy tracked artifacts snapshots）

- [x] `P4-C2-S1S2`：cleanup 前跑固定 write-gate 回归包 + Evidence 入账（pre）。
- [x] `P4-C2-S3`：删除 legacy tracked artifacts snapshots（旧 write-gate run dumps；仅保留 latest SoT）。
- [x] `P4-C2-S4S5`：cleanup 后再跑固定 write-gate 回归包 + Evidence 入账（post；SoT 更新）。

### P4-C3（Search cleanup：remove ops worker shim; keep stable entrypoint）

- [x] `P4-C3-S1S2`：cleanup 前跑固定 write-gate 回归包 + Evidence 入账（pre）。
- [x] `P4-C3-S3`：cleanup - remove unused Search ops worker shim（use stable entrypoint）。
- [x] `P4-C3-S4S5`：cleanup 后再跑固定 write-gate 回归包 + Evidence 入账（post；SoT 更新）。

### P4-C4（Chronicle cleanup：restore stable entrypoints; retire ops worker shim）

- [x] `P4-C4-S1S2`：cleanup 前跑固定 write-gate 回归包 + Evidence 入账（pre）。
- [x] `P4-C4-S3`：cleanup - restore stable chronicle worker/replay entrypoints（scripts/） and retire ops worker shim。
- [x] `P4-C4-S4S5`：cleanup 后再跑固定 write-gate 回归包 + Evidence 入账（post；SoT 更新）。

### P4-C5（Search cleanup：add missing stable replay entrypoint）

- [x] `P4-C5-S1S2`：cleanup 前跑固定 write-gate 回归包 + Evidence 入账（pre）。
- [x] `P4-C5-S3`：cleanup - add missing stable search replay entrypoint（scripts/）。
- [x] `P4-C5-S4S5`：cleanup 后再跑固定 write-gate 回归包 + Evidence 入账（post；SoT 更新）。

### P4-C6（Replay shims cleanup：ops entrypoints forward canonical stable entrypoints）

- [x] `P4-C6-S1S2`：cleanup 前跑固定 write-gate 回归包 + Evidence 入账（pre）。
- [x] `P4-C6-S3`：cleanup - make ops replay shims forward canonical stable entrypoints（scripts/），避免双份 shim 漂移。
- [x] `P4-C6-S4S5`：cleanup 后再跑固定 write-gate 回归包 + Evidence 入账（post；SoT 更新）。

### P5（real cutover + deprecate window）

> 说明：当前 `P3` 的 cutover 相关步骤以 rehearsal/窗口演练为主；`P5` 用于把“真实切换 + 观察窗口”显式化并闭环。

- [x] `P5-C1-S1S2`：真实 cutover 前跑固定 write-gate 回归包 + Evidence 入账（pre）。
- [x] `P5-C1-S3`：真实 cutover（Chronicle-first：默认读切到 `chronicle_entries`；保留 `MERGED_READ_ENABLED=0` 一键回滚 + drills/单测语义同步）。
- [x] `P5-C1-S4S5`：真实 cutover 后再跑固定 write-gate 回归包 + Evidence 入账（post；SoT 更新）。

- [x] `P5-C2-S1S2`：deprecate window 观察计划（窗口长度/关键指标/告警阈值/回滚手册）；只写清单不删旧路径。
- [x] `P5-C2-S3`：将旧路径标注为 deprecated（runbook + 本 log；仍保留回滚入口）。
- [x] `P5-C2-S4S5`：窗口期结束后再跑固定 write-gate 回归包 + Evidence 入账。

#### P5-C2（deprecate window：观察计划 + 回滚手册；doc-only）

> 目标：在 **cutover default 已生效** 的前提下，把“可观察、可回滚、可审计”的窗口操作写成可执行清单。
> 说明：本窗口不删除旧路径/旧表/旧 flag；旧路径仅作为回滚与对比排障的安全垫。

**Evidence window（建议口径；以“轮次/事件量”替代纯时间）**:

- 窗口时长（参考）：`2–6h` 通常足够；核心不是等时间，而是跑出足够“扰动 + 轮次 + 事件量”的证据。
- 窗口开始条件：`P5-C1` post-cutover 固定 write-gate 6-pack 为绿（6/6 success）。
- 窗口内目标（最小可执行版本）：
  - 连续跑 `N` 轮固定 write-gate 6-pack（建议 `N>=3`），每轮之间人为引入少量扰动/间隔（sleep/jitter）。
  - 至少 1 次把 `shadow_verify_dual_run_window`（window sustained）跑成“更高事件量”的 profile（通过 workflow inputs 的 `window_*` 调整 `max_total_events / duration / interval / batch_size`）。
  - 至少 1 次做“回滚演练”（见下方 Rollback manual；推荐跑 `rehearsal_chronicle_read_switch_smoke` 作为可审计的 smoke）。
- 窗口结束动作：执行 `P5-C2-S4S5`（再跑一轮固定 6-pack，并入账 Evidence + 更新 SoT）。

**Key signals（只选“最小且能止血”的观测点）**:

- `API 5xx/exception`：Chronicle 读相关接口在窗口内无新增异常峰值。
- `DB pressure`：Postgres 慢查询/锁等待无明显回归（以现有监控/日志为准）。
- `Drill health`：固定 write-gate 6 scenarios 在窗口末仍保持全绿（作为最小可审计证据）。

**Rollback manual（止血优先；只做读侧回滚）**:

- 触发条件（任一满足即可回滚）：
  - Chronicle 读相关错误率明显上升且短时间无法解释
  - 出现数据不一致/查询结果异常的告警或人工确认
- 回滚动作：设置 `MERGED_READ_ENABLED=0`，强制回到 legacy read（旧路径）。
- 回滚后必做：
  - 记录回滚原因与时间点（本 log 的 Evidence 区追加一条备注）
  - 重新跑固定 write-gate 6-pack（用于确认“止血后回归包仍可解释”）

**Deprecated markers（宣告弃用，但不删除）**:

- runbook：见 `docs/runbook/run-S2B-projection-table-merge.md` 的 “Current state（cutover + rollback；Chronicle）”。
- 本 log：从本 cycle 起，legacy read 路径仅作为回滚/排障对比路径；任何新逻辑不得再把它当默认依赖。

**Evidence templates（copy/paste；窗口期执行完就入账）**:

> 目的：把“跑了什么、用的什么扰动参数、结果如何、run URL 在哪”用一致格式落账。
> 说明：
> - 固定 6-pack：建议用 `scripts/p1_write_gate_regression.ps1` 输出的 Evidence snippet 直接粘贴。
> - window sustained profile：建议单独记录“用的 window_* 参数”，避免只看到 run URL 却不知道负载口径。
> - 回滚演练：推荐 `rehearsal_chronicle_read_switch_smoke`（同一次 run 同时覆盖 `MERGED_READ_ENABLED=0/1` 两条路径）。

Template A — Round i/N: fixed write-gate 6-pack (all green)

- Date: `YYYY-MM-DD`
  - Change: `S2B-4A/P5-C2-S4S5: evidence window round i/N (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Command: `scripts/p1_write_gate_regression.ps1 -Rounds N -JitterSecondsMin <min> -JitterSecondsMax <max>`
  - Notes: `jitter applied between rounds; cutover default active; rollback available via MERGED_READ_ENABLED=0`
  - Evidence (paste from script output):
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_write_gate` | Run URL: `<url>` | status/conclusion: `<status>` / `<conclusion>`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_paging_stability` | Run URL: `<url>` | status/conclusion: `<status>` / `<conclusion>`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_shared_keys` | Run URL: `<url>` | status/conclusion: `<status>` / `<conclusion>`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_run_window` | Run URL: `<url>` | status/conclusion: `<status>` / `<conclusion>`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_canary_dual_write` | Run URL: `<url>` | status/conclusion: `<status>` / `<conclusion>`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_write_sampling` | Run URL: `<url>` | status/conclusion: `<status>` / `<conclusion>`

Template B — High volume sustained window profile (synthetic peak/valley)

- Date: `YYYY-MM-DD`
  - Change: `S2B-4A/P5-C2-S4S5: evidence window (synthetic peak/valley via sustained window)`
  - Drill: `drill-dual-run`
  - scenario_id: `dual_run/search/window_sustained`
  - Inputs (window_*):
    - window_duration_seconds: `<seconds>`
    - window_interval_seconds: `<seconds>`
    - window_enqueue_batch_size: `<n>`
    - window_max_total_events: `<n>`
    - window_drain_timeout_seconds: `<seconds>`
    - window_worker_max_runtime_seconds: `<seconds>`
  - Run URL: `<url>`
  - status/conclusion: `<status>` / `<conclusion>`
  - Notes: `peak=raise batch/short interval; valley=lower batch/longer interval or pause between runs; interpret via artifacts/summary.json`

Template C — Rollback rehearsal (must do once)

- Date: `YYYY-MM-DD`
  - Change: `S2B-4A/P5-C2-S4S5: rollback rehearsal (Chronicle read switch)`
  - Drill: `drill-verify`
  - scenario_id: `rehearsal_chronicle_read_switch_smoke`
  - Expected: `ok=true; validates MERGED_READ_ENABLED=0 rollback path and MERGED_READ_ENABLED=1 cutover path`
  - Run URL: `<url>`
  - status/conclusion: `<status>` / `<conclusion>`

## P1-C1-S1（Schema/Index Proposal，draft；Chronicle-first）

> 本步只做“提案/边界/索引策略草案”，不做 schema migration。

**Context（来自 runbook/ADR 的事实点）**:

- Chronicle：旧 SoT 为 `chronicle_events`，新投影表为 `chronicle_entries`（runbook）。
- 固定顺序：`Shadow → Dual-run → Cutover(先读后写) → Cleanup`（ADR）。

**Constraints**:

- 不新增第二套入口：仍以 `docs/runbook/run-S2B-projection-table-merge.md` + `drill-write-gate` + `backend/scripts/cli.py` 为单入口。
- 列/索引只承载“稳定、低基数、调度/过滤必需”的字段；避免把每个业务细节都变成索引。

**Minimal schema（draft，先写原则与占位；后续 P1-C2 才落地到 DB）**:

- 必需：能够支撑 claim/reclaim/verify 的调度字段（例如 status + available_at/next_retry_at + owner/lease_until/processing_started_at 等“调度维度”）。
- 必需：能够用于排障与审计的低基数字段（例如 projection / event_type / schema_version / error_reason 的低基数枚举）。
- payload：高基数业务字段放 payload（JSON/文本），只保留 schema_version 之类稳定路由字段上浮。

**Index policy（draft）**:

- P0（必须）：驱动调度/claim/reclaim 的索引（以 status/available_at/lease_until 等调度字段为中心）。
- P1（建议）：排障/聚合索引（例如 projection + event_type）。
- 禁止：为每个临时业务字段随意加索引（需要在本 log 明确“为何必须 + 代价 + 回滚方案”）。

## P1-C1-S2（Rollback / Switch Checklist，no DB change）

> 本步只把“回滚与开关点”写清楚，确保后续切换时是可执行的。

**Read switch（回滚优先级最高）**:

- Chronicle read switch：`MERGED_READ_ENABLED=0/1`（runbook）。
- Search read switch：`SEARCH_MERGED_READ_ENABLED=0/1`（runbook；不复用 Chronicle 的开关）。

**Write switch / runtime control（先停新写侧，再恢复旧 claim）**:

- Worker 一键回滚（Search outbox worker）：`SEARCH_OUTBOX_WORKER_ENABLED=0/1`（runbook）。
- 限速/隔离（用于窗口期风险控制）：`OUTBOX_CONCURRENCY`、`OUTBOX_BULK_SIZE`/`OUTBOX_BATCH_SIZE`（runbook）。

**Rollback sequence（最小可执行顺序，draft）**:

- 先回读：将 read switch 置回旧路径（优先级最高；目标是快速止血）。
- 再停新写：关闭新写侧/worker（若存在），避免继续写入造成状态分叉。
- 再恢复旧 claim：恢复旧 worker/旧 claim 入口（保持单入口，不新增第二套脚本）。

**Cutover guard（进入 cutover 前必须满足）**:

- 固定 write-gate 回归包持续全绿；并且窗口类场景（dual-run window / canary / sampling）可从 artifacts 解释。

## P4-C1-S1（Cleanup ledger：stub/deprecate window + cleanup plan）

> 目标：把“什么时候可以删旧路径/旧表/旧 flag”的边界写清楚；本步不做任何删除，保持回滚优先。

### Stub window（保留旧路径，明确禁用/隔离；可随时回滚）

- 旧 read/write 路径与旧表：保留（不删、不重命名），但在 runbook 中标记为 **stub-only**。
- rollback controls：明确并保留 read switch / worker enable 开关（以“快速止血”为优先级）。
- 观测约束：stub window 内，只接受“回归包持续全绿 + 关键指标无回归”的变更（不引入新语义）。

### Deprecate window（宣布弃用但仍可回滚；观察窗口内验证）

- 进入条件：
  - 连续至少 2 轮固定 write-gate 回归包保持全绿（6/6）。
  - 窗口类演练（dual-run window / sustained window）可解释且无异常回归。
- 行为：
  - 把旧路径在文档中标注为 deprecated（仍保留回滚开关与排障入口）。
  - 把 cleanup 的“删除项”列表化（表/脚本/flag/配置），并声明删除前必须再跑一轮回归包。

### Cleanup（最终删除；需要单独切片与证据）

- 删除前 guard（必须全部满足）：
  - 旧路径在运行时不再被使用（无读/无写/无 worker 实例在跑）。
  - 固定 write-gate 回归包在“当前默认开关组合”下保持全绿（6/6）。
  - 如有问题，能用 artifacts（summary/logs/traces/zip）解释并可回滚。
- 删除动作：必须单独开切片（未来 `P4-C2` 或后续 cycle），并把删除前后的回归证据入账。

## Evidence

固定 write-gate 回归包（6 scenarios）run↔scenario 映射：

- SoT: `artifacts/write_gate_runs.latest.json`

后续每个 Phase 2 里程碑合入后：

- 必须跑一轮固定 write-gate 回归包，并把 run URL + conclusion 记到本 log。

**Evidence (auto/manual)**:

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S1S2: pre-cutover regression (fixed write-gate pack; baseline before cutover default)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385907779`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S1S2: pre-cutover regression (fixed write-gate pack; baseline before cutover default)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385908706`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S1S2: pre-cutover regression (fixed write-gate pack; baseline before cutover default)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385909608`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S1S2: pre-cutover regression (fixed write-gate pack; baseline before cutover default)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385910538`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S1S2: pre-cutover regression (fixed write-gate pack; baseline before cutover default)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385911503`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S1S2: pre-cutover regression (fixed write-gate pack; baseline before cutover default)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385912495`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Conclusion: `Pre-cutover baseline confirmed: fixed write-gate pack is green (6/6).`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S4S5: post-cutover regression (fixed write-gate pack) + SoT update (chronicle default read cutover)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22423951111`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S4S5: post-cutover regression (fixed write-gate pack) + SoT update (chronicle default read cutover)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22423952059`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S4S5: post-cutover regression (fixed write-gate pack) + SoT update (chronicle default read cutover)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22423952934`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S4S5: post-cutover regression (fixed write-gate pack) + SoT update (chronicle default read cutover)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22423953832`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S4S5: post-cutover regression (fixed write-gate pack) + SoT update (chronicle default read cutover)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22423954695`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C1-S4S5: post-cutover regression (fixed write-gate pack) + SoT update (chronicle default read cutover)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22423955489`
  - status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Conclusion: `Post-cutover regression is green: fixed write-gate pack remains green (6/6) and SoT mapping updated.`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C2-S4S5: evidence window round 1/3 (fixed write-gate pack)`
  - Command: `scripts/p1_write_gate_regression.ps1 -Rounds 3 -JitterSecondsMin 30 -JitterSecondsMax 120`
  - Notes: `jitter applied between rounds; cutover default active; rollback available via MERGED_READ_ENABLED=0`
  - Evidence:
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_write_gate` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426204387` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_paging_stability` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426205389` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_shared_keys` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426206283` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_run_window` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426207140` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_canary_dual_write` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426208014` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_write_sampling` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426208987` | status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C2-S4S5: evidence window round 2/3 (fixed write-gate pack)`
  - Command: `scripts/p1_write_gate_regression.ps1 -Rounds 3 -JitterSecondsMin 30 -JitterSecondsMax 120`
  - Notes: `jitter applied between rounds; cutover default active; rollback available via MERGED_READ_ENABLED=0`
  - Evidence:
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_write_gate` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426275462` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_paging_stability` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426276092` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_shared_keys` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426277010` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_run_window` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426277871` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_canary_dual_write` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426278514` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_write_sampling` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426279148` | status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C2-S4S5: evidence window round 3/3 (fixed write-gate pack) + SoT update`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Command: `scripts/p1_write_gate_regression.ps1 -Rounds 3 -JitterSecondsMin 30 -JitterSecondsMax 120`
  - Notes: `jitter applied between rounds; cutover default active; rollback available via MERGED_READ_ENABLED=0`
  - Evidence:
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_write_gate` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426346945` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_search_index_paging_stability` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426347653` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_shared_keys` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426348404` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_run_window` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426349120` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_canary_dual_write` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426349884` | status/conclusion: `completed / success`
    - Drill: `drill-write-gate` | scenario_id: `shadow_verify_dual_write_sampling` | Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426350657` | status/conclusion: `completed / success`

- Date: `2026-02-26`
  - Change: `S2B-4A/P5-C2-S4S5: evidence window (synthetic peak/valley via sustained window)`
  - Drill: `drill-dual-run`
  - scenario_id: `dual_run/search/window_sustained`
  - Inputs (window_*):
    - window_duration_seconds: `900`
    - window_interval_seconds: `1`
    - window_enqueue_batch_size: `20`
    - window_max_total_events: `10000`
    - window_drain_timeout_seconds: `1800`
    - window_worker_max_runtime_seconds: `2400`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22426587311`
  - status/conclusion: `completed / success`
  - Notes: `runtime ~10m (03:29:47Z → 03:40:02Z); batch_size=20 to respect pg_candidates_total gate`

- Date: `2026-02-24`
  - Change: `S2B-4A/P5-C2-S4S5: rollback rehearsal (Chronicle read switch)`
  - Drill: `drill-verify`
  - scenario_id: `rehearsal_chronicle_read_switch_smoke`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22346672508`
  - status/conclusion: `completed / success`
  - Notes: `single run covers MERGED_READ_ENABLED=0/1 paths; validates rollback entrypoint stays viable`

- Date: `2026-02-24`
  - Change: `S2B-4A/P0-C1-S1S2: Phase 2 baseline (fixed write-gate regression pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22342770561`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P0-C1-S1S2: Phase 2 baseline (fixed write-gate regression pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22342771898`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P0-C1-S1S2: Phase 2 baseline (fixed write-gate regression pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22342773217`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P0-C1-S1S2: Phase 2 baseline (fixed write-gate regression pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22342774605`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P0-C1-S1S2: Phase 2 baseline (fixed write-gate regression pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22342775901`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P0-C1-S1S2: Phase 2 baseline (fixed write-gate regression pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22342777244`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Conclusion: `Phase 2 baseline established: fixed write-gate regression pack is green (6/6).`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C1-S3S4: regression after P1-C1-S1S2 (doc-only; no DB change)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343172034`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C1-S3S4: regression after P1-C1-S1S2 (doc-only; no DB change)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343173297`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C1-S3S4: regression after P1-C1-S1S2 (doc-only; no DB change)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343174538`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C1-S3S4: regression after P1-C1-S1S2 (doc-only; no DB change)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343175716`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C1-S3S4: regression after P1-C1-S1S2 (doc-only; no DB change)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343176964`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C1-S3S4: regression after P1-C1-S1S2 (doc-only; no DB change)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343178160`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Conclusion: `P1-C1 doc-only change is regression-safe: fixed write-gate pack remains green (6/6).`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C2-S3S4: regression after P1-C2-S1S2 (DB schema/index only; chronicle_entries envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343576888`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C2-S3S4: regression after P1-C2-S1S2 (DB schema/index only; chronicle_entries envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343578338`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C2-S3S4: regression after P1-C2-S1S2 (DB schema/index only; chronicle_entries envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343579719`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C2-S3S4: regression after P1-C2-S1S2 (DB schema/index only; chronicle_entries envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343581138`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C2-S3S4: regression after P1-C2-S1S2 (DB schema/index only; chronicle_entries envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343582517`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P1-C2-S3S4: regression after P1-C2-S1S2 (DB schema/index only; chronicle_entries envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343584015`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Conclusion: `P1-C2 schema/index change is regression-safe: fixed write-gate pack remains green (6/6).`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C1-S3S4: regression after P2-C1-S1S2 (backfill prep: rebuild+worker fill envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343953408`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C1-S3S4: regression after P2-C1-S1S2 (backfill prep: rebuild+worker fill envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343954915`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C1-S3S4: regression after P2-C1-S1S2 (backfill prep: rebuild+worker fill envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343956163`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C1-S3S4: regression after P2-C1-S1S2 (backfill prep: rebuild+worker fill envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343957387`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C1-S3S4: regression after P2-C1-S1S2 (backfill prep: rebuild+worker fill envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343958622`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C1-S3S4: regression after P2-C1-S1S2 (backfill prep: rebuild+worker fill envelope columns)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22343959943`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Conclusion: `P2-C1 backfill-prep change is regression-safe: fixed write-gate pack remains green (6/6).`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C2-S1S2: backfill rehearsal (dry-run/small window; payload-first chronicle envelope extraction)`
  - Drill: `drill-verify`
  - scenario_id: `rehearsal/chronicle/envelope_backfill_small_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22345362340`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C2-S3S4: regression after P2-C2-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22345558614`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C2-S3S4: regression after P2-C2-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22345560550`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C2-S3S4: regression after P2-C2-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22345562343`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C2-S3S4: regression after P2-C2-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22345564130`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C2-S3S4: regression after P2-C2-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22345565700`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P2-C2-S3S4: regression after P2-C2-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22345567547`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Conclusion: `P2-C2 rehearsal + regression is green: drill-verify passed and fixed write-gate pack remains green (6/6).`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C1-S1S2: chronicle read switch smoke rehearsal (MERGED_READ_ENABLED=0/1)`
  - Drill: `drill-verify`
  - scenario_id: `rehearsal/chronicle/read_switch_smoke`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22346672508`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C1-S3S4: regression after P3-C1-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22346836914`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C1-S3S4: regression after P3-C1-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22346841164`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C1-S3S4: regression after P3-C1-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22346844858`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C1-S3S4: regression after P3-C1-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22346848468`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C1-S3S4: regression after P3-C1-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22346852269`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C1-S3S4: regression after P3-C1-S1S2 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22346856122`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Conclusion: `P3-C1 rehearsal + regression is green: drill-verify passed and fixed write-gate pack remains green (6/6).`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C2-S1S2: search read switch smoke rehearsal (SEARCH_MERGED_READ_ENABLED=0/1 provider selection)`
  - Drill: `drill-verify`
  - scenario_id: `rehearsal/search/read_switch_smoke`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22348268347`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C2-S3S4: search write cutover window (sustained enqueue + outbox drain + ES index)`
  - Drill: `drill-dual-run`
  - scenario_id: `dual_run/search/window_sustained`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22348148713`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C2-S5S6: regression after P3-C2-S1S2S3S4 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22348545688`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C2-S5S6: regression after P3-C2-S1S2S3S4 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22348549773`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C2-S5S6: regression after P3-C2-S1S2S3S4 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22348553869`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C2-S5S6: regression after P3-C2-S1S2S3S4 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22348558358`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C2-S5S6: regression after P3-C2-S1S2S3S4 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22348562380`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P3-C2-S5S6: regression after P3-C2-S1S2S3S4 (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22348566572`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Conclusion: `P3-C2 rehearsal/window + regression is green: drill-verify + drill-dual-run passed and fixed write-gate pack remains green (6/6).`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C1-S3S4: doc-only cleanup ledger regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354111598`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C1-S3S4: doc-only cleanup ledger regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354116129`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C1-S3S4: doc-only cleanup ledger regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354120792`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C1-S3S4: doc-only cleanup ledger regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354125424`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C1-S3S4: doc-only cleanup ledger regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354129996`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C1-S3S4: doc-only cleanup ledger regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354134571`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Conclusion: `P4-C1 doc-only cleanup ledger is regression-safe: fixed write-gate pack remains green (6/6).`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354734132`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354735894`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354737573`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354739144`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354740818`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354742553`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Conclusion: `P4-C2 pre-cleanup regression is green: fixed write-gate pack remains green (6/6).`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S3: cleanup - delete legacy tracked write-gate snapshots (keep latest SoT only)`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354858653`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354860537`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354862346`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354864440`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354866085`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Change: `S2B-4A/P4-C2-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22354867629`
  - status/conclusion: `completed / success`

- Date: `2026-02-24`
  - Conclusion: `P4-C2 post-cleanup regression is green: cleanup is regression-safe and fixed write-gate pack remains green (6/6).`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22377902365`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22377903257`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22377904316`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22377905240`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22377906221`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22377907168`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Conclusion: `P4-C3 pre-cleanup regression is green: fixed write-gate pack remains green (6/6).`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S3: cleanup - remove unused Search ops worker shim (use stable entrypoint)`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22378693742`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22378694617`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22378695629`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22378696619`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22378697373`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C3-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22378698264`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Conclusion: `P4-C3 post-cleanup regression is green: cleanup is regression-safe and fixed write-gate pack remains green (6/6).`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379012003`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379012781`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379013702`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379014527`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379015431`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379016377`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Conclusion: `P4-C4 pre-cleanup regression is green: fixed write-gate pack remains green (6/6).`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S3: cleanup - restore stable chronicle worker/replay entrypoints (scripts/) and retire ops worker shim`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379096518`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379097306`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379098396`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379099328`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379100296`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C4-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22379101188`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Conclusion: `P4-C4 post-cleanup regression is green: cleanup is regression-safe and fixed write-gate pack remains green (6/6).`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383114394`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383115286`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383116183`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383117088`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383117991`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383118870`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Conclusion: `P4-C5 pre-cleanup regression is green: fixed write-gate pack remains green (6/6).`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S3: cleanup - add missing stable search replay entrypoint (scripts/)`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383188397`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383189251`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383190116`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383190948`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383191760`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C5-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22383192478`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Conclusion: `P4-C5 post-cleanup regression is green: cleanup is regression-safe and fixed write-gate pack remains green (6/6).`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385780473`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385781471`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385782379`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385783372`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385784515`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S1S2: pre-cleanup regression (fixed write-gate pack)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385785603`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Conclusion: `P4-C6 pre-cleanup regression is green: fixed write-gate pack remains green (6/6).`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S3: cleanup - make ops replay shims forward canonical stable entrypoints (scripts/)`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385907779`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385908706`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385909608`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385910538`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385911503`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Change: `S2B-4A/P4-C6-S4S5: post-cleanup regression (fixed write-gate pack)`
  - SoT: `artifacts/write_gate_runs.latest.json`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22385912495`
  - status/conclusion: `completed / success`

- Date: `2026-02-25`
  - Conclusion: `P4-C6 post-cleanup regression is green: cleanup is regression-safe and fixed write-gate pack remains green (6/6).`

## References

- `docs/adr/adr-S2B-projection-table-merge.md`
- `docs/runbook/run-S2B-projection-table-merge.md`
- `docs/logs/log-S2B-projection-table-merge.md`
- `docs/logs/log-S2B-3A-unified-consumer-framework.md`
