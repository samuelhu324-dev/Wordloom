# log-S4C-3A (Phase 3: Connect wordloom-v3 runtimes to cloud dev/test infra)

---

**id**: `S4C-3A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `Cloud dev/test wordloom integration（env + smoke drills） v1`
**status**: `stable`           # draft | stable | archived
**scope**: `S4`
**tags**: `EVOLUTION, Cloud, Terraform, Runtime, Drills, Evidence, epic/s4, sub/3a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4C-cloud-services-and-terraform-epic.md`
  **previous_log**: `docs/logs/log-S4C-2A-cloud-devtest-db-and-storage.md`
  **reference_log_1**: `docs/logs/_template-log-phase-drills-evidence.md`
**roadmap_path**: `docs/roadmap/road-S1-systems-platform-ops-roadmap-v5.md`
**roadmap_milestone**: `M3`
**roadmap_phase**: `M3-P2`
**roadmap_bridge_refs**: `docs/roadmap/road-S1-systems-platform-ops-roadmap-v5.md#M3-P2, docs/roadmap/road-S1-systems-platform-ops-roadmap-v5.md#M3-P3`
**created**: `2026-03-22`
**updated**: `2026-03-23`

---

## Decision / Outcome

**Decision**:

- 在 S4C-2A 已经证明 cloud-dev 网络与 Postgres 生命周期可控之后，继续推进到应用侧：让 wordloom-v3 的本机 runtime 能通过一套单独的 cloud-dev env 配置连接到云上的 DB / 存储；
- 重点不是“部署整套应用到云上”，而是先打通“本机 runtime -> 云上 dev/test infra”的稳定开发路径，并留下 smoke evidence。

**Default choices (phase defaults / v1)**:

- 优先采用仓库根目录 `.env.cloud.dev` 来承接 cloud-dev 连接串，并继续复用现有 `backend/scripts/ops/run_api.sh` / `run_worker.sh` 入口，不引入新的隐式加载路径；
- 先选择最小 smoke path：`run_api.sh .env.cloud.dev` 成功启动并通过 startup env guard，再执行一个独立的 DB-only smoke（`SELECT current_database(), SELECT 1`），暂不在 P1 阶段引入业务写入；
- 如需临时公网访问，只作为 drill 手段，成功后应尽快回收或切回更安全的访问路径。

## Constraints

- 本 phase 不要求把完整应用部署到 AWS，只要求本机 runtime 能稳定访问云上 dev/test infra；
- 所有凭证不得写入仓库，应用层配置通过本地 env 或安全参数注入；
- 每次 smoke drill 需要记录 headSha、env 名称、目标 endpoint 类型和结果摘要。

## Scope

- `P0`: contract（cloud-dev env 命名、配置边界、smoke evidence 约定）。
- `P1`: implementation（为 wordloom-v3 增加/整理 cloud-dev env 配置入口）。
- `P2`: drill / verify（运行一次本机 runtime -> 云上 DB/存储的 smoke drill）。
- `P3`: drill / wording（总结 cloud-dev runtime integration 的 narrative，并与 S4C-2A / road-S1 对齐）。

## Success Criteria (DoD)

- 应用层存在清晰的 cloud-dev 配置入口，不与本地默认 env 混淆；
- 至少完成一次本机 runtime 连接云上 DB 的 smoke drill，并记录 evidence；
- 能明确说明：哪些内容属于 infra（Terraform），哪些属于 runtime config（env / app settings）。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`：cloud-dev env/config contract 固定
- [x] `P0-C1-S2`：smoke evidence contract 固定

### P1（Implementation）

- [x] `P1-C1-S1`：cloud-dev env/config 入口建立
- [x] `P1-C1-S2`：最小 smoke script 或 run path 就绪

### P2（Drill / Verify）

- [x] `P2-C1-S1`：本机 runtime -> 云上 DB smoke drill 入账

### P3（Drill / Wording）

- [x] `P3-C1-S1`：integration narrative 写入 docs

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records head SHA, env/config identifiers, and smoke results.

### P0-C1-S1（S4C-3A skeleton created｜2026-03-22）

- headSha: `<TBD-after-first-S4C-3A-commit>`
- artifacts:
  - `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
- expected:
  - 为 S4C-3A 定义最小目标：从本机 wordloom-v3 runtime 连接 cloud-dev infra，并形成 smoke/evidence 路径。
- observed:
  - 本 skeleton 已创建，等待后续 contract 与 implementation 落地。

### P0-C1-S1（cloud-dev env/config contract fixed｜2026-03-22）

- headSha: `<pending-current-worktree-commit>`
- artifacts:
  - `.env.cloud.dev.example`
  - `backend/scripts/ops/run_api.sh`
  - `backend/scripts/ops/run_worker.sh`
  - `backend/api/app/main.py`
  - `backend/infra/database/env_guard.py`
- expected:
  - cloud-dev 不另起一套启动器，而是复用现有 repo-root env + ops wrapper 体系；
  - cloud-dev env 文件应与 `.env.dev` / `.env.test` 同级，避免 `backend/api/.env` 这类隐式回退路径成为主入口；
  - `WORDLOOM_ENV=dev` 与 cloud-dev 数据库哨兵/库名约定保持一致。
- observed:
  - `run_api.sh` / `run_worker.sh` 都会把相对 env 路径解释为 repo 根目录下的文件，因此 `.env.cloud.dev` 放在仓库根目录最一致；
  - API startup 已内置 `WORDLOOM_ENV` 对 DB 的保护检查，cloud-dev 可以直接复用这套防误连保险丝；
  - 因此 P0 合同固定为：repo-root `.env.cloud.dev` + 现有 ops wrappers + DB guard，不新增隐藏入口。

### P0-C1-S2（cloud-dev smoke evidence contract fixed｜2026-03-22）

- headSha: `<pending-current-worktree-commit>`
- artifacts:
  - `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
  - `backend/scripts/ops/cloud_dev_db_smoke.py`
- expected:
  - 首次 smoke evidence 至少覆盖 env 文件名、masked DATABASE_URL、目标 DB 名、startup 结果和 DB ping 结果；
  - P1 先证明“runtime 能安全连上云 DB”，不要求先做业务写入。
- observed:
  - smoke contract 固定为两段：
    - API path：`./backend/scripts/ops/run_api.sh .env.cloud.dev` 并确认 startup env guard 通过；
    - DB-only path：`python backend/scripts/ops/cloud_dev_db_smoke.py --env-file .env.cloud.dev`，记录 masked URL、`current_database`、`current_user`、`server_addr`、`server_port`、`ping_ok`；
  - 这套证据足以支撑 S4C-3A 的第一轮 runtime integration，而不会过早引入业务数据污染。

### P1-C1-S1（cloud-dev env/config entry created｜2026-03-22）

- headSha: `<pending-current-worktree-commit>`
- artifacts:
  - `.env.cloud.dev.example`
  - `.gitignore`
- expected:
  - 提供一个可复制的 cloud-dev env 模板，但不把真实凭证入库；
  - 明确 cloud-dev 使用独立 API/metrics 端口，避免与本地 dev/test 端口混淆。
- observed:
  - 已新增 `.env.cloud.dev.example`，包含 `WORDLOOM_ENV=dev`、`ENVIRONMENT=cloud-dev`、独立 `API_PORT=30021`、`OUTBOX_METRICS_PORT=9118`、RDS `DATABASE_URL` 模板和默认本地 ES 占位；
  - `.gitignore` 已允许提交 `.env.cloud.dev.example`，但继续忽略真实 `.env.cloud.dev`。

### P1-C1-S2（minimal cloud-dev smoke path prepared｜2026-03-22）

- headSha: `<pending-current-worktree-commit>`
- artifacts:
  - `backend/scripts/ops/cloud_dev_db_smoke.py`
- expected:
  - 提供一个最小、可重复、非业务写入的 cloud-dev smoke 脚本，直接回答“当前 runtime 能不能连上云 DB”。
- observed:
  - 已新增 `backend/scripts/ops/cloud_dev_db_smoke.py`；
  - 该脚本支持 `--env-file .env.cloud.dev`，读取 `DATABASE_URL` 后执行 `current_database/current_user/inet_server_addr/inet_server_port/select 1`，输出脱敏 JSON；
  - 这使得 S4C-3A 在 P2 阶段可以先做 DB connectivity smoke，再决定是否推进到 API 读写或 worker 路径。

### P2-C1-S1（local runtime -> cloud-dev DB/API smoke succeeded｜2026-03-23）

- headSha: `dd50553109f3cf02020046ed3b2d36f01783c0fe`
- artifacts:
  - `.env.cloud.dev`
  - `backend/scripts/ops/cloud_dev_db_smoke.py`
  - `backend/scripts/legacy/run_api_win.py`
  - `backend/infra/database/env_guard.py`
- commands & outcomes（Windows PowerShell，本机 cloud-dev drill）:
  - `Set-Location d:/Project/wordloom-v3/infra/terraform/aws/network; terraform apply -auto-approve`
    - 结果：把 `allowed_postgres_cidrs` 从 `49.196.216.90/32` 更新为当前公网 IP `49.196.236.62/32`；
    - 输出确认：`Apply complete! Resources: 0 added, 1 changed, 0 destroyed.`
  - `Set-Location d:/Project/wordloom-v3; c:/python314/python.exe backend/scripts/ops/cloud_dev_db_smoke.py --env-file .env.cloud.dev`
    - 结果：DB smoke 成功，输出 JSON：
      - `ok = true`
      - `environment = "cloud-dev"`
      - `wordloom_env = "dev"`
      - `current_database = "wlv3_cloud_dev"`
      - `current_user = "wlv3_dev"`
      - `server_port = 5432`
      - `ping_ok = true`
  - `c:/python314/python.exe backend/scripts/legacy/run_api_win.py`
    - 说明：在 Windows 下改用专用 launcher，规避 `psycopg async` 与 `ProactorEventLoop` 的兼容问题；
    - 同时修复 `backend/infra/database/env_guard.py`：当 sentinel 查询失败时先 `rollback()`，避免 startup 检查落入 `InFailedSqlTransaction`；
  - 本机 health probe：`GET http://127.0.0.1:30021/api/v1/health`
    - 返回：`200`
    - body：`{"status":"healthy","version":"1.0.0","infrastructure_available":true,"routers_loaded":11}`
  - `Set-Location d:/Project/wordloom-v3/backend; c:/python314/python.exe -m alembic -c alembic.ini upgrade head`
    - 结果：成功把 cloud-dev RDS schema 迁移到 head，包括 `libraries`、`bookshelves`、`books`、`blocks`、outbox、audit、membership 等基础表；
    - 说明：这一步回答了“为什么健康检查通过，但业务 GET 还可能失败”这个问题。仅有 DB 连通不够，cloud-dev 还必须完成应用 schema migration。
  - 本机 app-level read smoke：`GET http://127.0.0.1:30021/api/v1/libraries`
    - 返回：`200`
    - body 类型：`list`
    - 当前结果：`[]`（空列表）
- observed:
  - S4C-3A 第一轮最小 runtime integration 已打通：本机 `.env.cloud.dev` 可以连上 AWS RDS，且 API 能在 cloud-dev 配置下正常启动并通过健康检查；
  - 本轮阻塞点并不是凭证或 Python 环境，而是公网 IP 白名单漂移；修正 SG allowlist 后，连接恢复；
  - 另外顺手暴露并修复了一个后端真实缺陷：`env_guard` 在 sentinel 表缺失时未 rollback 事务，导致后续 startup 检查异常；
  - 经过 Alembic migration 后，业务只读接口也已返回 `200`，说明这轮已经从“能连上云 DB”推进到“应用层能用 cloud-dev schema 正常读数据”。

### P3-C1-S1（cloud-dev runtime integration narrative written｜2026-03-23）

- headSha: `dd50553109f3cf02020046ed3b2d36f01783c0fe`
- artifacts:
  - `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
  - `.env.cloud.dev`
  - `backend/scripts/ops/cloud_dev_db_smoke.py`
  - `backend/scripts/legacy/run_api_win.py`
  - `backend/infra/database/env_guard.py`
- narrative:
  - 对我来说，S4C-3A 解决的不是“把应用部署上云”，而是把 S4C-2A 已经证明可控的 cloud-dev RDS 真正接回 wordloom-v3 runtime。到这一步为止，我已经能用一份独立的 `.env.cloud.dev` 在本机启动后端，让它连接 AWS 上的 cloud-dev Postgres，并通过最小 smoke 路径验证三层事实：第一，数据库网络与凭证可达；第二，应用 startup 能通过环境保护检查；第三，业务层只读接口在 schema 完成迁移后可以返回正常的 `200` 响应。
  - 这轮也把边界讲清楚了：Terraform 负责的是 VPC、子网、SG、RDS、白名单这类 infra 原语；runtime config 负责的是 `.env.cloud.dev`、`DATABASE_URL`、API 端口、Windows/WSL 启动入口；Alembic migration 则是应用 schema 落地层，既不属于纯 infra，也不能靠“网络连通”自动完成。换句话说，S4C-2A 证明“云上的 DB 能被创建并能连上”，而 S4C-3A 证明“wordloom-v3 本机 runtime 能实际把这台云 DB 用起来”。
  - 因此，本 phase 的最小目标已经达成，可以进入 stable；后续如果继续扩展，重点就不再是“能不能连上”，而是选做两类增强：一类是最小业务写入 smoke，验证 cloud-dev runtime 的写路径；另一类是安全与运维收口，例如密码 rotation、临时公网访问回收、以及未来切换到 bastion/SSM/private access 路径。
