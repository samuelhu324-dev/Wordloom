# log-S4F-1A (Phase 1: Backend-only access / subscription deployable cut)

---

**id**: `S4F-1A`
**kind**: `log`
**title**: `backend-only access / subscription deployable cut (S4D workflow reuse, access-aware verify, and drills/evidence) v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, AccessControl, Verification, Drills, Evidence, epic/s4, sub/1a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **roadmap**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
  **parent_log**: `docs/logs/log-S4F-access-subscription-deployable-runtime-cut.md`
  **previous_log**: `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
  **reference_log_1**: `docs/logs/log-S4D-1A-cloud-runtime-release-path.md`
  **reference_log_2**: `docs/logs/log-S0F-9C-backend-vertical-slice-for-subscription-access-minimum-closure.md`
  **reference_log_3**: `docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md`
  **reference_log_4**: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
**issue_keyword**: `runtime`
**issue_top_labels**: ``
**issue_scope_labels**: ``
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
**roadmap_milestone**: `M1`
**roadmap_phase**: `M1-P3`
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-20`
**updated**: `2026-04-20`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this runtime packet.
- Day-level precision is acceptable here because the lane is opening as one bounded deployable-cut packet rather than one fine-grained execution replay.
- `reviewed` should remain `pending` until the first backend-only access/subscription deployable cut is explicitly accepted.

## Decision / Outcome

**Decision**:

- `S4F-1A` opens the first concrete `road-002-01/M1` execution packet as a backend-only access/subscription deployable cut.
- The packet reuses the stable `S4D` single-entry release workflow, target shape, and evidence bundle, but replaces generic backend smoke with access-aware verify and member/admin drill contracts.

**Default choices (phase defaults / v1)**:

- Keep the deployable unit as one backend container on one Linux VM against external cloud-dev RDS.
- Keep frontend cloud closure out of scope for this first lane; the deployed proof should come from backend/API truth first.
- The first verify contract must prove more than `health` and `libraries`: it must cover at least one member-facing access read, one admin-facing subscription read, and one bounded lifecycle mutation followed by re-read.
- Reuse `summary.json`, `operator_guidance.txt`, and the existing `S4D` failure taxonomy shape unless one access-specific gap proves a bounded extension is needed.
- Do not widen into provider realism, UI hosting, worker runtime, or object-storage work in this packet.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S4F-1A` is expected to drive the first concrete deployable-cut PR under `road-002-01/M1`.

**PR summary bullets**:

- Reuse the stable `S4D` cloud release workflow for the first backend-only access/subscription deployable cut.
- Fix an access-aware verify contract that checks member read, admin read, and bounded lifecycle re-read instead of generic backend smoke only.
- Prove the first deployed member/admin drill pair on the existing backend access/subscription slice before considering frontend cloud closure.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S4F-1A-backend-only-access-subscription-deployable-cut.md`
- Runbook: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
- Evidence artifact: ``

**Evidence Footer Source**:

- `P1-C1-S1S2` | artifact: ``

## Definitions (optional)

- `backend-only deployable cut`: one deployed runtime proof that stops at backend/API truth and does not yet require cloud-hosted UI.
- `access-aware verify`: one verify surface that checks the deployed access/subscription contract rather than generic runtime liveness alone.
- `member flow`: one bounded user-facing read path derived from current tenant, subscription state, and effective entitlement truth.
- `admin flow`: one bounded admin-facing read or mutation path for subscription state and membership-aware access standing.

## Constraints

- Do not invent a second release workflow beside `scripts/ops/cloud_release_workflow.sh`.
- Do not redefine the stable backend module contract already fixed in `S0F-9C`; consume it as the deployable feature surface.
- Do not require full frontend cloud hosting or browser E2E for the first packet to pass.
- Do not accept a verify contract that proves only generic container liveness while skipping access/subscription semantics.

## Scope

- `P0`: contract (deployable cut boundary, verify surface, evidence contract)
- `P1`: implementation / packaging (bind the current backend access/subscription slice into the reused `S4D` release path)
- `P2`: drill / verify (run deployed member/admin/lifecycle checks)
- `P3`: close-out / next-lane decision (decide whether frontend cloud closure is now justified)

## Success Criteria (DoD)

- The packet fixes one explicit backend-only AWS v1 cut for the access/subscription slice.
- The packet reuses the stable `S4D` release workflow and evidence shape without creating a second operator path.
- The deployed verify contract covers at least:
  - one member-facing access-context read
  - one admin-facing subscription-state read
  - one bounded lifecycle mutation followed by deterministic re-read
- The packet leaves one explicit decision about whether the next lane should add frontend cloud closure.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the deployable-cut boundary is explicit;
  - the access-aware verify and drill contract is explicit;
  - at least one deployed evidence bundle proves the backend-only member/admin/lifecycle flow end to end.

## P0 (Contract | v1)

### P0-C1-S1 (Backend-only deployable cut boundary | v1)

- Reuse the existing `S4D` target shape:
  - one Linux VM
  - one backend container
  - one external cloud-dev RDS
- The feature slice inside that target is the current backend access/subscription surface, not the whole product.
- The first packet includes:
  - shared auth/admission-backed backend truth already present in repo
  - current tenant context and membership-aware access truth
  - subscription/access aggregation reads
  - bounded admin lifecycle mutation support
- The first packet excludes:
  - frontend cloud hosting
  - worker deployment
  - provider callbacks and real billing integration

### P0-C1-S2 (Access-aware verify contract | v1)

- The verify surface must extend generic runtime smoke with the following feature checks:
  - member read: current access-context or equivalent member-facing aggregated read returns expected standing
  - admin read: current subscription/admin detail read returns expected state/history
  - lifecycle re-read: one bounded admin event changes lifecycle state and the resulting read path reflects the change deterministically
- Generic `health` and startup checks remain necessary but are no longer sufficient by themselves.

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - `headSha`
  - `targetHostKind`
  - `envFilePath`
  - `imageTag`
  - `memberReadResult`
  - `adminReadResult`
  - `lifecycleMutationResult`
  - `rerenderedStateResult`
  - `deployResult`
  - `verifyResult`
  - `rollbackResult`
  - `result`

## P1 (Implementation / packaging | v1)

### P1-C1-S1 (Reuse binding onto the stable `S4D` workflow | v1)

- `S4F-1A` does not open a second deploy path; the canonical operator entry remains `bash scripts/ops/cloud_release_workflow.sh`.
- The reused deploy target remains exactly the stable `S4D` target tuple:
  - one Linux VM reached over SSH
  - one backend container
  - one cloud-dev env file
  - one external cloud-dev RDS
- `S4F-1A` reuses the existing `S4D` stage contract unchanged for preflight, deploy, generic runtime verify, summary, guidance, and optional rollback:
  - `preflight.log`
  - `deploy.log`
  - `verify.log`
  - `rollback.log`
  - `summary.json`
  - `operator_guidance.txt`
- The only `S4F-1A` specialization in `P1` is the feature-level verify overlay that must run against the deployed API after the generic `S4D` verify gate is green.
- The deployed API contract reused by this packet is:
  - auth carrier: `Authorization: Bearer <jwt>`
  - tenant carrier: `X-Library-Id: <library-id>`
  - base URL shape: `http://<target-host>:<api-port>/api/v1`
- `P1` fixes one explicit operator-supplied verify tuple instead of inventing setup automation in this packet:
  - `VERIFY_LIBRARY_ID`: one existing library id that already has a valid subscription row in the deployed environment
  - `MEMBER_TOKEN`: one JWT whose `user_id` resolves to `member` standing for `VERIFY_LIBRARY_ID`
  - `ADMIN_TOKEN`: one JWT whose `user_id` resolves to `admin` or `owner` standing for `VERIFY_LIBRARY_ID`
  - `API_BASE_URL`: deployed backend base URL rooted at `/api/v1`
- `P1` therefore binds the current access/subscription slice into the reused `S4D` path as: `S4D deploy + generic verify PASS` -> `S4F access-aware probes` -> `S4F evidence write-up`.

### P1-C1-S2 (Deploy-time feature probes fixed | v1)

- The first deployed verify contract is fixed as exactly three probes and one shared input block:

```bash
API_BASE_URL="http://<target-host>:<api-port>/api/v1"
VERIFY_LIBRARY_ID="<uuid>"
MEMBER_TOKEN="<jwt>"
ADMIN_TOKEN="<jwt>"
```

- Probe 1: member read

```bash
curl -sS "$API_BASE_URL/access-context/me" \
  -H "Authorization: Bearer $MEMBER_TOKEN" \
  -H "X-Library-Id: $VERIFY_LIBRARY_ID"
```

  Expected result:
  - HTTP `200`
  - response `tenant_id == VERIFY_LIBRARY_ID`
  - response `roles` contains `member`
  - response contains non-empty `plan_code`
  - response contains non-empty `subscription_state`
  - response `entitlements` contains `read_library`

- Probe 2: admin read

```bash
curl -sS "$API_BASE_URL/admin/subscriptions/$VERIFY_LIBRARY_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "X-Library-Id: $VERIFY_LIBRARY_ID"
```

  Expected result:
  - HTTP `200`
  - response `library_id == VERIFY_LIBRARY_ID`
  - response contains non-empty `plan_code`
  - response contains non-empty `subscription_state`
  - response `entitlements` contains `read_library`

- Probe 3: lifecycle mutation + deterministic re-read

```bash
curl -sS -X POST "$API_BASE_URL/admin/subscriptions/$VERIFY_LIBRARY_ID/events" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "X-Library-Id: $VERIFY_LIBRARY_ID" \
  -H "Content-Type: application/json" \
  -d '{"event_type":"upgrade_success"}'

curl -sS "$API_BASE_URL/admin/subscriptions/$VERIFY_LIBRARY_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "X-Library-Id: $VERIFY_LIBRARY_ID"

curl -sS "$API_BASE_URL/admin/subscriptions/$VERIFY_LIBRARY_ID/history" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "X-Library-Id: $VERIFY_LIBRARY_ID"
```

  Expected result:
  - mutation call HTTP `200`
  - mutation response `library_id == VERIFY_LIBRARY_ID`
  - mutation response `subscription_state == active`
  - re-read call HTTP `200`
  - re-read response `subscription_state == active`
  - history call HTTP `200`
  - history response contains at least one item whose `event_type == upgrade_success`
- The first lifecycle probe is intentionally fixed as one single-step `upgrade_success` promotion. `renewal_failed` or longer chains can be added later in `P2` evidence if one deployed sample proves they are worth widening.
- `P1` does not require a separate feature script yet. The minimum acceptable implementation for this packet is that the three HTTP probes above can be run deterministically against one deployed backend cut and written back into the `S4D` evidence bundle as `memberReadResult`, `adminReadResult`, `lifecycleMutationResult`, and `rerenderedStateResult`.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4F-1A/P<phase>-C<cycle>-S<steps>: <summary>`

**Branch convention**:

- `S4F-1A` 相关实现与文档优先落在 `S4F-access-subscription-deployable-runtime-cut` 分支。

**Commit discipline (recommended)**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4F-access-subscription-deployable-runtime-cut`。

## Plan (draft)

### P1 (Implementation / packaging)

- P1-C1-S1: map the current backend access/subscription slice onto the reused `S4D` release target
- P1-C1-S2: define the concrete deploy-time verify commands and feature-specific probes

### P2 (Drill / Verify)

- P2-C1-S1: execute one deployed member-facing access read
- P2-C1-S2: execute one deployed admin read and one bounded lifecycle mutation followed by re-read

### P3 (Close-out / next-lane decision)

- P3-C1-S1: record whether backend-only deployed proof is sufficient or whether frontend cloud closure should open next

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: backend-only deployable cut boundary fixed
- [x] `P0-C1-S2`: access-aware verify contract fixed
- [x] `P0-C1-S3`: evidence contract fixed

### P1 (Implementation / packaging)

- [x] `P1-C1-S1`: reused `S4D` release path bound to the current access/subscription backend slice
- [x] `P1-C1-S2`: deploy-time feature probes fixed

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: deployed member read proved
- [ ] `P2-C1-S2`: deployed admin read + lifecycle re-read proved

### P3 (Close-out / next-lane decision)

- [ ] `P3-C1-S1`: next-lane decision recorded

## Current Status (recommended)

- `S4F-1A/P1` is now fixed at the contract level: the packet reuses the stable `S4D` workflow and now carries one explicit deployed verify tuple plus three concrete feature probes.
- The next step is `P2`: run the deployed member read, admin read, and lifecycle re-read against one real `VERIFY_LIBRARY_ID`, then write the resulting evidence bundle back into this log.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, deploy parameters, and deployed member/admin verify artifacts once they exist.

## Recent changes (for traceability, optional)

- 2026-04-20: first created `S4F-1A` as the backend-only access/subscription deployable-cut packet under `road-002-01/M1-P3`.
- 2026-04-20: completed `P1-C1-S1S2` by binding the packet to the stable `S4D` operator workflow and fixing the first three deployed access-aware verify probes.