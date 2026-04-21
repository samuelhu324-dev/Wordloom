# log-S4F (Access / Subscription Deployable Runtime Cut)

---

**id**: `S4F`
**kind**: `log`
**title**: `access / subscription deployable runtime cut v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, AccessControl, ReleaseOperations, epic/s4, epic/s4f`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **roadmap**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
  **reference_log_1**: `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  **reference_log_2**: `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
  **phase_log_1**: `docs/logs/log-S4F-1A-backend-only-access-subscription-deployable-cut.md`
  **phase_log_2**: `docs/logs/log-S4F-2A-cloud-target-operator-evidence-packet.md`
  **phase_log_3**: `docs/logs/log-S4F-2B-release-path-dependency-trust-hardening.md`
  **phase_log_4**: `docs/logs/log-S4F-2C-deployed-identity-admission-membership-truth-hardening.md`
  **phase_log_5**: ``
  **phase_log_6**: ``
**issue_keyword**: `platform`
**issue_top_labels**: ``
**issue_scope_labels**: ``
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
**roadmap_milestone**: `M1`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-20`
**updated**: `2026-04-20`

---

## Decision / Outcome（结论区）

**Decision**:

- Open `S4F` as the new `S4` top-level spine for the first `road-002-01` deployable runtime cut that reuses the proven `S4D` cloud release path instead of inventing a second release family.
- Treat `S4F` as the runtime-execution owner for the branch-road's first cloud closure: backend-first access/subscription deployment, access-aware verify gates, and bounded member/admin drills.

**Default choices（默认基线 / v1）**:

- Reuse the stable `S4D` single-VM, backend-container, external-RDS release workflow as the default release substrate.
- Keep the first `S4F` lane backend-only; do not require frontend cloud closure before the first deployable-cut proof exists.
- Replace generic backend smoke as the success center with access-aware verify and drill contracts that match the recent auth/access/subscription slice.
- Keep provider realism, UI cloud hosting, worker cloud residency, and asset-platform work out of the first `S4F` packet.
- 若 `issue_*` 字段为空，automation 必须保守留空并要求人工确认，而不是猜测 title keyword、labels 或 milestone。
- 若 `pr_*` 字段为空，PR automation 必须保守留空并显式报告缺口，而不是复制 issue metadata 或猜测 base / milestone / development issue。
- roadmap 与 logs 的机械桥接必须通过 `roadmap_path + roadmap_milestone + roadmap_phase` 明确声明；roadmap 内的正式 bridge ledger 默认只计入 child logs，而不是 parent/spine prose。

## PR Summary Inputs（可选）

- This parent/spine is intended to define one bounded runtime execution family under `road-002-01`; the concrete review packet should come from `S4F-1A`.

**PR summary bullets**:

- Open one new `S4` spine for the first backend-first access/subscription deployable runtime cut under `road-002-01`.
- Reuse the stable `S4D` operator workflow and evidence contract instead of creating a second cloud release path.
- Route the first actual deployable packet into `S4F-1A`, where access-aware verify and member/admin drills are fixed explicitly.

**PR checklist source**:

- Default source: reuse the concrete execution checklist from `docs/logs/log-S4F-1A-backend-only-access-subscription-deployable-cut.md`.

**PR links**:

- Parent log: `docs/logs/log-S4F-access-subscription-deployable-runtime-cut.md`
- Child log source(s): `docs/logs/log-S4F-1A-backend-only-access-subscription-deployable-cut.md` ; `docs/logs/log-S4F-2A-cloud-target-operator-evidence-packet.md`
- Evidence artifact: `artifacts/_tmp_s4f1a_p2_run_24652525475/labs-evidence-verify_access_subscription_deployable_cut-24652525475-1-verify_access_subscription_deployable_cut/summary.json`

## Background（背景）

- `road-002-01` already fixed the first branch-road goal: one deployable AWS-oriented runtime cut for the stable access/auth/subscription slice.
- The repository already has one proven cloud release substrate in `S4D`: single VM, backend container, external cloud-dev RDS, single-entry operator workflow, failure taxonomy, and machine-readable evidence.
- The missing piece is no longer generic release plumbing; it is a feature-scoped runtime family that reuses that plumbing for the recent access/subscription slice and replaces generic smoke with access-aware verification.

## Constraints（约束）

- Do not reopen `S4D` as if the cloud release path itself were still undefined.
- Do not widen the first lane into frontend cloud hosting, worker runtime, or asset-platform readiness.
- Do not treat local-first access/subscription semantics as sufficient proof once the slice is deployed; `S4F` must define explicit deployed verification and drills.
- Do not introduce a second competing release workflow when the current `S4D` workflow is already stable and reusable.

## Scope（本 log 范围）

- 本 log 负责：
  - define `S4F` as the top-level `S4` spine for the first access/subscription deployable runtime cut;
  - fix the default reuse rule from `S4D` into `road-002-01/M1`;
  - route the first concrete execution packet to `S4F-1A`.
- 本 log 不负责：
  - detailed endpoint lists, drill steps, or evidence blocks for the first packet;
  - frontend cloud closure or asset-platform design.

## Success Criteria（DoD）

- 结构层面：
  - readers can see in one place why `S4F` exists and why it is distinct from `S4D` and `S4E`;
  - `S4F-1A` is explicitly named as the first runtime packet under this spine.
- 工程层面：
  - the default release substrate is explicitly the stable `S4D` operator workflow;
  - the first packet is explicitly backend-only and access-aware.
- 证据层面：
  - later `S4F-*` evidence can reuse `S4D` bundle shape while adding access-specific verify/drill results.

## Phases（切片）

- `S4F-1A`（Phase 1）：backend-only access/subscription deployable cut
  - 详见：`docs/logs/log-S4F-1A-backend-only-access-subscription-deployable-cut.md`
- `S4F-2A`（Phase 2）：cloud-target operator evidence packet
  - 详见：`docs/logs/log-S4F-2A-cloud-target-operator-evidence-packet.md`
- `S4F-2B`（Phase 2 follow-up）：release-path dependency trust hardening
  - 详见：`docs/logs/log-S4F-2B-release-path-dependency-trust-hardening.md`
- `S4F-2C`（Phase 2 follow-up）：deployed identity/admission/membership truth hardening
  - 详见：`docs/logs/log-S4F-2C-deployed-identity-admission-membership-truth-hardening.md`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：`S4F` parent/spine created for the first `road-002-01/M1` runtime packet
- [x] `P1`：first child packet fixed as `S4F-1A`
- [x] `P2`：default reuse boundary from `S4D` fixed
- [x] `P3`：first concrete deployable packet executed and evidenced

## Current Status（进展摘要）

- `S4F` now has one completed first packet in `S4F-1A`, one completed cloud-target evidence packet in `S4F-2A`, one completed trust-hardening follow-up packet in `S4F-2B`, and one completed realism-hardening follow-up packet in `S4F-2C`.
- `S4F-2A/P1` is now landed: the reused `S4D` release path can optionally run the `S4F` access-aware verify overlay and write the combined result back into the retained artifact bundle.
- `S4F-2A/P2` is now complete. The lane progressed through three distinct failure classes on the same operator path before closing green: target reachability (`24655583207`), post-change runtime verify (`24654777721`), and access-overlay script parsing (`24661990707`), then finished with a full PASS evidence bundle in run `24662387235` on head `07c99aa0f571cf04ba97ef25b4d52cf52d9f64e7`.
- `S4F-2A/P2` also now includes the operator-side observation fallback and API-path diagnosis: the queued Windows fallback run `24654777721` can be read cleanly via one-shot `gh run view` / `gh api`, and the earlier `gh run watch` failure has been narrowed to an intermittent local polling-path timeout rather than a repo-side workflow lookup failure.
- `S4F-2B` has now produced one hardened stable-runner evidence run, and `S4F-2C/P0-P3` are now fixed: the current slice now has one retained cloud-target member/admin drill bundle proving request-level dev actor identity plus persistence-backed tenant standing on the deployed path, and the next execution lane should leave `M2` and move to `road-002-01/M3-P0` cloud-backed asset-platform readiness contract work.

## Notes（落地原则，可选）

- Reuse infrastructure and workflow first; only specialize the verify/drill contract.
- Keep the first deployed proof narrow enough that one operator can explain it end to end.

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - the `S4F` family boundary is fixed;
  - the default reuse rule from `S4D` is fixed;
  - the first concrete packet and its success criteria are explicit.

## Numbering & Commit Naming（编号与提交命名）

- 编号约定：`P<n>` 表示 Phase，`C<n>` 表示 Cycle，`S<n>` 表示 Step。
- Commit / PR 命名：
  - 基础形式：`S4F/P<phase>-C<cycle>-S<steps>: <summary>`；
  - 若一个 PR 一次性汇总多个完整 phase，应优先压缩成 phase 范围标题：`S4F/P0-P3: access / subscription deployable runtime cut`。

**Branch 约定（建议）**:

- `S4F` 相关实现与文档当前优先落在 `S4F-access-subscription-deployable-runtime-cut` 分支。

**Commit 纪律（建议）**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push`；
- phase-specific 变更优先使用对应 child log 前缀，例如 `S4F-1A/...`。

## Recent changes（for traceability，可选）

- 2026-04-20：首次创建 `S4F`，作为 `road-002-01/M1` 的新 `S4` 顶层 spine，并把第一条 execution lane 固定到 `S4F-1A`。
- 2026-04-20：`S4F-1A` completed `P0-P3`, so the parent spine now has its first executed and evidenced child packet plus one explicit next-lane decision: prioritize cloud-path operator evidence before frontend cloud closure.
- 2026-04-20：opened `S4F-2A` as the next child packet, dedicated to one cloud-target operator evidence run on the reused `S4D` release substrate.
- 2026-04-20：completed `S4F-2A/P1-C1-S1S2`, wiring the access-aware verify overlay into the reused `S4D` cloud release workflow and summary artifact contract.
- 2026-04-20：recorded the first real `S4F-2A/P2` stable-runner attempt (`24655583207`), which retained artifacts successfully but failed preflight on target SSH reachability before deploy/verify/access overlay execution.
- 2026-04-20：fixed the post-run summary renderer indentation in both cloud release dispatch workflows so reruns report the retained `summary.json` outcome cleanly.
- 2026-04-20：added `S4F-2A/P2` fallback run-status evidence and operator-to-GitHub API diagnostics, confirming that `gh run watch` was the unstable observation path while one-shot API reads remained healthy.
- 2026-04-20：recovered the local operator path by resetting the VM, restoring guest SSH on `127.0.0.1:22022`, re-registering the deleted Windows self-hosted runner, and turning fallback run `24654777721` into a real deploy/verify sample.
- 2026-04-20：recorded that the new `S4F-2A/P2` blocker is no longer target reachability on the local path but post-change verify readiness: the candidate deploy passed, yet the expected `wordloom-api-cloud-dev` container was not alive by verify time and guest-side evidence showed a host-port binding conflict during failed container startup.
- 2026-04-20：restored RDS reachability for the current operator egress path, isolated and fixed the access-overlay JSON parsing defect in `cloud_release_access_verify.sh`, and closed `S4F-2A/P2` with one full PASS cloud-target evidence run (`24662387235`).
- 2026-04-20：recorded the next-lane decision from `S4F-2A/P3`: `road-002-01/M1` now has sufficient backend deployment-facing evidence, and the remaining hardening work should move to a separate lane that removes drifting operator public-IP / RDS allowlist dependence.
- 2026-04-20：opened `S4F-2B` as that follow-up lane and scaffolded it as the source log for release-path dependency trust hardening.
- 2026-04-20：opened `S4F-2C` as the next follow-up lane after `S4F-2B`, dedicated to `road-002-01/M2` credibility hardening for deployed identity/admission/membership truth.
- 2026-04-20：completed `S4F-2C/P0-C1-S1S2S3`, fixing the first deployed credibility boundary and narrowing the next implementation target to backend-validated identity plus persistence-backed admission/membership truth.
- 2026-04-20：completed `S4F-2C/P1-C1-S1S2`, landing a stable dev actor identity bridge from frontend session state into backend auth-context fallback so membership-backed tenant standing can resolve per actor instead of per process.
- 2026-04-20：completed `S4F-2C/P2-C1-S1S2`, retaining one stable-runner cloud-target PASS run (`24668611462`) whose access overlay proved member/admin standing through the new request-level dev identity bridge and persistence-backed tenant membership truth.
- 2026-04-20：completed `S4F-2C/P3-C1-S1`, deciding that no immediate second `M2` child packet is required and that the next branch-road execution lane should move to `M3/P0` asset-platform readiness contract work.
