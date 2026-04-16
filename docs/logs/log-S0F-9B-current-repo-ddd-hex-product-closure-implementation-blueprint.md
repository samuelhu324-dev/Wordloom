# log-S0F-9B (Phase 9B: Current-repo DDD/HEX product-closure implementation blueprint)

---

**id**: `S0F-9B`
**kind**: `log`
**title**: `current-repo DDD-HEX product-closure implementation blueprint packet v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Access, Billing, Architecture, Runtime, Drills, Evidence, epic/s0, sub/9b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
  **reference_log_1**: `docs/logs/log-S0F-10A-book-first-access-control-minimum-closure.md`
  **reference_log_2**: `docs/logs/log-S0F-10B-plan-and-entitlement-minimum-widening.md`
  **reference_log_3**: `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
  **reference_log_4**: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
  **reference_log_5**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**issue_keyword**: `runtime`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/9b`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M4`
**roadmap_phase**: `M4-P1`
**roadmap_bridge_refs**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md#M4-P1`
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-16`
**updated**: `2026-04-16`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this blueprint packet.
- Day-level precision is acceptable while this lane is still deciding concrete repo landing shape rather than running implementation drills.
- If this lane later becomes the active source log for implementation work, subsequent updates should preserve deterministic roadmap bridge, issue, and PR fields rather than inferring them from downstream code changes.

## Decision / Outcome

**Decision**:

- `S0F-9B` opens as one bounded implementation-blueprint packet for the current repo's mixed `DDD/HEX + modular-monolith` architecture after the `M4` boundary stack in `S0F-10A/10B/10C/10D` is already explicit.
- The first deliverable is not one provider integration or one UI mock alone; it is one defended implementation blueprint that answers where the new commercial-access closure should land in backend modules, infrastructure adapters, frontend validation surfaces, and replay-facing APIs.
- This lane should keep the first implementation target local-first and repo-native: one bounded module family inside the current backend monolith, plus thin `admin / user / mock billing / replay` surfaces that exercise the backend state model.

**Default choices (phase defaults / v1)**:

- Keep the backend landing shape aligned to the repo's current mixed `DDD/HEX` pattern rather than opening a separate service too early.
- Keep existing auth/membership infrastructure as the source of collaboration-role standing.
- Keep the new commercial-access closure responsible for `plan`, `subscription_state`, `payment_event`, and `entitlement_snapshot` rather than overloading existing role semantics.
- Keep frontend validation surfaces thin and local-first; do not let the browser become the source of policy truth.
- Keep provider realism deferred; the first implementation loop should still rely on bounded local event simulation.

## PR Summary Inputs (optional)

- Use this block because `S0F-9B` is intended to become the implementation-facing source packet for the next concrete `M4-P1` work.

**PR summary bullets**:

- Open one bounded implementation-blueprint packet for the `M4` product closure on the current repo architecture.
- Fix the intended backend module, infra adapter, API, and frontend validation-surface landing points before generating code.
- Keep provider realism deferred while making the admin/user/mock-billing/replay loop explicit enough for implementation planning.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0F-9B-current-repo-ddd-hex-product-closure-implementation-blueprint.md`
- Previous log: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`

## Exported Sections / Outlet Ownership

- This slice starts as one `log-retained core + implementation-blueprint contract-first` lane.
- The expected first landing is one stable implementation blueprint that answers backend module boundaries, infra persistence shape, API surface, frontend validation surfaces, and first local verification loop.

**Outlet ownership**:

- `contract`: define the bounded implementation blueprint for the current repo architecture
- `runbook`: no-op at packet open; operator procedure should wait until the first code-bearing implementation slice exists
- `view`: no-op at packet open; reader-facing summary should wait until the first blueprint table is explicit
- `index/front-door`: no-op at packet open
- `disposition/placement`: no-op at packet open
- `log-retained core`: lane boundary, architecture decisions, implementation plan, execution checklist, and later evidence ledger remain here

## Definitions (optional)

- `commercial-access closure`: the bounded capability family that combines plan, lifecycle state, payment events, and entitlement outcomes without replacing collaboration-role semantics.
- `backend module family`: one repo-native module under `backend/api/app/modules/...` that owns domain and application logic for the new closure.
- `access context`: one aggregated surface that combines existing auth/membership standing with computed commercial entitlement outcome.
- `mock billing panel`: one bounded admin-facing UI surface that emits trusted local events such as `upgrade_success` and `renewal_failed`.
- `scenario replay console`: one debug or admin-facing surface that replays the first `10D` scenario set step by step and returns invariant checks.

## Constraints

- Do not rewrite existing membership/auth infrastructure into the new module.
- Do not split the first implementation into a separate payment microservice.
- Do not let frontend surfaces become the source of entitlement policy truth.
- Do not introduce real provider webhook, invoice, tax, or settlement realism in the opening implementation packet.
- Do not collapse `role`, `plan`, `subscription_state`, and `entitlement_snapshot` back into one overloaded permission field.

## Scope

- `P0`: implementation-blueprint contract for backend, infra, API, and frontend landing shape
- `P1`: repo-path and code-generation plan for the first bounded backend module and validation surfaces
- `P2`: local verification and replay plan for the first admin/user/mock-billing loop
- `P3`: provider-adapter defer and later split decision for post-closure widening

## Success Criteria (DoD)

- The lane fixes one concrete backend module landing shape aligned to the repo's current mixed `DDD/HEX + modular-monolith` pattern.
- The lane fixes one concrete infra landing shape for persistence models and repository implementations.
- The lane fixes one concrete API and frontend validation-surface set for `user`, `admin`, `mock billing`, and replay use cases.
- The lane keeps collaboration-role standing separate from commercial entitlement outcome.
- The lane leaves one reader able to answer which files, module folders, and first endpoints should be created before implementation begins.
- The lane keeps provider realism explicitly deferred while still defining one local-first validation loop.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the backend, infra, API, and frontend landing shape are explicit
  - the first code-generation and verification plan is explicit
  - the provider-defer handoff rule for this implementation packet is explicit
  - the Evidence section includes traceable `headSha` values plus artifact paths
- `stable` for this blueprint packet does not require code to be merged; it requires the implementation shape to be explicit enough that the next code-bearing slice does not need to rediscover the architecture.

## P0 (Contract | v1)

### P0-C1-S1 (Backend module landing shape)

- Fix one intended bounded module family under `backend/api/app/modules/...` for the commercial-access closure.
- Keep domain, application, router, schema, and repository-port responsibilities separate and aligned to current repo patterns.

### P0 Backend Module Decision (v1)

- `P0` is now fixed as one explicit repo-path-and-boundary contract for the first code-bearing `M4` implementation slice.
- The bounded backend module family in this packet is now fixed as `subscription_access`.
- The intended module root in this packet is now fixed as:
  - `backend/api/app/modules/subscription_access/`
- The first module file tree in this packet is now fixed as:
  - `backend/api/app/modules/subscription_access/__init__.py`
  - `backend/api/app/modules/subscription_access/exceptions.py`
  - `backend/api/app/modules/subscription_access/repository.py`
  - `backend/api/app/modules/subscription_access/schemas.py`
  - `backend/api/app/modules/subscription_access/domain/__init__.py`
  - `backend/api/app/modules/subscription_access/domain/models.py`
  - `backend/api/app/modules/subscription_access/domain/value_objects.py`
  - `backend/api/app/modules/subscription_access/domain/event_types.py`
  - `backend/api/app/modules/subscription_access/domain/services.py`
  - `backend/api/app/modules/subscription_access/application/__init__.py`
  - `backend/api/app/modules/subscription_access/application/use_cases.py`
  - `backend/api/app/modules/subscription_access/routers/subscription_access_router.py`
- The first ownership rule for those files is now fixed as follows:
  - `domain/*` owns `Plan`, `Subscription`, `PaymentEvent`, `EntitlementSnapshot`, and value/policy objects such as entitlement rule evaluation inputs
  - `application/use_cases.py` owns orchestration such as `ApplyPaymentEvent`, `ComputeEntitlementSnapshot`, `GetAccessContext`, and `RunScenarioReplay`
  - `repository.py` owns abstract ports only; it should not become an ORM adapter file
  - `schemas.py` owns request and response DTOs for admin events, access-context reads, and replay outputs
  - `routers/subscription_access_router.py` owns HTTP entrypoints only and should delegate policy and recomputation to use cases
- The first aggregation rule in this packet is now fixed as:
  - existing `AuthContext` remains the source of user identity, tenant selection, and collaboration-role standing
  - the new module computes commercial lifecycle and entitlement outcome
  - one higher-level `AccessContext` surface should aggregate both without replacing existing auth semantics
- The preferred first shared landing path for that aggregate surface is now fixed as:
  - `backend/api/app/shared/access_context.py`
- The `P0-C1-S1` success rule in this packet is:
  - one reader should be able to answer exactly which backend module folder should be created first
  - one reader should be able to separate role standing from commercial entitlement calculation
  - one reader should be able to explain why this is one new module family inside the monolith rather than one new microservice

#### P0 Backend Module Table (v1)

| repo path or surface | fixed role in `S0F-9B` | not allowed to do |
| --- | --- | --- |
| `backend/api/app/modules/subscription_access/domain/*` | own commercial-access domain state and rules | read HTTP directly or depend on ORM models |
| `backend/api/app/modules/subscription_access/application/use_cases.py` | orchestrate event application, entitlement recompute, access-context reads, and scenario replay | become the persistence layer or own request parsing |
| `backend/api/app/modules/subscription_access/repository.py` | define repository ports for subscriptions, events, plans, and entitlement snapshots | contain SQLAlchemy implementation detail |
| `backend/api/app/modules/subscription_access/routers/subscription_access_router.py` | expose admin/user/replay HTTP entrypoints | become the place where entitlement policy truth lives |
| `backend/api/app/shared/access_context.py` | aggregate auth standing with computed commercial entitlement | replace `AuthContext` as the source of authentication or membership truth |

### P0-C1-S2 (Infra and frontend landing shape)

- Fix one intended infra landing shape under `backend/infra/database/models/...` and `backend/infra/storage/...`.
- Fix one intended frontend validation-surface set for `user`, `admin`, `mock billing`, and scenario replay.

### P0 Infra And Frontend Decision (v1)

- The first infrastructure landing shape in this packet is now fixed as:
  - `backend/infra/database/models/plan_catalog_models.py`
  - `backend/infra/database/models/subscription_models.py`
  - `backend/infra/database/models/payment_event_models.py`
  - `backend/infra/database/models/entitlement_snapshot_models.py`
  - `backend/infra/storage/plan_catalog_repository_impl.py`
  - `backend/infra/storage/subscription_repository_impl.py`
  - `backend/infra/storage/payment_event_repository_impl.py`
  - `backend/infra/storage/entitlement_snapshot_repository_impl.py`
- The first infrastructure rule in this packet is now fixed as:
  - ORM models should follow the existing repo pattern where persistence models live under `backend/infra/database/models/...`
  - storage implementations should follow the existing repo pattern where SQLAlchemy adapters live under `backend/infra/storage/...`
  - the new commercial-access infra should reuse existing membership/auth data where needed and must not fork that source of truth
- The first API surface set in this packet is now fixed as:
  - `GET /api/v1/access-context/me`
  - `GET /api/v1/admin/subscriptions/{libraryId}`
  - `POST /api/v1/admin/subscriptions/{libraryId}/events`
  - `POST /api/v1/admin/subscriptions/{libraryId}/corrections`
  - `GET /api/v1/admin/subscriptions/{libraryId}/history`
  - `POST /api/v1/admin/scenario-replays/{scenarioName}`
- The first frontend validation-surface set in this packet is now fixed as:
  - `frontend/src/app/admin/subscriptions/page.tsx`
  - `frontend/src/app/admin/subscriptions/[libraryId]/page.tsx`
  - `frontend/src/app/admin/scenario-replays/page.tsx`
  - `frontend/src/features/subscription-access/ui/AccessContextPanel.tsx`
  - `frontend/src/features/subscription-access/ui/MockBillingPanel.tsx`
  - `frontend/src/features/subscription-access/ui/ScenarioReplayPanel.tsx`
  - `frontend/src/widgets/library/LibraryAccessWidget.tsx`
- The first frontend responsibility rule in this packet is now fixed as:
  - `admin/subscriptions/*` pages inspect subscription state and emit bounded admin/payment events
  - `admin/scenario-replays/page.tsx` runs the first `10D` scenario set and renders step-by-step replay results plus invariant checks
  - `LibraryAccessWidget.tsx` or equivalent user-facing widget reads aggregated access context and renders gated actions such as `copy_block_cross_book` and `export_book`
  - feature components should remain thin and should render backend-derived state rather than re-implementing entitlement rules locally
- The `P0-C1-S2` success rule in this packet is:
  - one reader should be able to answer which ORM and repository files should be created first
  - one reader should be able to answer which first endpoints and frontend pages belong in the local validation loop
  - one reader should be able to explain that mock billing is one controlled admin-facing event surface, not one fake provider integration

#### P0 Infra And Frontend Table (v1)

| repo path or surface | fixed role in `S0F-9B` | not allowed to do |
| --- | --- | --- |
| `backend/infra/database/models/*subscription*` and related files | persist plan catalog, lifecycle state, events, and entitlement snapshots | own HTTP semantics or frontend-facing policy summaries |
| `backend/infra/storage/*_repository_impl.py` for the new module | implement SQLAlchemy adapters for the module ports | become the domain-model source of truth |
| `GET /api/v1/access-context/me` | expose one aggregated user-facing access context | mutate lifecycle state |
| `POST /api/v1/admin/subscriptions/{libraryId}/events` | emit bounded lifecycle/payment events for local-first validation | accept arbitrary provider payloads |
| `frontend/src/app/admin/scenario-replays/page.tsx` | run and inspect bounded replay drills | become a second backend orchestration layer |
| `frontend/src/widgets/library/LibraryAccessWidget.tsx` | render user-visible gated actions from backend-derived access context | compute entitlement rules independently in the browser |

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - `plannedModulePath`
  - `plannedInfraPaths`
  - `plannedApiSurfaces`
  - `plannedFrontendSurfaces`
  - `verificationLoop`
  - `providerDeferDecision`

### P0 Evidence Contract Decision (v1)

- The first evidence shape in this packet is now fixed as one implementation-blueprint artifact rather than one runtime drill output.
- The minimum evidence payload in this packet is now fixed as:
  - `plannedModulePath`: the chosen backend module root
  - `plannedModuleFiles`: the first module file tree
  - `plannedInfraPaths`: the chosen ORM and repository implementation paths
  - `plannedApiSurfaces`: the first endpoint set for access reads, admin events, and replay
  - `plannedFrontendSurfaces`: the first page/component set for `user`, `admin`, `mock billing`, and replay
  - `verificationLoop`: the first local-first validation loop such as `trial upgrade -> active entitlement -> renewal failure -> narrowed entitlement`
  - `providerDeferDecision`: the explicit rule that provider realism remains out of scope for the first code-bearing slice
- The first representative verification loop in this packet is now fixed as:
  - load one user-facing library surface under narrower trial standing
  - emit `upgrade_success` from one admin/mock billing surface
  - verify widened access in `GET /api/v1/access-context/me`
  - emit `renewal_failed`
  - verify narrowed or suspended entitlement outcome while role standing remains unchanged
- The `P0-C1-S3` success rule in this packet is:
  - one later implementation slice should be able to generate files and APIs without rediscovering the basic repo-path contract
  - one reader should be able to explain what the first evidence artifact must prove before code is judged coherent
  - one reader should be able to explain why provider realism is still intentionally absent from the opening implementation slice

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-9B/P<phase>-C<cycle>-S<steps>: <summary>`

## Plan (draft)

### P1 (Repo-path and code-generation plan)

- `P1-C1-S1`: fix the first backend module/file tree for the commercial-access closure on the current repo architecture
- `P1-C1-S2`: fix the first infra and API path set, including persistence models, repositories, routers, and schemas

### P2 (Local verification and replay plan)

- `P2-C1-S1`: fix the first admin/user/mock-billing validation loop against the current SoT
- `P2-C1-S2`: map the first `10D` scenario replay set to concrete backend/API/frontend verification points

### P3 (Provider-adapter defer decision)

- `P3-C1-S1`: define what later provider-adapter work may add without changing the implementation blueprint
- `P3-C1-S2`: define the later-packet entry conditions for real provider realism after the first local closure exists

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: fix the backend module landing shape
- [x] `P0-C1-S2`: fix the infra and frontend landing shape
- [x] `P0-C1-S3`: fix the implementation evidence contract

### P1 (Repo-path and code-generation plan)

- [ ] `P1-C1-S1`: fix the first backend module/file tree
- [ ] `P1-C1-S2`: fix the first infra and API path set

### P2 (Local verification and replay plan)

- [ ] `P2-C1-S1`: fix the first admin/user/mock-billing validation loop
- [ ] `P2-C1-S2`: map the first scenario replay set to concrete verification points

### P3 (Provider-adapter defer decision)

- [ ] `P3-C1-S1`: define later provider-adapter permissions and limits
- [ ] `P3-C1-S2`: define later-packet entry conditions

## Current Status (recommended)

- `S0F-9B` is now opened as one implementation-blueprint packet after the `M4` boundary stack in `10A/10B/10C/10D` has been stabilized.
- `P0` is now complete: the lane now fixes one first backend module family, one first infra landing shape, one first API and frontend validation-surface set, and one first evidence contract for the local product closure.
- The lane remains a `draft` source log because the concrete code-generation file tree expansion in `P1`, the verification mapping in `P2`, and the later provider-handoff boundary in `P3` still remain open.
- The next step should be `P1`, where the first repo-path file-generation plan should be fixed in more detailed sequence; automation should still read this log as the active source for this packet.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2S3 (Implementation-blueprint landing contract fixed | 2026-04-16)

- headSha: `586a8c8f9`
- artifacts: `docs/logs/log-S0F-9B-current-repo-ddd-hex-product-closure-implementation-blueprint.md`
- expected:
  - `P0` fixes the first concrete backend module landing shape for the new commercial-access closure.
  - `P0` fixes the first concrete infra, API, and frontend validation-surface set.
  - `P0` fixes one evidence contract and one first local validation loop while keeping provider realism deferred.
- observed:
  - Added one explicit backend module decision, one infra and frontend landing decision, one implementation evidence contract decision, completed the `P0` checklist, and updated packet status for the next `P1` repo-path planning phase.

## Recent changes (for traceability, optional)

- 2026-04-16: Opened `S0F-9B` as one bounded implementation-blueprint packet for the current repo's mixed `DDD/HEX + modular-monolith` product-closure work after the `M4` boundary stack stabilized.
- 2026-04-16: Completed `S0F-9B/P0` by fixing the first backend module, infra path, API surface, frontend validation-surface, and implementation evidence contract for the local product-closure loop.