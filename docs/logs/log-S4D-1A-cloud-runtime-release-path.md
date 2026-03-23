# log-S4D-1A (Phase 1: Cloud Runtime Release Path)

---

**id**: `S4D-1A`
**kind**: `log`
**title**: `cloud runtime release path (deploy target, env contract, verify/rollback baseline) + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, ReleaseOperations, Deploy, Rollback, Drills, Evidence, epic/s4, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  **previous_log**: `docs/logs/log-S4C-cloud-services-and-terraform-epic.md`
  **reference_log_1**: `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md`
  **reference_log_2**: `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
  **reference_log_3**: `docs/logs/_template-log-phase-drills-evidence.md`
**created**: `2026-03-23`
**updated**: `2026-03-23`

---

## Decision / Outcome

**Decision**:

- `S4D-1A` 作为 `S4D` 的首个 phase，先固定一条最小 cloud runtime release path，而不是同时讨论多个部署目标；
- 本 phase 的交付重点是：部署目标选择、env/config contract、verify/rollback baseline，以及最小 evidence contract。

**Default choices (phase defaults / v1)**:

- 优先复用已经存在的 runtime contract：应用配置继续以 repo-root env 文件和既有启动入口为基础，不引入第三套配置模型；
- deploy target 先追求“最小可解释、可验证、可回退”，不追求 production-grade HA；
- verify 先固定为 health + 关键 read smoke + 日志摘要，写路径和复杂回放放到后续 phase；
- rollback 先固定为“回到上一个已知可用版本/配置”的简单策略。

## Definitions (optional)

- **Deploy target**：第一轮承接 wordloom-v3 runtime 的 cloud/staging-like 运行目标。
- **Release path**：从选择构建物、注入 env、启动服务、执行 smoke、到必要时回退的完整 operator 路径。
- **Post-change verification**：部署完成后，用于判断“能否继续前进”的最小检查集合。
- **Known-good version**：最近一个已通过 verify 的版本/配置组，用作 rollback 基线。

## Constraints

- 不把 deploy target 与 infra target 混成一个问题；云资源本身的建立仍由 `S4C` 负责；
- 不提交真实 secrets；env/config 只记录 contract 与文件/变量名；
- 每次 deploy/rollback drill 都需要记录 target、headSha、env 名、关键命令和结果摘要；
- v1 不引入高复杂度发布策略（蓝绿/金丝雀/多版本并行）。

## Scope

- `P0`: contract（deploy target 选择原则、env/release contract、evidence contract）
- `P1`: implementation / target definition（固定最小 deploy target 与 release path）
- `P2`: drill / verify（首轮 deploy -> verify -> rollback 样本）
- `P3`: docs / operator wording（把 release path 变成 operator-facing 说明）

## Success Criteria (DoD)

- 明确一个 v1 deploy target；
- 明确 deploy 所需的 env/config contract 与最小 verify checklist；
- 至少有一条首轮 deploy/rollback drill 的 evidence 入口；
- 能明确回答：`S4B`、`S4C`、`S4D-1A` 各自负责哪一段 operator path。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 target 选择、release path 与 verify/rollback baseline 已稳定；
  - Evidence 区至少记录一条可追溯的 deploy/rollback 样本（headSha + artifact path / terminal proof / CI run URL）。

## P0 (Contract | v1)

### P0-C1-S1 (Deploy target selection contract | v1)

- v1 deploy target 必须满足：
  - 可低成本获得；
  - 可清楚解释配置注入和启动路径；
  - 支持最小 smoke 与回退验证；
  - 不需要生产级编排前置条件。

### P0-C1-S2 (Release path contract | v1)

- release path 至少应明确：
  - 构建物或启动入口是什么；
  - env/config 如何注入；
  - deploy 成功后的 verify 检查项；
  - rollback 如何回到 known-good version。

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON 后续至少应包含：
  - `headSha`
  - `deploy_target`
  - `env_name`
  - `deploy_command_summary`
  - `verify_summary`
  - `rollback_summary`
  - `result`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4D-1A/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`）或同一 phase / cycle 下连续 steps 的组合（如 `1S2`）。

**Branch convention**:

- `S4D-1A` 相关实现与文档优先落在 `S4D-cloud-runtime-deploy-verify-rollback` 分支。

**Commit discipline (recommended)**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4D-cloud-runtime-deploy-verify-rollback`。

## Plan (draft)

### P1 (Implementation / target definition)

- P1-C1-S1: 选定 v1 deploy target
- P1-C1-S2: 固定 env/release contract 与 verify checklist

### P2 (Drill / Verify)

- P2-C1-S1: 首轮 deploy -> verify 样本入账
- P2-C1-S2: 首轮 rollback 样本入账

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: deploy target selection contract
- [ ] `P0-C1-S2`: release path contract
- [ ] `P0-C1-S3`: evidence contract

### P1 (Implementation / target definition)

- [ ] `P1-C1-S1`: v1 deploy target selected
- [ ] `P1-C1-S2`: env/release contract and verify checklist fixed

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: first deploy -> verify sample recorded
- [ ] `P2-C1-S2`: first rollback sample recorded

### P3 (Docs / operator wording)

- [ ] `P3-C1-S1`: operator-facing wording written

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, deploy target, env/config identifiers, and drill outcomes.

### P0-C1-S1 (S4D-1A skeleton created | 2026-03-23)

- headSha: `<TBD-after-first-S4D-commit>`
- artifacts:
  - `docs/logs/log-S4D-1A-cloud-runtime-release-path.md`
- expected:
  - 为 `S4D-1A` 固定最小 release path 的目标边界、contract 与 evidence 结构。
- observed:
  - phase skeleton 已创建，等待后续 target 选择与首轮 deploy/rollback drills。

## Recent changes (for traceability, optional)

- 2026-03-23: scaffolded `S4D-1A` as the first phase of the cloud runtime deploy/verify/rollback spine.