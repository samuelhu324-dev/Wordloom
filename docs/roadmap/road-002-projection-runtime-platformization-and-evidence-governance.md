# road-002-projection-runtime-platformization-and-evidence-governance

---

**id**: `road-002`
**kind**: `roadmap`
**title**: `002: Projection runtime, platformization, and evidence-governed adoption roadmap`
**status**: `draft`
**scope**: `002`
**tags**: `ROADMAP, projection, platformization, hard-gate, evidence, planning`
**links**: ``
  **source**: `docs/roadmap/road-S2-.md`
  **reference_template**: `docs/roadmap/road-template-main-roadmap.md`
  **reference_log_1**: `docs/logs/log-S2B-projection-table-merge.md`
  **reference_log_2**: `docs/logs/log-S2C-projection-framework-platformization.md`
  **reference_log_3**: `docs/logs/log-S2D-projection-onboarding-hard-gates.md`
  **reference_log_4**: `docs/logs/log-S0E-docs-management-v5.md`
  **reference_log_5**: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
**created**: `2026-04-04`
**updated**: `2026-04-04`

---

## Positioning

**Context / role targeting**

- `road-002` 是新的 S2 主线 roadmap，但命名已经与 `S2` scope 本身解耦，避免再和 `docs/logs/INDEX.md` 里的层级编号混淆。
- 这条主线的核心不是单个 projection 或单个模块，而是把 wordloom-v3 的 projection runtime 从“局部实现集合”推进成“可迁移、可平台化、可强制 onboarding、可治理证据面”的长期 backbone。
- `S2B` 负责把 projection runtime 的 failure contract、统一消费框架、table merge 与 unified outbox runtime 做实。
- `S2C` 负责把 projection 体系抽象为 spec/registry/harness/templates，而不是每新增一条 projection 就重新手搓 worker/rebuild/drills。
- `S2D` 负责把“是否真的按平台方式 onboarding projection”变成 hard gate，而不是停留在工程自觉。
- `S0E` 与 `S6B` 不作为这条主线的业务核心，但它们提供了这条主线后续需要的 roadmap/docs bridge、issue/PR automation、evidence taxonomy 与 inventory 治理支撑面，因此必须并入 roadmap 而不是留在旁注里。

**One-sentence goal**

- Build a projection backbone that is runtime-hardened, platformized, onboarding-gated, and governed by explicit docs/evidence contracts.

## Scope & Audience

- **Primary audience**: 你自己后续在 wordloom-v3 上继续推进 projection/runtime/platform work 时的主线导航，以及任何需要快速理解这条能力线的人。
- **Time horizon**: 以中长期演进为主，允许先收口已有完成面，再逐步推进 evidence/storage/governance follow-up。
- **Code base**: `wordloom-v3`
- **Current ownership boundary**: `road-002` 主体优先承接 `S2B + S2C + S2D` 的 projection 主心骨；`S0E` 与 `S6B` 在这里承担的是“治理与可追溯支撑面”，不是替代 projection 本身的业务主线。

## Mainline / Branch Rules

- `road-002` 是 projection/runtime/platformization 的主线 road。
- 当前没有必须单独拆出的 `road-002-xx` branch road；如果未来出现“asset platform”或“projection-only legacy migration”这类长期 detour，再另开支线而不是污染主线。
- 主线 bridge ledger 的 canonical rows 仍然应该优先指向 child logs，而不是把 parent/spine prose 当作完成项。
- `S0E` 与 `S6B` 在本路线里允许承担治理类 child-log 完成项，但它们服务的是 S2 主线的可追溯性与治理面，而不是重定义 projection 本体。

## Roadmap / Log Bridge Contract

- `road-002` owns the `M* / M*-P*` capability language for the projection backbone.
- Child logs own implementation, drills, evidence, and hard-gate detail.
- This roadmap should stay child-log-first wherever the current log family already exposes a clear child slice.
- `Evidence Pointers` and `Recent Changes` are supporting narrative only.

## Branch Road Register

- `none yet`
- If a future branch road appears, it should isolate one focused detour such as asset-platform elevation, legacy projection migration batching, or service-extraction planning.

## Current ownership boundary

- `media / asset platform` 目前仍更适合作为与 S1/S2 邻接的独立能力面，而不是立即并入 `road-002` 的主 milestone。
- “是否拆微服务”在当前阶段也不是主线 deliverable；对 wordloom-v3 来说，更合理的顺序仍是先把 projection/runtime/platform boundaries 做稳，再决定是否要把 Search、Media、Audit/Evidence 这类外围能力独立部署。
- 因此这条 roadmap 现在优先收口的是：projection runtime consistency、platformization、onboarding hard gates、以及 docs/evidence governance；而不是提前把 asset platform 或 service split 当成既定里程碑。

## Milestone overview (M1-M5)

- **M1. Projection failure contracts and unified consumer baseline**
- **M2. Table merge, cutover, and unified outbox runtime**
- **M3. Projection framework platformization and reusable templates**
- **M4. Projection onboarding hard gates and CI adoption**
- **M5. Roadmap/docs/evidence governance for projection operations**

## Future capabilities & trigger conditions

### F1: Asset platform elevation

- `media` 目前更适合作为 S1/S2 邻接模块，而不是直接升级成新层或并入当前 roadmap 主 milestone。
- 当它真正具备独立生命周期、存储策略、访问控制、异步任务与运维口径时，再评估是否提升为 `Asset Platform` 级支线，而不是继续沿用 `media` 这种过窄命名。

### F2: Service extraction triggers

- 微服务不是这条路线当前的默认目标。
- 只有当 projection/search/audit/media 出现明显独立扩缩容需求、隔离边界要求、或部署冲突时，才值得从当前模块化单体演进到独立服务。
- 对 wordloom-v3 来说，最可能先独立出去的仍是 Search、Media asset、Async projection runtime、Audit/Evidence 这类外围能力，而不是 SoT 主链路对象本身。

### F3: Governance widening after taxonomy baseline

- `S6B` 现在已经把 evidence family、inventory ledger 与 hotspot list 打开，但 retention policy、generator policy 与 bounded cutover 仍未完成。
- `S0E` 已把 roadmap/docs/issue/PR bridge 做到较强完成面，后续若要继续收紧自动化或把 `road-002` 接到 milestone automation，需要在现有 bridge contract 上做增量接线，而不是重新发明一套 docs 流程。

## Milestones (M1-M5)

### M1: Projection failure contracts and unified consumer baseline

**Goal**

- 把 projection runtime 的 failure contract、write-gate 语义、统一消费框架与可审计 drill 口径做成稳定基线，让后续 table merge 与 platformization 有可靠底座。

**Bridge Ledger (child logs only)**

- `M1-P0`:
  - `docs/logs/log-S2B-1A-failure-contract-v1.md`
- `M1-P1`:
  - `docs/logs/log-S2B-2A-failure-contract-v2.md`
  - `docs/logs/log-S2B-2A-1A-shadow-verify-write-gate.md`
- `M1-P2`:
  - `docs/logs/log-S2B-3A-unified-consumer-framework.md`
- `M1-P3`:
  - `docs/logs/log-S2B-2A-2A-dual-run-cutover-closure.md`

**Plan (P0-P3)**

- `P0` Contract: 固定 projection failure contract、shadow verify、read switch 与 evidence chain 的最小口径。
- `P1` Implementation: 把 write-gate、dual-run、cutover closure 收敛为统一的 projection runtime failure semantics。
- `P2` Drill: 把 claim/retry/reclaim/DLQ/replay/runbook 升级为统一 consumer framework。
- `P3` Drill: 以 cutover closure 和 write-gate evidence 验证前述 contract 不是只停留在设计层。

**Execution Checklist**

- [x] `M1-P0`: failure contract baseline 已落地
- [x] `M1-P1`: write-gate / shadow-verify contract 已落地
- [x] `M1-P2`: unified consumer framework 已落地
- [x] `M1-P3`: dual-run / cutover closure 已形成稳定证据面

### M2: Table merge, cutover, and unified outbox runtime

**Goal**

- 在 M1 基线之上，把 projection runtime 从“统一语义”推进到“统一物理与迁移闭环”，包括 table merge、search/chronicle cutover 与 unified outbox table migration。

**Bridge Ledger (child logs only)**

- `M2-P0`:
  - `docs/logs/log-S2B-4A-table-merge-migration.md`
- `M2-P1`:
  - `docs/logs/log-S2B-5A-table-merge-migration.md`
  - `docs/logs/log-S2B-5A-table-merge-migration-v2.md`
- `M2-P2`:
  - `docs/logs/log-S2B-6A-unified-outbox-table-merge.md`
- `M2-P3`:
  - `docs/logs/log-S2B-projection-table-merge.md`

**Plan (P0-P3)**

- `P0` Contract: 明确 Chronicle-first table merge migration 的 schema/index/backfill/rehearsal 边界。
- `P1` Implementation: 把 Search 侧收敛到和 Chronicle 对齐的迁移/cutover/deprecate 口径。
- `P2` Drill: 在 payload 治理与容量/隔离策略明确后推进 unified outbox table merge。
- `P3` Drill: 以 parent spine 收口整个 S2B runtime merge line 的边界与后续维护口径。

**Execution Checklist**

- [x] `M2-P0`: table-merge migration baseline 已落地
- [x] `M2-P1`: Search/Chronicle cutover closure 已落地
- [x] `M2-P2`: unified outbox table merge 已落地
- [x] `M2-P3`: runtime merge 主线已具备完整 spine

### M3: Projection framework platformization and reusable templates

**Goal**

- 把 projection 从一组工程实现提升为可复制框架，让新增 projection 优先变成“填 spec + 写 apply + 复用 harness/templates”，而不是复制 worker/rebuild/drills。

**Bridge Ledger (child logs only)**

- `M3-P0`:
  - `docs/logs/log-S2C-1A-projection-spec-registry-harness.md`
- `M3-P1`:
  - `docs/logs/log-S2C-2A-projection-writer-template.md`
  - `docs/logs/log-S2C-3A-projection-rebuild-backfill-template.md`
- `M3-P2`:
  - `docs/logs/log-S2C-4A-projection-drills-template.md`
  - `docs/logs/log-S2C-5A-projection-backfill-template.md`
- `M3-P3`:
  - `docs/logs/log-S2C-6A-search-harness-migration.md`

**Plan (P0-P3)**

- `P0` Contract: 固定 `ProjectionSpec` / registry / harness 的最小接口与边界。
- `P1` Implementation: 把 writer、rebuild、backfill runner 做成通用模板，而不是 projection-specific one-off 工具。
- `P2` Drill: 把 drills template 与 catalog 规则做成新增 projection 时可直接复用的最小套餐。
- `P3` Drill: 用 Search harness migration 证明这套平台化路径可以承接真实 legacy projection，而不只是 DB-to-DB 简单样本。

**Execution Checklist**

- [x] `M3-P0`: spec/registry/harness 基线已落地
- [x] `M3-P1`: writer / rebuild / backfill 模板已落地
- [x] `M3-P2`: drills / backfill 模板已落地
- [x] `M3-P3`: Search harness migration 已落地

### M4: Projection onboarding hard gates and CI adoption

**Goal**

- 把“projection 是否真的按平台方式落地”从 code review 自觉提升为 onboarding contract、coverage drill、hard gate entrypoint 与 CI workflow 可机械判定的能力。

**Bridge Ledger (child logs only)**

- `M4-P0`:
  - `docs/logs/log-S2D-1A-projection-onboarding-contract-and-sample.md`
- `M4-P1`:
  - `docs/logs/log-S2D-1B-projection-onboarding-skeleton-second-sample.md`
  - `docs/logs/log-S2D-1C-projection-onboarding-skeleton-third-sample.md`
  - `docs/logs/log-S2D-1D-projection-onboarding-skeleton-fourth-sample.md`
  - `docs/logs/log-S2D-2A-onboarding-coverage-and-catalog-rules.md`
- `M4-P2`:
  - `docs/logs/log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI.md`
- `M4-P3`:
  - `unmapped`

**Plan (P0-P3)**

- `P0` Contract: 固定 onboarding contract 与 first sample projection 的全链路边界。
- `P1` Implementation: 为后续 legacy projection 提供第二、第三、第四条 skeleton/sample，并建立 coverage/catalog 规则。
- `P2` Drill: 把 S2D hard gate entrypoint 与 CI wiring 做成持续可复跑的门禁层。
- `P3` Drill: 后续再决定何时把更多 projection 从 optional/observer 提升为 required，而不是现在提前硬写死。

**Execution Checklist**

- [x] `M4-P0`: first sample onboarding contract 已落地
- [x] `M4-P1`: onboarding skeleton 与 coverage/catalog rules 已落地
- [x] `M4-P2`: hard gate entrypoint 与 CI wiring 已落地
- [ ] `M4-P3`: broader required-rollout 仍待后续按 projection family 分批收口

### M5: Roadmap/docs/evidence governance for projection operations

**Goal**

- 把 projection 主线继续接到明确的 roadmap/docs/evidence 治理面上，避免后续 runtime/platform/hard-gate 工作继续依赖口头映射、临时 artifact 认知或无主的 evidence surface。

**Bridge Ledger (child logs only)**

- `M5-P0`:
  - `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  - `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  - `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  - `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  - `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  - `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
- `M5-P1`:
  - `docs/logs/log-S0E-3B-github-label-inventory-and-live-preflight.md`
  - `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  - `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
  - `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
  - `docs/logs/log-S0E-4D-review-hold-and-full-auto-lifecycle-orchestration-follow-up.md`
  - `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
  - `docs/logs/log-S0E-4F-pr-body-metadata-links-redundancy-follow-up.md`
  - `docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
- `M5-P2`:
  - `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  - `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  - `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  - `docs/logs/log-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
  - `docs/logs/log-S0E-6B-log-stability-and-gate-strategy.md`
  - `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
  - `docs/logs/log-S0E-6D-natural-issue-context-rendering-and-weak-gate.md`
  - `docs/logs/log-S0E-6E-single-item-context-authoring-and-batch-preserve-boundary.md`
  - `docs/logs/log-S0E-6F-issue-body-metadata-links-boundary-follow-up.md`
  - `docs/logs/log-S6B-1A-evidence-surface-inventory-ledger.md`
- `M5-P3`:
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md`
  - `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
  - `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
  - `docs/logs/log-S0E-7E-publish-verify-remediation-gate-thin-orchestration-entrypoint.md`
  - `docs/logs/log-S0E-7F-publish-verify-remediation-gate-read-only-wrapper-adoption.md`
  - `docs/logs/log-S0E-7G-publish-verify-remediation-gate-workflow-dispatch-wrapper-surface.md`
  - `docs/logs/log-S6B-evidence-drills-taxonomy.md`

**Plan (P0-P3)**

- `P0` Contract: 先把 roadmap milestone <-> child log bridge 固定成 child-log-first contract，避免 `road-002` 后续又回到 prose-only 记账。
- `P1` Implementation: 继续沿用 `S0E` 已完成的双轨证据、issue/PR/docs automation 能力，为 projection 主线提供稳定的治理入口。
- `P2` Drill: 先把 evidence inventory ledger 建出来，明确当前 repo 中哪些 surface 是 human-ledger、fact-source、retained-summary、workflow-derived、tmp-scratch。
- `P3` Drill: 在 inventory 之上继续推进 taxonomy、retention、generator policy 与 bounded cutover，而不是继续把所有东西泛称为 `artifacts`。

**Execution Checklist**

- [x] `M5-P0`: roadmap/log bridge contract 已完成并可复用
- [x] `M5-P1`: docs/evidence dual-track baseline 已完成并可复用
- [ ] `M5-P2`: repo-level evidence inventory 已开账，但后续 policy/cutover 尚未完成
- [ ] `M5-P3`: taxonomy/retention/generator/cutover 仍在进行中

## Evidence Pointers (cross-log)

- `S2B` 是 projection runtime consistency、table merge、unified outbox 的主事实线。
- `S2C` 是 projection platformization 的主事实线。
- `S2D` 是 onboarding hard-gate 与 CI adoption 的主事实线。
- `S0E` 是 roadmap/docs/issue/PR bridge 与 automation governance 的支撑线。
- `S6B` 是 evidence taxonomy、inventory 与后续 retention/generator policy 的支撑线。

## Recent Changes

- 2026-04-04: created `road-002` as the numeric successor to the old `road-S2` idea, explicitly separating roadmap numbering from `S*` scope numbering.
- 2026-04-04: reframed the old `road-S2-.md` draft into a proper mainline roadmap centered on `S2B + S2C + S2D`, while absorbing `S0E` and `S6B` as governance support surfaces instead of leaving them as unrelated side work.
- 2026-04-04: kept asset-platform elevation and service extraction as future-trigger notes rather than forcing them into the active roadmap milestones before the projection backbone is fully governed.