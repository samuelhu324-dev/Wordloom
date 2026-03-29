# road-S1-1-gov-role-minimal-ops-loop

---

**id**: `road-S1-1`
**kind**: `roadmap`
**title**: `S1-1: Government-role minimal systems/platform ops loop`
**status**: `draft`
**scope**: `S1`
**tags**: `ROADMAP, systems/platform, government-role, minimal-loop`
**links**: ``
  **parent_road**: `docs/roadmap/road-S1-systems-platform-ops-roadmap-v5.md`
  **source**: `legacy/from_structured_docs/from-roadmap/ROADMAP v5.md`
  **reference_template**: `docs/roadmap/road-template-branch-roadmap.md`
  **reference_log_1**: `docs/logs/log-S4B-infra-as-code-and-runtime-packaging.md`
  **reference_log_2**: `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
  **reference_log_3**: `docs/logs/log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md`
  **reference_log_4**: `docs/logs/log-S5A-3B-backup-restore-sanitize-verify.md`
**created**: `2026-03-21`
**updated**: `2026-03-29`

---

## Positioning

**Context / role targeting**

- 这一份 `road-S1-1` 是 `road-S1`（ROADMAP v5）的一个子路线，专门聚焦“对准政府这个岗需要的所有最小闭环 / 技术需求”。
- 它不是覆盖 ROADMAP v5 的全部广度，而是从中挑出对岗位描述最直接命中的那一圈：
  - systems / platform operations
  - automation / scripting / reproducible environment
  - backup / recovery / disaster readiness
  - documented sustainable runtime
- 在当前仓库记账边界上，`road-S1-1` 不负责承接 `S4C/S4D` 这类继续向 cloud/runtime 主心骨演进的主线；它更准确的职责，是把 `S4B` 的本地最小 runtime / scripting / Terraform baseline，连同 `S5A-3B` 的 recovery sample 和 `S4A` 的方法论语言，收口成“现在就能讲”的政府岗最小闭环。

**One-sentence goal**

- Deliver a minimal but real systems/platform ops loop around wordloom-v3 that can be confidently explained in a government-style interview.

## Scope & Audience

- **Primary audience**: 招聘 JD 中的 systems / platform operations / DevOps-support 岗位（含政府 / 公共部门）。
- **Relation to road-S1**: 从 road-S1 的完整路线中抽取必需的最小闭环，优先完成可以“现在就讲”的部分。
- **Time horizon**: 约 4–8 周，可滚动拉长，但 v1 聚焦最小闭环，而不是所有增强项。

## Parent / Branch Rules

- `road-S1-1` 是 `road-S1` 之下的支线 road，不是第二条独立主线。
- 它存在的原因，是把一段 focused minimal loop 集中解决掉，而不污染 `road-S1` 的长线 narrative。
- 但它完成的 child logs 仍然属于 `road-S1` 的一部分，因此 branch ledger 和 parent ledger 都需要显式记账同一批 child logs。
- 如果某个 slot 暂时没有合适的 child log，就必须写 `unmapped`，不能继续藏在 prose 中。

## Roadmap / Log Bridge Contract

- This branch road owns focused selection and parent alignment.
- Child logs remain the canonical implementation rows.
- Any output that counts back to `road-S1` must be stated explicitly in both the branch ledger and the parent road ledger.

## Parent Contribution Ledger

- `road-S1 M1-P0 <- docs/logs/log-S4A-1A-ops-scripting-baseline.md`
- `road-S1 M1-P1 <- docs/logs/log-S4A-5A-operational-visibility-and-post-change-verification.md`
- `road-S1 M2-P0 <- docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `road-S1 M2-P1 <- docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `road-S1 M2-P2 <- docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `road-S1 M2-P3 <- docs/logs/log-S4A-1A-ops-scripting-baseline.md`
- `road-S1 M3-P0 <- docs/logs/log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md`
- `road-S1 M4-P0 <- docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`
- `road-S1 M5-P0 <- docs/logs/log-S4A-4A-hybrid-runtime-awareness.md`
- `road-S1 M5-P1 <- docs/logs/log-S5A-3B-object-storage-backup.md`

## Current ownership boundary

- `road-S1-1` 的主完成面当前应以 `S4B` 为核心：也就是 from-zero runtime、ops scripts、Terraform skeleton 与 deployable dev/test baseline；
- `S4A` 在这条子路线里主要提供 hard-gate / post-change verification / operator wording 的方法来源，而不是作为当前主完成面的整棵树全量纳入；
- `S5A-3B` 继续作为 backup / recovery / sanitise / verify 的最小 recovery sample；
- `S4C` 与 `S4D` 则应明确算在 `road-S1` 主线里，因为它们承接的是 cloud services / cloud runtime deploy-verify-rollback 的持续演进，而不是政府岗最小闭环的主记账面。

## Milestone overview (picked from ROADMAP v5)

- **M2. IaC / scripting / automation**（Bash + Terraform + 现有 GitHub workflows）
- **M3. Runtime packaging & deploy / verify / rollback**（Docker/compose + scripts + post-change verification）
- **M4. Backup / recovery / operational support narrative**（S5A-3B 为核心样本）

Cloud fundamentals / hybrid awareness 仍然重要，但在 `road-S1-1` 中只要求能讲“基本概念 + 如何往上长”，不要求马上交付完整云侧样本。

**Current evidence base (v1)**

- `S4B`：作为最小闭环的主资产来源，提供 from-zero runtime、ops scripts、Terraform skeleton、deployable dev/test baseline；
- `S4B` 顶层 spine 已在 2026-03-25 正式标记为 `stable`，因此这里引用的不再只是分散样本，而是一个已经完成 parent/child 对齐记账的最小 runtime/IaC 闭环；
- `S4A`：提供 systems/platform wording、hard-gate、post-change verification 与 fallback 叙事的方法来源；
- `S5A-3B`：提供 backup / recovery / sanitise / verify 的恢复闭环样本；
- `S4C/S4D`：保留在 `road-S1` 主线中，作为“如果继续往 cloud/runtime 主心骨延伸，会如何增长”的上层方向，而不是本子路线当前的主完成面。

## Milestones (M1–M5) and current status

> 说明：这里用 `M*` 表达里程碑而不是线性 Phase；每个 M* 内部用 P0–P3 来描述 contract / implementation / drills，但整体是推荐顺序，而非硬性时间线。

### M1: Systems administration / operational support language

**Goal**

- 能够用 systems/platform operations 语言，自然描述 wordloom-v3 的运行面：installation、configuration、maintenance、monitoring、backup/recovery、operational support、lifecycle management。

**Bridge Ledger (child logs only)**

- `M1-P0`:
  - `docs/logs/log-S4A-1A-ops-scripting-baseline.md`
- `M1-P1`:
  - `docs/logs/log-S4A-5A-operational-visibility-and-post-change-verification.md`
- `M1-P2`:
  - `unmapped`
- `M1-P3`:
  - `unmapped`

**Parent alignment**

- `road-S1 M1-P0 <- docs/logs/log-S4A-1A-ops-scripting-baseline.md`
- `road-S1 M1-P1 <- docs/logs/log-S4A-5A-operational-visibility-and-post-change-verification.md`

**Plan (P0–P3)**

- `P0` Contract: 梳理最小 vocabulary、典型句子，并把现有资产（S4A/S5A/S6A）映射到这些词。
- `P1` Implementation: 写 1–2 页 note/cheatsheet，并在若干 log/runbook 里嵌入这些表述。
- `P2` Drill: 设计 1–2 个面试式问答，专门用这套语言讲解 S4A-5A、S5A-3B、S4B-1A/2A。
- `P3` Drill: 根据复盘修改 wording，把稳定版本固化到 docs 里。

**Execution Checklist**

- [ ] `M1-P0`: vocabulary + mapping note（根据 ROADMAP v5 文本起草）。
- [ ] `M1-P1`: 至少 1–2 个 log/runbook 使用 systems/platform 语言重写了“Decision / Outcome”。
- [ ] `M1-P2`: 至少一次 mock interview Q&A（可在 docs/interview/ 下落地）。
- [ ] `M1-P3`: 稳定版 wording 记录在 roadmap / logs 中。

**Status (2026-03-21)**

- ROADMAP v5 已经给出了详细的语言方向和关键词，但还停留在说明层：`部分完成（contract 思想已写好，具体 note/cheatsheet 还未落地）`。

### M2: Bash + automation scripts（runtime operations）

**Goal**

- 保持一套小而实在的 Bash 脚本（start/stop/health/backup/logs），对齐 ROADMAP v5 的“automation / scripting / reproducible environment” 优先级，并且有从-zero-to-dev/test 的演练和 evidence。

**Bridge Ledger (child logs only)**

- `M2-P0`:
  - `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `M2-P1`:
  - `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `M2-P2`:
  - `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `M2-P3`:
  - `docs/logs/log-S4A-1A-ops-scripting-baseline.md`

**Parent alignment**

- `road-S1 M2-P0 <- docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `road-S1 M2-P1 <- docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `road-S1 M2-P2 <- docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `road-S1 M2-P3 <- docs/logs/log-S4A-1A-ops-scripting-baseline.md`

**Plan (P0–P3)**

- `P0` Contract: 明确脚本命名、目录、输入参数、输出（包括 evidence 风格）；和 S4B-1A/S4A-2A 的 contract 对齐。
- `P1` Implementation: 盘点并轻量收敛 `scripts/` 与 `scripts/ops/`（例如 `env_prep.sh`, `start.sh`, `status.sh`, `health.sh` 等）。
- `P2` Drill: 在 WSL 上从零跑通 dev/test 路径（已完成一次 FAIL→PASS），并记录 evidence JSON/TXT。
- `P3` Drill: 写 operator-facing runbook + 面试话术。

**Execution Checklist**

- [x] `M2-P0`: 合同思想在 S4B-1A/S4A spine 中已经形成（从-zero-to-dev/test 路径、artifacts 不进 git、evidence JSON 字段等）。
- [x] `M2-P1`: 核心脚本集已经存在并在 S4B-1A 中被清点和引用。
- [x] `M2-P2`: 从零到 dev/test 的 FAIL→PASS 演练已经在 WSL 上完成，并在 S4B-1A Evidence 中记录。
- [x] `M2-P3`: runbook `run-S4B-1A-from-zero-to-devtest-runtime.md` 和对应的面试故事骨架已存在。

**Status (2026-03-21)**

- `M2` 基本视为 v1 完成，后续更多是小幅打磨（命名统一度、runbook 细节），不再是 open gap。

### M3: Terraform / IaC minimal sample

**Goal**

- 交付一份可运行的 Terraform/IaC 最小样本，用来定义 dev/test 基础设施（目前是 devtest DB），强调 repeatable environment，而不是复杂云平台能力。

**Bridge Ledger (child logs only)**

- `M3-P0`:
  - `docs/logs/log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md`
- `M3-P1`:
  - `docs/logs/log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md`
- `M3-P2`:
  - `docs/logs/log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md`
- `M3-P3`:
  - `docs/logs/log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md`

**Parent alignment**

- `road-S1 M3-P0 <- docs/logs/log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md`

**Plan (P0–P3)**

- `P0` Contract: 明确 scope 只覆盖 dev/test；资源边界和 evidence contract；避免假装 production 级别。
- `P1` Implementation: 在 `infra/terraform/` 下实现 skeleton module（当前是 `devtest-db`）。
- `P2` Drill: 在 WSL 中安装 Terraform，并针对 skeleton 执行 `terraform init/validate/plan` drill，记录 evidence。
- `P3` Drill: 写 operator-facing wording + interview narrative，说明这是什么级别的 IaC 能力。

**Execution Checklist**

- [x] `M3-P0`: 在 `log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md` 中已经写明 contract 和 v1 范围。
- [x] `M3-P1`: `infra/terraform/devtest-db` skeleton （variables/main/outputs） 已实现并对齐 `.env.dev` / compose。
- [x] `M3-P2`: Terraform 已在 WSL 安装；`init/validate/plan` drill 已跑通，并在 S4B-2A Evidence 中记录 headSha 与 artifact。
- [x] `M3-P3`: S4B-2A 中已写入 operator-facing wording 和 interview story 入口。

**Status (2026-03-21)**

- `M3` v1 已完成（devtest-db skeleton + plan drill）。后续可以按需要扩到 MinIO 或其它模块，但不属于这一轮最小闭环的刚需。

### M4: Docker + deployable runtime & post-change verification

**Goal**

- 展示一套可部署、可验证、可回滚意识的 runtime：包括 Dockerfile/compose/env/health，以及 deploy → verify → fallback 的闭环。

**Bridge Ledger (child logs only)**

- `M4-P0`:
  - `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`
- `M4-P1`:
  - `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `M4-P2`:
  - `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
- `M4-P3`:
  - `docs/logs/log-S4A-5A-operational-visibility-and-post-change-verification.md`

**Parent alignment**

- `road-S1 M4-P0 <- docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`

**Plan (P0–P3)**

- `P0` Contract: 定义 “deployable runtime（dev/test）” 的含义（包括 health 入口、evidence 风格、回滚策略）。
- `P1` Implementation: 盘点并整理 Dockerfile、compose 文件、env 模板与健康检查脚本。
- `P2` Drill: 至少一次“部署 + smoke verify” drill，附带 evidence。
- `P3` Drill: 写出 rollback/fallback 的叙事（可以利用 S4A-2A/S3A 的 hard gate 和 post-change verification 思维）。

**Execution Checklist**

- [x] `M4-P0`: 已在本 roadmap 中写清「deployable runtime（dev/test）」的 contract，并在相关 logs 中建立引用。
- [x] `M4-P1`: 实际上已有一套 Docker/compose/env + health.sh 体系，并在 S4B-1A 中被使用（从-zero-to-dev/test runtime）。
- [x] `M4-P2`: 已选定 S4B-1A 中一次典型 from-zero → runtime 的运行作为“部署 + smoke verify” drill，并在此处与 log 中建立 evidence 链接。
- [x] `M4-P3`: 已在本 roadmap 中集中写出 rollback/fallback 的叙事，并指向 S3A/S6A 的 hard gate / post-change verification 思维。

**Status (2026-03-21)**

- `M4` v1 已完成：基础设施（scripts + compose + health）与 from-zero drill 已存在，本 roadmap 现在补上了 deployable runtime contract、选定并链接了典型部署+验证 drill，并集中写出了 rollback/fallback 叙事；后续主要是随实际云/更复杂环境演进时做增强。

**Contract snapshot（v1）**

- dev/test 的 deployable runtime 至少包含：
  - 有版本控制的 Dockerfile（app/ui 等）、compose 文件和 `.env.*` 模板；
  - 可在 WSL 上一键拉起的脚本入口（例如 `scripts/ops/start.sh dev app` + `scripts/ops/start.sh dev infra`）；
  - 明确的 health 检查入口（`scripts/ops/health.sh dev` 或 HTTP health endpoint），以及必要时的 log 检查路径；
  - 出问题时可以回退到“上一个已知可用 compose/env 版本”的策略，而不是在坏状态上反复 patch。

**Canonical drill（v1）**

- 典型 drill 选用 `log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md` 中的 from-zero-to-dev/test 运行：
  - 在干净环境下执行 env_prep + start.sh（infra/db/app）组合；
  - 通过 health.sh / HTTP 检查确认应用可用；
  - 把关键命令、headSha 和结果写入 Evidence（已在 S4B-1A 中实现）。
- 这个 drill 在 S1-1 语境下被视为“部署 + smoke verify”的标准样本，可在面试中直接引用。

**Rollback / fallback 叙事（v1）**

- 概念上采用 "prefer revert over hotfix"：
  - 如果部署后 health 检查失败，优先回退到上一个已知可用的 compose/env 版本，而不是在坏版本上打补丁；
  - 回退后重新执行 from-zero drill 确认恢复；
  - 利用 S3A/S6A 的 hard gate / post-change verification 思维，将“通过 health + evidence 才允许继续后续更改”视为默认策略。

---

### M5: Backup / recovery minimal story (with light cloud/hybrid framing)

**Goal**

- 巩固 backup/recovery 叙事（以 S5A-3B 为核心），并在此基础上加一层 cloud/hybrid 基础认知，用于面试和岗位对话；不要求立刻交付完整云侧样本。

**Bridge Ledger (child logs only)**

- `M5-P0`:
  - `docs/logs/log-S4A-4A-hybrid-runtime-awareness.md`
- `M5-P1`:
  - `docs/logs/log-S5A-3B-object-storage-backup.md`
- `M5-P2`:
  - `docs/logs/log-S5A-3B-object-storage-backup.md`
- `M5-P3`:
  - `docs/logs/log-S4A-4A-hybrid-runtime-awareness.md`

**Parent alignment**

- `road-S1 M5-P0 <- docs/logs/log-S4A-4A-hybrid-runtime-awareness.md`
- `road-S1 M5-P1 <- docs/logs/log-S5A-3B-object-storage-backup.md`

**Plan (P0–P3)**

- `P0` Contract: 定义“最小 cloud/hybrid scope”（IAM/VPC/RDS/S3/CloudWatch basics），以及如何与现有 backup/recovery 资产对齐。
- `P1` Implementation: 写一份 mapping note：把 S5A-3B 的 backup/upload/restore/sanitize/verify 映射到岗位描述里的 disaster readiness / recoverability narrative。
- `P2` Drill: 至少一次 backup/restore drill 的 evidence（已有），外加一段 cloud/hybrid 视角的解释。
- `P3` Drill: 写出 1–2 段面试话术，把 on-prem/devtest 与 cloud basics 串起来。

**Execution Checklist**

- [x] `M5-P0`: 已在本 roadmap 中定义最小 cloud/hybrid scope，并说明与现有 backup/recovery 资产的关系。
- [x] `M5-P1`: 在本节中写出 mapping note，把 S5A-3B 的 backup/upload/restore/sanitize/verify 映射到 disaster readiness / recoverability narrative。
- [x] `M5-P2`: S5A-3B 的 backup/restore/sanitize/verify drill 和 evidence 已经存在。
- [x] `M5-P3`: 在本节中固化 1–2 段面试话术，把 on-prem/devtest 与 cloud basics 串起来。

**Status (2026-03-21)**

- `M5` v1 已完成：backup/recovery 的技术闭环仍以 S5A-3B 为核心，本 roadmap 现在补完了最小 cloud/hybrid contract、mapping note 和稳定面试话术；后续只需在真正引入云侧样本时做增量更新。

**Cloud/hybrid minimal contract（v1）**

- 这一轮只要求对下面概念有清晰、可讲的认知，而非完整生产级实践：
  - IAM basics（谁可以访问备份、恢复环境）；
  - VPC / 网络分区的基本概念（备份/恢复流量走哪条路）；
  - RDS / S3 或等价服务作为“托管数据库 + 对象存储”的代表；
  - CloudWatch 或等价监控服务，作为备份/恢复过程中的日志与告警来源；
  - 如何用这些概念解释：本地 dev/test → 云上（或混合）环境的迁移与恢复思路。

**Mapping note（v1）**

- S5A-3B 里的步骤可以直接映射到岗位语言：
  - `backup` → periodic snapshots / backups，保护关键业务数据；
  - `upload` → off-site / off-box storage，将备份放到独立介质（例如对象存储或异地）；
  - `restore` → recovery procedure，从备份恢复到新的或干净的环境；
  - `sanitize` → data sanitisation / privacy protection，确保恢复或导出时不泄露敏感字段；
  - `verify` + evidence JSON → recoverability verification / disaster recovery drill，有客观记录可审计。
- 在 cloud/hybrid 语境下，可以简单描述为：
  - 本地 dev/test 侧执行备份和初步恢复流程；
  - 把备份推到云侧对象存储（如 S3）或等价服务；
  - 在需要时，可以在云侧或另一环境执行受控恢复，并通过日志与监控确认成功。

**Interview wording（v1）**

- 中文版要点：
  - “我在 wordloom-v3 里有一套完整的备份与恢复流程，包括备份、上传到独立存储、在新环境中恢复、做脱敏处理，以及用 evidence JSON 记录每次演练的结果。现在这套流程可以很自然地套到 cloud/hybrid 语境：把对象存储换成云上的 S3 之类的服务，恢复目标可以是云中托管数据库或新的虚机，但流程仍然是备份 → 上传 → 恢复 → 验证。”
- 英文简版：
  - “In wordloom-v3 I maintain a full backup-and-recovery loop: backup, upload to an independent store, restore into a clean environment, sanitise sensitive data, and record every run as evidence JSON. This maps directly to a cloud or hybrid setup: object storage becomes S3 or similar, the restore target can be a managed database or VM in the cloud, but the operational narrative stays the same – backup, upload, restore, verify.”

## Evidence Pointers (cross-log)

- Runtime from-zero drills: 见 `log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md` Evidence（M2/M4 相关）。
- Terraform devtest DB skeleton drills: 见 `log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md` Evidence（M3 相关）。
- Backup / recovery drills: 见 `log-S5A-3B-backup-restore-sanitize-verify.md` Evidence（M5 相关）。
- Hard-gate / post-change verification 思维: 见 S3A/S6A 系列 logs。

## Recent Changes

- 2026-03-29: migrated `road-S1-1` to the branch-road bridge-ledger format and wrote explicit parent alignment back to `road-S1` instead of leaving those links inside prose-only descriptions.
- 2026-03-21: 从早期的 `road-001` 重构为 `road-S1-1`，明确其作为 road-S1 子路线的定位，保留原有 M1–M5 结构，并强调这是“政府岗最小闭环”的子集，而不是覆盖 ROADMAP v5 的全部内容。
- 2026-03-25: 明确当前记账边界：`road-S1-1` 以 `S4B` 为最小闭环主完成面，吸收 `S4A` 的方法论与 `S5A-3B` 的 recovery sample；`S4C/S4D` 继续归入 `road-S1` 主线承接。
- 2026-03-25: 同步 `S4B` 最新闭环状态：`S4B`、`S4B-1A`、`S4B-2A` 均已标记为 `stable`，因此 `road-S1-1` 当前引用的最小 runtime + Terraform baseline evidence 已形成稳定父子链路。
