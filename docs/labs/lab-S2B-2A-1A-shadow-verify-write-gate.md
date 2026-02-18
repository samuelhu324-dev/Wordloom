# Lab-S2B-2A-1A：shadow verify write-gate（idempotency/uniqueness）

---

**id**: `S2B-2A-1A`
**kind**: `lab`               # log | lab | runbook | adr | note
**title**: `shadow verify write-gate (idempotency/uniqueness)`
**status**: `draft`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Projection, Search, Chronicle, sub/2`
**links**: ``
  **issue**: `#64, #65`
  **pr**: ``
  **adr**: ``
  **runbook**: `docs/runbook/run-S2B-projection-table-merge.md`
**created**: `2026-02-18`
**updated**: `2026-02-18`

---

目标：把 v2 的第一刀（write-gate）落成可复验证据：

- 在不引入 dual-run、不改写路径的前提下
- 将 shadow verify 从“counts/missing/extra”升级出 **幂等与唯一性** 的准入门槛
- 并且保持证据链与入口稳定（CLI + `_result.json` + exit code）

本 lab 以 Postgres 侧投影为对账对象：

- 投影表：`search_index`
- 本阶段只做 **唯一性**（防止重复副作用的最小代理指标）

---

## 0) 前置条件

- 有可用 Postgres（本地/容器均可）
- 已完成 Alembic migrations（保证 `search_index` 存在）
- Search projector 至少跑过一轮（否则数据不足可能导致误判）

---

## 1) 执行方式

### 1.1 本地运行（推荐：稳定入口）

- 全量 write-gate：
  - `python backend/scripts/cli.py labs shadow-verify-search-index-write-gate --database-url "postgresql://..."`
- 限定单个 library（可选 scope，仅用于缩小排查面）：
  - `python backend/scripts/cli.py labs shadow-verify-search-index-write-gate --database-url "postgresql://..." --library-id <uuid>`

默认输出目录：
- `docs/labs/_snapshot/auto/S2B-2A-1A/shadow_verify_search_index_write_gate/<run_id>/_result.json`

---

## 2) 结果解释（验收口径）

### 2.1 唯一性（核心 gate）

目标：`search_index` 内同一实体不允许出现多行。

- `duplicates_groups_total`：全量范围内，`(entity_type, entity_id)` 出现 `COUNT(*)>1` 的 group 数量
- `duplicates_extra_rows_total`：全量范围内，重复导致的“多余行数”（对每个 group 求 `COUNT(*)-1` 再求和）
- `duplicates_by_entity_type`：按 `entity_type` 拆分的重复统计（用于快速定位）

如果提供 `--library-id`（或脚本 `LIBRARY_ID`）：

- `duplicates_groups_scoped` / `duplicates_extra_rows_scoped`：仅统计 `search_index.library_id == <library_id>` 的范围（用于缩小排查面）

判定：
- `duplicates_extra_rows_total == 0` → 通过（exit 0）
- 否则 → 失败（exit 2）

---

## 3) 证据与关联位置

- 稳定 CLI 入口：`backend/scripts/cli.py`（`labs shadow-verify-search-index-write-gate`）
- CI workflow：`.github/workflows/drill-write-gate.yml`
- 相关父 log：`docs/logs/log-S2B-2A-failure-contract-v2.md`
- 子 log（规则语义）：`docs/logs/log-S2B-2A-1A-shadow-verify-write-gate.md`

---

## 4) 常见失败与排查

- 出现 duplicates：
  - 先看 `duplicates_by_entity_type` 确认是哪类实体
  - 再用 `library-id` 缩小范围
  - 最后回到写入侧（projector/worker）排查“重复投递是否导致重复插入”或“缺失唯一约束/冲突策略”

注：本 lab 是 v2 write-gate 的最小代理指标；它不等价于“完全幂等证明”，但能先把最危险的重复副作用显式化并工程化阻断。

---

## 5) Evidence note（2026-02-18 本地 5 次运行）

本 lab 已在本地连续运行 5 次并落盘快照：

- `20260218T185230-wg-run1`
- `20260218T185231-wg-run2`
- `20260218T185232-wg-run3`
- `20260218T185233-wg-run4`
- `20260218T185234-wg-run5`
