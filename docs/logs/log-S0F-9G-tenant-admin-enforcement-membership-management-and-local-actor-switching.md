# log-S0F-9G (Phase 9G: tenant-admin enforcement, membership management, and local actor switching)

---

**id**: `S0F-9G`
**kind**: `log`
**title**: `tenant-admin enforcement, membership management, and local actor-switching minimum closure + drills/evidence + v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Access, Auth, Membership, Runtime, Drills, Evidence, epic/s0, sub/9g`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
  **reference_log_1**: `docs/logs/log-S0F-9D-frontend-admin-consumer-lane-for-subscription-access-closure.md`
  **reference_log_2**: `docs/logs/log-S0F-9E-workbox-subscription-entry-auth-routing-and-admin-view-gating.md`
  **reference_log_3**: `docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
  **reference_log_4**: `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
**issue_keyword**: `runtime`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/9g`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M4`
**roadmap_phase**: `M4-P1`
**roadmap_bridge_refs**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md#M4-P1`
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
- Day-level precision is acceptable while this packet is still closing the first local-first permission loop rather than one already-reviewed tenant-governance surface.
- If this lane later splits backend admin enforcement, tenant membership UI, and local actor-switching into separate child packets, the source log must still retain the execution checklist, current status, and evidence ledger.

## Decision / Outcome

**Decision**:

- `S0F-9G` opens as the next lane after `S0F-9F`, with the narrow goal of closing the first real `tenant admin vs user` permission loop across backend authority, minimum membership operations, and reproducible local actor switching.
- This packet should turn the currently-stable frontend entry split from `9E` and the explicit tenant-context runtime from `9F` into one stronger admin/user closure where backend admin routes stop depending on frontend-only hiding and operators no longer have to hand-edit browser session state to simulate users.
- The first deliverable is one minimum closure across three surfaces only:
  - one backend admin-policy boundary for subscription-admin routes and related tenant-governance actions
  - one minimum tenant membership management surface that can list, grant, and revoke standing inside the selected tenant
  - one local actor-switching or seed-console surface that makes member/admin/owner drills reproducible without manual storage edits
- This packet is not the place to widen real auth-provider realism, platform-support impersonation, cross-tenant operations, or payment-provider realism; it exists to close the first enforceable tenant-admin/user runtime loop on the current SoT.

**Default choices (phase defaults / v1)**:

- Keep backend authorization as the final authority; frontend menu and route gating must align with backend policy but must not replace it.
- Keep the first membership-management surface narrow: one tenant-scoped list plus bounded grant/revoke actions is enough for v1.
- Keep the first actor-switching surface local-first and explicitly non-production; it exists to support drills and developer verification, not real impersonation or support tooling.
- Keep the loop tenant-scoped: membership changes and admin actions must stay bound to the currently selected tenant context.
- Do not reopen the already-stable commercial lifecycle semantics from `10B/10C/10D`; this lane consumes those semantics rather than redefining them.
- draft 阶段默认继续把 source log 当作集中面；如果 backend policy、membership UI、actor-switching flow 仍在一起变化，不要过早把 weak-structure 内容拆到多个 outlets。
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S0F-9G` is intended to drive the next packet that turns the current UI split into one stronger tenant-admin/user permission closure.

**PR summary bullets**:

- Add backend admin/owner enforcement for subscription-admin routes so tenant-admin views no longer depend on frontend-only gating.
- Land one minimum tenant membership-management surface for listing, granting, and revoking tenant standing inside the selected tenant.
- Add one local actor-switching or seed-console surface so member/admin/owner drills no longer rely on hand-editing browser session storage.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md`
- Runbook: ``
- Evidence artifact: ``

**Evidence Footer Source**:

- `P0-C1-S1S2S3` | artifact: ``
- `P3-C1-S1S2` | artifact: `artifacts/_tmp_s0f_9g_p3_permission_loop_verify.json`

- Keep footer rows low-cardinality: prefer one representative artifact per relevant unit instead of replaying the full artifact inventory.
- Generated PR body should keep `Evidence Footer` as the only optional section; development issue identity stays in `Metadata`.
- `Evidence Footer` rows must be copied only from `Evidence Footer Source` and must keep the same line shape.

## Exported Sections / Outlet Ownership

- This slice opens as one `log-retained core + runtime permission-closure source` lane.
- Stable extraction should wait until backend admin policy, membership UI, and local actor-switching settle into one reusable operator story.

**Outlet ownership**:

- `contract`: keep the first backend admin-policy, membership-operation, and local actor-switching rule set in this log until the packet stabilizes
- `runbook`: no-op at packet open; repeatable operator steps should wait until one local demo flow is stable
- `view`: no-op at packet open; a reader-facing admin/user closure summary can be exported later if the packet settles
- `index/front-door`: no-op at packet open; this packet widens enforcement and drillability more than navigation shape
- `disposition/placement`: no-op at packet open
- `log-retained core`: scope boundary, defaults, checklist, current status, and evidence ledger remain here

## Definitions (optional)

- `tenant-admin enforcement`: the backend policy rule that tenant-admin surfaces and mutation endpoints require `admin/owner` standing inside the selected tenant rather than relying on frontend hiding.
- `membership management surface`: one bounded tenant-scoped UI and API surface that can list, grant, and revoke user standing for the selected tenant.
- `local actor switching`: one local-first mechanism for changing the simulated current user or seeded session among bounded roles without using production impersonation semantics.
- `seed console`: one developer-facing local surface that materializes or selects known user/role combinations for reproducible drills.
- `permission loop`: the combined frontend-view, backend-policy, tenant-context, and membership-standing story that determines what one actor can see or mutate.

## Constraints

- Do not treat frontend role gating as sufficient authority for admin subscription routes; backend policy must enforce the same separation.
- Do not introduce cross-tenant impersonation, support-superuser tooling, or hidden bypasses in the first actor-switching surface.
- Do not widen this lane into real auth-provider identity sync, invitation email flows, or enterprise membership lifecycle complexity.
- Do not let actor-switching bypass tenant membership truth; selected actor identity and selected tenant still need bounded standing.
- Do not reopen the already-stable trigger-chain and entitlement semantics from `10B/10C/10D` unless one concrete enforcement bug requires a targeted extension.
- Do not commit generated artifacts or seed dumps to git; evidence should remain local artifacts unless a later packet explicitly changes that rule.

## Scope

- `P0`: contract for backend admin enforcement, minimum membership-management surface, local actor-switching boundary, and evidence contract
- `P1`: implement backend admin-policy enforcement and the first tenant-scoped membership-management slice
- `P2`: implement local actor-switching or seed-console support and wire the first reproducible user/admin demo flow
- `P3`: drill and verify end-to-end admin/user permission closure, tenant scoping, and bounded local actor simulation

## Success Criteria (DoD)

- Admin subscription routes reject ordinary members at the backend rather than relying only on frontend route hiding.
- One tenant-admin can list current tenant memberships and apply bounded grant/revoke actions inside the selected tenant.
- Ordinary users continue to see only `My Subscription`, while `admin/owner` can reach subscription-admin and membership-governance surfaces.
- One local actor-switching or seed-console flow exists so member/admin/owner drills no longer require hand-editing localStorage.
- The loop preserves explicit current tenant context and does not silently widen into cross-tenant state.
- The lane records evidence for backend admin enforcement, membership-management behavior, and actor-switching verification with traceable artifacts.
- Later auth-provider realism, invite flows, or support tooling can widen without reopening the first admin/user permission boundary.

## Stability (what stable means)

- This log can be marked `stable` when:
  - backend admin subscription routes and related tenant-governance actions enforce `admin/owner` standing for the selected tenant
  - one minimum tenant membership-management surface exists and has been exercised successfully
  - one local actor-switching or seed-console flow exists for reproducible member/admin/owner drills
  - focused drills prove frontend view split, backend enforcement, and tenant-context integrity on the same packet
  - the Evidence section includes traceable `headSha` values plus artifact paths
- `stable` for this packet means the first tenant-admin/user runtime loop no longer depends on frontend-only hiding or manual storage surgery.

## P0 (Contract | v1)

### P0-C1-S1 (Backend admin-enforcement contract)

- Admin subscription detail, history, and bounded event-apply routes must require `admin/owner` standing inside the selected tenant.
- The first fail-closed rule in this packet is now: `member` may read only user-facing access-context surfaces and must not use admin subscription endpoints successfully.
- Backend enforcement must remain aligned with the same tenant context rule fixed in `9F`; admin authority belongs to one actor inside one selected tenant, not to global client state.

### P0 Backend Admin-Enforcement Decision (v1)

- `P0` now fixes the first backend authority boundary in this lane as:
  - `/admin/subscriptions/{libraryId}` state read = `admin/owner` only
  - `/admin/subscriptions/{libraryId}/history` = `admin/owner` only
  - `/admin/subscriptions/{libraryId}/events` = `admin/owner` only
- The packet should prefer one shared backend policy helper for tenant-admin checks rather than repeating role assertions ad hoc across routes.
- The first deny contract in this packet is now fixed as fail-closed `403` for authenticated non-admin actors and tenant-mismatch failure when tenant scope and requested tenant diverge.

### P0-C1-S2 (Membership-management and actor-switching contract)

- The first membership-management surface in this packet is tenant-scoped and minimum only: list current memberships, grant/update one role, and revoke one role.
- The first actor-switching surface is local-first and bounded: it may materialize or select known user sessions for drills, but it must not imply production impersonation authority.
- Membership-management UI and actor-switching flow must both consume explicit current tenant context rather than silently inferring scope from whichever page was last open.

### P0 Membership And Actor-Switching Decision (v1)

- `P0` now fixes the first membership-management UI boundary in this lane as:
  - one tenant-admin view for current tenant membership rows
  - one bounded grant/update action
  - one bounded revoke action
- `P0` now fixes the first local actor-switching boundary in this lane as:
  - one developer-facing or drill-facing selector for known member/admin/owner sessions
  - one optional seed-materialization step if local data must be created before switching
  - no hidden cross-tenant bypass or support-style superuser mode

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - `adminRouteMatrix`
  - `membershipSurfaceActions`
  - `actorSwitchingCases`
  - `tenantScopeAssumptions`
  - `passFail`

### P0 Evidence Contract Decision (v1)

- `P0` now requires one local contract artifact before implementation lands.
- The first artifact path in this packet is fixed as `artifacts/_tmp_s0f_9g_p0_permission_loop_contract.json`.
- The artifact now records backend admin-route expectations, tenant membership surface actions, local actor-switching cases, and tenant-scope assumptions in one auditable packet.

### P0 Permission-Loop Contract Decision (v1)

- `P0` now fixes the first end-to-end permission-loop boundary in this lane as one three-part minimum closure:
  - backend admin routes fail closed for `member` and require `admin/owner` inside the selected tenant
  - tenant-scoped membership operations stay bounded to list, grant/update, and revoke inside current tenant context
  - local actor-switching stays explicit, local-first, and drill-oriented rather than support-style impersonation
- The first contract stance in this packet is now:
  - user-facing `access-context` remains readable to authenticated tenant-scoped actors
  - tenant-admin subscription state, history, and bounded event mutation are now reserved for `admin/owner`
  - actor-switching is allowed only when it preserves visible operator intent and tenant-scoped standing

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-9G/P<phase>-C<cycle>-S<steps>: <summary>`
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0F-9G/P0-P3: tenant-admin enforcement, membership management, and local actor-switching minimum closure`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title.

**Branch convention**:

- This lane belongs to the active `S0F-*` family because it closes the next runtime/admin/user permission gap on top of `9E` and `9F`.
- If the permission-closure work later splits into a deeper auth/provider or support-tooling stream, one later split may be justified, but this packet should start on the current scope branch.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, commit and push promptly with one evidence note in the log.
- Prefer one commit for `P0`, one for backend enforcement plus minimum membership slice, one for local actor-switching support, one for drill/verification, and one backfill commit if `headSha` needs to be recorded later.

## Plan (draft)

### P1 (Backend enforcement and membership slice)

- `P1-C1-S1`: land one shared backend tenant-admin policy for subscription-admin routes and related tenant-governance actions
- `P1-C1-S2`: land the first minimum tenant-scoped membership-management surface against the current backend contract

### P2 (Local actor-switching support)

- `P2-C1-S1`: land one local actor-switching or seed-console surface for bounded member/admin/owner simulation
- `P2-C1-S2`: wire the first reproducible admin/user demo flow so tenant-context and role changes stop depending on manual storage edits

## P1 (Backend enforcement and membership slice)

- `P1` lands the first code-bearing permission-closure slice for this packet without widening into real provider auth, invite lifecycle, or support tooling.
- The implementation goal in this packet is to make the current admin/user split enforceable at the backend and usable from one minimum tenant-admin management surface on the existing admin detail page.
- `P1` remains intentionally narrow: it adds one shared tenant-admin policy to subscription-admin routes and one tenant-scoped membership-management slice that consumes the current backend contract rather than opening a separate governance console.

### P1 Backend Enforcement Decision (v1)

- `P1` now lands the first reusable backend tenant-admin policy surface by reusing one shared `admin/owner` assertion for subscription-admin routes.
- The first backend enforcement rule in this packet is now fixed as:
  - `/admin/subscriptions/{libraryId}` denies `member` at the backend
  - `/admin/subscriptions/{libraryId}/history` denies `member` at the backend
  - `/admin/subscriptions/{libraryId}/events` denies `member` at the backend
- The first validation rule in this packet is now fixed as one focused backend router test proving `member -> 403` and `admin -> PASS` on the same route family.

### P1 Membership Surface Decision (v1)

- `P1` now lands the first tenant-scoped membership-management slice through:
  - `GET /libraries/{libraryId}/memberships`
  - existing bounded `grant/update` membership write path
  - existing bounded `revoke` membership write path
- The first frontend management surface in this packet is now fixed as one `TenantMembershipPanel` rendered inside `/admin/subscriptions/[libraryId]`.
- The opening UI rule in this packet is now fixed as:
  - list current tenant memberships
  - allow bounded grant/update by `user_id + role`
  - allow bounded revoke for one current tenant member
  - keep all actions on the same explicit current tenant context already fixed in `9F`

### P3 (Drill / Verify)

- `P3-C1-S1`: verify backend admin routes deny ordinary members and accept tenant admins under explicit tenant scope
- `P3-C1-S2`: verify membership-management and actor-switching flows preserve tenant scoping and expected admin/user views

## P3 (Drill / Verify)

- `P3` closes the first permission-loop packet by proving the new backend enforcement, membership-management surface, and local actor-switching flow behave coherently on the same tenant-scoped model.
- The drill goal in this packet is not to add new capability; it is to prove the slice is now stable enough to act as one reusable local-first admin/user closure rather than three loosely related features.
- `P3` also acts as the stable close-out gate for `9G`, so a passing packet here should move the log from active draft to stable packet status.

### P3 Permission-Loop Verification Decision (v1)

- `P3` now fixes the first close-out verification surface in this lane as one combined backend-plus-frontend drill set.
- The first close-out rule in this packet is now fixed as:
  - backend tests must prove both subscription-admin enforcement and tenant membership list allow/deny behavior
  - frontend drills must prove membership-management visibility and actor-switching route/menu behavior on the same local-first session model
  - the current tenant context must survive actor changes rather than resetting into hidden implicit state
- `P3` now treats `9G` as stable when those focused drills pass together, because the packet then has contract, implementation, and end-to-end evidence for one bounded permission loop.

## P2 (Local actor-switching support)

- `P2` lands the first reproducible local actor-switching flow for this packet without widening into production impersonation or support tooling.
- The implementation goal in this packet is to remove manual browser-storage edits from member/admin/owner drills while preserving the explicit tenant-context contract already fixed in `9F`.
- `P2` remains intentionally bounded: one shared header control is enough for the first demo loop as long as it rewrites session state explicitly, preserves tenant scope, and routes into the correct role-aware landing surface.

### P2 Local Actor-Switching Decision (v1)

- `P2` now lands one shared `LocalActorSwitcher` surface in the header for authenticated sessions.
- The first switching rule in this packet is now fixed as:
  - select one bounded local actor profile (`member`, `admin`, `owner`)
  - rewrite the local-first session explicitly through the shared auth shell
  - preserve the current tenant context as the switched session's tenant scope
  - redirect immediately to the role-appropriate landing path after the switch
- The first non-goal in this packet is now fixed as:
  - no support-style cross-tenant impersonation
  - no hidden session mutation without a visible operator action
  - no separate one-off actor switcher page

### P2 Reproducible Demo-Flow Decision (v1)

- `P2` now fixes the first reproducible admin/user demo flow in this lane as one shared navigation-level control rather than page-local debug code.
- The first demo flow in this packet is now:
  - start from one authenticated actor under one explicit tenant context
  - switch actor from the shared header
  - allow protected-route logic and menu visibility to recompute from the new role
  - land on the new role's default route without hand-editing storage

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: fix the first backend admin-enforcement contract for tenant-admin routes
- [x] `P0-C1-S2`: fix the first membership-management and local actor-switching boundary
- [x] `P0-C1-S3`: create the first evidence artifact contract for the permission loop

### P1 (Backend enforcement and membership slice)

- [x] `P1-C1-S1`: implement one shared backend tenant-admin policy for subscription-admin routes
- [x] `P1-C1-S2`: implement one minimum tenant-scoped membership-management surface

### P2 (Local actor-switching support)

- [x] `P2-C1-S1`: implement one local actor-switching or seed-console surface
- [x] `P2-C1-S2`: wire one reproducible admin/user demo flow without manual storage edits

### P3 (Drill / Verify)

- [x] `P3-C1-S1`: verify backend admin enforcement and tenant-scoped deny/allow behavior
- [x] `P3-C1-S2`: verify membership-management and actor-switching flows preserve expected admin/user views

## Current Status (recommended)

- `S0F-9G` is now stable: the packet has contract, backend enforcement, tenant-scoped membership management, bounded local actor switching, and focused close-out drills on the same tenant-scoped model.
- `9G` now acts as the stable source packet for the first enforceable local-first tenant-admin/user permission loop under the current `M4-P1` product-entry stack.
- The next step is no longer inside `9G`; the downstream choice should now be one later auth/provider realism or invite/identity-flow packet rather than reopening this first permission-loop boundary.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2S3 (Permission-loop contract fixed | 2026-04-17)

- headSha: `55773b233`
- artifacts: `artifacts/_tmp_s0f_9g_p0_permission_loop_contract.json`
- expected:
  - one reader can identify which subscription-admin routes require `admin/owner` and which user-facing surface remains readable to authenticated actors
  - one reader can identify the minimum tenant-scoped membership-management boundary and the first allowed local actor-switching shape
  - one reader can identify that tenant authority remains per-tenant and fail-closed rather than frontend-only or cross-tenant implicit
- observed:
  - `P0` now fixes explicit backend admin-route expectations, tenant-scoped membership surface actions, local actor-switching cases, and tenant-scope assumptions in one auditable contract artifact
  - `9G` now acts as the active source packet for turning the current UI split into one enforceable admin/user runtime loop

### P1-C1-S1S2 (Admin enforcement and membership slice landed | 2026-04-17)

- headSha: `a14dd8cb5`
- artifacts: `artifacts/_tmp_s0f_9g_p1_admin_enforcement_membership_slice.json`
- expected:
  - admin subscription routes fail closed for ordinary members at the backend
  - one tenant-admin view can list, grant/update, and revoke tenant memberships inside the selected tenant
  - the existing admin detail route remains compatible with explicit current tenant context after the new management surface lands
- observed:
  - `subscription_access` admin routes now reuse one shared tenant-admin policy helper, and focused backend router tests passed (`4 passed`)
  - `GET /libraries/{library_id}/memberships` now exists as the first tenant-scoped membership list read path, backed by the current library membership repository
  - `/admin/subscriptions/[libraryId]` now renders `TenantMembershipPanel` for list/grant/revoke actions against the selected tenant, and the focused Playwright tenant-context drill still passed (`2 passed`)

### P2-C1-S1S2 (Local actor-switching landed | 2026-04-17)

- headSha: `7f85e72c3`
- artifacts: `artifacts/_tmp_s0f_9g_p2_local_actor_switching.json`
- expected:
  - one local operator can switch between bounded `member/admin/owner` actors without hand-editing browser storage
  - the switched session preserves current tenant scope and recomputes route/menu visibility from the new role
  - the switched actor lands on the correct role-aware entry surface automatically
- observed:
  - `LocalActorSwitcher` now exists in the shared header and rewrites the local-first auth session through the shared auth shell
  - the switcher preserves current tenant scope by reusing the explicit current tenant context as the next session library scope
  - `npm run test:e2e -- tests/e2e/local-actor-switching.spec.ts` passed (`1 passed`) while proving admin -> member -> admin switching without manual storage edits

### P3-C1-S1S2 (Permission-loop verification passed | 2026-04-17)

- headSha: `29e5544c7`
- artifacts: `artifacts/_tmp_s0f_9g_p3_permission_loop_verify.json`
- expected:
  - backend tests prove tenant-admin allow/deny behavior for subscription-admin and membership-management reads under explicit tenant scope
  - frontend drills prove membership-management visibility and actor-switching route/menu behavior on the same local-first session model
  - the packet can now be judged as one stable permission loop rather than separate partial slices
- observed:
  - `c:/python314/python.exe -m pytest api/app/tests/test_library_router/test_membership_router.py api/app/tests/test_subscription_access/test_router.py -q` passed (`6 passed`)
  - `npm run test:e2e -- tests/e2e/local-actor-switching.spec.ts` passed (`1 passed`) while proving admin-only membership-management view visibility, actor switching, and preserved tenant scope
  - `S0F-9G` now satisfies its own stable close-out rule and moves from active draft to stable packet status

## Recent changes (for traceability, optional)

- 2026-04-17: opened `S0F-9G` as the next runtime permission-closure lane after `S0F-9F`, targeting backend tenant-admin enforcement, minimum tenant membership management, and bounded local actor-switching rather than widening auth-provider realism or payment-provider complexity.
- 2026-04-17: completed `S0F-9G/P0-C1-S1S2S3` by fixing the first backend admin-enforcement boundary, minimum membership-management contract, and local actor-switching contract in one evidence-backed packet.
- 2026-04-17: completed `S0F-9G/P1-C1-S1S2` by landing shared backend tenant-admin enforcement on subscription-admin routes and the first tenant-scoped membership-management surface on the admin subscription detail page.
- 2026-04-17: completed `S0F-9G/P2-C1-S1S2` by landing one shared local actor-switching surface in the header and proving a reproducible admin/member demo flow without manual storage edits.
- 2026-04-17: completed `S0F-9G/P3-C1-S1S2` and marked the packet stable after focused backend and frontend drills proved the first tenant-admin/user permission loop end to end.