# log-S4C-1A (Phase 1: Cloud dev/test Terraform bootstrap)

---

**id**: `S4C-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `Cloud dev/test Terraform bootstrap（account + CLI + layout） v1`
**status**: `stable`          # draft | stable | archived
**scope**: `S4`
**tags**: `EVOLUTION, Cloud, Terraform, Drills, Evidence, epic/s4, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4C-cloud-services-and-terraform-epic.md`
  **previous_log**: ``
  **reference_log_1**: `docs/logs/_template-log-phase-drills-evidence.md`
**created**: `2026-03-22`
**updated**: `2026-03-22`

---

## Decision / Outcome

**Decision**:

- 为 cloud dev/test 路线建立一个最小可用的 Terraform bootstrap：从 0 到拥有一个安全的 playground 账号、CLI 登录能力，以及一个清晰的 `infra/terraform` 目录骨架。
- 通过 P0/P1/P2/P3，确保后续关于网络、DB、存储等模块都可以在这一骨架下增量添加，而不会反复改目录结构或 state 位置。

**Default choices (phase defaults / v1)**:

- 先选定单一云平台（例如 AWS），避免初学阶段在 provider 之间频繁切换；
- 默认使用本地 state（`terraform.tfstate`），通过 `.gitignore` 确保 state 不被提交到仓库；
- 所有资源都使用专用 playground 账号/订阅，并在 docs 中记录成本边界与清理策略；
- 以 dev/test env 命名 workspace/env（例如 `cloud-dev`），不直接创建 `prod` env。

## Definitions (optional)

- **playground account**：仅用于练习的云账号或订阅，与个人/工作生产账号隔离。
- **state**：Terraform 记录当前已知资源实际状态的文件或后端。
- **workspace/env**：区分不同环境（cloud-dev / cloud-test）的逻辑命名。

## Constraints

- 本 phase 不创建任何长期存在的云资源，可以只到 `plan` 或创建极少量、立刻销毁的样本资源；
- 所有 CLI/凭证配置必须避免 hard-code 到 repo 内（使用本地配置文件或环境变量）；
- 目录结构一旦在 P0/P1 固定，下一个 phase（S4C-2A）应在此结构之上扩展，而不是推翻重来。

## Scope

- `P0`: contract（命名、目录结构、state/evidence 约定）。
- `P1`: implementation（创建 playground 账号、配置 CLI、初始化 `infra/terraform` 骨架）。
- `P2`: drill / verify（至少一次 `terraform init/validate/plan` 练习，记录 evidence）。
- `P3`: drill / wording（用自己的话总结「Terraform 在整个链路的角色」）。

## Success Criteria (DoD)

- 有一份明确的 contract 说明：
  - 选定了哪一家云平台；
  - Terraform 目录结构如何划分（例如 `infra/terraform/<cloud>/{network,db,storage}`）；
  - state 存放位置与 `.gitignore` 规则。
- 能够在本机成功安装 Terraform/CLI，并对选定云平台完成一次登录配置；
- 至少完成一次 `terraform init/validate/plan`（可以针对一个非常简单的资源），并在 Evidence 中记录 headSha + 命令输出要点；
- 你能用一段稳定的话术解释「Docker/脚本 vs 云服务 vs Terraform」的分工。

## Stability (what stable means)

- 本 log 标记为 `stable` 时：
  - P0 合同不再大改（仅允许小幅补充字段）；
  - Terraform 目录结构和 state/凭证约定稳定，后续 S4C-2A/3A 直接复用；
  - 至少一次成功的 `plan` drill 被记录在 Evidence 中。

## P0 (Contract | v1)

### P0-C1-S1（云平台与 playground 账号约定）

- 选定首选云平台为 **AWS**，后续所有 Terraform 练习默认以 AWS 为 provider；
- 为练习创建专用 AWS playground 账号/子账号，并：
  - 启用基本的计费告警或预算限制；
  - 不在其中存放生产数据或高敏感数据。

### P0-C1-S2（Terraform 目录与 state/evidence 约定）

- 目录约定：
  - AWS 相关 Terraform 代码集中放在 `infra/terraform/aws/` 下；
  - 常见子目录示例：`network/`、`devtest-db/`、`storage/` 等，后续 phase 按需新增。
- state 与 `.gitignore`：
  - 默认使用本地 state 文件 `terraform.tfstate`，位于各模块目录或上层 env 目录；
  - 在仓库根或 `infra/terraform` 下的 `.gitignore` 中忽略 `*.tfstate` 及其备份；
  - 如未来切换到 remote backend，再在 S4C-2A 或 S4C-3A 中更新约定。

### P0-C1-S3（Evidence contract | v1）

- 每次执行 Terraform 关键命令时，应保留最小 evidence：
  - `headSha=<git sha>`；
  - `command=<terraform subcommand>`（如 `init`/`validate`/`plan`）；
  - `module_path=<relative path>`；
  - `summary=<one-line outcome>`（例如 `plan: 1 to add, 0 to change, 0 to destroy`）。
- Evidence 可以记录在本 log 的 Evidence 区，或在后续 S4C-2A/3A 中引用。
 - Evidence 可以记录在本 log 的 Evidence 区，或在后续 S4C-2A/3A 中引用。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4C-1A/P<phase>-C<cycle>-S<steps>: <summary>`，例如：
  - `S4C-1A/P0-C1-S1: choose cloud provider and playground account`。

**Branch convention**:

- 本 phase 隶属于 `S4C` scope，相关改动默认落在 `S4C-cloud-services-and-terraform-minimal-path` 分支上。

**Commit discipline (recommended)**:

- 完成每个 `P*-C*-S*` 单元后，尽量在 `S4C-*` 分支上及时 `commit/push`；
- 如需跨 scope/index（例如同时修改 S5B 日志），推荐拆分提交。

## Plan (draft)

### P1（Implementation）

- P1-C1-S1：选定云平台（AWS），创建并启用个人 playground 账号，在 docs 中记录：账号类型（个人练习）、默认 region（如 `ap-southeast-2`）、以及当前成本边界（例如免费额度/预算上限）。
- P1-C1-S2：安装 Terraform + AWS CLI，在本机完成登录配置，并在 `infra/terraform/aws/` 下创建最小目录骨架（含 `.gitignore`）。

### P2（Drill / Verify）

- P2-C1-S1：在 `infra/terraform/aws/examples/bootstrap/` 目录执行一次 `terraform init` / `terraform validate` / `terraform plan`，并在本 log 的 Evidence 中记录 headSha + 关键输出摘要（不粘贴敏感信息）。

### P3（Drill / Wording）

- P3-C1-S1：写一段 interview-style 段落，说明「从本地 Docker/脚本 → 云服务 → Terraform/IaC」的关系，并链接到本 log 与 `road-001`。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`：云平台与 playground 账号约定固定（选定 AWS）
- [x] `P0-C1-S2`：Terraform 目录与 state/evidence 约定固定（`infra/terraform/aws`）
- [x] `P0-C1-S3`：Evidence contract 固化

### P1（Implementation）

- [x] `P1-C1-S1`：playground 账号创建并记录（个人 AWS 账号 + `ap-southeast-2` + 免费额度边界）
- [x] `P1-C1-S2`：本机 CLI + Terraform 安装 & 目录骨架就绪（`infra/terraform/aws`）

### P2（Drill / Verify）

- [x] `P2-C1-S1`：首次 `terraform plan` drill 入账

### P3（Drill / Wording）

- [x] `P3-C1-S1`：interview-style narrative 写入 docs

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P0-C1-S1（Cloud dev/test Terraform bootstrap contract established｜2026-03-22）

- headSha: `<TBD-after-first-commit>`
- artifacts:
  - `docs/logs/log-S4C-cloud-services-and-terraform-epic.md`
  - `docs/logs/log-S4C-1A-cloud-devtest-terraform-bootstrap.md`
- expected:
  - 明确 cloud dev/test Terraform bootstrap 的合同与目录约定，为后续 S4C phases 提供稳定骨架。
- observed:
  - 本 log 已经写明上述 contract，并在 Execution Checklist 中预留对应项，后续提交会补充 headSha。

### P1-C1-S1（AWS playground 账号与 region 确认｜2026-03-22）

- headSha: `<TBD-after-first-terraform-drill>`
- summary（non-sensitive）:
  - 账号类型：个人 AWS playground 账号，用于 cloud/devtest 练习；
  - 当前 region：`ap-southeast-2`（Asia Pacific, Sydney）；
  - 成本边界：采用 AWS 免费计划 / 赠送额度（约 US$100，约 185 天有效期），作为 early-phase 练习的主要费用上限，后续如需额外预算再补充 Billing Alarm/预算规则。

### P1-C1-S2（AWS CLI + Terraform 安装与本机登录配置｜2026-03-22）

- headSha: `<TBD-after-first-terraform-drill>`
- env: Windows 10/11 + PowerShell
- commands:
  - `aws --version` → `aws-cli/2.34.14 Python/3.14.3 Windows/10 exe/AMD64`（摘要）；
  - `terraform version` → `Terraform v1.14.7 on windows_amd64`；
  - `aws configure` → 默认 profile，region=`ap-southeast-2`，output=`json`，访问密钥仅保存在本机，不出现在仓库或日志中。

### P2-C1-S1（First terraform init/validate/plan drill｜2026-03-22）

- headSha: `<TBD-after-next-S4C-1A-commit>`
- module_path: `infra/terraform/aws/examples/bootstrap`
- commands & outcomes（PowerShell，Windows，本地 state）：
  - `terraform init`
    - provider `hashicorp/aws` (~> 5.0) 成功下载并写入 `terraform.lock.hcl`；
    - 终端输出 `Terraform has been successfully initialized!`。
  - `terraform validate`
    - 输出 `Success! The configuration is valid.`。
  - `terraform plan`
    - 针对 `aws_s3_bucket.bootstrap` 生成执行计划；
    - 末尾摘要：`Plan: 1 to add, 0 to change, 0 to destroy.`；
    - **未执行 `terraform apply`**，此次 drill 仅到 plan 阶段。

### P3-C1-S1（Docker / Cloud services / Terraform narrative｜2026-03-22）

- 本地 Docker / 脚本：
  - 主要用于在个人开发机上把基础设施类依赖（DB、ES、observability 等）隔离出来，用 compose / 脚本统一起停，减少「手工点服务 + 本地环境污染」的问题；
  - 对单人或少量开发者来说，可以快速复现一套近似的依赖组合，但它本身仍然是「跑在你这台机器上的临时环境」。
- 云服务（AWS RDS / S3 等）：
  - 把这些基础设施搬到云账号里，由云厂商托管运行和高可用，你不需要在各种混合环境里手工建库、配磁盘；
  - 对团队协作来说，好处是：环境是统一的、配置可以复用，权限/网络边界清晰，不容易因为「每个人本地都不一样」而失真。
- Terraform / IaC：
  - 站在本地应用和云服务之间，作为「描述云资源的合同层」，用代码来定义 VPC、DB、S3 等，而不是登录控制台到处点；
  - 所有改动都通过 commit + plan/apply 流程进入云环境，可以避免「console 上手动改了一堆结果没人记得」这种 configuration drift；
  - 这次 S3 bucket 示例就是一个最小的 contract：`main.tf` 里写清楚 bucket 名称和 tags，`plan` 告诉你「如果 apply 会新增 1 个 bucket」。
- 关于 drill 和 S3 bucket 的关系：
  - 对我来说，本 phase 的 drill 概念是「一小段可重复的链路练习 + 最小证据」：你从 `terraform init` 开始到 `plan` 结束，证明 toolchain、凭证、目录、state 约定都能正常工作；
  - observability 里的 drill 更多是运行时生成日志/指标，这里的 S3 bucket drill 更像是「控制平面」层面的练习：不一定真的 apply，但已经验证了声明式合同（Terraform 配置）和云 API 之间是打通的。

## Recent changes (for traceability, optional)

- 2026-03-22：初始化 `S4C-1A`，定义 cloud dev/test Terraform bootstrap 的合同与计划，用于承接原 `road-001-2` 中的 Terraform 学习路径。