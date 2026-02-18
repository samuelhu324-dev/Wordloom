# Lab-S2B-1A-1A：chronicle concurrent handling

---

**id**: `S2B-1A-1A`
**kind**: `lab`               # log | lab | runbook | adr | note
**title**: `chronicle concurrent handling`
**status**: `draft`           # draft | stable | archived
**scope**: `S2B`
**tags**: `EVOLUTION, Chronicle, Projection, lab, sub/2`
**links**: ``
  **issue**: `#56, #57`
  **pr**: ``
  **adr**: ``
  **runbook**: ``
**created**: `2026-02-18`
**updated**: `2026-02-18`

---

目标：给“合表/合 projection 的安全迁移”提供一个最小可复验的样板闭环：

- 先做 shadow verify（对账证据）
- 再做可回滚的 read switch（默认不影响现网）

本 lab 以 Chronicle 为样例：
- 旧 SoT：`chronicle_events`
- 新投影表：`chronicle_entries`
- read switch：`MERGED_READ_ENABLED=0/1`

---

## 0) 前置条件

- 有可用 Postgres（本地/容器均可）
- 已完成 Alembic migrations（保证 `chronicle_events` / `chronicle_entries` 存在）
- `chronicle_entries` 已有数据来源（backfill 或 projector 已跑过）
  - 若 `chronicle_entries` 为空但 `chronicle_events` 非空，本 lab 应该失败（这是预期信号）

---

## 1) 执行方式

### 1.1 本地运行（推荐：稳定入口）

使用稳定 CLI 入口（会把 `_result.json` 落到统一快照目录）：

- 全量对账：
  - `python backend/scripts/cli.py labs shadow-verify-chronicle-entries --database-url "postgresql://..."`
- 限定单本书：
  - `python backend/scripts/cli.py labs shadow-verify-chronicle-entries --database-url "postgresql://..." --book-id <uuid>`

默认输出目录：
- `docs/labs/_snapshot/auto/S2B-1A-1A/shadow_verify_chronicle_entries/<run_id>/_result.json`

### 1.2 本地运行（脚本直跑，可选）

如果只想要最小检查 + 退出码：
- `DATABASE_URL=... python backend/scripts/labs/lab-S2B-1A-1A.py`

如果希望也写出 `_result.json`（便于留证）：
- `OUTDIR=... RUN_ID=... DATABASE_URL=... python backend/scripts/labs/lab-S2B-1A-1A.py`

---

## 2) 结果解释（验收口径）

输出字段：
- `events_total`：`chronicle_events` 行数
- `entries_total`：`chronicle_entries` 行数
- `missing_entries`：在 events 存在但 entries 缺失的数量
- `extra_entries`：在 entries 存在但 events 缺失的数量（不应出现）
- `mismatched_book_id`：同一 `id` 下 entries 与 events 的 `book_id` 不一致数量（不应出现）

判定：
- `missing_entries == 0 && extra_entries == 0 && mismatched_book_id == 0` → 通过
- 否则 → 失败（进程退出码非 0，当前为 2）

说明：这份 lab 当前仍属于“低成本、可重复”的 v0 shadow verify 口径（count + key-level 对账）。
若后续要固化为 stable，建议再补更强约束（例如排序/关键字段一致性/分页稳定性等），但需要先明确这些语义在新旧模型间如何映射。

---

## 3) CI（GitHub Actions）

Workflow：`.github/workflows/drill-shadow-verify-entries.yml`

Artifacts 规范（简单版）：
- 每次 drill 生成：
  - `artifacts/summary.json`
  - `artifacts/logs.txt`
  - `artifacts/traces.json`
- CI 统一上传：`drill-${scenario}-${run_id}`
- 成功只上传 `summary.json`
- 失败上传完整 `artifacts.zip`（包含三件套）并让 job 失败

说明：这个 drill 当前不采集 tracing，所以 `traces.json` 先用占位 `[]` 固定格式，后续若要接 Jaeger/OTEL 再升级。

---

## 4) Read switch（切读与回滚）

- 默认：`MERGED_READ_ENABLED=0`（Chronicle 查询读 events repo）
- 开启：`MERGED_READ_ENABLED=1`（Chronicle 查询读 entries repo）
- 回滚：把开关关回 0

建议顺序：
1) 先做 shadow verify 通过（出证据）
2) 再短时间开启 read switch 做冒烟
3) 发现异常立即回滚

---

## 5) 证据与关联位置

- Read switch / DI：`backend/api/app/dependencies_real.py`
- Settings：`backend/api/app/config/setting.py`
- Wiring tests：`backend/api/app/tests/test_chronicle/test_merged_read_flag.py`
- Entries read-only repo：`backend/infra/storage/chronicle_entries_repository_impl.py`
- Shadow verify script：`backend/scripts/labs/lab-S2B-1A-1A.py`

---

## 6) 常见失败与排查

- `missing_entries > 0`：优先检查 `chronicle_entries` 是否完成 backfill / projector 是否跑过。
- `chronicle_entries` 表不存在：说明 migrations 未跑或 DB 指向不对。
- CI 失败：先下载失败时上传的 zip，看 `logs.txt` 与 `summary.json`。
