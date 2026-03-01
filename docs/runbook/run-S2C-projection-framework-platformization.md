# Run-S2C: projection framework platformization（Spec/Registry/Harness/Templates/Drills）

---

**id**: `S2C-projection-framework-platformization`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/S2C-projection-framework-platformization`
**status**: `draft`          # draft | stable | archived
**scope**: `S2C`
**decision_date**: `2026-03-01`
**context_issue**:
  **DoD**: ``
  **Labs**: ``
**decision**: `Standardize a reusable, auditable projection framework (spec/registry/harness/templates + drills) so new projections ship as spec+apply with repeatable evidence.`
  **positive**: `"Reusable harness + templates", "Catalog-driven drills", "Artifacts as SoT"`
  **negative**: `"Search DB→ES migration needs independent slice + evidence", "Requires docker compose for DB/infra"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 给 S2C（路线 A）提供可执行的“最小运维闭环”：
  - 用 catalog scenario 跑出 `_result.json` 证据（SoT）
  - 当需要回填/重建时，优先走模板化 runner（rebuild/backfill）
- 把日常操作入口从“散落脚本”统一到：
  - GitHub Actions：`drill-labs-scenario`（按 `scenario_id` 触发）
  - 本地：按 scenario 对应脚本执行，落盘快照

## 2) Scope（本 runbook 覆盖什么）

- DB-only（无需 ES）：
  - outbox writer-template/harness evidence（S2C-2A）
  - chronicle rebuild smoke（S2C-3A）
  - backfill template smoke（S2C-5A；SoT→outbox）
- ES-involved：不在本 runbook 直接给出“Search worker → harness”的迁移执行口径；该迁移必须跟随 `S2C-6A` 独立证据链交付。

## 3) Evidence Bundle（S2C）

### 3.1 Output root

- 自动快照根目录：`docs/labs/_snapshot/auto/<scenario_slug>/<run_id>/`

### 3.2 Minimal contract

- 每次运行至少生成：`_result.json`（事实源 SoT；包含 `ok` + counts + 参数/上下文）
- GitHub Actions（reusable runner）会按既定合约上传 artifacts（成功/失败不同包型）。

## 4) One-click Automation（GitHub Actions）

- Workflow：`.github/workflows/drill-labs-scenario.yml`
- 运行方式：手动触发 `workflow_dispatch`，输入 `scenario_id`。

### 4.1 Scenario ids（S2C 常用）

- `verify/outbox/writer_template_harness_evidence`（DB-only；S2C-2A 证据包）
- `verify/chronicle/rebuild_entries_smoke`（DB-only；S2C-3A smoke）
- `verify/search/backfill_outbox_smoke`（DB-only；S2C-5A backfill template smoke）

> 注：所有可用 scenario 以 `docs/labs/scenarios/catalog.yml` 为准。

## 5) Local Operation

### 5.1 Prerequisites

- Docker engine 可用（用于 devtest Postgres）
- backend Python 依赖可用（能运行 `backend/scripts/*`）

### 5.2 Start devtest DB（示例）

- `docker compose -f docker-compose.devtest-db.yml up -d --wait`

### 5.3 Run S2C scenarios（示例）

S2C-5A（backfill template smoke；SoT→outbox；DB-only）：

- PowerShell（Windows）：
  - `$env:DATABASE_URL='postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test'`
  - `python backend/scripts/labs/s2c5a_backfill_search_outbox_smoke.py --database-url "$env:DATABASE_URL" --run-id <run_id> --outdir "docs/labs/_snapshot/auto/s2c5a_backfill_search_outbox_smoke/<run_id>"`

S2C-3A（chronicle rebuild smoke；DB-only）：

- `python backend/scripts/labs/s2c3a_rebuild_chronicle_entries_smoke.py --database-url "$DATABASE_URL" --run-id <run_id> --outdir "docs/labs/_snapshot/auto/s2c3a_rebuild_chronicle_entries_smoke/<run_id>"`

S2C-2A（writer-template/harness evidence；DB-only）：

- `python backend/scripts/labs/s2c2a_writer_template_harness_evidence.py --database-url "$DATABASE_URL" --run-id <run_id> --outdir "docs/labs/_snapshot/auto/s2c2a_writer_template_harness_evidence/<run_id>"`

## 6) Troubleshooting

- `ModuleNotFoundError: infra`：确保从 repo root 运行；如仍失败，确认脚本具备自包含的 `sys.path` 处理（S2C-5A smoke 已内建）。
- backfill env gate：真实 backfill 工具建议要求 `OUTBOX_BACKFILL_ENABLED=true`；labs smoke runner 会在证据运行中显式满足 gate。
- 数据不足导致 verify 失败：优先看对应 `_result.json` 的 counters 与建议字段（或提高 ensure-min-rows/limit）。

## 7) Notes（边界与下一步）

- 本 runbook 只覆盖“框架化后的可执行入口与证据口径”。
- Search 的 DB→ES 消费迁移（worker → harness）属于 `S2C-6A`：需要 ES 依赖、回滚面、N≥3 rounds 证据，必须独立交付。
