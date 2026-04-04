# log-S4D-4A (Phase 4: Cloud Runtime Semi-Automated Release Workflow)

---

**id**: `S4D-4A`
**kind**: `log`
**title**: `cloud runtime semi-automated release workflow (single-entry operator command, evidence capture, failure-oriented gates) + drills/evidence v1`
**status**: `stable`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, ReleaseOperations, Automation, Verification, Rollback, FailureTaxonomy, Evidence, epic/s4, sub/4a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
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
- P3-C3-S1: 固定 release preflight gate families，把 `identity/auth`、`target reachability`、`dependency connectivity`、`release contract`、`post-change verify`、`rollback readiness` 明确映射到 low-cardinality failure classes
- P3-C3-S2: 扩展 `summary.json` / `operator_guidance.txt` contract，使其能稳定记录 gate-level results、terminal gate、operator next action 与 evidence completeness，而不是只给出总结果
- P3-C3-S3: 补一轮或多轮“定向 gate fail -> 明确 failure class -> 停止推进/回滚/人工恢复”样本，优先选择安全且可重复的 preflight/contract 级失败，而不是先依赖真实坏 candidate
- P3-C4-S1: 把 preflight family 的 `operator_guidance.txt` 从共享 `stop_and_fix_preflight` 文案细分为 `identity_auth_failure`、`target_reachability_failure`、`contract_validation_failure` 三类专属 guidance
- P3-C4-S2: 复跑最小 preflight taxonomy 样本，验证 guidance 已与对应 `terminalGate` / `failureClass` 对齐，而不再依赖宽泛的通用提示
- P3-C5-S1: 设计并记录第一条 `dependency_connectivity_gate` targeted FAIL 样本，优先采用“独立 container + 独立 host port + 临时坏依赖 env”的隔离做法，不干扰当前正常 service
- P3-C5-S2: 在依赖层 targeted taxonomy 的基础上，再补 `post_change_verify_gate` targeted FAIL 样本，区分“依赖不通”与“依赖正常但 verify 失败”
- P3-C5-S3: 在 runtime 层边界更清楚后，再补 `deploy_execution_gate` targeted FAIL 样本，避免把 build/run/startup 噪声过早和 dependency / verify 混在一起
- P3-C6-S1: 把 runtime family 的 `operator_guidance.txt` 从共享 runtime 文案细分为 `dependency_connectivity_failure`、`verify_failure`、`deploy_execution_failure` 三类专属 guidance
- P3-C6-S2: 复跑最小 runtime taxonomy 样本，验证 guidance 已与 `dependency_connectivity_gate`、`post_change_verify_gate`、`deploy_execution_gate` 及各自 `failureClass` 对齐
- P3-C7-S1: 把 rollback family 的 `operator_guidance.txt` 从宽泛的 rollback 说明细分为 `rollback_recovery` 与 `rollback_failure` 两类更可执行的 guidance
- P3-C7-S2: 复跑最小 rollback sample set，验证 guidance 已与 `rollback_readiness_gate`、`candidate_reverted_to_known_good`、`manual_recovery_required` 及对应 artifact 对齐
- P3-C8-S1: 固定 `evidence_capture_failure` contract，并在 workflow 中加入低扰动、可控的 evidence fault injection 入口，使 evidence 不完整时能稳定收口到 `terminalGate=evidence_capture`
- P3-C8-S2: 基于新的 fault injection 入口，补第一条 `evidence_capture_failure` targeted FAIL 样本，验证 `summary.json` 会保留运行结果但把最终分支提升为 evidence failure
- P3-C8-S3: 在 rollback branch 上复用 evidence fault injection，验证真实 `PASS_AFTER_ROLLBACK` 也会在 evidence 缺失时被提升为 `evidence_capture_failure`，而不是停留在 rollback-family result

### P3-C2 (Targeted rollback drill recipe | prepared)

- 目标：先验证 `verify FAIL -> auto rollback -> PASS_AFTER_ROLLBACK` 这条 workflow 分支，且不要求先制造一个会把 rollback 一起打坏的真实坏镜像；
- 最小做法：保持 candidate image 与 host port 都正常，只在 workflow verify 阶段故意传入错误的 `--api-port`，例如 `39999`；这样 candidate verify 会因 probe 命中错误端口而 FAIL，而 rollback helper 在当前实现里仍会按 `--host-port 30021` 回到 known-good 并执行 rollback verify；
- 这条 drill 验证的是 `S4D-4A/P3` 刚收口的 trigger/operator wording/summary branch，而不是应用本身的真实坏版本；如果要补“真实坏 candidate”证据，应另起后续 cycle。

建议执行命令（Windows PowerShell，本地工作机触发）：

```powershell
bash scripts/ops/cloud_release_workflow.sh \
  --ssh-host 127.0.0.1 \
  --ssh-port 22022 \
  --ssh-user wordloom \
  --ssh-identity-file /c/Users/H/.ssh/id_ed25519 \
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

### P3-C3 (Gate hardening / taxonomy refinement | planned)

- 目标：把 `S4D-4A` 里已经真实暴露过的 operator 失败面，从“单轮样本里的现象”提升为稳定 gate contract；这样后续再出现 `ssh user mismatch`、`identity file invalid`、`env contract missing`、`RDS unreachable`、`verify probe mismatch` 时，workflow 不需要靠人工阅读长日志才能先分辨失败落在哪一层。
- 这一轮是 `stable v1` 之后的加固 cycle，不推翻当前 `S4D-4A` 已达成的 v1 结论；它的作用是把已有 PASS / FAIL / PASS_AFTER_ROLLBACK 经验压缩成更稳定的 release interface。
- 默认 gate families：
  - `identity_auth_gate`：SSH user、identity file、非交互认证、host trust
  - `target_reachability_gate`：SSH connectivity、远端 shell、docker/runtime prerequisites
  - `dependency_connectivity_gate`：RDS / registry / object storage 等依赖面连通性
  - `release_contract_gate`：image tag、env file、required vars、known-good rollback inputs
  - `deploy_execution_gate`：image build/run、container start、host-port bind 与 deploy wrapper 执行结果
  - `post_change_verify_gate`：container running、migration、health、read smoke（必要时 write smoke）
  - `rollback_readiness_gate`：rollback helper、known-good tag、rollback verify entrypoint
- 默认 low-cardinality failure classes：
  - `identity_auth_failure`
  - `target_reachability_failure`
  - `dependency_connectivity_failure`
  - `contract_validation_failure`
  - `deploy_execution_failure`
  - `verify_failure`
  - `rollback_failure`
  - `evidence_capture_failure`
- 本 cycle 的最小 DoD：
  - workflow 文档中明确 gate family -> failure class -> operator next action 的映射；
  - `summary.json` 至少能固定记录 `gateResults`、`terminalGate`、`failureClass`、`operatorAction`、`evidenceComplete`；
  - 至少一轮安全、可重复的 gate-fail 样本被记账，用来证明 workflow 会在正确 gate 停止，而不是把 preflight/contract 失败推进成 deploy/verify 噪声。

**Current status (P3-C3)**

- `P3-C3-S1` 已完成第一版 gate family mapping：`cloud_release_workflow.sh` 现在把 preflight / deploy / verify / rollback 的结果正式映射到 `identity_auth_gate`、`target_reachability_gate`、`dependency_connectivity_gate`、`release_contract_gate`、`deploy_execution_gate`、`post_change_verify_gate`、`rollback_readiness_gate`。
- `P3-C3-S2` 已完成第一版 gate-level summary contract：`summary.json` 现可记录 `terminalGate`、`gateResults` 与 `evidenceComplete`，不再只给出 stage-level PASS/FAIL。
- `P3-C3-S3` 已完成两条最干净的 preflight-level targeted gate-fail 样本：
  - 一条 `identity_auth_gate` FAIL（无效 `--ssh-identity-file`）；
  - 一条 `release_contract_gate` FAIL（不存在的 `--env-file`）；
- `P3-C3-S3` 现已补齐第三条 `target_reachability_gate` FAIL（故意使用不通的 SSH 端口）；
  至此，preflight taxonomy 的三条最小 targeted evidence 已成组：
  - `identity_auth_gate`
  - `target_reachability_gate`
  - `release_contract_gate`
  这三条样本都在 preflight 阶段停止，并把 `terminalGate`、`failureClass` 与后续 gates `NOT_RUN` / `PASS` 的边界如实写入 artifact。

### P3-C4 (Preflight operator guidance refinement | planned)

- 目标：在 `P3-C3` 已把 preflight taxonomy 打成标准件之后，把 `operator_guidance.txt` 也按 preflight family 进一步拆细，避免 `identity_auth_failure`、`target_reachability_failure`、`contract_validation_failure` 仍共用过于宽泛的 `stop_and_fix_preflight` 说明。
- 这一轮的重点不再是补 taxonomy，而是让 operator 下一步动作与排查顺序更贴近失败层级：
  - `identity_auth_failure`：优先检查 user / key / file permission / host trust；
  - `target_reachability_failure`：优先检查 port forwarding / listener / network path / DNS；
  - `contract_validation_failure`：优先检查 `remote_repo_dir`、`env_file`、required inputs。
- 本 cycle 的最小 DoD：
  - `operator_guidance.txt` 对上述三类 preflight failure 给出不同的 next action 与 guidance；
  - 至少一组最小 preflight taxonomy 样本完成复跑，证明 guidance 已与 `terminalGate` / `failureClass` 对齐；
  - 记账边界保持清晰：`P3-C3` 负责 gate taxonomy，`P3-C4` 负责 operator guidance refinement。

**Current status (P3-C4)**

- `P3-C4-S1` 已完成：`cloud_release_workflow.sh` 现在会为 `identity_auth_failure`、`target_reachability_failure`、`contract_validation_failure` 输出不同的 `next_action` 与 `guidance_*`。
- `P3-C4-S2` 已完成第一轮最小样本复跑：三条 preflight taxonomy 样本均已复跑并验证 `operator_guidance.txt` 与 `terminalGate` / `failureClass` 对齐，不再共用含糊的 preflight guidance。

### P3-C5 (Dependency/runtime targeted taxonomy | started)

- 目标：在 preflight taxonomy 与 preflight-family guidance 已稳定之后，开始把 targeted taxonomy 推进到 dependency / runtime 层，但仍保持“先 isolated，再逐步加复杂度”的策略。
- 当前优先顺序：
  - 先拿 `dependency_connectivity_gate` 的隔离样本；
  - 再补 `post_change_verify_gate`；
  - 最后再补 `deploy_execution_gate`。
- 本 cycle 的最小 DoD：
  - 至少一条 `dependency_connectivity_gate` targeted FAIL 样本被正式记账，且证据显示 `preflight=PASS`、`deploy=PASS`、`verify=FAIL`，说明失败面已经推进到依赖层而不是停留在 preflight；
  - 这条样本优先使用独立 container、独立 host port 与临时坏依赖 env，避免干扰当前正常 service。

**Current status (P3-C5)**

- `P3-C5-S1` 已完成第一条 `dependency_connectivity_gate` targeted FAIL 样本：当前使用远端临时坏 DB 端口 env（`DATABASE_URL` 端口改为 `65432`）+ 独立 container / port，workflow 已稳定收口到 `terminalGate=dependency_connectivity_gate`、`failureClass=dependency_connectivity_failure`。
- `P3-C5-S2` 已完成第一条 `post_change_verify_gate` targeted FAIL 样本：当前使用正常 cloud-dev env + 独立 container / port，但故意把 verify probe 指向错误端口，workflow 已稳定收口到 `terminalGate=post_change_verify_gate`、`failureClass=verify_failure`，同时把 `dependencyConnectivityGate=PASS` 与 `postChangeVerifyGate=FAIL` 明确分开。
- `P3-C5-S3` 已完成第一条 `deploy_execution_gate` targeted FAIL 样本：当前先在远端占住独立 host port，再让 workflow 用同一端口起 isolated candidate，workflow 已稳定收口到 `terminalGate=deploy_execution_gate`、`failureClass=deploy_execution_failure`，且 `verifyResult=NOT_RUN`。

### P3-C6 (Runtime-family operator guidance refinement | started)

- 目标：在 `P3-C5` 已把 runtime taxonomy 打成标准件之后，把 `operator_guidance.txt` 也按 runtime family 进一步拆细，避免 `dependency_connectivity_failure`、`verify_failure`、`deploy_execution_failure` 仍共用过于宽泛的 runtime guidance。
- 这一轮的重点不再是补 taxonomy，而是让 runtime 失败后的第一排查动作更贴近失败层级：
  - `dependency_connectivity_failure`：优先检查 DB / registry / DNS / 上游依赖 reachability、credential 与 env-target correctness；
  - `verify_failure`：优先检查 probe target、port selection、routing、health/read smoke expectation 与应用级 verify 边界；
  - `deploy_execution_failure`：优先检查 image build、docker run、host-port bind、container name/runtime prerequisite 冲突。
- 本 cycle 的最小 DoD：
  - `operator_guidance.txt` 对上述三类 runtime failure 给出不同的 next action 与 guidance；
  - 至少一组最小 runtime taxonomy 样本完成复跑，证明 guidance 已与对应 `terminalGate` / `failureClass` 对齐；
  - 记账边界保持清晰：`P3-C5` 负责 runtime taxonomy，`P3-C6` 负责 runtime-family operator guidance refinement。

**Current status (P3-C6)**

- `P3-C6-S1` 已完成：`cloud_release_workflow.sh` 现在会为 `dependency_connectivity_failure`、`verify_failure`、`deploy_execution_failure` 输出不同的 `next_action` 与 `guidance_*`。
- `P3-C6-S2` 已完成第一轮最小样本复跑：三条 runtime taxonomy 样本均已复跑并验证 `operator_guidance.txt` 与 `terminalGate` / `failureClass` 对齐，不再共用含糊的 runtime guidance。

### P3-C7 (Rollback-family operator guidance refinement | started)

- 目标：在 `P3-C2` 已拿到 rollback branch evidence、`P3-C3` 已固定 rollback gate contract 之后，把 rollback family 的 `operator_guidance.txt` 也进一步拆细，避免 `rollback_recovery` 与 `rollback_failure` 仍停留在过于宽泛的 rollback 文案上。
- 这一轮的重点不再是补 rollback taxonomy，而是让 rollback 分支收口后的 operator 第一动作更贴近真实处置路径：
  - `rollback_recovery`：优先确认 known-good 已恢复、对照 candidate verify 失败原因，并阻止同一 candidate 盲目重发；
  - `rollback_failure`：优先检查 known-good image 可用性、rollback helper 执行失败点、rollback verify entrypoint、以及残留 candidate 的人工清理/替换动作。
- 本 cycle 的最小 DoD：
  - `operator_guidance.txt` 对 rollback 成功恢复与 rollback 恢复失败给出不同的 next action 与 guidance；
  - 至少一组最小 rollback 样本完成复跑，证明 guidance 已与 `rollback_readiness_gate` / `rollback_recovery` / `rollback_failure` 对齐；
  - 记账边界保持清晰：`P3-C2` 负责 rollback branch closure，`P3-C7` 负责 rollback-family operator guidance refinement。

**Current status (P3-C7)**

- `P3-C7-S1` 已完成：`cloud_release_workflow.sh` 现在会为 `candidate_reverted_to_known_good` / `rollback_recovery` 与 `manual_recovery_required` / `rollback_failure` 输出更具体的 rollback-family guidance。
- `P3-C7-S2` 已完成第一轮最小 rollback 样本复跑：一条 `PASS_AFTER_ROLLBACK` 样本和一条 `rollback_failure` 样本均已复跑并验证 `operator_guidance.txt` 与 rollback-family branch 对齐。

### P3-C8 (Evidence-capture failure contract | started)

- 目标：把 `evidence_capture_failure` 从“taxonomy 里已定义但没有稳定入口”的状态，推进为 workflow 中可控、可重复、低扰动的 evidence failure branch；这样后续可以专门验证“运行本身成功或如实失败，但 artifact bundle 不完整”的收口语义。
- 这一轮的重点不是制造远端 runtime 故障，而是把 evidence 缺失本身视为一类一等失败：
  - 允许通过受控的 fault injection 入口故意制造 `operator_guidance.txt` 缺失；
  - 当 evidence 不完整时，workflow 应保留真实的 stage/gate 结果，但把最终 `failureClass` 提升为 `evidence_capture_failure`，并把 `terminalStage` 收口到 `evidence`。
- 本 cycle 的最小 DoD：
  - workflow 提供一条低扰动、只影响 artifact 而不影响远端 deploy/runtime 的 evidence fault injection 入口；
  - evidence 缺失时，workflow 能稳定写出 `failureClass=evidence_capture_failure`、`terminalGate=evidence_capture` 与 `evidenceComplete=false`；
  - 至少一条最小 targeted sample 被记账，证明 evidence failure 不会被静默吞掉或混入其他 gate。

**Current status (P3-C8)**

- `P3-C8-S1` 已完成：`cloud_release_workflow.sh` 现在支持 `--simulate-evidence-failure operator-guidance-missing`，并会在 evidence 不完整时把最终分支提升为 `failureClass=evidence_capture_failure`、`terminalStage=evidence`、`operatorAction=inspect_artifacts`。
- `P3-C8-S2` 已完成第一条 `evidence_capture_failure` targeted FAIL 样本：当前已验证在 `preflight/deploy/verify` 全部 PASS 的情况下，只要受控省略 `operator_guidance.txt`，`summary.json` 就会保留真实 gate 结果并把最终分支提升为 `failureClass=evidence_capture_failure`、`terminalGate=evidence_capture`、`evidenceComplete=false`。
- `P3-C8-S3` 已完成 rollback-branch evidence 样本：当前已验证在真实 `verify FAIL -> rollback PASS` 的情况下，只要同样受控省略 `operator_guidance.txt`，workflow 仍会保留 rollback 相关 gate/stage 结果，但把最终分支提升为 `failureClass=evidence_capture_failure`、`terminalGate=evidence_capture`、`evidenceComplete=false`。

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
- [x] `P3-C2-S1`: targeted rollback drill recipe fixed for a safe `verify FAIL -> PASS_AFTER_ROLLBACK` branch
- [x] `P3-C2-S2`: first targeted `PASS_AFTER_ROLLBACK` workflow sample recorded
- [x] `P3-C2-S3`: targeted drill evidence recorded with `summary.json` and `operator_guidance.txt`
- [x] `P3-C3-S1`: gate families and low-cardinality failure-class mapping fixed
- [x] `P3-C3-S2`: gate-level `summary.json` / `operator_guidance.txt` contract fixed
- [x] `P3-C3-S3`: first targeted gate-fail sample recorded with terminal gate evidence
- [x] `P3-C4-S1`: preflight-family-specific operator guidance fixed
- [x] `P3-C4-S2`: refreshed preflight sample set recorded with family-specific guidance
- [x] `P3-C5-S1`: first isolated `dependency_connectivity_gate` targeted FAIL sample recorded
- [x] `P3-C5-S2`: first `post_change_verify_gate` targeted FAIL sample recorded
- [x] `P3-C5-S3`: first `deploy_execution_gate` targeted FAIL sample recorded
- [x] `P3-C6-S1`: runtime-family-specific operator guidance fixed
- [x] `P3-C6-S2`: refreshed runtime sample set recorded with family-specific guidance
- [x] `P3-C7-S1`: rollback-family-specific operator guidance fixed
- [x] `P3-C7-S2`: refreshed rollback sample set recorded with family-specific guidance
- [x] `P3-C8-S1`: evidence-capture failure contract and injection hook fixed
- [x] `P3-C8-S2`: first `evidence_capture_failure` targeted FAIL sample recorded
- [x] `P3-C8-S3`: rollback-branch `evidence_capture_failure` sample recorded

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

### P3-C2-S1S2S3 (First targeted PASS_AFTER_ROLLBACK workflow sample | 2026-03-25)

- headSha: `db761caa`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T110448Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T110448Z/preflight.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T110448Z/deploy.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T110448Z/verify.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T110448Z/rollback.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T110448Z/operator_guidance.txt`
- expected:
  - 按 `P3-C2` 的最小 recipe，从本地工作机经 SSH 触发 Ubuntu VM 上的 deploy / verify / auto rollback，故意通过错误 verify probe port 触发 candidate verify FAIL，但保持 known-good rollback path 可恢复，从而验证 `PASS_AFTER_ROLLBACK` 分支、`rollback_recovery` 分类与 `operator_guidance.txt` 收口语义。
- observed:
  - 本轮 `preflightResult=PASS`、`deployResult=PASS`、`verifyResult=FAIL`、`rollbackResult=PASS`、`result=PASS_AFTER_ROLLBACK`，且 `failureClass=rollback_recovery`、`operatorAction=candidate_reverted_to_known_good`、`terminalStage=rollback`，与 `P3-C2` 目标完全一致；
  - `verify.log` 显示 candidate 容器本身已正常启动并完成 migration，`container_running OK`、`migration_ok OK`、`env_guard_ok OK`，但由于 probe 被故意打到 `http://127.0.0.1:39999/api/v1`，所以 `health_ok FAIL (000)`、`read_smoke_ok FAIL (code=000)`，证明这轮 FAIL 是 workflow 设计内的定向 verify FAIL，而不是 candidate runtime 自身崩溃；
  - `rollback.log` 显示 workflow 已自动切回 `wordloom-backend:cloud-dev-known-good-20260325-pass`，并在 rollback 后再次通过 verify：`container_running OK`、`migration_ok OK`、`health_ok OK (200)`、`read_smoke_ok OK (200 list payload)`、`env_guard_ok OK`、`CLOUD_RELEASE_ROLLBACK_RESULT=PASS`；
  - `operator_guidance.txt` 给出的下一步是保留 service 在 known-good 上、调查 candidate logs 后再做下一轮 deploy；这说明 `S4D-4A/P3` 需要的 trigger / summary / guidance contract 已不止停留在文案层，而是已拿到一轮真实 `PASS_AFTER_ROLLBACK` evidence。
- result:
  - `PASS_AFTER_ROLLBACK`

### P3-C3-S1S2 (Gate family mapping and gate-level summary contract fixed | 2026-03-25)

- artifacts:
  - `scripts/ops/cloud_release_workflow.sh`
  - `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
- expected:
  - 把 `S4D-4A` 已经出现过的 preflight / deploy / verify / rollback 失败面，从 stage-level 结果提升为 gate-level contract，使 workflow 能稳定指出“失败落在哪一类 gate”，而不是只输出总的 `FAIL` 与宽泛的 `failureClass`；
  - `summary.json` 至少固定记录 `terminalGate`、`gateResults`、`evidenceComplete`，便于后续 `P3-C3-S3` 直接围绕单个 gate 设计安全、可重复的 failure drill。
- observed:
  - `cloud_release_workflow.sh` 现已显式维护 `identity_auth_gate`、`target_reachability_gate`、`dependency_connectivity_gate`、`release_contract_gate`、`deploy_execution_gate`、`post_change_verify_gate`、`rollback_readiness_gate` 七类 gate 结果；
  - failure classification 已从旧的 `ssh_connectivity` / `preflight_contract` / `verify_gate` 等 phase-local 名称，收口为 `identity_auth_failure`、`target_reachability_failure`、`dependency_connectivity_failure`、`contract_validation_failure`、`deploy_execution_failure`、`verify_failure`、`rollback_failure` 等 low-cardinality classes；
  - `summary.json` 现已新增 `terminalGate`、`gateResults` 与 `evidenceComplete`，因此后续样本不仅能说明 FAIL 发生在哪个阶段，还能说明 workflow 判定的终止 gate 是什么，以及最小 evidence bundle 是否完整。

### P3-C3-S3 (First targeted identity_auth_gate FAIL sample | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T130950Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T130950Z/preflight.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T130950Z/operator_guidance.txt`
- expected:
  - 用一条安全、可重复、不会触碰真实 deploy/runtime 依赖的样本，证明 `P3-C3` 的 gate-level contract 已能把错误明确落到 `identity_auth_gate`，并在 preflight 阶段停止 workflow；
  - `summary.json` 预期至少记录 `terminalGate=identity_auth_gate`、`failureClass=identity_auth_failure`、`preflightResult=FAIL`，且 `deploy/verify` 结果保持 `NOT_RUN`。
- observed:
  - 通过故意传入不存在的 `--ssh-identity-file`，workflow 在 preflight 阶段如实停止，`summary.json` 记录 `terminalGate=identity_auth_gate`、`failureClass=identity_auth_failure`、`preflightResult=FAIL`、`deployResult=NOT_RUN`、`verifyResult=NOT_RUN`、`rollbackResult=SKIPPED`、`result=FAIL`；
  - `gateResults` 显示仅 `identityAuthGate=FAIL`，其余 gates 均为 `NOT_RUN`，说明 workflow 没有把 identity/auth 失败继续推进成 reachability、deploy 或 verify 噪声；
  - `preflight.log` 同时包含 `Identity file ... not accessible` 与后续 SSH 连接失败文本，但 workflow 仍按更前置的身份合同失败分类为 `identity_auth_failure`；这符合 `P3-C3`“先按最靠前的 gate 收口”的设计目标；
  - `operator_guidance.txt` 明确给出 `stop_and_fix_preflight`，说明这条样本已证明 targeted gate-fail 路径不仅可记录，还能给出正确的 operator next action。
- result:
  - `FAIL (identity_auth_gate)`

### P3-C3-S3 (Second targeted release_contract_gate FAIL sample | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T131737Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T131737Z/preflight.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T131737Z/operator_guidance.txt`
- expected:
  - 用一条安全、可重复、不会触碰真实 deploy/runtime 依赖的样本，证明 `P3-C3` 的 gate-level contract 也能把错误明确落到 `release_contract_gate`，并在 preflight 阶段停止 workflow；
  - `summary.json` 预期至少记录 `terminalGate=release_contract_gate`、`failureClass=contract_validation_failure`、`preflightResult=FAIL`，同时保留 `identityAuthGate=PASS`、`targetReachabilityGate=PASS`，从而说明失败落在更靠后的合同输入层，而不是 SSH 本身。
- observed:
  - 通过故意传入不存在的 `--env-file`，workflow 在 preflight 阶段如实停止，`summary.json` 记录 `terminalGate=release_contract_gate`、`failureClass=contract_validation_failure`、`preflightResult=FAIL`、`deployResult=NOT_RUN`、`verifyResult=NOT_RUN`、`rollbackResult=SKIPPED`、`result=FAIL`；
  - `gateResults` 显示 `identityAuthGate=PASS`、`targetReachabilityGate=PASS`、`releaseContractGate=FAIL`，其余 gates 保持 `NOT_RUN`，说明 workflow 已能把“SSH 身份/连通性通过，但 remote contract 输入错误”与前一条 `identity_auth_gate` 样本清晰地区分开；
  - 为了让这条样本能稳定命中 contract 层，本轮同时修复了当前 WSL/Windows 混合环境中的 SSH client selection：workflow 现在会在 WSL/MSYS 场景优先使用 Windows OpenSSH（`ssh.exe`），避免 `/usr/bin/ssh` 对本地转发 endpoint 的误判把 contract 样本污染成 reachability failure；
  - `preflight.log` 现会明确留下 `env_file_missing=/etc/wordloom/.env.cloud.dev.DOES_NOT_EXIST`，`operator_guidance.txt` 也会在 `contract_validation_failure` 时提示优先检查 `remote_repo_dir`、`env_file` 与 preflight 合同输入，而不是笼统地提示“修 SSH 或 remote contract”。
- result:
  - `FAIL (release_contract_gate)`

### P3-C3-S3 (Third targeted target_reachability_gate FAIL sample | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T132308Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T132308Z/preflight.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T132308Z/operator_guidance.txt`
- expected:
  - 用一条安全、可重复、不会触碰真实 deploy/runtime 依赖的样本，证明 `P3-C3` 的 gate-level contract 也能把错误明确落到 `target_reachability_gate`，并在 preflight 阶段停止 workflow；
  - `summary.json` 预期至少记录 `terminalGate=target_reachability_gate`、`failureClass=target_reachability_failure`、`preflightResult=FAIL`，且 `deploy/verify` 结果保持 `NOT_RUN`。
- observed:
  - 通过故意把 `--ssh-port` 改成不通的 `22999`，workflow 在 preflight 阶段如实停止，`summary.json` 记录 `terminalGate=target_reachability_gate`、`failureClass=target_reachability_failure`、`preflightResult=FAIL`、`deployResult=NOT_RUN`、`verifyResult=NOT_RUN`、`rollbackResult=SKIPPED`、`result=FAIL`；
  - `gateResults` 显示仅 `targetReachabilityGate=FAIL`，其余 gates 均为 `NOT_RUN`，说明 workflow 没有把 reachability 失败继续推进成 contract、deploy 或 verify 噪声；
  - `preflight.log` 中的 `banner exchange: Connection to UNKNOWN port -1: Connection refused` 证明本轮失败落在 SSH reachability 层，而不是身份合同或远端 env/repo 合同层；
  - 至此，`identity_auth_gate`、`target_reachability_gate`、`release_contract_gate` 三条 preflight-level targeted samples 已形成一组可对照的最小 taxonomy evidence。
- result:
  - `FAIL (target_reachability_gate)`

### P3-C4-S1 (Preflight-family-specific operator guidance fixed | 2026-03-25)

- artifacts:
  - `scripts/ops/cloud_release_workflow.sh`
  - `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
- expected:
  - 在 `P3-C3` 已明确 preflight taxonomy 之后，`operator_guidance.txt` 不应继续把 `identity_auth_failure`、`target_reachability_failure`、`contract_validation_failure` 混成同一种排障说明；
  - workflow 应按 failure family 输出更具体的 operator next action，减少 preflight 失败后的第一轮误诊。
- observed:
  - `cloud_release_workflow.sh` 现已对 `stop_and_fix_preflight` 进一步分支：
    - `identity_auth_failure`：聚焦 `ssh-user`、identity file、file permission、host trust；
    - `target_reachability_failure`：聚焦 port forwarding、listener availability、port number、network path / DNS；
    - `contract_validation_failure`：聚焦 `remote_repo_dir`、`env_file`、required workflow inputs；
  - 至此 `P3-C4` 已完成脚本层 contract 收口；下一步只需复跑最小样本，确认新的 guidance 输出与对应 failure class 一致。

### P3-C4-S2 (Refreshed preflight sample set validated family-specific guidance | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T133112Z/operator_guidance.txt`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T133047Z/operator_guidance.txt`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T133049Z/operator_guidance.txt`
- expected:
  - 在 `P3-C4-S1` 之后，三类最小 preflight failures 不应继续共用同一段 `stop_and_fix_preflight` 文案；
  - 复跑后的 `operator_guidance.txt` 应分别指向 identity/auth、target reachability、contract inputs 三种不同的第一排查动作。
- observed:
  - `identity_auth_failure` 复跑样本当前使用错误 SSH 用户名，`operator_guidance.txt` 现明确提示优先检查 `ssh-user`、identity file、file permission 与 host trust；对应 evidence 为 `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T133112Z/operator_guidance.txt`；
  - `target_reachability_failure` 复跑样本当前使用不通的 `--ssh-port 22999`，`operator_guidance.txt` 现明确提示优先检查 port forwarding、listener、port number 与 network path；对应 evidence 为 `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T133047Z/operator_guidance.txt`；
  - `contract_validation_failure` 复跑样本当前使用不存在的 `--env-file`，`operator_guidance.txt` 现明确提示优先检查 `remote_repo_dir`、`env_file` 与 required inputs；对应 evidence 为 `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T133049Z/operator_guidance.txt`；
  - 至此，`P3-C4` 已把 preflight taxonomy 的 operator guidance 从“单一 stop-and-fix”升级为 family-specific remediation，后续可以在不混淆 preflight 层的前提下进入 dependency/runtime 类 targeted taxonomy。

### P3-C5-S1 (First isolated dependency_connectivity_gate FAIL sample | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T133956Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T133956Z/verify.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T133956Z/operator_guidance.txt`
- expected:
  - 在不影响当前正常 service 的前提下，补出第一条 dependency/runtime 层 targeted taxonomy 证据：workflow 应先通过 preflight 与 deploy，再在 verify 阶段因为 runtime 无法连接 DB 而收口到 `dependency_connectivity_gate`；
  - 做法应尽量隔离：使用临时坏依赖 env、独立 container 名、独立 host port，而不是覆盖现有正常 container。
- observed:
  - 通过远端临时复制 `.env.cloud.dev` 并把 `DATABASE_URL` 端口改为 `65432`，再以 `wordloom-api-cloud-dev-dependency-fail` + `30031` 触发 isolated candidate，workflow 如实记录 `preflightResult=PASS`、`deployResult=PASS`、`verifyResult=FAIL`、`terminalGate=dependency_connectivity_gate`、`failureClass=dependency_connectivity_failure`；
  - `summary.json` 同时显示 `identityAuthGate=PASS`、`targetReachabilityGate=PASS`、`releaseContractGate=PASS`、`deployExecutionGate=PASS`、`dependencyConnectivityGate=FAIL`、`postChangeVerifyGate=FAIL`，说明失败面已经推进到 runtime dependency 层，而不是停留在 preflight 或 deploy 输入层；
  - `verify.log` 明确留下 `psycopg.OperationalError` / `sqlalchemy.exc.OperationalError`，指向 `13.211.43.32:65432` 的连接失败；这证明当前样本的失败根因是 DB dependency connectivity，而不是 verify probe 本身；
  - 样本结束后，远端临时 env 文件 `/tmp/wordloom.env.cloud.dev.bad-db-port` 与隔离 container 已被清理，避免把 targeted drill 的残留状态带回当前正常 service。
- result:
  - `FAIL (dependency_connectivity_gate)`

### P3-C5-S2 (First isolated post_change_verify_gate FAIL sample | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T135743Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T135743Z/verify.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T135743Z/operator_guidance.txt`
- expected:
  - 在 `P3-C5-S1` 已经拿到 dependency 层 FAIL 样本之后，再补一条“依赖正常但 verify 失败”的 isolated 样本，使 `dependency_connectivity_gate` 与 `post_change_verify_gate` 的边界在 artifact 中可直接对照；
  - 做法仍保持低扰动：使用正常 cloud-dev env、独立 container 名、独立 host port，但故意把 verify probe 指到错误端口，而不是破坏当前正常 service 或真实依赖。
- observed:
  - 当前以 `wordloom-api-cloud-dev-post-verify-fail` + `30032` 启动 isolated candidate，并故意把 verify probe 指向 `39998`；workflow 如实记录 `preflightResult=PASS`、`deployResult=PASS`、`verifyResult=FAIL`、`terminalGate=post_change_verify_gate`、`failureClass=verify_failure`；
  - `summary.json` 现明确显示 `identityAuthGate=PASS`、`targetReachabilityGate=PASS`、`releaseContractGate=PASS`、`deployExecutionGate=PASS`、`dependencyConnectivityGate=PASS`、`postChangeVerifyGate=FAIL`、`rollbackReadinessGate=NOT_RUN`，说明这次样本已经把“依赖正常”与“verify 失败”稳定拆开；
  - `verify.log` 显示 `container_running OK`、`migration_ok OK`、`env_guard_ok OK`，且容器日志内应用已完成 startup，但 `health_ok FAIL (000)`、`read_smoke_ok FAIL (code=000)`；这证明当前失败根因是 verify probe mismatch，而不是 DB / dependency 连通性；
  - 为了让这条样本拿到干净 taxonomy evidence，本轮同时补了两个 workflow 侧修正：一是普通 `verify_failure` 现会把 `dependencyConnectivityGate` 明确写为 `PASS`；二是在 `ssh.exe` 场景下把 `--ssh-identity-file` 规范化为 Windows 路径，避免非致命 identity warning 污染 deploy/verify 日志并误导 gate classification；
  - 样本结束后，远端隔离 container 已被清理，避免把 targeted drill 的残留状态带回当前正常 service。
- result:
  - `FAIL (post_change_verify_gate)`

### P3-C5-S3 (First isolated deploy_execution_gate FAIL sample | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T140306Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T140306Z/deploy.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T140306Z/operator_guidance.txt`
- expected:
  - 在 `P3-C5-S1` 与 `P3-C5-S2` 已分别拿到 dependency 与 verify 层样本之后，再补一条 deploy 层 targeted FAIL 样本，使 `deploy_execution_gate` 与 dependency / verify 层边界在 artifact 中可直接对照；
  - 做法仍保持低扰动：先在远端占住一个独立 host port，再让 workflow 用同一端口启动 isolated candidate，使失败稳定落在 container bind / startup 层，而不是影响当前正常 service。
- observed:
  - 当前先在远端以临时 port blocker 占住 `127.0.0.1:30033`，再以 `wordloom-api-cloud-dev-deploy-fail` + `30033` 触发 workflow；workflow 如实记录 `preflightResult=PASS`、`deployResult=FAIL`、`verifyResult=NOT_RUN`、`terminalGate=deploy_execution_gate`、`failureClass=deploy_execution_failure`；
  - `summary.json` 现明确显示 `identityAuthGate=PASS`、`targetReachabilityGate=PASS`、`releaseContractGate=PASS`、`deployExecutionGate=FAIL`，而 `dependencyConnectivityGate`、`postChangeVerifyGate`、`rollbackReadinessGate` 均保持 `NOT_RUN`，说明本轮样本没有把 deploy 层失败继续推进成 dependency / verify 噪声；
  - `deploy.log` 显示 backend image build 本身成功，但在 `docker run` 时出现 `failed to bind host port for 0.0.0.0:30033 ... address already in use`；这证明当前失败根因是 deploy execution 层的 host-port bind 冲突，而不是 image contract、runtime dependency 或 post-change verify；
  - `operator_guidance.txt` 当前收口为 `stop_and_fix_deploy`，提示先检查 `deploy.log` 再重跑；样本结束后，远端 port blocker 已清理，`30033` 端口确认释放，没有给当前正常 service 留下残余占口状态。
- result:
  - `FAIL (deploy_execution_gate)`

### P3-C6-S1 (Runtime-family-specific operator guidance fixed | 2026-03-25)

- artifacts:
  - `scripts/ops/cloud_release_workflow.sh`
  - `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
- expected:
  - 在 `P3-C5` 已明确 runtime taxonomy 之后，`operator_guidance.txt` 不应继续把 `dependency_connectivity_failure`、`verify_failure`、`deploy_execution_failure` 混成同一种 runtime 排障说明；
  - workflow 应按 runtime family 输出更具体的 operator next action，减少 verify/deploy 失败后的第一轮误诊。
- observed:
  - `cloud_release_workflow.sh` 现已对 runtime guidance 进一步分支：
    - `dependency_connectivity_failure`：聚焦 DB / registry / DNS / 上游依赖 reachability、credentials 与 env-target correctness；
    - `verify_failure`：聚焦 probe target、port selection、routing、health/read smoke expectation 与应用级 verify 边界；
    - `deploy_execution_failure`：聚焦 image build、docker run、host-port bind、container name 与 runtime prerequisite 冲突；
  - 同时修正了 runtime dependency 分类优先级：verify/runtime 阶段出现 `OperationalError`、`server closed the connection unexpectedly`、`Network is unreachable` 等 dependency 信号时，会优先收口为 `dependency_connectivity_failure`，避免被更宽泛的 reachability 规则误判。

### P3-C6-S2 (Refreshed runtime sample set validated family-specific guidance | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T141401Z/operator_guidance.txt`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T141509Z/operator_guidance.txt`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T141603Z/operator_guidance.txt`
- expected:
  - 在 `P3-C6-S1` 之后，三类最小 runtime failures 不应继续共用同一段 runtime guidance 文案；
  - 复跑后的 `operator_guidance.txt` 应分别指向 dependency diagnosis、verify expectation/probe diagnosis、deploy execution diagnosis 三种不同的第一排查动作。
- observed:
  - `dependency_connectivity_failure` 复跑样本当前继续使用远端临时坏 DB 端口 env，workflow 已恢复稳定收口到 `terminalGate=dependency_connectivity_gate`、`failureClass=dependency_connectivity_failure`；`operator_guidance.txt` 现明确提示优先检查 DB / registry / DNS / 上游依赖连通性、credentials 与 env-target correctness；对应 evidence 为 `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T141401Z/operator_guidance.txt`；
  - `verify_failure` 复跑样本当前继续使用正常 cloud-dev env + 错误 verify probe port，workflow 继续稳定收口到 `terminalGate=post_change_verify_gate`、`failureClass=verify_failure`；`operator_guidance.txt` 现明确提示优先检查 probe target、port selection、routing 与应用级 verify expectation；对应 evidence 为 `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T141509Z/operator_guidance.txt`；
  - `deploy_execution_failure` 复跑样本当前继续使用远端临时 port blocker 制造 host-port bind 冲突，workflow 继续稳定收口到 `terminalGate=deploy_execution_gate`、`failureClass=deploy_execution_failure`；`operator_guidance.txt` 现明确提示优先检查 image build、docker run、host-port bind 与 runtime prerequisite 冲突；对应 evidence 为 `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T141603Z/operator_guidance.txt`；
  - 至此，`P3-C6` 已把 runtime taxonomy 的 operator guidance 从“共享 runtime advice”升级为 family-specific remediation，后续如果继续扩展 rollback 或 evidence-capture failure drill，边界会更清晰。

### P3-C7-S1 (Rollback-family-specific operator guidance fixed | 2026-03-25)

- artifacts:
  - `scripts/ops/cloud_release_workflow.sh`
  - `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
- expected:
  - 在 `P3-C2` 与 `P3-C3` 已经固定 rollback 分支与 rollback gate contract 之后，`operator_guidance.txt` 不应继续把 rollback success-recovery 与 rollback failure 混成同一种宽泛说明；
  - workflow 应按 rollback family 输出更具体的 operator next action，减少 verify FAIL 后进入 rollback 分支时的第一轮误诊。
- observed:
  - `cloud_release_workflow.sh` 现已对 rollback guidance 进一步分支：
    - `rollback_recovery` / `candidate_reverted_to_known_good`：聚焦确认 known-good 已恢复、对照 verify.log 与 rollback.log、避免同一 candidate 盲目重发；
    - `rollback_failure` / `manual_recovery_required`：聚焦 known-good image availability、rollback helper 执行失败点、rollback verify entrypoint、以及残留 candidate 的人工清理/替换动作；
  - 同时补齐了 `rollback_recovery` 的 `terminalGate` 映射：`PASS_AFTER_ROLLBACK` 样本现在会稳定写出 `terminalGate=rollback_readiness_gate`，不再出现 `unknown`。

### P3-C7-S2 (Refreshed rollback sample set validated family-specific guidance | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T142829Z/operator_guidance.txt`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T142654Z/operator_guidance.txt`
- expected:
  - 在 `P3-C7-S1` 之后，rollback success-recovery 与 rollback failure 不应继续共用同一段 rollback guidance 文案；
  - 复跑后的 `operator_guidance.txt` 应分别指向 rollback recovered 与 manual recovery required 两种不同的处置路径。
- observed:
  - `rollback_recovery` 复跑样本当前继续使用 isolated candidate + 错误 verify probe port + 有效 known-good image tag，workflow 稳定收口到 `result=PASS_AFTER_ROLLBACK`、`failureClass=rollback_recovery`、`terminalGate=rollback_readiness_gate`；`operator_guidance.txt` 现明确提示对照 verify.log 与 rollback.log，并阻止同一 candidate 在未解释失败前直接重发；对应 evidence 为 `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T142829Z/operator_guidance.txt`；
  - `rollback_failure` 复跑样本当前继续使用 isolated candidate + 错误 verify probe port + 不存在的 known-good image tag，workflow 稳定收口到 `result=FAIL`、`failureClass=rollback_failure`、`terminalGate=rollback_readiness_gate`、`operatorAction=manual_recovery_required`；`operator_guidance.txt` 现明确提示先检查 rollback.log 中的 known-good image availability、rollback helper 执行失败点，并处理残留 candidate；对应 evidence 为 `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T142654Z/operator_guidance.txt`；
  - `rollback.log` 当前明确留下 `image not found for --skip-build: wordloom-backend:cloud-dev-known-good-DOES-NOT-EXIST`，说明这条 rollback failure 样本确实停在 rollback readiness 层，而不是又回退成 deploy/verify 噪声。

### P3-C8-S1 (Evidence-capture failure contract and injection hook fixed | 2026-03-25)

- artifacts:
  - `scripts/ops/cloud_release_workflow.sh`
  - `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
- expected:
  - `evidence_capture_failure` 不应继续只停留在 taxonomy 枚举里，而应有一条低扰动、可重复、不会影响远端 deploy/runtime 的 controlled path；
  - 当 evidence 缺失时，workflow 应保留真实的 preflight/deploy/verify/rollback 结果，但把最终收口提升为 evidence failure，而不是仍然报告 PASS 或把问题混入其他 gate。
- observed:
  - `cloud_release_workflow.sh` 现已新增 `--simulate-evidence-failure operator-guidance-missing`，可在不改变远端 workflow 路径的前提下，故意让 `operator_guidance.txt` 缺失；
  - workflow 现已新增 evidence promotion 逻辑：只要 `evidence_complete_json()` 判断 evidence bundle 不完整，就会把最终收口提升为 `failureClass=evidence_capture_failure`、`terminalStage=evidence`、`operatorAction=inspect_artifacts`，并在 `summary.json` 中稳定写出 `terminalGate=evidence_capture` 与 `evidenceComplete=false`；
  - 这条 contract 同时覆盖 PASS、FAIL、PASS_AFTER_ROLLBACK 三类收口路径，因此后续 `P3-C8-S2` 可以直接围绕一条已有安全 recipe 注入 evidence 缺失，而不必另造新的远端故障源。

### P3-C8-S2 (First targeted evidence_capture_failure sample recorded | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T143916Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T143916Z/preflight.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T143916Z/deploy.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T143916Z/verify.log`
- expected:
  - 在不引入新的远端 runtime 故障的前提下，补一条最小 `evidence_capture_failure` 样本，证明 workflow 可以在真实 `preflight/deploy/verify` 全部 PASS 时，仅因 evidence bundle 缺失而把最终结果提升为 evidence failure；
  - `summary.json` 预期至少记录 `preflightResult=PASS`、`deployResult=PASS`、`verifyResult=PASS`、`terminalGate=evidence_capture`、`failureClass=evidence_capture_failure`、`evidenceComplete=false`、`result=FAIL`。
- observed:
  - 当前通过 isolated candidate `wordloom-api-cloud-dev-evidence-fail` + `30034` 运行正常 cloud-dev recipe，并附加 `--simulate-evidence-failure operator-guidance-missing`；远端真实运行结果如预期全部通过，`verify.log` 留下 `container_running OK`、`migration_ok OK`、`health_ok OK (200)`、`read_smoke_ok OK (200 list payload)`、`env_guard_ok OK`；
  - artifact 目录中仅保留 `preflight.log`、`deploy.log`、`verify.log`、`summary.json`，故意缺失 `operator_guidance.txt`；`summary.json` 则稳定记录 `preflightResult=PASS`、`deployResult=PASS`、`verifyResult=PASS`、`rollbackResult=SKIPPED`、`terminalStage=evidence`、`terminalGate=evidence_capture`、`failureClass=evidence_capture_failure`、`operatorAction=inspect_artifacts`、`evidenceComplete=false`、`result=FAIL`；
  - 这说明 `P3-C8` 已经拿到一条干净的 targeted evidence：workflow 会保留真实 gate/stage 结果，但不会把 evidence bundle 缺失静默吞掉或误报为 PASS；
  - 本轮同时暴露并修复了一个小的一致性缺口：成功分支在 evidence promotion 后，终端摘要原本仍打印旧的 `result=PASS` / `result=PASS_AFTER_ROLLBACK`；当前已改为统一打印最终 `FINAL_RESULT` 与 `FAILURE_CLASS`，避免控制台摘要与 `summary.json` 脱节；
  - 样本取证完成后，远端隔离 container 已清理，避免给当前正常 service 留下额外运行实例。
- result:
  - `FAIL (evidence_capture)`

### P3-C8-S3 (Rollback-branch evidence_capture_failure sample recorded | 2026-03-25)

- headSha: `8704eda0`
- artifacts:
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T144741Z/summary.json`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T144741Z/verify.log`
  - `artifacts/_tmp_s4d4a_cloud_release_workflow/20260325T144741Z/rollback.log`
- expected:
  - 在 `P3-C8-S2` 已证明正常 PASS 分支会因 evidence 缺失被提升为 `evidence_capture_failure` 之后，再补一条 rollback branch 样本，证明 workflow 即使真实完成 `verify FAIL -> rollback PASS`，也不会因为 evidence fault injection 而丢失 rollback 语义；
  - `summary.json` 预期至少记录 `preflightResult=PASS`、`deployResult=PASS`、`verifyResult=FAIL`、`rollbackResult=PASS`、`postChangeVerifyGate=FAIL`、`rollbackReadinessGate=PASS`，同时把最终结果提升为 `terminalGate=evidence_capture`、`failureClass=evidence_capture_failure`、`evidenceComplete=false`、`result=FAIL`。
- observed:
  - 当前通过 isolated candidate `wordloom-api-cloud-dev-evidence-rollback-fail` + `30035` 运行 rollback recipe：verify 阶段故意把 probe 指向 `39997`，并提供有效 `--known-good-image-tag wordloom-backend:cloud-dev-known-good-20260325-pass` 与 `--rollback-on-verify-fail`，同时附加 `--simulate-evidence-failure operator-guidance-missing`；
  - `verify.log` 如预期记录真实 candidate verify FAIL：`container_running OK`、`migration_ok OK`、`env_guard_ok OK`，但 `health_ok FAIL (000)`、`read_smoke_ok FAIL (code=000)`；`rollback.log` 则如预期记录真实 rollback PASS：known-good 镜像被重新拉起，并通过 `container_running OK`、`migration_ok OK`、`health_ok OK (200)`、`read_smoke_ok OK (200 list payload)`、`env_guard_ok OK`；
  - artifact 目录中故意缺失 `operator_guidance.txt`，但 `summary.json` 稳定保留了 rollback 分支的真实 stage/gate 结果：`verifyResult=FAIL`、`rollbackResult=PASS`、`postChangeVerifyGate=FAIL`、`rollbackReadinessGate=PASS`；与此同时，最终分支被提升为 `terminalStage=evidence`、`terminalGate=evidence_capture`、`failureClass=evidence_capture_failure`、`operatorAction=inspect_artifacts`、`evidenceComplete=false`、`result=FAIL`；
  - 这说明 `P3-C8` 已经覆盖了两条最关键的成功终态变体：正常 PASS 和 `PASS_AFTER_ROLLBACK` 都会在 evidence bundle 缺失时被一致地提升为 evidence failure，而不是静默保持原终态；
  - 样本取证完成后，远端隔离 container 已清理，避免给当前正常 service 留下额外运行实例。
- result:
  - `FAIL (evidence_capture over rollback_recovery)`

## Recent changes (for traceability, optional)

- 2026-03-25: 已为 `S4D` 生成 top-level runbook：`docs/runbook/run-S4D-cloud-runtime-release-operations.md`；`S4D-4A` 现作为该 runbook 的稳定执行来源，而不再只依赖 phase log 阅读来理解 operator path。
- 2026-03-25: `P3-C8-S3` 已完成 rollback-branch evidence 样本；workflow 现已证明即使真实 `verify FAIL -> rollback PASS` 已恢复 known-good，只要 evidence bundle 故意缺失 `operator_guidance.txt`，最终仍会稳定收口到 `failureClass=evidence_capture_failure`、`terminalGate=evidence_capture`，同时保留 `postChangeVerifyGate=FAIL` 与 `rollbackReadinessGate=PASS`。
- 2026-03-25: `P3-C8-S2` 已完成第一条 `evidence_capture_failure` targeted FAIL 样本；workflow 现已证明即使真实 `preflight/deploy/verify` 全部 PASS，只要 evidence bundle 故意缺失 `operator_guidance.txt`，最终也会稳定收口到 `failureClass=evidence_capture_failure`、`terminalGate=evidence_capture`、`evidenceComplete=false`。
- 2026-03-25: 为保证 `P3-C8-S2` 的控制台证据与 `summary.json` 一致，已修正 workflow 成功分支的终端摘要输出；evidence promotion 后不再继续打印过期的 `result=PASS` / `result=PASS_AFTER_ROLLBACK`。
- 2026-03-25: `P3-C8-S1` 已完成第一步：为 `evidence_capture_failure` 增加了 workflow 内的 controlled injection 入口，并把 evidence 不完整时的最终分支收口正式提升为 `evidence_capture_failure` / `terminalGate=evidence_capture`。
- 2026-03-25: `P3-C7` 已完成第一轮收口：rollback-family-specific `operator_guidance.txt` 已落地，并通过一条 `PASS_AFTER_ROLLBACK` 样本与一条 `rollback_failure` 样本复跑验证 rollback guidance 已分流。
- 2026-03-25: 为保证 `P3-C7` 的 rollback evidence contract 完整，已补齐 `rollback_recovery -> rollback_readiness_gate` 的 `terminalGate` 映射，避免 `PASS_AFTER_ROLLBACK` summary 出现 `terminalGate=unknown`。
- 2026-03-25: `P3-C6` 已完成第一轮收口：runtime-family-specific `operator_guidance.txt` 已落地，并通过三条最小 runtime 样本复跑验证 `dependency_connectivity` / `verify_failure` / `deploy_execution` 的 guidance 已分流。
- 2026-03-25: 为保证 `P3-C6` 的 runtime guidance 复跑证据干净，已修正 verify/runtime 阶段的 dependency classification 优先级，避免 dependency 日志里的 `Network is unreachable` 等文本被更宽泛的 reachability 规则误判。
- 2026-03-25: `P3-C5-S3` 已完成第一条 `deploy_execution_gate` isolated FAIL 样本；workflow 现已分别拿到 dependency / verify / deploy 三层 targeted taxonomy evidence，且 deploy 样本能稳定停在 `deployExecutionGate=FAIL`、`verifyResult=NOT_RUN`。
- 2026-03-25: `P3-C5-S2` 已完成第一条 `post_change_verify_gate` isolated FAIL 样本；workflow 现可在 artifact 中明确写出 `dependencyConnectivityGate=PASS` 与 `postChangeVerifyGate=FAIL`，从而把“依赖正常但 verify 失败”与 `P3-C5-S1` 的 dependency failure 清晰分离。
- 2026-03-25: 为拿到干净的 `P3-C5-S2` taxonomy evidence，已补两处 workflow 修正：普通 `verify_failure` 现在会显式保留 `dependencyConnectivityGate=PASS`；`ssh.exe` 场景下的 `--ssh-identity-file` 会先规范化为 Windows 路径，避免非致命 identity warning 污染 deploy/verify 分类。
- 2026-03-25: 新增 `P3-C5`，开始把 targeted taxonomy 从 preflight 层推进到 dependency/runtime 层；第一条 `dependency_connectivity_gate` isolated FAIL 样本已完成，并采用“临时坏 env + 独立 container/port + 事后清理”的低扰动路径。
- 2026-03-25: `P3-C4` 已完成第一轮收口：preflight-family-specific `operator_guidance.txt` 已落地，并通过三条最小 preflight 样本复跑验证 `identity_auth` / `target_reachability` / `contract_validation` 的 guidance 已分流。
- 2026-03-25: 新增 `P3-C4`，把当前工作从“补 preflight taxonomy”切换到“细分 preflight-family operator guidance”；`identity_auth`、`target_reachability`、`contract_validation` 三类 preflight failure 不再共用同一段宽泛 guidance。
- 2026-03-25: `P3-C3-S3` 已补齐第三条 preflight-level targeted evidence：通过不通的 SSH 端口触发 `target_reachability_gate` FAIL；至此 `identity_auth` / `reachability` / `release contract` 三类最小 preflight taxonomy 样本均已成组。
- 2026-03-25: `P3-C3-S3` 已补出第二条 preflight-level targeted evidence：通过不存在的 `--env-file` 触发 `release_contract_gate` FAIL；同时为当前 WSL/Windows 混合环境补齐了 Windows OpenSSH client preference，避免 `/usr/bin/ssh` 把 contract 样本误判成 reachability failure。
- 2026-03-25: `P3-C3-S3` 已拿到第一条 targeted gate-fail evidence：通过无效 `--ssh-identity-file` 触发 `identity_auth_gate` FAIL，artifact 已如实记录 `terminalGate=identity_auth_gate`、`failureClass=identity_auth_failure`，且后续 gates 保持 `NOT_RUN`。
- 2026-03-25: `P3-C3-S1/S2` 已完成第一版落地：`cloud_release_workflow.sh` 现已输出 gate-level results、`terminalGate` 与 `evidenceComplete`，并把 failure taxonomy 收口为更稳定的 low-cardinality classes。
- 2026-03-25: 在 `road-001/M4` 明确之后，已把 `S4D-4A` 的下一段工作固定为 `P3-C3`：继续留在当前 phase 下，专门收口 release preflight gates、failure taxonomy refinement 与 gate-level evidence contract，而不是新开 `S6B` 顶层 spine。
- 2026-03-25: 创建 `S4D-4A`，把 `S4D` 的下一步工作重点明确收敛到“半自动 release workflow + failure taxonomy + evidence capture”，而不是继续停留在人工 SSH 操作层。
- 2026-03-25: 已新增 `scripts/ops/cloud_release_workflow.sh`，把远端 preflight / deploy / verify / optional rollback 收口为单入口 workflow，并固定输出 evidence bundle 与 failure class 摘要。
- 2026-03-25: 第一次本地触发 workflow 样本暴露出结果记账 bug：`ssh` 失败时 `run_remote_step()` 仍返回成功，导致 `summary.json` 错写 PASS；当前已转入修复并准备重跑。
- 2026-03-25: 修复 workflow result accounting 后，第一轮真实本地触发样本已如实记录为 `FAIL (ssh_connectivity)`；当前下一步不再是修脚本，而是诊断 WSL 工作机到 Ubuntu VM 的 SSH 路径。
- 2026-03-25: 在补齐 PowerShell 非交互 SSH 认证后，第一轮 authenticated local-triggered 样本已把失败面推进到 `dependency_connectivity`：当前阻塞位于 Ubuntu VM 到 RDS `5432` 的真实数据库连通层。
- 2026-03-25: 在为当前公网 IP 补齐 RDS inbound allow rule 后，第一轮 local-triggered semi-automated workflow 已取得 PASS；`S4D-4A/P2` 现已具备真实本地触发 deploy/verify evidence。
- 2026-03-25: `S4D-4A/P3` 已把 rollback trigger 与 operator wording 收口进 workflow：`summary.json` 现可固定记录 `rollbackTrigger/operatorAction/terminalStage`，并新增 `operator_guidance.txt` 作为失败后的下一步动作说明。
- 2026-03-25: `P3-C2` 已准备最小定向 rollback drill recipe：优先用 verify probe port mismatch 触发 `verify FAIL -> PASS_AFTER_ROLLBACK`，先验证 branch 语义与 operator guidance，再决定是否继续补真实坏 candidate 样本。
- 2026-03-25: `P3-C2` 已拿到第一条真实 `PASS_AFTER_ROLLBACK` 样本：candidate verify 被定向打成 FAIL，但 workflow 已自动切回 known-good 并通过 rollback verify，`operator_guidance.txt` 也已按 `candidate_reverted_to_known_good` 收口。
- 2026-03-25: 稳定性评估完成；由于 `P0-P3` 的 contract、single-entry workflow、failure taxonomy、operator wording、真实本地 PASS 样本与真实 `PASS_AFTER_ROLLBACK` 样本均已到位，`S4D-4A` 现可按 v1 口径标记为 `stable`。