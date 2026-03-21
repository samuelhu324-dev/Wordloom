# Run-S4A-5A: operational visibility & post-change verification (dev/test)

---

**id**: `S4A-5A-operational-visibility-and-post-change-verification`
**kind**: `runbook`
**title**: `run/S4A-5A-operational-visibility-and-post-change-verification`
**status**: `draft`
**scope**: `S4A-5A`
**decision_date**: `2026-03-21`
**context_issue**:
  **DoD**: ``
  **Labs**: `S4A-5A`
**decision**: `Use existing status/health scripts, the deploy_app_verify gate, and the labs failure drills as one thin operator path to answer "Is the system healthy now?", "Did this change keep it healthy?", and "If not, where do I look first?" on dev/test.`
  **positive**: `"Reuses existing scripts & drills", "Low-cardinality PASS/FAIL signals", "Concrete samples for both green and failure cases"`
  **negative**: `"Covers only dev/test & demo", "No full observability platform", "Depends on S4A-1A/2A/3A/S3A/S6A assets"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 给 operator 一条统一的入口，在 dev/test 里回答三个问题：
  - 现在这个系统健康吗？
  - 最近一次变更之后，它还是健康的吗？
  - 如果不健康，我第一时间应该去哪里看脚本输出 / evidence 包？
- 不新增复杂的监控平台，而是复用：
  - `scripts/ops/status.sh` + `scripts/ops/health.sh` 作为 health summary；
  - `scripts/ops/deploy_app_verify.sh` 作为 post-change verification gate；
  - S3A/S6A 的 labs failure drills 和 evidence 包，作为“从异常到诊断”的样本。

## 2) Scope

- Covered：
  - dev/test 本地环境下的 runtime 健康视图（DB/API/UI/ES/worker）；
  - 变更后通过 `deploy_app_verify` + 轻量 HTTP smoke 检查“是否仍然健康”；
  - 当 labs/failure drill 报 FAIL 时，如何通过 evidence 包快速定位问题。
- Out of scope：
  - 生产级监控 / 日志聚合 / tracing 平台的设计与运维；
  - 正式 incident 管理流程（告警分派、值班轮换等）；
  - 非 dev/test 环境（staging/prod）的 SLO/SLA 指标和 dashboard。
- 主要参考：
  - `docs/logs/log-S4A-5A-operational-visibility-and-post-change-verification.md`
  - `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`
  - `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/runbook/run-S4A-2A-deploy-verify-rollback-runtime-path.md`
  - `docs/runbook/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
  - `scripts/ops/status.sh`, `scripts/ops/health.sh`, `scripts/ops/deploy_app_verify.sh`
  - `backend/scripts/cli.py labs ...` 与 `docs/labs/_snapshot/auto/**`

## 3) Evidence Bundle

### 3.1 Output roots

- Phase logs：
  - S4A-5A：`docs/logs/log-S4A-5A-operational-visibility-and-post-change-verification.md`（P2-C1-S1/S2 evidence 摘要）；
  - S4A-2A：`docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`（deploy_app_verify happy path PASS 样本）；
  - S3A-2A-4B：`docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`（failure drills malfunction 与 evidence 结构）；
- Machine-verifiable checks：
  - `scripts/ops/status.sh <env>` 的 `[ops/status]` 输出（`db_container`、`infra_es`、`api_health`、`ui_http`、`es_http` 等键）；
  - `scripts/ops/health.sh <env>` 的健康检查结果与 exit code；
  - `scripts/ops/deploy_app_verify.sh <env>` 的 `POST_DEPLOY_RESULT=PASS|FAIL` 行及退出码；
  - `docs/labs/_snapshot/auto/**` 中 `_result.json` 和 `_recipe.json` 等 evidence。

### 3.2 Summary or ledger

- S4A-5A 不引入新的 JSON ledger，而是复用：
  - S4A-2A 中的 deploy_app_verify PASS/FAIL 样本；
  - S3A-2A-4B 中 labs run/verify/export 的 evidence 包目录结构；
- 当 operator 需要“证明”时，可以引用：
  - 一次 `deploy_app_verify` PASS 输出（含 `phase=S4A-2A env=dev target_head_sha=<sha>`）；
  - 一次 labs 场景从 FAIL → 修复 → PASS 的 `_result.json` + `_recipe.json`。

## 4) Health Summary View（status + health）

### 4.1 快速检查：status

- 命令：
  - `bash scripts/ops/status.sh dev`
- 关键信息：
  - `env_file`：当前使用的 env 文件（例如 `.env.dev`）；
  - `db_container`：`healthy` / `not-running` / `unknown`；
  - `infra_es`：`healthy` / `not-running` / `unknown`；
  - `api_health`：API `/api/v1/health` HTTP 状态码（期望 `200`）；
  - `worker_healthz` / `worker_readyz`：worker metrics 端点 HTTP 状态码；
  - `ui_http`：UI 根路径 HTTP 状态码（期望 `200` 或 `30x`）；
  - `es_http`：ES HTTP 状态码（期望 `200`）。
- 解读模式：
  - `db_container` / `infra_es` 非 `healthy`：优先按 S4A-1A runbook 排查容器和 infra；
  - HTTP 为 `000`：通常表示端口未监听或连接失败；
  - UI 为 `30x`：对本地或 Vercel demo 通常是可接受的重定向。

### 4.2 严格 gate：health

- 命令：
  - `bash scripts/ops/health.sh dev`
- 行为：
  - 若找不到 devtest DB 容器或其 health 非 `healthy`，脚本会打印 `[ops] db_devtest unhealthy` 并 `exit 1`；
  - 对 API/UI/ES 执行 HTTP 检查，不在允许列表中的状态码会导致脚本 `exit 1`；
  - 若 `SEARCH_OUTBOX_WORKER_ENABLED=0`，worker 路径会被跳过，打印 `worker runtime skipped` 并正常退出；
- 解读模式：
  - exit 0：dev/test runtime 处于“可继续操作”状态；
  - 非 0：优先查看输出中的 `[ops]` 行与各 `check_http_ok` 标签（`api_health` / `ui_http` / `es_http`）。

## 5) Post-change Verification Checklist（after deploy or config change）

### 5.1 变更前（可选但推荐）

- 在大改动前，建议先跑一轮 baseline：
  - `bash scripts/ops/status.sh dev`
  - `bash scripts/ops/health.sh dev`
- 如果 baseline 已经 FAIL，先按 S4A-1A / S4A-2A / S3A runbook 修复，再进行后续变更。

### 5.2 变更后标准流程

1. 按 S4A-1A/S4A-2A runbook 启动环境：
   - `./scripts/ops/env_prep.sh dev`
   - `./scripts/ops/start.sh dev app --no-worker`（或 `all --no-worker`，视需要而定）。
2. 跑一轮健康摘要：
   - `bash scripts/ops/status.sh dev`
   - `bash scripts/ops/health.sh dev`
3. 跑 post-change verification gate：
   - `bash scripts/ops/deploy_app_verify.sh dev`
4. 可选：针对本次变更相关的关键路径做一轮 HTTP smoke：
   - API：`curl http://127.0.0.1:<API_PORT>/api/v1/health`；
   - UI：`curl http://127.0.0.1:30002/` 或打开浏览器访问 `/demo`。

### 5.3 成功 / 失败判定

- 成功（“变更后仍然健康”）：
  - `deploy_app_verify` 输出 `POST_DEPLOY_RESULT=PASS` 并 exit 0；
  - `status.sh` / `health.sh` 没有异常行，关键字段为 green；
- 失败：
  - `deploy_app_verify` 输出 `POST_DEPLOY_RESULT=FAIL ...` 或 exit 非 0；
  - 即使 `deploy_app_verify` 未运行，只要 `health.sh` exit 非 0，也应视为 post-change verification 失败，需要排查。

## 6) Using Failure Drills & Evidence when Things Break

### 6.1 何时转向 failure drills

- 以下情况可以/应该调用 labs failure drills 来协助诊断：
  - 健康检查通过，但功能仍有可疑（例如 ES 写入路径、collector、outbox worker）；
  - 你需要验证某个特定场景（如 `es_write_block_4xx`）在修复后是否真的恢复；
  - 希望留下结构化 evidence 包用于后续复盘或交接。

### 6.2 基本命令形态

- 典型调用：
  - `python backend/scripts/cli.py labs run <scenario> --env .env.dev`
  - `python backend/scripts/cli.py labs verify <scenario> --env .env.dev`
  - `python backend/scripts/cli.py labs export <scenario> --env .env.dev`
- 运行后，自动生成的 evidence 通常位于：
  - `docs/labs/_snapshot/auto/<lab_id>/<scenario>/<run_id>/`。

### 6.3 Operator 视角的诊断步骤

- 当某个 labs 场景 verify 为 FAIL 时：
  1. 打开对应目录中的 `_result.json`，阅读：
     - `result`（PASS/FAIL）、`why`、关键计数或 delta；
  2. 对照 `_recipe.json` 看本次运行使用了哪些开关（`FAULT_SCENARIO` / 环境变量等）；
  3. 根据 S3A-2A-4B runbook 中的 malfunction 记录，确认这属于哪一类常见问题；
  4. 修复配置或前置数据，重新 run/verify，直到 `_result.json` 报 PASS。

## 7) Troubleshooting

- `deploy_app_verify` FAIL 且 `status_rc!=0`：
  - 直接运行 `bash scripts/ops/status.sh dev`，查看 `db_container` / `infra_es` / `api_health` / `ui_http` / `es_http` 哪一项异常；
  - 按 S4A-1A runbook 排查容器、端口或 env 配置；
- `deploy_app_verify` FAIL 且 `status_rc==0` 但 `health_rc!=0`：
  - 说明基础组件表面正常，但健康检查发现 HTTP 行为异常；
  - 运行 `bash scripts/ops/health.sh dev` 直接查看 `[ops]` 错误行；
  - 检查最近有关 API/UI/ES 的代码或配置改动；
- `health.sh` 报 DB unhealthy：
  - 根据 S4A-1A / S4A-3A runbook 检查 devtest DB 容器和数据；
- labs verify FAIL 且 `_result.json` 显示 metrics/日志不符合预期：
  - 按 S3A-2A-4B runbook 提到的场景，检查：
    - 是否选择了错误的端口或 env；
    - 是否缺失前置数据（例如 `search_index` 行）；
    - 是否需要调整注入配方或 duration；
  - 修复后重新 run/verify，并记录修复前后的 `_result.json` 差异。

## 8) Notes and Boundaries

- 本 runbook 只是 S4A-5A phase log 的 operator 入口，不替代 phase log 本身；
- 所有示例均以 dev/test 为前提：
  - 不直接迁移到 prod/staging，而是作为“本地演练故事”在面试和设计文档中讲述；
- 建议在对外描述时重复使用的语言：
  - "health summary view"：基于 status + health 的 dev/test 运行时健康摘要；
  - "post-change verification gate"：基于 deploy_app_verify 的变更后闸门；
  - "failure drill evidence bundle"：labs 产出的 `_recipe.json` + `_result.json` + metrics/logs/traces；
- 未来扩展方向：
  - 针对特定业务功能增加少量 HTTP 级别的 smoke tests；
  - 将部分 status/health/labs 检查接入 CI 作为 hard gate；
  - 在有需要时再引入更完整的 dashboard，而不是在 v1 就过度设计。
