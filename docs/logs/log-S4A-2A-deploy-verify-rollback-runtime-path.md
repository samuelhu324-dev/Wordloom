# log-S4A-2A (Phase 2: Deploy / Verify / Rollback Runtime Path)

---

**id**: `S4A-2A`
**kind**: `log`
**title**: `deploy / verify / rollback runtime path + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, Operations, Runtime, Deploy, Verification, Rollback, Drills, Evidence, epic/s4, epic/s4a, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4A-2A-deploy-verify-rollback-runtime-path.md`
  **parent_log**: `docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md`
  **previous_log**: `docs/logs/log-S4A-1A-ops-scripting-baseline.md`
  **reference_log_1**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_2**: `docs/logs/log-S5A-3B-object-storage-backup.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
**created**: `2026-03-21`
**updated**: `2026-03-21`

---

## Decision / Outcome

**Decision**:

- `S4A-2A` 聚焦于把 `wordloom-v3` 现有的启动链、drills/evidence 习惯和 Git/CI 资产，收口成一条明确的 `deploy / post-deploy verify / rollback` runtime path。
- 本 phase 不追求生产级多环境发布平台，而是先在本地 dev/test 语境下，形成可讲的 "安全部署 + 发布后验证 + 回滚" 样本和脚本约定。

**Default choices (phase defaults / v1)**:

- 目标环境：优先 dev/test，本地 WSL + Docker Desktop 语境，不在本 phase 扩展到云端多环境。
- 部署语义：优先复用现有脚本与 Procfile 入口（`scripts/ops/start.sh` / `scripts/app_up.sh` 等），在其之上定义 deploy/verify/rollback 的 operator 视角，而不是另起一套完全不同的部署链。
- 验证语义：尽量沿用 `S6A` drills/evidence 里的 PASS/FAIL 语义与低基数字段，用 "post-deploy verification gate" 语言来描述。
- 回滚语义：优先定义“如何安全退回到上一个已知良好状态”的 operator path，可以是 Git 层、配置层或 runtime 层的回滚，不要求一次性覆盖所有维度。

## Definitions (optional)

- **Deploy runtime path**：在给定环境（本 phase 先聚焦 dev/test）下，把一组服务从 "未运行" 或 "旧版本" 推进到 "新版本并通过基本验证" 的操作序列，可以是脚本、命令或 CI 入口。
- **Post-deploy verification**：在 deploy 之后，通过 health/status/drills 等手段，确认关键服务和依赖处于可继续操作状态的检查集合。
- **Rollback path**：当 post-deploy verification 失败或观察到明显退化时，用于将系统恢复到上一个已知良好状态的可重复入口。
- **Runtime gate**：结合 deploy / verify / rollback 的硬性检查点，用来阻断不安全变更或引导 operator 执行回滚动作。

## Constraints

- 不引入生产级蓝绿 / canary / traffic shifting 等复杂机制；以本地 dev/test 环境的可讲样本为主。
- 不在本 phase 内重写 CI/CD 平台，而是围绕现有 GitHub Actions / scripts 补最小 deploy/verify/rollback 语义。
- 所有新的脚本和入口命名必须能直接翻译成 `deployment / operational support / maintenance / recoverability` 语言，并与 `S4A-1A` 的 `start / stop / status / health / logs / env_prep` 保持一致风格。
- 若定义 evidence JSON 或 drills 结果，字段必须尽量低基数，可机械判定，方便与 `S6A` spine 兼容。

## Scope

- `P0`: contract（deploy 入口分类、post-deploy verification/rollback 语义、最小 evidence 口径）
- `P1`: implementation / scripts（deploy / verify / rollback 脚本或命令入口）
- `P2`: drill / verify（至少 1 条 deploy+verify+rollback 路径可复跑）
- `P3`: docs / operator wording（把 deploy/verify/rollback 入口翻译成 systems/platform operations 语言）

## Success Criteria (DoD)

- 明确一组最小 deploy 入口分类（例如：`deploy_app`, `deploy_db_migrations`, `deploy_runtime_bundle`），以及对应输入和成功/失败语义。
- 至少定义 1 条典型的 `deploy -> post-deploy verify -> optional rollback` 路径，覆盖 API + DB + UI 中的关键子集。
- 至少形成 1 套可机械判定的 post-deploy verification 结果（例如基于 `scripts/ops/health.sh` / drills 输出）。
- 至少定义 1 条可执行的 rollback path（哪怕是围绕 Git revert + 再 deploy 这一层），并给出 operator 视角的边界说明。
- 在 wording 上，能把这一 phase 翻译成 `deployment safety / change verification / rollback readiness` 语言，以便写入申请材料与 runbook。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 deploy/verify/rollback contract、脚本入口与 operator wording 已稳定，并且不会因为后续小改动频繁变更主语义。
  - Evidence 区至少记录 1~2 条成功的 deploy+verify 链路，以及至少 1 条触发 rollback 的演练样本（包含 headSha + artifact path / CI run URL）。

## P0 (Contract | v1)

### P0-C1-S1 (Deploy entry categories | v1)

- 初步计划的 deploy 入口分类（名称先按 operator 语义定义，后续由脚本实现对齐）：
  - `deploy_app`: 面向 API + UI (+ worker) 的应用层发布入口，默认封装现有 `scripts/ops/start.sh` / `scripts/app_up.sh` / `Procfile.*` 语义，用于把一组 app 进程从“未运行或旧版本”切换到“新版本已起且可验证”。
  - `deploy_db_migrations`: 面向 dev/test schema 迁移的入口，围绕 `scripts/db_migrate.sh` 和既有 migration 流程，将“应用新的 DB schema 变更并验证通过”收敛成可复跑脚本。
  - `deploy_runtime_bundle`: 预留给后续“打包 + 分发 + 启动”一条龙脚本（例如 WSL -> Windows 的简化安装脚本），把 env_prep + infra/db/app 启动封装成一个半自动安装/更新入口。
- 每个 deploy 入口都应明确：
  - 输入参数（如 `ENV_NAME=dev|test`、`--no-worker`、`--dry-run` 等）；
  - 预期影响范围（API / DB / UI / worker / infra）；
  - 成功标准（哪些健康检查/状态检查必须通过）与 failure 语义（失败时是否自动尝试 rollback，还是仅提示 operator）。

### P0-C1-S2 (Post-deploy verification & rollback semantics | v1)

- Post-deploy verification：
  - 默认通过 `scripts/ops/status.sh` 与 `scripts/ops/health.sh` 组合完成，必要时补充 drills（例如针对关键 API 的 smoke test）。
  - 输出需要能给出明确的 PASS/FAIL 决策，以及关键摘要（API / DB / UI / worker / ES 的 HTTP/status/health 汇总），便于 operator 在几秒钟内判断是否继续推进或触发回滚。
- Rollback 语义：
  - v1 默认以“回到上一个已知良好 Git 版本 + 重新执行对应 deploy_*** 入口”作为最小 rollback path，并在 log 中记录被回滚的 headSha 与目标 headSha。
  - 如未来引入配置层或数据层的细粒度回滚（例如恢复上一版 env file / 还原备份 snapshot），则在后续 cycle 中扩展，不在 v1 内一次性解决。

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON / drills 结果至少应包含（字段命名尽量与 `S6A` 兼容）：
  - `phase_id` / `script_kind` / `script_name`（例如 `S4A-2A`, `deploy_app`, `scripts/ops/deploy_app.sh`）；
  - `env_name` 与关键输入参数（如 `env_name=dev`、`no_worker=true`、`dry_run=false`）；
  - `target_head_sha` 与实际部署到的 `deployed_head_sha`（若两者不一致需在 observed 中说明原因，例如 dry-run）；
  - `post_deploy_result`（`PASS` / `FAIL` / `ROLLBACKED` 等低基数状态）以及关键摘要字段（例如 `api_health=200`、`ui_http=200`、`db_container=healthy`）；
  - 若触发 rollback：`rollback_entrypoint`（脚本或命令）、`rollback_to_head_sha`、rollback 之后的最终状态摘要（同样使用低基数字段）。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4A-2A/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`）或同一 phase / cycle 下连续 steps 的组合（如 `1S2`）。

**Branch convention**:

- `S4A-2A` 相关实现与文档默认仍落在 `S4A-systems-platform-operations-runtime-foundation` 分支；如有必要，可在其下开短生命周期子分支。
- 与 `S0D` 相关的 docs/automation 仍沿用 `S0D-docs-management-v4`，不与 `S4A` phase 改动混线。

**Commit discipline (recommended)**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4A-systems-platform-operations-runtime-foundation`。

## Plan (draft)

### P1 (Implementation / scripts)

- P1-C1-S1: 盘点当前仓库中已有的 deploy / verify / rollback 相关入口（例如 GitHub Actions、`scripts/db_migrate.sh`、`scripts/ops/health.sh` 等），并整理到本 log。
- P1-C1-S2: 在盘点结果的基础上，设计并命名最小 deploy/verify/rollback 脚本集合（优先 `scripts/ops/` 目录下的新入口）。
- P1-C1-S3: 在不破坏现有 `start/app_up` 前台运行语义的前提下，选择至少 1 条适合收口成 `deploy -> verify` 的路径，并为其实现首批脚本样本（可以是“启动与验证分离”的两步式）。

### P1-C1-S1 (Existing deploy/verify/rollback entrypoints | inventory)

- 本地脚本层：
  - 启动链：`scripts/ops/start.sh`（封装 `env_prep / infra_up / db_up / up / app_up`）、`scripts/up.sh`、`scripts/app_up.sh`、`scripts/db_up.sh`、`scripts/infra_up.sh`、`scripts/preflight.sh`。
  - 迁移与 DB：`scripts/db_migrate.sh`（按 env 运行 Alembic/db migration）、`docker-compose.devtest-db.yml` 下的 `db_devtest` 服务（通过 `scripts/db_up.sh` 管理）。
  - 验证链：`scripts/ops/status.sh`（runtime 摘要）、`scripts/ops/health.sh`（post-start verification gate，聚合 API/DB/UI/ES/worker 状态）。
  - 关闭链：`scripts/ops/stop.sh`（受控关闭 docker-managed runtime）、`scripts/ops/logs.sh`（incident triage 日志入口）。
- Git / CI 层：
  - Git：当前所有 deploy 相关操作默认以 `git` HEAD 为单位（本 phase 将在脚本中显式记录 `target_head_sha` / `deployed_head_sha`）。
  - GitHub Actions：`.github/workflows/` 下已有 `drill-*` / `hard-gate-*` / `reusable-*` 等 workflows，主要负责 drills / evidence / hard gate 执行；S4A-2A 不在 v1 内重写这些 CI，而是复用其 evidence 语义，在需要时新增 "deploy + post-deploy verify" 风格的 workflow。
- 回滚相关：
  - 当前实际 rollback 动作主要依赖 Git 操作（revert / reset）与手工重新运行 `start`/drills；本 phase 将在 contract 层把这一模式显式命名为最小 rollback path，并预留 future-work 钩子去接 DB/配置级别的细粒度回滚。

### P1-C1-S2 (Minimal script set | design)

- 首轮脚本集合（设计层）：
  - `scripts/ops/deploy_app_verify.sh`：
    - 语义：在 app 已通过 `scripts/ops/start.sh dev app [--no-worker]` 启动的前提下，执行一轮标准化的 post-deploy verification gate（基于 `status` + `health`），并按 P0 定义输出低基数的 PASS/FAIL 摘要；未来可扩展为生成 evidence JSON。
    - 理由：不改变现有 `app_up` 前台阻塞语义，把 deploy 拆成“启动由 start 负责 + verify 由 deploy_*_verify 负责”的两步式，更符合当前 WSL + honcho 使用方式。
  - `scripts/ops/deploy_db_migrations.sh`（占位）：
    - 语义：封装一条对 dev/test 运行 `scripts/db_migrate.sh` 的路径，附带最小前置检查和结果摘要；首轮可以先只在 log 中定义，不必须立即实现脚本。
  - `scripts/ops/deploy_runtime_bundle.sh`（占位）：
    - 语义：预留给后续 "打包 + 分发 + 启动" 的一键式 runtime 安装/更新路径（例如 Windows 侧同事只需跑一条命令即可完成 env_prep + infra/db/app）。
- 设计约束：
  - 不改变 `scripts/up.sh` / `scripts/app_up.sh` 已有的“前台长跑 + Ctrl+C 退出”行为；新脚本更像“在现有运行面的上方增加 deploy/verify/rollback 语义层”。
  - deploy_*_verify 脚本优先实现“检查 + 摘要 + 退出码”，evidence JSON 的实际落地可以放在 P2 drill / verify 阶段。

### P1-C1-S3 (First script sample | implemented 2026-03-21)

- 首批实现脚本：`scripts/ops/deploy_app_verify.sh`
  - 入口：`./scripts/ops/deploy_app_verify.sh [dev|test]`
  - 行为：
    - 通过 `_common.sh` 解析 env（`resolve_env_name`）并定位 `REPO_ROOT`；
    - 读取当前 `HEAD_SHA=git rev-parse HEAD`，以 `phase=S4A-2A env=<env> target_head_sha=<sha>` 形式打印摘要；
    - 依次调用 `scripts/ops/status.sh <env>` 与 `scripts/ops/health.sh <env>`，捕获各自退出码但不中断执行；
    - 若两者均退出码为 0，则输出 `POST_DEPLOY_RESULT=PASS` 并以 0 退出；否则输出 `POST_DEPLOY_RESULT=FAIL` 及 `status_rc` / `health_rc`，并以非 0 退出。
  - 设计意图：
    - 把 `S4A-1A` 已有的 `status` / `health` 组合提升为一条可复跑的 post-deploy verification gate，而不改变 `start/app_up` 的前台运行语义；
    - 为后续 P2 evidence JSON 奠定字段口径（`phase_id` / `target_head_sha` / `post_deploy_result` 等），当前以人类可读摘要先行。

### P2 (Drill / Verify)

- P2-C1-S1: 设计并执行至少 1 条正常的 deploy+verify 演练，记录 expected/observed 摘要。
- P2-C1-S2: 设计并执行至少 1 条需要 rollback 的演练（例如故意注入错误配置），并记录 rollback 行为和结果。

### P3 (Docs / Operator wording)

- P3-C1-S1: 把 deploy/verify/rollback 入口改写成 systems/platform operations 语言，并与 `S4A-1A` 的 operator wording 对齐（例如 `post-deploy verification gate`、`runtime rollback path`）。
- P3-C1-S2: 起草 `docs/runbook/run-S4A-2A-deploy-verify-rollback-runtime-path.md`，为值班 / 运行支持提供薄 runbook。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: deploy 入口分类与命名 contract
- [x] `P0-C1-S2`: post-deploy verification / rollback 语义 contract
- [x] `P0-C1-S3`: 最小 evidence 口径

### P1 (Implementation / scripts)

- [x] `P1-C1-S1`: 盘点现有 deploy/verify/rollback 相关入口
- [x] `P1-C1-S2`: 设计最小脚本集合
- [x] `P1-C1-S3`: 实现首批脚本样本

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: 正常 deploy+verify 演练
- [ ] `P2-C1-S2`: 带 rollback 的演练

### P3 (Docs / Operator wording)

- [ ] `P3-C1-S1`: operator-facing wording 收口
- [ ] `P3-C1-S2`: runbook 草稿

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P2-C1-S1 (reserved | 2026-03-21)

- headSha: ``
- artifacts: ``
- expected:
  - 待定：至少 1 条正常 deploy+verify 链路。
- observed:
  - （本 phase scaffold 时留空，后续补充实测结果。）

### P2-C1-S2 (reserved | 2026-03-21)

- headSha: ``
- artifacts: ``
- expected:
  - 待定：至少 1 条需要 rollback 的演练链路。
- observed:
  - （本 phase scaffold 时留空，后续补充实测结果。）

## Recent changes (for traceability, optional)

- 2026-03-21: scaffolded `S4A-2A` as the second `S4A` phase, focusing on deploy / verify / rollback runtime paths building on top of the `S4A-1A` ops scripting baseline.
