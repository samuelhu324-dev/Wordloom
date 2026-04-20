# log-S4F-2B (Phase 2: Release-path dependency trust hardening)

---

**id**: `S4F-2B`
**kind**: `log`
**title**: `release-path dependency trust hardening (remove operator public /32 RDS allowlist dependence) v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, NetworkTrust, ReleaseOperations, Drills, Evidence, epic/s4, sub/2b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **roadmap**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
  **parent_log**: `docs/logs/log-S4F-access-subscription-deployable-runtime-cut.md`
  **previous_log**: `docs/logs/log-S4F-2A-cloud-target-operator-evidence-packet.md`
  **reference_log_1**: `docs/logs/log-S4F-2A-cloud-target-operator-evidence-packet.md`
  **reference_log_2**: `docs/logs/log-S4D-4C-408-timeout-eradication.md`
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

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this dependency-hardening packet.
- Day-level precision is acceptable while the lane is being opened and scoped.
- `reviewed` should remain `pending` until one explicit trust-model decision and one real hardened operator-path evidence sample are retained.

## Decision / Outcome

**Decision**:

- `S4F-2B` opens the realism-hardening follow-up lane identified by `S4F-2A/P3`: remove dependence on drifting operator public `/32` RDS ingress for the reused `S4D` release path.
- The packet's job is not to prove access behavior again; it is to harden the dependency/trust shape under that already-proven path so release and verify no longer rely on per-operator egress-IP allowlist maintenance.
- `S4F-2B/P0` fixes the default target trust model up front: prefer a stable trusted runner position as the release origin and a durable RDS trust path bound to that fixed identity, rather than keeping the operator workstation as the routine dependency origin.

**Default choices (phase defaults / v1)**:

- Keep the release entry on the existing `S4D` substrate unless this lane proves that one narrow trust relocation is required.
- Treat the current problem as a dependency/trust issue, not as a feature or API-semantic issue: the backend access/subscription slice is already evidenced by `S4F-2A`.
- The default implementation target for this lane is: GitHub Actions stable self-hosted runner in a stable trusted network position, with the RDS trust path attached to that fixed runner/compute identity rather than to a drifting operator public `/32`.
- SG-to-SG trust, or another equivalently durable fixed-identity trust rule, is the preferred RDS-side realization of that target; operator public `/32` ingress is demoted to break-glass/debug-only status.
- Do not widen this packet into production HA, frontend hosting, or general infra modernization.
- draft 阶段默认继续把 source log 当作集中面；如果问题边界、规则、过程、reader summary 或 front-door 影响仍在变化，不要过早把 weak-structure 内容拆到多个 outlets。
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S4F-2B` is expected to drive the dependency-hardening PR once the target trust model is fixed.

**PR summary bullets**:

- Replace the fragile operator public-IP allowlist dependency under the reused `S4D` cloud release path with one durable trust model.
- Keep `S4F` on the same backend/runtime family while tightening the network and dependency boundary proven to be brittle in `S4F-2A`.
- Capture one hardened cloud-target evidence run showing that release/verify no longer depends on ad hoc operator `/32` maintenance.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S4F-2B-release-path-dependency-trust-hardening.md`
- Runbook: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
- Evidence artifact: ``

**Implementation anchor(s)**:

- `infra/terraform/aws/runner-host/main.tf`
- `infra/terraform/aws/runner-host/terraform.tfvars`
- `docs/runbook/run-S4D-cloud-stable-runner-cutover.md`
- `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml`

**Evidence Footer Source**:

- `P2-C1-S1` | artifact: ``

## Exported Sections / Outlet Ownership

- `S4F-2B` is opening as a new active source log. Outlet ownership is stated now, but export should wait until the trust model is actually chosen and exercised.

**Outlet ownership**:

- `contract`: likely candidate after the lane stabilizes; the durable trust rule for cloud release/RDS dependency wiring may need to leave this log.
- `runbook`: likely candidate after the lane stabilizes; if the hardened operator path changes the required release steps, update or extract the stable procedure.
- `view`: no-op for now; reader-facing family summary can remain in the parent `S4F` spine until the new lane settles.
- `index/front-door`: no-op for now; no new front-door navigation is justified at scaffold time.
- `disposition/placement`: no-op for now; this is an active runtime lane, not support-only standing.
- `log-retained core`: keep the decision, active trust-model options, checklist, current status, and evidence ledger here.

## Definitions (optional)

- `operator public /32 dependence`: any release/verify path that succeeds only when the operator's current public egress IP is manually present in the RDS ingress allowlist.
- `durable trust model`: a release/dependency shape that continues to work without operator-by-operator public-IP maintenance.
- `stable trusted network position`: a runner or network identity whose access to RDS can be trusted through a fixed SG-to-SG or equivalent durable rule.

## Constraints

- Do not reopen feature-level access verification as the primary question; `S4F-2A` already proved that behavior.
- Do not change more of the `S4D` release workflow than needed to eliminate the operator-IP dependency.
- Do not leave the outcome at prose-only recommendation; the lane must end with one explicit target trust shape plus evidence.
- Do not accept another solution that still depends on recurring manual `/32` edits as the default operating mode.
- Reuse the already-landed `S4D-4C` stable-runner host/module and cutover assets unless a concrete defect proves they are insufficient for `S4F-2B`.

## Scope

- `P0`: contract (dependency boundary, candidate trust models, success/evidence contract)
- `P1`: implementation / infra wiring (apply one chosen durable trust path with minimal release-path drift)
- `P2`: drill / verify (capture one real operator-facing cloud-target run on the hardened trust path)
- `P3`: close-out / export decision (decide what leaves the log as contract/runbook and what remains retained core)

## Success Criteria (DoD)

- The lane names one explicit dependency/trust boundary that was brittle in `S4F-2A`.
- One chosen trust model is fixed clearly enough that operators can say why it is more durable than public `/32` allowlists.
- The hardened path still reuses the `S4D` release family unless a narrow, justified contract change is recorded.
- At least one real retained run proves release and verify can reach required dependencies without adding a fresh operator public `/32` to RDS ingress.
- The retained evidence names the trust position used by the successful run.
- The log leaves one explicit close-out decision on whether the new trust rule belongs in contract, runbook, both, or log-retained core only.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the dependency/trust contract is explicit;
  - one hardened trust path is implemented or otherwise fixed as the default decision;
  - one real evidence sample proves the path without fresh operator-IP allowlist maintenance;
  - the outlet decisions for `contract / runbook / view / index/front-door / disposition/placement / log-retained core` are answered explicitly.

## P0 (Contract | v1)

### P0-C1-S1 (Dependency boundary | v1)

- `S4F-2B` treats the RDS trust path as part of the release dependency contract, not as incidental operator setup.
- The brittle boundary to remove is: successful release depends on the current operator machine's public `/32` being manually present in the cloud-dev DB security group.

### P0-C1-S2 (Chosen trust-model boundary | v1)

- `S4F-2B` chooses one default trust model instead of keeping multiple equal candidates open:
  - release/verify should originate from the existing stable self-hosted cloud runner path, not from the operator workstation as the routine dependency origin;
  - the RDS trust path should be bound to that stable runner or another fixed in-network compute identity through SG-to-SG trust or an equivalently durable fixed-identity rule;
  - operator public `/32` allowlist edits are no longer part of the normal operating contract for cloud-dev release evidence.
- This keeps `S4F-2B` narrow: the lane is not redesigning all cloud networking, only moving the release dependency trust anchor from drifting operator egress to one stable reviewed identity.

### P0-C1-S3 (Evidence contract | v1)

- Evidence for this lane must include at least:
  - `headSha`
  - `workflowCommandSummary`
  - `releaseOriginKind`
  - `targetHostKind`
  - `trustModel`
  - `rdsTrustPathKind`
  - `deployResult`
  - `verifyResult`
  - `operatorIpAllowlistMutationRequired`
  - `operatorIpAllowlistMutationKind`
  - `result`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4F-2B/P<phase>-C<cycle>-S<steps>: <summary>`

**Branch convention**:

- `S4F-2B` related implementation and documentation should continue on `S4F-access-subscription-deployable-runtime-cut` unless the dependency-hardening work later justifies a narrower focused branch.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit, whether it is contract work, implementation, or drills/evidence, commit/push promptly on the current `S4F` working branch.

## Plan (draft)

### P1 (Implementation / infra wiring)

- P1-C1-S1: map the current stable cloud runner path to one concrete durable RDS trust anchor and record the exact contract delta from `S4F-2A`
- P1-C1-S2: land the minimal runner/network/security-group wiring needed to make operator `/32` maintenance non-routine

### P2 (Drill / Verify)

- P2-C1-S1: capture one real cloud-target operator evidence run on the hardened trust path without fresh operator `/32` maintenance
- P2-C1-S2: record the resulting artifact path, trust-model details, and dependency results in this log

### P3 (Close-out / export decision)

- P3-C1-S1: answer the outlet decisions and record whether the durable trust rule should leave this log as contract/runbook text

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: dependency boundary fixed
- [x] `P0-C1-S2`: chosen trust-model boundary fixed
- [x] `P0-C1-S3`: hardened dependency evidence contract fixed

### P1 (Implementation / infra wiring)

- [x] `P1-C1-S1`: one durable trust model chosen and recorded
- [x] `P1-C1-S2`: minimal trust-path wiring landed

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: hardened cloud-target evidence run captured without fresh operator `/32` maintenance
- [x] `P2-C1-S2`: artifact path and trust-model results recorded

### P3 (Close-out / export decision)

- [ ] `P3-C1-S1`: outlet decisions recorded explicitly

## Current Status (recommended)

- `S4F-2B` is newly opened as the follow-up lane to `S4F-2A/P3`.
- The problem is already well enough bounded to start: the backend release path is proven, and the remaining fragility is the dependency trust model around RDS ingress and operator network identity.
- `P0` is now fixed: the lane will treat the stable self-hosted cloud runner path as the default release origin and will move RDS trust to one durable fixed-identity path instead of recurring operator public `/32` edits.
- `P1` is now also fixed at the implementation-anchor level: the trust anchor is the existing stable runner host module plus the cloud-dev basic security group (`sg-027e05455509e0730`, `wlv3-cloud-dev-sg-basic`), which the cloud-dev DB security group (`sg-0873e947b9947639d`, `wlv3-cloud-dev-sg-db`) can trust without per-operator public-IP churn.
- The repo-side implementation surface is already present and aligned: `infra/terraform/aws/runner-host/` provisions the host, `scripts/ops/cloud_stable_runner_bootstrap.sh` and `scripts/ops/cloud_stable_runner_probe.sh` bootstrap/probe it, and `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml` is the corresponding release entry.
- `P2` is now fixed with one real retained run: workflow run `24664326210` completed `PASS` on the stable Linux runner path, and the retained `summary.json` shows all release, verify, and access-aware gates green.
- The evidence now supports the lane claim that the release path itself no longer needed a fresh operator public `/32` in the RDS allowlist; the durable dependency trust anchor was the stable runner host attached to `wlv3-cloud-dev-sg-basic` reaching `wlv3-cloud-dev-sg-db` by fixed identity.
- One bootstrap caveat remains explicit: the operator did add the current public `/32` to the runner SSH security group so the reverse tunnel to the local-only target could be established, but that mutation was outside the RDS trust path and therefore does not reopen the `S4F-2B` dependency boundary that this lane was created to remove.
- The next step is `P3`: answer outlet/export placement now that the trust rule and one real hardened sample are both retained.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, trust model, and retained artifact paths or run URLs.
- At scaffold time, the seed evidence is the conclusion retained by `S4F-2A`, which identified the brittle dependency boundary.

### P0-C1-S1 (Seed dependency failure boundary from prior lane | 2026-04-20)

- headSha: `129fb1729`
- artifacts: `artifacts/_tmp_s4d4b_cloud_release_dispatch/24662387235-1/summary.json`
- expected:
  - `S4F-2A` should finish with one explicit next-lane decision if the remaining blocker is dependency/trust realism rather than feature behavior.
- observed:
  - `S4F-2A/P3` concluded that `road-002-01/M1` has sufficient backend deployment-facing evidence.
  - The remaining hardening gap is recurring operator public `/32` maintenance for RDS ingress, which should move to a separate follow-up lane instead of being left as the default operating model.

### P0-C1-S1S2S3 (Dependency boundary, chosen trust model, and evidence contract fixed | 2026-04-20)

- headSha: `af365da90`
- artifacts:
  - `docs/logs/log-S4F-2B-release-path-dependency-trust-hardening.md`
  - `docs/logs/log-S4D-4C-408-timeout-eradication.md`
  - `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml`
- expected:
  - `S4F-2B/P0` should convert the follow-up recommendation from `S4F-2A/P3` into one explicit default trust model rather than leaving multiple equal candidates open.
  - The chosen model should align with already-recorded `S4D` stable-runner governance instead of inventing a second unrelated release origin.
- observed:
  - `S4F-2B/P0` now fixes the brittle dependency boundary as operator public `/32` dependence for RDS ingress.
  - The chosen default trust model is the stable self-hosted cloud runner path plus one durable fixed-identity RDS trust path, with operator public `/32` ingress demoted to break-glass/debug-only status.
  - The evidence contract now requires explicit recording of release origin and whether any operator-IP allowlist mutation was still required.

### P1-C1-S1S2 (Stable-runner trust anchor mapped to concrete cloud-dev wiring | 2026-04-20)

- headSha: `960c10e9c`
- artifacts:
  - `infra/terraform/aws/runner-host/main.tf`
  - `infra/terraform/aws/runner-host/terraform.tfvars`
  - `docs/runbook/run-S4D-cloud-stable-runner-cutover.md`
  - `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml`
- expected:
  - `S4F-2B/P1` should identify one concrete trust anchor already present in the repo or explicitly prove that a new one must be created.
  - The chosen implementation anchor should show how `S4F-2A`'s operator-origin dependency changes under the hardened path.
- observed:
  - `infra/terraform/aws/runner-host/main.tf` explicitly requires attaching the runner host to the cloud-dev basic security group so the DB SG can trust the host by SG instead of public IP.
  - The committed `infra/terraform/aws/runner-host/terraform.tfvars` currently attaches `sg-027e05455509e0730`, and AWS readback confirms this is `wlv3-cloud-dev-sg-basic`.
  - AWS readback also confirms the cloud-dev DB SG is `sg-0873e947b9947639d` / `wlv3-cloud-dev-sg-db`, so the trust anchor is now recorded as `stable-runner host attached to cloud-dev basic SG -> DB SG trust path`.
  - The exact contract delta from `S4F-2A` is: operator workstation and temporary Windows runner are no longer the routine dependency origin for RDS reachability; they remain only as bootstrap/debug or bridge surfaces while the preferred release origin becomes the stable Linux runner path.

### P2-C1-S1S2 (Stable-runner hardened cloud-target evidence run retained | 2026-04-20)

- headSha: `5f68f8a9c68fdcfa9f31eb2ba36266db96454bce`
- runUrl: `https://github.com/samuelhu324-dev/wordloom-v3/actions/runs/24664326210`
- artifacts:
  - `artifacts/_tmp_s4f2b_run_24664326210/s4d-cloud-release-stable-runner-24664326210-1/summary.json`
  - `artifacts/_tmp_s4f2b_run_24664326210/s4d-cloud-release-stable-runner-24664326210-1/preflight.log`
  - `artifacts/_tmp_s4f2b_run_24664326210/s4d-cloud-release-stable-runner-24664326210-1/deploy.log`
  - `artifacts/_tmp_s4f2b_run_24664326210/s4d-cloud-release-stable-runner-24664326210-1/verify.log`
  - `artifacts/_tmp_s4f2b_run_24664326210/s4d-cloud-release-stable-runner-24664326210-1/access_verify_result.json`
- expected:
  - `S4F-2B/P2` should retain one real run proving the hardened release path can complete deploy, generic verify, and the `S4F` access overlay without adding a fresh operator public `/32` to RDS ingress.
  - The retained evidence should identify the release origin, trust path kind, and whether any operator-IP mutation was still required.
- observed:
  - Workflow run `24664326210` on `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml` completed `success`; `Run cloud release workflow` itself also completed `success`.
  - The retained `summary.json` reports `preflightResult=PASS`, `deployResult=PASS`, `verifyResult=PASS`, `accessVerifyResult=PASS`, `result=PASS`, and all relevant gates green through `accessAwareVerifyGate=PASS`.
  - `workflowCommandSummary` shows the release origin as the stable Linux self-hosted runner path driving `cloud_release_workflow.sh` against `ssh_host=127.0.0.1`, `ssh_port=22022`, `ssh_user=wordloom`, with the target still being the local-only cloud VM reached through the reverse tunnel.
  - The dependency trust model exercised by the passing run is `stable self-hosted Linux runner attached to wlv3-cloud-dev-sg-basic -> SG-based reachability to wlv3-cloud-dev-sg-db`; no fresh operator public `/32` was added to the RDS allowlist for this run.
  - `releaseOriginKind=stable_self_hosted_linux_runner`, `targetHostKind=local_only_cloud_target_via_reverse_tunnel`, `trustModel=stable_runner_fixed_identity_plus_sg_bound_rds_trust`, `rdsTrustPathKind=sg_to_sg_via_wlv3_cloud_dev_sg_basic_to_wlv3_cloud_dev_sg_db`, `operatorIpAllowlistMutationRequired=false`, `operatorIpAllowlistMutationKind=none_for_rds_allowlist`.
  - A separate bootstrap detail remains relevant but out of scope for the brittle boundary removed by this lane: the operator temporarily added `49.196.191.226/32` to the runner SSH security group so the reverse tunnel to the local-only target could be established. That was a runner-SSH ingress bootstrap action, not an RDS allowlist mutation.

## Recent changes (for traceability, optional)

- 2026-04-20: opened `S4F-2B` as the direct follow-up lane to `S4F-2A/P3`, dedicated to removing operator public `/32` RDS allowlist dependence from the reused `S4D` release path.
- 2026-04-20: completed `P0-C1-S1S2S3` by fixing the dependency boundary, choosing the stable-runner-based trust model as the default lane target, and tightening the evidence contract around release origin and allowlist-mutation requirements.
- 2026-04-20: completed `P1-C1-S1S2` by mapping `S4F-2B` onto the already-landed `S4D-4C` stable-runner assets, confirming the concrete trust anchor (`wlv3-cloud-dev-sg-basic` -> `wlv3-cloud-dev-sg-db`), and recording the exact release-origin delta from `S4F-2A`.
- 2026-04-20: completed `P2-C1-S1S2` with stable-runner workflow run `24664326210`, retaining one real passing cloud-target evidence sample that no longer required a fresh operator public `/32` in the RDS allowlist.