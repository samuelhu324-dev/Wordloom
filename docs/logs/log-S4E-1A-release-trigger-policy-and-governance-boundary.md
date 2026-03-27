# log-S4E-1A (Phase 1: Release Trigger Policy and Governance Boundary)

---

**id**: `S4E-1A`
**kind**: `log`
**title**: `cloud-dev release trigger policy and governance boundary + drills/evidence v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, ReleaseOperations, Governance, Automation, Drills, Evidence, epic/s4, sub/4e1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **parent_log**: `docs/logs/log-S4E-release-operating-model-and-governance.md`
  **previous_log**: `docs/logs/log-S4D-4C-408-timeout-eradication.md`
  **reference_log_1**: `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
  **reference_log_2**: `docs/logs/log-S4D-4C-408-timeout-eradication.md`
  **reference_log_3**: `docs/roadmap/road-S1-systems-platform-ops-roadmap-v5.md`
**created**: `2026-03-27`
**updated**: `2026-03-27`

---

## Decision / Outcome

**Decision**:

- `S4E-1A` 先不处理新的 runner、network 或 deploy semantics，而是先固定 `cloud-dev` 的 release trigger policy、approval boundary 与 governance contract；
- 第一轮交付目标不是“再做一个 workflow”，而是明确 auto-dispatch、manual `workflow_dispatch`、approval、rerun、drill、override 各自的角色与边界。

**Default choices (phase defaults / v1)**:

- `cloud-dev` 的 routine repo-controlled candidate path 可以保留 auto-dispatch surface，但 manual `workflow_dispatch` 必须继续保留为 drill / override / controlled rerun surface；
- approval boundary 必须独立于 trigger surface：自动启动不等于自动放行；
- release record v1 先要求最小字段集合，而不是引入额外数据库或管理系统；
- `S4E-1A` 只讨论 `cloud-dev`，不在 v1 内直接定义 staging/prod promotion policy。

## Definitions (optional)

- **Trigger surface**：启动一次 release run 的入口，例如 `push` auto-dispatch、manual `workflow_dispatch`、rerun。
- **Approval boundary**：run 已启动但尚未被 reviewer 放行进入高风险步骤的受控门。
- **Release record**：把一次 release run 的关键信息固定下来的一份最小记录，至少包括 `headSha`、trigger surface、target environment、approval actor 与 artifact/run URL。
- **Override**：在 routine auto path 之外，由操作者明确发起的一次手动触发或 rerun。

## Constraints

- 不重复定义 `cloud_release_workflow.sh` 的 deploy / verify / rollback 语义；
- 不把 `S4D-4C` 的 timeout / stable-runner / auto-dispatch 根因治理重新写一遍；
- 不把 `cloud-dev` 的 policy 直接扩写为 prod 级制度；
- 证据字段必须能和现有 GitHub Actions run / artifact 路径直接对齐。

## Scope

- `P0`: contract（trigger surface policy、approval boundary、release record contract）
- `P1`: policy mapping / wording（把现有 `S4D-4B/4C` 行为压缩成显式 policy 文本）
- `P2`: drill / verify（用现有 run 样本验证 manual vs auto 与 approval 的边界）
- `P3`: next-step runway（为 promotion / release governance 下一 phase 留出清晰入口）

## Success Criteria (DoD)

- 明确区分至少三类 trigger surface：routine auto-dispatch、manual drill/override、rerun；
- 明确说明 approval boundary 与 trigger surface 的分工，而不是继续混写成“手点 workflow”；
- 固定一份最小 release record 字段集；
- 至少一条 evidence 能同时指向 auto 与 manual 两类 run 的实际样本；
- 文档层面不再把 `S4D-4B`、`S4D-4C`、`S4E-1A` 的边界写混。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` 的 trigger policy、approval boundary 与最小 release record contract 已稳定；
  - The Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## P0 (Contract | v1)

### P0-C1-S1 (Trigger surface policy contract | v1)

- `cloud-dev` 的 trigger surface 至少区分为：
  - routine auto-dispatch：面向常规 repo-controlled candidate path；
  - manual `workflow_dispatch`：面向 drills、override、手动重试与显式 operator 介入；
  - rerun：面向已有 run 的受控再执行；
- 任何新 surface 都必须说明其默认用途与风险边界，而不是只看 GitHub Actions 的按钮形式。

### P0-C1-S2 (Approval and governance boundary contract | v1)

- approval boundary 与 trigger surface 分离记账；
- 必须明确至少以下问题：
  - 谁能启动 run；
  - 谁能 approve；
  - 谁能 rerun/override；
  - 哪些动作需要被写进 release record；
- `S4E-1A` v1 只要求在 `cloud-dev` 说清这套边界，不要求一次扩展到更高环境。

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON / log 至少应包含：
  - `headSha`
  - `triggerSurface`
  - `targetEnvironment`
  - `runUrl` 或等价 CI run 标识
  - `approvalState`
  - `approvalActor`（若存在）
  - `result`
  - `artifactPath` 或 artifact bundle 引用

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4E-1A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S4E-1A` 相关变更默认继续落在 `S4D-cloud-runtime-deploy-verify-rollback` 分支，直到 `S4E` 独立出更明确的工作分支需求。

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.

## Plan (draft)

### P1 (Policy mapping / wording)

- P1-C1-S1: 固定 auto-dispatch、manual dispatch、rerun 在 `cloud-dev` 的用途和默认边界
- P1-C1-S2: 固定 approval boundary 与 override / rerun 的最小治理 wording

**Current status (S4E-1A / P0-P1)**

- `P0-C1-S1` 已完成第一版 trigger surface contract：当前 `cloud-dev` 已明确区分 routine auto-dispatch、manual `workflow_dispatch` 与 rerun 三种 surface；其中 auto-dispatch 面向常规 candidate path，manual `workflow_dispatch` 面向 drill / override / controlled rerun，而 rerun 只应被视为既有 run 的受控再执行，而不是新的独立发布策略。
- `P0-C1-S2` 已完成第一版 approval/governance boundary：当前 policy 已固定“启动 run”与“批准进入高风险步骤”是两个不同权限面；manual 与 auto 都可以先进入 run，但 approval actor 仍单独负责是否允许进入 `cloud-dev` 受控门后步骤。
- `P0-C1-S3` 已完成第一版 release record contract：当前 `S4E-1A` 已固定最小记录字段为 `headSha`、`triggerSurface`、`targetEnvironment`、`runUrl`、`approvalState`、`approvalActor`、`result` 与 `artifactPath`/artifact bundle 引用，后续 evidence 必须按此口径回填。
- `P1-C1-S1` 已完成第一版 wording 映射：`S4D-4B` 中 `workflow_dispatch` 基线与 `S4D-4C` 中 auto-dispatch follow-up 现在已经被压缩为统一 policy 表述，而不再混写成单个 workflow 的实现细节。
- `P1-C1-S2` 已完成第一版 governance wording：当前 policy 已明确 override / rerun 只能作为受控 operator 动作存在，不能替代 approval boundary，也不能把“成功启动 run”误写成“已批准发布”。

### P2 (Drill / Verify)

- P2-C1-S1: 回填至少一组 auto/manual 并存样本，证明 trigger surface policy 有真实对应面
- P2-C1-S2: 回填至少一组 approval evidence，证明 approval boundary 独立于 trigger surface

### P3 (Next-step runway)

- P3-C1-S1: 为 promotion / release record / governance hierarchy 下一 phase 定义最小入口

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: trigger surface policy fixed
- [x] `P0-C1-S2`: approval and governance boundary fixed
- [x] `P0-C1-S3`: release record evidence contract fixed

### P1 (Policy mapping / wording)

- [x] `P1-C1-S1`: auto/manual/rerun wording fixed
- [x] `P1-C1-S2`: approval boundary wording fixed

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: trigger-surface evidence backfilled
- [ ] `P2-C1-S2`: approval-boundary evidence backfilled

### P3 (Next-step runway)

- [ ] `P3-C1-S1`: promotion/governance runway defined

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P0-C1-S1S2S3 / P1-C1-S1S2 (trigger policy, approval boundary, and wording fixed for cloud-dev | 2026-03-27)

- headSha: `90afbd66`
- artifacts:
  - `docs/logs/log-S4E-release-operating-model-and-governance.md`
  - `docs/logs/log-S4E-1A-release-trigger-policy-and-governance-boundary.md`
  - `docs/logs/log-S4D-4B-github-actions-release-dispatch.md`
  - `docs/logs/log-S4D-4C-408-timeout-eradication.md`
- expected:
  - `cloud-dev` 的 release control-plane 至少要明确区分 auto-dispatch、manual `workflow_dispatch` 与 rerun 三类 surface；
  - approval boundary 必须被明确定义为独立于 trigger surface 的治理门，而不是继续混写成“谁点了 workflow”；
  - `S4E-1A` 应把 `S4D-4B/4C` 中已经存在的事实行为收口为稳定 wording，而不是再去引入新的 workflow 实现。
- observed:
  - `S4E-1A` 当前已正式固定三类 trigger surface：routine auto-dispatch、manual `workflow_dispatch`、rerun，并明确各自用途与默认边界；
  - approval/governance wording 已明确写成独立权限面：run 的启动、approval 的放行、rerun/override 的使用场景必须分开记账；
  - 最小 release record 字段集已固定，可直接用于后续 `P2` evidence 回填；
  - `S4D-4B` 与 `S4D-4C` 的既有事实面已被吸收到统一 policy 文本中，因此 `S4E-1A/P0-P1` 现已具备进入 evidence backfill 的前提。

## Recent changes (for traceability, optional)

- 2026-03-27: 已完成 `S4E-1A/P0-C1-S1S2S3` 与 `P1-C1-S1S2` 的第一轮合同/wording 收口；当前下一步转入 `P2`，用现有 auto/manual/approval 样本回填正式 evidence。
- 2026-03-27: 首次创建 `S4E-1A`，把 `cloud-dev` 的 release trigger policy、approval boundary 与最小 release record contract 单独提升为 phase v1；当前尚未回填正式 evidence。
