# log-S4D-4B (Phase 4B: GitHub Actions Release Dispatch)

---

**id**: `S4D-4B`
**kind**: `log`
**title**: `cloud runtime release workflow via GitHub Actions dispatch (approval-ready runner entry, evidence upload, operator handoff) + drills/evidence v1`
**status**: `draft`
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

**Current status (S4D-4B)**

- `P0-C1-S1` 已完成第一版 Actions trigger contract：当前已固定 `workflow_dispatch` 输入集合，覆盖 SSH target、release inputs、runtime inputs、rollback toggle 与 verify tuning。
- `P0-C1-S2` 已完成第一版 runner/secret contract：当前使用 `S4D_SSH_PRIVATE_KEY` 作为 required secret，`S4D_SSH_KNOWN_HOSTS` 作为 optional secret，并已确认 repo 可创建 `cloud-dev` environment 与 self-hosted runner registration token。
- `P0-C1-S3` 已完成第一版 evidence/run-summary contract：当前 workflow 会上传整个 artifact 目录，并把 `result`、`failureClass`、`terminalGate`、`terminalStage`、`operatorAction`、`evidenceComplete` 与 gate results 写入 `GITHUB_STEP_SUMMARY`。
- `P1-C1-S1` 与 `P1-C1-S2` 已完成第一版落地：仓库现已新增 `.github/workflows/s4d-cloud-release-dispatch.yml`，直接复用 `cloud_release_workflow.sh` 作为 runner entry。
- `P1-C1-S3` 已完成：当前 workflow 已收紧为 `runs-on: self-hosted`，并显式验证 self-hosted runner 的 bash/git/ssh contract，不再维持对 GitHub-hosted runner 的模糊兼容假设。
- `P2-C1-S1` 当前转入执行中；第一轮真实 dispatch evidence 将直接围绕“本机 self-hosted runner -> 127.0.0.1:22022 target -> PASS artifact bundle”来取证。

### P2 (Drill / Verify)

- P2-C1-S1: 执行第一轮 Actions-triggered deploy -> verify 样本
- P2-C1-S2: 执行第一轮 Actions-triggered verify FAIL -> rollback PASS_AFTER_ROLLBACK 样本

### P3 (Approvals / Handoff)

- P3-C1-S1: 固定 environment approval / manual confirmation 的最小边界
- P3-C1-S2: 固定 run summary 到 operator handoff 的最小 wording 与 artifact path

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: Actions trigger contract fixed
- [x] `P0-C1-S2`: runner and secret contract fixed
- [x] `P0-C1-S3`: evidence upload and run-summary contract fixed

### P1 (Implementation / workflow)

- [x] `P1-C1-S1`: workflow_dispatch entry prepared
- [x] `P1-C1-S2`: artifact upload and run summary prepared
- [x] `P1-C1-S3`: self-hosted runner v1 contract aligned with current SSH target

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: first Actions-triggered PASS sample recorded
- [ ] `P2-C1-S2`: first Actions-triggered PASS_AFTER_ROLLBACK sample recorded

### P3 (Approvals / Handoff)

- [ ] `P3-C1-S1`: environment approval boundary fixed
- [ ] `P3-C1-S2`: operator handoff summary fixed

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

## Recent changes (for traceability, optional)

- 2026-03-26: 已新增 `.github/workflows/s4d-cloud-release-dispatch.yml`，把 `S4D-4A` 的单入口 release workflow 接入 GitHub Actions `workflow_dispatch`，并补齐 artifact upload 与 run summary contract。
- 2026-03-26: 已把 `S4D-4B` 的 v1 runner boundary 从泛化 hosted/self-hosted 收紧为 self-hosted runner contract；这一步应记为 `P1-C1-S3`，因为它不仅修正文字合同，也改变了实际 workflow 的 `runs-on` 与 runner validation 逻辑。
- 2026-03-25: 创建 `S4D-4B` draft，明确下一阶段不是重写 deploy/rollback 语义，而是把 `S4D-4A` 已稳定的单入口 workflow 接入 GitHub Actions 的 dispatch / approval / artifact upload path。