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
- P1-C3-S1: 当当前 target 仍是 operator 本机 local-only 入口时，用 reverse tunnel 把该 target bridge 到 stable runner host
- P1-C3-S2: 用 reverse tunnel bridge 把 stable-runner target SSH probe 从 `FAIL` 推进到 `PASS`
- P1-C3-S3: 通过已注册的 stable-runner Actions workflow 采集第一条 reverse-tunnel-backed dispatch evidence

**Current status (S4D-4C / P1)**

- `P1-C1-S1S2` 已完成 repo-side cutover assets：当前仓库已补齐 stable runner host Terraform module、Linux runner bootstrap 脚本、reachability probe 脚本，以及 stable-runner 专用 GitHub Actions workflow；
- 这意味着 `S4D-4C` 的第一个问题不再停留在“建议迁移 runner”，而是已经有可执行的 provision -> bootstrap -> probe -> dispatch 路径；
- `P1-C2-S1` 已完成默认等待窗口收口：release workflow / verify / rollback 的 verify wait 已统一提高到 `180s`，SSH `ConnectTimeout` 已提高到 `30s`，用于降低冷启动误判；
- `P1-C2-S2` 已不再阻塞于 operator ingress：当前 operator host 已恢复到 stable runner `3.27.164.166:22` 的 SSH 连通，Linux stable runner `wordloom-cloud-dev-runner` 已注册并在线，probe 已证明 GitHub / RDS reachability 为 `PASS`；
- 当前 `P1-C2-S2` 的剩余项已进一步收敛：当前 release target 仍是 operator 本机通过 `127.0.0.1:22022` 暴露的 VirtualBox NAT Ubuntu VM，而不是 stable runner 可直接到达的云端 SSH endpoint；因此最后一段 blocker 已从“未知 direct target host”收窄为“target 仍未脱离本地 NAT / 本地转发前提”。
- `P1-C3-S1S2` 已完成：当前 operator host 已通过 reverse tunnel 把本地 `127.0.0.1:22022` bridge 到 stable runner host 的 `127.0.0.1:22022`，并已把 stable-runner target SSH probe 从 `FAIL` 推进到 `PASS`；
- `P1-C3-S3` 已完成第一条 reverse-tunnel-backed stable-runner dispatch evidence，并已进一步完成一次根因修复后的 PASS 复跑：当前 P1 的 runner path / bridge / dispatch / dependency recovery 样本都已具备真实证据。

### P2 (Automation trigger hardening)

- P2-C1-S1: 把 `cloud-dev` 发布入口从纯 `workflow_dispatch` 升级为自动触发
- P2-C1-S2: 保留 GitHub environment approval，但移除“人工手点启动”作为常态前提

**Current status (S4D-4C / P2)**

- `P2-C1-S1S2` 已完成 control-plane 收口：当前 `.github/workflows/s4d-cloud-release-dispatch.yml` 同时支持 `push` 自动触发与 `workflow_dispatch` 手动触发；
- `cloud-dev` environment 已新增 required reviewer protection，因此 auto-dispatch run 会先停在 approval，而不是要求操作者先手点启动 workflow；
- 第一条真实 push-triggered run `23589344188` 已证明自动触发与 approval-only manual boundary 生效；其此前在 approval 后停在 `queued`，根因是 repo 内唯一 Windows self-hosted runner `wordloom-s4d-temp-win` 一度 `offline`；
- 截至本轮恢复动作完成后，`wordloom-s4d-temp-win` 已在当前 Windows operator host 上重新注册并恢复 `online`，因此 auto-dispatch 的 runner availability blocker 也已被收口。

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
- [x] `P1-C2-S2`: stable-runner runtime timeout evidence baseline fixed
- [x] `P1-C3-S1`: reverse tunnel bridge for local-only target fixed
- [x] `P1-C3-S2`: reverse-tunnel-backed stable-runner target probe fixed
- [x] `P1-C3-S3`: reverse-tunnel-backed stable-runner dispatch evidence fixed

### P2 (Automation trigger hardening)

- [x] `P2-C1-S1`: auto-dispatch to cloud-dev prepared
- [x] `P2-C1-S2`: approval-only manual boundary fixed

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

### P1-C2-S2 (stable-runner evidence attempt blocked at operator ingress | 2026-03-26)

- headSha: `f62165d7`
- timeoutFamily: `runtime_dependency_timeout`
- triggerSurface: `stable-runner probe`, `operator -> runner SSH ingress`
- artifacts:
  - `infra/terraform/aws/runner-host/terraform.tfstate`
  - `docs/runbook/run-S4D-cloud-stable-runner-cutover.md`
- expected:
  - 从当前 operator host 连到 stable runner `3.27.164.166`，随后执行 probe / dispatch，拿到真实 stable-runner evidence；
  - 用 probe 结果证明 runner host 对 GitHub、RDS、target SSH 的 reachability 已进入可验证状态。
- observed:
  - 本地 state 已确认 stable runner host outputs：`runner_public_ip=3.27.164.166`、`runner_private_ip=10.42.0.141`；
  - 当前 operator host 以本机默认 SSH key 对 `ubuntu@3.27.164.166:22` 的只读连通测试返回 `connection timed out`；
  - 因此 `P1-C2-S2` 当前 blocker 已收敛为“operator -> stable runner ingress 尚未打通”，还未进入 runner-side probe / dispatch 阶段。

### P1-C2-S2 (operator ingress restored and stable-runner bootstrap/probe PASS | 2026-03-26)

- headSha: `e0eb581a`
- timeoutFamily: `runtime_dependency_timeout`
- triggerSurface: `operator -> runner SSH ingress`, `stable-runner bootstrap`, `stable-runner probe`
- artifacts:
  - `artifacts/_tmp_s4d4c_cloud_runner_bootstrap/20260326T105721Z/bootstrap.json`
  - `artifacts/_tmp_s4d4c_cloud_runner_bootstrap/20260326T105721Z/remote-bootstrap.log`
  - `artifacts/_tmp_s4d4c_cloud_runner_probe/20260326T105909Z/probe.json`
- expected:
  - 当前 operator host 到 stable runner `3.27.164.166:22` 的 SSH ingress 已恢复，不再停留在 `connection timed out`；
  - stable runner host 上的 Linux GitHub Actions runner 已注册为 service 并进入 `online`；
  - probe 至少证明 runner host 对 GitHub、RDS 和本地 listener 健康检查可达。
- observed:
  - 当前 operator 公网 IP 已确认为 `49.196.51.46`，而 runner SSH security group `sg-07929a5f53aec6029` 先前仅允许旧 `/32` `49.196.236.62/32`；补入当前 `/32` 后，对 `3.27.164.166:22` 的 TCP 探测恢复为 `PASS`；
  - 当前 operator host 使用本机 `id_ed25519` 已可执行 `ssh ubuntu@3.27.164.166 hostname`，返回 `ip-10-42-0-141`，说明 operator -> runner ingress 已真实打通；
  - `cloud_stable_runner_bootstrap.sh` 已在远端把 `wordloom-cloud-dev-runner` 注册为 Linux self-hosted runner，并以 systemd service 方式运行；
  - `probe.json` 已记录 `githubReachability=PASS`、`runnerListener=PASS`、`dependencyTcpReachability=PASS`；当前 `targetSshReachability=SKIPPED`，说明 residual gap 已从“runner host 不可达”收窄为“direct target SSH host 尚未显式纳入 probe 参数”。

### P1-C2-S2 (target path remains local VirtualBox NAT, so stable-runner target SSH still FAIL | 2026-03-26)

- headSha: `ad8475b7`
- timeoutFamily: `runtime_dependency_timeout`
- triggerSurface: `stable-runner probe`, `target SSH reachability`, `local NAT forwarding`
- artifacts:
  - `artifacts/_tmp_s4d4c_cloud_runner_probe/20260326T110703Z/probe.json`
- expected:
  - 当 stable runner network path 已恢复后，若当前 release target 已具备 direct SSH entry，则从 stable runner 对 target SSH 的 TCP reachability 应为 `PASS`；
  - 若 target 仍只是 operator 本地转发入口，则该 probe 应显式暴露为 `FAIL`，而不是继续把问题记成“runner host 自身超时”。
- observed:
  - 当前 operator host 的 `127.0.0.1:22022` listener 由 `VirtualBoxVM.exe` 持有；通过该入口登录后，目标主机 hostname 为 `wordloom-ubuntu`，网卡地址为 `10.0.2.15/24`，属于典型 VirtualBox NAT guest；
  - 同一主机已确认存在 `/home/wordloom/work/wordloom-v3`、`/etc/wordloom/.env.cloud.dev` 与 Docker runtime，说明这就是当前实际 release target，而不是一台额外的云端 Ubuntu VM；
  - 从 stable runner 对当前 operator 公网 IP `49.196.51.46:22022` 的 probe 已返回 `targetSshReachability=FAIL`；因此当前 residual blocker 已被明确固定为：release target 仍依赖 operator 本机的本地 NAT / 端口转发入口，而 stable runner 只能稳定替代“runner 位置”和“RDS allowlist 漂移”问题，无法自动穿透这一类本地 VirtualBox NAT 前提。

### P1-C3-S1S2 (reverse tunnel bridge established and stable-runner target probe restored | 2026-03-26)

- headSha: `273952be`
- timeoutFamily: `runtime_dependency_timeout`
- triggerSurface: `reverse tunnel bridge`, `stable-runner probe`, `local NAT target bridge`
- artifacts:
  - `scripts/ops/cloud_target_reverse_tunnel.ps1`
  - `artifacts/_tmp_s4d4c_cloud_runner_probe/20260326T111822Z/probe.json`
  - `docs/runbook/run-S4D-cloud-stable-runner-cutover.md`
- expected:
  - 当当前 release target 仍只有 operator 本机上的 `127.0.0.1:22022` local forward 时，operator 应能把这条入口反向桥接到 stable runner host；
  - stable runner host 上的本机端口应出现可用的 target SSH 入口，并让 probe 的 `targetSshReachability` 从 `FAIL` 恢复为 `PASS`。
- observed:
  - 已新增 `scripts/ops/cloud_target_reverse_tunnel.ps1`，用于从 operator Windows host 直接建立 `ssh -R 127.0.0.1:22022:127.0.0.1:22022 ubuntu@3.27.164.166` 风格的 reverse tunnel bridge；
  - runner host `sshd -T` 已确认 `allowtcpforwarding yes`、`permitopen any`，因此可接受这一类 reverse port forward；
  - 在 reverse tunnel 存活期间，从 stable runner 对 `127.0.0.1:22022` 的 probe 已返回 `targetSshReachability=PASS`，并且 runner host 上的 `127.0.0.1:22022` 原始 TCP 检测同样为 `PASS`；
  - 因此当前 residual gap 已从“stable runner 打不到 target”收窄为“stable-runner Actions workflow 尚未在默认分支 registry 中注册”。

### P1-C3-S3 (stable-runner dispatch still blocked by workflow registration gap | 2026-03-26)

- headSha: `273952be`
- timeoutFamily: `runtime_dependency_timeout`
- triggerSurface: `workflow_dispatch`, `stable-runner control plane`
- artifacts:
  - `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml`
- expected:
  - reverse tunnel bridge 打通后，应能直接通过 `workflow_dispatch` 触发 `s4d-cloud-release-dispatch-stable-runner`，并把 `ssh_host=127.0.0.1`、`ssh_port=22022` 作为 stable-runner 本机 target 入口；
  - 由此采集第一条 reverse-tunnel-backed stable-runner dispatch evidence。
- observed:
  - 当前 GitHub repo 的 registered workflow 列表中尚未出现 `s4d-cloud-release-dispatch-stable-runner`；
  - `gh workflow run s4d-cloud-release-dispatch-stable-runner.yml` 返回 `HTTP 404: workflow ... not found on the default branch`；
  - 因此当前 blocker 已不再是 reverse tunnel 或 target reachability，而是 control-plane registry 仍以默认分支 `main` 为准，当前 stable-runner workflow 文件尚未进入该 registry。

### P1-C3-S3 (first reverse-tunnel-backed stable-runner dispatch evidence captured | 2026-03-26)

- headSha: `562974d6`
- timeoutFamily: `runtime_dependency_timeout`
- triggerSurface: `workflow_dispatch`, `stable-runner dispatch`, `reverse tunnel bridge`
- runUrl: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23592172058`
- artifacts:
  - `artifacts/_tmp_s4d4c_stable_runner_run_23592172058/s4d-cloud-release-stable-runner-23592172058-1/summary.json`
  - `artifacts/_tmp_s4d4c_stable_runner_run_23592172058/s4d-cloud-release-stable-runner-23592172058-1/verify.log`
  - `artifacts/_tmp_s4d4c_stable_runner_run_23592172058/s4d-cloud-release-stable-runner-23592172058-1/operator_guidance.txt`
- expected:
  - stable-runner workflow 进入默认分支 registry 后，应能以 `ssh_host=127.0.0.1`、`ssh_port=22022`、`ssh_user=wordloom` 成功触发第一条 reverse-tunnel-backed dispatch；
  - 当前样本至少应证明 control-plane、stable runner contract、target reachability 与 deploy execution 已真实走通，不再停留在“workflow 404”或“target SSH 不通”。
- observed:
  - `s4d-cloud-release-dispatch-stable-runner` 现已进入 GitHub 默认分支 registry，并成功以 `workflow_dispatch` 方式启动 run `23592172058`；
  - 该 run 已通过 environment approval，并在 stable runner 上真实执行；`preflightResult=PASS`、`deployResult=PASS`、`targetReachabilityGate=PASS`；
  - 终态为 `verifyResult=FAIL`、`terminalGate=dependency_connectivity_gate`、`failureClass=dependency_connectivity_failure`，说明当前新的真实 blocker 已收口为 target runtime 在数据库迁移阶段连接 cloud-dev RDS 失败，而不是 runner / reverse tunnel / workflow registry；
  - `verify.log` 已记录容器启动后在 Alembic migration 阶段抛出 `psycopg.OperationalError`，签名为 `connection to server at "13.211.43.32", port 5432 failed: server closed the connection unexpectedly`；
  - `summary.json` 同时保留一个残余差异：当前 `remoteHeadSha=b3002d071d08f748ea438883914c876238af440f`，仍未与本次触发所用的 `headSha=b63cb3d0451bc8e06b30e95a2ceec7038b79a3c7` 收口到同一版本。

### P1-C3-S3 (dependency connectivity and head drift fixed; stable-runner dispatch PASS | 2026-03-26)

- headSha: `00353942`
- timeoutFamily: `runtime_dependency_timeout`
- triggerSurface: `workflow_dispatch`, `stable-runner dispatch`, `dependency recovery rerun`
- runUrl: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23595354059`
- artifacts:
  - `artifacts/_tmp_s4d4c_stable_runner_run_23595354059/s4d-cloud-release-stable-runner-23595354059-1/summary.json`
  - `artifacts/_tmp_s4d4c_stable_runner_run_23595354059/s4d-cloud-release-stable-runner-23595354059-1/preflight.log`
  - `artifacts/_tmp_s4d4c_stable_runner_run_23595354059/s4d-cloud-release-stable-runner-23595354059-1/verify.log`
- expected:
  - 在第一次 reverse-tunnel-backed dispatch 样本暴露 `dependency_connectivity_failure` 和 `remoteHeadSha` 漂移后，应能先从 target VM 上完成最小诊断，再修复 RDS allowlist 与 target repo HEAD，随后复跑 stable-runner dispatch 并把结果推进到 `PASS`；
  - PASS 样本应同时证明：dependency gate 恢复、post-change verify 恢复，以及 target host 实际运行版本与触发版本一致。
- observed:
  - 当前 target VM 上已确认实际公网出口 IP 为 `49.196.51.46`，而 cloud-dev RDS security group `sg-0873e947b9947639d` 在第一次 FAIL 样本前并未包含该 `/32`；这说明第一次 FAIL 的主根因是 target egress IP 漂移后未被 allowlist 覆盖；
  - 已为 `sg-0873e947b9947639d` 补入 `49.196.51.46/32` 的 `5432/TCP` allow rule，并把 target VM 上的 `/home/wordloom/work/wordloom-v3` 快进到 `origin/S4D-cloud-runtime-deploy-verify-rollback`；
  - 复跑 run `23595354059` 后，`summary.json` 已记录 `result=PASS`、`failureClass=none`、`dependencyConnectivityGate=PASS`、`postChangeVerifyGate=PASS`；
  - `preflight.log` 与 `summary.json` 已同时确认 `remoteHeadSha=0035394235c3fdfe905ac780c322987cf988eced`，说明这次 trigger SHA 与 target runtime HEAD 已收口一致；
  - `verify.log` 已记录 `container_running OK`、`migration_ok OK`、`health_ok OK (200)`、`read_smoke_ok OK (200 list payload)`，因此当前 stable-runner reverse-tunnel path 已取得第一条真实 PASS 样本。

### P2-C1-S1S2 (auto-dispatch and approval-only boundary proven | 2026-03-26)

- headSha: `f62165d7f93243dd8001aee80d3836f9d80ddd40`
- timeoutFamily: `runtime_dependency_timeout`
- triggerSurface: `auto-dispatch`, `push`, `cloud-dev environment approval`
- runUrl: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/23589344188`
- artifacts:
  - `.github/workflows/s4d-cloud-release-dispatch.yml`
  - `cloud-dev` GitHub Actions environment configuration
- expected:
  - 向 `S4D-cloud-runtime-deploy-verify-rollback` 分支推送 release-related 变更后，`cloud-dev` release workflow 不再要求人工先手点 `workflow_dispatch`；
  - 人工只保留 `cloud-dev` environment approval 这一条手动边界。
- observed:
  - push `f62165d7` 后，workflow `s4d-cloud-release-dispatch` 自动生成 run `23589344188`，事件类型为 `push`；
  - 在未审批前，该 run 状态为 `waiting`，说明当前手动边界已从“手点 workflow_dispatch”收口为 environment approval；
  - 审批 `cloud-dev` deployment 后，该 run 继续进入 `queued`，当前剩余 blocker 是 repo 内唯一 self-hosted runner `wordloom-s4d-temp-win` 处于 `offline`，而不是 auto-dispatch / approval contract 本身。

### P2-C1-S1S2 (windows self-hosted runner availability restored | 2026-03-26)

- headSha: `e0eb581a`
- timeoutFamily: `runtime_dependency_timeout`
- triggerSurface: `auto-dispatch runner scheduling`, `self-hosted runner recovery`
- artifacts:
  - `D:/actions-runner/wordloom-s4d-temp-win/.runner`
- expected:
  - 先前卡在 `queued` 的 Windows self-hosted dispatch path 不再因 repo 内无可用 runner 而挂起；
  - `wordloom-s4d-temp-win` 应恢复为 `online`，继续承担旧 Windows dispatch workflow 的 fallback 入口。
- observed:
  - 当前 Windows operator host 已完成 `wordloom-s4d-temp-win` 的同名替换注册，并重新启动 `run.cmd` listener；
  - GitHub repo runner inventory 已显示 `wordloom-s4d-temp-win` 从 `offline` 恢复为 `online`；
  - 因此 `P2` 之前暴露的 runner availability blocker 已被关闭，后续 auto-dispatch run 不再缺少 Windows 落点。

## Recent changes (for traceability, optional)

- 2026-03-26: 已完成 `S4D-4C/P1-C1-S1S2` 的 repo-side 交付：新增 stable runner host Terraform module、bootstrap/probe 脚本、stable-runner workflow 与 cutover runbook，使“迁移 self-hosted runner 到稳定网络位置”从建议变成可执行路径。
- 2026-03-26: 已完成 `S4D-4C/P1-C2-S1` 的默认等待窗口收口：`cloud_release_workflow.sh`、`cloud_release_verify.sh`、`cloud_release_rollback.sh` 与 stable-runner workflow 已统一提高 verify wait baseline，并把 SSH preflight timeout 提高到更适合云端冷启动的范围。
- 2026-03-26: 已完成 `S4D-4C/P2-C1-S1S2` 的 control-plane 收口：`s4d-cloud-release-dispatch.yml` 已支持 push 自动触发，`cloud-dev` environment 已新增 required reviewer protection；第一条真实 push-triggered run `23589344188` 已证明 auto-dispatch 与 approval-only manual boundary 生效。
- 2026-03-26: 已尝试执行 `S4D-4C/P1-C2-S2` 的 stable-runner evidence capture；当前 blocker 已收敛为 operator host 到 stable runner `3.27.164.166:22` 的 SSH ingress timeout，因此 runner-side probe / dispatch evidence 仍待后续补齐。
- 2026-03-26: 已恢复 repo Windows self-hosted runner `wordloom-s4d-temp-win` 在线状态，并关闭 auto-dispatch 的 runner availability blocker。
- 2026-03-26: 已补入当前 operator `/32` 到 stable runner SSH ingress，完成 `wordloom-cloud-dev-runner` 的 Linux service bootstrap，并拿到 GitHub / RDS / runner listener 的 probe PASS；当前 residual gap 只剩 direct target SSH host 尚未显式纳入 probe 参数。
- 2026-03-26: 已进一步确认当前 release target 并非 stable runner 可直接访问的云端 SSH endpoint，而是当前 operator Windows 主机上由 `VirtualBoxVM.exe` 持有 `127.0.0.1:22022` 转发的本地 NAT Ubuntu VM；从 stable runner 对当前 operator 公网 IP `49.196.51.46:22022` 的 probe 已显式返回 `FAIL`。
- 2026-03-26: 已新增 reverse tunnel bridge 脚本 `scripts/ops/cloud_target_reverse_tunnel.ps1`，并把当前 local-only target 的 `127.0.0.1:22022` 反向桥接到 stable runner host；随后 stable-runner probe 已把 `targetSshReachability` 从 `FAIL` 推进到 `PASS`。
- 2026-03-26: `s4d-cloud-release-dispatch-stable-runner.yml` 已进入 GitHub 默认分支 registry，并已取得第一条 reverse-tunnel-backed stable-runner dispatch evidence `23592172058`；当前新的真实 blocker 已收口为 target runtime 的 `dependency_connectivity_failure`，而非 workflow registry / reverse tunnel。
- 2026-03-26: 已从 target VM 本身完成最小 RDS 依赖诊断，确认当前出口 IP 为 `49.196.51.46`，并据此把该 `/32` 补入 cloud-dev RDS security group `sg-0873e947b9947639d`；同时已把 target repo HEAD 快进到 `0035394235c3fdfe905ac780c322987cf988eced`。
- 2026-03-26: 已完成 reverse-tunnel-backed stable-runner PASS 复跑 `23595354059`，当前 `dependencyConnectivityGate=PASS`、`postChangeVerifyGate=PASS`，且 trigger SHA 与 remote HEAD 已一致。
- 2026-03-26: 新增 `S4D-4C`，把最近频发的 408/timeout 问题正式从 `S4D-4B` 之后拆成独立治理 phase，并固定优先顺序为“稳定 runner 网络位置 -> 自动触发到 cloud-dev -> 大入口文件减压”。