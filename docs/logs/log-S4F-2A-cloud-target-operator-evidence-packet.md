# log-S4F-2A (Phase 2: Cloud-target operator evidence packet)

---

**id**: `S4F-2A`
**kind**: `log`
**title**: `cloud-target operator evidence packet (S4D release path reuse + S4F access-aware verify overlay) v1`
**status**: `stable`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, CloudRuntime, AccessControl, Verification, ReleaseOperations, Drills, Evidence, epic/s4, sub/2a`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/508`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/512`
  **runbook**: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  **roadmap**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
  **parent_log**: `docs/logs/log-S4F-access-subscription-deployable-runtime-cut.md`
  **previous_log**: `docs/logs/log-S4F-1A-backend-only-access-subscription-deployable-cut.md`
  **reference_log_1**: `docs/logs/log-S4D-2A-post-change-verification-and-operational-checks.md`
  **reference_log_2**: `docs/logs/log-S4D-4A-cloud-runtime-semi-automated-release-workflow.md`
  **reference_log_3**: `docs/logs/log-S4D-4C-408-timeout-eradication.md`
  **reference_log_4**: `docs/logs/log-S4F-1A-backend-only-access-subscription-deployable-cut.md`
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
- Day-level precision is acceptable here because the lane is opening as one bounded operator-evidence packet rather than one long multi-environment program.
- `reviewed` should remain `pending` until one real cloud-target operator evidence bundle is accepted.

## Decision / Outcome

**Decision**:

- `S4F-2A` opens the next concrete `S4F` packet after `S4F-1A`, focusing on one operator-facing cloud-target evidence run instead of more local or CI-only runtime proof.
- The packet reuses the stable `S4D` release substrate and adds the `S4F` access-aware verify overlay so one evidence bundle can prove both generic deploy/verify success and feature-level member/admin/lifecycle success.

**Default choices (phase defaults / v1)**:

- Keep the target shape on the existing `S4D` substrate: one Linux VM, one backend container, one cloud-dev env file, and one external cloud-dev RDS.
- Do not open frontend cloud closure in this packet; the required proof is operator-facing cloud runtime evidence for the backend access/subscription slice.
- Do not invent a new workflow. The default entry remains the reused `S4D` operator workflow and its stable evidence bundle shape.
- Evidence in this packet must be cloud-target and operator-facing; GitHub-hosted CI runtime proof alone is no longer sufficient.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S4F-2A` is intended to drive the next deployment-facing PR under `road-002-01/M1-P3`.

**PR summary bullets**:

- Reuse the stable `S4D` cloud release path for one operator-facing cloud-target evidence run of the access/subscription slice.
- Add the `S4F` access-aware verify overlay to the same run so member/admin/lifecycle probes are proven on the actual release path.
- Close the gap left by `S4F-1A`: move from runnable CI proof to operator-facing cloud runtime evidence.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S4F-2A-cloud-target-operator-evidence-packet.md`
- Runbook: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
- Evidence artifact: `artifacts/_tmp_s4d4b_cloud_release_dispatch/24662387235-1/summary.json`

**Evidence Footer Source**:

- `P2-C1-S1` | artifact: `artifacts/_tmp_s4d4b_cloud_release_dispatch/24662387235-1/summary.json`

## Definitions (optional)

- `cloud-target operator evidence`: one evidence bundle produced through the real `S4D` release path against the actual cloud-target runtime, not a host-local drill harness.
- `access-aware verify overlay`: the `S4F` probe layer that checks member read, admin read, lifecycle mutation, and deterministic re-read on top of generic runtime readiness.
- `combined evidence bundle`: one retained artifact set where `preflight/deploy/verify` results and `memberReadResult/adminReadResult/lifecycleMutationResult/rerenderedStateResult` can be read together.

## Constraints

- Do not introduce a second operator path beside `scripts/ops/cloud_release_workflow.sh`.
- Do not widen this packet into frontend cloud hosting, worker residency, or asset-platform object handling.
- Do not treat generic health or startup checks as sufficient; the packet must prove the feature overlay on the same cloud-target path.
- Do not claim success from CI-hosted local runtime only; the required evidence surface is the operator-facing cloud release path.

## Scope

- `P0`: contract (combined cloud-target evidence shape, verify overlay boundary, operator input tuple)
- `P1`: implementation / packaging (wire `S4F` access-aware probes onto the reused `S4D` operator path and artifact bundle)
- `P2`: drill / verify (capture one real cloud-target operator evidence run)
- `P3`: close-out / next-lane decision (decide whether `M1` is sufficiently evidenced or whether one more realism-tightening packet is required)

## Success Criteria (DoD)

- The packet fixes one explicit cloud-target operator evidence boundary for the access/subscription slice.
- The packet reuses the stable `S4D` workflow and evidence bundle instead of inventing another release entry.
- The evidence bundle records both generic workflow results and feature-level access-aware probe results.
- At least one real run proves:
  - `deployResult=PASS`
  - `verifyResult=PASS`
  - `memberReadResult=PASS`
  - `adminReadResult=PASS`
  - `lifecycleMutationResult=PASS`
  - `rerenderedStateResult=PASS`
- The packet leaves one explicit conclusion on whether branch-road `M1` now has sufficient deployment-facing evidence.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the combined cloud-target evidence contract is explicit;
  - one real operator-facing cloud-target run is captured with traceable artifacts;
  - the next-lane decision after that evidence is recorded explicitly.

## P0 (Contract | v1)

### P0-C1-S1 (Combined cloud-target evidence boundary | v1)

- `S4F-2A` must prove the access/subscription slice on the same operator-facing cloud release path already stabilized by `S4D`.
- The packet boundary is not "another backend drill"; it is one release-facing evidence packet that joins generic runtime release truth with feature-level access truth.

### P0-C1-S2 (Verify overlay contract | v1)

- The `S4F` verify overlay for this packet remains the same three feature probes fixed by `S4F-1A`:
  - member read
  - admin read
  - bounded lifecycle mutation followed by deterministic re-read/history
- The required difference is execution surface: these probes must run on the real cloud-target operator path after the reused `S4D` generic verify gate passes.

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON for this packet must include at least:
  - `headSha`
  - `workflowCommandSummary`
  - `targetHostKind`
  - `envFilePath`
  - `imageTag`
  - `deployResult`
  - `verifyResult`
  - `memberReadResult`
  - `adminReadResult`
  - `lifecycleMutationResult`
  - `rerenderedStateResult`
  - `rollbackResult`
  - `result`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4F-2A/P<phase>-C<cycle>-S<steps>: <summary>`

**Branch convention**:

- `S4F-2A` related implementation and documentation should continue on `S4F-access-subscription-deployable-runtime-cut` unless a later packet justifies a separate focused branch.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit, whether it is contract work, implementation, or drills/evidence, commit/push promptly on the current `S4F` working branch.

## Plan (draft)

### P1 (Implementation / packaging)

- P1-C1-S1: define the exact operator-facing verify tuple and artifact write-back shape for the `S4F` overlay on the reused `S4D` path
- P1-C1-S2: wire the overlay commands or helper script into the retained cloud release evidence bundle

### P2 (Drill / Verify)

- P2-C1-S1: capture one real cloud-target operator evidence run with generic `S4D` workflow PASS plus `S4F` feature probe PASS
- P2-C1-S2: capture the resulting artifact path, run metadata, and probe outputs in this log

### P3 (Close-out / next-lane decision)

- P3-C1-S1: decide whether branch-road `M1` now has sufficient deployment-facing evidence or whether one more realism-tightening packet is required

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: combined cloud-target evidence boundary fixed
- [x] `P0-C1-S2`: verify overlay contract fixed for the real operator path
- [x] `P0-C1-S3`: combined evidence JSON contract fixed

### P1 (Implementation / packaging)

- [x] `P1-C1-S1`: operator-facing verify tuple and artifact write-back shape fixed
- [x] `P1-C1-S2`: overlay wiring landed on the reused `S4D` path

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: cloud-target operator evidence run captured
- [x] `P2-C1-S2`: evidence artifact, run-state fallback query, and operator/API path diagnostics recorded

### P3 (Close-out / next-lane decision)

- [x] `P3-C1-S1`: branch-road `M1` sufficiency decision recorded

## Current Status (recommended)

- `S4F-2A` is now end-to-end evidenced on the reused `S4D` path. Real run `24662387235` on head `07c99aa0f571cf04ba97ef25b4d52cf52d9f64e7` passed preflight, deploy, generic verify, and the `S4F` access-aware overlay, producing one complete operator-facing cloud-target evidence bundle.
- `P2` produced four meaningful samples on the way to closure: stable-runner preflight failure (`24655583207`), local-path deploy/verify failure (`24654777721`), local-path verify-pass/access-script failure (`24661990707`), and the final clean PASS run (`24662387235`). Together they separate environment reachability, runtime readiness, and overlay-script defects instead of collapsing them into one opaque failure.
- The GitHub Actions observation path is now also pinned down for `P2`: `gh run watch` timed out while polling the jobs endpoint from this operator machine, but one-shot `gh run view` and `gh api` queries succeeded against the same runs and endpoint, so the evidence points to an intermittent local-to-GitHub API polling-path timeout rather than a bad run id, bad token, or bad workflow reference.
- The packet's next-lane decision is now explicit: `road-002-01/M1` has sufficient backend deployment-facing evidence for the access/subscription slice, while the remaining realism-tightening work should move to a separate lane that removes dependence on drifting operator public `/32` RDS allowlists.

## Evidence (reserved)

- Artifacts are the source of truth for evidence. The first real `P2` attempt is now retained as a failing preflight sample:
- run id: `24655583207`
- head sha: `68d0af1b2f7f6b8c2d0d7981670ee40303342d30`
- workflow: `s4d-cloud-release-dispatch-stable-runner`
- result: `FAIL`
- failure class: `evidence_capture_failure`
- terminal stage / gate: `evidence` / `evidence_capture`
- preflight result: `FAIL`
- target reachability gate: `FAIL`
- deploy / verify / access overlay: `NOT_RUN` / `NOT_RUN` / `NOT_RUN`
- retained artifact dir: `artifacts/_tmp_s4f2a_p2_run_24655583207`
- retained files:
  - `summary.json`
  - `preflight.log`
  - `operator_guidance.txt`
- preflight failure excerpt: `ssh: connect to host 49.196.191.226 port 22022: Connection timed out`
- operator guidance outcome: stop at preflight, fix target reachability, then rerun the same workflow command.
- GitHub Actions status fallback evidence recorded during `P2`:
  - `gh run view 24654777721 --json ...` returned `status=queued`, `conclusion=null`, workflow `s4d-cloud-release-dispatch`, head sha `68d0af1b2f7f6b8c2d0d7981670ee40303342d30`
  - `gh api repos/samuelhu324-dev/wordloom-v3/actions/runs/24654777721/jobs ...` returned one queued job: `cloud-runtime-release` (`72085514477`)
  - `gh run view 24655583207 --json ...` returned `status=completed`, `conclusion=failure`, workflow `s4d-cloud-release-dispatch-stable-runner`, with the known failed steps `Write run summary` and `Enforce workflow result` from the pre-fix run
- Operator-to-GitHub API path diagnosis recorded during `P2`:
  - `gh auth status` remained healthy for `samuelhu324-dev`; token scopes included `repo` and `workflow`
  - proxy environment variables were empty: `HTTPS_PROXY`, `HTTP_PROXY`, `ALL_PROXY`, `NO_PROXY`
  - DNS resolution for `api.github.com` succeeded (`A 4.237.22.34`, `AAAA 2405:dc00:0:3::4ed:1622`)
  - `Invoke-WebRequest https://api.github.com/rate_limit` returned `200 OK`
  - `Test-NetConnection api.github.com -Port 443` returned `TcpTestSucceeded=True`
  - working conclusion: the screenshot failure was a local polling-path timeout during `gh run watch`, not an authentication failure and not proof that the run state was unavailable from GitHub.
- Second real `P2` sample retained after SSH and runner recovery:
  - run id: `24654777721`
  - workflow: `s4d-cloud-release-dispatch`
  - target host kind: `Ubuntu Server VM via SSH (wordloom@127.0.0.1:22022)`
  - head sha / remote head sha: `68d0af1b2f7f6b8c2d0d7981670ee40303342d30` / `68d0af1b2f7f6b8c2d0d7981670ee40303342d30`
  - result: `FAIL`
  - preflight / deploy / verify / access overlay: `PASS` / `PASS` / `FAIL` / `NOT_RUN`
  - gate results:
    - `identityAuthGate=PASS`
    - `targetReachabilityGate=PASS`
    - `dependencyConnectivityGate=PASS`
    - `releaseContractGate=PASS`
    - `deployExecutionGate=PASS`
    - `postChangeVerifyGate=FAIL`
    - `accessAwareVerifyGate=NOT_RUN`
  - retained artifact dir: `artifacts/_tmp_s4d4b_cloud_release_dispatch/24654777721-1`
  - retained files:
    - `preflight.log`
    - `deploy.log`
    - `verify.log`
    - `operator_guidance.txt`
    - `summary.json`
  - verify failure excerpt:
    - `container not found: wordloom-api-cloud-dev`
    - `health_ok FAIL (000)`
    - `read_smoke_ok FAIL (code=000)`
  - guest-side root-cause probe after the run:
    - fallback Windows runner `wordloom-s4d-temp-win` had to be re-registered because its server-side registration had been deleted
    - guest SSH on `127.0.0.1:22022` was restored by resetting the local VM and confirming `systemctl is-active ssh = active`
    - deploy had briefly hung on removing the old container; after manual `docker rm -f wordloom-api-cloud-dev`, the workflow continued
    - the failed deploy container state captured `created|128|failed to bind host port for 0.0.0.0:30033 ... address already in use|wordloom-backend:cloud-dev`
  - operator guidance outcome: candidate appeared deployed enough for deploy PASS, but post-change verify failed; inspect probe target / API reachability / container survival before the next deploy attempt.
- Third real `P2` sample retained after RDS ingress restoration:
  - run id: `24661990707`
  - workflow: `s4d-cloud-release-dispatch`
  - target host kind: `Ubuntu Server VM via SSH (wordloom@127.0.0.1:22022)`
  - head sha / remote head sha: `96049c9c540b21112e843b89dd9ba361f8657228` / `96049c9c540b21112e843b89dd9ba361f8657228`
  - result: `FAIL`
  - preflight / deploy / verify / access overlay: `PASS` / `PASS` / `PASS` / `NOT_RUN`
  - retained artifact dir: `artifacts/_tmp_s4d4b_cloud_release_dispatch/24661990707-1`
  - retained files:
    - `preflight.log`
    - `deploy.log`
    - `verify.log`
    - `operator_guidance.txt`
    - `summary.json`
  - verify failure excerpt:
    - `CLOUD_RELEASE_VERIFY_RESULT=PASS`
    - `Traceback (most recent call last):`
    - `NameError: name 'null' is not defined`
  - root cause: `scripts/ops/cloud_release_access_verify.sh` mixed Python heredoc script input with later stdin redirection from JSON files, so Python executed JSON payload text instead of the intended script.
- Final `P2` success sample retained on the same local operator path:
  - run id: `24662387235`
  - workflow: `s4d-cloud-release-dispatch`
  - target host kind: `Ubuntu Server VM via SSH (wordloom@127.0.0.1:22022)`
  - head sha / remote head sha: `07c99aa0f571cf04ba97ef25b4d52cf52d9f64e7` / `07c99aa0f571cf04ba97ef25b4d52cf52d9f64e7`
  - result: `PASS`
  - preflight / deploy / verify / access overlay: `PASS` / `PASS` / `PASS` / `PASS`
  - gate results:
    - `identityAuthGate=PASS`
    - `targetReachabilityGate=PASS`
    - `dependencyConnectivityGate=PASS`
    - `releaseContractGate=PASS`
    - `deployExecutionGate=PASS`
    - `postChangeVerifyGate=PASS`
    - `accessAwareVerifyGate=PASS`
  - retained artifact dir: `artifacts/_tmp_s4d4b_cloud_release_dispatch/24662387235-1`
  - retained files:
    - `preflight.log`
    - `deploy.log`
    - `verify.log`
    - `access_verify_result.json`
    - `operator_guidance.txt`
    - `summary.json`
  - access-aware overlay observed values:
    - `memberReadResult=true`
    - `adminReadResult=true`
    - `lifecycleMutationResult=true`
    - `rerenderedStateResult=true`

## P3 (Close-out / next-lane decision)

### P3-C1-S1 (M1 sufficiency and realism-tightening follow-up | 2026-04-20)

- `road-002-01/M1` now has sufficient backend deployment-facing evidence for the access/subscription slice because one retained operator-facing cloud-target run proves the reused `S4D` release path plus the `S4F` access-aware overlay on the actual target host.
- The next lane should not repeat `S4F-2A`; it should remove the remaining operator-environment fragility by eliminating dependence on drifting operator public `/32` RDS ingress rules.
- Default follow-up direction: move release/verify execution onto a stable VPC-positioned runner or equivalent trusted network position, then replace per-operator `/32` allowlists with a durable SG-to-SG or otherwise fixed-trust path.

## Recent changes (for traceability, optional)

- 2026-04-20: first created `S4F-2A` as the next `S4F` child packet to capture one operator-facing cloud-target evidence run after `S4F-1A` completed the backend-only runtime cut and next-lane decision.
- 2026-04-20: completed `P1-C1-S1S2` by adding `scripts/ops/cloud_release_access_verify.sh`, extending `scripts/ops/cloud_release_workflow.sh` and `scripts/ops/cloud_release_workflow_helpers.sh`, and exposing the optional overlay through `.github/workflows/s4d-cloud-release-dispatch-stable-runner.yml`.
- 2026-04-20: attempted the first real `P2` stable-runner execution (`24655583207`) with `--access-verify-overlay`; the run reached retained artifacts but failed preflight on target SSH reachability before deploy or verify started.
- 2026-04-20: fixed the workflow summary renderer indentation in both cloud release dispatch workflows so future reruns surface the real `summary.json` outcome without a secondary post-run script failure.
- 2026-04-20: added `P2` run-observation fallback evidence showing that one-shot `gh run view` / `gh api` calls can read both relevant workflow runs even though `gh run watch` timed out from the operator machine.
- 2026-04-20: added `P2` operator-to-GitHub API path diagnostics showing healthy auth, DNS, HTTP, and TCP baseline checks, narrowing the screenshot failure to an intermittent polling-path timeout rather than a repo-side workflow error.
- 2026-04-20: recovered the local Ubuntu VM SSH path on `127.0.0.1:22022`, re-registered and relaunched the Windows self-hosted runner `wordloom-s4d-temp-win`, and thereby turned fallback run `24654777721` from `queued` into a real deploy/verify sample.
- 2026-04-20: recorded the second real `P2` sample (`24654777721`), which proved `preflight=PASS` and `deploy=PASS` on the local operator path but failed `postChangeVerifyGate` before the `S4F` access-aware overlay began, with guest-side evidence pointing to container survival / host-port-conflict problems.
- 2026-04-20: restored DB reachability by confirming the current operator egress `/32` in the RDS security group, then captured run `24661990707`, which proved generic verify had recovered and isolated a local script bug in `cloud_release_access_verify.sh` (`NameError: null`).
- 2026-04-20: fixed `cloud_release_access_verify.sh` by piping JSON payloads into Python instead of overriding heredoc script stdin, manually revalidated the overlay on the guest path, and then captured the first full PASS bundle in run `24662387235`.
- 2026-04-20: recorded the close-out decision that `M1` now has sufficient backend deployment-facing evidence and that the remaining public-IP-drift / RDS-trust hardening belongs in a separate follow-up lane.