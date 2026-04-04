# log-S4A-2A (Phase 2: Deploy / Verify / Rollback Runtime Path)

---

**id**: `S4A-2A`
**kind**: `log`
**title**: `deploy / verify / rollback runtime path + drills/evidence v1`
**status**: `stable`
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
**roadmap_path**: `docs/roadmap/road-001-01-gov-role-minimal-ops-loop.md`
**roadmap_milestone**: `M4`
**roadmap_phase**: `M4-P0`
**roadmap_bridge_refs**: `docs/roadmap/road-001-01-gov-role-minimal-ops-loop.md#M4-P0`
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

### P2-C1-S1 (Happy-path deploy+verify drill | plan)

- 目标：定义一条标准的 "deploy -> post-deploy verify" happy-path 演练，验证 `deploy_app_verify` gate 在 app 正常运行时稳定给出 PASS 结果，并可复跑。
- 推荐路径：
  - 步骤 1（环境准备）：
    - `wsl.exe -e bash -lc "cd /mnt/d/Project/wordloom-v3 && ./scripts/ops/env_prep.sh dev"`
  - 步骤 2（冷启动 runtime）：
    - `wsl.exe -e bash -lc "cd /mnt/d/Project/wordloom-v3 && ./scripts/ops/start.sh dev infra es"`
    - `wsl.exe -e bash -lc "cd /mnt/d/Project/wordloom-v3 && ./scripts/ops/start.sh dev db"`
  - 步骤 3（app warm-start）：
    - 在 WSL 终端前台执行：`./scripts/ops/start.sh dev app --no-worker`
      - 保持该终端前台运行（honcho 进程树在其中），只在需要关闭时 Ctrl+C。
  - 步骤 4（post-deploy verification gate）：
    - 在 Windows 侧 PowerShell 或另一 WSL 终端中执行：
      - `bash scripts/ops/deploy_app_verify.sh dev`
- 预期：
  - `deploy_app_verify.sh dev` 能稳定完成一轮 `status + health` 检查，并输出 `POST_DEPLOY_RESULT=PASS`，退出码为 0。
  - 输出中至少包含 `phase=S4A-2A env=dev target_head_sha=<sha>` 与关键组件状态摘要（来自 status/health）。
- 记录方式：
  - 在 Evidence 区新增一条 `P2-C1-S1` 记录，填写 headSha、使用的命令、expected/observed 摘要，并可在后续迭代中补充 JSON artifact 路径。

### P2-C1-S2 (Rollback drill | implemented 2026-03-21)

- 目标：设计一条可控的 "post-deploy verify 失败 -> 触发 rollback -> 恢复到已知良好版本" 演练，验证 rollback 语义和 evidence 口径。
- 推荐场景（配置级回滚样本）：
  - 步骤 1（基线状态）：按 `P2-C1-S1` 的步骤 1~4，先确保当前 HEAD 在 dev 环境下能够通过 `deploy_app_verify`（PASS）。
  - 步骤 2（注入可逆配置错误）：
    - 修改 `.env.dev` 中与 API 或 UI 可用性相关的一个配置（例如把 API_PORT 改成与已有端口冲突的值，或错误的后端 URL），并 `git commit` 或至少 `git diff` 记录该变更点。
  - 步骤 3（观察失败）：
    - 重新执行 `env_prep`（如有必要）和 `start.sh dev app --no-worker`，然后在独立终端再次运行 `bash scripts/ops/deploy_app_verify.sh dev`，预期得到 `POST_DEPLOY_RESULT=FAIL`，并在 status/health 输出中看到明确的失败信号（例如 API health 000 / 5xx）。
  - 步骤 4（执行 rollback）：
    - 在 Git 层执行 rollback，例如：`git restore .env.dev` 或 `git revert` 对应的错误 commit，使工作区回到上一个已知良好配置版本；
    - 如有需要，重新跑一遍 `env_prep` 和 `start`，然后第三次执行 `bash scripts/ops/deploy_app_verify.sh dev`，预期恢复为 `POST_DEPLOY_RESULT=PASS`。
- 预期：
  - Evidence 能清楚体现：
    - 失败前后的 `headSha` / `target_head_sha`；
    - 出错配置的简要说明（低基数字段，例如 `rollback_reason=config_error_api_port`）；
    - rollback 使用的入口（例如 `git restore .env.dev`）和最终恢复后的 `POST_DEPLOY_RESULT=PASS` 摘要。
- 记录方式：
  - 在 Evidence 区新增 `P2-C1-S2` 记录，包含三次关键命令（baseline PASS / injected FAIL / rollback 后 PASS）、对应 headSha，以及简要 expected/observed。

### P3 (Docs / Operator wording)

- P3-C1-S1: 把 deploy/verify/rollback 入口改写成 systems/platform operations 语言，并与 `S4A-1A` 的 operator wording 对齐（例如 `post-deploy verification gate`、`runtime rollback path`）。
- P3-C1-S2: 起草 `docs/runbook/run-S4A-2A-deploy-verify-rollback-runtime-path.md`，为值班 / 运行支持提供薄 runbook。

### P3-C1-S1 (Operator-facing wording | implemented 2026-03-21)

- Operator 视角下的主语义：
  - `deploy_app_verify`: post-deploy verification gate（发布后验证闸门），用于在 dev/test 环境中给出低基数的 `POST_DEPLOY_RESULT=PASS|FAIL`；
  - `POST_DEPLOY_RESULT`: deployment outcome（发布结果），可作为 CI / 值班决策的直接信号；
  - `rollback path`: runtime rollback path（运行时回滚路径），当前以 env/Git 层的最小可重复模式为主，而非数据级别回滚；
  - 整体 Phase 语言：`deployment safety / change verification / rollback readiness for local dev/test`。
- 与 `S4A-1A` 对齐的 wording 映射：
  - `start` / `env_prep` 仍然归 S4A-1A：分别是 environment readiness check 和 cold/warm-start runtime path；
  - `status` / `health` 在 S4A-2A 中被提升为 deploy 后的 runtime summary 与 post-deploy verification gate 组成部分；
  - `deploy_app_verify` 则是“站在 operator 视角，把 status+health 组合成一条 post-deploy gate 的专用入口”。
- 对外材料（roadmap / 申请材料）中可使用的简写：
  - "local dev/test deploy safety + post-deploy verification gate + rollback readiness"；
  - "one thin post-deploy gate script (deploy_app_verify) with env/Git-based rollback pattern"。

### P3-C1-S2 (Runbook draft | implemented 2026-03-21)

- Runbook 位置：`docs/runbook/run-S4A-2A-deploy-verify-rollback-runtime-path.md`。
- Runbook 主体：
  - section 1/2：明确本 runbook 只覆盖本地 dev/test 环境的 deploy/verify/rollback，强调是建立在 `S4A-1A` ops scripting baseline 之上的“薄层”；
  - section 3：把 Evidence bundle 收口到 phase log 与 `deploy_app_verify` 的 `POST_DEPLOY_RESULT`、status/health 摘要上；
  - section 4：用 operator 语言描述 `deploy_app_verify` 的行为与使用方法（包含成功/失败标准，以及可调的 env 输入）；
  - section 5：给出本地操作样例，包括“deploy+verify”与“config-level / Git-level rollback” 两类模式；
  - section 6：列出若干高价值故障模式（status_rc!=0 / health_rc!=0 / api_health DOWN 等），并指向首选排查命令或 log 入口；
  - section 7：说明边界（仅 dev/test、无数据级回滚、不替代 S6A/S3A 的 CI hard-gate），以及未来可能扩展点（`deploy_db_migrations`、JSON evidence、CI workflow 调用等）。

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

- [x] `P2-C1-S1`: 正常 deploy+verify 演练
- [x] `P2-C1-S2`: 带 rollback 的演练

### P3 (Docs / Operator wording)

- [x] `P3-C1-S1`: operator-facing wording 收口
- [x] `P3-C1-S2`: runbook 草稿

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P2-C1-S1 (reserved | 2026-03-21)

- headSha: `1555803fd9a82f3f6805d25891b25846076c604b`
- artifacts: `terminal proof (PowerShell -> WSL deploy_app_verify.sh dev; env_prep/start app 已在此前多次验证，本次重点验证 post-deploy gate 行为)`
- expected:
  - 在 dev 环境下，已按 `S4A-1A` 路径成功拉起 db/infra/app 时，`bash scripts/ops/deploy_app_verify.sh dev` 能顺利完成 `status + health` 检查，并给出 `POST_DEPLOY_RESULT=PASS`，退出码为 0；
  - 输出中包含 `phase=S4A-2A env=dev target_head_sha=<sha>` 以及 runtime 摘要（API/DB/UI/ES 皆为绿色，worker 关闭）。
- observed:
  - 实际命令：`bash scripts/ops/deploy_app_verify.sh dev`
  - 关键输出：
    - `phase=S4A-2A env=dev target_head_sha=1555803fd9a82f3f6805d25891b25846076c604b`
    - `api_health 200`、`ui_http 200`、`es_http 200`、`db_container healthy`；
    - `worker runtime is disabled by env (SEARCH_OUTBOX_WORKER_ENABLED=0)`；
    - `POST_DEPLOY_RESULT=PASS`，脚本退出码为 0。
  - 结论：在当前 headSha 下，`deploy_app_verify` 能作为 post-deploy verification gate 稳定给出 PASS，符合预期。

### P2-C1-S2 (reserved | 2026-03-21)

- headSha: `279a66861dfd44ef034f3b3261bc8f294960546f`
- artifacts: `terminal proof (WSL bash scripts/ops/deploy_app_verify.sh dev; .env.dev 中 API_PORT 从 30001 -> 39999 -> 30001 的一次往返)`
- expected:
  - 在 dev 环境基线为 PASS（`deploy_app_verify` 正常）的前提下，临时把 `.env.dev` 中的 `API_PORT` 改为一个没有进程监听的端口（39999），会导致：
    - `scripts/ops/health.sh dev` 中的 `api_health` 检查失败（HTTP 000 / DOWN）；
    - `scripts/ops/deploy_app_verify.sh dev` 汇总结果为 `POST_DEPLOY_RESULT=FAIL`，退出码为非 0；
  - 将 `.env.dev` 中的 `API_PORT` 恢复为 30001 后，再次运行 `health.sh` / `deploy_app_verify.sh`，预期恢复为 PASS。
- observed:
  - 基线确认：
    - 命令：`bash scripts/ops/deploy_app_verify.sh dev`
    - 关键输出：
      - `phase=S4A-2A env=dev target_head_sha=279a66861dfd44ef034f3b3261bc8f294960546f`
      - `POST_DEPLOY_RESULT=PASS`（status/health 各子检查均 OK）。
  - 注入配置错误（API_PORT 39999）：
    - 修改 `.env.dev`：`API_PORT=30001 -> API_PORT=39999`；
    - `bash scripts/ops/health.sh dev`：
      - `[ops] db_devtest OK (healthy)`；
      - `[ops] api_health DOWN (http://127.0.0.1:39999/api/v1/health)`；
      - 脚本退出码为非 0；
    - `bash scripts/ops/deploy_app_verify.sh dev`（在修正脚本逻辑后）：
      - status 摘要中 `api_health 000`；
      - health 阶段同样输出 `api_health DOWN (http://127.0.0.1:39999/api/v1/health)`；
      - 最终输出 `POST_DEPLOY_RESULT=FAIL status_rc=0 health_rc=1`，脚本退出码为非 0。
  - 回滚配置并验证恢复：
    - 回滚入口：手动将 `.env.dev` 中 `API_PORT` 恢复为 30001（本仓库不对 `.env.dev` 入库，因此本例使用“手动恢复 env 配置”为最小 rollback path；若未来引入 `.env.dev.example` 并入库，则可改为 Git 层的 `git restore`/`git checkout`）。
    - `bash scripts/ops/health.sh dev`：
      - `db_devtest OK (healthy)`；`api_health OK (200)`；`ui_http OK (200)`；`es_http OK (200)`；
    - `bash scripts/ops/deploy_app_verify.sh dev`：
      - 再次输出 `POST_DEPLOY_RESULT=PASS`，退出码为 0。
  - 结论：在当前 headSha 下，故意将 `.env.dev` 中 `API_PORT` 配坏可以稳定触发 `deploy_app_verify` 的 FAIL，并通过恢复该配置回到 PASS，形成一条可复现的“配置级 rollback” 样本。

## Recent changes (for traceability, optional)

- 2026-03-21: scaffolded `S4A-2A` as the second `S4A` phase, focusing on deploy / verify / rollback runtime paths building on top of the `S4A-1A` ops scripting baseline.
