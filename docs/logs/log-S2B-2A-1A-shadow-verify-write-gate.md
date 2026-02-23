# Log-S2B-2A-1A: idempotency/shadow verify → write-gate

---

**id**: `S2B-2A-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `idempotency/shadow verify → write-gate`
**status**: `stable`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Projection, Search, Chronicle, sub/2`
**links**: ``
  **issue**: `#56, #64, #65`
  **pr**: ``
  **adr**: ``
  **runbook**: `docs/runbook/run-S2B-projection-table-merge.md`
**created**: `2026-02-18`
**updated**: `2026-02-23`

---

## Decision / Outcome（结论区）

**Decision**:

- 将 v2 的第一阶段（1A）定义为“把 shadow verify 升级到可切写准入门槛（write-gate）的第一刀”：先落地 **幂等与唯一性** 口径，并以统一 artifacts 证据链输出。
- write-gate 的入口必须稳定且唯一：在 CI 与手动运行中都以 `backend/scripts/cli.py labs ...` 为准，避免 workflow/脚本入口分叉造成语义不一致。
- 本阶段只做 **验证与证据**（verify + artifacts），不引入 dual-run 写侧并行，不改变生产写路径。

**Drivers**:

- v1 的 counts/missing/extra 足以做早期对比，但不足以支撑切写；写侧风险首先体现在“重复投递/重复副作用”。
- 先把“入口稳定 + 幂等证据”做实，可以在不引入新系统的前提下，把 cutover 风险从“感觉”变成“门槛”。

**Non-goals**:

- 不在 1A 内实现 Dual-run（写侧影子并行）与 Write switch。
- 不在 1A 内处理排序/分页稳定性与可观测共享键一致（这两项在 1B 处理，见下方注释）。
- 不在 1A 内决定最终“合表/合 projection”的 schema 形态。

**Success criteria（DoD）**:

- Search shadow verify 具备“幂等与唯一性”证据字段，并在 mismatch 时以非 0 退出：
  - 至少覆盖 `search_index` 内的 `(entity_type, entity_id)` 唯一性（不允许多行）
  - 至少覆盖“同一实体的重复变更信号”（例如重复 outbox 投递导致的重复版本/重复写入痕迹，具体字段以现有 schema 可表达为准）
- Chronicle/Search 的 drill 入口一致：
  - `python backend/scripts/cli.py labs shadow-verify-chronicle-entries ...`
  - `python backend/scripts/cli.py labs shadow-verify-search-index ...`
- artifacts contract 不变：产出 `artifacts/summary.json`（来自 `_result.json`），失败上传 zip 并 fail job。

**Current status（现状）**:

- ✅ workflow 已强制统一入口为 CLI（不允许改走 lab 脚本），确保 scenario 执行路径不分叉：`.github/workflows/drill-shadow-verify-entries.yml`
- ✅ Search/Chronicle CLI 命令已存在并可用：`backend/scripts/cli.py`（`labs shadow-verify-chronicle-entries` / `labs shadow-verify-search-index`）
- ✅ 已新增 write-gate 专用入口与证据字段：`backend/scripts/cli.py`（`labs shadow-verify-search-index-write-gate`）+ `docs/labs/lab-S2B-2A-1A-shadow-verify-write-gate.md`
- ✅ CI 已跑通 write-gate drill（`drill-write-gate` 手动触发，2026-02-18，run #1，约 36s）。
- ✅ 本地已连续运行 write-gate 5 次并落盘快照（2026-02-18）：
  - `20260218T185230-wg-run1`
  - `20260218T185231-wg-run2`
  - `20260218T185232-wg-run3`
  - `20260218T185233-wg-run4`
  - `20260218T185234-wg-run5`

**Evidence（代码证据 / 入口证据）**:

- Actions workflow（scenario，统一入口）：`.github/workflows/drill-shadow-verify-entries.yml`
- Write-gate workflow（write-gate 专用 drill）：`.github/workflows/drill-write-gate.yml`
- Search shadow verify（stable CLI）：`backend/scripts/cli.py`（`labs shadow-verify-search-index`）
- Chronicle shadow verify（stable CLI）：`backend/scripts/cli.py`（`labs shadow-verify-chronicle-entries`）
- Write-gate lab manual：`docs/labs/lab-S2B-2A-1A-shadow-verify-write-gate.md`
- Write-gate stable CLI：`backend/scripts/cli.py`（`labs shadow-verify-search-index-write-gate`）

**Acceptance checklist（验收清单）**:

- [x] Search `_result.json` 增加幂等/唯一性字段（例如 duplicates 统计）
- [x] `ok` 判定纳入幂等/唯一性（duplicates==0）
- [x] CI workflow 运行 Search scenario 时，summary/zip 证据链可重复获得
- [x] 文档/Runbook 引用的入口命令不再出现脚本入口分叉

**Closure（收尾）**:

- 本子 log 的 DoD 已满足，当前标记为 `stable`。
- 后续增量（排序/分页稳定性、共享键一致性、dual-run/cutover/cleanup）按 v2 路线在 `S2B-2A` 的后续子 log 中推进。

## Background

v2 的目标是把“切写级别”的风险用证据链收敛。最先需要被工程化的风险是：重复投递导致的重复副作用。

## Problem / Malfunction

- Dual-run/Write switch 前，如果无法证明“重复投递不会造成重复副作用”，并行运行会把系统打成筛子。
- 若 workflow 在“CLI 命令缺失时自动改走脚本”，则同一 scenario 会出现两套语义与两份证据链，无法作为稳定契约。

## What/How to do（落地规则）

### 1) 入口稳定：workflow 只调用 CLI

- 所有 drill scenario 都应调用 `backend/scripts/cli.py labs ...`，并将 `_result.json` 写入 `.drill_snapshot`。

### 2) 幂等与唯一性：最小可行检查（Search）

- 在 `shadow-verify-search-index` 的结果中加入以下最小证据字段（字段名可按实际实现调整，但语义要固定）：
  - `duplicates_entity_rows`: `COUNT(*)` of rows where `(entity_type, entity_id)` 出现多于 1 行
  - （可选）`duplicates_by_entity_type`: 分 entity_type 计数，用于定位
- `ok` 判定必须包含 `duplicates_entity_rows == 0`。

> 注释（下一阶段 2A 要做的点）
>
>- 排序/分页稳定性：定义稳定排序键 + 游标翻页协议，并对比多页窗口的一致性
>- 可观测共享键一致：将 `run_id/library_id/outbox_event_id/entity_id` 等 key 串联到 logs/metrics/traces 的可查询证据
>- Dual-run/Write switch：在满足 write-gate 后再推进

## Next

- 落地 Search 的幂等/唯一性 write-gate 校验（先最小 SQL 统计 + 纳入 `ok`）。
- 在父 log `S2B-2A` 中，将本子 log 与 1B 子 log 作为 v2 的“收工拆分”依据。

## References

- `docs/logs/log-S2B-2A-failure-contract-v2.md`（v2 总纲）
- `docs/logs/log-S2B-1A-failure-contract-v1.md`（v1 契约样板）
- `docs/runbook/run-S2B-projection-table-merge.md`（合表/合 projection 上下文）
