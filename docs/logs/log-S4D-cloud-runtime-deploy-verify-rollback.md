# log-S4D (Cloud Runtime Deploy / Verify / Rollback)

---

**id**: `S4D`
**kind**: `log`
**title**: `cloud runtime deploy / verify / rollback (staging-like target, release operations, post-change verification) v1`
**status**: `stable`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, Deploy, Rollback, ReleaseOperations, Verification, epic/s4, epic/s4d`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: ``
  **previous_log**: `docs/logs/log-S4C-cloud-services-and-terraform-epic.md`
  **reference_log_1**: `docs/logs/log-S4B-infra-as-code-and-runtime-packaging.md`
  **reference_log_2**: `docs/logs/log-S4C-cloud-services-and-terraform-epic.md`
  **reference_log_3**: `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`
  **reference_log_4**: `docs/logs/log-S4A-5A-operational-visibility-and-post-change-verification.md`
  **phase_log_1**: `docs/logs/log-S4D-1A-cloud-runtime-release-path.md`
  **phase_log_2**: `docs/logs/log-S4D-2A-post-change-verification-and-operational-checks.md`
  **phase_log_3**: `docs/logs/log-S4D-3A-cloud-runtime-rollback-sample.md`
**created**: `2026-03-23`
**updated**: `2026-03-25`

---

## Decision / Outcome

**Decision**:

- 启动 `S4D` 作为 `S4 Ops Runtime` 下的新顶层 spine，专门承接 `deployable cloud runtime + release operations` 这条主线；
- `S4D` 的目标不是重复 `S4C` 的云基础与连通性说明，而是把应用 runtime 本身推进到一个 staging-like target，并建立 `deploy -> verify -> rollback` 的 operator path。

**Default choices (phase defaults / v1)**:

- 先选一条最小、可解释、可演示的 cloud/staging runtime 目标，不同时并行多个部署目标；
- 优先复用 `S4B` 的 runtime packaging 入口与 `S4C` 的 cloud-dev 基础设施，不再重造第二套 env/runtime contract；
- 部署验证优先采用 machine-verifiable smoke：health、关键 HTTP probe、日志摘要、必要时加最小 metrics/checklist；
- rollback 优先采用“回到上一个已知可用版本/配置”的简单策略，而不是一开始引入复杂蓝绿/金丝雀体系。

**Non-goals（不做什么）**:

- 不在 v1 内直接引入生产级多环境发布平台、复杂流水线编排或 Kubernetes；
- 不在 `S4D` 内重新定义云网络、RDS、对象存储 contract，这些继续由 `S4C` 承担；
- 不把 `S4D` 做成完整 CI/CD 平台 epic；它先聚焦 deployable runtime 与最小 release operations 样本。

## Background（背景）

- `S4B` 已证明：本地 dev/test runtime 可以从零拉起，并有 packaging、health、from-zero drills 与 runbook；
- `S4C` 已证明：Terraform-managed cloud infra 可以建立，且本机 runtime 能通过 `.env.cloud.dev` 连上 cloud-dev RDS 并完成最小 smoke；
- 当前主线缺口是：应用 runtime 还没有真正进入一个 cloud/staging target，也还没有形成一条面向发布与回退的 operator path；
- 因此 `S4D` 的存在意义，是把“本机连云 DB”推进成“云端可部署 runtime + deploy/verify/rollback 样本”。

## Constraints（约束）

- 先做单一路径样本，不追求覆盖 VM、container service、serverless 等多种目标；
- 配置与 secrets 继续通过 env/config 注入管理，不把敏感值写入仓库；
- 每次部署/回退 drill 需要留下可追溯 evidence（headSha、target、env 名、关键命令、结果摘要）；
- 优先低成本、可回收、可重复演练的 staging-like 目标，不追求长期常驻环境。

## Scope（本 log 范围）

- 本 log 负责：
  - 定义 cloud runtime deploy/verify/rollback 的目标边界、默认策略与 phase 拆分；
  - 明确 `S4D` 与 `S4B` / `S4C` 的责任边界；
  - 作为 `S4` 主线里“release operations / post-change verification”方向的顶层索引。
- 本 log 不负责：
  - 云网络/数据库/对象存储资源本身的 IaC 细节；
  - 复杂 CI/CD、审批流、蓝绿/金丝雀、多 region 部署架构。

## Success Criteria（DoD）

- 结构层面：
  - 读者能在 30 秒内理解：`S4D` 解决什么问题、与 `S4B/S4C` 的边界是什么、下一步先落哪个 target；
  - `docs/INDEX.md` 能导航到 `S4D` spine 与首个 phase log。
- 工程层面：
  - 至少确定 1 个最小 cloud/staging target；
  - 至少定义 1 条 deploy -> verify -> rollback 的最小 operator path；
  - 至少明确一组 post-change verification 入口（health / logs / key probe / checklist）。
- 证据层面：
  - 每个 phase 后续至少预留 1 条可追溯 evidence 入口（headSha + artifact path / terminal proof / CI run URL）。

## Phases（切片）

- `S4D-1A`（Phase 1）：Cloud runtime release path（deploy target, env contract, verify/rollback baseline）
  - 详见：`docs/logs/log-S4D-1A-cloud-runtime-release-path.md`
- `S4D-2A`（Phase 2）：Post-change verification & operational checks（health, logs, smoke, release checklist）
  - 详见：`docs/logs/log-S4D-2A-post-change-verification-and-operational-checks.md`
- `S4D-3A`（Phase 3）：Release drill evidence（repeatable deploy/rollback drills with artifacts）
  - 详见：`docs/logs/log-S4D-3A-cloud-runtime-rollback-sample.md`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：contract/indexing（定义 `S4D` 主轴、边界与 phase 拆分）
- [x] `P1`：Phase 1 seed（cloud runtime release path phase log scaffolded）
- [x] `P2`：最小 deploy target、env contract 与 target-host verify gate 固定
- [x] `P3`：首轮 deploy / verify / rollback drill 入账

## Current Status（进展摘要）

- `S4D` 刚完成顶层 spine 定义；
- `S4D-1A` 已完成第一步：v1 deploy target 固定为“单 Linux 主机 + backend API container + external cloud-dev RDS”；
- `S4D-1A` 已继续完成 env/release contract 与 verify checklist 固定；
- `S4D-1A` 已补上 target-host verify gate（`scripts/ops/cloud_release_verify.sh`）与 target-host deploy command path（`scripts/ops/cloud_release_run_container.sh`），因此 release-path contract 已具备进入真实样本的条件；
- 2026-03-24 起，真实 Ubuntu VM 上的 deploy -> verify 样本、operator checks、failure evidence 与由 drill 暴露出的脚本修复，统一转入 `S4D-2A` 记账；
- `S4D-2A` 已拿到第一轮真实 Ubuntu VM verify PASS：`container_running OK`、`migration_ok OK`、`health_ok OK (200)`、`read_smoke_ok OK (200 list payload)`、`env_guard_ok OK`；
- `S4D-3A` 已进入脚本与文档准备阶段：当前已开始为 known-good image/tag rollback 样本补齐 existing-image deploy path 与 rollback helper；
- 2026-03-25 已完成第一份 known-good image tag 留存，并跑了第一轮 rollback drill 尝试；
- 在补齐 verify readiness wait、恢复 VM 到 RDS `5432` 连通后，第一轮真实 rollback sample 已通过：candidate verify PASS，rollback verify PASS，`CLOUD_RELEASE_ROLLBACK_RESULT=PASS`；
- `S4D` 的最小目标已经完成：真实 Ubuntu VM 上的 deploy -> verify -> rollback operator path 已具备可追溯 evidence，因此本顶层 spine 现可标记为 `stable`；
- 更强的 failure-oriented rollback drills 不是当前 v1 stable 的前置条件；如果后续要系统化推进“坏 candidate / 明确 trigger / 更细 recovery evidence”，应新增 `S4D-4A`，而不是继续扩大 `S4D-3A` 的定义。

## Notes（落地原则）

- 先选最容易解释的 deploy target，再谈更复杂的 release engineering；
- 先把 deploy / verify / rollback 的 operator path 跑通，再扩展自动化与平台化；
- `S4D` 默认 scope branch 使用：`S4D-cloud-runtime-deploy-verify-rollback`。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - `S4D` 的边界、phase 拆分与最小 release operations contract 已稳定；
  - 至少 `S4D-1A` 已形成一条可追溯的 deploy/verify/rollback 样本路径与 evidence 入口。

## Numbering & Commit Naming（编号与提交命名）

- 编号约定：`P<n>` 表示 Phase，`C<n>` 表示 Cycle，`S<n>` 表示 Step。
- Commit / PR 命名：
  - 顶层 spine 自身的变更使用：`S4D-cloud-runtime-deploy-verify-rollback/P<phase>-C<cycle>-S<steps>: <summary>`；
  - phase-specific 变更使用对应 phase log 的前缀，例如：`S4D-1A/...`、`S4D-2A/...`；
  - `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。

**Branch 约定（建议）**:

- 与 `S4D` 相关的实现与文档优先落在 `S4D-cloud-runtime-deploy-verify-rollback` 分支；
- 若后续某个 release phase 体量明显扩大，可在 `S4D-*` 分支下开短生命周期子分支；默认仍不建议为每个 phase 单独切碎分支。

**Commit 纪律（建议）**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4D-cloud-runtime-deploy-verify-rollback`。

## Recent changes（for traceability，可选）

- 2026-03-23：首次创建 `S4D`，作为 `S4` 主线中承接 cloud runtime deploy/verify/rollback 的新顶层 spine。
- 2026-03-24：确认第一台 Ubuntu VM 已完成 host prep 与 repo sync，当前仅剩 env placement 与第一次真实 deploy/verify 样本。
- 2026-03-24：第一次真实 deploy 尝试发现 `cloud_release_run_container.sh` 的 `docker run` 参数拼接缺陷；当前已转入修复 wrapper 并重跑 deploy/verify。
- 2026-03-24：deploy wrapper 修复后，真实样本已推进到“容器启动成功”，当前新发现 verify 端口变量碰撞问题，需再修复一次 verify gate 才能完成首个 PASS 样本。
- 2026-03-24：新增 `S4D-2A`，把真实 Ubuntu VM post-change verification / operational checks 与对应提交命名从顶层 `S4D` 前缀收敛到 phase 前缀 `S4D-2A`。
- 2026-03-24：重新核对历史命名后，已把原先误挂在顶层 `S4D` 前缀下的 P1/P2 phase-specific 提交分别改写到 `S4D-1A` 与 `S4D-2A`。
- 2026-03-24：第一轮真实 Ubuntu VM verify 已通过，`S4D-2A` 的工作重点已从 verify 修复切换到 rollback 样本。
- 2026-03-24：新增 `S4D-3A`，并为 image-level rollback 样本准备 `--skip-build` 路径与 `cloud_release_rollback.sh` helper。
- 2026-03-25：第一轮 rollback drill 已证明 known-good tag 和 rollback helper 路径可执行，但也暴露 verify readiness wait 缺口，当前已转入修复该 gate 并重跑 rollback 样本。
- 2026-03-25：在 verify wait 修复和 RDS 连通恢复后，第一轮真实 rollback sample 已 PASS 收口，`S4D` 已具备 deploy -> verify -> rollback 的最小 operator path 样本。
- 2026-03-25：完成稳定性评估后，`S4D` 已按 v1 口径标记为 `stable`；更强失败样本被明确归为潜在后续 phase `S4D-4A`，不再作为当前收口前置条件。