# log-S4D-2A (Phase 2: Post-Change Verification & Operational Checks)

---

**id**: `S4D-2A`
**kind**: `log`
**title**: `post-change verification & operational checks (health, logs, smoke, release checklist) + drills/evidence v1`
**status**: `stable`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, Verification, ReleaseOperations, Drills, Evidence, epic/s4, sub/2a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  **previous_log**: `docs/logs/log-S4D-1A-cloud-runtime-release-path.md`
  **reference_log_1**: `docs/logs/log-S4A-5A-operational-visibility-and-post-change-verification.md`
  **reference_log_2**: `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
  **reference_log_3**: `docs/logs/_template-log-phase-drills-evidence.md`
**roadmap_path**: `docs/roadmap/road-001-systems-platform-ops-roadmap-v5.md`
**roadmap_milestone**: `M4`
**roadmap_phase**: `M4-P2`
**roadmap_bridge_refs**: `docs/roadmap/road-001-systems-platform-ops-roadmap-v5.md#M4-P2`
**created**: `2026-03-24`
**updated**: `2026-03-25`

---

## Decision / Outcome

**Decision**:

- `S4D-2A` 承接 `S4D-1A` 已固定的 cloud runtime release path，把重点收敛到真实目标主机上的 post-change verification 与 operator-facing operational checks；
- 从本 phase 开始，凡是围绕真实 deploy 样本展开的 host prep、health/log probe、read smoke、release checklist、drill evidence 与由 drill 暴露出的 release-tooling 缺陷修正，都按 `S4D-2A/P*-C*-S*` 记账与命名。

**Default choices (phase defaults / v1)**:

- 先以单台 Ubuntu Linux VM 为唯一真实样本目标，不并行多个 target host；
- verify 默认围绕 `container_running`、`migration_ok`、`health_ok`、`read_smoke_ok`、`env_guard_ok` 五项 gate；
- 证据优先记录真实 operator 路径中的 head SHA、目标主机语境、关键命令摘要、FAIL/PASS 结果与根因，而不是只保留结论；
- 对真实 drill 暴露出的脚本缺陷，允许在同一 cycle 内立即修复并重跑，但必须把失败原因和修复点写入本 phase evidence。

## Definitions (optional)

- **Post-change verification**：部署或配置变更后，用来判断“当前版本是否仍可继续前进”的最小检查集合。
- **Operational checks**：operator 在目标主机上执行的健康检查、日志观察、HTTP smoke 与 checklist 判定。
- **Real VM sample**：不是本机模拟，而是在一台真实 Linux VM 上执行 deploy 和 verify 的样本。
- **Host/container port boundary**：宿主机对外探测端口与容器内部监听端口的区分，二者不能混淆。

## Constraints

- 不在本 phase 内扩展到生产级多主机编排或监控平台；
- 不提交真实 secrets；env file 只作为路径与 contract 被引用；
- 真实 drill 中的 FAIL 也属于证据的一部分，不能因为后续修复成功就抹掉；
- 本 phase 默认在 `S4D-cloud-runtime-deploy-verify-rollback` 分支上连续提交，不为每一次 drill 单独切 branch。

## Scope

- `P0`: contract（phase 边界、命名、evidence contract）
- `P1`: implementation / checks（release checklist、verify 入口、operator order）
- `P2`: drill / verify（真实 Ubuntu VM deploy/verify 样本与问题收敛）
- `P3`: repeatable evidence / rollback handoff（首个 PASS 样本入账，并把回滚入口交给后续 phase）

## Success Criteria (DoD)

- 读者能清楚区分 `S4D-1A` 与 `S4D-2A` 的边界：前者负责 release path contract，后者负责真实 host 上的 verification/checks/evidence；
- `S4D-2A` 下至少有一条真实 Ubuntu VM deploy/verify 样本链路，且 failure 与 fix 均可追溯；
- commit 命名从本 phase 起与 `S4D-2A` 一致，不再把真实 verification drill 继续记在顶层 `S4D` 前缀下；
- 首个真实 verify PASS 后，Evidence 区能给出对应 `headSha`、env file 路径摘要、关键检查结果与 artifact/terminal proof。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 phase 边界、operator checks 与真实 drill evidence 已稳定；
  - 至少一条真实 Ubuntu VM deploy/verify 样本以 PASS 收口，且失败修复链路可追溯。

## P0 (Contract | v1)

### P0-C1-S1 (Phase boundary and naming contract | v1)

- `S4D-1A` 负责：deploy target 选择、env/release contract、verify/rollback baseline；
- `S4D-2A` 负责：真实主机上的 post-change verification、operator checks、release checklist、drill evidence，以及 drill 暴露出的脚本缺陷修复与复验；
- 从本 phase 开始，commit / PR 命名固定为：
  - `S4D-2A/P<phase>-C<cycle>-S<steps>: <summary>`

### P0-C1-S2 (Evidence contract | v1)

- 本 phase 的 evidence 至少应记录：
  - `headSha`
  - `target_host_kind`
  - `env_file_path`
  - `deploy_command_summary`
  - `verify_command_summary`
  - `verify_check_results`
  - `root_cause`（如 FAIL）
  - `fix_commit`（如本轮 drill 触发了代码修复）
  - `result`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4D-2A/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`）或同一 phase / cycle 下连续 steps 的组合（如 `1S2`）。

**Branch convention**:

- `S4D-2A` 相关实现与文档优先落在 `S4D-cloud-runtime-deploy-verify-rollback` 分支。

**Commit discipline (recommended)**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4D-cloud-runtime-deploy-verify-rollback`。

## Plan (draft)

### P1 (Implementation / checks)

- P1-C1-S1: 固定 Ubuntu VM operator order 与 release checklist
- P1-C1-S2: 固定 target-host verify 入口与 host/container port 边界

### P2 (Drill / Verify)

- P2-C1-S1: 记录第一台 Ubuntu VM host prep 与 repo sync baseline
- P2-C1-S2: 记录首次真实 deploy FAIL 与 `docker run -d` wrapper 修复
- P2-C1-S3: 记录 verify host/container port collision 与 verify gate 修复
- P2-C1-S4: 重跑 verify，拿到首个真实 PASS 样本

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: phase boundary and naming contract fixed
- [x] `P0-C1-S2`: evidence contract fixed

### P1 (Implementation / checks)

- [x] `P1-C1-S1`: Ubuntu VM operator order and release checklist fixed
- [x] `P1-C1-S2`: target-host verify path and host/container port boundary fixed

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: first Ubuntu VM host prep and repo sync baseline recorded
- [x] `P2-C1-S2`: first deploy FAIL recorded and wrapper fix landed
- [x] `P2-C1-S3`: verify port collision recorded and verify fix landed
- [x] `P2-C1-S4`: first real verify PASS recorded

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths or terminal proof.

### P2-C1-S1 (Ubuntu VM repo sync baseline | 2026-03-24)

- headSha: `234cb498`
- target_host_kind: `Ubuntu Server VM in VirtualBox (SSH via 127.0.0.1:2222)`
- env_file_path: `/etc/wordloom/.env.cloud.dev` (planned target path)
- expected:
  - 主机完成 `git clone`、branch checkout、HEAD 校验与 Docker 可用性确认；
  - 为第一次真实 deploy/verify 样本建立可重复 baseline。
- observed:
  - Ubuntu VM 已完成 host prep、repo sync 与 branch/HEAD 校验；
  - 后续真实 deploy/verify 样本已收敛到同一台主机与同一条 operator path。

### P2-C1-S2 (First real deploy FAIL -> wrapper fix | 2026-03-24)

- headSha: `562a712b`
- deploy_command_summary: `bash scripts/ops/cloud_release_run_container.sh --env-file /etc/wordloom/.env.cloud.dev`
- verify_command_summary: `bash scripts/ops/cloud_release_verify.sh --env-file /etc/wordloom/.env.cloud.dev`
- verify_check_results:
  - `container_running=FAIL`
  - `migration_ok=FAIL`
  - `health_ok=FAIL`
  - `read_smoke_ok=FAIL`
  - `env_guard_ok=OK`
- root_cause:
  - `cloud_release_run_container.sh` 把 Docker 参数拼成了 `docker -d run ...`，导致容器根本未创建。
- fix_commit:
  - `562a712b`
- result:
  - `FAIL -> fixed in same cycle`

### P2-C1-S3 (Verify port collision -> verify gate fix | 2026-03-24)

- headSha: `164f58f2`
- deploy_command_summary: `bash scripts/ops/cloud_release_run_container.sh --env-file /etc/wordloom/.env.cloud.dev`
- verify_command_summary: `bash scripts/ops/cloud_release_verify.sh --env-file /etc/wordloom/.env.cloud.dev`
- verify_check_results:
  - `container_running=OK`
  - `migration_ok=OK`
  - `health_ok=FAIL (000)`
  - `read_smoke_ok=FAIL (code=000)`
  - `env_guard_ok=OK`
- root_cause:
  - verify 脚本把 env file 中的 `API_PORT=8000` 当成宿主机探测端口，错误探测了 `127.0.0.1:8000` 而不是 host port `30021`。
- fix_commit:
  - `164f58f2`
- result:
  - `FAIL -> fixed in same cycle; PASS rerun pending`

### P2-C1-S4 (First real verify PASS on Ubuntu VM | 2026-03-24)

- headSha: `937d202a`
- target_host_kind: `Ubuntu Server VM in VirtualBox (SSH via 127.0.0.1:2222)`
- env_file_path: `/etc/wordloom/.env.cloud.dev`
- deploy_command_summary:
  - host already aligned to `origin/S4D-cloud-runtime-deploy-verify-rollback` at `HEAD=937d202a40706158db3b3415d86af9c85edaba51`
- verify_command_summary: `bash scripts/ops/cloud_release_verify.sh --env-file /etc/wordloom/.env.cloud.dev`
- verify_check_results:
  - `container_running=OK`
  - `migration_ok=OK`
  - `health_ok=OK (200)`
  - `read_smoke_ok=OK (200 list payload)`
  - `env_guard_ok=OK`
- observed:
  - verify 输出包含 `CLOUD_RELEASE_VERIFY_RESULT=PASS`；
  - 这说明第一轮真实 Ubuntu VM post-change verification 已闭环，cloud runtime 的最小 release gate 已可在真实目标主机上通过。
- result:
  - `PASS`

## Recent changes (for traceability, optional)

- 2026-03-24: 创建 `S4D-2A`，把真实 Ubuntu VM post-change verification 与 operational checks 从 `S4D-1A` 的 release-path contract 中拆分出来。
- 2026-03-24: 明确从本 phase 开始，真实 deploy/verify drill 与由 drill 暴露出的修复提交统一采用 `S4D-2A/P*-C*-S*` 命名。
- 2026-03-24: 重新核对历史后，已把早先误挂在顶层 `S4D` 前缀下的 phase-specific 提交重新归位到 `S4D-1A` 与 `S4D-2A`，并刷新相关 SHA 引用。
- 2026-03-24: 第一轮真实 Ubuntu VM verify 已拿到 `CLOUD_RELEASE_VERIFY_RESULT=PASS`，因此 `S4D-2A` 当前下一步从 verify 收口切换为 rollback 样本。
- 2026-03-25: 稳定性评估完成；由于 phase 边界、失败修复链路与首个真实 verify PASS 均已固定，`S4D-2A` 现可标记为 `stable`，后续 rollback 深化工作转交 `S4D-3A` / 潜在 `S4D-4A`。