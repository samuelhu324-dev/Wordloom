# road-002-projection-runtime-platformization-and-evidence-governance

---

**id**: `road-002`
**kind**: `roadmap`
**title**: `002: projection runtime platformization and evidence governance roadmap`
**status**: `draft`
**scope**: `002`
**tags**: `ROADMAP, projection runtime, evidence governance, docs governance, access control, asset platform`
**links**: ``
  **source**: `docs/roadmap/road-template-main-roadmap.md`
  **reference_log_1**: `docs/logs/log-S0E-docs-management-v5.md`
  **reference_log_2**: `docs/logs/log-S0F-docs-management-v6.md`
  **reference_log_3**: `docs/roadmap/_draft/road-S2-.md`
**created**: `2026-04-14`
**updated**: `2026-04-16`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for roadmap frontmatter.
- Day-level precision is acceptable here because this file is currently a planning backbone rather than a fine-grained execution ledger.
- `reviewed` should remain `pending` until this first mainline draft is explicitly accepted as the new stable planning front door.

## Positioning

**Context / role targeting**

- `road-002` is the next mainline roadmap for the repo's projection-runtime, evidence-governance, and product-control-plane direction.
- It is not a pure docs roadmap even though the first completed surface is docs-heavy; the docs/GitHub automation and governance work exists here because it is the safest first production-adjacent place to fix ownership, approval, contract shape, and controlled mutation semantics.
- The roadmap deliberately starts with `S0E` and `S0F` because those lines let the repo harden governance and operational discipline around `S0 / DOC / contract` with the lowest immediate business damage while still producing reusable control-plane rules.
- `M3` should initially remain `DOC`-first in execution shape: the first governance-control lane should still be opened and judged through docs/governance surfaces before any later abstraction tries to treat governance as an app-wide runtime subsystem.
- The ordering below is a preferred current sequence, not a hard serial law: roadmap milestones remain selectable during execution when new evidence changes priority.

**One-sentence goal**

- Build a staged backbone from docs/GitHub lifecycle discipline, into ownership-and-access control planes, and only then into an asset platform whose value depends on those control surfaces already existing.

## Mainline / Branch Rules

- `road-002` is the long-running mainline for this capability family.
- Focused branch roads may appear later when one sub-problem becomes too detailed for the mainline body, but the mainline ledger must still point to child logs as the canonical execution rows.
- The ordering inside this roadmap expresses today's best execution shape, but any `M* / P*` slot may be selected earlier when evidence, repo state, or real product pressure justifies it.
- Mainline bridge rows should prefer real logs already in the repo; draft discussions or scratch notes may appear only in `Evidence Pointers`, not as canonical implementation rows.

## Scope & Audience

- **Primary audience**: repo owner, future platform/operator readers, and later collaborators who need one backbone view across docs governance, runtime governance, access control, and asset-platform timing.
- **Time horizon**: 6 months to multiple years.
- **Code base**: `wordloom-v3`.

## Roadmap / Log Bridge Contract

- `road-002` owns the durable `M* / M*-P*` capability language for this direction.
- Child logs own the actual implementation, drills, evidence, and bounded decision records.
- The canonical machine-readable bridge remains `M*-P* -> child log`.
- This roadmap intentionally uses the docs/GitHub family as the first execution surface, but later milestones are broader than docs and should not be reduced back to a docs-only interpretation.
- `Evidence Pointers` remain supporting narrative only; they do not replace the bridge ledger.

## Branch Road Register

- No focused branch road is opened yet.
- Likely future branch-road candidates:
  - one branch for cross-repo governance control plane rollout after the first `log -> ledger -> contract` rules are accepted;
  - one branch for tenant / entitlement / billing simulation once the first SoT-side access model needs concentrated design detail;
  - one branch for asset-platform admission if media/object handling becomes detailed enough to flood the mainline body.

## Milestone overview (M1-M5)

- **M1. Docs/GitHub lifecycle automation and structured-log discipline (`S0E`)**
- **M2. Docs governance, chronology-first contracts, and ledger accountability (`S0F`)**
- **M3. Governance control plane for ownership, approval, provenance, contribution, and handoff**
- **M4. Tenant access control plane and mock billing closure on the current SoT**
- **M5. Asset platform activation after governance and access baselines exist**

> 说明：当前最理想顺序是先完成 `M1 + M2`，再推进 `M3 + M4`，最后才让 `M5` 真正进入高价值实现阶段；但这不排除局部前置研究，只是主闭环不应倒置。

## Future capabilities & trigger conditions

### F1: Runbook / evidence / drills governance rollout

- 这些面现在不应先于 `M3` 进入全面治理推广。
- 触发条件是：`log -> ledger -> contract` 上的 ownership / approval / handoff / provenance 协议已经稳定，且读者能明确分清 current steward、owner team、approver 与 evidence verifier 的角色边界。

### F2: Internal-tool permission realism

- 在真实业务不足的情况下，内部工具权限不应先做成复杂企业系统模拟。
- 触发条件是：`M4` 至少已经把 `tenant / membership / role / plan / entitlement` 的最小闭环跑通，能够在 `library -> bookshelf -> book -> block` 上证明授权不是空想。

### F3: Real payment integration

- 支付不应先于 entitlement 模型进入主线。
- 触发条件是：mock billing 状态机已经在本地形成闭环，且系统已经证明订阅状态变化能稳定改写 entitlement snapshot。

### F4: Asset platform admission

- media/asset 只有在前两个控制面都存在之后才值得进入高优先级，因为对象生命周期、权限、签名 URL、审计、归档和共享能力都依赖责任与授权模型。
- 触发条件是：`M3` 与 `M4` 至少各自形成第一版可复用 contract，且对象存储/附件/导出包开始要求统一平台化治理。

## Milestones (M1-M5)

### M1: Docs/GitHub lifecycle automation and structured-log discipline (`S0E`)

**Goal**

- Use the docs/GitHub lifecycle as the first low-damage proving ground for structured automation, strong-vs-weak log boundaries, fail-closed issue/PR/conclusion mutation, and retained evidence around controlled live actions.
- Current rough standing: this milestone is already materially advanced, with roughly sixty-to-seventy percent of the intended first-generation work already present across `S0E`.

**Bridge Ledger (child logs only)**

- `M1-P0`:
  - `docs/logs/log-S0E-docs-management-v5.md`
  - `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  - `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
- `M1-P1`:
  - `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  - `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  - `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  - `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
- `M1-P2`:
  - `docs/logs/log-S0E-4D-review-hold-and-full-auto-lifecycle-orchestration-follow-up.md`
  - `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  - `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  - `docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
  - `docs/logs/log-S0E-6B-log-stability-and-gate-strategy.md`
- `M1-P3`:
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md`
  - `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
  - `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`

**Plan (P0-P3)**

- `P0` Contract: finish the controlled mapping from structured logs into issue/PR/conclusion surfaces, including strong-structure vs weak-structure ownership and deterministic machine-readable bridge rules.
- `P1` Implementation: keep the semi-automated and guarded live-mutation path stable for issue creation, PR creation, relationship attach, and issue conclusion without reintroducing guess-first behavior.
- `P2` Drill: continue hardening lifecycle audit, dry-run planning, body-shape gates, and local-first fail-closed checks so the docs/GitHub family remains a reliable proving ground for later control-plane work.
- `P3` Drill: keep post-publish verification, attribution-first GitHub-side mirroring, historical replay sampling, and publish-verify-remediation packaging stable enough that this line can act as a reusable operational substrate rather than a one-off docs experiment.

### M2: Docs governance, chronology-first contracts, and ledger accountability (`S0F`)

**Goal**

- Use the docs layer as the first governance-heavy production-adjacent surface: fix fail-closed entrypoints, stabilize governance registry and lineage, rebuild chronology-first contracts, and prove that approval/provenance/accountability can be made explicit on `S0 / DOC / contract` before riskier business surfaces are touched.

**Bridge Ledger (child logs only)**

- `M2-P0`:
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
  - `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
  - `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
- `M2-P1`:
  - `docs/logs/log-S0F-2A-maintenance-lanes-and-direct-patch-ledger.md`
  - `docs/logs/log-S0F-2B-family-patch-and-ops-maintenance-model.md`
  - `docs/logs/log-S0F-3A-governance-contract-index-and-delta-model.md`
  - `docs/logs/log-S0F-3B-governance-contract-registry-and-naming-model.md`
  - `docs/logs/log-S0F-3H-recurring-governance-run-model-and-ledger-split.md`
  - `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- `M2-P2`:
  - `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
  - `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
  - `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
  - `docs/logs/log-S0F-5A-stable-first-close-out-protocol-and-post-stable-outlet-export.md`
  - `docs/logs/log-S0F-6C-outlet-and-lifecycle-observability.md`
- `M2-P3`:
  - `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
  - `docs/logs/log-S0F-7B-release-based-contract-lineage-and-ledger-model.md`
  - `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  - `docs/logs/log-S0F-7G-approval-facing-screenshot-evidence-review-and-attachment-protocol.md`
  - `docs/logs/log-S0F-7H-actor-and-provenance-fields-for-evidence-review-governance.md`
  - `docs/logs/log-S0F-7I-ledger-and-contract-structure-integration-audit-and-remediation-plan.md`

**Plan (P0-P3)**

- `P0` Contract: finish the fail-closed and maintenance-side boundary so docs/GitHub mutation, log structure, and patch/maintenance lanes remain explicit and reviewable.
- `P1` Implementation: continue consolidating the governance registry, contract placement, lineage, cleanup staging, recurring-run packaging, and current-surface rules until the docs layer behaves like a real governed system rather than an accreted archive.
- `P2` Drill: keep stabilizing reader surfaces, old-history front doors, outlet observability, and doc-current-vs-legacy routing so the repo's public governance surface stays legible.
- `P3` Drill: continue the chronology-first rebuild and ledger/supplement accountability work, especially where approval-facing review, provenance, and actor boundaries become reusable precursors for the broader governance control plane.

### M3: Governance control plane for ownership, approval, provenance, contribution, and handoff

**Goal**

- Define the first repo-wide governance control plane that answers who submitted something, who currently owns it, who approved it, who verified its evidence, how stewardship changed over time, and how contribution can later be viewed without confusing contribution with current responsibility.
- This milestone should start with `log -> ledger -> contract` and only later widen to runbook, evidence, and drills.
- The first opening should remain `DOC`-first: in practical lane ownership terms, `M3` should still begin inside docs/governance management rather than splitting immediately into a separate product/runtime stream.

**Opening stance**

- The first `M3` lane should be opened as one `DOC`-governed control-plane contract packet, not as a broad repo-wide schema program.
- The immediate execution surface should stay `docs/governance + source logs + ledgers + contracts`, because those surfaces already expose the ownership, approval, chronology, and evidence problems in reviewable form.
- The first expansion target after that should be `runbook / evidence / drills`, not tenant permissions; authorization and commercial gating belong to `M4`, not to `M3`.
- A later rename into a more product-neutral family is acceptable only after the first `DOC`-first packet proves the vocabulary is stable and reusable.

**Bridge Ledger (child logs only)**

- `M3-P0`:
  - `docs/logs/log-S0F-9A-doc-first-governance-control-plane-vocabulary-and-boundary.md`
- `M3-P1`:
  - `unmapped`
- `M3-P2`:
  - `unmapped`
- `M3-P3`:
  - `unmapped`

**Opening precursors**

- `S0F-7G`, `S0F-7H`, and `S0F-7I` remain the immediate precursor packet for `M3-P0`: they fixed screenshot-review readability, minimum packet-level actor/provenance accountability, and structure-integration audit boundaries before the first explicit `M3` child log was opened.

**Plan (P0-P3)**

- `P0` Contract: fix the minimum shared vocabulary for `actor`, `owner_team`, `current_steward`, `approval_state`, `approved_by`, `reviewed_by`, `contribution_event`, and `ownership_handoff_event`, while preserving the distinction between ownership, approval, contribution, and authorization.
- `P1` Implementation: apply the first minimal governance block to `log -> ledger -> contract`, keeping contract frontmatter focused on current effective responsibility and keeping event/history detail in ledgers or dedicated contribution/stewardship tables.
- `P2` Drill: prove handoff, steward replacement, approver separation, and evidence-verifier accountability on real docs-family samples before expanding the same protocol to runbook, evidence, and drills.
- `P3` Drill: add reader-facing views for current ownership, historical handoff, and aggregated contribution scoring without turning those views into false sources of governance truth.

**First lane packet (intended)**

- `M3-P0-A`: one bounded vocabulary-and-boundary lane that distinguishes `owner`, `steward`, `approver`, `reviewer`, `contributor`, and `verifier` without collapsing them into one overloaded `actor` field.
- `M3-P1-A`: one bounded `DOC` packet that applies those fields to `log -> ledger -> contract`, with frontmatter for current state and table/event surfaces for historical changes.
- `M3-P2-A`: one bounded handoff drill that proves leaving-person replacement, delegated stewardship, and retrospective provenance correction on representative docs-family samples.
- `M3-P3-A`: one bounded reader surface that answers three separate questions cleanly: who owns this now, who approved this current state, and who contributed materially over time.

**Current first packet**

- `S0F-9A` is now the first real `M3` child log and should be treated as the active vocabulary-and-boundary source packet for `M3-P0-A`.
- `DOC-CONTROL-PLANE-0001` now acts as the first landed reusable contract for that packet's shared current-state vocabulary, event-history placement rule, and authorization boundary.

**Exit signals**

- `M3` should be considered first-generation ready when readers can identify current ownership and approval without consulting prose history, and when stewardship handoff no longer requires ad hoc note-writing.
- `M3` should not be treated as mature merely because extra fields exist; the fields must support at least one real handoff, one approval separation case, and one contribution-vs-ownership distinction that survives replay.

### M4: Book-first access control and staged product closure on the current SoT

**Goal**

- Build the first simple but real access-control closure on the existing SoT by treating `book` as the first independent authorization container, keeping `block` as inherited content-only structure, and proving a minimum role-separated user/admin model before any larger entitlement or mock-billing design is allowed to widen the lane.
- After that minimum closure is stable, widen the same milestone in bounded packets for `plan / entitlement`, `payment_event -> subscription_state -> entitlement` semantics, and replayable scenario simulation, so the roadmap can support one real admin/user/mock-billing product loop rather than stopping at domain vocabulary only.
- The intended implementation target is still one module family inside the current backend modular monolith, plus thin frontend/admin validation surfaces, not one separate payment microservice.

**Opening stance**

- `M4` should open only after `M3` has fixed the governance vocabulary enough that authorization is not asked to carry ownership semantics.
- The first `M4` lane should stay on the current SoT rather than inventing a new platform surface, because the point is to prove permissions on resources the repo already understands.
- The first independent authorization surface should be `book`, not `block`.
- `block` should remain an editor/content unit that inherits the enclosing `book` standing rather than opening block-level ACL in v1.
- The first closure should stay minimum and policy-first:
  - separate ordinary user roles from platform/system admin roles
  - do not freeze a complex commercial plan matrix yet
  - keep `plan` and later `entitlement` as reserved extension concepts rather than as the first lane's main complexity driver
- No real payment provider, tax/invoice realism, or enterprise policy sprawl should enter the opening lane.
- The widening after the minimum closure should still follow the repo's current mixed `DDD/HEX + modular-monolith` structure rather than inventing a second architectural style just for billing/access:
  - domain and application logic should live under one bounded backend module family in `backend/api/app/modules/...`
  - persistence models should continue to land under `backend/infra/database/models/...`
  - repository implementations should continue to land under `backend/infra/storage/...`
  - frontend validation surfaces should remain thin and should primarily exercise the backend state model instead of duplicating policy logic in the browser

**Bridge Ledger (child logs only)**

- `M4-P0`:
  - `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
  - `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
  - `docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
- `M4-P1`:
  - `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
  - `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
  - `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
  - `docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md`
  - `docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md`
- `M4-P2`:
  - `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
  - `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
  - `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- `M4-P3`:
  - `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`

**Plan (P0-P3)**

- `P0` Contract: fix the minimum access model for `user`, `membership`, `book role`, `system role`, `book` as the first independent authorization object, and `block` as inherited content structure; then widen the same contract into `plan`, `entitlement`, `subscription_state`, and scenario replay without collapsing those concepts back into role semantics.
- `P1` Implementation: map that model onto the current SoT through a minimum `book` action set such as `read_book`, `edit_book`, `share_book`, `delete_book`, `transfer_book_owner`, and `manage_book_members`, while keeping `block` under inherited `book` standing; then land the first backend module and admin/user/mock-billing surfaces that can compute and expose `entitlement_snapshot`.
- `P2` Drill: prove one minimum replayable role flow such as owner grants editor, editor edits but cannot re-share, owner revokes access, and system admin can perform bounded platform override without becoming a normal collaboration role; then prove one scenario-driven replay where lifecycle standing changes effective entitlement without mutating role or override semantics.
- `P3` Drill: decide whether later provider realism should stay outside the first closure, and define the handoff rule by which one future provider-adapter packet may translate real external signals into trusted replay inputs without reopening the already-stable role, entitlement, or scenario contracts.

**First lane packet (intended)**

- `M4-P0-A`: one bounded access-model contract that fixes `user`, `membership`, `book_role`, and `system_role` as separate concepts, while reserving `plan` and `entitlement` for later widening.
- `M4-P1-A`: one bounded resource-action matrix centered on `book` as the first independent authorization container, with `block` inheriting `book` standing and no block-level ACL in v1.
- `M4-P2-A`: one bounded role-flow drill covering share, edit, revoke, owner transfer boundary, and system-admin override on the same `book` surface.
- `M4-P3-A`: one bounded widening decision on whether `plan / entitlement / mock billing` should remain deferred, be partially introduced, or open as a second-stage packet after the minimum closure is stable.

**Current first packet**

- `S0F-10A` now acts as the stable minimum-closure source packet for `M4-P0` through `M4-P3`.
- That packet fixes the first `book`-first role boundary, the first replayable share/revoke and override drills, and the first widening decision that keeps `plan / entitlement` deferred while splitting `mock billing` to a later packet.

**Current widening packets**

- `S0F-10B` now acts as the stable entitlement-boundary widening packet for `M4`, fixing `plan / entitlement / subscription_state` as separate concepts rather than hidden extensions of ordinary collaboration role.
- `S0F-10C` now acts as the stable trigger-chain widening packet for `M4`, fixing `payment_event -> subscription_state -> entitlement outcome` semantics without introducing provider realism.
- `S0F-10D` now acts as the stable scenario-replay widening packet for `M4`, fixing the first realistic replay catalog and mock-state-machine drill surface on top of `10A/10B/10C`.

**Immediate next closure after the current widening stack**

- The next `M4` lane should not widen payment realism first; it should close the first real tenant-facing product entry surface on top of the already-stable access and subscription slices.
- That next lane should treat `Workbox` as the stable control-plane entry rather than continuing to scatter access or subscription surfaces across `library` or `bookshelf` content pages.
- The next lane should explicitly separate `user-facing account/subscription visibility` from `tenant-admin governance visibility` while preserving one shared backend access-context contract.
- The next lane should also fix the first minimum auth-entry assumptions so protected pages are no longer treated as direct-click surfaces without login or role-aware routing.

**Immediate next packet candidates (intended)**

- `M4-P1-B`: one bounded `tenant-admin vs user workbox entry` packet that moves subscription and access surfaces under `Workbox`, keeps `user` on a light `My Subscription` view, and restricts `event history`, mutation controls, and broader tenant governance views to `tenant admin` only.
- `M4-P1-C`: one bounded `login / registration / routed entry` packet that defines one shared login surface, one minimum registration flow, post-login role-aware landing rules, and fail-closed route gating for unauthenticated or non-admin users.
- `M4-P0-B`: one bounded `tenant identity and data ownership` packet that fixes `tenant`, `membership`, `current tenant context`, and `tenant_id` as the primary ownership boundary for product data rather than treating database count as the first multi-tenant design lever.
- `M4-P0-C`: one bounded `shared relational storage vs object storage boundary` packet that keeps the first implementation on shared relational storage with strong tenant scoping, while reserving object storage for files, exports, and larger asset/blob lifecycles rather than for core subscription or membership truth.

**Implementation shape on the current repo architecture**

- The backend should continue the repo's current mixed `DDD/HEX + modular-monolith` pattern rather than splitting this capability into a separate runtime prematurely.
- The intended backend landing shape is one bounded module family for the commercial-access closure, tentatively `subscription_access` or equivalent, with this structure:
  - `backend/api/app/modules/<module>/domain`: `Plan`, `Subscription`, `PaymentEvent`, `EntitlementSnapshot`, and related policy/value objects
  - `backend/api/app/modules/<module>/application`: use cases such as `ApplyPaymentEvent`, `ComputeEntitlementSnapshot`, `GetAccessContext`, `RunScenarioReplay`
  - `backend/api/app/modules/<module>/routers`: admin and user-facing HTTP entrypoints
  - `backend/api/app/modules/<module>/schemas`: request/response DTOs for access context, admin events, and replay results
  - `backend/api/app/modules/<module>/repository`: repository interfaces or ports needed by the domain/application layer
- The intended infrastructure landing shape should stay parallel to the existing repo patterns:
  - `backend/infra/database/models`: tables/models for `plan_catalog`, `subscription`, `payment_event`, and `entitlement_snapshot` or their equivalent persistence shapes
  - `backend/infra/storage`: repository implementations for the new module ports
  - existing auth/membership infrastructure should remain the source of collaboration role standing and should not be rewritten into the new commercial-access module
- The intended aggregation rule is:
  - current `AuthContext` or its successor continues to answer identity, tenant/library selection, and ordinary role standing
  - the new module computes commercial lifecycle and entitlement outcome
  - one higher-level access-context surface combines both for frontend/API consumers
- The intended multi-tenant data-ownership rule is:
  - `tenant` or equivalent workspace/library container remains the first data-ownership boundary for business records
  - `membership` remains the join that grants one user a role inside one tenant rather than turning account identity into implicit global authority
  - one user may later belong to multiple tenants, so `current tenant context` should be explicit in routing, session, and query boundaries
  - the default early-stage storage stance should remain `shared database + shared schema + explicit tenant_id scoping`, not `one database per simulated tenant`
  - per-tenant databases should remain a later enterprise or compliance widening only if isolation, residency, backup, or scale pressure justifies the operational cost
- The intended storage-boundary rule is:
  - relational storage remains the source of truth for identity, membership, subscription, entitlement, library, bookshelf, and book metadata
  - object storage should later hold files, uploads, exports, covers, and other blob-like assets, but should not replace relational multi-tenant truth
- The intended frontend validation surfaces for the first product closure are:
  - one `user` workspace/access view that shows current role, plan, subscription standing, entitlement snapshot, and gated actions
  - one `admin` subscription console that can inspect tenant state and apply bounded admin/payment events
  - one mock billing panel that emits controlled local events such as `upgrade_success`, `renewal_failed`, `cancellation_requested`, `refund_applied`, and `admin_correction`
  - one scenario replay console or equivalent debug view that runs the first bounded `10D` drills end to end and returns step-by-step results plus invariant checks
- The intended frontend validation surfaces for the next tenant-facing entry closure are:
  - one `Workbox > My Subscription` user view that shows only the current user's standing, plan, and gated capabilities without exposing admin event history or mutation controls
  - one `Workbox > Subscription Console` tenant-admin view that shows tenant-wide state, drill-down capability, and bounded admin-only operational surfaces
  - one minimum auth shell with login, registration, protected-route gating, and role-aware menu visibility so admin-only views stop depending on direct local navigation
- The first validation loop should remain local-first and should prove:
  - user-facing capability widening after successful activation
  - capability narrowing or suspension after lifecycle degradation
  - preserved collaboration role and override semantics throughout the commercial-state change

**Exit signals**

- `M4` should be considered first-generation ready when a reader can answer who may read, edit, share, and administer one `book`, what a system admin may override, and why `block` still inherits `book` standing rather than carrying its own ACL.
- `M4` should not be treated as mature merely because a permission matrix exists; at least one owner/editor/share-revoke flow and one bounded system-admin override case should be replayable through the same model.
- `M4` should be considered product-closure-ready only when one admin/user/mock-billing loop can run against the current SoT and show `payment_event -> subscription_state -> entitlement outcome` changes without mutating collaboration-role standing.
- `M4` should still avoid real provider integration until one later packet can justify why local event simulation is no longer sufficient.

**Recent Changes**

- 2026-04-15: opened `S0F-10A` as the first real `M4` child log and fixed `M4-P0` as a book-first minimum access packet rather than a billing-first design exercise.
- 2026-04-15: completed `S0F-10A/P1-C1-S1S2` and `P2-C1-S1S2`, so `M4-P1` and `M4-P2` now bridge to the first role matrix and replay drills on the same packet.
- 2026-04-15: completed `S0F-10A/P3-C1-S1S2`, so `M4-P3` now bridges to an explicit widening decision that keeps `plan / entitlement` deferred and splits `mock billing` into later work.
- 2026-04-15: completed `S0F-10B`, `S0F-10C`, and `S0F-10D`, so `M4` now has stable widening packets for entitlement boundary, trigger-chain semantics, and scenario replay rather than only one minimum role packet.
- 2026-04-16: extended the `M4` roadmap body from domain-only boundary language into one concrete product-closure blueprint, aligning the next implementation surface with the repo's current mixed `DDD/HEX + modular-monolith` structure and with one admin/user/mock-billing validation loop.
- 2026-04-16: stabilized the first backend and frontend/admin subscription-access validation slices, proving one local admin/user/mock-billing loop before the next product-entry and tenant-boundary packets are opened.
- 2026-04-16: added the next `M4` roadmap intent for `tenant admin vs user Workbox entry`, `login / registration / routed entry`, and `tenant data ownership / shared relational storage boundary`, so the next lane can close real SaaS entry and tenant-scoping gaps rather than widening payment realism prematurely.
- 2026-04-17: opened `S0F-9F` as the first explicit `M4-P0-B` child lane for tenant identity, data ownership, and current-tenant context, so the next runtime slice can widen tenant scoping before auth-provider realism or tenant analytics.
- 2026-04-17: opened `S0F-9G` as the next explicit `M4-P1` child lane for backend tenant-admin enforcement, minimum tenant membership management, and local actor-switching, so the current admin/user product-entry split can widen into one stronger permission loop without payment-provider realism.
- 2026-04-17: completed `S0F-9G` through `P3`, so `M4-P1` now has one stable child packet for backend tenant-admin enforcement, tenant-scoped membership management, and bounded local actor switching on top of the current Workbox/auth entry stack.
- 2026-04-19: opened `S0F-9H` as the next explicit `M4-P1-C` child lane for shared auth/provider realism, invite/onboarding, membership admission, and routed entry, so the current Workbox/auth stack can widen beyond local-first role fabrication without opening support tooling first.
- 2026-04-19: completed `S0F-9H/P1-C1-S1S2`, so `M4-P1-C` now has the first code-bearing child slice for identity-first auth entry, explicit local-first membership admission, and pending-to-admitted standing on the current Workbox/auth stack.
- 2026-04-19: completed `S0F-9H/P2-C1-S1S2`, so `M4-P1-C` now has tenant-aware routed entry with safe-`next` preservation and tenant-scoped admin landing on the current Workbox/auth stack.

### M5: Asset platform activation after governance and access baselines exist

**Goal**

- Admit an asset platform only after the repo already has workable governance and access control planes, so media/attachment/object handling can inherit real ownership, approval, entitlement, retention, and audit semantics rather than becoming another isolated module with implicit rules.

**Bridge Ledger (child logs only)**

- `M5-P0`:
  - `unmapped`
- `M5-P1`:
  - `unmapped`
- `M5-P2`:
  - `unmapped`
- `M5-P3`:
  - `unmapped`

**Plan (P0-P3)**

- `P0` Contract: decide the stable platform name and boundary, preferring `Asset Platform` or similar capability language rather than a narrow `media`-only framing.
- `P1` Implementation: define the first object model for blob/ref lifecycle, storage backends, attachment classes, audit attachment handling, retention, and signed access paths, but only after M3 and M4 have produced reusable control surfaces.
- `P2` Drill: prove that assets can participate in the same approval, entitlement, and audit story as the rest of the system, including export packages, attachments, and future evidence artifacts.
- `P3` Drill: decide whether the capability remains a module inside the modular monolith or has become platformized enough to justify a stronger deployment/runtime boundary later.

## Evidence Pointers (cross-log)

- `docs/logs/log-S0E-docs-management-v5.md` currently provides the clearest already-realized surface for semi-automated docs/GitHub lifecycle control.
- `docs/logs/log-S0F-docs-management-v6.md` currently provides the clearest already-realized surface for docs governance, chronology-first contracts, and approval/provenance precursors.
- `docs/roadmap/_draft/road-S2-.md` currently holds the strongest draft material for the future governance-control-plane and access-control-plane framing, especially around ownership, handoff, tenant/plan/entitlement, and mock billing closure.
- `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md` now opens the first `M4-P0` child lane around book-first minimum closure, user/admin role separation, and block inheritance.
- `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`, `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`, and `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md` now complete the first `M4` widening stack for entitlement boundary, trigger semantics, and scenario replay.

## Recent Changes (optional)

- 2026-04-14: created the first `road-002` mainline draft to absorb the existing `S0E` and `S0F` progress, while reserving the next major backbone slots for governance control plane, tenant access control, and later asset-platform admission.
- 2026-04-14: refined `M3` and `M4` into lane-opening shape, fixed the first `DOC`-first stance for governance-control rollout, and made explicit that access control remains a separate second control plane rather than a hidden extension of ownership semantics.
- 2026-04-15: opened `S0F-9A` as the first real `M3` child log, moved `M3-P0` from borrowed precursor context into one explicit `DOC`-first vocabulary-and-boundary packet, and retained `S0F-7G/7H/7I` as opening precursors rather than as the bridge ledger itself.
- 2026-04-15: landed `DOC-CONTROL-PLANE-0001` as the first reusable `M3-P0` contract, and used two bounded `S0F-9A` sample rounds to justify the shared current-state vocabulary, event-history placement rule, and `M3` versus `M4` boundary.
- 2026-04-15: revised `M4` into a book-first minimum-closure opening, mapped `M4-P0` to `S0F-10A`, and made explicit that the first authorization lane should separate ordinary user roles from system-admin override while keeping `block` under inherited `book` standing.
- 2026-04-15: completed the first `S0F-10A` minimum closure packet through `M4-P1` and `M4-P2` by fixing a first `book` action matrix plus one replayable owner/editor/share-revoke and system-admin override drill, while still deferring `plan / entitlement / mock billing` to later widening.
- 2026-04-16: recorded the next `M4` follow-up shape directly in the mainline roadmap, separating `tenant admin vs user entry and login design` from `tenant data ownership and storage-boundary design` so the next lane can target product entry and multi-tenant scope cleanly.