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

## Plan (draft)

### P1 (Implementation / scaffolding)

- P1-C1-S1: inventory dev/test infra 相关资产：
  - `docker-compose.devtest-db.yml`、`docker-compose.infra.yml`、`docker-compose.yml`；
  - 后端/前端相关 Dockerfile（如有）；
  - `.env.dev` / `.env.test` 等样例；
- P1-C1-S2: 用一小节文字描述 "从零到 dev/test" 的高层步骤：
  - 安装 Docker Desktop + WSL2；
  - 准备 env 文件；
  - 使用 `env_prep.sh` + `start.sh` 启动 infra / db / app；
- P1-C1-S3: 在本 log 中预留 Terraform 入口：
  - 标注哪些资源后续会用 Terraform 表达，并记录对应期望的 state/outputs 口径。

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

### P1 (Implementation / scaffolding)

- [ ] `P1-C1-S1`: inventory dev/test infra/runtime assets
- [ ] `P1-C1-S2`: high-level from-zero-to-dev/test steps
- [ ] `P1-C1-S3`: Terraform entrypoints & boundaries

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
