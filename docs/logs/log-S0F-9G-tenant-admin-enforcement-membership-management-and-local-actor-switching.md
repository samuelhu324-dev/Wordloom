# log-S0F-9G (Phase 9G: tenant-admin enforcement, membership management, and local actor switching)

---

**id**: `S0F-9G`
**kind**: `log`
**title**: `tenant-admin enforcement, membership management, and local actor-switching minimum closure + drills/evidence + v1`
**status**: `draft`
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

### P3 (Drill / Verify)

- `P3-C1-S1`: verify backend admin routes deny ordinary members and accept tenant admins under explicit tenant scope
- `P3-C1-S2`: verify membership-management and actor-switching flows preserve tenant scoping and expected admin/user views

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: fix the first backend admin-enforcement contract for tenant-admin routes
- [x] `P0-C1-S2`: fix the first membership-management and local actor-switching boundary
- [x] `P0-C1-S3`: create the first evidence artifact contract for the permission loop

### P1 (Backend enforcement and membership slice)

- [ ] `P1-C1-S1`: implement one shared backend tenant-admin policy for subscription-admin routes
- [ ] `P1-C1-S2`: implement one minimum tenant-scoped membership-management surface

### P2 (Local actor-switching support)

- [ ] `P2-C1-S1`: implement one local actor-switching or seed-console surface
- [ ] `P2-C1-S2`: wire one reproducible admin/user demo flow without manual storage edits

### P3 (Drill / Verify)

- [ ] `P3-C1-S1`: verify backend admin enforcement and tenant-scoped deny/allow behavior
- [ ] `P3-C1-S2`: verify membership-management and actor-switching flows preserve expected admin/user views

## Current Status (recommended)

- `S0F-9G` is now opened as the next active source log after `S0F-9F`.
- `9E` already fixed the first user/admin entry split and local auth shell, while `9F` fixed explicit current tenant context; this new lane exists because the first runtime loop still lacks backend admin-route enforcement, a minimum tenant membership-management surface, and a reproducible local actor-switching flow.
- `S0F-9G/P0` is now complete: the packet now has one explicit contract for backend admin enforcement, minimum tenant-scoped membership operations, and bounded local actor-switching.
- The next step is now `P1` implementation work rather than more contract widening, because the packet has a stable enough authority and drillability boundary to land code.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2S3 (Permission-loop contract fixed | 2026-04-17)

- headSha: `pending-backfill`
- artifacts: `artifacts/_tmp_s0f_9g_p0_permission_loop_contract.json`
- expected:
  - one reader can identify which subscription-admin routes require `admin/owner` and which user-facing surface remains readable to authenticated actors
  - one reader can identify the minimum tenant-scoped membership-management boundary and the first allowed local actor-switching shape
  - one reader can identify that tenant authority remains per-tenant and fail-closed rather than frontend-only or cross-tenant implicit
- observed:
  - `P0` now fixes explicit backend admin-route expectations, tenant-scoped membership surface actions, local actor-switching cases, and tenant-scope assumptions in one auditable contract artifact
  - `9G` now acts as the active source packet for turning the current UI split into one enforceable admin/user runtime loop

## Recent changes (for traceability, optional)

- 2026-04-17: opened `S0F-9G` as the next runtime permission-closure lane after `S0F-9F`, targeting backend tenant-admin enforcement, minimum tenant membership management, and bounded local actor-switching rather than widening auth-provider realism or payment-provider complexity.
- 2026-04-17: completed `S0F-9G/P0-C1-S1S2S3` by fixing the first backend admin-enforcement boundary, minimum membership-management contract, and local actor-switching contract in one evidence-backed packet.