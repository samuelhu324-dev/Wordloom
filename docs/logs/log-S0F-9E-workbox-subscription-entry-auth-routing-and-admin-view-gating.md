# log-S0F-9E (Phase 9E: Workbox subscription entry, auth routing, and admin view gating)

---

**id**: `S0F-9E`
**kind**: `log`
**title**: `workbox subscription entry, auth routing, and admin-view gating minimum closure + drills/evidence + v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Access, Auth, Frontend, Admin, Runtime, Drills, Evidence, epic/s0, sub/9e`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-9D-frontend-admin-consumer-lane-for-subscription-access-closure.md`
  **reference_log_1**: `docs/logs/log-S0F-9D-frontend-admin-consumer-lane-for-subscription-access-closure.md`
  **reference_log_2**: `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
  **reference_log_3**: `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
  **reference_log_4**: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
**issue_keyword**: `runtime`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/9e`
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
**created**: `2026-04-16`
**updated**: `2026-04-16`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this lane.
- Day-level precision is acceptable while this packet is still defining the first real SaaS-style entry and role-aware navigation closure rather than one already-reviewed auth contract.
- If this lane later splits route policy, reader-facing navigation, and auth-provider details into separate outlets, the source log must still retain the current execution checklist, status, and evidence ledger.

## Decision / Outcome

**Decision**:

- `S0F-9E` opens as the next frontend/product-entry lane after `S0F-9D`, with the narrow goal of turning the stable subscription-access slice into one role-aware product entry surface.
- This packet should move subscription and access visibility out of incidental `library` or `bookshelf` placement and into one stable `Workbox` entry model.
- The first deliverable is one minimum closure across three surfaces only:
  - `Workbox > My Subscription` for ordinary users
  - `Workbox > Subscription Console` for tenant admins
  - one minimum auth shell with login, registration, and protected-route behavior
- This packet is not the place to widen payment realism, platform-admin tooling, or deep tenant analytics; it exists to close the first product-entry and role-gating gap.

**Default choices (phase defaults / v1)**:

- Keep `Workbox` as the stable home for subscription and access surfaces; do not continue embedding those surfaces in content-first `library` or `bookshelf` pages as the primary UX.
- Keep one shared login surface; do not create separate admin and user login pages in this first closure.
- Keep the first role split limited to `user/member` versus `tenant admin/owner` for UI entry and view gating.
- Keep admin-only visibility fail-closed: hidden in menu, protected in route handling, and later expected to be rejected by the backend as well.
- Keep `event history`, mutation controls, tenant-wide visibility, and support/debug-style views out of ordinary user pages.
- Keep tenant data-ownership and storage-boundary design out of this packet unless one concrete auth or routing decision depends on them.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S0F-9E` is intended to drive the first PR that closes real role-aware navigation and auth entry behavior for the already-stable subscription-access slice.

**PR summary bullets**:

- Move subscription visibility into `Workbox` with separate user and tenant-admin entry behavior.
- Add one minimum login, registration, and protected-route shell so internal pages stop relying on direct local navigation.
- Gate the first admin-only subscription and operational views so ordinary users no longer see tenant-wide history or mutation surfaces.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0F-9E-workbox-subscription-entry-auth-routing-and-admin-view-gating.md`
- Runbook: ``
- Evidence artifact: `artifacts/_tmp_s0f_9e_p1_workbox_auth_impl.json`

**Evidence Footer Source**:

- `P1-C1-S1S2` | artifact: `artifacts/_tmp_s0f_9e_p1_workbox_auth_impl.json`

## Exported Sections / Outlet Ownership

- This slice opens as one log-retained source packet because the rule, UI placement, and route-gating details are still changing together.
- Stable extraction should wait until there is one accepted auth-entry and Workbox-navigation contract rather than exporting premature fragments.

**Outlet ownership**:

- `contract`: keep the first Workbox-entry, auth-routing, and admin-view-gating rule set in this log until the packet stabilizes
- `runbook`: no-op at packet open; repeatable operator steps should wait until there is one stable local auth/test path
- `view`: no-op at packet open; a reader-facing navigation summary can be exported later if the product front door stabilizes
- `index/front-door`: likely later candidate because this packet may eventually mutate visible app navigation, but defer export until the first route model lands
- `disposition/placement`: no-op at packet open
- `log-retained core`: scope boundary, defaults, checklist, current status, and evidence ledger remain here

## Definitions (optional)

- `My Subscription`: the user-facing Workbox surface that shows only the current user's plan, standing, capabilities, and friendly gating explanation.
- `Subscription Console`: the tenant-admin-facing Workbox surface that may show tenant-wide subscription state, history, and bounded operational controls.
- `protected route`: one page or layout that requires login and optionally a specific role before it renders protected UI.
- `admin-only view`: one route, panel, or action surface that ordinary users should not see in menu, route output, or interaction flow.
- `auth shell`: the minimum shared login, registration, session, and route-gating layer needed before product pages stop behaving like anonymous direct-link pages.

## Constraints

- Do not create separate admin and user login pages in v1.
- Do not expose admin history, mutation controls, or support/debug views to ordinary users.
- Do not use this packet to open platform-admin or cross-tenant operations.
- Do not reopen the already-stable subscription-access backend lifecycle contract from `9C/9D` unless a concrete auth or route boundary requires one backend extension.
- Do not force full production auth-provider realism in the opening lane; the goal is minimum local-first product-entry closure.

## Scope

- `P0`: contract for Workbox placement, role-aware page split, auth shell boundary, and evidence contract
- `P1`: implement Workbox subscription relocation plus the first login/registration/protected-route shell
- `P2`: implement and verify the first admin-only menu, route, and view gating behavior
- `P3`: close out the entry model and define the handoff boundary into later tenant analytics, richer auth, or platform-admin widening

## Success Criteria (DoD)

- The lane fixes `Workbox` as the primary entry for subscription/access surfaces.
- Ordinary users can reach one `My Subscription` surface without seeing tenant-admin event history or mutation controls.
- Tenant admins can reach one `Subscription Console` surface from `Workbox`.
- The app exposes one minimum login and registration flow rather than relying on direct-click access to internal pages.
- Unauthenticated users are redirected or blocked from protected pages.
- Non-admin users do not see the first admin-only menu items or route outputs.
- The lane records evidence for role-aware navigation, protected-route behavior, and admin-view gating with traceable artifacts.
- The lane leaves tenant data ownership, object storage, and richer analytics able to widen later without reopening the first entry model.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `Workbox > My Subscription` and `Workbox > Subscription Console` exist with role-appropriate entry behavior
  - one minimum login and registration shell exists and is sufficient to gate protected pages locally
  - unauthenticated and non-admin route handling has been exercised through focused drills
  - the Evidence section includes traceable `headSha` values plus artifact paths
  - the next-lane handoff rule is explicit for tenant analytics, richer auth/provider realism, or data-ownership widening
- `stable` for this packet means the product front door and first admin-only view gating no longer depend on ad hoc local navigation.

## P0 (Contract | v1)

### P0-C1-S1 (Workbox subscription entry contract)

- The first stable subscription/access entry in this packet is fixed under `Workbox`, not under content-first `library` or `bookshelf` pages.
- The first two entry surfaces are fixed as:
  - `Workbox > My Subscription` for ordinary users
  - `Workbox > Subscription Console` for tenant admins
- `My Subscription` may show current plan, standing, and gated capabilities for the current user only.
- `Subscription Console` may show tenant-wide subscription state, history, and bounded admin controls.
- `event history`, tenant-wide state, and mutation controls are explicitly admin-only in this packet.

### P0 Workbox Entry Contract Decision (v1)

- `P0` now fixes `Workbox` as the only primary entry surface for this packet's subscription/access UI.
- The first role-aware entry split is now fixed as:
  - `Workbox > My Subscription` for `member/user`
  - `Workbox > Subscription Console` for `admin/owner`
- Content-first `library` and `bookshelf` pages are no longer the canonical front door for subscription visibility in this lane.
- Tenant-wide state, event history, and mutation controls are now explicitly excluded from ordinary user entry surfaces.

### P0-C1-S2 (Auth and admin-view gating contract)

- The app must use one shared login surface and one minimum registration surface in v1.
- Post-login landing may vary by role, but authentication itself must stay unified.
- The first fail-closed gating rule in this packet is:
  - unauthenticated users cannot render protected internal pages
  - authenticated non-admin users cannot render admin-only views
  - menu visibility must align with route visibility so admin-only pages are not advertised to ordinary users
- Backend authorization remains the final authority, but this packet focuses first on frontend shell, navigation, and route behavior.

  ### P0 Auth and View-Gating Decision (v1)

  - `P0` now fixes the first shared auth-shell assumption in this lane as one login surface plus one minimum registration surface.
  - The first fail-closed route contract is now fixed as:
    - unauthenticated users must be redirected or blocked before protected internal UI renders
    - authenticated non-admin users must not render admin-only routes or views
    - menu and route visibility must stay aligned so admin entrypoints are not advertised to ordinary users
  - The first admin-only view family in this lane is now fixed as:
    - subscription event history
    - bounded mutation controls
    - tenant-wide subscription state panels
    - support/debug-style operational views

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - `workboxEntryPoints`
  - `userVisibleSurfaces`
  - `adminVisibleSurfaces`
  - `protectedRouteCases`
  - `roleScenarioMatrix`
  - `passFail`

### P0 Evidence Contract Decision (v1)

- `P0` now requires one contract artifact before implementation lands.
- The first artifact path in this packet is fixed as `artifacts/_tmp_s0f_9e_p0_entry_and_route_contract.json`.
- The artifact now records Workbox entry split, admin-only view family, protected-route cases, and role-scenario expectations in one auditable packet.

## P1 (Implementation | v1)

### P1-C1-S1 (Workbox entry relocation and role-aware surfaces)

- `P1` must land one authenticated user route for `Workbox > My Subscription` and preserve one tenant-admin route for `Workbox > Subscription Console`.
- `WorkboxMenu` must become role-aware so ordinary users do not see tenant-admin navigation entries.
- Existing admin-only Workbox entries such as `Libraries`, `Basement`, `Chronicle`, and `Tags` remain admin/owner only in this packet.

### P1 Workbox Entry Implementation Decision (v1)

- `P1` now lands `frontend/src/app/workbox/subscription/page.tsx` as the first user-facing Workbox route for subscription visibility.
- `WorkboxMenu` now renders role-aware entries:
  - authenticated users see `My Subscription`
  - `admin/owner` additionally see `Subscription Console` and the pre-existing admin workbox routes
- The home-page Workbox quick link now targets `/workbox/subscription` rather than an admin-only route.

### P1-C1-S2 (Minimum auth shell and protected-route implementation)

- `P1` must land one shared login route and one shared registration route without splitting authentication into separate admin and user entry pages.
- The opening protected-route shell must gate authenticated internal pages and keep admin routes restricted to `admin/owner`.
- This packet may use a local-first browser session to validate entry and gating behavior before provider realism exists.

### P1 Auth Shell Implementation Decision (v1)

- `P1` now lands one local-first auth shell through:
  - `frontend/src/app/login/page.tsx`
  - `frontend/src/app/register/page.tsx`
  - `frontend/src/shared/auth/AuthContext.tsx`
  - `frontend/src/shared/auth/ProtectedRoute.tsx`
- `frontend/src/app/providers.tsx` now mounts the auth provider so header, Workbox menu, and protected routes share one session source.
- `frontend/src/app/admin/layout.tsx` now requires `admin/owner`, while `frontend/src/app/workbox/layout.tsx` now requires any authenticated session.
- `frontend/src/shared/layouts/header.tsx` now exposes login/register when signed out and session badge plus sign-out when signed in.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-9E/P<phase>-C<cycle>-S<steps>: <summary>`
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0F-9E/P0-P3: workbox subscription entry, auth routing, and admin-view gating minimum closure`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title.

**Branch convention**:

- This lane belongs to the active `S0F-*` family because it directly widens the first product-entry closure on top of the subscription-access work stabilized in `9D`.
- If the auth shell later becomes a larger multi-scope stream, one later split may be justified, but this packet should start on the current scope branch.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, commit and push promptly with one evidence note in the log.
- Prefer one commit for `P0`, one for Workbox/auth implementation, one for route-gating verification, and one backfill commit if `headSha` needs to be recorded later.

## Plan (draft)

### P1 (Workbox entry and auth shell implementation)

- `P1-C1-S1`: move subscription/access entry into `Workbox` and split the first user-facing versus tenant-admin entry surfaces
- `P1-C1-S2`: add one minimum login, registration, and protected-route shell for internal pages

### P2 (Role-aware gating drill / verify)

- `P2-C1-S1`: verify user-facing `My Subscription` visibility without admin-only history or mutation controls
- `P2-C1-S2`: verify tenant-admin menu visibility and admin-route access while non-admin users remain blocked or redirected

### P3 (Close-out / handoff)

- `P3-C1-S1`: define which product-entry and gating behaviors are now stable enough for later lanes to consume directly
- `P3-C1-S2`: define the handoff boundary into later tenant analytics, richer auth/provider realism, or multi-tenant data-ownership work

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: fix `Workbox > My Subscription` versus `Workbox > Subscription Console` as the first stable entry split
- [x] `P0-C1-S2`: fix the minimum login/registration/protected-route and admin-view-gating rules for v1
- [x] `P0-C1-S3`: create the first evidence artifact contract for role-aware entry and route verification

### P1 (Workbox entry and auth shell)

- [x] `P1-C1-S1`: implement Workbox subscription relocation and role-aware entry surfaces
- [x] `P1-C1-S2`: implement the minimum login, registration, and protected-route shell

### P2 (Role-aware gating drill / verify)

- [ ] `P2-C1-S1`: verify ordinary-user visibility is limited to `My Subscription`
- [ ] `P2-C1-S2`: verify tenant-admin access and non-admin blocking for the first admin-only views

### P3 (Close-out / handoff)

- [ ] `P3-C1-S1`: freeze the first stable entry and gating behaviors
- [ ] `P3-C1-S2`: define the downstream handoff rule without reopening v1 entry design

## Current Status (recommended)

- `S0F-9E/P0` is now complete: the Workbox entry split, shared auth-shell assumption, and first admin-only view family are fixed in one contract artifact.
- `S0F-9E/P1` is now complete: the lane now has one local-first login/register shell, one authenticated `My Subscription` route, and one admin-gated `Subscription Console` path.
- The upstream backend and frontend/admin subscription-access slice remains stable enough to support this lane, so the next step is now `P2` role-aware gating verification rather than more implementation widening.
- Automation should continue to treat this log as the active source for the first Workbox-entry and auth-routing closure until the packet stabilizes through `P2`.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths.
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2S3 (Entry and route contract fixed | 2026-04-16)

- headSha: `06cac16c4`
- artifacts: `artifacts/_tmp_s0f_9e_p0_entry_and_route_contract.json`
- expected:
  - one contract artifact fixes the first Workbox entry split before implementation starts
  - the artifact is sufficient to record route visibility, admin-only views, and role scenario results
- observed:
  - `Workbox > My Subscription` and `Workbox > Subscription Console` are now fixed as the opening role-aware entry split
  - the first shared login/registration and fail-closed route assumptions are now recorded in one contract packet
  - the first admin-only view family is now fixed before `P1` implementation

### P1-C1-S1S2 (Workbox entry and auth shell landed | 2026-04-16)

- headSha: `pending-backfill`
- artifacts: `artifacts/_tmp_s0f_9e_p1_workbox_auth_impl.json`
- expected:
  - one authenticated user route exists for `Workbox > My Subscription`
  - one shared login and registration shell exists before deeper auth/provider work
  - admin routes and admin-only menu entries are gated to `admin/owner`
- observed:
  - `/workbox/subscription` now exists as the first user-facing Workbox subscription route
  - `/login` and `/register` now exist with one local-first session model
  - admin layout now requires `admin/owner`, and workbox layout now requires any authenticated session
  - `WorkboxMenu` and header now derive visible entrypoints from the shared auth session
  - focused diagnostics on touched files passed, while repo-wide `npm run type-check` still reports unrelated pre-existing errors outside the `9E` touch set

## Recent changes (for traceability, optional)

- 2026-04-16: opened `S0F-9E` as the first focused lane for Workbox subscription entry, login/registration/protected-route closure, and admin-only view gating on top of the stable `9D` slice.
- 2026-04-16: completed `S0F-9E/P0-C1-S1S2S3` by fixing the first Workbox entry split, auth-shell assumptions, admin-only view family, and contract artifact for later `P1` implementation.
- 2026-04-16: completed `S0F-9E/P1-C1-S1S2` by landing the first local-first auth shell, authenticated Workbox subscription route, and admin-gated subscription console entry.