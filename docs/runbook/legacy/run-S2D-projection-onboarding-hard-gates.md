# Run-S2D: projection onboarding hard gates（sample projection 套餐）

---

**id**: `S2D-projection-onboarding-hard-gates`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/S2D-projection-onboarding-hard-gates`
**status**: `draft`          # draft | stable | archived
**scope**: `S2D`
**decision_date**: `2026-03-09`
**context_issue**:
  **DoD**: ``
  **Labs**: `S2D-1A`
**decision**: `Provide a one-command onboarding package for the S2D-1A sample projection (chronicle_daily_stats), reusing S2C templates and recording runs under artifacts/s2d-runs.json.`
  **positive**: `"统一 onboarding 套餐入口", "Evidence 可机械判定", "易于推广到其他 projection"`
  **negative**: `"目前仅覆盖单条示范投影", "还未接到统一 CI hard gate"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 为 S2D-1A 的示范投影 `chronicle_daily_stats` 提供一个“一条命令跑完整个 onboarding 套餐”的入口：
  - backfill smoke（SoT → outbox，幂等）
  - harness drill（outbox → projection adapter）
- 把每次运行的结果汇总到 `artifacts/s2d-runs.json`，作为后续 S2D-2A/3A hard gate 的基础事实源。

## 2) Scope（本 runbook 覆盖什么）

- 仅覆盖 S2D-1A 的 sample projection：`chronicle_daily_stats`。
- 环境：dev/test Postgres（本地 docker compose 或 CI 中的 devtest DB）。
- 依赖的底层 lab：
  - `backend/scripts/labs/s2d1a_chronicle_daily_stats_backfill_smoke.py`
  - `backend/scripts/labs/s2d1a_chronicle_daily_stats_harness_drill.py`

## 3) Evidence Bundle（S2D-1A 套餐）

### 3.1 Output roots

- 自动快照根目录（按 scenario + run_id 分桶）：
  - `docs/labs/_snapshot/auto/s2d1a_chronicle_daily_stats_backfill_smoke/<run_id>/`
  - `docs/labs/_snapshot/auto/s2d1a_chronicle_daily_stats_harness_drill/<run_id>/`
- 每个 scenario 下至少包含：`_result.json`（`ok` + 关键 counters + 参数）。

### 3.2 Runs summary（artifacts/s2d-runs.json）

- 归档文件：`artifacts/s2d-runs.json`（JSON array）。
- 每次执行 onboarding 套餐会追加一条记录，字段包含：
  - `log_id`：`"S2D-1A"`
  - `phase/cycle/step`：`"P3" / "C1" / "S1"`
  - `head_sha`：当前 git HEAD（best-effort）
  - `run_id`：本次运行的 run id（默认 `YYYYMMDD-HHMMSS`）
  - `database_url`：所用 dev/test DB 的 URL（建议为 PostgreSQL devtest 实例）
  - `ok`：整体是否通过（两个 scenario 都 ok）
  - `scenarios[]`：每个 scenario 的 `scenario_id/script/run_dir/ok/exit_code`。

## 4) Local Operation

### 4.1 Prerequisites

- Docker engine 可用（用于 devtest Postgres）：
  - `docker compose -f docker-compose.devtest-db.yml up -d --wait`
- backend Python 依赖可用（能运行 `backend/scripts/*`）。

### 4.2 One-command onboarding 套餐

假设本地 devtest DB URL 为：

- `postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test`

PowerShell（Windows）示例：

- 设置环境变量（可选，方便复用）：
  - `$env:DATABASE_URL = 'postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test'`
- 运行 S2D-1A onboarding 套餐脚本：
  - `python scripts/projections/s2d_1a_p3c1s1_sample_onboarding.py --database-url "$env:DATABASE_URL"`

说明：

- `--run-id` 可选；不传则默认使用 `YYYYMMDD-HHMMSS`。
- `--snapshot-root` 可选；默认 `docs/labs/_snapshot/auto`。

运行完成后：

- backfill smoke 结果：
  - `docs/labs/_snapshot/auto/s2d1a_chronicle_daily_stats_backfill_smoke/<run_id>/_result.json`
- harness drill 结果：
  - `docs/labs/_snapshot/auto/s2d1a_chronicle_daily_stats_harness_drill/<run_id>/_result.json`
- 汇总记录：
  - `artifacts/s2d-runs.json` 末尾新增一条记录（`ok` 字段表示整体是否通过）。

## 5) Troubleshooting

- `ModuleNotFoundError: infra`：请确认从 repo root 执行命令，并使用 `python scripts/projections/...` 形式；labs 本身已包含 `sys.path` 处理。
- `_result.json` 缺失或 `ok=false`：
  - 优先查看对应 scenario 下的 `_result.json` 内容（backfill/harness 各自解释原因）。
  - 脚本会根据 exit code + `_result.json.ok` 共同判定 `ok`；若 exit code=0 但 `ok=false`，整体 `ok` 仍为 false。
- `artifacts/s2d-runs.json` 损坏：
  - 若文件被手工编辑导致 JSON 解析失败，脚本会从空数组重新开始写入；如需保留旧记录，建议先修复该 JSON 文件。

## 6) Notes & Next（边界与下一步）

- 当前 runbook 仅提供 S2D-1A 示例投影的本地 onboarding 套餐入口，尚未接到统一的 CI hard gate；S2D-3A 将在此基础上扩展到多投影 + CI workflow。
- 如果未来有更多 projection 按 S2D onboarding 落地，可以：
  - 复用本脚本模式，为每条 projection 增加对应的 labs + onboarding 套餐脚本；
  - 或在新的 S2D-2A/3A phase 中引入 catalog 驱动的多投影 runner。
