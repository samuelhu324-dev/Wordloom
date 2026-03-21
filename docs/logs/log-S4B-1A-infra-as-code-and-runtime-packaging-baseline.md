# log-S4B-1A (Phase 1A: Infra as Code & Runtime Packaging Baseline)

---

**id**: `S4B-1A`
**kind**: `log`
**title**: `infra as code & runtime packaging baseline (dev/test) v1`
**status**: `draft`
**scope**: `S4B`
**tags**: `EVOLUTION, OpsRuntime, Operations, InfraAsCode, Terraform, Docker, Runtime, epic/s4, epic/s4b, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4B-infra-as-code-and-runtime-packaging.md`
  **reference_log_1**: `docs/logs/log-S4A-1A-ops-scripting-baseline.md`
  **reference_log_2**: `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
**created**: `2026-03-21`
**updated**: `2026-03-21`

---

## Decision / Outcome

**Decision**:

- `S4B-1A` 作为 `S4B` 的首个 phase，聚焦在 dev/test 语境下打好最小的 "infra as code & runtime packaging baseline"：
  - 盘点并整理当前用于 dev/test 的 docker-compose / Dockerfile / env 示例；
  - 明确未来 Terraform（或等价 IaC）样本会从哪些资源开始（例如 devtest DB / MinIO）；
  - 把 "从一台干净机器到可用 dev/test runtime" 的关键步骤先用文字和命令梳理出来，为后续 P2 drill 做准备。
- 本 phase 不追求一次性完成所有 IaC 代码，而是给后续 work 一个稳定的入口和约束：知道从哪里开始补、优先补什么、哪些内容可以推迟到未来 phase。

**Default choices (phase defaults / v1)**:

- dev/test first：所有样本均以本地 dev/test 环境为前提，不引入生产级 cloud 复杂度；
- Terraform/IaC v1 只做样本与边界，不追求一次性覆盖所有资源类型；
- 继续沿用 S6A 的证据习惯：后续 drill/evidence 优先使用低基数 PASS/FAIL 与清晰的 artifact 路径。

## Definitions (optional)

- dev/test infra：本地开发与测试环境依赖的基础设施组合，包含 devtest DB、对象存储（MinIO）、可选 ES。 
- runtime packaging：通过 Dockerfile、docker-compose 与 ops 脚本，将应用与依赖打包成可启动、可检查健康的 runtime 的方式。
- from-zero-to-dev/test path：在一台干净机器上，从安装依赖到 env 准备、infra 启动、app 启动的一组有序步骤。

## P0 (Contract | v1)

### P0-C1-S1 (Baseline contract for dev/test infra as code | v1)

- 关键问题：
  - 如果现在只给一台干净的 Windows + WSL2 机器，我如何描述 dev/test infra 需要哪些资源？
  - 这些资源里，哪些适合由 Terraform/IaC 管理，哪些继续由 docker-compose 承担？
- v1 contract：
  - 用文字先固定 dev/test 运行所需的最小资源清单（DB、object storage、ES、网络端口等）；
  - 为未来 Terraform module 预留清晰的边界与命名，而不是直接在本 phase 写完全部 IaC。

### P0-C1-S2 (Baseline contract for runtime packaging | v1)

- 关键问题：
  - 应用在 dev/test 环境中是如何被打包和启动的（容器组合、前后端进程、ops 脚本）；
  - 哪些入口脚本负责从 "infra up" 到 "app up"，与 S4A-1A 的启动脚本如何协同；
- v1 contract：
  - 将当前 docker-compose 文件和 `scripts/ops/start.sh` / `env_prep.sh` 的角色讲清楚，并与后续 IaC 故事对齐；
  - 暂不强求镜像与 registry 策略，只关心本地可复用的 runtime packaging 模式。

### P0-C1-S3 (Evidence contract | v1)

- 本 phase 自身不直接产出 drills JSON，但约定后续 S4B P2/P3 的 evidence 口径：
  - 至少记录：
    - `headSha`（当前 Git 提交）；
    - `env`（例如 `dev`）；
    - `path_kind`（例如 `from_zero_to_devtest`）；
    - `steps`（关键命令列表或引用的脚本）；
    - `result`（`PASS|FAIL`）；
  - Artifacts 可以是简单的 Markdown/日志片段或轻量 JSON，存放在 `artifacts/` 或 `docs/labs/_snapshot/` 下，由后续 P2 阶段补齐具体路径。

## Plan (draft)

### P1 (Implementation / scaffolding)

#### P1-C1-S1 (Inventory dev/test infra/runtime assets | v1)

- Compose & Docker：
  - `docker-compose.devtest-db.yml`：dev/test 数据库容器定义（卷挂载、端口、健康检查）；
  - `docker-compose.infra.yml`：infra 级别依赖（例如 ES）容器定义；
  - `docker-compose.yml`：默认 compose 入口（与上面两个如何组合，由后续 P2 进一步细化）；
  - 应用相关 Dockerfile（backend/frontend，如存在）：作为未来镜像构建与部署的基础；
- Env & 脚本：
  - `.env.dev` / `.env.test`：本地 dev/test 环境变量样例（数据库 URL、API/ES 端口等）；
  - `scripts/ops/env_prep.sh`：负责为 dev/test 准备 env 与依赖；
  - `scripts/ops/start.sh`：统一的启动入口，用 `start.sh <env> infra/db/app/all` 组合拉起 compose 与 app；
- 其他：
  - 与 infra 相关的 docs/logs（例如 S4A-1A / S4A-2A / S3A-2A-4B 中对 devtest DB、ES 的描述），在本 phase 中只作为参考，不重新定义。

#### P1-C1-S2 (High-level from-zero-to-dev/test steps | v1)

- 在一台新的 Windows + WSL2 机器上，从零到可用 dev/test runtime 的高层步骤可以描述为：
  1. 安装 Docker Desktop，并启用 WSL2 integration；
  2. 在 WSL2（例如 Ubuntu 发行版）中 clone `wordloom-v3` 仓库；
  3. 准备环境变量文件：复制或创建 `.env.dev` / `.env.test`，填入最小必需字段（数据库 URL、API/ES 端口等）；
  4. 在 WSL 中执行：
     - `./scripts/ops/env_prep.sh dev`
     - `./scripts/ops/start.sh dev infra es`（启动 ES 等 infra 组件，如需要）；
     - `./scripts/ops/start.sh dev db`（启动 devtest DB）；
     - `./scripts/ops/start.sh dev app --no-worker`（启动应用本身）；
  5. 使用 `bash scripts/ops/status.sh dev` 与 `bash scripts/ops/health.sh dev` 验证 runtime 是否已经处于 "green" 状态；
- P1 的目标不是让这些步骤全部自动化，而是把它们以稳定、可复述的顺序固定下来，为 S4B 后续 drill 与 IaC work 提供真实起点。

#### P1-C1-S3 (Terraform entrypoints & boundaries | v1)

- 在本 phase 中，仅确定未来 Terraform/IaC 的入口和边界，不直接实现：
  - 候选资源：
    - devtest DB 容器所映射的持久化卷与网络（例如用于本地/云端一体化时的数据库实例）；
    - MinIO 或等价对象存储（与 S5A-3B 备份故事对齐）；
  - 期望 state/outputs（示例）：
    - `db_endpoint` / `db_port` / `db_name`；
    - `object_storage_endpoint` / `bucket_name`；
  - 边界约束：
    - IaC v1 只为 dev/test 提供样本和 state 描述，不负责生产环境资源；
    - 与现有 docker-compose 定义保持一致（端口、卷路径等），避免出现两套不一致的真相来源。

### P2 (Drill / Verify)

- P2-C1-S1: 设计一条 "从空环境到可用 dev/test runtime" 的脚本化路径（即使暂时不完全由 Terraform 驱动）；
- P2-C1-S2: 为该路径记录一份 evidence（命令输出 / 简单 JSON / 文字步骤），对齐 `S6A` 的低基数 PASS/FAIL 习惯。

### P3 (Docs / Operator wording)

- P3-C1-S1: 用岗位语言回答：
  - dev/test 环境在基础设施和 runtime packaging 层面是如何定义的；
  - operator 在新机器上要做哪些步骤才算 "把系统拉起来"；
- P3-C1-S2: 视需要起一份 runbook，作为 "新环境站起来" 的操作手册草稿。

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: dev/test infra as code baseline contract
- [ ] `P0-C1-S2`: dev/test runtime packaging baseline contract
- [ ] `P0-C1-S3`: evidence contract

### P1 (Implementation / scaffolding)

- [x] `P1-C1-S1`: inventory dev/test infra/runtime assets
- [x] `P1-C1-S2`: high-level from-zero-to-dev/test steps
- [x] `P1-C1-S3`: Terraform entrypoints & boundaries

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: from-zero-to-dev/test scripted path
- [ ] `P2-C1-S2`: evidence recorded

### P3 (Docs / Operator wording)

- [ ] `P3-C1-S1`: operator-facing wording
- [ ] `P3-C1-S2`: runbook (if needed)

## Evidence (reserved)

- 预留：后续在本 phase 定义第一条 from-zero-to-dev/test 路径时，再补充具体样本与 evidence。

## Recent changes (for traceability, optional)

- 2026-03-21: scaffolded `S4B-1A` as the first `S4B` phase, focusing on a dev/test infra-as-code and runtime-packaging baseline before deeper IaC work.
