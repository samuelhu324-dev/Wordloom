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
**updated**: `2026-02-24`

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

> Cycle 约定：若同一组步骤需要重复一轮（回归重跑/补证据/修正后再跑），在 step 前加 cycle，例如 `P1-C2-S3`；若多个 step 一起提交，可合并写成 `P1-C2-S1S2`。

## Execution Checklist（可执行清单 / checked）

### P0（baseline）

- [x] `P0-C1-S1S2`：固定 write-gate 回归包 baseline 已完成，并已在 Evidence 入账（6/6 success）。

## Evidence

固定 write-gate 回归包（6 scenarios）run↔scenario 映射：

- SoT: `artifacts/write_gate_runs.latest.json`

后续每个 Phase 2 里程碑合入后：

- 必须跑一轮固定 write-gate 回归包，并把 run URL + conclusion 记到本 log。

**Evidence (auto/manual)**:

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

## References

- `docs/adr/adr-S2B-projection-table-merge.md`
- `docs/runbook/run-S2B-projection-table-merge.md`
- `docs/logs/log-S2B-projection-table-merge.md`
- `docs/logs/log-S2B-3A-unified-consumer-framework.md`
