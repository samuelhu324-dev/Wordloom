# log-S4F-2C (Phase 2 follow-up: Deployed identity/admission/membership truth hardening)

---

**id**: `S4F-2C`
**kind**: `log`
**title**: `deployed identity/admission/membership truth hardening v1`
**status**: `stable`
**scope**: `S4`
**tags**: `EVOLUTION, AccessControl, Auth, CloudRuntime, CredibleSimulation, Drills, Evidence, epic/s4, sub/2c`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/510`
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **roadmap**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
  **parent_log**: `docs/logs/log-S4F-access-subscription-deployable-runtime-cut.md`
  **previous_log**: `docs/logs/log-S4F-2B-release-path-dependency-trust-hardening.md`
  **reference_log_1**: `docs/logs/log-S4F-2B-release-path-dependency-trust-hardening.md`
  **reference_log_2**: `docs/logs/log-S0F-9F-tenant-identity-data-ownership-and-current-tenant-context.md`
  **reference_log_3**: `docs/logs/log-S0F-9G-tenant-admin-enforcement-membership-management-and-local-actor-switching.md`
  **reference_log_4**: `docs/logs/log-S0F-9H-shared-auth-provider-realism-invite-onboarding-and-membership-admission.md`
  **reference_log_5**: `docs/logs/log-S0F-10C-payment-event-subscription-state-entitlement-trigger-packet.md`
  **reference_log_6**: `docs/logs/log-S0F-10D-scenario-catalog-and-mock-state-machine-replays.md`
**issue_keyword**: `runtime`
**issue_top_labels**: ``
**issue_scope_labels**: ``
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
**roadmap_milestone**: `M2`
**roadmap_phase**: `M2-P3`
**roadmap_bridge_refs**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md#M2-P1, docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md#M2-P2, docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md#M2-P3`
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-20`
**updated**: `2026-04-20`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this realism-hardening packet.
- Day-level precision is acceptable while the lane is being opened and scoped.
- `reviewed` should remain `pending` until one explicit credibility boundary and one real deployed evidence sample are retained.

## Decision / Outcome

**Decision**:

- `S4F-2C` opens the next `road-002-01/M2` lane after `S4F-2B`: tighten the deployed access/subscription slice so identity, admission, membership, and lifecycle standing are no longer describable as browser-local or operator-assumed truth.
- The packet's job is not to reopen deployability or network trust; those were already evidenced by `S4F-2A` and hardened by `S4F-2B`.
- The lane should convert one bounded deployed member flow and one bounded deployed admin flow from local-first scaffolding toward backend-issued or persistence-backed truth that can be replayed and verified on the cloud target.

**Default choices (phase defaults / v1)**:

- Keep the release/runtime substrate on the existing `S4D`/`S4F` path unless a bounded realism gap proves that one narrow runtime contract change is required.
- Treat the current problem as a credibility/truth-boundary issue, not as a packaging or RDS-connectivity issue.
- Prioritize backend-issued or backend-validated identity/session truth, persistence-backed admission and membership truth, and backend-enforced lifecycle/entitlement truth before any broader provider integration work.
- Keep provider integration, enterprise SSO sprawl, frontend hosting, and asset-platform work out of this packet.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S4F-2C` is expected to drive the first realism-tightening PR under `road-002-01/M2` once the truth boundary is fixed.

**PR summary bullets**:

- Tighten the deployed access/subscription slice so member/admin truth is backend-issued or persistence-backed rather than browser-local.
- Reuse the already-proven `S4F` cloud runtime path while replacing local-first credibility gaps with deployed server-side truth.
- Capture one deployed member flow and one deployed admin flow whose key state changes are replayable from backend/database-backed evidence.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S4F-2C-deployed-identity-admission-membership-truth-hardening.md`
- Runbook: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
- Evidence artifact: ``

## Definitions (optional)

- `backend-issued or backend-validated identity truth`: deployed identity/session state that the backend issues or verifies, rather than the browser unilaterally asserting standing.
- `persistence-backed admission truth`: invite/admission/membership state that survives reloads and replay through database-backed records rather than in-memory or browser-local scaffolding.
- `credible deployed drill`: a member or admin flow whose key state transitions can be observed through deployed APIs, retained database-backed truth, and repeatable evidence artifacts.

## Constraints

- Do not reopen `S4F-2A` or `S4F-2B` as if deployability or RDS trust were still the primary blocker.
- Do not widen this packet into real provider integration or full auth-platform replacement.
- Do not accept browser-local actor switching, tenant standing, or membership state as the final authority for the deployed path.
- Do not describe the slice as credible unless the retained evidence shows backend/database-backed truth for at least one member flow and one admin flow.

## Scope

- `P0`: contract (credibility boundary, chosen truth surfaces, evidence contract)
- `P1`: implementation (tighten one bounded deployed identity/admission/membership truth path)
- `P2`: drill / verify (retain one member flow and one admin flow against deployed backend/database-backed truth)
- `P3`: close-out / next-lane decision (record what remains transitional and whether another realism packet is required)

## Success Criteria (DoD)

- The lane names one explicit credibility boundary that is still too local-first in the deployed slice.
- One bounded truth model is chosen clearly enough that readers can say what the backend/database now authoritatively owns.
- The deployed path still reuses the `S4F` runtime family unless a narrow, justified contract change is recorded.
- At least one retained member drill and one retained admin drill prove key state changes come from backend/database-backed truth rather than only browser-local state.
- The retained evidence names the identity truth source, membership/admission truth source, and lifecycle/entitlement truth source exercised by the passing run.
- The log leaves one explicit close-out decision on what realism gap remains transitional after this packet lands.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the credibility/truth contract is explicit;
  - one bounded deployed truth path is implemented or otherwise fixed as the default decision;
  - one real evidence sample proves member/admin drills against backend/database-backed truth;
  - the next realism gap, if any, is named explicitly instead of being left as generic “demo-ness”.

## P0 (Contract | v1)

### P0-C1-S1 (Credibility boundary | v1)

- `S4F-2C` treats identity/admission/membership standing as part of the deployed credibility contract, not as incidental frontend scaffolding.
- The brittle boundary to remove is: the deployed slice can still be interpreted as relying on browser-local or operator-assumed truth for who the current actor is, whether admission/membership standing is durable, and whether lifecycle/entitlement outcomes are backend-authoritative.

### P0 Credibility Boundary Decision (v1)

- `P0` now fixes the first controlling credibility gap in this lane as one three-part browser-authority problem on the currently deployed slice:
  - `frontend/src/shared/auth/AuthContext.tsx` still materializes the authenticated session, admitted standing, tenant target, and role claims in browser storage, including the admitted role derived from local admission-code lookup;
  - `frontend/src/app/onboarding/admission/page.tsx` still resolves membership admission through local-first code claim behavior rather than one backend/database-backed admission source;
  - `frontend/src/shared/layouts/LocalActorSwitcher.tsx` still rewrites actor role through explicit `dev-bypass`, which is acceptable as drill scaffolding but cannot remain on the authority path for the first credible deployed member/admin drills.
- The first explicit non-credible rule in this packet is now fixed as:
  - browser-local session state must not remain the final authority for current actor identity or admitted tenant standing on the passing deployed drill paths;
  - local actor switching may remain as a visible dev/drill adapter, but any path that still depends on it is not eligible to count as the first credible deployed member/admin evidence.

### P0-C1-S2 (Chosen truth-model boundary | v1)

- `S4F-2C` chooses one default truth model instead of leaving multiple equal candidates open:
  - one bounded deployed identity/session path should be backend-issued or backend-validated;
  - one bounded admission/membership path should be persistence-backed and replayable;
  - one bounded lifecycle/entitlement outcome should be backend-computed and observable through the same deployed APIs and retained records;
  - browser-local actor or standing shims may remain only as transitional adapters, not as the final authority for the passing drill paths.

### P0 Chosen Truth-Model Decision (v1)

- `P0` now fixes one default truth model for the first `S4F-2C` packet instead of leaving multiple equal realism candidates open:
  - `identityTruthSource` for the first credible deployed path must move from browser-materialized session claims toward backend-validated request identity, using the existing backend auth-context seam (`backend/api/app/shared/auth_context.py`, `backend/api/app/shared/actor.py`, `backend/api/app/config/security.py`) as the authority boundary to tighten next;
  - `admissionTruthSource` and `membershipTruthSource` for the first credible deployed path must move from `LOCAL_ADMISSION_RECORDS` plus browser storage toward persistence-backed tenant membership/admission records that survive reload and replay;
  - `lifecycleTruthSource` may continue to reuse the already-stable backend subscription/access/lifecycle semantics from `S0F-10C/10D`, because this lane's first missing authority boundary is identity/admission/membership rather than lifecycle computation.
- The first bounded authority shift in this lane is now fixed as:
  - preserve the current deployed runtime/release family unchanged;
  - keep `LocalActorSwitcher` and other local-first shims only as explicit non-authoritative drill tooling;
  - treat the first credible target path as one member flow plus one admin flow whose actor identity and tenant standing are accepted by the backend from persistence-backed truth instead of being fabricated entirely in the browser.

### P0-C1-S3 (Evidence contract | v1)

- Evidence for this lane must include at least:
  - `headSha`
  - `workflowCommandSummary`
  - `releaseOriginKind`
  - `targetHostKind`
  - `identityTruthSource`
  - `admissionTruthSource`
  - `membershipTruthSource`
  - `lifecycleTruthSource`
  - `memberFlowResult`
  - `adminFlowResult`
  - `persistenceBackedMutationObserved`
  - `result`

### P0 Evidence Contract Decision (v1)

- `P0` now fixes the first realism evidence contract in this lane as one backend-authority audit packet plus one later deployed drill packet.
- The first artifact path in this packet is fixed as `artifacts/_tmp_s4f2c_p0_truth_boundary_contract.json`.
- The first contract artifact must record at least:
  - `identityTruthSource` with explicit classification of `browser-local`, `backend-validated`, or `backend-issued` for the passing path;
  - `admissionTruthSource` with explicit classification of `local-code`, `persistence-backed`, or later widened source;
  - `membershipTruthSource` with explicit classification of where tenant role/standing is actually read for the passing path;
  - `lifecycleTruthSource` naming the backend lifecycle/entitlement surface reused by the same drill;
  - `localBypassStillPresent` and `localBypassInPassingPath` as separate booleans so the log can distinguish “debug shim still exists” from “debug shim still controls credibility”.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4F-2C/P<phase>-C<cycle>-S<steps>: <summary>`

**Branch convention**:

- `S4F-2C` related implementation and documentation should continue on `S4F-access-subscription-deployable-runtime-cut` unless the realism-hardening work later justifies a narrower focused branch.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit, whether it is contract work, implementation, or drills/evidence, commit/push promptly on the current `S4F` working branch.

## Plan (draft)

### P1 (Implementation)

- P1-C1-S1: identify the narrowest deployed identity/admission/membership slice that still relies on local-first truth and record the exact authority shift required
- P1-C1-S2: land the minimal backend/database-backed changes needed so one member flow and one admin flow can no longer be explained as browser-local-only behavior

### P1 Authority Shift Decision (v1)

- `P1-C1-S1` is now fixed as one request-identity bridge rather than a generic auth rewrite:
  - keep the current frontend local session/admission scaffolding temporarily in place for drill ergonomics;
  - stop allowing no-token dev/demo requests to collapse to one shared backend fallback actor;
  - move the backend-facing actor identity for the known demo sessions onto one explicit request-level actor id that the existing auth-context seam can use before membership lookup.
- The bounded authority shift chosen here is:
  - `frontend/src/shared/auth/AuthContext.tsx` owns a stable `userId` for the current demo actor session instead of only storing role/display state;
  - `frontend/src/shared/api/client.ts` bridges that actor identity into dev requests with `X-Dev-User-Id` while continuing to send `X-Library-Id` / `X-Tenant-Id` for tenant targeting;
  - `backend/api/app/config/security.py` accepts that explicit dev actor id only on the existing no-token fallback path, then continues into persistence-backed tenant membership resolution rather than one process-wide fallback actor.

### P1 Implementation Decision (v1)

- `P1-C1-S2` now lands the smallest code path that makes backend/database-backed standing reachable from the deployed frontend slice:
  - known demo actors (`member@wordloom.dev`, `admin@wordloom.dev`, `owner@wordloom.dev`) now map to stable actor UUIDs inside `AuthSession`;
  - dev-session API requests now carry `X-Dev-User-Id` when no real bearer token is present;
  - backend auth fallback now resolves the current actor from that header before running the already-existing membership repository lookup and owner fallback;
  - a focused backend test proves that the final returned roles come from membership-backed truth for the bridged actor identity.

### P2 (Drill / Verify)

- P2-C1-S1: capture one deployed member flow whose key state changes come from backend/database-backed truth
- P2-C1-S2: capture one deployed admin flow whose key state changes come from backend/database-backed truth and retain the artifact paths/results here

### P2 Deployed Drill Decision (v1)

- `P2` now fixes one bounded deployed evidence path on the already-hardened stable-runner release substrate instead of inventing a separate drill harness:
  - reuse `s4d-cloud-release-dispatch-stable-runner.yml` plus `scripts/ops/cloud_release_workflow.sh --access-verify-overlay` as the operator path;
  - tighten `scripts/ops/cloud_release_access_verify.sh` so the deployed member/admin probes no longer rely on JWTs minted inside the container, but instead use the same explicit dev actor ids that `P1` bridged into backend auth fallback;
  - retain the resulting `summary.json`, `verify.log`, and `access_verify_result.json` as the first cloud-target proof that actor identity and standing are accepted per request from backend/database-backed truth.

### P3 (Close-out / next-lane decision)

- P3-C1-S1: record what realism gap remains transitional after this packet and whether another bounded child packet is required

### P3 Remaining Gap Decision (v1)

- `P3-C1-S1` now fixes the remaining realism gap as a bounded decision rather than another generic “keep hardening” placeholder:
  - this packet has already reached the first `road-002-01/M2` credibility threshold required for the deployed access/subscription slice, because one cloud-target member flow and one cloud-target admin flow now read standing through backend-validated identity plus persistence-backed membership truth;
  - the deployed slice is still explicitly transitional in one narrow sense: browser-local shared auth session materialization and local-first admission-code UX remain on the identity-entry path (`frontend/src/shared/auth/AuthContext.tsx`, `frontend/src/app/onboarding/admission/page.tsx`), even though they are no longer the final authority for the retained passing drills;
  - provider integration and broader auth-platform realism remain deferred by branch-road rule, not by accident, and therefore should not be reopened inside this packet;
  - asset/object handling has not yet opened a cloud-backed packet, so the next meaningful branch-road work is no longer another access-truth drill but the first `M3/P0` contract that states the cloud boundary for blob/object handling versus relational metadata truth.
- The `P3` decision in this packet is therefore:
  - do **not** open another `M2` child packet immediately from `S4F-2C`;
  - treat the current access/subscription slice as the first credible deployed truth proof, while still describing the auth-entry layer as transitional;
  - route the next execution lane to `road-002-01/M3-P0`: define the first cloud-backed asset-platform entry contract.

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: credibility boundary fixed
- [x] `P0-C1-S2`: chosen truth-model boundary fixed
- [x] `P0-C1-S3`: realism evidence contract fixed

### P1 (Implementation)

- [x] `P1-C1-S1`: one bounded deployed authority shift chosen and recorded
- [x] `P1-C1-S2`: minimal backend/database-backed truth changes landed

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: deployed member flow retained against backend/database-backed truth
- [x] `P2-C1-S2`: deployed admin flow retained against backend/database-backed truth

### P3 (Close-out / next-lane decision)

- [x] `P3-C1-S1`: remaining transitional realism gap recorded explicitly

## Current Status (recommended)

- `S4F-2C/P0-P3` is now complete and this child log can close as `stable`.
- The deployable runtime path is already proven and the release-path dependency trust is already hardened enough to stop treating RDS ingress drift as the controlling blocker.
- `P0` is now fixed: the first controlling credibility gap is no longer generic “demo-ness” but the specific fact that the currently deployed actor identity, admission standing, and role truth still originate in frontend-local session/admission machinery while the backend auth actor remains intentionally minimal.
- The first bounded truth shift is also now fixed: `S4F-2C` should tighten backend-validated identity plus persistence-backed admission/membership truth first, while leaving local actor switching explicitly outside the authority path for the eventual passing drills.
- `P1` is now fixed: dev/demo requests no longer need to collapse to one shared backend fallback actor before membership resolution, because the frontend can bridge one stable actor identity per session into the backend auth-context seam.
- `P2` is now fixed: one stable-runner cloud-target run retained both a member and an admin drill through the new request-level dev identity bridge, and the retained overlay evidence now records the backend/database truth sources explicitly.
- `P3` is now fixed: the first credible deployed truth threshold for the access/subscription slice is satisfied, the remaining auth-entry layer is explicitly marked transitional, and this packet does not justify another immediate `M2` child.
- The next step is no longer another access-truth drill; it is `road-002-01/M3-P0`, i.e. the first cloud-backed asset-platform readiness contract.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, truth model, and retained artifact paths or run URLs.
- At scaffold time, the seed evidence is the conclusion retained by `S4F-2B`, which closed the release-path dependency trust gap and exposed credibility as the next controlling boundary.

### P0-C1-S1 (Seed credibility boundary from prior lane | 2026-04-20)

- headSha: `c2bc2c74f`
- artifacts:
  - `artifacts/_tmp_s4f2b_run_24664326210/s4d-cloud-release-stable-runner-24664326210-1/summary.json`
  - `docs/logs/log-S4F-2B-release-path-dependency-trust-hardening.md`
- expected:
  - `S4F-2B` should finish with one explicit next-lane decision if deployability and dependency trust are no longer the primary blockers.
- observed:
  - `S4F-2B/P2` retained one real stable-runner cloud-target evidence run with `deploy=PASS`, `verify=PASS`, `accessVerifyResult=PASS`, and `result=PASS`.
  - The remaining gap is no longer release-path realism around RDS trust; it is whether the deployed member/admin flows are authoritative enough to count as credible backend/database-backed truth rather than local-first scaffolding.

### P0-C1-S1S2S3 (Credibility boundary, chosen truth model, and realism evidence contract fixed | 2026-04-20)

- headSha: `c2bc2c74f`
- artifacts:
  - `docs/logs/log-S4F-2C-deployed-identity-admission-membership-truth-hardening.md`
  - `frontend/src/shared/auth/AuthContext.tsx`
  - `frontend/src/shared/layouts/LocalActorSwitcher.tsx`
  - `frontend/src/app/onboarding/admission/page.tsx`
  - `backend/api/app/shared/auth_context.py`
  - `backend/api/app/shared/actor.py`
  - `backend/api/app/config/security.py`
- expected:
  - `S4F-2C/P0` should name one narrow credibility boundary that can be tightened without reopening deployability or release-path trust.
  - The chosen truth model should explain exactly which current surfaces remain local-first and which backend seam should become authoritative next.
- observed:
  - The narrowest controlling credibility boundary is the current actor/admission/membership authority path, not runtime packaging or cloud connectivity.
  - The deployed frontend still owns too much truth today: `AuthContext` materializes session and admitted standing from browser storage, onboarding admission resolves from local-first code lookup, and `LocalActorSwitcher` can rewrite standing through explicit `dev-bypass`.
  - The backend seam for the next tightening step is already visible but intentionally thin: request actor/auth context is minimal and does not yet authoritatively resolve tenant membership/standing from persistence-backed truth.
  - `P0` now fixes the first truth shift as `backend-validated identity + persistence-backed admission/membership truth`, while lifecycle/entitlement semantics can continue to reuse the already-stable backend subscription/access surface.

### P1-C1-S1S2 (Stable dev actor identity bridge landed | 2026-04-20)

- headSha: `WORKTREE`
- artifacts:
  - `frontend/src/shared/auth/AuthContext.tsx`
  - `frontend/src/shared/api/client.ts`
  - `backend/api/app/config/security.py`
  - `backend/api/app/tests/test_security/test_auth_context_dev_identity_bridge.py`
- expected:
  - a dev/demo browser session should be able to identify one concrete actor to the backend without requiring a real JWT issuer yet;
  - backend roles for that request should resolve from persistence-backed membership truth for that actor rather than from one shared `DEV_USER_ID` fallback.
- observed:
  - frontend auth sessions now retain a stable `userId`, with fixed actor ids for the known demo users used by the local actor switcher and admission drills;
  - the API client now sends `X-Dev-User-Id` on dev-session requests when no bearer token is available;
  - backend auth fallback now reads that explicit actor id before membership lookup, so tenant standing can resolve per actor from `library_memberships` (or the existing owner fallback);
  - focused validation passed for the new seam in `backend/api/app/tests/test_security/test_auth_context_dev_identity_bridge.py`.

### P2-C1-S1S2 (Deployed member/admin truth drills retained on stable runner | 2026-04-20)

- headSha: `f4e94ad1f`
- run:
  - `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/24668611462`
- artifacts:
  - `artifacts/_tmp_s4f2c_p2_run_24668611462/s4d-cloud-release-stable-runner-24668611462-1/summary.json`
  - `artifacts/_tmp_s4f2c_p2_run_24668611462/s4d-cloud-release-stable-runner-24668611462-1/verify.log`
  - `artifacts/_tmp_s4f2c_p2_run_24668611462/s4d-cloud-release-stable-runner-24668611462-1/access_verify_result.json`
- expected:
  - the passing deployed member flow should read `access-context/me` as the fixed member actor through the new request-level dev identity bridge, and should fail admin subscription access with `not_admin`;
  - the passing deployed admin flow should read admin subscription state, list tenant memberships, mutate lifecycle state, and re-read the updated state through the same backend/database-backed truth path.
- observed:
  - stable-runner release run `24668611462` completed with `deploy=PASS`, `verify=PASS`, `accessVerifyResult=PASS`, and `result=PASS`;
  - the retained `s4f-2c.access-verify.v1` payload fixes `identityTruthSource=backend-validated.dev-header`, `admissionTruthSource=persistence-backed.library_memberships`, `membershipTruthSource=persistence-backed.library_memberships`, and `lifecycleTruthSource=backend.subscription_access`;
  - the member drill passed with `memberReadStatus=200`, `memberRoles=["member"]`, and `memberAdminDenyStatus=403` / `memberAdminDenyReason="not_admin"` for the fixed demo member actor `11111111-1111-4111-8111-111111111111`;
  - the admin drill passed with `adminReadStatus=200`, `adminMembershipsStatus=200`, and `adminMembershipRoles` showing the retained member/admin rows for the fixed demo actors, plus `lifecycleMutationStatus=200` and `rerenderedStateStatus=200` after the upgrade event.

### P2-C1-S1S2 (Retry note | 2026-04-20)

- first retry run `24668271445` failed before access verify due one local startup regression introduced while wiring request-aware dev fallback: FastAPI rejected `get_current_user_id(request: Optional[Request] = None)` as a dependency field type on router startup.
- the fix was to keep `get_current_user_id()` signature startup-safe for existing `Depends(get_current_user_id)` call sites and move request-aware header fallback into a separate helper consumed only by `get_auth_context()`.
- focused validation then passed locally across:
  - `api/app/tests/test_security/test_auth_context_dev_identity_bridge.py`
  - `api/app/tests/test_subscription_access/test_router.py`
  - `api/app/tests/test_library_router/test_membership_router.py`

### P3-C1-S1 (Remaining transitional realism gap fixed | 2026-04-20)

- headSha: `eb76bb256`
- artifacts:
  - `docs/logs/log-S4F-2C-deployed-identity-admission-membership-truth-hardening.md`
  - `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
  - `frontend/src/shared/auth/AuthContext.tsx`
  - `frontend/src/app/onboarding/admission/page.tsx`
- expected:
  - `P3` should decide whether the remaining realism gap is large enough to require another bounded `M2` child packet, or whether the branch road should advance to the next milestone.
- observed:
  - the first deployed credibility threshold named by `road-002-01` is now satisfied for access/membership/lifecycle truth, because the retained member/admin drills no longer depend on browser-local standing as final authority;
  - the remaining transitional gap is narrower than a full second `M2` packet: identity entry and admission UX still start from browser-local/shared-auth scaffolding, but that scaffolding is now outside the final authority path for the passing deployed drills;
  - provider realism remains intentionally deferred by the branch-road AWS v1 cut rule;
  - the next meaningful execution lane is therefore `M3/P0` cloud-backed asset-platform readiness contract work, not another immediate `S4F-2C` follow-up drill packet.

## Recent changes (for traceability, optional)

- 2026-04-20: opened `S4F-2C` as the next child lane after `S4F-2B`, shifting the `S4F` family focus from deployability/trust hardening to deployed identity/admission/membership truth hardening under `road-002-01/M2`.
- 2026-04-20: completed `S4F-2C/P0-C1-S1S2S3` by fixing the first deployed credibility boundary on the current cloud slice, choosing backend-validated identity plus persistence-backed admission/membership truth as the next authority shift, and tightening the realism evidence contract around explicit truth sources.
- 2026-04-20: completed `S4F-2C/P1-C1-S1S2` by bridging stable dev actor identity from frontend session state into backend auth-context fallback so membership-backed tenant standing can resolve per actor instead of per process.
- 2026-04-20: completed `S4F-2C/P2-C1-S1S2` by rerouting the stable-runner access overlay through the new request-level dev identity bridge and retaining one full PASS cloud-target member/admin drill bundle in run `24668611462`.
- 2026-04-20: completed `S4F-2C/P3-C1-S1`, deciding that the first `M2` credible-threshold proof is sufficient and the next execution lane should move to `M3/P0` cloud-backed asset-platform readiness contract work rather than another immediate `M2` child.