# Log-S2B-3A: extraction/unified consumer framework（outbox_core）

---

**id**: `S2B-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `extraction/unified consumer framework (outbox_core extraction & rollout)`
**status**: `draft`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Projection, Outbox, Worker, epic/s2, sub/3`
**links**: ``
  **issue**: `#119`
  **pr**: ``
  **adr**: `docs/adr/adr-S2B-projection-table-merge.md`
  **runbook**: `docs/runbook/run-S2B-projection-table-merge.md`
**created**: `2026-02-23`
**updated**: `2026-02-23`

---

## Decision / Outcome（结论区）

**Decision**:

- （draft）将 Search/Chronicle 两条 projection 的 worker/daemon 共性能力，从脚本/legacy 实现中抽成可复用的 `backend/infra/outbox_core`，作为 Phase 1（unified consumer framework）的代码落地。
- （draft）对外稳定面仍以 Failure Contract v1/v2 为准：稳定入口（CLI/runbook）、稳定证据链（artifacts）、稳定共享键（logs/metrics/traces）。

**Non-goals**:

- 本 log 不直接推进“表结构合并（table merge）”；Phase 2 单独记账。
- 不新增第二套入口（不引入新的脚本路径/新 runbook 分叉）；仅在既有入口内替换/下沉实现。

## Background

S2B-1A / S2B-2A 已经把 Failure Contract（证据链 + 可切写口径 + dual-run/cutover closure）作为稳定对外接口跑通。
但当前 worker/daemon 的核心行为（claim/retry/backoff/stuck reclaim/DLQ/replay）仍主要散落在脚本与 legacy 实现中，导致“新增一个 projection / 迁移一个 worker”仍容易复制粘贴与语义漂移。

## Problem / Malfunction

- 核心消费语义分散：Search/Chronicle 容易出现状态机、重试、stuck 判定、指标口径不一致。
- 运维资产难复用：同类告警/看板/排障链路容易按 projection 分裂。
- Phase 2（table merge）风险过高：如果 Phase 1 的框架能力没先统一，合表只会把分裂放大。

## Success criteria（DoD）

- `backend/infra/outbox_core` 至少覆盖：
  - claim/lease/reclaim（含 stuck reclaim predicate）
  - retry/backoff/jitter（含 deterministic vs transient 的 reason 分类约束）
  - DLQ + replay 入口（由既有 CLI/runbook 调用）
- Search/Chronicle 的 worker/daemon 在不改变外部入口的情况下，迁移到同一套 outbox_core 语义与指标口径。
- Failure Contract v2 的 drills 继续全绿，并且 artifacts/共享键证据链不变。

## Implementation Status

- 已存在的 outbox_core 基础：`backend/infra/outbox_core/stuck.py`
- S1（取边界 / 纯重构，Search 先接入）已抽取并接入：
  - `backend/infra/outbox_core/lease.py`：`lease_until` / `renew_lease`（统一 lease 续约与更新口径）
  - `backend/infra/outbox_core/sanitize.py`：`sanitize_terminal_rows`（统一“terminal rows 不得残留 owner/lease”不变量）
  - `backend/infra/outbox_core/reclaim.py`：`reclaim_stuck_processing`（统一 stuck reclaim，复用 `stuck_processing_predicate`）
  - `backend/infra/outbox_core/claim.py`：`claim_pending_batch`（统一 claim：`FOR UPDATE SKIP LOCKED` + break-atomicity 实验开关）
  - `backend/infra/outbox_core/retry.py`：`compute_exponential_backoff_seconds` / `compute_next_retry_at`（统一 backoff 计算入口；用参数保持各 worker 既有公式）
  - `backend/infra/outbox_core/reasons.py`：`is_transient_reason` +（Search）ES/HTTPX reason 分类 helper（低基数 reason 字符串保持不变）
  - Search legacy worker 已改为调用上述 helper（入口/行为不变）：`backend/scripts/legacy/search_outbox_worker.py`
- Chronicle legacy worker 已开始接入 outbox_core（纯重构，不改入口/行为）：
  - claim：已切到 `outbox_core.claim.claim_pending_batch`（排序/提交点保持一致）：`backend/scripts/legacy/chronicle_outbox_worker.py`
  - reclaim：已切到 `outbox_core.reclaim.reclaim_stuck_processing`（并清理 `next_retry_at=None` 以保持原语义）：`backend/scripts/legacy/chronicle_outbox_worker.py`
- Search 稳定入口保持不变（Procfile/runbook/肌肉记忆不动）：`backend/scripts/search_outbox_worker.py` → `backend/scripts/legacy/search_outbox_worker.py`
- 已完成的 Failure Contract：
  - v1：`docs/logs/log-S2B-1A-failure-contract-v1.md`
  - v2：`docs/logs/log-S2B-2A-failure-contract-v2.md`

## Plan（draft）

### S1 范围边界（draft，Search-first）

- 目标：先把“可复用且投影无关”的 outbox 行为抽成最小边界（outbox_core），Search 先接入验证回归链路，做到“只抽取不改行为”。
- 已收口到 outbox_core 的语义：
  - terminal sanitize（done/failed/processed_at 的 owner/lease 清理不变量）
  - stuck reclaim（lease expiry / max processing exceeded）
  - lease renew / lease_until
  - claim_batch（`SELECT ... FOR UPDATE SKIP LOCKED` + break-atomicity 实验开关）
  - retry/backoff（先收口 backoff/next_retry_at 计算入口；reason 分类仍以“低基数集合 + 各 worker 保持既有字符串/口径”为主）
- 暂不在 S1 里做的内容（避免语义漂移）：
  - metrics schema 的统一（先不改 labels/名称，避免观测断链）

### Step 切片（建议开工顺序，供记账）

> 注：这是“可循环”的步骤命名法。若发生第二轮/第三轮迭代，可在 step 前加 cycle 标记（例如 `P0-C2-S1`）。

- S0（基线证据）：不改代码，手动触发一组核心 drills（例如 `drill-write-gate` 的 dual-run/window、canary dual-write），把 run URL + conclusion 记到 Evidence。
- S1（抽取最小 outbox_core 契约，不改行为）：从现有 worker 里抽“纯逻辑/纯语义”的共性到 `backend/infra/outbox_core`（先以 `stuck.py` 为基石继续扩展），目标是“代码位置变了但行为不变”。
- S2（Search 迁移到 outbox_core）：把 Search outbox worker 的 claim/lease/reclaim/retry 等继续迁移到 outbox_core，但稳定入口保持不变（shim 继续复用），优先只动 `backend/scripts/legacy/search_outbox_worker.py` 的实现落点。
- S3（回归 + 证据）：重复 S0 的 drills，把新的 run URL + conclusion 追加到 Evidence；若出现差异，用 artifacts 定位并修复，直到“入口不变、证据链不变、语义不漂”。

## Execution Checklist（可执行清单 + 可验收字段）

> 目标：把 Phase 1 做成“可验收的代码收口”，并且在不改变外部入口/证据链的前提下完成迁移。

### P0（必须）：Phase 1 收口到 outbox_core（可复用消费框架）

**P0.DoD（验收字段）**：

- [x] `backend/infra/outbox_core` 形成最小“消费框架契约”（可复用 API/语义），至少包含：
  - [x] claim/lease（设置 owner/lease_until/processing_started_at）
  - [x] reclaim（stuck reclaim：基于 lease_until + processing_started_at 的统一判定；已存在 `stuck_processing_predicate` 视为基石）
  - [x] retry/backoff/jitter（同一套重试策略与上限，不再在不同 worker 中各写一份）
  - [x] failure reason 低基数约束（deterministic vs transient 的 reason 分类可枚举/可聚合）
  - [x] DLQ + replay（ops/CLI/runbook 入口不变，内部逻辑收口到 outbox_core）
- [x] Search 与 Chronicle 的 worker/daemon（至少 1 条链路先落地）切换为调用 outbox_core 的实现，但外部入口保持不变：
  - [x] workflow / runbook / CLI 仍然只引用既有稳定入口（不新增第二套脚本路径）
  - [x] artifacts contract 不变（summary.json / failure zip / `_result.json` 仍是 SoT）
- [x] metrics/shared keys 口径可复用（至少对同类指标/标签做到“可比对、可聚合、不爆炸”）：
  - [x] 关键 label 集合稳定（projection/op/reason 等）
  - [x] shared keys（如 run_id/library_id/outbox_event_id/entity_id）在 logs/metrics/traces 中可互证

#### 下一轮切分：P0-C2-S2S3（DLQ/replay 收口 + 回归证据）

> 目标：把“replay terminal failed rows → pending”的公共语义抽到 `outbox_core`，并保持既有稳定入口不变；随后用同一组 write-gate drills 产出新一轮证据。

**S2（Implementation）**：

- [x] 新增 `backend/infra/outbox_core/replay.py`（或同名模块）：提供“replay failed → pending + audit fields”的可复用 helper
  - [x] 能覆盖 Search/Chronicle 两个 outbox 表的共同字段：`status/owner/lease_until/processing_started_at/attempts/next_retry_at/error_reason/error/replay_count/last_replayed_*/updated_at`
  - [x] 支持 filter：`entity_type`、`since_hours`；并支持可选 `ids`（Chronicle 已有该能力）
  - [x] 支持 `limit` 与 `dry_run`（保持当前脚本 UX）
- [x] 重构 replay 工具的 legacy 实现为“薄壳”调用 outbox_core（稳定入口保持不变）：
  - [x] `backend/scripts/legacy/search_outbox_replay_failed.py`
  - [x] `backend/scripts/legacy/chronicle_outbox_replay_failed.py`
  - [x] `backend/scripts/ops/search_outbox_replay_failed.py` 与 `backend/scripts/ops/chronicle_outbox_replay_failed.py` 不改路径/参数
- [ ] （可选但推荐）在 replay helper 中复用/对齐 `sanitize_terminal_rows` 的不变量（replay 也要清 owner/lease/processing_started_at 等）

**S3（Evidence）**：

- [x] 触发与 S0/S3 相同的一组 write-gate drills（见 Evidence：run_id=22308739330..22308752185）
- [x] 在 Evidence 追加新条目：
  - Change 建议用：`S2B-3A/P0-C2-S2S3: extract replay helpers into outbox_core (commit <sha>)`
  - 粘贴 run URL + conclusion（6 个 scenario）

**P0.Verification（如何验证）**：

- [ ] 现有 drills 不需要改操作入口即可继续运行（重点是 `drill-write-gate` 的 dual-run/window 与 canary dual-write）。
- [ ] 选一个“最小迁移面”的 worker 先切（建议 Search outbox worker），确保回滚路径存在（shim/feature flag 或保持旧实现可切回）。

### P1（必须）：回归验证与证据链（防语义漂移）

**P1.DoD（验收字段）**：

- [ ] 选择一组“必须全绿”的回归 drills（建议至少覆盖）：
  - [ ] write-gate：幂等/唯一性（1A）
  - [ ] paging stability + shared keys（2A）
  - [ ] dual-run stage2 / sustained window（2A）
  - [ ] canary dual-write + sampling sustained dual-write（2A）
- [ ] 每次触发都在本 log 的 Evidence 区追加 run URL，并在完成后补齐 conclusion（success/failure）。
- [ ] 若出现 failure：必须能从 artifacts（summary/logs/traces/zip）定位原因，并在 Evidence 备注里写明“原因 + 处置”。

### P2（建议/后置）：Phase 2（table merge）开工门槛（何时新开 log）

**P2.Gate（开工门槛 / 可验收字段）**：

- [ ] Phase 1（P0）完成后，在一段窗口内（例如连续多次 drills + 手动演练）没有出现“语义漂移/指标不可比/排障断链”。
- [ ] runbook 入口与 replay/DLQ 语义保持稳定（不需要按 projection 分裂两套操作手册）。
- [ ] 满足门槛后，再新开 Phase 2 log（建议命名：`log-S2B-4A-table-merge-migration.md`）专门追踪 schema/migration/backfill/rollback。

## Evidence

> 使用方式：每次 P0 里程碑变更合入后，跑一组 P1 drills，把 run URL 粘贴到这里；完成后补 conclusion。

**Evidence (auto/manual)**:

- Date: `YYYY-MM-DD`
  - Change: `S2B-3A/P0[-C<n>]-S<step>: ...` / `commit ...` / `ref ...`
  - Drill: `drill-write-gate` / `drill-shadow-verify-entries` / ...
  - scenario_id: `...`
  - Run URL: `https://github.com/<org>/<repo>/actions/runs/<id>`
  - status/conclusion: `completed / success|failure`
  - Notes: `what it proves; if failure -> root cause + fix`

S0（Search baseline / before P0 changes）：

- Date: `2026-02-23`
  - Change: `S0 baseline evidence (no code changes)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22301350604`
  - status/conclusion: `completed / success`
  - Notes: `Baseline: write-gate idempotency/uniqueness gate is green.`

- Date: `2026-02-23`
  - Change: `S0 baseline evidence (no code changes)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22301356404`
  - status/conclusion: `completed / success`
  - Notes: `Baseline: paging stability gate is green.`

- Date: `2026-02-23`
  - Change: `S0 baseline evidence (no code changes)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22301361750`
  - status/conclusion: `completed / success`
  - Notes: `Baseline: shared keys evidence bundle is green.`

- Date: `2026-02-23`
  - Change: `S0 baseline evidence (no code changes)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22301371033`
  - status/conclusion: `completed / success`
  - Notes: `Baseline: sustained dual-run window parity is green.`

- Date: `2026-02-23`
  - Change: `S0 baseline evidence (no code changes)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22301379799`
  - status/conclusion: `completed / success`
  - Notes: `Baseline: canary dual-write + cleanup is green.`

- Date: `2026-02-23`
  - Change: `S0 baseline evidence (no code changes)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22301385240`
  - status/conclusion: `completed / success`
  - Notes: `Baseline: sustained dual-write sampling parity is green.`

S3（Regression evidence / after S1 extraction on S2B-3A）：

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-S1 (commit 3258e06e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22306069159`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S1): write-gate idempotency/uniqueness gate remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-S1 (commit 3258e06e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22306070870`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S1): paging stability gate remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-S1 (commit 3258e06e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22306072595`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S1): shared keys evidence bundle remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-S1 (commit 3258e06e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22306074556`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S1): sustained dual-run window parity remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-S1 (commit 3258e06e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22306076437`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S1): canary dual-write + cleanup remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-S1 (commit 3258e06e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22306078507`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S1): sustained dual-write sampling parity remains green.`

S3（Regression evidence / after P0-C2-S2S3 on S2B-3A）：

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C2-S2S3 (commit cb7d0d58)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22308739330`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S2S3): write-gate idempotency/uniqueness gate remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C2-S2S3 (commit cb7d0d58)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22308741945`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S2S3): paging stability gate remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C2-S2S3 (commit cb7d0d58)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22308744260`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S2S3): shared keys evidence bundle remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C2-S2S3 (commit cb7d0d58)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22308746786`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S2S3): sustained dual-run window parity remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C2-S2S3 (commit cb7d0d58)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22308749501`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S2S3): canary dual-write + cleanup remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C2-S2S3 (commit cb7d0d58)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22308752185`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after S2S3): sustained dual-write sampling parity remains green.`

S3（Regression evidence / after P0-C3-S2 on S2B-3A）：

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C3-S2 (commit ee3d001e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_write_gate`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22310188227`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after P0-C3-S2): write-gate idempotency/uniqueness gate remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C3-S2 (commit ee3d001e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_search_index_paging_stability`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22310191418`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after P0-C3-S2): paging stability gate remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C3-S2 (commit ee3d001e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_shared_keys`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22310163509`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after P0-C3-S2): shared keys evidence bundle remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C3-S2 (commit ee3d001e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_run_window`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22310194207`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after P0-C3-S2): sustained dual-run window parity remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C3-S2 (commit ee3d001e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_canary_dual_write`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22310197235`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after P0-C3-S2): canary dual-write + cleanup remains green.`

- Date: `2026-02-23`
  - Change: `S2B-3A/P0-C3-S2 (commit ee3d001e)`
  - Drill: `drill-write-gate`
  - scenario_id: `shadow_verify_dual_write_sampling`
  - Run URL: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/22310199997`
  - status/conclusion: `completed / success`
  - Notes: `S3 regression (after P0-C3-S2): sustained dual-write sampling parity remains green.`

## References

- `docs/logs/log-S2B-projection-table-merge.md`
- `docs/logs/log-S2B-1A-failure-contract-v1.md`
- `docs/logs/log-S2B-2A-failure-contract-v2.md`
- `docs/logs/log-S3A-2A-2B-daemon-ready-worker-migration.md`
