# log-S4B-1A (Phase 1A: Infra as Code & Runtime Packaging Baseline)

---

**id**: `S4B-1A`
**kind**: `log`
**title**: `infra as code & runtime packaging baseline (dev/test) v1`
**status**: `stable`
**scope**: `S4B`
**tags**: `EVOLUTION, OpsRuntime, Operations, InfraAsCode, Terraform, Docker, Runtime, epic/s4, epic/s4b, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4B-1A-from-zero-to-devtest-runtime.md`
  **parent_log**: `docs/logs/log-S4B-infra-as-code-and-runtime-packaging.md`
  **reference_log_1**: `docs/logs/log-S4A-1A-ops-scripting-baseline.md`
  **reference_log_2**: `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
**created**: `2026-03-21`
**updated**: `2026-03-25`

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

- 在本 phase 中，仅确定未来 Terraform/IaC 的入口和边界，不直接在此处实现完整 module：
  - 候选资源：
    - devtest DB 容器所映射的持久化卷与网络（例如用于本地/云端一体化时的数据库实例）；
    - MinIO 或等价对象存储（与 S5A-3B 备份故事对齐）；
  - 期望 state/outputs（示例）：
    - `db_endpoint` / `db_port` / `db_name`；
    - `object_storage_endpoint` / `bucket_name`；
  - 边界约束：
    - IaC v1 只为 dev/test 提供样本和 state 描述，不负责生产环境资源；
    - 与现有 docker-compose 定义保持一致（端口、卷路径等），避免出现两套不一致的真相来源；
  - 具体的 Terraform skeleton 实现从 `S4B-2A` phase 开始落地，首个样本为 `infra/terraform/devtest-db` 中的 devtest DB module。

### P2 (Drill / Verify)

#### P2-C1-S1 (From-zero-to-dev/test scripted path | v1)

- 目标：在不强制引入 Terraform 的前提下，先固定一条可复述、可脚本化的 from-zero-to-dev/test 路径，为后续 IaC 化提供对照基线。
- 路径形态（dev/test、本地 WSL2 语境）：
  1. 机器前置：Windows + Docker Desktop（开启 WSL2 integration）+ WSL2 Ubuntu；
  2. 在 WSL 中 clone 仓库并进入 `wordloom-v3` 根目录；
  3. 准备环境：
     - 确认存在 `.env.dev`，或由模板创建，并填入最低必要字段（DB URL、API/ES 端口等）；
  4. 运行 infra & runtime 脚本：
     - `./scripts/ops/env_prep.sh dev`
     - `./scripts/ops/start.sh dev infra es`
     - `./scripts/ops/start.sh dev db`
     - `./scripts/ops/start.sh dev app --no-worker`
  5. 验证 runtime：
     - `bash scripts/ops/status.sh dev`
     - `bash scripts/ops/health.sh dev`
- v1 不强制要求将上述步骤封装为单一脚本，但要求：
  - 以固定顺序 & 命令集呈现；
  - 后续可以直接复制这些命令到 from-zero-to-dev/test drill 中执行并产生 evidence。

#### P2-C1-S2 (Evidence for from-zero-to-dev/test path | v1)

- 目标：为上述路径设计一份轻量 evidence 结构，使其满足 S6A 风格的低基数 PASS/FAIL 和可追溯要求。
- 建议 evidence 载体：
  - 例如 `artifacts/_tmp_s4b1a_from_zero_to_devtest.json`（文件名可在后续真实演练时敲定）；
- 推荐字段：
  - `phase_id`: `S4B-1A`；
  - `path_kind`: `from_zero_to_devtest`；
  - `headSha`: `<git sha>`；
  - `env`: `dev`；
  - `steps`: 命令数组（例如 `['./scripts/ops/env_prep.sh dev', './scripts/ops/start.sh dev infra es', ...]`）；
  - `status_summary`: 来自 `status.sh` 关键字段的摘要（例如 db_container/api_health/ui_http/es_http）；
  - `health_result`: `PASS|FAIL`，由 `health.sh` exit code 映射；
  - `result`: `PASS|FAIL`（整体 from-zero-to-dev/test 路径是否成功）；
  - `notes`: 可选文字说明（例如异常时的简短 root cause）。
- 后续在实际跑第一次 drill 时，只需要：
  - 记录当前 `headSha`；
  - 复用 P2-C1-S1 中的命令顺序执行；
  - 按上述字段填写一个 JSON 或 Markdown 片段，并将路径登记到 Evidence 小节。

### P3 (Docs / Operator wording)

- P3-C1-S1: 用岗位语言回答：
  - dev/test 环境在基础设施和 runtime packaging 层面是如何定义的；
  - operator 在新机器上要做哪些步骤才算 "把系统拉起来"；
  - 这些步骤在 S4B-1A P2 drill 中是如何被验证并留下 evidence 的（包括 FAIL→PASS 的演进）。
- P3-C1-S2: 起一份 runbook，作为 "新环境站起来" 的操作手册草稿，并在 links.runbook 中挂上路径。

#### P3-C1-S1 (Operator-facing wording | v1)

- 基础设施层面（dev/test infra）：
  - dev/test 依赖的基础设施主要由 docker-compose 管理，包括 devtest DB 容器、ES 容器等；
  - 这些资源通过 `scripts/ops/start.sh dev infra es` 与 `scripts/ops/start.sh dev db` 启动，并通过 `scripts/ops/status.sh dev` / `scripts/ops/health.sh dev` 进行状态与健康检查；
  - future IaC（例如 Terraform）会以 devtest DB / MinIO 等为切入点，将当前 compose 描述逐步抽象为可重复、可审计的 infra module。
- runtime packaging 层面：
  - 应用 runtime（api + ui）通过 Dockerfile + docker-compose + `Procfile.dev` 打包，并由 `scripts/ops/start.sh dev app --no-worker` 拉起；
  - `scripts/ops/env_prep.sh dev` 负责准备本地 env 与依赖，保证 compose 与应用进程有一致的配置入口；
  - runtime 的健康度由 `scripts/ops/health.sh dev` 汇总多个探针（db/api/ui/es）给出 PASS/FAIL 结论。
- operator 的工作视角（新机器 bring-up）：
  - 准备阶段：安装 Docker Desktop + WSL2，在 WSL 中 clone 仓库，并配置 `.env.dev`；
  - bring-up 阶段：按固定顺序执行 env_prep → infra es → db → app → status/health；
  - 验证阶段：以 `status.sh dev` 和 `health.sh dev` 输出为主，确认 devtest DB/ES 容器 healthy，api/ui HTTP 探针 200，整体 health PASS；
  - 故障处理：若任一步骤 FAIL（例如端口占用、DB 容器起不来），operator 可以参考 Evidence 中的 FAIL drill 与 runbook 中的 troubleshooting 小节进行排查。
- drill 与 evidence：
  - 本 phase 已经完成两次 from-zero-to-dev/test drill：
    - 第一次 FAIL（端口占用导致 DB 容器与 app up 失败），对应 `artifacts/_tmp_s4b1a_from_zero_to_devtest.json`；
    - 第二次 PASS（DB/ES/health 全绿，api 端口有预警但整体健康 OK），对应 `artifacts/_tmp_s4b1a_from_zero_to_devtest_v2.json`；
  - 通过 FAIL→PASS 的演进，operator 可以在文档中讲清：
    - from-zero 路径不仅存在，而且经过实战演练；
    - 关键故障模式（端口占用等）有 evidence 和 runbook 可追溯。

#### P3-C1-S2 (Runbook reference | v1)

- 本 phase 对应的新环境 bring-up runbook：
  - `docs/runbook/run-S4B-1A-from-zero-to-devtest-runtime.md`
- runbook 中包含：
  - 适用场景与前置条件；
  - 从零到 dev/test runtime 的操作步骤（env_prep → infra → db → app → status/health）；
  - 如何在演练完成后记录 evidence（headSha、env、path_kind、status/health 摘要与 PASS/FAIL 结论）；
  - 常见故障（端口占用、容器不健康、health FAIL）的排查建议。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: dev/test infra as code baseline contract
- [x] `P0-C1-S2`: dev/test runtime packaging baseline contract
- [x] `P0-C1-S3`: evidence contract

### P1 (Implementation / scaffolding)

- [x] `P1-C1-S1`: inventory dev/test infra/runtime assets
- [x] `P1-C1-S2`: high-level from-zero-to-dev/test steps
- [x] `P1-C1-S3`: Terraform entrypoints & boundaries

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: from-zero-to-dev/test scripted path
- [x] `P2-C1-S2`: evidence recorded (first run: FAIL, see Evidence)

### P3 (Docs / Operator wording)

- [x] `P3-C1-S1`: operator-facing wording
- [x] `P3-C1-S2`: runbook (if needed)

## Evidence

- 2026-03-21（v1 drill，从零到 dev/test 路径，结果 FAIL）：
  - headSha: `f66aad9167757de2bb8dd6340a4aae984016832b`
  - env: `dev`
  - path_kind: `from_zero_to_devtest`
  - artifacts: `artifacts/_tmp_s4b1a_from_zero_to_devtest.json`
  - result: `FAIL`（devtest DB 5435 端口已被占用，`start.sh dev db` 无法绑定；API 端口已被占用导致 app up 失败；`health.sh dev` 报告 `db_devtest` 容器不存在，但 UI 与 ES HTTP 探针为 200）
- 2026-03-21（v2 drill，从零到 dev/test 路径，结果 PASS）：
  - headSha: `f66aad9167757de2bb8dd6340a4aae984016832b`
  - env: `dev`
  - path_kind: `from_zero_to_devtest`
  - artifacts: `artifacts/_tmp_s4b1a_from_zero_to_devtest_v2.json`
  - result: `PASS`（devtest DB 容器与 ES 均为 healthy，`status.sh dev` 显示 db_container/infra_es/ui_http/es_http 均正常，`health.sh dev` 报告 db/api/ui/es 全部 OK；`env_prep.sh` 仍有 api 端口占用提示，但不影响整体健康）

## Recent changes (for traceability, optional)

- 2026-03-21: scaffolded `S4B-1A` as the first `S4B` phase, focusing on a dev/test infra-as-code and runtime-packaging baseline before deeper IaC work.
- 2026-03-25: marked `S4B-1A` as `stable` after the FAIL→PASS from-zero-to-dev/test drills, operator wording, and runbook all converged on a stable v1 baseline.
