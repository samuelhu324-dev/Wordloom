# run-S4D (Cloud Runtime Release Operations)

---

**id**: `run-S4D-cloud-runtime-release-operations`
**kind**: `runbook`
**title**: `run/S4D-cloud-runtime-release-operations`
**status**: `stable`
**scope**: `S4D`
**decision_date**: `2026-03-25`
**context_issue**:
  **DoD**: `S4D-4A established a stable single-entry operator workflow for cloud runtime deploy, verify, rollback, and evidence capture.`
  **Labs**: ``
**decision**: `Use scripts/ops/cloud_release_workflow.sh as the canonical operator entry for cloud runtime release operations, with summary.json and operator_guidance.txt as the minimum evidence contract.`
  **positive**: `"Repeatable operator entry", "Machine-verifiable evidence", "Stable troubleshooting path"`
  **negative**: `"Still operator-driven rather than CI-triggered", "Need to keep release and evidence contracts stable"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 给操作者一条最小、稳定、可重复的 cloud runtime release path：从本地工作机触发远端 preflight、deploy、verify，并在需要时自动 rollback。
- 固定 release operations 的最小证据合同：每次运行都应留下 `summary.json`、阶段日志，以及在非故意注入 evidence fault 时生成 `operator_guidance.txt`。
- 让操作者在失败时先看 gate/failure class 和 guidance，而不是先回到“手动 SSH + 人肉拼命令 + 人脑判错”的旧路径。

## 2) Scope

- 覆盖内容：
  - `S4D-4A` 已稳定的 single-entry cloud release workflow；
  - 本地工作机到单 Ubuntu VM 的 backend container deploy / verify / optional rollback operator path；
  - gate-level result、failure taxonomy、operator guidance 与 evidence bundle 的最小收口；
  - 正常 PASS、`PASS_AFTER_ROLLBACK`、targeted FAIL、以及 evidence failure 的一等处理。
- 不覆盖内容：
  - GitHub Actions runner、environment approval、repo secret wiring、artifact upload retention policy；
  - GitOps controller、Kubernetes reconciliation、multi-host orchestration；
  - UI/worker 云端部署或 production-grade traffic shifting。
- 深层历史与契约来源：
  - `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  - `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
  - `docs/logs/log-S4D-3A-cloud-runtime-rollback-sample.md`
  - `scripts/ops/cloud_release_workflow.sh`
  - `scripts/ops/cloud_release_verify.sh`
  - `scripts/ops/cloud_release_rollback.sh`

## 3) Evidence Bundle

### 3.1 Output roots

- 默认 artifact 根目录：`artifacts/_tmp_s4d4a_cloud_release_workflow/<timestamp>/`
- 最小证据文件：
  - `preflight.log`
  - `deploy.log`
  - `verify.log`
  - `rollback.log`（如发生 rollback）
  - `summary.json`
  - `operator_guidance.txt`（若不是故意执行 evidence fault injection）
- 最低有效判断：
  - `summary.json` 必须能说明 `preflight/deploy/verify/rollback` 结果、`terminalGate`、`failureClass`、`operatorAction` 与 `evidenceComplete`。

### 3.2 Summary or ledger

- phase ledger：`docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
- 顶层 spine：`docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
- 最低字段：
  - `headSha`
  - `targetHostKind`
  - `envFilePath`
  - `imageTag`
  - `deployResult`
  - `verifyResult`
  - `rollbackResult`
  - `terminalGate`
  - `failureClass`
  - `gateResults`
  - `operatorAction`
  - `evidenceComplete`
  - `result`

## 4) One-click Automation

### 4.1 What it does

- 从本地工作机通过 SSH 连接远端 Ubuntu VM。
- 先做 release preflight，验证 repo 目录、env file、SSH 身份与目标 reachability。
- 调用既有 helper 执行 deploy、verify，并在 armed 情况下执行 rollback。
- 把 stage-level 结果压缩成 gate-level summary、failure class 和 operator action。
- 在本地生成 evidence bundle，并在 evidence 不完整时把最终结果提升为 `evidence_capture_failure`。

### 4.2 Operator instructions

- canonical entrypoint：

```powershell
bash scripts/ops/cloud_release_workflow.sh \
  --ssh-host 127.0.0.1 \
  --ssh-port 22022 \
  --ssh-user wordloom \
  --ssh-identity-file /c/Users/H/.ssh/id_ed25519 \
  --remote-repo-dir /home/wordloom/work/wordloom-v3 \
  --env-file /etc/wordloom/.env.cloud.dev \
  --image-tag wordloom-backend:cloud-dev \
  --container-name wordloom-api-cloud-dev \
  --host-port 30021 \
  --api-port 30021
```

- operator 可调整的稳定输入：
  - SSH target：`--ssh-host`、`--ssh-port`、`--ssh-user`、`--ssh-identity-file`
  - release target：`--remote-repo-dir`、`--env-file`、`--image-tag`
  - runtime target：`--container-name`、`--host-port`、`--api-port`
  - rollback：`--known-good-image-tag`、`--rollback-on-verify-fail`
  - evidence drill only：`--simulate-evidence-failure operator-guidance-missing`
- success 语义：
  - `summary.json` 显示 `result=PASS`，或在 armed rollback recovery 下显示 `result=PASS_AFTER_ROLLBACK`；
  - `failureClass=none` 或 `rollback_recovery`；
  - `evidenceComplete=true`。
- failure 语义：
  - `summary.json` 显示 `result=FAIL`；
  - `terminalGate`、`failureClass` 和 `operatorAction` 能直接指出第一处理方向；
  - 若 `evidenceComplete=false`，即使真实 deploy/verify/rollback 已完成，也应按 `evidence_capture_failure` 处理。

## 5) Local Operation

### 5.1 Prerequisites

- 本地工作机可运行 `bash` 与 `git`；
- 可用的 SSH 身份文件，且当前环境下若优先使用 `ssh.exe`，路径需可被 Windows OpenSSH 识别；
- 远端 Ubuntu VM 已准备好 Docker、repo sync、以及可用的 env file；
- cloud-dev RDS 与相关依赖保持可达；
- 若需要 rollback，已知的 `known-good image tag` 必须存在且可被远端拉起。

### 5.2 Commands

- 默认 PASS path：

```powershell
bash scripts/ops/cloud_release_workflow.sh \
  --ssh-host 127.0.0.1 \
  --ssh-port 22022 \
  --ssh-user wordloom \
  --ssh-identity-file /c/Users/H/.ssh/id_ed25519 \
  --remote-repo-dir /home/wordloom/work/wordloom-v3 \
  --env-file /etc/wordloom/.env.cloud.dev \
  --image-tag wordloom-backend:cloud-dev \
  --container-name wordloom-api-cloud-dev \
  --host-port 30021 \
  --api-port 30021
```

- 默认 rollback-armed path：

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

- evidence drill only：

```powershell
bash scripts/ops/cloud_release_workflow.sh \
  --ssh-host 127.0.0.1 \
  --ssh-port 22022 \
  --ssh-user wordloom \
  --ssh-identity-file /c/Users/H/.ssh/id_ed25519 \
  --remote-repo-dir /home/wordloom/work/wordloom-v3 \
  --env-file /etc/wordloom/.env.cloud.dev \
  --image-tag wordloom-backend:cloud-dev \
  --container-name wordloom-api-cloud-dev-evidence-fail \
  --host-port 30034 \
  --api-port 30034 \
  --simulate-evidence-failure operator-guidance-missing
```

## 6) Troubleshooting

- 症状：`failureClass=identity_auth_failure`
  - 先看 `preflight.log`；优先检查 `ssh-user`、identity file 路径、文件权限、host trust。

- 症状：`failureClass=target_reachability_failure`
  - 先看 `preflight.log`；优先检查目标端口、listener、端口转发与 operator host 到 target 的网络路径。

- 症状：`failureClass=contract_validation_failure`
  - 先看 `preflight.log` 或 `deploy.log`；优先检查 `remote_repo_dir`、`env_file`、image tag、required inputs。

- 症状：`failureClass=dependency_connectivity_failure`
  - 先看 `verify.log`；优先检查 DB / registry / DNS / 上游依赖可达性、credentials、env-target correctness。

- 症状：`failureClass=verify_failure`
  - 先看 `verify.log`；若 `container_running`、`migration_ok`、`env_guard_ok` 已通过，就先排查 probe target、port、routing 和 verify expectation。

- 症状：`failureClass=rollback_failure`
  - 先看 `rollback.log`；优先检查 known-good image 是否存在、rollback helper 执行点、rollback verify entrypoint，以及残留 candidate 清理。

- 症状：`failureClass=evidence_capture_failure`
  - 先看 `summary.json` 的 `gateResults` 和 `evidenceComplete`，再确认 artifact 目录是否缺失 `operator_guidance.txt` 或其他最低 evidence 文件。

## 7) Notes and Boundaries

- 这份 runbook 是稳定 operator path，不是 phase 时间线；详细 drill 证据仍以 `S4D-4A` log 为准。
- 当前 canonical path 仍是 operator-driven local trigger，不是 GitHub Actions workflow，也不是 GitOps controller。
- evidence fault injection 只用于 drills，不应作为日常 release 默认参数。
- 下一步最自然的扩展点是把当前单入口 workflow 接入 GitHub Actions 的受控 dispatch / approval path；如果进入这一步，应在后续 `S4D-4B` 中记录，而不是继续把 runbook 变成 phase 历史副本。