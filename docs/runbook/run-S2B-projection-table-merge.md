# Run-S2B: projection table merge（Chronicle v0：Shadow Verify + Read Switch）

---

**id**: `S2B-projection-table-merge`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/S2B-projection-table-merge`
**status**: `stable`          # draft | stable | archived
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
- `artifacts/traces.json`（默认可能为占位 `[]`；shared-keys drill 会写入最小 span 以便 logs/traces 互证）

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
  - 或：
    - `scenario=shadow_verify_search_index_paging_stability`
    - `scenario=shadow_verify_shared_keys`
    - `scenario=shadow_verify_dual_run_readiness_gate`
    - `scenario=shadow_verify_dual_run_stage1`
    - `scenario=shadow_verify_dual_run_stage2`
    - `scenario=shadow_verify_dual_run_window`
    - `scenario=shadow_verify_canary_dual_write`
    - `scenario=shadow_verify_dual_write_sampling`
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

Search paging stability（v2 2A，分页稳定性最小口径）：

- `python backend/scripts/cli.py labs shadow-verify-search-index-paging-stability --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test"`

说明：该命令会要求验证至少 2 页；若数据库数据不足，可追加：

- `--ensure-min-rows 120`

输出目录（默认）：

- `docs/labs/_snapshot/auto/S2B-2A-2A/shadow_verify_search_index_paging_stability/<run_id>/_result.json`

Search shared keys（v2 2A，共享键证据包最小口径）：

- `python backend/scripts/cli.py labs shadow-verify-shared-keys --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test"`

说明：该命令输出 `shared_keys + evidence_queries`，用于后续在 logs/metrics/traces 中反查同一链路；若需要确保 sample 存在，可追加：

- `--ensure-min-rows 5`

输出目录（默认）：

- `docs/labs/_snapshot/auto/S2B-2A-2A/shadow_verify_shared_keys/<run_id>/_result.json`

Search 2A readiness gate（v2 2A，dry-run 准入门：聚合 1A/2A 前置证据，不写入）：

- `python backend/scripts/cli.py labs shadow-verify-dual-run-readiness-gate --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test"`

说明：该命令会在一个 `_result.json` 中聚合：

- write-gate（1A）
- paging stability（2A）
- shared keys evidence bundle（2A）

输出目录（默认）：

- `docs/labs/_snapshot/auto/S2B-2A-2A/shadow_verify_dual_run_readiness_gate/<run_id>/_result.json`

Search true dual-run stage1（v2 2A：读侧并行对账，Postgres vs Elasticsearch；CI-safe 不启动 outbox worker）：

- `python backend/scripts/cli.py labs shadow-verify-dual-run-stage1 --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test" --ensure-min-rows 25 --candidate-limit 20 --strategy strict --es-url "http://127.0.0.1:19200" --es-index "wordloom-search-index-drill-<run_id>" --recreate-index`

说明：该命令会落盘 `backfill.log`，用于排查 ES backfill 过程。

输出目录（默认）：

- `docs/labs/_snapshot/auto/S2B-2A-2A/shadow_verify_dual_run_stage1/<run_id>/_result.json`

Search true dual-run stage2（v2 2A：写侧影子闭环，outbox → worker → ES → 对账；CI-safe one-shot worker）：

- `python backend/scripts/cli.py labs shadow-verify-dual-run-stage2 --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test" --ensure-min-rows 25 --candidate-limit 20 --strategy strict --es-url "http://127.0.0.1:19200" --es-index "wordloom-search-index-drill-<run_id>" --recreate-index`

说明：该命令会落盘 `worker.log`（用于排查 outbox worker claim/poll/indexing）。

输出目录（默认）：

- `docs/labs/_snapshot/auto/S2B-2A-2A/shadow_verify_dual_run_stage2/<run_id>/_result.json`

Search sustained dual-run window（v2 2A：持续窗口验证，worker 常驻 + 周期性 enqueue + drain + 对账）：

- `python backend/scripts/cli.py labs shadow-verify-dual-run-window --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test" --ensure-min-rows 25 --candidate-limit 20 --strategy strict --duration-seconds 30 --interval-seconds 1 --enqueue-batch-size 20 --max-total-events 200 --drain-timeout-seconds 20 --max-outbox-failed 0 --max-outbox-pending 0 --max-outbox-processing 0 --require-outbox-done-eq-enqueued --es-url "http://127.0.0.1:19200" --es-index "wordloom-search-index-drill-<run_id>" --recreate-index`

说明：该命令会落盘 `worker.log`；并在 `_result.json` 中写入 `window.samples`（每个采样点包含 outbox status_counts），用于在 runbook checklist 中审计“窗口内 backlog 是否受控”。
补充：window 结束后 labs 会主动停止 worker，因此 `worker.exit_code` 可能为非 0；以 `_result.json.ok=true` 与 outbox drained（`pending/processing=0, failed=0`）为准。

Window hard gate（阈值化 checklist；用于从“能跑”推进到“可执行/可放行”）：

- 口径（以 `_result.json` 为事实源）：
  - `outbox.status_counts.failed <= max_outbox_failed`（默认 0）
  - `outbox.status_counts.pending <= max_outbox_pending`（默认 0）
  - `outbox.status_counts.processing <= max_outbox_processing`（默认 0）
  - `require_outbox_done_eq_enqueued=true` 时：`outbox.status_counts.done == outbox.enqueued_total`
  - `worker.ok=true`（允许 stop requested；详见 `_result.json.worker.stop_requested`）
  - `compare.parity_ok=true`（strategy=strict 时为 ordered strict parity）
- 对应 CLI 参数（CI 可显式传参，保证 hard gate 可审计）：
  - `--max-outbox-failed 0 --max-outbox-pending 0 --max-outbox-processing 0 --require-outbox-done-eq-enqueued`
- 推进动作（从“能跑”→“更接近可放行”）：
  - 先固定 hard gate 不变，把 `--duration-seconds` 拉长（例如 300s），并相应提高 `--max-total-events`（保持低速）；审计 `_result.json.window.samples` 中 `pending/processing` 是否在窗口内反复积压。
  - 准入门槛建议：至少连续 N 次（例如 N=3）long-window 运行均 `ok=true` 且 outbox drained（`pending/processing=0, failed=0`）。

Manual long window（300s，低速示例；用于拿更接近真实的窗口证据）：

重要：要验证“持续窗口（sustained）”，必须确保整个窗口内都在持续 enqueue。

- 经验公式：`max_total_events >= floor(duration_seconds / interval_seconds) * enqueue_batch_size`
  - 若 `max_total_events` 过小，会提前达到上限，导致实际 enqueue 只跑了十几秒（窗口未被真正覆盖）。

Profile A（推荐：真实 300s sustained，保持 CI 同款节奏）：

- `python backend/scripts/cli.py labs shadow-verify-dual-run-window --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test" --ensure-min-rows 25 --candidate-limit 20 --strategy strict --duration-seconds 300 --interval-seconds 1 --enqueue-batch-size 5 --max-total-events 1500 --drain-timeout-seconds 120 --max-outbox-failed 0 --max-outbox-pending 0 --max-outbox-processing 0 --require-outbox-done-eq-enqueued --es-url "http://127.0.0.1:19200" --es-index "wordloom-search-index-drill-<run_id>" --recreate-index --worker-max-runtime-seconds 450`

Profile B（轻量 300s sustained：降低速率，减少总事件数）：

- `python backend/scripts/cli.py labs shadow-verify-dual-run-window --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test" --ensure-min-rows 25 --candidate-limit 20 --strategy strict --duration-seconds 300 --interval-seconds 2 --enqueue-batch-size 2 --max-total-events 300 --drain-timeout-seconds 120 --max-outbox-failed 0 --max-outbox-pending 0 --max-outbox-processing 0 --require-outbox-done-eq-enqueued --es-url "http://127.0.0.1:19200" --es-index "wordloom-search-index-drill-<run_id>" --recreate-index --worker-max-runtime-seconds 450`

Actions（workflow_dispatch，手动长窗口）：

- `drill-write-gate`：选择 `scenario=shadow_verify_dual_run_window`，并通过 inputs 覆盖：
  - `window_duration_seconds / window_interval_seconds / window_enqueue_batch_size / window_max_total_events / window_drain_timeout_seconds / window_worker_max_runtime_seconds`
- 本地快速审计（示例）：
  - `jq '{ok, outbox: .outbox.status_counts, enqueued: .outbox.enqueued_total, worker_ok: .worker.ok, parity_ok: .compare.parity_ok, stop: .worker.stop_requested}' docs/labs/_snapshot/auto/S2B-2A-2A/shadow_verify_dual_run_window/<run_id>/_result.json`

输出目录（默认）：

- `docs/labs/_snapshot/auto/S2B-2A-2A/shadow_verify_dual_run_window/<run_id>/_result.json`

Dual-run 最小上线形态（runtime entrypoint + 一键回滚开关）

目标：把“能跑通的 worker”变成“默认 off、可控启停、可限速/可隔离”的线上形态，避免 Procfile/脚本分叉。

- 稳定入口（Procfile 使用）：
  - worker 进程：`bash ./backend/scripts/ops/run_worker.sh .env.dev`（见 `Procfile.dev`/`Procfile.test`）
  - Python 入口：`python backend/scripts/search_outbox_worker.py`
- 一键回滚（推荐默认关闭，显式开启）：
  - `SEARCH_OUTBOX_WORKER_ENABLED=0`：worker 启动后立即退出（exit code=0）
  - `SEARCH_OUTBOX_WORKER_ENABLED=1`：允许 worker 正常运行
- 限速/隔离常用环境变量（worker 内部读取）：
  - `OUTBOX_CONCURRENCY`（默认 1）
  - `OUTBOX_BULK_SIZE` / `OUTBOX_BATCH_SIZE`（默认 100）
  - `OUTBOX_POLL_INTERVAL_SECONDS`（默认 1.0）
  - `OUTBOX_LEASE_SECONDS`（默认 30）
  - `OUTBOX_MAX_RUNTIME_SECONDS`（可选；用于 canary/演练窗口，避免跑飞）
  - `SEARCH_OUTBOX_LIBRARY_ALLOWLIST`（可选；逗号分隔 UUID；仅 claim 指定 library 的 outbox 行，用于 canary/隔离；默认空=不限制）
- 最小验证点（上线形态 sanity）：
  - 临时开启：在 `.env.dev`/`.env.test` 中将 `SEARCH_OUTBOX_WORKER_ENABLED=1`，然后通过 `Procfile.dev`/`Procfile.test` 启动 `worker_search`
  - 临时关闭（回滚）：将 `SEARCH_OUTBOX_WORKER_ENABLED=0` 并重启 `worker_search`
  - 开启后，worker log 中应持续出现 `outbox.claim_batch` / `projection.process_batch`（无 backlog 增长）
  - 关闭开关后，worker 应快速退出；outbox 仍可通过 replay/cleanup runbook 动作回收

Search canary dual-write（v2 2A，最小真写入 + 默认回滚/cleanup）：

- `python backend/scripts/cli.py labs shadow-verify-canary-dual-write --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test"`

说明：该命令会写入极小 canary 行到：

- `search_index`
- `search_outbox_events`

并默认执行 cleanup（作为 rollback 证据），以保持 devtest/CI 环境干净。

输出目录（默认）：

- `docs/labs/_snapshot/auto/S2B-2A-2A/shadow_verify_canary_dual_write/<run_id>/_result.json`

Search dual-write sampling（v2 2A，allowlist/sampling sustained dual-write）：

- CI-safe（默认建议）：strict + 不注入失败 + cleanup
  - `python backend/scripts/cli.py labs shadow-verify-dual-write-sampling --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test" --ensure-min-rows 25 --sample-size 20 --strategy strict --inject-failed-rate 0.0 --cleanup`

- Demonstrate DLQ + replay（只建议在隔离环境跑）：soft + 注入失败 + replay + cleanup
  - `python backend/scripts/cli.py labs shadow-verify-dual-write-sampling --database-url "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test" --ensure-min-rows 25 --sample-size 50 --strategy soft --inject-failed-rate 0.2 --replay-failed --replay-by ops --replay-reason "drill evidence" --cleanup`

说明：该命令从 `search_index` 采样既有行，向 `search_outbox_events` enqueue（影子旁写）；并可选模拟新侧失败（DLQ）与回放（replay）证据。

输出目录（默认）：

- `docs/labs/_snapshot/auto/S2B-2A-2A/shadow_verify_dual_write_sampling/<run_id>/_result.json`

### 5.4 Evidence note（2026-02-18 本地 5 次运行）

S2B-1A-2A（Search shadow verify）已在本地连续运行 5 次并落盘快照：

- `20260218T151416-search-run1`
- `20260218T151418-search-run2`
- `20260218T151420-search-run3`
- `20260218T151421-search-run4`
- `20260218T151423-search-run5`

S2B-2A-1A（Search write-gate）已在本地连续运行 5 次并落盘快照：

- `20260218T185230-wg-run1`
- `20260218T185231-wg-run2`
- `20260218T185232-wg-run3`
- `20260218T185233-wg-run4`
- `20260218T185234-wg-run5`

CI（GitHub Actions）：

- `drill-write-gate` 已手动触发并通过（2026-02-18，run #1，约 36s）

补充（2026-02-19）：

- `drill-write-gate` → `shadow_verify_search_index_paging_stability`：run_id=`22164058062-1`（ok=true，pages_checked=2）
- `drill-write-gate` → `shadow_verify_shared_keys`：run_id=`22164060556-1`（ok=true）
- `drill-write-gate` → `shadow_verify_dual_run_stage1`：run_id=`22174370696-1`（ok=true，strict parity；ES backfill + ordered candidates match）
- `drill-write-gate` → `shadow_verify_dual_run_stage2`：run_id=`22178056521-1`（ok=true，outbox worker one-shot；ordered candidates strict parity）
- `drill-write-gate` → `shadow_verify_canary_dual_write`：run_id=`22168857459-1`（ok=true，cleanup_enabled=true，remaining=0）
- `drill-write-gate` → `shadow_verify_dual_write_sampling`：run_id=`22170284952-1`（ok=true，strategy=strict，ensure_min_rows=25，sample_size=20，max_total_events=20，cleanup_enabled=true，remaining=0）

Local evidence（2026-02-19，devtest DB）:

- `labs shadow-verify-dual-write-sampling`（CI-safe strict）：run_id=`20260219T133300-sampling-run1`（ok=true）
- `labs shadow-verify-dual-write-sampling`（DLQ+replay demo）：run_id=`20260219T133500-sampling-dlq-replay-run1`（ok=true，dlq_failed_simulated_total>0，replayed_total>0）

说明：按截图1-2合约，成功时 artifact 下载包内仅包含 `summary.json`（其内容即 drill 的 `_result.json`）。

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

## 9) Cutover checklist（先读后写 + 回滚动作 + 准入证据）

本节作为 `S2B-2A` 的可执行准入清单；以 `_result.json` 与 workflow artifacts 为事实源。

### 9.1 Read cutover（Step A）

准入前置（全部满足）：

- `shadow_verify_dual_run_readiness_gate` 为 `ok=true`
- `shadow_verify_dual_run_stage1` 为 strict parity（`compare.parity_ok=true`）
- `shadow_verify_dual_run_window` 满足 hard gate（`failed/pending/processing` 阈值、`done==enqueued`、`worker.ok=true`）

执行：

1) Staging 先开启 `MERGED_READ_ENABLED=1` / `SEARCH_MERGED_READ_ENABLED=1` 做小窗口验证。
2) 观察窗口内证据：`_result.json` + logs/traces 可互证（shared keys 可反查）。
3) 无异常后再扩大范围。

回滚：

- 任一异常（分页漂移、parity 退化、链路不可观测）立即关闭 read switch（回到 `0`）。

### 9.2 Write cutover（Step B）

准入前置（全部满足）：

- Step A 已稳定通过。
- sustained dual-run window 在约束窗口内通过（建议连续 N 次，默认 N=3）。
- canary/sampling 证据可回放（含 strict/soft、DLQ/replay 路径）。

执行：

1) 停旧写侧 claim 路径（旧 worker 不再 claim）。
2) 新写侧 worker 接管（`SEARCH_OUTBOX_WORKER_ENABLED=1`，并保留 `OUTBOX_*` 限速参数）。
3) 持续观察 backlog 与失败重试曲线。

回滚：

- 立即停止新写侧消费（`SEARCH_OUTBOX_WORKER_ENABLED=0`），恢复旧写侧 claim。
- 保留本次窗口 artifacts，按 run_id 归档并登记 log。

## 10) Cleanup ledger（stub + deprecate window + ADR/Log 记账）

目标：避免“跑通后遗留双入口”。Cleanup 采用“先标注、后下线”的保守策略。

### 10.1 Stub policy（入口稳定）

- 对历史脚本/文档入口保留 stub 与跳转说明（禁止直接删除造成断链）。
- workflow/scenario 维持单入口：`drill-write-gate` + `backend/scripts/cli.py`。

### 10.2 Deprecate window（建议）

- T0：在 log/runbook 标注 deprecated（仅保留回滚用途）。
- T0 + 7d：若无回滚事件，移除默认调用路径（保留手动应急入口）。
- T0 + 14d：完成 ADR/Log 记账后正式下线 stub（如需）。

### 10.3 Record of completion（S2B-2A）

- Log：`docs/logs/log-S2B-2A-failure-contract-v2.md`
- Log：`docs/logs/log-S2B-2A-2A-dual-run-cutover-closure.md`
- ADR：`docs/adr/adr-S2B-projection-table-merge.md`

## 11) References

- Logs:
  - `docs/logs/log-S2B-1A-failure-contract-v1.md`
  - `docs/logs/log-S2B-1A-1A-chronicle-concurrent-handling.md`
  - `docs/logs/log-S2B-2A-failure-contract-v2.md`
  - `docs/logs/log-S2B-2A-2A-dual-run-cutover-closure.md`
- ADR:
  - `docs/adr/adr-S2B-projection-table-merge.md`
- Lab manual:
  - `docs/labs/lab-S2B-1A-1A-chronicle-concurrent-handling.md`
- Workflow:
  - `.github/workflows/drill-shadow-verify-entries.yml`
- Harness:
  - `backend/scripts/cli.py`
