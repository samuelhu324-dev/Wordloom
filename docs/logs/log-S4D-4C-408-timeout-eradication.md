# log-S4D-4C (Phase 4C: 408 Timeout Eradication)

---

**id**: `S4D-4C`
**kind**: `log`
**title**: `408 timeout eradication (timeout taxonomy, stable runner network path, controlled auto-dispatch, large-entrypoint reduction) + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, ReleaseOperations, Automation, Timeout, Evidence, epic/s4, sub/4c`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **parent_log**: `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  **previous_log**: `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
  **reference_log_1**: `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
  **reference_log_2**: `docs/logs/log-S0C-3A-cli-breakdown.md`
  **reference_log_3**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_4**: `docs/runbook/run-S4D-cloud-stable-runner-cutover.md`
**created**: `2026-03-26`
**updated**: `2026-03-26`

---

## Decision / Outcome

**Decision**:

- `S4D-4C` 专门承接最近频发的“408 / timeout 类问题”治理，但第一原则是不再把不同来源的 timeout 混成一个问题；
- v1 先把当前已确认的两大问题族分开处理：一类是 `Agent/Copilot` 侧的上下文膨胀 / 请求超时，一类是 cloud runtime release path 上的真实依赖连通性 / 调度等待超时；
- 本 phase 的目标不是继续手工补洞，而是把 `S4D-4B` 暴露出的不稳定前提收口成更稳的网络位置、更少人工 dispatch、更薄的大入口文件。

**Default choices (phase defaults / v1)**:

- `408` v1 明确拆成两条治理线：
  - `ops/runtime timeout family`：target host / runner / dependency / workflow wait 超时；
  - `agent/context timeout family`：超大入口文件、过宽检索面导致的上下文膨胀和交互超时；
- cloud release path 优先解决“根因级”不稳定项，而不是继续依赖公网出口 IP 白名单漂移这种脆弱前提；
- GitHub Actions v1.5 的目标是“自动触发到 `cloud-dev` + 人工仅保留 approval”，而不是长期停留在纯 `workflow_dispatch` 手工触发；
- developer-efficiency 侧优先继续治理大入口文件与高扇出上下文入口，避免 Copilot/Agent 在 drill/workflow 问题上再次拉爆上下文。

## Definitions

- **Agent/context 408**：Copilot Chat/Agent 因读取超大入口文件、检索面过宽或请求体过大而出现的交互超时。
- **Runtime/dependency timeout**：release workflow 在 target host、database、network、SSH 或 workflow wait 阶段遇到的真实运行时超时。
- **Stable runner network path**：runner 所在网络位置对 target host、RDS、GitHub Actions 都是稳定可达的，不依赖临时公网 IP 漂移。
- **Controlled auto-dispatch**：自动触发发布流程，但仍通过 GitHub environment approval 控制进入更高风险步骤。
- **Public-IP drift**：runner 或 target host 的公网出口变化，导致先前 allowlist 失效，进而触发 `dependency_connectivity_failure` 或超时。

## Constraints

- 不能把所有 timeout 都重命名成 `408` 后统一处理；分类必须能落到明确 owner、脚本、网络边界和证据；
- 不把 SSH key、数据库 secrets、allowlist 明细直接写入仓库；
- 不以“继续手动运行 workflow_dispatch”作为长期解法；
- 不把大入口文件治理降级成一次性风格整理，必须保留行为与 evidence contract 稳定。

## Scope

- `P0`: contract（408 taxonomy、problem statement、evidence contract、优先级边界）
- `P1`: infra/network hardening（stable self-hosted runner 位置、RDS reachability、去除公网 IP 漂移依赖）
- `P2`: automation trigger hardening（从手工 dispatch 升级到自动触发 + approval 保留）
- `P3`: agent/context pressure reduction（继续治理大入口文件、缩小高频检索面、降低 Copilot/Agent 408 频率）

## Success Criteria (DoD)

- 文档层面已经明确区分至少两类 timeout/408 家族，避免后续排障继续混淆；
- `S4D-4B` 当前依赖的 self-hosted runner 路径不再以“临时公网 IP allowlist”作为默认前提，或已明确替换为更稳定的网络路径；
- `cloud-dev` 发布入口不再要求人工手动点击 `workflow_dispatch` 才能启动，人工仅保留 approval 或更高风险边界；
- 至少一项 developer-efficiency 治理动作被固定为 `S4D-4C` 的正式交付物，用于降低 Agent/Copilot 上下文 408 频率；
- 后续 evidence 能区分“runtime timeout 已消除”和“agent/context timeout 已缓解”两条结果，而不是只记录“这次没报错”。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 taxonomy、网络收口、自动触发边界和上下文减压动作都已至少完成一轮有证据的落地；
  - Evidence 区至少包含一条 runtime timeout family 的改善样本，以及一条 agent/context family 的改善样本或结构性收口证据。

## P0 (Contract | v1)

### P0-C1-S1 (408 taxonomy contract | v1)

- `S4D-4C` v1 明确只承接以下两类问题：
  - `agent_context_timeout`：大入口文件、检索范围过宽、上下文载荷过大导致的 Agent/Copilot 请求超时；
  - `runtime_dependency_timeout`：SSH reachability、DB connectivity、workflow wait、service readiness 导致的真实运行时超时；
- 任何新出现的“408”都必须先归类，再决定进入 `S4D-4C/P1-P3` 的哪个 cycle；
- 不接受“408 原因未知，先继续手跑”作为默认处理方式。

### P0-C1-S2 (priority and treatment contract | v1)

- 当前优先级按根因收益排序固定为：
  - 第一优先：把 self-hosted runner 移到稳定网络位置，消除 target host / RDS 依赖公网出口漂移；
  - 第二优先：把当前 `workflow_dispatch` 升级为自动触发到 `cloud-dev`，人工仅保留 approval；
  - 第三优先：持续治理大入口文件和高扇出上下文入口，减少 Agent/Copilot 408；
- `S4D-4B` 后续 drill 不应与 `S4D-4C` 抢优先级；凡是触及 timeout 根因治理的工作，优先记入 `S4D-4C`。

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON / log 记账至少要包含：
  - timeout family：`agent_context_timeout` 或 `runtime_dependency_timeout`
  - trigger surface：例如 `workflow_dispatch`、auto-dispatch、CLI/Agent 检索、target-host verify
  - before/after baseline：例如 allowlist 漂移前后、手工触发前后、入口文件拆分前后
  - output artifact / run URL / headSha
  - final decision：`PASS`、`PASS_WITH_APPROVAL`、`FAIL`、`MITIGATED`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4D-4C/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`）或同一 phase / cycle 下连续 steps 的组合（如 `1S2`）。

**Branch convention**:

- `S4D-4C` 相关实现与文档优先继续落在 `S4D-cloud-runtime-deploy-verify-rollback` 分支，除非后续需要拆出专门的 timeout-hardening 子分支。

**Commit discipline (recommended)**:

- 每完成一个明确的根因治理单元，应尽量及时 `commit/push`，并把证据同步挂回本 log，而不是只散落在 terminal history 或临时 artifacts。

## Plan (draft)

### P1 (Infra / network hardening)

- P1-C1-S1: 固定 self-hosted runner 的稳定网络位置，使其对 target host / RDS 可达且不依赖临时公网出口 allowlist
- P1-C1-S2: 为 stable-runner 路径补齐 repo-side cutover assets（Terraform module、bootstrap/probe 脚本、stable-runner workflow、runbook）
- P1-C2-S1: 为 runtime timeout family 固定 release readiness / SSH wait baseline，避免把冷启动、镜像拉取、迁移等待误判成 workflow timeout
- P1-C2-S2: 采集真实 stable-runner probe / dispatch evidence，证明新 runner host 已替代临时公网 IP allowlist 路径

**Current status (S4D-4C / P1)**

- `P1-C1-S1S2` 已完成 repo-side cutover assets：当前仓库已补齐 stable runner host Terraform module、Linux runner bootstrap 脚本、reachability probe 脚本，以及 stable-runner 专用 GitHub Actions workflow；
- 这意味着 `S4D-4C` 的第一个问题不再停留在“建议迁移 runner”，而是已经有可执行的 provision -> bootstrap -> probe -> dispatch 路径；
- `P1-C2-S1` 已完成默认等待窗口收口：release workflow / verify / rollback 的 verify wait 已统一提高到 `180s`，SSH `ConnectTimeout` 已提高到 `30s`，用于降低冷启动误判；
- `P1-C2-S2` 仍待完成真实 probe/evidence 入账，用于证明新 runner host 已真实替代临时公网 IP allowlist 路径。

### P2 (Automation trigger hardening)

- P2-C1-S1: 把 `cloud-dev` 发布入口从纯 `workflow_dispatch` 升级为自动触发
- P2-C1-S2: 保留 GitHub environment approval，但移除“人工手点启动”作为常态前提

### P3 (Agent/context pressure reduction)

- P3-C1-S1: 识别并继续治理高频大入口文件 / 高扇出检索入口
- P3-C1-S2: 为后续 drill/workflow/cli 文档与入口建立更窄的索引面，减少 Agent/Copilot 上下文装载压力

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: 408 taxonomy fixed
- [x] `P0-C1-S2`: priority and treatment contract fixed
- [x] `P0-C1-S3`: evidence contract fixed

### P1 (Infra / network hardening)

- [x] `P1-C1-S1`: stable runner network path fixed
- [x] `P1-C1-S2`: stable runner repo-side cutover assets fixed
- [x] `P1-C2-S1`: runtime readiness / SSH wait baseline fixed
- [ ] `P1-C2-S2`: stable-runner runtime timeout evidence baseline fixed

### P2 (Automation trigger hardening)

- [ ] `P2-C1-S1`: auto-dispatch to cloud-dev prepared
- [ ] `P2-C1-S2`: approval-only manual boundary fixed

### P3 (Agent/context pressure reduction)

- [ ] `P3-C1-S1`: high-pressure entrypoints identified and sequenced
- [ ] `P3-C1-S2`: reduced-context guidance / indexing fixed

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, timeout family, key parameters, and artifact paths (or CI run URLs).

### P0-C1-S1S2S3 (408 taxonomy and treatment priority formalized | 2026-03-26)

- headSha: `38b3e4b5`
- artifacts:
  - `docs/logs/log-S4D-4C-408-timeout-eradication.md`
  - `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
- expected:
  - 明确把“最近大量 408”从单一模糊抱怨收口为可执行的问题分层；
  - 记录当前最优后续路线：稳定 runner 网络位置、自动触发到 `cloud-dev`、继续治理大入口文件；
  - 使 `S4D-4C` 成为 `S4D` 当前优先 phase，而不是零散结论。
- observed:
  - 已把 408 问题正式拆成 `agent_context_timeout` 与 `runtime_dependency_timeout` 两个 family；
  - 已把优先级固定为“稳定 runner 网络位置 -> 自动触发 + approval -> 大入口文件减压”；
  - 已把 `S4D-4C` 明确挂入 `S4D` spine，作为当前优先处理的 timeout eradication phase。

### Reference evidence (already observed before opening this phase)

- `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
  - 已证明 `S4D-4B` 的 Actions chain 本身可以 PASS；此前真实 blocker 是 target host 到 RDS 的 `dependency_connectivity_failure`，其恢复动作是临时补入当前出口 IP `125.253.50.4/32`。
- `docs/logs/log-S0C-3A-cli-breakdown.md`
  - 已明确记录超大 `backend/scripts/cli.py` 会导致 Copilot/Agent 侧上下文膨胀与 408 风险，因此 agent/context timeout family 不是猜测，而是仓库中已有问题陈述。
- `scripts/ops/cloud_release_workflow.sh`
  - 已有明确 failure taxonomy，把 `timeout expired`、`connection timed out`、`network is unreachable` 等签名收口为 runtime/dependency 或 target reachability failure。

### P1-C1-S1 (stable runner cutover assets prepared | 2026-03-26)

- headSha: `38b3e4b5d9dbd7c1df8c0051a4869a2bdcb75e86`
- artifacts:
  - `infra/terraform/aws/runner-host/main.tf`
  - `infra/terraform/aws/runner-host/terraform.tfvars.example`
  - `scripts/ops/cloud_stable_runner_bootstrap.sh`
  - `scripts/ops/cloud_stable_runner_probe.sh`
  - `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml`
  - `docs/runbook/run-S4D-cloud-stable-runner-cutover.md`
- expected:
  - 仓库内出现一条不再依赖临时 Windows self-hosted runner 的 stable cloud runner cutover path；
  - stable runner host 应能以 cloud-dev security group 身份访问 RDS，而不是继续依赖公网 IP allowlist 漂移；
  - operator 应能按 runbook 完成 provision、bootstrap、probe 与 stable-runner dispatch。
- observed:
  - 已新增 `runner-host` Terraform module，用于把 stable runner host 放进 cloud-dev 网络和基础 SG；
  - 已新增 runner bootstrap / probe 脚本，用于把 GitHub Actions runner 注册到 Linux host 并验证 GitHub、RDS、target SSH 三条 reachability；
  - 已新增 stable-runner 专用 dispatch workflow，后续切换后可避免继续依赖 Windows-specific runner shell contract。

### P1-C2-S1 (runtime readiness and SSH timeout baseline hardened | 2026-03-26)

- headSha: `pending-next-commit`
- timeoutFamily: `runtime_dependency_timeout`
- triggerSurface: `stable-runner dispatch`, `target-host verify`, `release workflow preflight`
- before:
  - `cloud_release_workflow.sh` 默认 `verify_max_wait_seconds=45`，SSH `ConnectTimeout=10`；
  - `cloud_release_verify.sh` 与 `cloud_release_rollback.sh` 默认也沿用 `45s` verify wait；
  - 对冷启动、镜像首次拉取、迁移或 cloud-init 后首轮服务启动不够宽松，容易把“正常慢路径”误记为 timeout。
- after:
  - `cloud_release_workflow.sh` 默认 `verify_max_wait_seconds=180`，SSH `ConnectTimeout=30`；
  - `cloud_release_verify.sh` 与 `cloud_release_rollback.sh` 默认 verify wait 统一为 `180s`；
  - stable-runner workflow 输入默认值同步提高到 `180s`，使 workflow 层和脚本层 baseline 一致。
- artifacts:
  - `scripts/ops/cloud_release_workflow.sh`
  - `scripts/ops/cloud_release_verify.sh`
  - `scripts/ops/cloud_release_rollback.sh`
  - `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml`
- expected:
  - 减少把冷启动、镜像拉取、迁移等待误判成 runtime timeout；
  - 让 stable-runner release path 的 workflow 输入默认值与脚本默认值保持一致；
  - 为后续真实 probe / dispatch evidence 提供更合理的 readiness baseline。
- observed:
  - release workflow、verify、rollback 三层默认 verify wait 已统一抬高到 `180s`；
  - SSH preflight 的连接超时已从 `10s` 提高到 `30s`；
  - 当前这一步解决的是 baseline hardening，不等于已拿到真实 stable-runner PASS evidence。

## Recent changes (for traceability, optional)

- 2026-03-26: 已完成 `S4D-4C/P1-C1-S1S2` 的 repo-side 交付：新增 stable runner host Terraform module、bootstrap/probe 脚本、stable-runner workflow 与 cutover runbook，使“迁移 self-hosted runner 到稳定网络位置”从建议变成可执行路径。
- 2026-03-26: 已完成 `S4D-4C/P1-C2-S1` 的默认等待窗口收口：`cloud_release_workflow.sh`、`cloud_release_verify.sh`、`cloud_release_rollback.sh` 与 stable-runner workflow 已统一提高 verify wait baseline，并把 SSH preflight timeout 提高到更适合云端冷启动的范围。
- 2026-03-26: 新增 `S4D-4C`，把最近频发的 408/timeout 问题正式从 `S4D-4B` 之后拆成独立治理 phase，并固定优先顺序为“稳定 runner 网络位置 -> 自动触发到 cloud-dev -> 大入口文件减压”。