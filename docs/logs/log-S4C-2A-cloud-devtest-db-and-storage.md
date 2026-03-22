# log-S4C-2A (Phase 2: Cloud dev/test network + DB + storage skeleton)

---

**id**: `S4C-2A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `Cloud dev/test network + DB + storage（Terraform modules + drills） v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S4`
**tags**: `EVOLUTION, Cloud, Terraform, Infra, Drills, Evidence, epic/s4, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4C-cloud-services-and-terraform-epic.md`
  **previous_log**: `docs/logs/log-S4C-1A-cloud-devtest-terraform-bootstrap.md`
  **reference_log_1**: `docs/logs/_template-log-phase-drills-evidence.md`
**created**: `2026-03-22`
**updated**: `2026-03-22`

---

## Decision / Outcome

**Decision**:

- 在 AWS playground 账号中，为 wordloom-v3 建立一套 **dev/test 专用** 的最小网络 + 托管 Postgres + 基础存储骨架；
- 使用 Terraform 在 `infra/terraform/aws/{network,devtest-db,storage}` 下实现这些模块，并通过 drills 证明可以安全地 `plan/apply/destroy`，成本可控、可重复。

**Default choices (phase defaults / v1)**:

- 仅面向 dev/test，所有资源大小、备份策略等以节省成本为第一优先；
- 所有资源位于同一 region：`ap-southeast-2`；
- 不在云上存放生产数据，仅使用演示/测试数据；
- 优先使用 AWS 提供的免费或低成本选项（例如小规格 RDS、低频访问存储等），并在需要长期保留资源前先跑通最小 drill；
- 所有 Terraform 更改通过 `plan` + 明确的 Evidence 记录后再 `apply`，避免控制台手工改配置。

## Definitions (optional)

- **devtest network**：专门用于开发/测试环境的 VPC + 子网 + 路由 + 安全组组合，不与生产网络混用。
- **devtest-db**：托管 Postgres（例如 AWS RDS）的最小实例，用于 wordloom-v3 的 cloud-dev 演练。
- **storage**：最小的 S3 bucket / 相关资源，用于存放日志、备份或简单文件（可能复用 S4C-1A 示例的经验，但以模块形式重写）。

## Constraints

- 本 phase 内只允许创建 **少量、易于销毁** 的资源，避免长时间保持大量 RDS/大容量存储；
- 不直接创建生产级多 AZ / 高可用拓扑，优先用单 AZ、小规格实例；
- 所有凭证/密码必须通过本地 env 或 AWS Secrets Manager/Parameter Store 管理，不 hard-code 在仓库；
- 每次 `apply` 之前都需要有对应的 `plan` Evidence（包含 headSha、模块路径、`plan` 摘要）。

## Scope

- `P0`: contract（命名、目录结构、资源范围、成本和 evidence 约定）。
- `P1`: implementation（network / devtest-db / storage Terraform 模块骨架）。
- `P2`: drill / verify（至少一次从 0 到 `apply` 再 `destroy` 的完整练习）。
- `P3`: drill / wording（总结「本机 API 如何连接云上 devtest DB/storage」的 narrative，并为后续 S4C-3A 铺路）。

## Success Criteria (DoD)

- 目录结构：在 `infra/terraform/aws/` 下存在 `network/`、`devtest-db/`（以及按需 `storage/`）目录，并有清晰的 `README.md` 说明；
- 能通过 Terraform 在 AWS 中成功创建并销毁一套最小 dev/test 网络 + Postgres 实例（或等价 DB 资源），全程有 `plan/apply/destroy` 的 Evidence；
- 所有资源的命名、tags 中包含 `wordloom-v3` 与 `cloud-dev`，便于区分和清理；
- 成本控制：RDS/存储配置在 AWS 控制台的月度成本预估保持在可接受范围（例如个位数美元级），并在 Evidence 中给出大致说明；
- 你能用一段稳定的话术解释「本机 wordloom-v3 通过什么网络路径、安全组和连接串，连到这套 dev/test DB」。

## Stability (what stable means)

- 本 log 标记为 `stable` 时：
  - P0/P1/P2/P3 均已完成，至少有一次成功的 end-to-end drill（新建 + 连接 + 销毁）；
  - network/devtest-db 模块结构稳定，后续 S4C-3A 可以直接复用；
  - Evidence 部分包含可追踪的 headSha + 关键命令输出 + 控制台截图/链接（描述级）。

## P0 (Contract | v1)

### P0-C1-S1（目录与模块命名约定）

- Terraform 代码布局：
  - `infra/terraform/aws/network/`：VPC、子网、路由表、Internet/NAT gateway、基础安全组等；
  - `infra/terraform/aws/devtest-db/`：面向 cloud-dev 的托管 Postgres 实例 + 相关参数组、安全组等；
  - `infra/terraform/aws/storage/`（可选，v1 可只做骨架）：与 dev/test 相关的 S3 bucket 等资源。

### P0-C1-S2（成本与安全边界约定）

- 所有资源均创建在 AWS playground 账号中，region 固定为 `ap-southeast-2`；
- RDS/等价 DB 实例采用小规格（例如 db.t4g.micro 级别）并启用自动关停/低成本选项（如有）；
- 不在这些资源中存放生产数据或个人敏感信息；
- 在 Billing 控制台中保持预算/告警开启，如预计会超过免费额度，需要在 Evidence 中注明原因和预计成本。

### P0-C1-S3（Evidence contract | v1）

- 每次关键操作需要在 Evidence 中记录：
  - `headSha=<git sha>`；
  - `module_path=<relative path>`（例如 `infra/terraform/aws/devtest-db`）；
  - `command=<terraform subcommand>`（`plan` / `apply` / `destroy`）；
  - `summary=<one-line outcome>`（例如 `apply: 3 added, 0 changed, 0 destroyed`）；
  - （可选）一句话描述当前月度成本预估/资源规模。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4C-2A/P<phase>-C<cycle>-S<steps>: <summary>`，例如：
  - `S4C-2A/P0-C1-S1: define aws network and devtest-db layout`。

**Branch convention**:

- 与本 phase 相关的改动，继续落在 `S4C-cloud-services-and-terraform-minimal-path` 分支上。

**Commit discipline (recommended)**:

- 完成每个 `P*-C*-S*` 后，尽量在 `S4C-*` 分支上及时 `commit/push`，保持 Evidence 易于追踪。

## Plan (draft)

### P1（Implementation）

- P1-C1-S1：在 `infra/terraform/aws/network/` 下创建最小 VPC + 子网 + 安全组模块骨架（暂不 apply）。
- P1-C1-S2：在 `infra/terraform/aws/devtest-db/` 下创建托管 Postgres 模块骨架（参数、变量、outputs），并预留与 network 模块的集成点（通过 `db_subnet_ids`、`db_security_group_id` 等变量接收 network 模块的输出）。
- P1-C1-S3：为上述目录添加 `README.md`，说明资源范围、成本预期和后续 drill 入口。

### P2（Drill / Verify）

- P2-C1-S1：使用 Terraform 在 playground 账号中创建一套最小 dev/test 网络 + Postgres 实例，并记录 `plan/apply` Evidence。
- P2-C1-S2：验证从本机使用 psql 或 wordloom-v3 的某个简单脚本能够连接到该 Postgres，并在 Evidence 中记录连接方法（不包含密码明文）。

### P3（Drill / Wording）

- P3-C1-S1：写一段 interview-style 段落，解释「S4C-2A 这套网络 + DB + 存储如何支持 wordloom-v3 的 cloud-dev 环境」，并链接到 S4C-3A 计划。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`：目录与模块命名约定固定
- [x] `P0-C1-S2`：成本与安全边界约定固定
- [x] `P0-C1-S3`：Evidence contract 固化

### P1（Implementation）

- [x] `P1-C1-S1`：network 模块骨架创建
- [x] `P1-C1-S2`：devtest-db 模块骨架创建
- [x] `P1-C1-S3`：network/devtest-db README 就绪

### P2（Drill / Verify）

- [ ] `P2-C1-S1`：首次 `plan/apply/destroy` drill 入账
- [ ] `P2-C1-S2`：本机连通性 drill 入账

### P3（Drill / Wording）

- [ ] `P3-C1-S1`：interview-style narrative 写入 docs

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log记录 head SHA、关键参数与 artifact 路径（或控制台 URL 的文字描述）。

### P0-C1-S1（S4C-2A contract draft created｜2026-03-22）

- headSha: `<TBD-after-first-S4C-2A-commit>`
- artifacts:
  - `docs/logs/log-S4C-2A-cloud-devtest-db-and-storage.md`
- expected:
  - 明确 S4C-2A 的目录布局、资源范围与成本/evidence 约定，为后续实现与 drills 奠定基础。
- observed:
  - 本 log 已包含上述内容，等待后续 commit 补充 headSha。

### P1-C1-S1（Network module first terraform plan drill｜2026-03-22）

- headSha: `<TBD-after-S4C-2A-network-plan-commit>`
- module_path: `infra/terraform/aws/network`
- commands & outcomes（PowerShell，Windows，本地 state）：
  - `terraform init`
    - provider `hashicorp/aws` (~> 5.0) 成功下载并写入 `terraform.lock.hcl`；
    - 终端输出 `Terraform has been successfully initialized!`。
  - `terraform validate`
    - 输出 `Success! The configuration is valid.`。
  - `terraform plan`
    - 生成 `aws_security_group.cloud_dev_basic`、`aws_subnet.public_a`、`aws_vpc.cloud_dev` 三个资源的执行计划；
    - 末尾摘要：`Plan: 3 to add, 0 to change, 0 to destroy.`；
    - **未执行 `terraform apply`**，此次 drill 仅到 plan 阶段，用于验证 network 模块 wiring 与 provider 配置。

## Recent changes (for traceability, optional)

- 2026-03-22：创建 `S4C-2A` phase skeleton，用于承接 S4C epic 中关于 cloud dev/test network + DB + storage 的最小实现与 drills。
