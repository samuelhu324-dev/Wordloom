# log-S4D-3A (Phase 3: Cloud Runtime Rollback Sample)

---

**id**: `S4D-3A`
**kind**: `log`
**title**: `cloud runtime rollback sample (known-good image/tag, rollback helper, repeatable VM recovery evidence) + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, Rollback, Recovery, ReleaseOperations, Drills, Evidence, epic/s4, sub/3a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  **previous_log**: `docs/logs/log-S4D-2A-post-change-verification-and-operational-checks.md`
  **reference_log_1**: `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`
  **reference_log_2**: `docs/logs/log-S4D-1A-cloud-runtime-release-path.md`
  **reference_log_3**: `docs/logs/_template-log-phase-drills-evidence.md`
**created**: `2026-03-24`
**updated**: `2026-03-24`

---

## Decision / Outcome

**Decision**:

- `S4D-3A` 承接 `S4D-2A` 已经闭环的真实 verify PASS，把重点收敛到 cloud runtime 的最小 rollback 样本与 recovery evidence；
- v1 rollback 不走复杂发布平台，也不做数据级回退，而是先固定一条 image-level known-good rollback path：保留已通过 verify 的本地镜像 tag，在目标主机上用同一份 env 重启容器并复跑 verify。

**Default choices (phase defaults / v1)**:

- rollback unit 默认是目标主机上已经存在的 known-good image tag，而不是远端 registry 或多版本部署平台；
- rollback 动作默认复用现有 container name、env file、host port，不引入第二套运行时 contract；
- rollback 成功标准默认仍以 `cloud_release_verify.sh` 的五项 gate 为准，而不是另造一套恢复语义；
- v1 只要求证明“能退回到上一版已知良好容器镜像并再次通过 verify”，不在本 phase 内覆盖 DB schema/data rollback。

## Definitions (optional)

- **Known-good image tag**：在目标主机上已经存在、且曾通过真实 verify 的 backend image tag。
- **Rollback helper**：把“停止当前容器、用 known-good image 重新起容器、必要时复跑 verify”收口成单一 operator 入口的脚本。
- **Recovery evidence**：用于证明 rollback 后系统重新回到 healthy 状态的 PASS/FAIL 摘要与关键命令记录。

## Constraints

- v1 rollback 样本不覆盖数据库 migration 的逆向回滚；默认前提是当前样本没有不可逆 schema/data 变更；
- 不依赖容器 registry、蓝绿、金丝雀或负载均衡切流；
- rollback helper 只使用目标主机本地已有镜像；如果 known-good tag 不存在，应明确失败并要求 operator 先准备基线镜像；
- 真实 rollback drill 仍需留下可追溯 evidence，不能只记录“已经恢复”。

## Scope

- `P0`: contract（rollback unit、known-good tag、evidence contract）
- `P1`: implementation / scripts（existing-image deploy path、rollback helper、operator order）
- `P2`: drill / verify（第一次真实 rollback 样本）
- `P3`: repeatable recovery wording（把 rollback 路径收口成 operator-facing 说明）

## Success Criteria (DoD)

- 读者能明确知道 v1 rollback 的最小前提：必须先在目标主机上保留一份 known-good image tag；
- 仓库内存在一条最小 rollback helper，可在不重新 build 当前 HEAD 的前提下启动已存在镜像；
- 第一次真实 rollback 样本能给出 rollback 前后镜像 tag、verify 结果与最终 PASS/FAIL；
- `S4D` 顶层 spine 与索引能导航到 `S4D-3A`，并把工作重心从 verify 转到 rollback sample。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 rollback contract、helper 脚本与 operator wording 已稳定；
  - 至少一条真实 Ubuntu VM rollback 样本以 PASS 收口，并记录 rollback 前后 image tag 与 verify 结果。

## P0 (Contract | v1)

### P0-C1-S1 (Rollback unit and precondition contract | v1)

- rollback unit 固定为目标主机本地已存在的 known-good backend image tag；
- operator 在做下一轮 forward deploy 之前，应先把当前 PASS 镜像额外打一个 known-good tag，例如：
  - `docker tag wordloom-backend:cloud-dev wordloom-backend:cloud-dev-known-good-<stamp>`
- 若 known-good image tag 不存在，rollback helper 必须直接 FAIL，而不是隐式回退到重新 build 当前 HEAD。

### P0-C1-S2 (Rollback evidence contract | v1)

- 本 phase 的 evidence 至少应记录：
  - `headSha`
  - `known_good_image_tag`
  - `rollback_target_image_tag`
  - `rollback_command_summary`
  - `verify_command_summary`
  - `verify_check_results`
  - `rollback_reason`
  - `result`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4D-3A/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`）或同一 phase / cycle 下连续 steps 的组合（如 `1S2`）。

**Branch convention**:

- `S4D-3A` 相关实现与文档优先落在 `S4D-cloud-runtime-deploy-verify-rollback` 分支。

**Commit discipline (recommended)**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4D-cloud-runtime-deploy-verify-rollback`。

## Plan (draft)

### P1 (Implementation / scripts)

- P1-C1-S1: 为现有 `cloud_release_run_container.sh` 增加 `--skip-build`，支持直接启动已存在镜像
- P1-C1-S2: 新增 `cloud_release_rollback.sh`，收口 image-level rollback + optional verify

### P2 (Drill / Verify)

- P2-C1-S1: 在 Ubuntu VM 上给当前 PASS 镜像打 known-good tag
- P2-C1-S2: 故意向前推进一个新候选版本或候选镜像后，执行第一次 rollback 样本并复跑 verify

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: rollback unit and precondition contract fixed
- [x] `P0-C1-S2`: rollback evidence contract fixed

### P1 (Implementation / scripts)

- [x] `P1-C1-S1`: existing-image deploy path prepared via `--skip-build`
- [x] `P1-C1-S2`: rollback helper prepared

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: known-good image tag captured on Ubuntu VM
- [ ] `P2-C1-S2`: first real rollback sample recorded

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, image tags, command summaries, and rollback outcomes.

### P1-C1-S1 (Existing-image deploy path prepared | 2026-03-24)

- headSha: `<pending-current-worktree-commit>`
- artifacts:
  - `scripts/ops/cloud_release_run_container.sh`
- expected:
  - 允许 operator 在不重新 build 当前 HEAD 的前提下，直接启动目标主机上已存在的 backend image tag。
- observed:
  - `cloud_release_run_container.sh` 新增 `--skip-build`，可直接复用目标主机本地已有镜像，为 rollback helper 提供底层入口。

### P1-C1-S2 (Rollback helper prepared | 2026-03-24)

- headSha: `<pending-current-worktree-commit>`
- artifacts:
  - `scripts/ops/cloud_release_rollback.sh`
  - `scripts/ops/cloud_release_run_container.sh`
  - `scripts/ops/cloud_release_verify.sh`
- expected:
  - 提供一条最小 image-level rollback 入口：指定 known-good image tag，重启容器，并在默认情况下立即复跑 verify。
- observed:
  - 已新增 `cloud_release_rollback.sh`，默认复用相同 env/container/host-port，并在 rollback 后调用 verify gate 输出 `CLOUD_RELEASE_ROLLBACK_RESULT=PASS|FAIL`。

## Recent changes (for traceability, optional)

- 2026-03-24: 创建 `S4D-3A`，把 `S4D-2A` 完成 verify PASS 之后的工作重点切换到 rollback 样本与 recovery evidence。
- 2026-03-24: 为 rollback 样本准备 existing-image deploy path 与 `cloud_release_rollback.sh` helper，避免回退时误重新 build 当前 HEAD。