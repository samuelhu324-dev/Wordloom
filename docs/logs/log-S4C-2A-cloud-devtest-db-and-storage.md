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
- 对于本机连通性 drill，优先采用“临时公网访问 + 白名单公网 IPv4/32 + drill 完成后立即 destroy/收口”的最小方案；bastion/SSM 作为后续更安全但更复杂的演进方向。
- 这意味着 v1 会接受一个明确 trade-off：为了先理解 endpoint / SG / subnet / public accessibility 的关系，允许短时把 RDS 放到“可公网访问 + 白名单 IP”的教学模式；但长期目标仍是私网 RDS + 跳板/SSM 接入。

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

- P2-C1-S1：先把 network 模块扩展为可承载 RDS 的最小结构（至少 2 个不同 AZ 的 DB 子网 + DB 专用 SG），再使用 Terraform 创建一套最小 dev/test 网络 + Postgres 实例，并记录 `plan/apply` Evidence。
- P2-C1-S2：验证从本机使用 psql 或 wordloom-v3 的某个简单脚本能够连接到该 Postgres，并在 Evidence 中记录连接方法（不包含密码明文）。当前优先采用“临时公网访问 + 白名单 IP + 练习后立即收口/销毁”的最小 drill，而不是直接引入 bastion/SSM。

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

- [x] `P2-C1-S1`：首次 `plan/apply/destroy` drill 入账
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

- headSha: `bd68d34f`
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

### P2-C1-S1（Network apply completed and outputs captured｜2026-03-22）

- headSha: `fc02054d`
- module_path: `infra/terraform/aws/network`
- commands & outcomes（PowerShell，Windows，本地 state）：
  - `terraform apply`
    - 根据既有 plan 成功创建了 3 个资源：VPC、public subnet、basic security group；
    - apply 后通过 `terraform output` 拿到了后续 devtest-db 需要的接线信息（`vpc_id`、`public_subnet_id`、`basic_sg_id`）。
  - `terraform validate`
    - apply 后再次验证，配置仍然有效。
  - `terraform plan`
    - 输出 `No changes. Your infrastructure matches the configuration.`，说明 state 与当前配置一致，没有 drift。
- note:
  - 这一步完成了 P2-C1-S1 的 network 侧前半段，为 devtest-db 模块的 plan/apply 做好了基础网络与输入变量准备；
  - 整个 P2-C1-S1 仍未完成，因为 Postgres 实例的 plan/apply/destroy 还没有执行。

### P2-C1-S1（Network expanded for RDS prerequisites｜2026-03-22）

- headSha: `df649235`
- module_path: `infra/terraform/aws/network`
- commands & outcomes（PowerShell，Windows，本地 state）：
  - `terraform plan`
    - 计划新增 3 个资源：`aws_security_group.db`、`aws_subnet.db_a`、`aws_subnet.db_b`；
    - 计划新增 2 个 outputs：`db_sg_id`、`db_subnet_ids`；
    - 末尾摘要：`Plan: 3 to add, 0 to change, 0 to destroy.`；
    - 说明这次 network 扩展会在保留既有 `vpc/public_subnet/basic_sg` 的前提下，补齐 RDS 需要的最小双 AZ DB 子网与 DB 专用安全组。
- changes prepared:
  - 新增 2 个 DB 专用子网：`db_a`（`ap-southeast-2a`）与 `db_b`（`ap-southeast-2b`）；
  - 新增 1 个 DB 专用 SG：仅允许来自 `cloud_dev_basic` SG 的 5432/TCP 流量；
  - 新增输出：`db_subnet_ids`、`db_sg_id`，供 `devtest-db` 模块接线。
- reason:
  - 这是 RDS 常见前置条件：DB subnet group 需要至少覆盖 2 个 AZ；
  - 先把 network 拆清楚，可以让 `devtest-db` 模块保持 decoupled，并降低后续 apply/destroy 的误操作范围。

### P2-C1-S1（First devtest-db plan/apply attempt blocked by provider constraints｜2026-03-22）

- headSha: `<TBD-after-devtest-db-fix-commit>`
- module_path: `infra/terraform/aws/devtest-db`
- observed:
  - `terraform validate` 成功；
  - `terraform plan` 成功生成了 `aws_db_subnet_group.devtest` 与 `aws_db_instance.devtest` 的创建计划，摘要为 `Plan: 2 to add, 0 to change, 0 to destroy.`；
  - 首次 `terraform apply` 中，`aws_db_subnet_group.devtest` 成功创建，但 `aws_db_instance.devtest` 创建失败，AWS 返回：`InvalidParameterCombination: Cannot find version 16.3 for postgres`；
  - 同时暴露出本地 `terraform.tfvars` 中存在旧字段 `db_sg_id` 的 warning，说明变量命名需要向前兼容或清理。
- fix:
  - 将 `db_engine_version` 改为可配置且默认 `null`，让 AWS 自动选择当前 region / instance class 支持的 Postgres 版本；
  - 为 `db_security_group_id` 增加向前兼容别名 `db_sg_id`，并在模板中继续推荐使用 `db_security_group_id`；
  - 保持 `db_subnet_ids` 至少两个子网的约束不变。

### P2-C1-S1（devtest-db apply succeeded after engine-version fix｜2026-03-22）

- headSha: `c7cc4a27`
- module_path: `infra/terraform/aws/devtest-db`
- commands & outcomes（PowerShell，Windows，本地 state）：
  - `terraform plan`
    - 末尾摘要：`Plan: 1 to add, 0 to change, 0 to destroy.`；
    - 这里只有 1 个 add 是符合预期的，因为更早那次失败的 apply 已经成功创建并保存了 `aws_db_subnet_group.devtest`，这次修复后只剩 `aws_db_instance.devtest` 需要创建。
  - `terraform apply`
    - `aws_db_instance.devtest` 创建成功；
    - 终端输出摘要：`Apply complete! Resources: 1 added, 0 changed, 0 destroyed.`。
  - `terraform output`
    - `db_endpoint = wlv3-cloud-dev-postgres.cbemuq6kv2pw.ap-southeast-2.rds.amazonaws.com:5432`
    - `db_identifier = db-AUYH7A2MQBAXS3GP3YRDXWJHCY`
    - `db_port = 5432`
- note:
  - 这一步说明最小 RDS Postgres 资源已经在 AWS playground 账号中成功创建；
  - 但当前 `publicly_accessible = false`，且 DB SG 只允许来自 `cloud_dev_basic` SG 的 5432 流量，因此你的本机还不能直接连上这台 DB；
  - 因此 `P2-C1-S1` 的 apply 部分已经完成，但 `P2-C1-S2`（本机连通性 drill）还需要额外的访问路径设计（例如临时开放白名单公网访问，或增加 bastion / SSM 跳板方案）。

### P2-C1-S1（Full plan/apply/destroy drill completed｜2026-03-22）

- headSha: `c7c084f5`
- module_path: `infra/terraform/aws/devtest-db`
- summary:
  - `plan` 已验证最小 Postgres 资源会被创建；
  - `apply` 已成功创建 `aws_db_instance.devtest`，并产出 `db_endpoint` / `db_port` / `db_identifier`；
  - `destroy` 已成功执行，终端摘要：`Destroy complete! Resources: 2 destroyed.`，说明 `aws_db_instance.devtest` 与 `aws_db_subnet_group.devtest` 均已清理。
- outcome:
  - 这次 drill 证明 S4C-2A 已经具备完整的最小 cloud-dev DB 生命周期能力：`plan -> apply -> output -> destroy`；
  - 因此 `P2-C1-S1` 可以标记为完成，后续重点转入 `P2-C1-S2` 的“本机如何安全地连到这台 DB”。

### P2-C1-S2（Temporary public-access connectivity path prepared｜2026-03-22）

- headSha: `<TBD-after-p2-c1-s2-prep-commit>`
- module_paths:
  - `infra/terraform/aws/network`
  - `infra/terraform/aws/devtest-db`
- prepared changes:
  - `network` 模块新增 `allowed_postgres_cidrs`，允许在 DB SG 上临时对白名单公网 IPv4/32 放开 5432；
  - `devtest-db` 模块新增 `db_publicly_accessible`，默认 `false`，做本机直连 drill 时临时切换到 `true`；
  - `terraform.tfvars.example` 已更新为这条 drill 路线：先加白名单 IP，再临时开启公网访问，练习后立即收口。
- intent:
  - 用最小改动把“本机直连 RDS”的路径打通，优先帮助理解 endpoint / SG / subnet / public accessibility 的关系；
  - 后续如果要升级安全性，再演进到 bastion / EC2 / SSM 跳板方案。

### P2-C1-S2（First temporary public-access attempt failed at VPC internet edge｜2026-03-22）

- headSha: `3842c39b`
- module_path: `infra/terraform/aws/devtest-db`
- observed:
  - network 模块已输出 `allowed_postgres_cidrs = ["49.196.216.90/32"]` 与新的 `db_sg_id`；
  - 但在 `db_publicly_accessible = true` 的情况下执行 `terraform apply`，AWS 返回：
    - `InvalidVPCNetworkStateFault: Cannot create a publicly accessible DBInstance. The specified VPC has no internet gateway attached.`
- root_cause:
  - 当前 VPC 虽然已有 public subnet 概念，但没有实际的 Internet Gateway 与 public route table，因此不满足“publicly accessible RDS”对 VPC internet edge 的最低要求；
  - 同时，做本机直连 drill 时，`db_subnet_ids` 也应临时切换为 network 的 `public_subnet_ids`，而不是继续使用 private-style DB 子网。
- trade_off:
  - 这次决定继续走“临时公网访问 + 白名单 IP”路线，而不是立即切换到 bastion/SSM；
  - 原因是当前阶段的学习重点仍然是把 VPC/IGW/public route/SG/RDS endpoint 这条直连路径讲清楚，先把最小网络原语吃透，再升级到更安全但更复杂的跳板方案。

## Recent changes (for traceability, optional)

- 2026-03-22：创建 `S4C-2A` phase skeleton，用于承接 S4C epic 中关于 cloud dev/test network + DB + storage 的最小实现与 drills。
