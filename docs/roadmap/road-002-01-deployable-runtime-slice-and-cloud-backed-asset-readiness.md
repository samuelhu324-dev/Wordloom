# road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness

---

**id**: `road-002-01`
**kind**: `roadmap`
**title**: `002-01: deployable runtime slice, credible simulation, and cloud-backed asset-platform readiness`
**status**: `draft`
**scope**: `002-01`
**tags**: `ROADMAP, branch-road, aws, deployable runtime, credible simulation, asset platform, access control`
**links**: ``
  **source**: `docs/roadmap/road-template-branch-roadmap.md`
  **parent_road**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **reference_log_1**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **reference_log_2**: `docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md`
  **reference_log_3**: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
**created**: `2026-04-19`
**updated**: `2026-04-19`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for roadmap frontmatter.
- Day-level precision is acceptable here because this branch road is opening as one focused execution detour rather than a second mainline.
- `reviewed` should remain `pending` until the first deployable-cut boundary and its parent contribution rows are explicitly accepted.

## Positioning

**Context / role targeting**

- Use this branch road when the `road-002` mainline has enough stable local-first access and product-entry work to support a real deployment cut, but the concentrated AWS/runtime packaging and realism-tightening details would otherwise flood the parent roadmap.
- This branch is not a replacement for `road-002`; it is the focused detour that turns the already-stable `M4` access/auth/subscription slices into one platform-demo story that can later support `M5` asset-platform work on real cloud primitives.

**One-sentence goal**

- Turn the current stable local-first auth/access/subscription slices into one deployable AWS-oriented runtime cut, tighten the simulation boundary until it is credible, and define the exact readiness bar for a cloud-backed `Asset Platform` v1.

## Parent / Branch Rules

- This branch road contributes back to `road-002` and must keep every concentrated slot mapped back to explicit parent `M4` or `M5` rows.
- This branch owns packaging, prioritization, and realism-tightening rules for the deployable cut; child logs still own implementation, drills, and evidence.
- The branch must prefer already-stable child logs where they exist, and use `unmapped` explicitly where the next execution packet has not yet been opened.
- This branch must not reopen the already-stable `9G/9H/10A-10D` contracts unless one AWS/runtime packaging decision or realism-tightening requirement proves that a bounded child packet is necessary.

## Scope & Audience

- **Primary audience**: repo owner, platform-engineering/interview readers, and future operators who need to understand what the first cloud-deployable Wordloom slice actually includes.
- **Relation to parent road**: concentrates the already-stable `M4` access/auth/subscription stack into one deployable runtime story and sets the gating rule for `M5` cloud-backed asset-platform entry.
- **Time horizon**: 4-8 weeks.

## Roadmap / Log Bridge Contract

- This branch roadmap owns the deployable-cut boundary, credible-simulation threshold, AWS-v1 packaging rule, and asset-readiness gate for the concentrated slice.
- Child logs still own implementation and evidence.
- Parent contribution remains explicit and must be recorded both here and in the parent branch register.

## Parent Contribution Ledger

- `parent M4-P0 <- docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
- `parent M4-P0 <- docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
- `parent M4-P1 <- docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md`
- `parent M4-P1 <- docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md`
- `parent M4-P1 <- docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
- `parent M4-P2 <- docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- `parent M4-P3 <- docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- `parent M5-P0 <- unmapped`

## Milestone overview

- **M1. Deployable runtime slice and AWS v1 closure**
- **M2. Credible simulation tightening on top of the stable `M4` stack**
- **M3. Cloud-backed asset-platform readiness cut**

## Milestones

### M1: Deployable runtime slice and AWS v1 closure

**Goal**

- Select one bounded Wordloom slice that is already stable enough to deploy, verify, drill, and destroy on AWS without pretending the whole `road-002` mainline is finished.
- The intended slice is the current auth/access/subscription/product-entry stack: shared login/register/admission, `Workbox > My Subscription`, `Workbox > Subscription Console`, tenant-scoped admin detail, backend access context, tenant membership management, and one bounded mock-billing or lifecycle drill.

**Bridge Ledger (child logs only)**

- `M1-P0`:
  - `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
  - `docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
- `M1-P1`:
  - `docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md`
  - `docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md`
  - `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
- `M1-P2`:
  - `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- `M1-P3`:
  - `unmapped`

**Parent alignment**

- `parent M4-P0 <- docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
- `parent M4-P0 <- docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
- `parent M4-P1 <- docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md`
- `parent M4-P1 <- docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md`
- `parent M4-P1 <- docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
- `parent M4-P2 <- docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`

**Plan (P0-P3)**

- `P0` Contract: define the exact deployable cut and list what must be inside AWS v1 versus what must be deferred.
- `P1` Implementation: package one standard path such as `deploy -> verify -> drill -> destroy` around the selected runtime slice.
- `P2` Drill: prove one admin flow and one member flow on the deployed environment using the same tenant-aware and subscription-aware runtime model already stabilized locally.
- `P3` Drill: backfill the first deployment-facing child log once the cut, commands, and verification surface are stable enough to justify a new packet.

### M2: Credible simulation tightening on top of the stable `M4` stack

**Goal**

- Stop treating the current auth/access/subscription slice as “only a simple demo” by making explicit which parts remain local-first scaffolding and which parts must become backend-issued or persistence-backed truth before the deployed slice can be described as credible.

**Bridge Ledger (child logs only)**

- `M2-P0`:
  - `docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
  - `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
- `M2-P1`:
  - `docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md`
  - `docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md`
  - `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
- `M2-P2`:
  - `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- `M2-P3`:
  - `unmapped`

**Parent alignment**

- `parent M4-P0 <- docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
- `parent M4-P0 <- docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
- `parent M4-P1 <- docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md`
- `parent M4-P1 <- docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md`
- `parent M4-P1 <- docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
- `parent M4-P2 <- docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
- `parent M4-P3 <- docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`

**Plan (P0-P3)**

- `P0` Contract: define the credibility line explicitly: frontend may not be the final authority for identity, role standing, tenant standing, or payment-state outcome.
- `P1` Implementation: move the deployable slice toward backend-issued identity/session truth, persistence-backed admission and membership truth, and backend-enforced lifecycle and entitlement state.
- `P2` Drill: prove that the first deployed drill paths mutate backend state and database-backed truth instead of only changing local browser state.
- `P3` Drill: open a bounded child packet only when a concrete realism-tightening unit is large enough to deserve its own contract and evidence.

### M3: Cloud-backed asset-platform readiness cut

**Goal**

- Define the exact readiness rule by which `Asset Platform` may open as a cloud-backed capability, so `M5` starts from real object-storage, signed-access, retention, and audit semantics rather than from another local-only module.

**Bridge Ledger (child logs only)**

- `M3-P0`:
  - `unmapped`
- `M3-P1`:
  - `unmapped`
- `M3-P2`:
  - `unmapped`
- `M3-P3`:
  - `unmapped`

**Parent alignment**

- `parent M5-P0 <- unmapped`
- `parent M5-P1 <- unmapped`
- `parent M5-P2 <- unmapped`
- `parent M5-P3 <- unmapped`

**Plan (P0-P3)**

- `P0` Contract: fix the first asset-platform entry rule: one bounded cloud object class, one metadata/blob split, one signed-access rule, and one tenant-scoped ownership rule.
- `P1` Implementation: prefer S3-compatible object storage, database metadata, signed URL access, retention/lifecycle controls, and explicit tenant scoping over another browser-local or filesystem-local simulation.
- `P2` Drill: prove upload, fetch, revoke/delete, and retention or export behavior on the same cloud-backed model.
- `P3` Drill: decide whether the first asset slice remains part of the modular monolith or becomes operationally distinct only after the cloud-backed path is stable.

## AWS v1 Cut Rule

- The first AWS runtime cut should include only these bounded surfaces:
  - shared auth entry and admission flow;
  - explicit current tenant context and tenant-aware landing;
  - `My Subscription` user view;
  - `Subscription Console` and tenant-scoped admin detail;
  - backend access context, membership management, and one bounded lifecycle/mock-billing drill.
- The first AWS runtime cut should explicitly exclude:
  - real provider integration;
  - enterprise SSO or broad identity sprawl;
  - multi-tenant analytics or support impersonation;
  - broad media/object handling beyond what is required for future asset readiness.

## Credible Simulation Threshold

- The deployed slice should be considered credible when:
  - frontend forms no longer act as the final authority for tenant/admin standing;
  - backend-issued or backend-validated identity truth exists for the deployed path, even if a local-first adapter still remains available for drills;
  - membership/admission truth is persistence-backed and replayable;
  - entitlement or subscription state changes are computed server-side and observable through the same deployed APIs;
  - at least one member flow and one admin flow can be drilled end to end against the deployed environment.
- The deployed slice should still be described as transitional when:
  - identity proof still depends on local-first scaffolding;
  - provider integration remains deferred;
  - asset/object handling has not yet opened its own cloud-backed packet.

## Asset-Platform Readiness Gate

- `Asset Platform` should not open as a serious lane until this branch has at least fixed:
  - one deployable AWS runtime cut;
  - one credible simulation threshold for identity/membership/access truth;
  - one explicit cloud boundary stating that object storage should carry blobs while relational storage remains the source of truth for tenant, membership, and entitlement metadata.
- The first asset class should remain narrow, such as one evidence attachment, export package, or media-cover/upload class, rather than a repo-wide asset explosion.

## Evidence Pointers (cross-log)

- `docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md` remains the clearest current source for tenant truth and explicit current-tenant context.
- `docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md` remains the clearest current source for backend tenant-admin enforcement and membership mutation authority.
- `docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md` remains the clearest current source for shared auth entry, explicit admission, and tenant-aware routed entry.
- `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md` and `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md` remain the clearest current sources for lifecycle-trigger semantics and replayable scenario proof.

## Recent Changes (optional)

- 2026-04-19: opened `road-002-01` as the first focused branch road under `road-002`, concentrating one deployable AWS runtime cut, one credible-simulation threshold, and one explicit readiness gate for cloud-backed `Asset Platform` work.
- 2026-04-19: fixed the branch scope so it reuses already-stable `M4` child logs rather than pretending the whole parent mainline must finish before AWS packaging can begin.