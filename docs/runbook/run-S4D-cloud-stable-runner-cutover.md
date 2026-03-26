# run-S4D (Cloud Stable Runner Cutover)

---

**id**: `run-S4D-cloud-stable-runner-cutover`
**kind**: `runbook`
**title**: `run/S4D-cloud-stable-runner-cutover`
**status**: `draft`
**scope**: `S4D`
**decision_date**: `2026-03-26`
**context_issue**:
  **DoD**: `S4D-4C/P1-C1-S1 requires a stable self-hosted runner path that no longer depends on temporary public-IP allowlists.`
  **Labs**: ``
**decision**: `Provision a small cloud-dev EC2 host attached to the cloud-dev basic security group, bootstrap a Linux GitHub Actions runner on that host, and use it as the preferred stable dispatch entry for S4D cloud releases.`
  **positive**: `"Stable network path to cloud-dev RDS", "Linux-native bash runner", "Removes dependence on operator public-IP drift"`
  **negative**: `"Adds one more dev/test host", "Still needs repo secrets and registration token handling outside Terraform"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- 给 `S4D-4C/P1-C1-S1` 一条可执行的 stable runner cutover path，而不是继续依赖临时 Windows self-hosted runner。
- 让 cloud release workflow 在 cloud-dev 网络边界内运行，从根上减少 `dependency_connectivity_failure` 和公网 IP 漂移。
- 把 bootstrap、probe、workflow cutover 放进同一条 operator path，便于后续记 evidence。

## 2) What this runbook covers

- `infra/terraform/aws/runner-host/`：创建 stable self-hosted runner host。
- `scripts/ops/cloud_stable_runner_bootstrap.sh`：把 GitHub Actions runner 注册并安装成 Linux service。
- `scripts/ops/cloud_stable_runner_probe.sh`：验证 runner host 对 GitHub、RDS、target host 的 reachability。
- `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml`：stable runner 专用 dispatch workflow。

## 3) Preconditions

- 已有 `cloud-dev` VPC / subnet / `basic_sg_id`。
- 操作者有 AWS CLI / Terraform 权限，以及 GitHub repo 的 runner registration token 权限。
- 理想状态下，target host 已具备 direct SSH entry，不再要求通过 `127.0.0.1:22022` 本地转发才能访问；
- 如果当前 target 仍是 operator 本机上的本地 NAT / 本地转发入口，则在切到 stable-runner workflow 之前，必须先建立一条到 stable runner host 的 reverse tunnel bridge。
- repo secrets 已准备好：
  - `S4D_SSH_PRIVATE_KEY`
  - `S4D_SSH_KNOWN_HOSTS`（可选，但推荐）

## 4) Step 1: Provision the stable runner host

在 `infra/terraform/aws/runner-host/terraform.tfvars` 中至少填这些值：

- `subnet_id`
- `security_group_ids`
  - 这里应传入 cloud-dev basic security group，使 DB SG 可以直接信任这个 host 的 SG，而不是公网 IP。
- `ssh_ingress_cidrs`
- `key_name`

运行：

```powershell
Set-Location d:/Project/wordloom-v3/infra/terraform/aws/runner-host
terraform init
terraform apply -auto-approve
```

预期输出：

- `runner_public_ip`
- `runner_private_ip`
- `runner_ssh_command`

## 5) Step 2: Bootstrap the GitHub runner

在 repo 根运行：

```powershell
bash scripts/ops/cloud_stable_runner_bootstrap.sh \
  --ssh-host <runner_public_ip> \
  --ssh-user ubuntu \
  --ssh-identity-file /c/Users/H/.ssh/id_ed25519 \
  --repo samuelhu324-dev/wordloom-v3 \
  --runner-name wordloom-cloud-dev-runner \
  --runner-labels s4d-cloud,cloud-dev,release
```

预期结果：

- 远端 host 已安装 GitHub Actions runner service；
- artifact 目录下会生成：
  - `remote-bootstrap.log`
  - `bootstrap.json`

## 6) Step 3: Probe the stable network path

在 repo 根运行：

```powershell
bash scripts/ops/cloud_stable_runner_probe.sh \
  --ssh-host <runner_public_ip> \
  --ssh-user ubuntu \
  --ssh-identity-file /c/Users/H/.ssh/id_ed25519 \
  --dependency-host wlv3-cloud-dev-postgres.cbemuq6ky2pw.ap-southeast-2.rds.amazonaws.com \
  --dependency-port 5432 \
  --target-ssh-host <direct_target_host> \
  --target-ssh-port 22
```

预期结果：

- `probe.json` 至少应显示：
  - `githubReachability=PASS`
  - `dependencyTcpReachability=PASS`
  - `runnerListener=PASS`

## 6A) Temporary bridge when the target is still local-only

如果当前 release target 仍是 operator 本机上的本地 VirtualBox / NAT Ubuntu VM，例如通过 `127.0.0.1:22022` 暴露，则先在 operator Windows host 上运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/ops/cloud_target_reverse_tunnel.ps1 \
  -RunnerHost <runner_public_ip> \
  -RunnerUser ubuntu \
  -IdentityFile $HOME/.ssh/id_ed25519 \
  -LocalTargetHost 127.0.0.1 \
  -LocalTargetPort 22022 \
  -RemoteBindHost 127.0.0.1 \
  -RemoteBindPort 22022
```

预期结果：

- stable runner host 本机出现一个新的 `127.0.0.1:22022` 入口；
- 该入口实际回连到 operator Windows host 上已存在的 local target forward；
- 随后 `cloud_stable_runner_probe.sh` 与 `s4d-cloud-release-dispatch-stable-runner` 都可以把 `ssh_host` 继续指向 `127.0.0.1`、`ssh_port` 指向 `22022`，但此时解析位置已经变成 stable runner host 本机，而不再是 GitHub Actions runner 外部无法访问的 operator 公网 IP。

## 7) Step 4: Use the stable-runner workflow

触发 workflow：

- workflow: `s4d-cloud-release-dispatch-stable-runner`
- file: `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml`

关键点：

- 这个 workflow 固定只跑在带标签 `s4d-cloud` 的 Linux self-hosted runner 上；
- 这是 `S4D-4C/P1` 的首选入口；
- 旧的 Windows dispatch workflow 可以暂时保留为 fallback，但不再是主路径。
- 如果当前仍通过 reverse tunnel bridge 暂时承接 local-only target，则 workflow_dispatch 输入应显式使用 `ssh_host=127.0.0.1`、`ssh_port=<RemoteBindPort>`、`ssh_user=wordloom`。
- 注意：GitHub Actions control plane 只会对默认分支 registry 中已注册的 workflow 响应 `workflow_dispatch`；若 `gh workflow run` 返回 “workflow not found on the default branch”，说明当前 blocker 是 workflow registry，而不是 reverse tunnel / target SSH reachability。

## 8) Evidence to keep

- Terraform apply output
- `bootstrap.json`
- `probe.json`
- 首次 stable-runner dispatch 的 GitHub Actions run URL
- 对应 `summary.json`

## 9) Boundaries

- 这份 runbook 解决的是 stable runner network position，不等于自动触发策略；自动触发属于 `S4D-4C/P2`。
- 这份 runbook 也不负责继续扩大 `workflow_dispatch` 的人工流程；真正的“自动触发 + approval”放到下一步做。