# Run-S2B: projection table merge（Chronicle v0：Shadow Verify + Read Switch）

---

**id**: `S2B-projection-table-merge`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/S2B-projection-table-merge`
**status**: `draft`          # draft | stable | archived
**scope**: `S2B`
**decision_date**: `2026-02-18`
**context_issue**:
  **DoD**: `#56, #57`
  **Labs**: `#56, #57`
**decision**: `Standardize a safe, rollbackable projection-table merge workflow using a v0 shadow verification drill + a read switch, starting with Chronicle.`
  **positive**: `"Rollbackable read switch", "Machine-verifiable shadow evidence", "Stable CLI + Actions entry"`
  **negative**: `"Needs DB/compose in CI", "Shadow verify scope is v0 (not full semantic parity)", "Tracing not collected yet"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Provide a repeatable workflow for “合表/合 projection”前的最小安全闭环：
  - 先做 shadow verify（对账证据）
  - 再做可回滚 read switch（默认不影响现网）
- 把“可审计证据链”从实现细节中抽离出来，作为 Failure Contract v1 的可落地样板（先从 Chronicle 开始）。

## 2) Scope（Chronicle + Search v0）

- 旧 SoT：`chronicle_events`
- 新投影表：`chronicle_entries`
- Shadow verify 场景：`shadow_verify_chronicle_entries`
- Read switch 开关：`MERGED_READ_ENABLED=0/1`

Search（v0 先做 shadow verify）：

- SoT：`blocks` / `books` / `tags`
- 投影表：`search_index`
- Shadow verify 场景：`shadow_verify_search_index`
- Read switch（独立开关）：`SEARCH_MERGED_READ_ENABLED=0/1`（不复用 Chronicle 的 `MERGED_READ_ENABLED`）

## 3) Evidence Bundle（v0）

### 3.1 Output root

- 自动快照根目录：
  - `docs/labs/_snapshot/auto/S2B-1A-1A/shadow_verify_chronicle_entries/<run_id>/`
  - `docs/labs/_snapshot/auto/S2B-1A-2A/shadow_verify_search_index/<run_id>/`

v2（write-gate，S2B-2A-1A）：

- `docs/labs/_snapshot/auto/S2B-2A-1A/shadow_verify_search_index_write_gate/<run_id>/`

### 3.2 Minimal contract

每次运行至少生成：
- `_result.json`：本次对账结果（`ok` + counts + mismatch counters）

GitHub Actions drill 额外生成（用于截图1-2约定的 artifacts）：
- `artifacts/summary.json`
- `artifacts/logs.txt`
- `artifacts/traces.json`（当前为占位 `[]`，此 drill 还不采集 tracing）

## 4) One-click Automation（GitHub Actions）

- Workflow：`.github/workflows/drill-shadow-verify-entries.yml`
- Workflow（write-gate 专用）：`.github/workflows/drill-write-gate.yml`
- 行为约定（截图1-2）：
  - 成功：仅上传 `summary.json`
  - 失败：上传完整 `artifacts.zip`（包含 summary/logs/traces）并让 job 失败

### 4.1 Operator instructions

- 打开 GitHub Actions：`drill-shadow-verify-entries`
- 输入：
  - `book_id`（可选，限定单本书；为空则全量）
- 运行后：下载 artifact `drill-shadow_verify_chronicle_entries-<run_id>`

write-gate：

- 打开 GitHub Actions：`drill-write-gate`
- 输入：
  - `scenario=shadow_verify_search_index_write_gate`
  - `library_id`（可选；为空则全量）

## 5) Local Operation

### 5.1 Prerequisites

- Docker engine 可用（用于 devtest Postgres）
- 已安装 backend Python 依赖（能运行 `backend/scripts/cli.py`）

### 5.2 Start devtest DB（示例）

- `docker compose -f docker-compose.devtest-db.yml up -d --wait`

### 5.3 Run shadow verify（稳定入口）

- 全量：
  - `python backend/scripts/cli.py labs shadow-verify-chronicle-entries --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test"`
- 限定单本书：
  - `python backend/scripts/cli.py labs shadow-verify-chronicle-entries --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test" --book-id <uuid>`

输出目录（默认）：
- `docs/labs/_snapshot/auto/S2B-1A-1A/shadow_verify_chronicle_entries/<run_id>/_result.json`

Search（全量）：

- `python backend/scripts/cli.py labs shadow-verify-search-index --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test"`

Search（限定 library，可选）：

- `python backend/scripts/cli.py labs shadow-verify-search-index --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test" --library-id <uuid>`

输出目录（默认）：

- `docs/labs/_snapshot/auto/S2B-1A-2A/shadow_verify_search_index/<run_id>/_result.json`

Search write-gate（v2 1A，唯一性/幂等最小代理）：

- `python backend/scripts/cli.py labs shadow-verify-search-index-write-gate --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test"`

输出目录（默认）：

- `docs/labs/_snapshot/auto/S2B-2A-1A/shadow_verify_search_index_write_gate/<run_id>/_result.json`

### 5.4 Evidence note（2026-02-18 本地 5 次运行）

S2B-1A-2A（Search shadow verify）已在本地连续运行 5 次并落盘快照：

- `20260218T151416-search-run1`
- `20260218T151418-search-run2`
- `20260218T151420-search-run3`
- `20260218T151421-search-run4`
- `20260218T151423-search-run5`

## 6) Verification / Acceptance（v0 口径）

### 6.1 Output fields

- `events_total`：`chronicle_events` 行数
- `entries_total`：`chronicle_entries` 行数
- `missing_entries`：events 存在但 entries 缺失数量
- `extra_entries`：entries 存在但 events 缺失数量（不应出现）
- `mismatched_book_id`：同一 `id` 下 `book_id` 不一致数量（不应出现）

### 6.2 Pass / Fail

- 通过：`missing_entries == 0 && extra_entries == 0 && mismatched_book_id == 0`
- 失败：任一非 0 → 退出码非 0（当前为 2）

说明：这是低成本、可重复的 v0 口径（count + key-level 对账）。
若要升级到 `stable`，建议明确并补齐更强语义约束（例如排序/关键字段一致性/分页稳定性等）以及它们在新旧模型间的映射规则。

## 7) Read switch（切读与回滚）

- 默认：`MERGED_READ_ENABLED=0`（Chronicle 查询读 events repo）
- 开启：`MERGED_READ_ENABLED=1`（Chronicle 查询读 entries repo）
- 回滚：把开关关回 `0`

Search（独立切读开关）：

- 默认：`SEARCH_MERGED_READ_ENABLED=0`（Search stage1 provider 遵循 `SEARCH_STAGE1_PROVIDER`，默认 postgres）
- 开启：`SEARCH_MERGED_READ_ENABLED=1`（强制 stage1 provider 使用 `postgres`，覆盖 `SEARCH_STAGE1_PROVIDER`）
- 回滚：把开关关回 `0`

建议顺序：
1) shadow verify 通过（留证据）
2) 短时间开启 read switch 做冒烟
3) 发现异常立即回滚

## 8) Troubleshooting

- `missing_entries > 0`：优先检查 `chronicle_entries` 是否完成 backfill / projector 是否跑过。
- `extra_entries > 0`：检查是否有错误写入/重复生成 entries，或 join key 不一致。
- `mismatched_book_id > 0`：检查 entries 写入时 book_id 映射/回填逻辑。
- CI 失败：下载失败时的 zip，优先查看 `logs.txt` 与 `summary.json`。

## 9) References

- Logs:
  - `docs/logs/log-S2B-1A-failure-contract-v1.md`
  - `docs/logs/log-S2B-1A-1A-chronicle-concurrent-handling.md`
- Lab manual:
  - `docs/labs/lab-S2B-1A-1A-chronicle-concurrent-handling.md`
- Workflow:
  - `.github/workflows/drill-shadow-verify-entries.yml`
- Harness:
  - `backend/scripts/cli.py`
