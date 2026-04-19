# log-S0F-9F (Phase 9F: tenant identity, data ownership, and current-tenant context)

---

**id**: `S0F-9F`
**kind**: `log`
**title**: `tenant identity, data ownership, and current-tenant context minimum closure + drills/evidence + v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Access, Tenancy, Auth, Runtime, Drills, Evidence, epic/s0, sub/9f`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-9E-workbox-subscription-entry-auth-routing-and-admin-view-gating.md`
  **reference_log_1**: `docs/logs/log-S0F-9E-workbox-subscription-entry-auth-routing-and-admin-view-gating.md`
  **reference_log_2**: `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
  **reference_log_3**: `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
  **reference_log_4**: `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
**issue_keyword**: `runtime`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/9f`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M4`
**roadmap_phase**: `M4-P0`
**roadmap_bridge_refs**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md#M4-P0`
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-17`
**updated**: `2026-04-17`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this lane.
- Day-level precision is acceptable while this packet is still fixing the first tenant-boundary contract rather than one already-reviewed multi-tenant runtime model.
- If this lane later splits identity vocabulary, session/current-tenant routing, and storage-boundary rules into separate packets, the source log must still retain the current execution checklist, status, and evidence ledger.

## Decision / Outcome

**Decision**:

- `S0F-9F` opens as the next lane after `S0F-9E`, with the narrow goal of fixing the first explicit tenant-boundary contract behind the newly-stable product entry model.
- This packet should define `tenant`, `membership`, `current tenant context`, and `tenant_id` as the primary ownership boundary for product data, session routing, and query scoping.
- The first deliverable is one minimum closure across three surfaces only:
  - one stable tenant identity vocabulary for backend/frontend/runtime use
  - one explicit current-tenant-context rule for routing, session, and query boundaries
  - one first-pass data-ownership rule that keeps relational truth tenant-scoped instead of database-count-driven
- This packet is not the place to widen real auth-provider realism, deeper tenant analytics, or support/platform-admin tooling; it exists to close the first tenant-boundary gap under the now-stable `9E` entry model.

**Default choices (phase defaults / v1)**:

- Keep `tenant` or equivalent workspace/library container as the first ownership boundary for product records.
- Keep `membership` as the join that grants one user a role inside one tenant; do not collapse tenant standing into global account identity.
- Keep `current tenant context` explicit in routing, session, and query boundaries; do not infer it indirectly from whichever library or page happened to load first.
- Keep the early-stage storage stance as shared relational storage with explicit `tenant_id` scoping; do not jump to one-database-per-tenant as the opening answer.
- Keep auth-provider realism, analytics widening, and platform-admin/support-only views out of this packet unless one concrete tenant-boundary decision requires them.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S0F-9F` is intended to drive the first PR that closes the tenant-boundary contract under the now-stable Workbox/auth entry slice.

**PR summary bullets**:

- Fix the first tenant identity and membership vocabulary so product data has one explicit ownership boundary.
- Make current-tenant context explicit in routing, session, and query behavior rather than implicit page-local state.
- Keep the first storage stance on shared relational truth with tenant scoping, while deferring richer auth realism and tenant analytics to later packets.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
- Runbook: ``
- Evidence artifact: `artifacts/_tmp_s0f_9f_p0_tenant_boundary_contract.json`

**Evidence Footer Source**:

- `P0-C1-S1S2S3` | artifact: `artifacts/_tmp_s0f_9f_p0_tenant_boundary_contract.json`

## Exported Sections / Outlet Ownership

- This slice opens as one log-retained source packet because tenant vocabulary, current-tenant-context routing, and storage-boundary assumptions are still changing together.
- Stable extraction should wait until there is one accepted tenant-boundary contract rather than exporting premature fragments into separate outlets.

**Outlet ownership**:

- `contract`: keep the first tenant identity, membership, current-tenant-context, and data-ownership rule set in this log until the packet stabilizes
- `runbook`: no-op at packet open; repeatable operator steps should wait until there is one stable local tenant-context drill path
- `view`: no-op at packet open; a reader-facing tenant-boundary summary can be exported later if the vocabulary and context model stabilize
- `index/front-door`: no-op at packet open; the current packet is backend/runtime-boundary-first rather than navigation-first
- `disposition/placement`: no-op at packet open
- `log-retained core`: scope boundary, defaults, checklist, current status, and evidence ledger remain here

## Definitions (optional)

- `tenant`: the primary product ownership boundary for records, membership, and access standing in this packet.
- `membership`: the relation that attaches one user/account to one tenant with one bounded role standing.
- `current tenant context`: the explicit tenant selection or binding used by routing, session, and queries when one user may belong to multiple tenants.
- `tenant_id`: the persistence-level ownership key that scopes relational truth for tenant-bound records.
- `tenant-scoped record`: one product record whose lifecycle and visibility belong to exactly one tenant unless a later packet explicitly defines cross-tenant rules.

## Constraints

- Do not infer tenant ownership from ad hoc page placement, bookshelf nesting, or whichever library page is currently open.
- Do not open one-database-per-tenant as the default first answer.
- Do not use this packet to widen real auth-provider integration, tenant analytics, or support/debug operations.
- Do not reopen the already-stable `9E` entry contract unless one concrete tenant-boundary rule truly requires one explicit replacement packet.
- Do not let one later multi-tenant design depend on invisible implicit state; routing, session, and query boundaries must be explicit enough to drill.

## Scope

- `P0`: contract for tenant identity vocabulary, membership semantics, current-tenant-context rule, and evidence contract
- `P1`: implement the minimum tenant-boundary surface in routing/session/query terms and the first thin validation hooks
- `P2`: drill and verify tenant-context selection, tenant-scoped data access, and non-implicit ownership behavior
- `P3`: close out the tenant-boundary packet and define handoff into richer auth/provider realism or tenant analytics without reopening the first ownership model

## Success Criteria (DoD)

- The lane fixes `tenant`, `membership`, `current tenant context`, and `tenant_id` as explicit first-class concepts.
- One user can be reasoned about as belonging to one or more tenants without collapsing tenant standing into global account identity.
- Routing, session, and query boundaries expose one explicit current-tenant-context rule rather than implicit page-local selection.
- The opening storage stance is explicit enough to say why shared relational truth plus tenant scoping is the current default.
- The lane records evidence for tenant-boundary contract, implementation slice, and verification drills with traceable artifacts.
- Later auth-provider realism and tenant analytics can widen without reopening the first ownership model.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the first tenant identity and membership vocabulary is fixed and no longer depends on prose-only interpretation
  - one current-tenant-context rule exists for routing, session, and query behavior
  - one focused drill proves tenant-scoped access and non-implicit ownership behavior
  - the Evidence section includes traceable `headSha` values plus artifact paths
  - the next-lane handoff rule is explicit for richer auth/provider realism, tenant analytics, or storage-boundary widening
- `stable` for this packet means tenant ownership and current context no longer depend on incidental page state or hidden inference.

## P0 (Contract | v1)

### P0-C1-S1 (Tenant identity and membership contract)

- `tenant` is the primary product ownership boundary for this packet.
- `membership` is the join that grants one user one bounded role inside one tenant.
- One user may later belong to multiple tenants, so tenant standing must not be derived from account identity alone.
- The first packet should answer identity and ownership vocabulary before deeper auth-provider realism exists.

### P0 Tenant Identity And Membership Decision (v1)

- `P0` now fixes the first tenant-boundary vocabulary in this lane as:
  - `tenant` = the first ownership boundary for product records, membership standing, and tenant-scoped access
  - `membership` = the join that grants one user one bounded standing inside one tenant
  - `user/account identity` = the global principal identity, not implicit authority inside every tenant
- The first membership rule in this packet is now fixed as:
  - one user may later belong to multiple tenants through multiple memberships
  - tenant standing must be resolved from membership plus current tenant context rather than from page-local state
  - losing or changing membership standing changes tenant authority without redefining account identity

### P0-C1-S2 (Current-tenant-context and data-ownership contract)

- `current tenant context` must be explicit in routing, session, and query boundaries in v1.
- Tenant-scoped records must carry one explicit ownership boundary such as `tenant_id` or equivalent.
- The opening storage stance remains shared relational truth plus strong tenant scoping; object storage and per-tenant databases remain later widening decisions.
- The first fail-closed rule in this packet is that tenant-scoped data must not resolve through implicit or stale tenant context.

### P0 Current-Tenant-Context And Data-Ownership Decision (v1)

- `P0` now fixes the first current-tenant-context rule in this lane as:
  - routing must bind or resolve one explicit tenant context before tenant-scoped UI renders
  - session may remember the last active tenant, but that remembered value remains one explicit field rather than hidden implicit state
  - query boundaries must use explicit current tenant context or an equivalent server-resolved tenant binding
- `P0` now fixes the first data-ownership rule in this lane as:
  - tenant-scoped relational records carry `tenant_id` or one equivalent ownership key
  - shared database plus shared schema plus explicit tenant scoping remains the opening default
  - object storage is reserved for later blob/file lifecycles and must not replace relational ownership truth in this packet

### P0 Storage Boundary Decision (v1)

- `P0` now fixes the first storage stance under the tenant-boundary packet as shared relational truth with explicit tenant scoping.
- This lane explicitly does not treat `one database per tenant` as the first multi-tenant answer.
- Per-tenant databases, provider-real auth authority, and tenant analytics remain later widening candidates after this ownership model is explicit.

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - `tenantVocabulary`
  - `membershipSemantics`
  - `currentTenantContextCases`
  - `tenantScopedRecordRules`
  - `storageBoundaryDefaults`
  - `passFail`

### P0 Evidence Contract Decision (v1)

- `P0` now requires one tenant-boundary contract artifact before implementation lands.
- The first artifact path in this packet is fixed as `artifacts/_tmp_s0f_9f_p0_tenant_boundary_contract.json`.
- The artifact now records tenant vocabulary, membership semantics, explicit current-tenant-context cases, tenant-scoped record rules, and storage-boundary defaults in one auditable packet.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-9F/P<phase>-C<cycle>-S<steps>: <summary>`
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0F-9F/P0-P3: tenant identity, data ownership, and current-tenant context minimum closure`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title.

**Branch convention**:

- This lane belongs to the active `S0F-*` family because it directly widens the first product/runtime closure on top of the `9E` product-entry and auth-routing packet.
- If the tenant-boundary work later splits into a larger multi-tenant stream, one later split may be justified, but this packet should start on the current scope branch.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, commit and push promptly with one evidence note in the log.
- Prefer one commit for `P0`, one for the minimum tenant-context implementation slice, one for verification drills, and one backfill commit if `headSha` needs to be recorded later.

## Plan (draft)

### P1 (Tenant-boundary implementation slice)

- `P1-C1-S1`: land the first tenant identity and membership surface in the current runtime vocabulary
- `P1-C1-S2`: land the first explicit current-tenant-context handling in routing, session, and query boundaries

## P1 (Tenant-boundary implementation slice)

- `P1` lands the first thin runtime surface for the tenant-boundary contract without widening into full auth-provider realism or deep multi-tenant backend redesign.
- The implementation goal in this packet is to stop treating active tenant/library scope as incidental local page state and instead expose one shared explicit runtime surface that later routes and queries can consume directly.
- `P1` remains intentionally thin: it may use the current `libraryId` as the v1 tenant-context carrier, but it must make that carrier explicit in auth/runtime behavior rather than hidden in ad hoc localStorage writes.

### P1 Tenant Runtime Surface Decision (v1)

- `P1` now lands the first explicit tenant runtime surface in the shared auth layer through:
  - `currentTenantContext`
  - `currentTenantId`
  - `setCurrentTenantContext(...)`
  - `clearCurrentTenantContext()`
- The first compatibility rule in this packet is now fixed as:
  - explicit tenant context persists through one dedicated storage shape
  - legacy `wl_active_library_id` remains as compatibility storage during the transition
  - the current runtime still uses `libraryId` as the v1 tenant-context carrier until a later packet widens the domain model further

### P1 Current-Tenant Handling Decision (v1)

- `P1` now fixes the first explicit current-tenant handling rule across three runtime surfaces:
  - shared auth/session state owns the explicit current tenant context
  - tenant-facing entry pages mutate current tenant context through shared runtime state instead of direct localStorage writes
  - the API client derives request scope from explicit current tenant context before falling back to legacy active-library storage
- The first route-binding rule in this packet is now fixed as:
  - `/admin/subscriptions/[libraryId]` binds current tenant context from the route
  - admin and user subscription entry pages reuse the same shared runtime surface for current tenant selection

### P2 (Tenant-context drill / verify)

- `P2-C1-S1`: verify tenant-scoped data resolves only under explicit current-tenant context
- `P2-C1-S2`: verify implicit or stale tenant selection does not retain cross-tenant access behavior

## P2 (Tenant-context drill / verify)

- `P2` validates the new tenant runtime surface through executable browser behavior instead of relying on contract-only interpretation.
- The drill should prove that explicit current tenant context is preferred over stale compatibility storage and that route-bound tenant detail pages correct stale context rather than preserving it.
- `P2` also acts as the first stability check for the `9F` runtime slice, so any failure here belongs to this packet before close-out handoff begins.

### P2 Tenant-Context Drill Decision (v1)

- `P2` now fixes the first explicit tenant-context verification surface in this lane as one focused Playwright drill.
- The first two scenarios in this packet are now fixed as:
  - explicit `currentTenantContext` remains the preferred runtime scope even when legacy `wl_active_library_id` is stale
  - route-bound `/admin/subscriptions/[libraryId]` overwrites stale tenant runtime state and compatibility storage with the route-bound value
- The `P2` success rule in this packet is:
  - one reader can show that the runtime prefers explicit tenant context over compatibility fallback
  - one reader can show that stale tenant context does not survive route-bound correction on tenant detail pages

### P3 (Close-out / handoff)

- `P3-C1-S1`: freeze the first stable tenant-boundary and current-context behaviors
- `P3-C1-S2`: define the downstream handoff rule into richer auth/provider realism or tenant analytics without reopening v1 ownership design

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: fix the first tenant identity and membership vocabulary
- [x] `P0-C1-S2`: fix the first current-tenant-context and data-ownership rule
- [x] `P0-C1-S3`: create the first evidence artifact contract for tenant-boundary verification

### P1 (Tenant-boundary implementation slice)

- [x] `P1-C1-S1`: implement the first tenant identity and membership surface in the current runtime slice
- [x] `P1-C1-S2`: implement the first explicit current-tenant-context handling across routing/session/query boundaries

### P2 (Tenant-context drill / verify)

- [x] `P2-C1-S1`: verify tenant-scoped access behavior under explicit current-tenant context
- [x] `P2-C1-S2`: verify implicit or stale tenant context does not preserve cross-tenant behavior

### P3 (Close-out / handoff)

- [ ] `P3-C1-S1`: freeze the first stable tenant-boundary and current-context behaviors
- [ ] `P3-C1-S2`: define the downstream handoff rule without reopening v1 ownership design

## Current Status (recommended)

- `S0F-9F/P0` is now complete: the first tenant identity vocabulary, membership semantics, explicit current-tenant-context rule, and shared-relational storage stance are fixed in one contract artifact.
- `S0F-9F/P1` is now complete: the frontend runtime now exposes one explicit current-tenant surface, and the user/admin subscription entry pages plus API request scope now consume that shared surface instead of direct page-local localStorage mutation.
- `S0F-9E` remains the stable source for product entry and first auth-routing behavior, while `S0F-9F` now acts as the active draft source for tenant-boundary drills and later close-out.
- `S0F-9F/P2` is now complete: the focused browser drill proves explicit tenant-context precedence and route-bound correction behavior on the current runtime slice.
- The next step is now `P3` close-out and handoff rather than more tenant-context implementation widening, because the packet now has contract, runtime slice, and executable drill evidence.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths.
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2S3 (Tenant-boundary contract fixed | 2026-04-17)

- headSha: `2114d5839`
- artifacts: `artifacts/_tmp_s0f_9f_p0_tenant_boundary_contract.json`
- expected:
  - one contract artifact fixes tenant vocabulary, membership semantics, current-tenant-context behavior, and storage defaults before implementation starts
  - later runtime work can answer tenant ownership and query/session scoping without relying on page-local inference
- observed:
  - `tenant`, `membership`, `current tenant context`, and `tenant_id` are now fixed as the first explicit tenant-boundary vocabulary in this packet
  - the first routing/session/query rule now requires explicit current tenant context instead of hidden incidental state
  - the first storage stance is now fixed as shared relational truth plus explicit tenant scoping, with object storage and per-tenant databases deferred

### P1-C1-S1S2 (Explicit current-tenant runtime landed | 2026-04-17)

- headSha: `07b918eb6`
- artifacts: `artifacts/_tmp_s0f_9f_p1_current_tenant_runtime_impl.json`
- expected:
  - one explicit current-tenant runtime surface exists for auth/session consumers and tenant-facing entry pages
  - request scoping prefers explicit tenant context instead of relying only on implicit active-library localStorage
  - the existing subscription entry and admin gating behavior remains intact after the runtime-surface change
- observed:
  - `AuthContext` now exposes `currentTenantContext`, `currentTenantId`, and explicit mutators for tenant-bound runtime state
  - user/admin subscription entry pages and the admin subscription detail route now read or bind tenant context through the shared runtime surface
  - the shared API client now prefers explicit tenant context storage and emits both `X-Library-Id` and `X-Tenant-Id` when it resolves scoped requests
  - `npm run test:e2e -- tests/e2e/subscription-gating.spec.ts` passed (`3 passed`) after the runtime-surface change

### P2-C1-S1S2 (Tenant-context drill passed | 2026-04-17)

- headSha: `5686bb6a5`
- artifacts: `artifacts/_tmp_s0f_9f_p2_tenant_context_verify.json`
- expected:
  - explicit current tenant context remains the preferred runtime scope even when legacy active-library storage is stale
  - route-bound tenant detail pages correct stale tenant runtime state instead of preserving cross-tenant behavior
- observed:
  - `frontend/tests/e2e/tenant-context.spec.ts` passed two focused Chromium scenarios covering explicit tenant-context precedence and route-bound correction of stale compatibility storage
  - the drill verifies that `/admin/subscriptions` renders the explicit tenant runtime value instead of the stale fallback value
  - the drill verifies that `/admin/subscriptions/[libraryId]` rewrites both `wl_current_tenant_context` and `wl_active_library_id` to the route-bound tenant value

## Recent changes (for traceability, optional)

- 2026-04-17: opened `S0F-9F` as the next tenant-boundary lane after `S0F-9E`, targeting tenant identity, data ownership, and explicit current-tenant context rather than widening auth-provider realism or tenant analytics first.
- 2026-04-17: completed `S0F-9F/P0-C1-S1S2S3` by fixing the first tenant-boundary contract, explicit current-tenant-context rule, and shared-relational ownership stance in one auditable artifact.
- 2026-04-17: completed `S0F-9F/P1-C1-S1S2` by landing the first explicit current-tenant runtime surface in shared auth state, binding tenant context from subscription entry routes, and validating that the existing subscription gating drill still passes.
- 2026-04-17: completed `S0F-9F/P2-C1-S1S2` by adding one focused Playwright drill for explicit tenant-context precedence and route-bound correction of stale compatibility storage.