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

**Default choices (phase defaults / v1)**:

- Keep the release entry on the existing `S4D` substrate unless this lane proves that one narrow trust relocation is required.
- Treat the current problem as a dependency/trust issue, not as a feature or API-semantic issue: the backend access/subscription slice is already evidenced by `S4F-2A`.
- Prefer one durable trust position such as a stable VPC-positioned runner, SG-to-SG trust, or another fixed network identity over any workflow that keeps re-authorizing operator public `/32`s.
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

### P0-C1-S2 (Candidate trust-model boundary | v1)

- Candidate directions for this packet are intentionally narrow:
  - stable VPC-positioned runner executing the existing release/verify path
  - SG-to-SG trust from a fixed compute identity already inside the trusted network position
  - another fixed network identity with equivalent durability and reviewable blast radius
- `S4F-2B` should compare candidates only enough to pick one concrete path for implementation and evidence; it should not turn into a broad cloud-network redesign study.

### P0-C1-S3 (Evidence contract | v1)

- Evidence for this lane must include at least:
  - `headSha`
  - `workflowCommandSummary`
  - `targetHostKind`
  - `trustModel`
  - `rdsTrustPathKind`
  - `deployResult`
  - `verifyResult`
  - `operatorIpAllowlistMutationRequired`
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

- P1-C1-S1: choose one durable trust model and record the exact release/dependency contract delta from `S4F-2A`
- P1-C1-S2: land the minimal runner/network/security-group wiring needed for that chosen trust model

### P2 (Drill / Verify)

- P2-C1-S1: capture one real cloud-target operator evidence run on the hardened trust path without fresh operator `/32` maintenance
- P2-C1-S2: record the resulting artifact path, trust-model details, and dependency results in this log

### P3 (Close-out / export decision)

- P3-C1-S1: answer the outlet decisions and record whether the durable trust rule should leave this log as contract/runbook text

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: dependency boundary fixed
- [ ] `P0-C1-S2`: candidate trust-model boundary fixed
- [ ] `P0-C1-S3`: hardened dependency evidence contract fixed

### P1 (Implementation / infra wiring)

- [ ] `P1-C1-S1`: one durable trust model chosen and recorded
- [ ] `P1-C1-S2`: minimal trust-path wiring landed

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: hardened cloud-target evidence run captured without fresh operator `/32` maintenance
- [ ] `P2-C1-S2`: artifact path and trust-model results recorded

### P3 (Close-out / export decision)

- [ ] `P3-C1-S1`: outlet decisions recorded explicitly

## Current Status (recommended)

- `S4F-2B` is newly opened as the follow-up lane to `S4F-2A/P3`.
- The problem is already well enough bounded to start: the backend release path is proven, and the remaining fragility is the dependency trust model around RDS ingress and operator network identity.
- The next step is not more runtime proof on the old path; it is a bounded `P0` decision on which durable trust model this lane will implement first.

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

## Recent changes (for traceability, optional)

- 2026-04-20: opened `S4F-2B` as the direct follow-up lane to `S4F-2A/P3`, dedicated to removing operator public `/32` RDS allowlist dependence from the reused `S4D` release path.