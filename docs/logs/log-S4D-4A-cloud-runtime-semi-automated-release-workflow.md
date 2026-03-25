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
- P3-C2-S1: 设计一轮最小定向 rollback drill，故意触发 candidate verify FAIL，但不破坏 known-good rollback 路径
- P3-C2-S2: 带 `--known-good-image-tag` 与 `--rollback-on-verify-fail` 执行 workflow，验证 `PASS_AFTER_ROLLBACK`
- P3-C2-S3: 记录定向 rollback drill 的 artifact、`operator_guidance.txt` 与最终分支结果；`manual_recovery_required` 另作为后续更强 failure drill

### P3-C2 (Targeted rollback drill recipe | prepared)

- 目标：先验证 `verify FAIL -> auto rollback -> PASS_AFTER_ROLLBACK` 这条 workflow 分支，且不要求先制造一个会把 rollback 一起打坏的真实坏镜像；
- 最小做法：保持 candidate image 与 host port 都正常，只在 workflow verify 阶段故意传入错误的 `--api-port`，例如 `39999`；这样 candidate verify 会因 probe 命中错误端口而 FAIL，而 rollback helper 在当前实现里仍会按 `--host-port 30021` 回到 known-good 并执行 rollback verify；
- 这条 drill 验证的是 `S4D-4A/P3` 刚收口的 trigger/operator wording/summary branch，而不是应用本身的真实坏版本；如果要补“真实坏 candidate”证据，应另起后续 cycle。

建议执行命令（Windows PowerShell，本地工作机触发）：

```powershell
bash scripts/ops/cloud_release_workflow.sh \
  --ssh-host 127.0.0.1 \
  --ssh-port 22022 \
  --ssh-user ubuntu \
  --ssh-identity-file /c/Users/H/.ssh/wordloom_cloud_dev \
  --remote-repo-dir /home/wordloom/work/wordloom-v3 \
  --env-file /etc/wordloom/.env.cloud.dev \
  --image-tag wordloom-backend:cloud-dev \
  --known-good-image-tag wordloom-backend:cloud-dev-known-good-20260325-pass \
  --container-name wordloom-api-cloud-dev \
  --host-port 30021 \
  --api-port 39999 \
  --rollback-on-verify-fail
```

预期：

- `summary.json` 预期记录 `verifyResult=FAIL`、`rollbackResult=PASS`、`result=PASS_AFTER_ROLLBACK`、`failureClass=rollback_recovery`；
- `operator_guidance.txt` 预期记录 `operatorAction=candidate_reverted_to_known_good`；
- artifact 目录预期新增 `preflight.log`、`deploy.log`、`verify.log`、`rollback.log`、`summary.json`、`operator_guidance.txt`。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: semi-automated release path contract fixed
- [x] `P0-C1-S2`: failure taxonomy and gate contract fixed
- [x] `P0-C1-S3`: evidence contract fixed

### P1 (Implementation / workflow)

- [x] `P1-C1-S1`: single-entry cloud release workflow prepared
- [x] `P1-C1-S2`: workflow evidence output and failure summary prepared

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: first semi-automated Ubuntu VM deploy -> verify sample recorded
- [x] `P2-C1-S2`: first semi-automated FAIL / PASS cycle recorded with failure class

### P3 (Rollback / operator wording)

- [x] `P3-C1-S1`: rollback trigger and rollback-after-fail path closed inside workflow
- [x] `P3-C1-S2`: operator wording for retry / stop / rollback fixed
- [ ] `P3-C2-S1`: targeted rollback drill recipe fixed for a safe `verify FAIL -> PASS_AFTER_ROLLBACK` branch
- [ ] `P3-C2-S2`: first targeted `PASS_AFTER_ROLLBACK` workflow sample recorded
- [ ] `P3-C2-S3`: targeted drill evidence recorded with `summary.json` and `operator_guidance.txt`

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

### P2-C1-S2 (First truthful local-triggered FAIL sample | 2026-03-25)

- headSha: `9ca59e21`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T090254Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T090254Z/preflight.log`
- expected:
  - 在修复 workflow result accounting 之后，重新从 Windows/WSL 本地工作机触发 Ubuntu VM 远端 preflight / deploy / verify，并得到一条与 artifact 一致的 PASS/FAIL 结果。
- observed:
  - 本轮 `summary.json` 与 `preflight.log` 已经一致：`preflightResult=FAIL`、`failureClass=ssh_connectivity`、`result=FAIL`；
  - `deployResult` / `verifyResult` 均保持 `NOT_RUN`，说明 workflow 已在 preflight 阶段如实停止，没有再错误地把失败样本推进成 PASS；
  - 当前暴露出的真实问题不再是 workflow 自身结果记账，而是“从当前 WSL 工作机访问 `127.0.0.1:22022` 时 SSH 不通”，也就是本地 operator host 到 Ubuntu VM 的连接路径仍未闭环。
- failure_class:
  - `ssh_connectivity`
- result:
  - `FAIL -> diagnose WSL-to-VM SSH path before rerun`

### P2-C1-S3 (First authenticated local-triggered FAIL sample reached runtime dependency layer | 2026-03-25)

- headSha: `b088e4c5`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T092531Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T092531Z/preflight.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T092531Z/deploy.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T092531Z/verify.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T092531Z/rollback.log`
- expected:
  - 在补齐非交互 SSH 认证后，从 Windows PowerShell 本地工作机触发 Ubuntu VM 远端 preflight / deploy / verify / optional rollback，并尽量把失败面推进到真实运行时层。
- observed:
  - 本轮 `preflightResult=PASS`、`deployResult=PASS`，说明本地 PowerShell -> Ubuntu VM 的 SSH 路径与非交互认证已经闭环；
  - `verifyResult=FAIL`、`rollbackResult=FAIL`，且 `verify.log` / `rollback.log` 均显示容器在 migration 阶段因 `psycopg.OperationalError` 退出，错误为 `connection to server at "13.211.43.32", port 5432 failed: server closed the connection unexpectedly`；
  - 这说明当前 workflow 已经能把失败面推进到真实运行时依赖层，剩余阻塞不再是 operator workflow，而是 Ubuntu VM 到 cloud-dev RDS 的数据库连通性/可用性问题；
  - 与 `S4D-3A` 期间曾出现过的 RDS 连通波动一致，本轮失败样本也证明 rollback 在依赖层失败时不会制造假 PASS，而会如实收口为 FAIL。
- failure_class:
  - `dependency_connectivity`
- result:
  - `FAIL -> validate VM-to-RDS 5432 connectivity and rerun`

### P2-C1-S4 (First local-triggered semi-automated PASS sample | 2026-03-25)

- headSha: `8caafc4f`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T093943Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T093943Z/preflight.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T093943Z/deploy.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T093943Z/verify.log`
- expected:
  - 在补齐 PowerShell 非交互 SSH 认证并修正 RDS inbound rule 后，从 Windows PowerShell 本地工作机触发 Ubuntu VM 远端 preflight / deploy / verify / optional rollback，并取得第一条与 artifact 一致的 PASS 样本。
- observed:
  - 本轮 `preflightResult=PASS`、`deployResult=PASS`、`verifyResult=PASS`、`rollbackResult=SKIPPED`、`result=PASS`，且 `failureClass=none`；
  - `verify.log` 显示五项 gate 全部通过：`container_running OK`、`migration_ok OK`、`health_ok OK (200)`、`read_smoke_ok OK (200 list payload)`、`env_guard_ok OK`；
  - 与上一轮 `dependency_connectivity` 样本对照可知，本轮 PASS 的直接恢复动作是补入当前公网 IP 对应的 RDS inbound allow rule；这说明 workflow 已经能把问题如实暴露、修复后再验证 PASS；
  - 至此 `S4D-4A/P2` 已完成首个真实“本地工作机 -> SSH -> Ubuntu VM -> deploy/verify”半自动 PASS 样本，当前下一步可转入 `P3` 的 rollback trigger / operator wording 收口。
- failure_class:
  - `none`
- result:
  - `PASS`

### P3-C1-S1S2 (Rollback trigger and operator wording fixed inside workflow | 2026-03-25)

- headSha: `96188b45`
- artifacts:
  - `scripts/ops/cloud_release_workflow.sh`
  - `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
- expected:
  - 把 `S4D-4A/P3` 从“verify 失败时可以可选回滚”推进到“workflow 内明确何时允许自动 rollback、何时必须停住、operator 下一步应该看哪份 artifact、应该执行什么动作”。
- observed:
  - `cloud_release_workflow.sh` 现在把 rollback trigger 固定为可追溯合同：默认 `manual_only`，只有在同时提供 `--rollback-on-verify-fail` 与 `--known-good-image-tag` 时才进入 `verify_fail_auto`；缺少 known-good tag 时会直接拒绝启动，而不是在 verify FAIL 后给出模糊行为；
  - workflow 现在会额外生成 `operator_guidance.txt`，并在 `summary.json` 中固定记录 `rollbackTrigger`、`operatorAction`、`terminalStage` 与 guidance artifact path，使 operator 能区分 `stop_and_fix_preflight`、`stop_and_fix_deploy`、`decide_manual_rollback_or_fix_forward`、`candidate_reverted_to_known_good`、`manual_recovery_required` 等后续动作；
  - verify FAIL 但未 arm rollback 时，workflow 会明确要求先停住、读 `verify.log`、再决定 fix-forward 还是带 known-good tag 重跑；verify FAIL 且 rollback PASS 时会以 `PASS_AFTER_ROLLBACK` + `rollback_recovery` 收口；rollback FAIL 时会明确收口到 `manual_recovery_required`，不再留下“到底该重试还是人工恢复”的空白地带；
  - 本次 `P3` 收口的是 workflow 语义与 operator wording，不是新增一轮远端 bad-candidate drill；如果后续要补更强证据，应专门执行一次“verify FAIL -> rollback trigger -> PASS_AFTER_ROLLBACK/FAIL”定向样本。
- result:
  - `PASS`

## Recent changes (for traceability, optional)

- 2026-03-25: 创建 `S4D-4A`，把 `S4D` 的下一步工作重点明确收敛到“半自动 release workflow + failure taxonomy + evidence capture”，而不是继续停留在人工 SSH 操作层。
- 2026-03-25: 已新增 `scripts/ops/cloud_release_workflow.sh`，把远端 preflight / deploy / verify / optional rollback 收口为单入口 workflow，并固定输出 evidence bundle 与 failure class 摘要。
- 2026-03-25: 第一次本地触发 workflow 样本暴露出结果记账 bug：`ssh` 失败时 `run_remote_step()` 仍返回成功，导致 `summary.json` 错写 PASS；当前已转入修复并准备重跑。
- 2026-03-25: 修复 workflow result accounting 后，第一轮真实本地触发样本已如实记录为 `FAIL (ssh_connectivity)`；当前下一步不再是修脚本，而是诊断 WSL 工作机到 Ubuntu VM 的 SSH 路径。
- 2026-03-25: 在补齐 PowerShell 非交互 SSH 认证后，第一轮 authenticated local-triggered 样本已把失败面推进到 `dependency_connectivity`：当前阻塞位于 Ubuntu VM 到 RDS `5432` 的真实数据库连通层。
- 2026-03-25: 在为当前公网 IP 补齐 RDS inbound allow rule 后，第一轮 local-triggered semi-automated workflow 已取得 PASS；`S4D-4A/P2` 现已具备真实本地触发 deploy/verify evidence。
- 2026-03-25: `S4D-4A/P3` 已把 rollback trigger 与 operator wording 收口进 workflow：`summary.json` 现可固定记录 `rollbackTrigger/operatorAction/terminalStage`，并新增 `operator_guidance.txt` 作为失败后的下一步动作说明。
- 2026-03-25: `P3-C2` 已准备最小定向 rollback drill recipe：优先用 verify probe port mismatch 触发 `verify FAIL -> PASS_AFTER_ROLLBACK`，先验证 branch 语义与 operator guidance，再决定是否继续补真实坏 candidate 样本。