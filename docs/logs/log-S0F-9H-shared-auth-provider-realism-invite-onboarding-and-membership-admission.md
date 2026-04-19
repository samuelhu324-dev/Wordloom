# log-S0F-9H (Phase 9H: shared auth/provider realism, invite/onboarding, and membership admission)

---

**id**: `S0F-9H`
**kind**: `log`
**title**: `shared auth/provider realism, invite/onboarding, and membership-admission minimum closure + drills/evidence + v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Access, Auth, Identity, Onboarding, Runtime, Drills, Evidence, epic/s0, sub/9h`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md`
  **reference_log_1**: `docs/logs/log-S0F-9E-workbox-subscription-entry-auth-routing-and-admin-view-gating.md`
  **reference_log_2**: `docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
  **reference_log_3**: `docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md`
  **reference_log_4**: `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
**issue_keyword**: `runtime`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/9h`
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
**created**: `2026-04-19`
**updated**: `2026-04-19`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this lane.
- Day-level precision is acceptable while this packet is still fixing the first more-realistic auth-entry and membership-admission flow rather than one already-reviewed provider contract.
- If this lane later splits provider-facing auth assumptions, invite/onboarding flow, and post-login tenant landing rules into separate child packets, the source log must still retain the execution checklist, current status, and evidence ledger.

## Decision / Outcome

**Decision**:

- `S0F-9H` opens as the next lane after `S0F-9G`, with the narrow goal of replacing the current local-first-only auth entry assumptions with one more realistic shared auth-entry and membership-admission closure.
- This packet should preserve the already-stable `9G` permission loop and treat it as a downstream consumer, while fixing how one user is admitted into the system, becomes a member of one tenant, and lands on the correct post-login route without relying on manual role selection as the primary product story.
- The first deliverable is one minimum closure across three surfaces only:
  - one more realistic shared auth-entry assumption that narrows the current local-first login/register shell toward provider-compatible identity flow
  - one minimum invite/onboarding or membership-admission path that explains how one identity gains tenant standing
  - one post-login routed-entry rule that resolves landing and tenant selection without reopening the already-stable tenant-context contract from `9F`
- This packet is not the place to widen support impersonation, cross-tenant operations, enterprise identity sprawl, or real payment-provider realism; it exists to close the first identity-to-membership-to-entry path on top of the stable `9G` permission loop.

**Default choices (phase defaults / v1)**:

- Keep one shared auth entry surface; do not split user and admin into separate login products.
- Keep the first provider realism bounded: the packet may move closer to provider-compatible identity assumptions, but it must not require a full production identity platform before proving the flow.
- Keep membership admission explicit: one identity should not become tenant member by hidden role selection alone.
- Keep post-login landing role-aware and tenant-aware, but do not reopen the already-stable `9G` admin/user permission boundary.
- Keep local-first drillability where it still helps, but stop treating manual role selection in login/register as the long-term primary product contract.
- draft 阶段默认继续把 source log 当作集中面；如果 provider boundary、invite/onboarding flow、membership admission、routed entry 仍在一起变化，不要过早把 weak-structure 内容拆到多个 outlets。
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S0F-9H` is intended to drive the next packet that turns the current local-first auth shell into one more realistic identity and onboarding entry surface.

**PR summary bullets**:

- Narrow the current login/register shell toward one more realistic shared auth-entry and provider-compatible identity assumption.
- Land one minimum invite/onboarding or membership-admission path so tenant standing no longer begins from manual role selection alone.
- Fix post-login role-aware and tenant-aware routed entry on top of the stable `9F/9G` runtime contracts.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md`
- Runbook: ``
- Evidence artifact: ``

**Evidence Footer Source**:

- `P0-C1-S1S2S3` | artifact: `artifacts/_tmp_s0f_9h_p0_auth_entry_membership_admission_contract.json`
- `P1-C1-S1S2` | artifact: `artifacts/_tmp_s0f_9h_p1_auth_entry_and_admission_slice.json`
- `P2-C1-S1S2` | artifact: `artifacts/_tmp_s0f_9h_p2_routed_entry_and_tenant_landing.json`

- Keep footer rows low-cardinality: prefer one representative artifact per relevant unit instead of replaying the full artifact inventory.
- Generated PR body should keep `Evidence Footer` as the only optional section; development issue identity stays in `Metadata`.
- `Evidence Footer` rows must be copied only from `Evidence Footer Source` and must keep the same line shape.

## Exported Sections / Outlet Ownership

- This slice opens as one `log-retained core + auth-entry/onboarding source` lane.
- Stable extraction should wait until auth entry, membership admission, and routed landing settle into one reusable product story.

**Outlet ownership**:

- `contract`: keep the first auth-entry, membership-admission, and routed-entry rule set in this log until the packet stabilizes
- `runbook`: no-op at packet open; operator procedure should wait until one stable onboarding drill path exists
- `view`: no-op at packet open; a reader-facing auth/onboarding summary can be exported later if the packet settles
- `index/front-door`: no-op at packet open; this packet changes entry assumptions more than broad navigation taxonomy
- `disposition/placement`: no-op at packet open
- `log-retained core`: scope boundary, defaults, checklist, current status, and evidence ledger remain here

## Definitions (optional)

- `shared auth entry`: one unified login/authentication entry surface used by all actors before role-aware landing occurs.
- `provider realism`: one bounded move from purely local-first session fabrication toward identity assumptions that a later real provider adapter could honor.
- `membership admission`: the explicit path by which one identity gains tenant standing, whether through invite, acceptance, or another bounded admission rule.
- `routed entry`: the post-login path resolution that decides where one actor lands and which tenant context is active.
- `invite/onboarding flow`: one bounded sequence that turns an invited or newly admitted identity into one authenticated tenant member.

## Constraints

- Do not reopen the already-stable `9G` admin/user permission boundary.
- Do not introduce support-style impersonation, cross-tenant inspection, or super-admin bypass into this packet.
- Do not widen this lane into full enterprise identity sprawl, SSO matrix design, or deep provider SDK orchestration.
- Do not let tenant standing continue to depend on manual role selection as the primary product contract.
- Do not reopen `9F` current-tenant-context semantics unless one concrete routed-entry decision requires a targeted extension.
- Do not commit generated artifacts or seed dumps to git; evidence should remain local artifacts unless a later packet explicitly changes that rule.

## Scope

- `P0`: contract for shared auth-entry realism, invite/onboarding and membership-admission boundary, routed-entry rule, and evidence contract
- `P1`: implement the first bounded auth-entry and membership-admission slice on top of the current local-first shell
- `P2`: implement and verify routed landing plus tenant-aware post-login behavior for newly admitted actors
- `P3`: drill and verify identity-to-membership-to-entry closure, then define handoff into later provider adapters or richer identity realism

## Success Criteria (DoD)

- The app no longer treats manual role selection in login/register as the long-term primary product contract for tenant standing.
- One explicit membership-admission path exists so a reader can explain how one identity becomes a member of one tenant.
- Post-login routing resolves into the correct tenant-aware and role-aware entry surface without reopening the stable `9G` permission loop.
- The packet preserves explicit current tenant context and does not silently widen into cross-tenant identity authority.
- The lane records evidence for auth-entry assumptions, membership-admission behavior, and routed-entry verification with traceable artifacts.
- Later provider adapters or richer identity realism can widen without reopening the first tenant-admin/user permission loop.

## Stability (what stable means)

- This log can be marked `stable` when:
  - one shared auth-entry assumption exists that is more realistic than pure manual role fabrication
  - one explicit membership-admission path exists for tenant standing
  - one post-login routed-entry rule exists and has been exercised successfully
  - focused drills prove identity-to-membership-to-entry closure on the same tenant-scoped model
  - the Evidence section includes traceable `headSha` values plus artifact paths
- `stable` for this packet means the first identity-to-membership-to-entry path no longer depends on manual role selection as the product contract.

## P0 (Contract | v1)

### P0-C1-S1 (Shared auth-entry and provider-realism contract)

- The first auth-entry surface remains shared across ordinary users and tenant admins.
- The packet must define which parts of the current local-first auth shell remain valid and which parts must be treated as temporary scaffolding.
- The first realism rule in this packet is that identity proof and tenant standing must be conceptually separated even if local-first mechanics still exist in v1.

### P0 Shared Auth-Entry Decision (v1)

- `P0` now fixes the first shared auth-entry boundary in this lane as:
  - keep one shared `/login` entry and one shared `/register` entry rather than splitting actor-specific auth surfaces
  - keep `email` and `displayName` as the first explicit identity claims carried by the local-first shell
  - treat manual `role` selection in auth forms as temporary scaffolding that must stop acting as the primary product truth for tenant standing
- The first provider-realism stance in this packet is now fixed as:
  - identity proof and membership standing are separate concepts
  - auth entry may still materialize a local-first session in v1, but tenant/admin standing must later come from admission truth rather than from whichever role the user picks in the form
  - `libraryId` may remain a temporary tenant-target hint during the transition, but it is no longer the long-term evidence of admitted standing by itself

### P0-C1-S2 (Membership-admission and routed-entry contract)

- The packet must define one explicit path by which one identity gains tenant standing.
- The packet must define how post-login landing resolves tenant-aware and role-aware entry behavior after admission.
- Routed entry must reuse the stable `9F` explicit current-tenant-context rule rather than inventing hidden fallback authority.

### P0 Membership-Admission And Routed-Entry Decision (v1)

- `P0` now fixes the first membership-admission boundary in this lane as one bounded local-first invite/admission contract:
  - one identity authenticates through the shared auth shell
  - one explicit admission record or invite acceptance grants standing inside one tenant
  - tenant role is derived from admitted standing, not freely fabricated during login/register
- `P0` now fixes the first routed-entry rule in this lane as:
  - if the authenticated identity has exactly one admitted tenant, post-login landing binds that tenant as explicit current tenant context and routes by admitted role
  - if the authenticated identity has no admitted tenant yet, post-login landing must stop on onboarding/admission completion rather than silently fabricating tenant authority
  - if the authenticated identity later has multiple admitted tenants, tenant selection must remain explicit and must reuse the stable `9F` current-tenant-context contract instead of hidden fallback storage
- The first landing-path stance in this packet is now fixed as:
  - admitted `member` lands on `Workbox > My Subscription`
  - admitted `admin/owner` lands on `Workbox > Subscription Console` or its admin entry equivalent already stabilized by `9E/9G`
  - unauthenticated access and non-admitted access remain fail-closed and must not depend on direct-click navigation

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - `authEntryAssumptions`
  - `membershipAdmissionCases`
  - `routedEntryRules`
  - `tenantScopeAssumptions`
  - `passFail`

### P0 Evidence Contract Decision (v1)

- `P0` now requires one local contract artifact before implementation lands.
- The first artifact path in this packet is fixed as `artifacts/_tmp_s0f_9h_p0_auth_entry_membership_admission_contract.json`.
- The artifact now records auth-entry assumptions, membership-admission cases, routed-entry rules, and tenant-scope assumptions in one auditable packet.

### P0 Auth-Entry And Membership-Admission Contract Decision (v1)

- `P0` now fixes the first end-to-end identity-to-membership-to-entry boundary in this lane as one three-part minimum closure:
  - shared auth entry proves identity shape but does not by itself prove tenant standing
  - explicit membership admission or invite acceptance grants standing inside one tenant
  - routed entry binds explicit current tenant context and chooses the role-aware landing path from admitted standing rather than manual role fabrication
- The first contract stance in this packet is now:
  - local-first session creation remains acceptable as transition scaffolding for v1
  - login/register forms must stop acting as the long-term authority for tenant role truth
  - post-login routing must fail closed when admitted tenant scope is absent or unresolved

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-9H/P<phase>-C<cycle>-S<steps>: <summary>`
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0F-9H/P0-P3: shared auth/provider realism, invite/onboarding, and membership-admission minimum closure`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title.

**Branch convention**:

- This lane belongs to the active `S0F-*` family because it continues the current `M4-P1` product-entry stack after `9G` reached stable close-out.
- If the work later splits into one dedicated provider-adapter or enterprise identity stream, one later split may be justified, but this packet should start on the current scope branch.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, commit and push promptly with one evidence note in the log.
- Prefer one commit for `P0`, one for the first auth-entry plus membership-admission slice, one for routed-entry implementation, one for drill/verification, and one backfill commit if `headSha` needs to be recorded later.

## Plan (draft)

### P1 (Auth entry and admission slice)

- `P1-C1-S1`: land one bounded shared auth-entry update that narrows manual role fabrication toward provider-compatible identity assumptions
- `P1-C1-S2`: land one explicit membership-admission slice so tenant standing no longer begins from free manual role selection alone

### P2 (Routed entry and tenant-aware landing)

- `P2-C1-S1`: land one post-login role-aware and tenant-aware routed-entry rule on top of the stable `9F/9G` runtime model
- `P2-C1-S2`: verify that admitted actors land on the correct tenant-scoped entry without hidden fallback authority

### P3 (Drill / Verify)

- `P3-C1-S1`: verify identity-to-membership closure under the new auth-entry and admission assumptions
- `P3-C1-S2`: verify routed-entry behavior and define handoff into later provider adapters or richer identity realism

## P1 (Auth entry and admission slice)

- `P1` lands the first code-bearing identity-entry slice for this packet without widening into real provider SDK orchestration, external invite delivery, or enterprise identity sprawl.
- The implementation goal in this packet is to stop treating login/register role selection as product truth, while still keeping one local-first path that can authenticate identity, pause on pending admission, and derive standing only after explicit admission claim.
- `P1` remains intentionally bounded: one shared auth shell update, one local-first admission page, one derived-standing rule in auth runtime, and one preserved dev-only bypass for `LocalActorSwitcher` are enough for the first slice.

### P1 Shared Auth-Entry Slice Decision (v1)

- `P1` now lands the first bounded shared auth-entry update through:
  - removing free role selection from `/login` and `/register`
  - keeping `email`, `displayName`, and `libraryId` as the user-entered identity plus tenant-target fields
  - deriving post-login standing from admission truth or explicit dev bypass rather than from the auth form itself
- The first auth-runtime rule in this packet is now fixed as:
  - ordinary auth entry creates either `pending` or `admitted` session state
  - `pending` sessions remain authenticated identities but must not reach protected member/admin surfaces yet
  - `LocalActorSwitcher` may still use one explicit `dev-bypass` path so drill tooling remains available without becoming the product contract

### P1 Membership-Admission Slice Decision (v1)

- `P1` now lands the first explicit local-first membership-admission surface through:
  - one `/onboarding/admission` page for pending identities
  - one bounded local admission-code claim flow
  - one derived-standing update in `AuthContext` that turns claimed admission into admitted tenant role
- The first admission rule in this packet is now fixed as:
  - pending identities land on onboarding instead of silently inheriting standing
  - admitted standing is derived from claimed local admission code for the selected tenant target
  - admitted identities then reuse the stable `9E/9F/9G` role-aware landing surfaces without reopening the permission loop

## P2 (Routed entry and tenant-aware landing)

- `P2` lands the first unified routed-entry rule for this packet, so shared auth entry, pending-onboarding redirects, admission completion, and dev-only actor switching all resolve through the same tenant-aware landing decision.
- The implementation goal in this packet is to stop treating post-login routing as one role-only shortcut and instead bind the first admitted tenant explicitly into the landing path when the actor has one admitted tenant.
- `P2` remains intentionally bounded: one shared landing resolver, one preserved safe-`next` rule through onboarding, one tenant-scoped admin default, and one focused drill set are enough for this slice.

### P2 Routed-Entry Decision (v1)

- `P2` now lands the first routed-entry tightening through:
  - one shared landing resolver in auth runtime that accepts optional `next` intent
  - one safe-`next` rule that rejects auth-loop paths and role-incompatible targets
  - one tenant-scoped default admin landing that uses the admitted tenant target directly
- The first routed-entry rule in this packet is now fixed as:
  - pending identities preserve safe intended destination by redirecting to `/onboarding/admission?next=...`
  - admitted `member` defaults to `/workbox/subscription`
  - admitted `admin/owner` defaults to `/admin/subscriptions/{libraryId}` so the first admitted tenant is bound into the route instead of relying on later manual selection

### P2 Tenant-Aware Landing Verification Decision (v1)

- `P2` now verifies tenant-aware landing through focused Playwright coverage for:
  - pending identity entry with preserved admin-target intent through onboarding
  - admitted admin landing on tenant-scoped subscription detail rather than generic admin console
  - local actor switching back into an admitted admin actor with the same tenant-scoped default route
- The first verification rule in this packet is now fixed as:
  - routed entry must preserve safe `next` intent across pending admission
  - routed entry must reject role-incompatible targets and fall back to admitted-role landing
  - tenant context must be observable from landing behavior rather than only from hidden storage fallback

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: fix the first shared auth-entry and provider-realism contract
- [x] `P0-C1-S2`: fix the first membership-admission and routed-entry contract
- [x] `P0-C1-S3`: create the first evidence artifact contract for auth-entry and onboarding closure

### P1 (Auth entry and admission slice)

- [x] `P1-C1-S1`: implement one bounded shared auth-entry update
- [x] `P1-C1-S2`: implement one explicit membership-admission slice

### P2 (Routed entry and tenant-aware landing)

- [x] `P2-C1-S1`: implement one role-aware and tenant-aware routed-entry rule
- [x] `P2-C1-S2`: verify admitted actors land on the correct tenant-scoped entry

### P3 (Drill / Verify)

- [ ] `P3-C1-S1`: verify identity-to-membership closure under the new auth-entry assumptions
- [ ] `P3-C1-S2`: verify routed-entry behavior and handoff into later identity realism

## Current Status (recommended)

- `S0F-9H/P2` is now landed: the packet now has one unified routed-entry rule on top of the already-landed shared auth-entry and explicit local-first admission slice.
- `9H/P2` now fixes the first tenant-aware landing closure in this lane: pending identities keep safe `next` intent through onboarding, admitted admins land directly on tenant-scoped admin detail, and member/admin fallback routing stays role-compatible.
- The next step is now `P3` drill/verify closure rather than more landing-surface widening, because the packet now has the first explicit identity-to-membership-to-entry path with tenant-aware routing behavior in place.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2S3 (Auth-entry and membership-admission contract fixed | 2026-04-19)

- `headSha`: `ca0d8eca8`
- `artifacts`:
  - `artifacts/_tmp_s0f_9h_p0_auth_entry_membership_admission_contract.json`
- `expected`:
  - shared auth entry remains unified, but manual role selection stops acting as long-term tenant-standing truth
  - one explicit local-first admission path explains how identity becomes tenant membership
  - routed entry reuses explicit current tenant context and fails closed when tenant scope is absent
- `observed`:
  - `P0` now fixes provider-compatible identity vs admitted-standing separation as the new packet boundary
  - `P0` now fixes one bounded invite/admission-first standing model instead of role fabrication during login/register
  - `P0` now fixes one post-login landing rule that binds explicit tenant context before role-aware entry

### P1-C1-S1S2 (Auth-entry and admission slice landed | 2026-04-19)

- `headSha`: `1938713f9`
- `artifacts`:
  - `artifacts/_tmp_s0f_9h_p1_auth_entry_and_admission_slice.json`
- `expected`:
  - login/register stop acting as free role-fabrication surfaces
  - pending identities must stop on onboarding before protected member/admin routes
  - claimed local admission must derive admitted tenant role and preserve the stable `9F/9G` runtime model
- `observed`:
  - shared auth shell now creates `pending` or `admitted` session state instead of treating form role as standing truth
  - onboarding now provides one explicit local-first admission claim path for pending identities
  - focused Playwright drills now prove the new admission flow plus existing subscription gating, tenant context, and local actor switching on the updated session model

### P2-C1-S1S2 (Routed-entry and tenant-aware landing landed | 2026-04-19)

- `headSha`: `pending-backfill`
- `artifacts`:
  - `artifacts/_tmp_s0f_9h_p2_routed_entry_and_tenant_landing.json`
- `expected`:
  - pending identities preserve safe intended destination through onboarding instead of dropping route intent
  - admitted actors land on role-compatible, tenant-aware entry surfaces without hidden fallback authority
  - admitted admins default to a tenant-scoped admin route rather than a generic console landing
- `observed`:
  - shared landing resolution now accepts safe `next` intent across login, register, onboarding, protected-route redirects, and dev-only actor switching
  - admitted `admin/owner` now land on `/admin/subscriptions/{libraryId}` while admitted `member` remains on `/workbox/subscription`
  - focused Playwright drills now prove admin-target intent survives onboarding and that tenant-scoped admin landing is the default for admitted admin actors

## Recent changes (for traceability, optional)

- 2026-04-19: opened `S0F-9H` as the next auth-entry and onboarding lane after stable close-out of `S0F-9G`, targeting shared auth/provider realism, membership admission, and routed entry rather than support tooling or payment-provider realism.
- 2026-04-19: completed `S0F-9H/P0-C1-S1S2S3` by fixing the first shared auth-entry realism boundary, explicit membership-admission contract, and tenant-aware routed-entry contract in one evidence-backed packet.
- 2026-04-19: completed `S0F-9H/P1-C1-S1S2` by removing free role fabrication from login/register, landing the first explicit local-first admission page, and proving the updated auth/admission flow together with existing gating and tenant-context drills.
- 2026-04-19: completed `S0F-9H/P2-C1-S1S2` by unifying routed-entry resolution, preserving safe `next` intent through onboarding, and landing tenant-scoped admin defaults on the current Workbox/auth stack.