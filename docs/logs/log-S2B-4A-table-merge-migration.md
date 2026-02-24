# Log-S2B-4A: table merge migration（Phase 2：schema/migration/backfill/rollback）

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

- Phase 1（unified consumer framework / outbox_core）已完成并具备固定回归包（P1），因此进入 Phase 2：table merge migration 的推进与记账。
- 本 log 只记录 Phase 2 的 schema/migration/backfill/rollback/cutover；Phase 1 的框架演进仍以 `S2B-3A` 为 SoT。

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
  - cutover 前：P1 固定回归包持续全绿（write-gate 6 scenarios）
  - cutover 后：同一回归包持续全绿，并且出现问题时可从 artifacts 定位原因。

## Plan（draft）

> 注：延续 Step/Cycle 命名法；每个切片都必须闭环：Implementation → Regression (P1) → Evidence。

- S0（门槛确认）：引用 Phase 1 的固定回归包与近期全绿证据，确认可以进入 Phase 2。
- S1（schema/index 准备）：整理/实现 schema 变更与索引策略（不触碰入口；保持可回滚）。
- S2（migration/backfill 演练）：定义 backfill 幂等脚本与窗口；确保失败语义与 replay/runbook 可用。
- S3（cutover + 窗口观察）：按 runbook 顺序推进 cutover，跑 P1 回归包并入账；窗口内异常必须可解释可回退。
- S4（cleanup ledger）：记录 stub/deprecate window 与清理计划（不提前删旧路径）。

## Evidence

P1 固定回归包（write-gate 6 scenarios）run↔scenario 映射：

- SoT: `artifacts/write_gate_runs.latest.json`

后续每个 Phase 2 里程碑合入后：

- 必须跑一轮 P1 固定回归包，并把 run URL + conclusion 记到本 log。

## References

- `docs/adr/adr-S2B-projection-table-merge.md`
- `docs/runbook/run-S2B-projection-table-merge.md`
- `docs/logs/log-S2B-projection-table-merge.md`
- `docs/logs/log-S2B-3A-unified-consumer-framework.md`
