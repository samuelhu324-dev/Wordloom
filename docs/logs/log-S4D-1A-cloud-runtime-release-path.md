# log-S4D-1A (Phase 1: Cloud Runtime Release Path)

---

**id**: `S4D-1A`
**kind**: `log`
**title**: `cloud runtime release path (deploy target, env contract, verify/rollback baseline) + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, ReleaseOperations, Deploy, Rollback, Drills, Evidence, epic/s4, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  **previous_log**: `docs/logs/log-S4C-cloud-services-and-terraform-epic.md`
  **reference_log_1**: `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
  **reference_log_2**: `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
  **reference_log_3**: `docs/logs/_template-log-phase-drills-evidence.md`
**created**: `2026-03-23`
**updated**: `2026-03-23`

---

## Decision / Outcome

**Decision**:

- `S4D-1A` 作为 `S4D` 的首个 phase，先固定一条最小 cloud runtime release path，而不是同时讨论多个部署目标；
- 本 phase 的交付重点是：部署目标选择、env/config contract、verify/rollback baseline，以及最小 evidence contract。

**Default choices (phase defaults / v1)**:

- 优先复用已经存在的 runtime contract：应用配置继续以 repo-root env 文件和既有启动入口为基础，不引入第三套配置模型；
- deploy target 先追求“最小可解释、可验证、可回退”，不追求 production-grade HA；
- v1 target 默认先收敛为“单 Linux 主机 + backend API container + 外部 cloud-dev RDS”，不把 UI、worker、复杂编排和多服务同机编排同时拉进第一轮；
- release contract 默认收敛为“单个 backend image + 单份 cloud-dev env + 单条 post-deploy verify checklist”，避免在第一轮把 build/deploy/verify 分裂成多套入口；
- verify 先固定为 health + 关键 read smoke + 日志摘要，写路径和复杂回放放到后续 phase；
- rollback 先固定为“回到上一个已知可用版本/配置”的简单策略。

## Definitions (optional)

- **Deploy target**：第一轮承接 wordloom-v3 runtime 的 cloud/staging-like 运行目标。
- **Release path**：从选择构建物、注入 env、启动服务、执行 smoke、到必要时回退的完整 operator 路径。
- **Post-change verification**：部署完成后，用于判断“能否继续前进”的最小检查集合。
- **Known-good version**：最近一个已通过 verify 的版本/配置组，用作 rollback 基线。

## Constraints

- 不把 deploy target 与 infra target 混成一个问题；云资源本身的建立仍由 `S4C` 负责；
- 不提交真实 secrets；env/config 只记录 contract 与文件/变量名；
- 每次 deploy/rollback drill 都需要记录 target、headSha、env 名、关键命令和结果摘要；
- v1 不引入高复杂度发布策略（蓝绿/金丝雀/多版本并行）。

## Scope

- `P0`: contract（deploy target 选择原则、env/release contract、evidence contract）
- `P1`: implementation / target definition（固定最小 deploy target 与 release path）
- `P2`: drill / verify（首轮 deploy -> verify -> rollback 样本）
- `P3`: docs / operator wording（把 release path 变成 operator-facing 说明）

## Success Criteria (DoD)

- 明确一个 v1 deploy target；
- 明确 deploy 所需的 env/config contract 与最小 verify checklist；
- 至少有一条首轮 deploy/rollback drill 的 evidence 入口；
- 能明确回答：`S4B`、`S4C`、`S4D-1A` 各自负责哪一段 operator path。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 target 选择、release path 与 verify/rollback baseline 已稳定；
  - Evidence 区至少记录一条可追溯的 deploy/rollback 样本（headSha + artifact path / terminal proof / CI run URL）。

## P0 (Contract | v1)

### P0-C1-S1 (Deploy target selection contract | v1)

- v1 deploy target 必须满足：
  - 可低成本获得；
  - 可清楚解释配置注入和启动路径；
  - 支持最小 smoke 与回退验证；
  - 不需要生产级编排前置条件。
- v1 选择优先级：
  - 第一优先：已有 Dockerfile/entrypoint、现成 runtime contract、最少新增平台概念；
  - 第二优先：能直接复用 `S4C` 已打通的 cloud-dev RDS；
  - 第三优先：rollback 可以通过单机容器版本或 known-good Git/env 组合完成；
  - 明确排除：在第一轮就同时引入 ECS/App Runner/多容器 UI+worker 编排、镜像仓库流水线、复杂 LB/域名/TLS 收口。

### P0-C1-S2 (Release path contract | v1)

- release path 至少应明确：
  - 构建物或启动入口是什么；
  - env/config 如何注入；
  - deploy 成功后的 verify 检查项；
  - rollback 如何回到 known-good version。
- v1 release contract 进一步固定为：
  - deployable unit = `backend` Docker image；
  - runtime dependency = 外部 `cloud-dev` RDS（由 `S4C` 负责生命周期）；
  - env source = 单份 cloud-dev env 文件或同名环境变量集合；
  - post-deploy gate = `health` + `libraries` + 容器日志摘要；
  - rollback unit = 上一个 known-good image/tag 或 known-good Git/env bundle。

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON 后续至少应包含：
  - `headSha`
  - `deploy_target`
  - `env_name`
  - `deploy_command_summary`
  - `verify_summary`
  - `rollback_summary`
  - `result`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4D-1A/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`）或同一 phase / cycle 下连续 steps 的组合（如 `1S2`）。

**Branch convention**:

- `S4D-1A` 相关实现与文档优先落在 `S4D-cloud-runtime-deploy-verify-rollback` 分支。

**Commit discipline (recommended)**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4D-cloud-runtime-deploy-verify-rollback`。

## Plan (draft)

### P1 (Implementation / target definition)

- P1-C1-S1: 选定 v1 deploy target
- P1-C1-S2: 固定 env/release contract 与 verify checklist

### P1-C1-S1 (v1 deploy target selected | implemented 2026-03-23)

- chosen target:
  - `AWS single Linux VM + backend API Docker container + external cloud-dev RDS`
- in-scope for v1:
  - 单台 Linux 主机（staging-like target）;
  - 只部署 backend API runtime；
  - 数据库继续复用 `S4C` 已打通的 `cloud-dev` RDS；
  - 应用通过 env 文件或等价环境变量注入 `DATABASE_URL` / `WORDLOOM_ENV` / `API_PORT`；
  - verify 以 `GET /api/v1/health` + `GET /api/v1/libraries` + 容器日志摘要为主；
  - rollback 以“回到上一个 known-good image/tag 或 known-good Git/env bundle”为主。
- explicitly out-of-scope for v1:
  - 前端 UI 云端部署；
  - worker 云端常驻运行；
  - App Runner / ECS / Kubernetes 等更复杂目标；
  - 负载均衡、TLS、域名、自动镜像流水线。
- why this target wins:
  - `backend/Dockerfile` 与 `backend/entrypoint.sh` 已存在，且 entrypoint 已封装 `alembic upgrade head`，说明 backend container 是当前最成熟的 deployable unit；
  - `S4C` 已证明 cloud-dev RDS 与 `.env.cloud.dev` 路径可用，因此 v1 最低风险的增量不是再建新 infra，而是把 API runtime 从本机推进到单机云主机；
  - 单主机容器目标最容易解释日志、健康检查、env 注入和回退，不会在第一轮被镜像仓库、服务发现、复杂编排分散注意力；
  - 业务最小 read smoke（`/health`、`/libraries`）已经在 `S4C-3A` 验证过，适合作为第一轮 release verify baseline。
- rejected alternatives:
  - `UI + API + worker` 同时上云：当前变更面过大，verify 和 rollback 面都变宽，不适合作为第一轮样本；
  - `ECS/App Runner`：虽然长期更像云端正道，但当前 repo 尚未形成稳定的 image build/push/release bundle，第一轮会把重点从 release path 转移到平台接线；
  - 继续只做“本机 runtime -> 云 DB”：这已经由 `S4C` 覆盖，不再回答 `S4D` 的核心问题。

### P1-C1-S2 (env/release contract and verify checklist fixed | implemented 2026-03-23)

- deployable unit:
  - `backend` image built from `backend/Dockerfile`;
  - container entrypoint uses `backend/entrypoint.sh`, which runs `alembic upgrade head` before starting the API process.
- runtime topology for v1:
  - one Linux VM hosts one backend API container;
  - database stays external and points to the existing `cloud-dev` RDS;
  - frontend UI and worker remain out of scope for the first release-path sample.
- env/config contract:
  - required envs:
    - `DATABASE_URL`
    - `WORDLOOM_ENV=dev`
    - `ENVIRONMENT=cloud-dev`
  - strongly recommended envs:
    - `LOG_LEVEL=INFO`
    - `DEBUG=False`
    - `WORDLOOM_TRACING_ENABLED=0`
    - `OTEL_SDK_DISABLED=1`
  - search/storage envs:
    - keep `ELASTIC_URL` / `ELASTIC_INDEX` explicit if search routes are expected to work;
    - for the first API release-path sample, `verify` does not depend on search-specific endpoints.
  - port contract:
    - container listens on internal port `8000` (Dockerfile default);
    - operator-facing external port remains `30021` via host mapping `30021:8000`, so the existing cloud-dev smoke URL stays stable.
- release-path contract:
  - build artifact = one backend image for the current `headSha`;
  - deploy action = run the backend container with the cloud-dev env injected;
  - success baseline = container starts, migrations finish, API serves health/read probes on the external port;
  - rollback baseline = stop current container and restart the previous known-good image/tag or the previous known-good Git/env bundle.
- verify checklist for v1:
  - `container_running`: target container is up after deploy;
  - `migration_ok`: logs contain successful migration/startup lines from `entrypoint.sh` and no immediate crash loop;
  - `health_ok`: `GET /api/v1/health` returns `200`;
  - `read_smoke_ok`: `GET /api/v1/libraries` returns `200` and a JSON list payload;
  - `env_guard_ok`: startup does not fail due to database-environment mismatch.
- why this checklist is different from earlier local gates:
  - `S4A-2A` 的 `deploy_app_verify` 是本地 dev/test runtime gate，检查的是一整套本机 DB/API/UI/ES 是否仍然健康；
  - `S4D-1A` 的 verify 是“云端 API 容器 release gate”，它更聚焦：容器是否起来、migration 是否通过、外部 RDS 是否可用、最小 API 路径是否仍然工作；
  - 两者都属于 post-change verification，但作用对象不同：一个验证本地 runtime，另一个验证云端 deploy target。

### P2 (Drill / Verify)

- P2-C1-S1: 首轮 deploy -> verify 样本入账
- P2-C1-S2: 首轮 rollback 样本入账

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: deploy target selection contract
- [x] `P0-C1-S2`: release path contract
- [ ] `P0-C1-S3`: evidence contract

### P1 (Implementation / target definition)

- [x] `P1-C1-S1`: v1 deploy target selected
- [x] `P1-C1-S2`: env/release contract and verify checklist fixed

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: first deploy -> verify sample recorded
- [ ] `P2-C1-S2`: first rollback sample recorded

### P3 (Docs / operator wording)

- [ ] `P3-C1-S1`: operator-facing wording written

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, deploy target, env/config identifiers, and drill outcomes.

### P0-C1-S1 (S4D-1A skeleton created | 2026-03-23)

- headSha: `<TBD-after-first-S4D-commit>`
- artifacts:
  - `docs/logs/log-S4D-1A-cloud-runtime-release-path.md`
- expected:
  - 为 `S4D-1A` 固定最小 release path 的目标边界、contract 与 evidence 结构。
- observed:
  - phase skeleton 已创建，等待后续 target 选择与首轮 deploy/rollback drills。

### P1-C1-S1 (v1 deploy target fixed | 2026-03-23)

- headSha: `<pending-current-worktree-commit>`
- artifacts:
  - `docs/logs/log-S4D-1A-cloud-runtime-release-path.md`
  - `backend/Dockerfile`
  - `backend/entrypoint.sh`
  - `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
- expected:
  - 选出一个足够小、足够真实、能承接后续 release path contract 的 v1 deploy target。
- observed:
  - 已将 v1 target 固定为“单 Linux 主机 + backend API Docker container + external cloud-dev RDS”；
  - 该选择直接复用已有 backend Dockerfile、entrypoint migration path 和 `S4C` 的 cloud-dev RDS，能够把第一轮复杂度压到最低；
  - 因此 `S4D-1A` 的下一步不再是争论部署目标，而是固定 `env/release contract` 与 `verify checklist`。

### P1-C1-S2 (env/release contract fixed | 2026-03-23)

- headSha: `<pending-current-worktree-commit>`
- artifacts:
  - `docs/logs/log-S4D-1A-cloud-runtime-release-path.md`
  - `.env.cloud.dev.example`
  - `backend/Dockerfile`
  - `backend/entrypoint.sh`
  - `scripts/ops/deploy_app_verify.sh`
- expected:
  - 为 v1 deploy target 固定一组足够小、足够清晰、可直接进入下一轮 deploy drill 的 env/release contract 与 verify checklist。
- observed:
  - 已固定 deployable unit、required envs、port contract、rollback unit 和 v1 verify checklist；
  - verify 的核心收敛为：`container_running`、`migration_ok`、`health_ok`、`read_smoke_ok`、`env_guard_ok`；
  - 因此 `S4D-1A` 下一步已经可以进入 `P2`：做第一轮真实 deploy -> verify -> rollback 样本，而不是继续停留在合同层。

## Recent changes (for traceability, optional)

- 2026-03-23: scaffolded `S4D-1A` as the first phase of the cloud runtime deploy/verify/rollback spine.
- 2026-03-23: fixed the v1 deploy target as a single Linux VM running the backend API container against the existing cloud-dev RDS.
- 2026-03-23: fixed the v1 env/release contract and verify checklist for the cloud runtime release path.