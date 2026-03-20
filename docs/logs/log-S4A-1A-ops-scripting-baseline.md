# log-S4A-1A (Phase 1: Ops Scripting Baseline)

---

**id**: `S4A-1A`
**kind**: `log`
**title**: `ops scripting baseline (start/stop/status/health/logs/env prep) + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, Operations, Runtime, Bash, Automation, Drills, Evidence, epic/s4, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md`
  **previous_log**: ``
  **reference_log_1**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_2**: `docs/logs/log-S5A-3B-object-storage-backup.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
**created**: `2026-03-20`
**updated**: `2026-03-20`

---

## Decision / Outcome

**Decision**:

- `S4A-1A` 作为 `S4A` 的首个 phase，优先补 `ops scripting baseline`，而不是先补 Terraform 或 Kubernetes。原因是它最贴近岗位明示的 `PowerShell / Bash`、`operational support`、`monitoring`、`maintenance` 语言，并且最容易在 6 天窗口内形成可讲样本。
- 本 phase 的默认交付范围收敛为一套最小运行脚本与口径：`start / stop / status / health / logs / env prep`，后续 phase 再接 deploy/rollback、backup/recovery、hybrid runtime awareness。

**Default choices (phase defaults / v1)**:

- 脚本优先语言：`Bash`。
- 脚本目标环境：优先覆盖本地 dev/test 和最小 runtime support 语境，不追求生产级 orchestration。
- 输出目标：优先形成“能说得出口的运维/运行支持样本”，其次才是抽象化复用。
- 证据基线：脚本后续若进入正式执行，应尽量产出 machine-verifiable 的检查结果（JSON / logs / exit codes），以便与既有 evidence 体系接轨。

## Definitions (optional)

- **Ops scripting baseline**：用于支撑最小运行支持语境的一组稳定脚本入口，包括启动、停止、状态检查、健康检查、日志查看和环境准备。
- **Runtime support**：聚焦服务是否可启动、可检查、可排障、可恢复，而非完整云平台编排。
- **Health check**：能快速判断关键服务、依赖或入口是否处于可继续操作状态的检查脚本或命令。
- **Env prep**：把运行所需的本地依赖、目录、配置和前置检查收敛成可重复执行的脚本步骤。

## Constraints

- 先补最小可用脚本，不追求跨平台大而全支持。
- 先用 Bash 补最直接命中的能力，PowerShell awareness 可在后续补充，不在本 phase 作为主交付物。
- 脚本应优先围绕现有 `wordloom-v3` 运行面组织，避免脱离仓库实际情况写空泛样板。
- 若后续接入 evidence，结果字段必须尽量低基数、可机械判定。

## Scope

- `P0`: contract（脚本分类、命名、退出语义、最小 evidence 口径）
- `P1`: implementation / scripts（start / stop / status / health / logs / env prep）
- `P2`: drill / verify（至少验证 1~2 条关键脚本路径可复跑）
- `P3`: docs / operator wording（把脚本入口翻译成 systems/platform operations 语言）

## Success Criteria (DoD)

- 明确一组最小脚本分类：`start`、`stop`、`status`、`health`、`logs`、`env_prep`。
- 至少定义每类脚本的预期目标、输入和成功/失败语义。
- 至少挑选 1 条关键服务路径，后续可通过脚本完成启动或检查。
- 至少挑选 1 条健康或日志检查路径，后续可作为 operational support sample。
- 脚本命名和入口说明应能被直接翻译到申请材料中的 `operational support / maintenance / monitoring` 语言。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的脚本 contract、最小脚本集合与 operator wording 已稳定。
  - Evidence 区至少记录 1~2 条成功演练或验证样本（headSha + artifact path / terminal proof / CI run URL）。

## P0 (Contract | v1)

### P0-C1-S1 (Script categories | v1)

- `start`: 启动本地或最小 runtime 所需服务。
- `stop`: 停止对应服务并尽量保持状态可清理。
- `status`: 返回关键服务当前状态与必要摘要。
- `health`: 执行最小健康检查，给出可继续操作的判断。
- `logs`: 提供关键日志查看入口。
- `env_prep`: 运行前置环境检查或准备动作。

### P0-C1-S2 (Exit semantics | v1)

- 成功：退出码 `0`。
- 预期失败但可识别：非 `0`，并尽量输出简洁、低基数原因。
- 脚本应避免把高基数原始错误直接当成结构化状态字段。

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON 后续至少应包含：
  - 脚本类别与脚本名
  - 关键输入参数（若有）
  - PASS / FAIL 决策
  - 关键输出路径或检查摘要

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4A-1A/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`）或同一 phase / cycle 下连续 steps 的组合（如 `1S2`）。

**Branch convention**:

- `S4A-1A` 相关实现与文档优先落在 `S4A-systems-platform-operations-runtime-foundation` 分支。
- `S0D` 相关 docs/automation 仍沿用 `S0D-docs-management-v4`，不与 `S4A` phase 改动混线。

**Commit discipline (recommended)**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4A-systems-platform-operations-runtime-foundation`。

## Plan (draft)

### P1 (Implementation / scripts)

- P1-C1-S1: 盘点 `wordloom-v3` 当前最适合抽成 ops scripting baseline 的入口（start/stop/status/health/logs/env prep）
- P1-C1-S2: 选择一批最小脚本样本并固化命名与目录约定

### P1-C1-S1 (Inventory | implemented 2026-03-20)

- `env_prep`
  - 现有真实入口：`scripts/preflight.sh`
  - 收口入口：`scripts/ops/env_prep.sh`
  - 语义：检查 WSL / docker / PowerShell / honcho / env file / Procfile / 关键端口与 tracing 依赖。
- `start`
  - 现有真实入口：`scripts/up.sh`、`scripts/infra_up.sh`、`scripts/db_up.sh`、`scripts/app_up.sh`
  - 收口入口：`scripts/ops/start.sh`
  - 语义：按 `all | infra | db | app | env_prep` 目标启动最小 runtime。
- `status`
  - 新增入口：`scripts/ops/status.sh`
  - 语义：输出 dev/test env file、db 容器健康态、infra ES 容器态、API/UI/worker/ES 的 HTTP 状态码摘要。
- `health`
  - 现有真实入口：API `/api/v1/health`、worker `/healthz` / `/readyz`
  - 新增入口：`scripts/ops/health.sh`
  - 语义：对 db、API、UI、ES 做可机械判定检查；若 worker 在 env 中启用，则额外检查 `/healthz` 和 `/readyz`。
- `logs`
  - 新增入口：`scripts/ops/logs.sh`
  - 语义：统一 tail docker-managed db/infra/es/minio 等日志；app logs 明确回到 honcho 前台终端。
- `stop`
  - 新增入口：`scripts/ops/stop.sh`
  - 语义：停止 docker-managed `db | infra | all`；对 Procfile app 进程显式保留“前台终端 Ctrl+C”语义，避免粗暴 kill 误伤。

### P1-C1-S2 (Minimal script set | implemented 2026-03-20)

- 目录约定：`scripts/ops/`
- 首批样本：
  - `scripts/ops/_common.sh`
  - `scripts/ops/env_prep.sh`
  - `scripts/ops/start.sh`
  - `scripts/ops/stop.sh`
  - `scripts/ops/status.sh`
  - `scripts/ops/health.sh`
  - `scripts/ops/logs.sh`
- 设计约束：
  - 不重写已有启动链，而是薄封装现有 `preflight/up/app_up/db_up/infra_up`。
  - `status` 偏摘要输出，`health` 偏 PASS/FAIL 判定，避免把两个语义混在一起。
  - `stop` 只处理 docker-managed runtime，避免对前台 app 进程使用高风险进程匹配杀进程策略。

### P2 (Drill / Verify)

- P2-C1-S1: 至少验证 1 条启动/状态或健康检查链路可复跑
- P2-C1-S2: 记录最小 evidence（headSha + output / path / observed summary）

### P2-C1-S1 (Replayable startup/status path | implemented 2026-03-20)

- 已验证可复跑链路：`env_prep -> start infra es -> start db -> status`
- 执行环境：WSL (`Ubuntu`) + Docker Desktop
- 实际结果：
  - `scripts/ops/env_prep.sh dev` -> PASS
  - `scripts/ops/start.sh dev infra es` -> PASS
  - `scripts/ops/start.sh dev db` -> PASS
  - `scripts/ops/status.sh dev` -> PASS（可稳定输出当前 runtime 摘要）
- 关键 observed summary：
  - `db_container=healthy`
  - `infra_es=healthy`
  - `es_http=200`
  - `api_health=000`
  - `ui_http=000`
- 补充观察：`scripts/ops/start.sh dev all --no-worker` 在本机 WSL 环境下未形成完整成功链路；失败点不在 db/migrate，而在 UI 启动阶段，命中 `cross-env` 未被解析。

### P2-C1-S2 (Evidence | implemented 2026-03-20)

- 证据形式：terminal proof
- 关键命令：
  - `wsl.exe -e bash -lc "cd /mnt/d/Project/wordloom-v3 && ./scripts/ops/env_prep.sh dev"`
  - `wsl.exe -e bash -lc "cd /mnt/d/Project/wordloom-v3 && ./scripts/ops/start.sh dev infra es && ./scripts/ops/start.sh dev db && ./scripts/ops/status.sh dev"`
- blocker proof：
  - `wsl.exe -e bash -lc "cd /mnt/d/Project/wordloom-v3 && ./scripts/ops/start.sh dev all --no-worker"`
  - observed blocker: WSL 中 `npm` 解析到 `/mnt/c/Program Files/nodejs//npm`，UI 启动阶段报 `'cross-env' ... 不是内部或外部命令`，导致 honcho 终止整条 app 链路。

### P3 (Operator wording)

- P3-C1-S1: 把脚本入口说明改写成 systems/platform operations 语言
- P3-C1-S2: 对齐 roadmap 和后续申请材料用语

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: 脚本分类 contract（start / stop / status / health / logs / env_prep）
- [x] `P0-C1-S2`: 退出语义 contract
- [x] `P0-C1-S3`: 最小 evidence 口径

### P1 (Implementation / scripts)

- [x] `P1-C1-S1`: 盘点当前仓库最适合抽成 ops scripts 的入口
- [x] `P1-C1-S2`: 形成首批最小脚本样本

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: 验证至少 1 条关键脚本路径
- [x] `P2-C1-S2`: 记录最小 evidence

### P3 (Operator wording)

- [ ] `P3-C1-S1`: 形成 systems/platform operations 语言说明

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P2-C1-S1 (reserved | 2026-03-20)

- headSha: `9f208dd7a05c1e7aa057706ca3cc2581475d9649`
- artifacts: `terminal proof (WSL env_prep + infra/db/status replay); no dedicated artifact file produced in this first pass`
- expected:
  - 至少 1 条最小脚本路径可复跑
  - 能输出清晰、低基数的成功/失败判断
- observed:
  - `env_prep -> infra es -> db -> status` 可复跑
  - `db_container=healthy`
  - `infra_es=healthy`
  - `es_http=200`
  - `api_health=000` / `ui_http=000`（本次未把 app 作为成功链路的一部分）
  - `start.sh dev all --no-worker` 暴露额外 blocker：WSL 下命中 Windows `npm`, UI 阶段 `cross-env` 未解析，需在后续 step 处理

## Recent changes (for traceability, optional)

- 2026-03-20: scaffolded `S4A-1A` as the first `S4A` phase, prioritizing ops scripting baseline over broader cloud/runtime topics to match the government-role timeline and wording.
- 2026-03-20: implemented `P1-C1-S1/S2` by inventorying runtime entrypoints and adding a first `scripts/ops/` wrapper set for `env_prep/start/stop/status/health/logs`.
- 2026-03-20: completed first `P2` pass with a replayable `env_prep + infra + db + status` chain and recorded the WSL `npm/cross-env` blocker on the full `all --no-worker` app path.