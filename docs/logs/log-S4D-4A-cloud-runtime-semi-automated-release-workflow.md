# log-S4D-4A (Phase 4: Cloud Runtime Semi-Automated Release Workflow)

---

**id**: `S4D-4A`
**kind**: `log`
**title**: `cloud runtime semi-automated release workflow (single-entry operator command, evidence capture, failure-oriented gates) + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, ReleaseOperations, Automation, Verification, Rollback, FailureTaxonomy, Evidence, epic/s4, sub/4a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  **previous_log**: `docs/logs/log-S4D-3A-cloud-runtime-rollback-sample.md`
  **reference_log_1**: `docs/logs/log-S5B-security-governance-hard-gates.md`
  **reference_log_2**: `docs/logs/log-S6A-4A-hard-gate-evidence-json.md`
  **reference_log_3**: `docs/logs/_template-log-phase-drills-evidence.md`
**created**: `2026-03-25`
**updated**: `2026-03-25`

---

## Decision / Outcome

**Decision**:

- `S4D-4A` 承接 `S4D-3A` 已经闭环的最小 deploy -> verify -> rollback operator path，把重点从“人工 SSH + 手动多步操作”推进到“单入口、半自动、可留痕”的 cloud runtime release workflow；
- v1 的目标不是直接上完整 CI/CD、GitOps 或 Kubernetes，而是先把当前已经存在的 deploy / verify / rollback helper 继续收敛成受控 operator workflow：一次触发、固定证据、明确 gate、可追溯失败分类。

**Default choices (phase defaults / v1)**:

- 半自动的最小单位默认仍是“单 operator 入口 + 单 Ubuntu VM + 单 backend container + 单 cloud-dev env file”，不同时扩到多主机、多环境并发发布；
- 自动化默认先收口为脚本 / workflow 级别，而不是一开始引入完整平台化编排；
- deploy / verify / rollback 的成功与失败，继续沿用 `S4D-2A` / `S4D-3A` 已固定的 gate 语义，而不是重造另一套判断标准；
- 每次运行都必须留下最小 evidence bundle，至少能追溯到 `headSha`、image tag、target host、阶段结果与 failure class；
- v1 允许 operator 在关键点做人工确认，但不再要求手动 SSH 后逐条敲散落命令。

## Definitions (optional)

- **Semi-automated release workflow**：从 operator 机器触发、自动完成远端 deploy / verify / rollback 子步骤，但仍保留人工观察和确认能力的受控发布路径。
- **Single-entry operator command**：一条明确入口的命令或脚本，内部编排多个已有 helper，而不是让 operator 自己拼装顺序。
- **Evidence bundle**：一次 release workflow 运行留下的结果摘要，至少包含输入参数、关键子步骤结果、PASS/FAIL 和 trace 字段。
- **Failure class**：对失败原因的低基数分类，例如 `ssh_connectivity`, `image_missing`, `container_startup`, `dependency_connectivity`, `verify_gate`, `rollback_recovery`。

## Constraints

- 不把真实 secrets、SSH 私钥或 env 文件内容提交到仓库；
- v1 不要求发布平台、审批系统或自动 secrets 分发；
- failure taxonomy 必须低基数、可聚合、可直接用于 operator 判断，而不是输出一次一个新 reason；
- 自动化路径必须复用已经存在的 deploy / verify / rollback helper，避免再造平行入口；
- 云上样本仍保持 `cloud-dev` 单 VM 路径，避免在此 phase 同时引入 ECS、Kubernetes 或多 host orchestration。

## Scope

- `P0`: contract（半自动 release path、failure taxonomy、evidence contract）
- `P1`: implementation / workflow（single-entry operator command、evidence output、remote orchestration）
- `P2`: drill / verify（第一次真实半自动 deploy -> verify 样本）
- `P3`: drill / rollback/failure handling（半自动 rollback / fail-path 样本与 operator wording）

## Success Criteria (DoD)

- 仓库内存在一条单入口的 cloud runtime release workflow，operator 不再需要手动 SSH 后逐条执行散落命令；
- workflow 至少能固定收口 deploy、verify，必要时继续收口 rollback；
- 每次运行都能生成可追溯 evidence，至少记录 `headSha`、target host、image tag、verify result、rollback result（如发生）与 failure class；
- failure taxonomy 至少覆盖当前已知高频失败面：SSH/host reachability、image/build、container startup、DB/dependency connectivity、verify gate、rollback recovery；
- 至少一轮真实 Ubuntu VM 半自动样本被记录进 Evidence，证明 operator path 不再依赖纯手工步骤。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的半自动 release contract、single-entry workflow、failure taxonomy 与 operator wording 已稳定；
  - 至少一轮真实 Ubuntu VM 半自动 deploy / verify / rollback 样本以可追溯 evidence 收口。

## P0 (Contract | v1)

### P0-C1-S1 (Semi-automated release path contract | v1)

- operator 入口默认从本地工作机发起，而不是先手动 SSH 再逐步执行；
- release path 至少应能表达以下步骤的固定顺序：
  - prepare / preflight
  - deploy
  - verify
  - optional rollback
- 单入口脚本只负责编排，不在 v1 中取代已有 helper 的核心语义。

### P0-C1-S2 (Failure taxonomy and gate contract | v1)

- 本 phase 默认 failure class 至少包括：
  - `preflight_contract`
  - `ssh_connectivity`
  - `image_build_or_lookup`
  - `container_startup`
  - `dependency_connectivity`
  - `verify_gate`
  - `rollback_recovery`
- 每个 failure class 都应能映射到一个明确的 operator next action，例如重试、停止推进、触发 rollback、转人工排查。

### P0-C1-S3 (Evidence contract | v1)

- 本 phase 的 evidence 至少应记录：
  - `headSha`
  - `workflow_command_summary`
  - `target_host_kind`
  - `env_file_path`
  - `image_tag`
  - `known_good_image_tag`（如适用）
  - `deploy_result`
  - `verify_result`
  - `rollback_result`（如适用）
  - `failure_class`（如 FAIL）
  - `artifacts`
  - `result`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4D-4A/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`）或同一 phase / cycle 下连续 steps 的组合（如 `1S2`）。

**Branch convention**:

- `S4D-4A` 相关实现与文档优先落在 `S4D-cloud-runtime-deploy-verify-rollback` 分支。

**Commit discipline (recommended)**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4D-cloud-runtime-deploy-verify-rollback`。

## Plan (draft)

### P1 (Implementation / workflow)

- P1-C1-S1: 新增 single-entry cloud release workflow 入口，收口远端 deploy + verify 顺序
- P1-C1-S2: 为 workflow 固定 evidence 输出与 failure class 摘要

### P2 (Drill / Verify)

- P2-C1-S1: 在 Ubuntu VM 上执行第一轮半自动 deploy -> verify 样本
- P2-C1-S2: 记录首轮 FAIL / PASS 与对应 failure class

### P3 (Rollback / operator wording)

- P3-C1-S1: 在 workflow 内收口 rollback trigger 与 rollback-after-fail path
- P3-C1-S2: 固化 operator-facing 说明，明确何时重试、何时停止、何时回滚

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: semi-automated release path contract fixed
- [x] `P0-C1-S2`: failure taxonomy and gate contract fixed
- [x] `P0-C1-S3`: evidence contract fixed

### P1 (Implementation / workflow)

- [x] `P1-C1-S1`: single-entry cloud release workflow prepared
- [x] `P1-C1-S2`: workflow evidence output and failure summary prepared

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: first semi-automated Ubuntu VM deploy -> verify sample recorded
- [ ] `P2-C1-S2`: first semi-automated FAIL / PASS cycle recorded with failure class

### P3 (Rollback / operator wording)

- [ ] `P3-C1-S1`: rollback trigger and rollback-after-fail path closed inside workflow
- [ ] `P3-C1-S2`: operator wording for retry / stop / rollback fixed

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, workflow entrypoint, target host, failure class, and drill outcomes.

### P0-C1-S1 (Phase scaffold and contract fixed | 2026-03-25)

- headSha: `89797cdf`
- artifacts:
  - `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
- expected:
  - 为 `S4D` 新增一条从手动 operator path 走向半自动 release workflow 的 phase，明确边界、默认选择、failure taxonomy 与 evidence contract。
- observed:
  - `S4D-4A` 已按 template 收口为独立 phase；当前下一步可直接落到 single-entry workflow implementation，而不必再重新讨论为什么要减少手工 SSH 操作。

### P1-C1-S1S2 (Single-entry workflow and evidence output prepared | 2026-03-25)

- headSha: `501fd981`
- artifacts:
  - `scripts/ops/cloud_release_workflow.sh`
  - `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
- expected:
  - 新增一条从本地工作机触发的单入口 workflow，自动完成远端 preflight、deploy、verify，并在需要时为 rollback 留出同一入口；
  - workflow 在本地生成固定 evidence bundle，收口关键结果字段与 low-cardinality failure class。
- observed:
  - 已新增 `cloud_release_workflow.sh`，支持通过 SSH 从本地工作机触发远端 `cloud_release_run_container.sh`、`cloud_release_verify.sh`，并可选在 verify FAIL 后继续调用 `cloud_release_rollback.sh`；
  - workflow 会在 `artifacts/_tmp_s4d4a_cloud_release_workflow/<timestamp>/` 下输出 `preflight.log`、`deploy.log`、`verify.log`、`rollback.log`、`summary.json`，固定记录 `headSha`、target host、image tag、阶段结果与 `failureClass`；
  - 当前 operator 已不再需要手动 SSH 后逐条执行散落命令，`S4D-4A/P1-C1-S1S2` 已具备进入真实半自动 drill 的条件。

### P2-C1-S1 (First local-triggered workflow attempt exposed result-accounting bug | 2026-03-25)

- headSha: `b3002d07`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T085728Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T085728Z/preflight.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T085728Z/deploy.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T085728Z/verify.log`
- expected:
  - 从 Windows/WSL 本地工作机通过 `cloud_release_workflow.sh` 远程触发 Ubuntu VM 上的 preflight / deploy / verify，并以 PASS/FAIL 与 `failureClass` 如实收口。
- observed:
  - 本轮样本的 artifact 真实落在本地仓库，说明“本地工作机触发 workflow 并生成 evidence bundle”这一层是成立的；
  - 但同一轮 artifact 出现了自相矛盾：`summary.json` 记录 `result=PASS`、`preflightResult=PASS`、`deployResult=PASS`、`verifyResult=PASS`，而对应 `preflight.log` / `deploy.log` / `verify.log` 均为 `ssh: connect to host 127.0.0.1 port 22022: Connection refused`；
  - 根因不是 operator 操作顺序，而是 `cloud_release_workflow.sh` 的 `run_remote_step()` 使用了没有 `else` 的 `if ssh ...; then ... fi; return $?`，导致 `ssh` 失败时函数仍返回成功，错误地把 FAIL 样本写成 PASS。
- failure_class:
  - `ssh_connectivity`（artifact surface）
  - `workflow_result_accounting_bug`（actual root cause）
- result:
  - `FAIL -> fix workflow result accounting before rerun`

## Recent changes (for traceability, optional)

- 2026-03-25: 创建 `S4D-4A`，把 `S4D` 的下一步工作重点明确收敛到“半自动 release workflow + failure taxonomy + evidence capture”，而不是继续停留在人工 SSH 操作层。
- 2026-03-25: 已新增 `scripts/ops/cloud_release_workflow.sh`，把远端 preflight / deploy / verify / optional rollback 收口为单入口 workflow，并固定输出 evidence bundle 与 failure class 摘要。
- 2026-03-25: 第一次本地触发 workflow 样本暴露出结果记账 bug：`ssh` 失败时 `run_remote_step()` 仍返回成功，导致 `summary.json` 错写 PASS；当前已转入修复并准备重跑。