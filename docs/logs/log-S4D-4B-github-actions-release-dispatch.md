# log-S4D-4B (Phase 4B: GitHub Actions Release Dispatch)

---

**id**: `S4D-4B`
**kind**: `log`
**title**: `cloud runtime release workflow via GitHub Actions dispatch (approval-ready runner entry, evidence upload, operator handoff) + drills/evidence v1`
**status**: `stable`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, ReleaseOperations, Automation, GitHubActions, Evidence, epic/s4, sub/4b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **parent_log**: `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  **previous_log**: `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
  **reference_log_1**: `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
  **reference_log_2**: `docs/runbook/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
  **reference_log_3**: `docs/logs/_template-log-phase-drills-evidence.md`
**created**: `2026-03-25`
**updated**: `2026-03-26`

---

## Decision / Outcome

**Decision**:

- `S4D-4B` 承接 `S4D-4A` 已稳定的 single-entry operator workflow，目标不是重写 deploy 语义，而是把现有 `cloud_release_workflow.sh` 接到 GitHub Actions 的受控 dispatch / approval / artifact upload path；
- v1 的重点是把“本地 operator 机器触发”升级为“repo-controlled runner 触发”，同时保留 `S4D-4A` 已固定的 gate taxonomy、failure classes、summary contract 与 rollback 语义。

**Default choices (phase defaults / v1)**:

- 优先复用 `scripts/ops/cloud_release_workflow.sh` 作为执行核心，不为 GitHub Actions 再造平行 deploy path；
- Actions v1 默认采用 `workflow_dispatch` 手动触发，而不是先做 merge-to-deploy 或 push-to-deploy 自动发布；
- approval、environment secrets、artifact upload、run summary 优先收口到 GitHub Actions 原生能力，而不是同时引入外部 deploy orchestrator；
- v1 仍以单 Ubuntu VM + backend container + cloud-dev env 为默认目标，不同时扩到多 host / 多 environment 并发矩阵；
- v1 runner contract 现已进一步收紧为 `self-hosted runner`，优先复用当前本地可达的 SSH target，而不是继续维持“GitHub-hosted 也许可用”的模糊前提；
- Actions job 的成功/失败语义继续以 `summary.json` 为准，而不是仅看 job exit text。

## Definitions (optional)

- **Dispatch workflow**：通过 GitHub Actions `workflow_dispatch` 手动触发的发布入口。
- **Runner entry**：在 GitHub-hosted 或 self-hosted runner 上执行的稳定命令入口。
- **Environment approval**：在 GitHub Actions environment 中要求人工确认后才能继续的受控门。
- **Uploaded evidence**：将本地 artifact 目录作为 workflow artifacts 上传，便于审计和回放。

## Constraints

- 不把 SSH 私钥、远端 env 文件内容或数据库 secrets 写入仓库；
- 不在第一轮同时引入 GitOps controller、Kubernetes deployment manifest、Argo CD/Flux；
- GitHub Actions 集成必须复用现有 gate/failure taxonomy，而不是在 Actions 层另造 PASS/FAIL 解释体系；
- v1 先保证可审计、可重放、可审批，再追求更强自动触发策略。

## Scope

- `P0`: contract（Actions trigger contract、inputs、secrets、artifact upload 与 run summary contract）
- `P1`: implementation / workflow（GitHub Actions workflow 文件、runner entry、artifact publish）
- `P2`: drill / verify（第一次 dispatch -> deploy -> verify / rollback 样本）
- `P3`: approvals / handoff（environment approval、operator handoff、failure triage wording）

## Success Criteria (DoD)

- 仓库内存在一条 Actions `workflow_dispatch` 入口，可稳定触发当前 `S4D-4A` release workflow；
- Actions run 至少能上传 `summary.json` 与阶段日志作为 workflow artifacts；
- run summary 至少能固定展示 `result`、`failureClass`、`terminalGate` 与 artifact 链接；
- 至少一轮 GitHub Actions dispatch 样本被记账，证明 repo-controlled runner 能替代本地 operator 机器触发；
- 失败 triage 仍然沿用 `S4D-4A` 的 gate taxonomy 与 operator guidance，而不是退回 Actions 文本拼接。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 GitHub Actions trigger contract、runner entry、artifact upload 与 approval path 已稳定；
  - Evidence 区至少包含一轮可追溯的 dispatch run（headSha + run URL / artifact URL + result summary）。

## P0 (Contract | v1)

### P0-C1-S1 (Actions trigger contract | v1)

- v1 触发方式固定为 `workflow_dispatch`；
- 至少允许以下输入：
  - target host inputs（host/user/port）
  - release inputs（env file、image tag）
  - runtime inputs（container name、host port、api port）
  - rollback inputs（known-good image tag、rollback toggle）
- evidence fault injection 输入仅保留给受控 drill，不应作为默认生产化入口暴露。

### P0-C1-S2 (Runner and secret contract | v1)

- runner 必须能访问 git、bash、ssh，并能读取受控 secret store 中的 SSH identity；
- 若当前 target 仍依赖本地转发的 `127.0.0.1:22022` 这类入口，则 GitHub-hosted runner 无法直接复用该路径；此时 v1 需要 self-hosted runner，或先把 target host 暴露成 runner 可达的 SSH endpoint；
- GitHub Actions environment 应明确区分 cloud-dev 与未来更高环境；
- Actions 层只负责安全注入与触发，不改变 `cloud_release_workflow.sh` 的业务语义。

### P0-C1-S3 (Evidence and run-summary contract | v1)

- 每次 run 至少应上传：
  - `summary.json`
  - `preflight.log`
  - `deploy.log`
  - `verify.log`
  - `rollback.log`（如发生）
  - `operator_guidance.txt`（如 evidence 完整）
- run summary 至少应展示：
  - `headSha`
  - `result`
  - `failureClass`
  - `terminalGate`
  - `evidenceComplete`
  - artifact 下载入口

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4D-4B/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`）或同一 phase / cycle 下连续 steps 的组合（如 `1S2`）。

**Branch convention**:

- `S4D-4B` 相关实现与文档优先落在 `S4D-cloud-runtime-deploy-verify-rollback` 分支，直至需要拆出单独 Actions-focused 子分支。

**Commit discipline (recommended)**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4D-cloud-runtime-deploy-verify-rollback`。

## Plan (draft)

### P1 (Implementation / workflow)

- P1-C1-S1: 新增 GitHub Actions `workflow_dispatch` 入口，映射 `S4D-4A` release workflow 的最小输入
- P1-C1-S2: 上传 `summary.json` 与阶段日志，并把关键字段写入 GitHub Actions run summary
- P1-C1-S3: 把 runner contract 从泛化的 hosted/self-hosted 二选一收紧为 self-hosted runner v1，并与当前 SSH target/network 前提对齐
- P1-C2-S1: 在 dispatch 前把 target repo 同步到 workflow branch/head，消除 `remoteHeadSha` 漂移
- P1-C2-S2: 用真实 Actions PASS 样本验证 `headSha == expectedHeadSha == remoteHeadSha`
- P1-C3-S1: 拆分 `push` 与 `workflow_dispatch` 的 concurrency group，避免 push waiting run 阻塞 manual drill materialization
- P1-C3-S2: 用真实 Actions 控制面样本验证 push/manual 可并存进入 waiting，而不再需要先取消旧 run

**Current status (S4D-4B)**

- `P0-C1-S1` 已完成第一版 Actions trigger contract：当前已固定 `workflow_dispatch` 输入集合，覆盖 SSH target、release inputs、runtime inputs、rollback toggle 与 verify tuning。
- `P0-C1-S2` 已完成第一版 runner/secret contract：当前使用 `S4D_SSH_PRIVATE_KEY` 作为 required secret，`S4D_SSH_KNOWN_HOSTS` 作为 optional secret，并已确认 repo 可创建 `cloud-dev` environment 与 self-hosted runner registration token。
- `P0-C1-S3` 已完成第一版 evidence/run-summary contract：当前 workflow 会上传整个 artifact 目录，并把 `result`、`failureClass`、`terminalGate`、`terminalStage`、`operatorAction`、`evidenceComplete` 与 gate results 写入 `GITHUB_STEP_SUMMARY`。
- `P1-C1-S1` 与 `P1-C1-S2` 已完成第一版落地：仓库现已新增 `.github/workflows/s4d-cloud-release-dispatch.yml`，直接复用 `cloud_release_workflow.sh` 作为 runner entry。
- `P1-C1-S3` 已完成：当前 workflow 已收紧为 `runs-on: self-hosted`，并显式验证 self-hosted runner 的 bash/git/ssh contract，不再维持对 GitHub-hosted runner 的模糊兼容假设。
- `P2-C1-S1` 已完成：当前 self-hosted runner 已拿到第一条真实 Actions-triggered PASS 样本，说明 GitHub Actions dispatch path 现在可以稳定完成 checkout、SSH identity 注入、`cloud_release_workflow.sh` 执行、`summary.json` 生成、artifact upload、run summary 输出与最终 PASS 判定。
- 本轮 PASS 的直接恢复动作是为 target host 当前出口公网 IP `125.253.50.4/32` 临时补入 cloud-dev RDS `5432` inbound allow rule；这说明前一轮 blocker 不是 Actions workflow，而是 target host 到 cloud DB 的环境依赖白名单漂移。
- `P2-C1-S2` 已完成：当前 workflow 已拿到第一条真实 Actions-triggered `PASS_AFTER_ROLLBACK` 样本，证明在 candidate verify 失败时，GitHub Actions path 能稳定完成自动 rollback、产出完整 evidence，并以成功 workflow 收口。
- `P3-C1-S1` 已完成：`cloud-dev` environment approval boundary 现已被真实 run 多次命中，manual `workflow_dispatch` run 会先进入 `waiting`，且只有在 reviewer approval 后才继续执行发布 job。
- `P3-C1-S2` 已完成：当前 workflow run summary 与 `operator_guidance.txt` 已稳定给出 `result`、`failureClass`、`terminalGate`、artifact 路径与下一步 operator action，handoff wording 已有真实 rollback 样本验证。
- `P1-C2-S1/S2` 已完成：当前 workflow 已把 `github.ref_name` 与 `github.sha` 作为显式 contract 传入 release script，并在 preflight 阶段完成 target repo 的 clean-check、`git fetch`、branch 对齐与 exact-head reset；最新 PASS 样本已证明 `headSha == expectedHeadSha == remoteHeadSha`。
- `P1-C3-S1/S2` 已完成：当前 workflow 已把 concurrency group 从“仅按 environment 串行”调整为“按 trigger surface + environment 串行”；真实控制面样本已证明同一 `headSha` 下的 `push` run 与 manual `workflow_dispatch` run 可以各自 materialize 出独立 job，并同时停在 `cloud-dev` approval gate，不再需要先取消 push waiting run。

### P2 (Drill / Verify)

- P2-C1-S1: 执行第一轮 Actions-triggered deploy -> verify 样本
- P2-C1-S2: 执行第一轮 Actions-triggered verify FAIL -> rollback PASS_AFTER_ROLLBACK 样本

### P3 (Approvals / Handoff)

- P3-C1-S1: 固定 environment approval / manual confirmation 的最小边界
- P3-C1-S2: 固定 run summary 到 operator handoff 的最小 wording 与 artifact path

**Current status (S4D-4B)**

- `P0-P3` 当前已全部完成；
- GitHub Actions 入口现已固定到可访问 `127.0.0.1:22022` target bridge 的 Windows self-hosted runner，并在 workflow 内补齐 Git Bash bootstrap 与 checked-out repo working-directory contract；
- 最新 head-sync validation run `23600877818` 已以 `result=PASS` 收口，且 `summary.json` 明确记录 `headSha == expectedHeadSha == remoteHeadSha == fdd3e812...`；连同此前 `23599857316` 的 rollback evidence，说明 `S4D-4B` 的 dispatch / approval / artifact / handoff / target-head alignment path 已满足 phase DoD。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: Actions trigger contract fixed
- [x] `P0-C1-S2`: runner and secret contract fixed
- [x] `P0-C1-S3`: evidence upload and run-summary contract fixed

### P1 (Implementation / workflow)

- [x] `P1-C1-S1`: workflow_dispatch entry prepared
- [x] `P1-C1-S2`: artifact upload and run summary prepared
- [x] `P1-C1-S3`: self-hosted runner v1 contract aligned with current SSH target
- [x] `P1-C2-S1`: target repo sync before release prepared
- [x] `P1-C2-S2`: remote head alignment evidence recorded
- [x] `P1-C3-S1`: push/manual concurrency groups split
- [x] `P1-C3-S2`: push/manual coexistence evidence recorded

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: first Actions-triggered PASS sample recorded
- [x] `P2-C1-S2`: first Actions-triggered PASS_AFTER_ROLLBACK sample recorded

### P3 (Approvals / Handoff)

- [x] `P3-C1-S1`: environment approval boundary fixed
- [x] `P3-C1-S2`: operator handoff summary fixed

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, Actions run URL, key inputs, and uploaded artifact paths.

### P0-C1-S1S2S3 / P1-C1-S1S2S3 (Actions dispatch workflow and self-hosted runner contract prepared | 2026-03-26)

- headSha: `e6ab1978`
- artifacts:
  - `.github/workflows/s4d-cloud-release-dispatch.yml`
  - `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
- expected:
  - 仓库内新增一条 GitHub Actions `workflow_dispatch` 入口，能复用 `cloud_release_workflow.sh` 执行 cloud runtime release；
  - workflow 至少能安全注入 SSH key、上传 artifact 目录，并把 `summary.json` 的关键字段写进 run summary；
  - contract 层应明确区分“workflow 已就绪”和“第一轮真实 dispatch evidence 尚未执行”的边界；
  - 若当前 target 继续使用 `127.0.0.1:22022` 这类本地转发入口，则 runner contract 应明确收敛到 self-hosted，而不是维持 hosted/self-hosted 混合表述。
- observed:
  - 当前已新增 `.github/workflows/s4d-cloud-release-dispatch.yml`，workflow 会通过 `workflow_dispatch` 收集 SSH target、release inputs、runtime inputs 与 rollback inputs，并在 runner 上直接调用 `scripts/ops/cloud_release_workflow.sh`；
  - workflow 现已固定 secret contract：`S4D_SSH_PRIVATE_KEY` 为 required secret，`S4D_SSH_KNOWN_HOSTS` 为 optional secret；同时 repo 侧 `cloud-dev` environment 与 runner registration token 权限已验证可用；
  - workflow 现已把 runner contract 收紧到 `runs-on: self-hosted`，并显式检查 self-hosted runner 的 bash/git/ssh 可用性，因此当前实现已与现有 `127.0.0.1:22022` target 前提对齐；
  - workflow 现已固定 evidence contract：无论成功或失败，都会上传本次 artifact 目录，并把 `summary.json` 中的 `result`、`failureClass`、`terminalGate`、`terminalStage`、`operatorAction`、`evidenceComplete` 与 gate results 写入 `GITHUB_STEP_SUMMARY`；
  - 当前 `S4D-4B` 已完成 P0/P1 的 contract 和 implementation，但 P2 尚未执行，因为第一轮真实 dispatch 样本仍取决于 runner 是否具备到 target host 的真实 SSH reachability。

### P2-C1-S1 (first real Actions-triggered dispatch executed, workflow path proven, PASS sample still blocked by real dependency failure | 2026-03-26)

- headSha: `0f354032`
- run_url: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23575789110`
- artifacts:
  - `artifacts/_tmp_s4d4b_run_23575789110/s4d-cloud-release-23575789110-1/summary.json`
  - `artifacts/_tmp_s4d4b_run_23575789110/s4d-cloud-release-23575789110-1/preflight.log`
  - `artifacts/_tmp_s4d4b_run_23575789110/s4d-cloud-release-23575789110-1/deploy.log`
  - `artifacts/_tmp_s4d4b_run_23575789110/s4d-cloud-release-23575789110-1/verify.log`
  - `artifacts/_tmp_s4d4b_run_23575789110/s4d-cloud-release-23575789110-1/operator_guidance.txt`
- expected:
  - 第一轮 GitHub Actions self-hosted dispatch 至少应完整走通 checkout、secret injection、remote preflight/deploy/verify、artifact upload 与 run summary；
  - 若 underlying release path 正常，则 `P2-C1-S1` 应以 PASS 样本收口，并把 Actions run URL 与 artifact bundle 记入本 log。
- observed:
  - 第四轮真实 dispatch run `23575789110` 已完整走通 `Checkout -> Validate self-hosted runner contract -> Validate secret contract -> Prepare SSH identity -> Run cloud release workflow -> Locate summary.json -> Write run summary -> Upload workflow artifacts`，说明 `S4D-4B` 的 Actions 执行链路已被真实打通；
  - 本轮 workflow failure 只发生在最终 `Enforce workflow result`，原因不是 Actions glue code 崩溃，而是 `summary.json` 明确记为 `result=FAIL`、`failureClass=dependency_connectivity_failure`、`terminalGate=dependency_connectivity_gate`；
  - artifact 中的 `verify.log` 显示 deploy 已成功启动 candidate container，但 migration 阶段连接云端 PostgreSQL 失败，容器以 exit code `1` 退出，因此 verify 收口为真实 dependency failure；
  - 对 target host 的非破坏性诊断进一步确认：当前 `/home/wordloom/work/wordloom-v3` 处于 clean state，但 HEAD 仍为 `b3002d071d08f748ea438883914c876238af440f`；同时从 target host 到 `wlv3-cloud-dev-postgres...:5432` 的原始 TCP 探测超时，因此当前 `P2-C1-S1` 的 blocker 是环境依赖可用性，而不是 runner / workflow contract。

### P2-C1-S1 (first real Actions-triggered PASS sample recorded after restoring target-host-to-RDS allowlist | 2026-03-26)

- headSha: `0f354032`
- run_url: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23578016775`
- artifacts:
  - `artifacts/_tmp_s4d4b_run_23578016775/s4d-cloud-release-23578016775-1/summary.json`
  - `artifacts/_tmp_s4d4b_run_23578016775/s4d-cloud-release-23578016775-1/preflight.log`
  - `artifacts/_tmp_s4d4b_run_23578016775/s4d-cloud-release-23578016775-1/deploy.log`
  - `artifacts/_tmp_s4d4b_run_23578016775/s4d-cloud-release-23578016775-1/verify.log`
  - `artifacts/_tmp_s4d4b_run_23578016775/s4d-cloud-release-23578016775-1/operator_guidance.txt`
- expected:
  - 在修复 target host -> cloud-dev RDS 的 dependency connectivity 后，下一轮 GitHub Actions self-hosted dispatch 应以真实 PASS 收口；
  - PASS run 至少应完整走通 `Run cloud release workflow`、artifact upload 与 `Enforce workflow result`，并在 `summary.json` 中收口为 `result=PASS`。
- observed:
  - 在为 target host 当前出口公网 IP `125.253.50.4/32` 临时补入 RDS security group 的 `5432/TCP` allow rule 后，从 target host 到 `wlv3-cloud-dev-postgres...:5432` 的原始 TCP 探测已恢复为 `PASS`；
  - 第五轮真实 dispatch run `23578016775` 已完整走通 `Checkout -> Validate self-hosted runner contract -> Validate secret contract -> Prepare SSH identity -> Run cloud release workflow -> Locate summary.json -> Write run summary -> Upload workflow artifacts -> Enforce workflow result`，且 job 最终为 `success`；
  - artifact 中的 `summary.json` 已明确记录 `result=PASS`、`deployResult=PASS`、`verifyResult=PASS`、`failureClass=none`、`terminalGate=none`、`evidenceComplete=true`；对应 `verify.log` 也已记录 `container_running OK`、`migration_ok OK`、`health_ok OK (200)`、`read_smoke_ok OK (200 list payload)`、`env_guard_ok OK`；
  - 当前 `S4D-4B/P2-C1-S1` 已按 phase 定义完成第一条真实 Actions-triggered PASS 样本，但 evidence 同时暴露一个残余差异：本次 `summary.json` 里的 `remoteHeadSha` 仍为 target host 当前 repo HEAD `b3002d071d08f748ea438883914c876238af440f`，尚未显式收口为“dispatch branch head 必须先同步到 target host”这一更强合同。

### P2-C1-S2 / P3-C1-S1S2 (first real Actions-triggered PASS_AFTER_ROLLBACK sample recorded, approval boundary re-proven, operator handoff fixed | 2026-03-26)

- headSha: `7f3c417d`
- run_url: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23599857316`
- artifacts:
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/summary.json`
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/preflight.log`
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/deploy.log`
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/verify.log`
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/rollback.log`
  - `artifacts/_tmp_s4d4b_run_23599857316/s4d-cloud-release-23599857316-1/operator_guidance.txt`
- expected:
  - manual `workflow_dispatch` run 应先命中 `cloud-dev` environment approval gate，再在 approval 后执行发布 job；
  - 受控 verify failure 输入（`api_port=39999`）应触发 candidate verify FAIL，但在 supplied known-good image + `rollback_on_verify_fail=true` 条件下，以 `PASS_AFTER_ROLLBACK` 收口；
  - workflow artifacts 与 run summary 应完整保留 rollback 场景所需的 triage / handoff 信息，而不是仅以 job success 文本结束。
- observed:
  - run `23599857316` 在 approval 前进入 `waiting`，且 `pending_deployments` 明确显示 `environment=cloud-dev`、`current_user_can_approve=true`、reviewer=`samuelhu324-dev`；approval 提交后 job 才继续执行，这直接证明了 `P3-C1-S1` 的 manual confirmation boundary；
  - 本轮已完整走通 `Checkout -> Bootstrap Git Bash on Windows runners -> Validate self-hosted runner contract -> Record trigger contract -> Validate secret contract -> Prepare SSH identity -> Run cloud release workflow -> Locate summary.json -> Write run summary -> Upload workflow artifacts -> Enforce workflow result`，workflow 结论为 `success`；
  - artifact 中的 `summary.json` 明确记录 `deployResult=PASS`、`verifyResult=FAIL`、`rollbackResult=PASS`、`rollbackTrigger=verify_fail_auto`、`operatorAction=candidate_reverted_to_known_good`、`failureClass=rollback_recovery`、`terminalGate=rollback_readiness_gate`、`result=PASS_AFTER_ROLLBACK`、`evidenceComplete=true`；
  - `verify.log` 明确显示本轮 candidate container 已成功启动并通过 migration / env guard，但由于 verify URL 被故意指向 `http://127.0.0.1:39999/api/v1`，`health_ok` 与 `read_smoke_ok` 以 `(000)` 失败，从而触发了预期中的自动 rollback；
  - `operator_guidance.txt` 已固定输出 rerun / rollback command、artifact 路径以及“keep service on known-good and investigate candidate logs before the next deploy”这类最小 handoff wording，证明 `P3-C1-S2` 已有真实 rollback 样本支撑。

### P1-C2-S1S2 (target repo synced to workflow head before release, remoteHeadSha drift removed | 2026-03-26)

- headSha: `fdd3e812`
- run_url: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23600877818`
- artifacts:
  - `artifacts/_tmp_s4d4b_run_23600877818/s4d-cloud-release-23600877818-1/summary.json`
  - `artifacts/_tmp_s4d4b_run_23600877818/s4d-cloud-release-23600877818-1/preflight.log`
  - `artifacts/_tmp_s4d4b_run_23600877818/s4d-cloud-release-23600877818-1/deploy.log`
  - `artifacts/_tmp_s4d4b_run_23600877818/s4d-cloud-release-23600877818-1/verify.log`
  - `artifacts/_tmp_s4d4b_run_23600877818/s4d-cloud-release-23600877818-1/operator_guidance.txt`
- expected:
  - dispatch workflow 应把 workflow branch/head 作为显式输入传给 release script，而不是只在 `summary.json` 中被动记录漂移后的 `remoteHeadSha`；
  - preflight 应在远端 repo clean 的前提下完成 `git fetch origin <branch>`、branch 对齐与 exact-head sync，使 target 上的 release repo 与 workflow `headSha` 保持一致；
  - 完成 sync 后的真实 PASS 样本应明确证明 `headSha == expectedHeadSha == remoteHeadSha`。
- observed:
  - `.github/workflows/s4d-cloud-release-dispatch.yml` 现已把 `${{ github.ref_name }}` 与 `${{ github.sha }}` 传给 `cloud_release_workflow.sh`，而 `cloud_release_workflow.sh` 在 preflight 中新增了 remote clean-check、`git fetch --quiet origin <branch>`、branch checkout/create 与 `git reset --hard <expected-head-sha>`；
  - validation run `23600877818` 在通过 `cloud-dev` approval gate 后完整走通 `Run cloud release workflow -> Locate summary.json -> Write run summary -> Upload workflow artifacts -> Enforce workflow result`，workflow 结论为 `success`；
  - `summary.json` 明确记录 `headSha=fdd3e812...`、`expectedHeadSha=fdd3e812...`、`remoteHeadSha=fdd3e812...`、`remoteBranch=S4D-cloud-runtime-deploy-verify-rollback`，从而消除了此前 evidence 中长期存在的 target-head drift；
  - `preflight.log` 进一步记录了 `expected_head_sha=fdd3e812...`、`HEAD is now at fdd3e812 ...` 与最终 `remote_head_sha=fdd3e812...`，说明 target repo 已在 release 前被精确同步到 workflow head，而不是延续旧的 `247ded5c...` 状态。

### P1-C3-S1S2 (push/manual concurrency groups split, both trigger surfaces can coexist at approval gate | 2026-03-26)

- headSha: `f9f5e485`
- run_url_push: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23601482418`
- run_url_manual: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23601495526`
- artifacts:
  - `.github/workflows/s4d-cloud-release-dispatch.yml`
  - `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
- expected:
  - 在保留同一 trigger surface + environment 串行保护的前提下，`push` 与 manual `workflow_dispatch` 不应再共享同一个 concurrency group；
  - 当已有 `push` run 因 `cloud-dev` approval 停在 `waiting` 时，新发起的 manual `workflow_dispatch` run 仍应正常 materialize 出 `cloud-runtime-release` job，而不是继续被旧的 waiting run 阻塞在 job 创建之前；
  - 两类 run 最终应各自进入相同的 environment approval gate，从而证明本次修正影响的是控制面排队模型，而不是 deploy/approval 语义本身。
- observed:
  - `.github/workflows/s4d-cloud-release-dispatch.yml` 的 `concurrency.group` 已从仅按 target environment 分组，调整为 `s4d-cloud-release-${{ github.event_name }}-${{ github.event_name == 'workflow_dispatch' && inputs.target_environment || 'cloud-dev' }}`，从而把 `push` 与 `workflow_dispatch` 分离到不同并发槽位；
  - push run `23601482418` 与 manual run `23601495526` 均基于同一 `headSha=f9f5e485...`，且二者都已 materialize 出名为 `cloud-runtime-release` 的独立 job，job `status` 同为 `waiting`，直接证明 manual run 不再因既有 push waiting run 而失去 job materialization；
  - 对 manual run `23601495526` 的 `pending_deployments` 查询明确返回 `environment=cloud-dev`、`current_user_can_approve=true` 与 reviewer=`samuelhu324-dev`，说明 manual run 已正常进入审批门，而不是卡在 concurrency controller 之前；
  - 本轮验证故意没有先取消 push run，因此 `P1-C3-S2` 的结论可直接用于替代此前“先取消 push waiting run，再发 manual drill”这一临时操作规程。

## Recent changes (for traceability, optional)

- 2026-03-26: 已完成 `S4D-4B/P1-C3-S1S2`；workflow concurrency group 现按 `event_name + target_environment` 分槽，真实控制面样本 `23601482418`（push）与 `23601495526`（workflow_dispatch）已证明两类 run 可以并存 materialize 并同时停在 `cloud-dev` approval gate，对应实现提交为 `f9f5e485`。
- 2026-03-26: 已新增 `S4D-4B/P1-C2` 以收口 target repo head drift；workflow 与 release script 现已显式传递 `github.ref_name` / `github.sha` 并在 preflight 阶段完成远端 repo sync，对应提交为 `7bea1d52` 与修正提交 `fdd3e812`；随后真实 PASS 样本 `23600877818` 已证明 `headSha == expectedHeadSha == remoteHeadSha`。
- 2026-03-26: 已为 `.github/workflows/s4d-cloud-release-dispatch.yml` 连续补齐五项实质性 contract 修复：Git Bash shell bootstrap、Windows self-hosted runner pin、bootstrap shell 改为 Windows PowerShell、过严 bash path 校验移除、checked-out repo working-directory / artifact upload path 修正；这些改动分别落在 `18d285c2`、`55f6c06e`、`0d4f260d`、`120032ef`、`7f3c417d`。
- 2026-03-26: 已完成 `S4D-4B/P2-C1-S2` 的第一条真实 `PASS_AFTER_ROLLBACK` 样本 `23599857316`，同时重新证明 `cloud-dev` approval boundary 与 operator handoff artifact contract 可用，因此 `S4D-4B` 现可标记为 `stable`。
- 2026-03-26: 已为 target host 当前出口公网 IP `125.253.50.4/32` 临时补入 cloud-dev RDS inbound allow rule，并据此完成 `S4D-4B/P2-C1-S1` 的第一条真实 GitHub Actions PASS 样本 `23578016775`。
- 2026-03-26: 已完成第一轮真实 GitHub Actions self-hosted dispatch 样本取证；当前 workflow path 已真实走通到 artifact upload，但 PASS 样本仍被 target host -> cloud DB dependency failure 阻塞。
- 2026-03-26: 为使 Windows self-hosted runner 能稳定执行该 workflow，已补齐三项运行时修正：runner 改为稳定 self-hosted 会话、Git `core.longpaths=true`、workflow 默认 shell 改为 Git Bash 短路径 `C:\PROGRA~1\Git\bin\bash.exe`，从而依次清除了 runner 会话冲突、checkout 文件名过长与 shell 解析错误。
- 2026-03-26: 已新增 `.github/workflows/s4d-cloud-release-dispatch.yml`，把 `S4D-4A` 的单入口 release workflow 接入 GitHub Actions `workflow_dispatch`，并补齐 artifact upload 与 run summary contract。
- 2026-03-26: 已把 `S4D-4B` 的 v1 runner boundary 从泛化 hosted/self-hosted 收紧为 self-hosted runner contract；这一步应记为 `P1-C1-S3`，因为它不仅修正文字合同，也改变了实际 workflow 的 `runs-on` 与 runner validation 逻辑。
- 2026-03-25: 创建 `S4D-4B` draft，明确下一阶段不是重写 deploy/rollback 语义，而是把 `S4D-4A` 已稳定的单入口 workflow 接入 GitHub Actions 的 dispatch / approval / artifact upload path。