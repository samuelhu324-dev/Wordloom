# log-S4B-2A (Phase 2A: Dev/test DB Terraform Skeleton)

---

**id**: `S4B-2A`
**kind**: `log`
**title**: `dev/test db terraform skeleton (infra as code sample) v1`
**status**: `stable`
**scope**: `S4B`
**tags**: `EVOLUTION, OpsRuntime, Operations, InfraAsCode, Terraform, Docker, Runtime, epic/s4, epic/s4b, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4B-infra-as-code-and-runtime-packaging.md`
  **reference_log_1**: `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
  **reference_log_2**: `docs/ROADMAP v5.md`
**roadmap_path**: `docs/roadmap/road-001-01-gov-role-minimal-ops-loop.md`
**roadmap_milestone**: `M3`
**roadmap_phase**: `M3-P0`
**roadmap_bridge_refs**: `docs/roadmap/road-001-01-gov-role-minimal-ops-loop.md#M3-P0, docs/roadmap/road-001-01-gov-role-minimal-ops-loop.md#M3-P1, docs/roadmap/road-001-01-gov-role-minimal-ops-loop.md#M3-P2, docs/roadmap/road-001-01-gov-role-minimal-ops-loop.md#M3-P3`
**created**: `2026-03-21`
**updated**: `2026-03-25`

---

## Decision / Outcome

**Decision**:

- `S4B-2A` 作为 `S4B` 的第二个 phase，聚焦在 dev/test DB 的 Terraform skeleton：
  - 选定 devtest DB 作为首个 IaC 目标资源；
  - 用 Terraform module 的形式固定 `db_endpoint` / `db_port` / `db_name` 等 state/outputs 口径；
  - 本阶段不强求真实云资源 provision，而是以 `null_resource + outputs` 的方式，提供一份可读、可演进的 infra-as-code 样本。
- 这一 phase 对应 ROADMAP v5 中的 `IaC / scripting / automation` 与 `minimal reproducible environment`：
  - 通过 Terraform skeleton 把 dev/test 环境中的 DB state 文档化、可重复；
  - 为未来 on-prem / cloud / hybrid 的 dev/test DB 运行面预留清晰接口。

**Default choices (phase defaults / v1)**:

- dev/test first：仅针对本地 dev/test DB，暂不涉及生产级云资源；
- Terraform skeleton 先用 `null_resource` 占位，后续再替换为真实 provider（如 AWS/Azure RDS）；
- 只关心 state/outputs 口径是否与当前 compose/.env.dev 对齐，不改变现有本地启动体验。

## P0 (Contract | v1)

### P0-C1-S1 (IaC skeleton contract for devtest DB | v1)

- 关键问题：
  - dev/test DB 在 IaC 视角下，应该暴露哪些关键字段（endpoint/port/name）；
  - 这些字段如何与 `.env.dev` 与 `docker-compose.devtest-db.yml` 对齐；
  - 如何在不真正创建云资源的前提下，先用 Terraform module 固定 state/outputs 口径。
- v1 contract：
  - 使用 `infra/terraform/devtest-db` 作为 devtest DB 的 IaC skeleton 根目录；
  - variables 与 outputs 中至少覆盖：`env`、`db_name`、`db_port`、`db_endpoint`；
  - module 必须可通过 `terraform validate`，但不强制跑 `apply`。

## Plan (draft)

### P1 (Implementation / skeleton)

#### P1-C1-S1 (Create devtest DB Terraform skeleton module | v1)

- 在 `infra/terraform/devtest-db/` 下创建：
  - `variables.tf`：定义 `env`、`db_name`、`db_port` 等变量；
  - `main.tf`：使用 `null_resource.devtest_db` + `triggers` 捕获 env/name/port 这几个 state；
  - `outputs.tf`：暴露 `db_endpoint` / `db_port` / `db_name`；
- v1 不绑定具体 provider，仅作为可阅读的 IaC 样本。

#### P1-C1-S2 (Align skeleton with compose/.env.dev | v1)

- 确认：
  - `db_port` 默认值与 devtest DB 在 compose 中暴露的端口一致（5435）；
  - `db_name` 默认值与当前 dev/test 数据库名一致（例如 `wordloom_dev`）；
  - `db_endpoint` 暂固定为 `localhost`，与本地开发体验保持一致。

### P2 (Drill / Verify)

#### P2-C1-S1 (Terraform validate/plan drill | v1)

- 目标：验证 skeleton module 至少可以被 Terraform 正常解析，并输出预期的 state/outputs：
  1. 在 WSL 中进入 `infra/terraform/devtest-db/`；
  2. 运行：
     - `terraform init`
     - `terraform validate`
     - （可选）`terraform plan`
- v1 不要求实际 `apply`，只需保证：
  - validate 通过；
  - plan 在 `null_resource.devtest_db` 基础上给出稳定的 diff。

#### P2-C1-S2 (Evidence for Terraform skeleton drill | v1)

- 建议在首次完整执行 `terraform validate/plan` 后：
  - 将关键输出（如 plan 摘要）保存到 `artifacts/` 或 `docs/labs/_snapshot/` 下的轻量文本/Markdown；
  - 在 Evidence 小节中登记：`headSha`、`env`、命令序列与 `result=PASS|FAIL`。

### P3 (Docs / Operator wording)

- P3-C1-S1: 用岗位语言回答：
  - 为什么要为 dev/test DB 提供一份 IaC skeleton；
  - 这份 skeleton 如何帮助实现 `minimal reproducible environment` 与配置一致性；
- P3-C1-S2: 在 S4B-2A 下准备一小段说明，作为面试时讲 Terraform/IaC 的入口。

#### P3-C1-S1 (Operator-facing wording | v1)

- 为什么要有 dev/test DB Terraform skeleton：
  - 在 dev/test 场景下，DB 目前是通过 docker-compose + `.env.dev` 启动的，但缺少一个“可以被阅读和版本控制的 infra state 定义”；
  - 通过 `infra/terraform/devtest-db` 这个 skeleton module，把 `env/db_name/db_port` 这些关键字段固定在 Terraform 里，可以更清楚地表达 dev/test DB 的期望 state/outputs；
  - 未来如果需要把 dev/test DB 挂到云端（如 RDS/Azure PG），只要替换 `null_resource` 为真实 provider 资源即可，variables/outputs 口径保持不变。
- 对 minimal reproducible environment 和配置一致性的帮助：
  - skeleton module 把 dev/test DB 的端口（5435）、数据库名（`wordloom_dev`）和 endpoint（`localhost`）写在变量/输出里，与 `.env.dev` 和 compose 对齐；
  - 这让“dev/test 环境长什么样”不再只存在于脚本和口头知识里，而是有一份 IaC 文件可以直接 diff/审查；
  - 即使现在不跑 `terraform apply`，也可以通过 `terraform validate/plan` 快速检查配置是否自洽。

#### P3-C1-S2 (Interview/story entrypoint | v1)

- 在面试中谈 Terraform/IaC 时，可以用 `S4B-2A` 做入口：
  - 我不是一开始就上云，而是先在现有 dev/test 环境上，为 DB 起了一份 Terraform skeleton，把 `env/db_name/db_port` 这些 state/outputs 口径固定下来；
  - 我用 `null_resource` + `outputs` 的方式，先完成“可以复述的 IaC 样本”，然后通过一次 `terraform init/validate/plan` drill 证明配置是可执行、可验证的；
  - 这样既能讲 `infrastructure scripting and automation`，又不会把重点从 systems/platform operations 和 reproducible env 上移开。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: IaC skeleton contract for devtest DB

### P1 (Implementation / skeleton)

- [x] `P1-C1-S1`: devtest DB Terraform skeleton module created
- [x] `P1-C1-S2`: skeleton aligned with compose/.env.dev defaults

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: Terraform validate/plan drill defined & executed
- [x] `P2-C1-S2`: evidence recorded

### P3 (Docs / Operator wording)

- [x] `P3-C1-S1`: operator-facing wording
- [x] `P3-C1-S2`: interview/story entrypoint (if needed)

## Evidence

- 2026-03-21（v1 drill，devtest DB Terraform skeleton validate/plan，结果 PASS）：
  - headSha: `780a665ed5e6c3f110bcc2a33b3ecb97ed25c85b`
  - env: `dev`
  - commands: `terraform init`, `terraform validate`, `terraform plan -no-color`
  - artifacts: `artifacts/_tmp_s4b2a_devtest_db_terraform_plan.txt`
  - result: `PASS`（配置通过 validate，plan 生成 1 个 `null_resource.devtest_db` 以及预期的 `db_endpoint/db_name/db_port` outputs，未执行 apply）

## Recent changes (for traceability, optional)

- 2026-03-21: scaffolded `S4B-2A` as a dev/test DB Terraform skeleton phase, aligned with ROADMAP v5 的 IaC / scripting / automation 与 minimal reproducible environment 目标。
- 2026-03-25: marked `S4B-2A` as `stable` after the Terraform skeleton contract, implementation, validate/plan drill, and operator wording all closed with PASS evidence.
