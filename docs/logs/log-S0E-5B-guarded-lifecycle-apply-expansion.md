# log-S0E-5B (Phase 5B: Guarded Lifecycle Apply Expansion)

---

**id**: `S0E-5B`
**kind**: `log`
**title**: `guarded lifecycle apply expansion v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Issues, PR, Automation, Drills, Evidence, epic/s0, sub/0e5b`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/307`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/308`
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  **reference_log_1**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
  **reference_log_4**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/307`
**created**: `2026-03-30`
**updated**: `2026-03-30`

---

## Decision / Outcome

**Decision**:

- `S0E-5B` exists as the follow-up after `S0E-5A`, focused on expanding guarded pre-gate behavior from one issue-conclusion mutation path to a broader set of real lifecycle apply operations.
- The next step is not another dry-run-only gate. It is a controlled apply expansion that keeps `S0E-5A` audit artifacts as the single precondition layer while widening the set of mutations that must honor that gate.
- The operator-facing goal is one consistent rule: if the lifecycle pre-gate does not allow apply, the tool must stop before mutating issue relationships, PR creation state, or later close-out steps.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Expand guarded lifecycle apply beyond issue conclusion by adding one targeted-remediation continuation rule for relationship attach while keeping the generic pre-gate as the source of truth.
- Add one guarded PR-body rewrite path that only proceeds on `allow-apply`, then validate it against a real merged PR and a frozen blocked fixture.
- Use `S0E-5B` itself as the representative sample so relationship attach, PR lifecycle, and post-merge close-out can all be traced on one real issue instead of isolated drills.

**PR checklist source**:

- Default source: reuse this log's execution checklist after `P0-P3` are reviewed.

**PR links / evidence footer**:

- Log: `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/307`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`

**Default choices (phase defaults / v1)**:

- `S0E-5B` should start from the already-validated `S0E-5A` contracts and avoid redefining audit severity or remediation semantics.
- Expansion should proceed one mutation family at a time, with real GitHub validation after each new guarded path rather than a large one-shot orchestration jump.
- Relationship attach and PR-side lifecycle mutations are the first expected guarded apply candidates because `S0E-5A` only proved the issue-conclusion path directly.
- The generic lifecycle pre-gate decision remains the source of truth, but a guarded mutation family may define one narrow continuation rule when the emitted remediation plan contains exactly the mutation family that the command is designed to apply.

## Constraints

- Do not weaken the fail-closed pre-gate policy introduced in `S0E-5A`.
- Do not bypass the explicit remediation-planning output when `warning` or `blocked` findings remain.
- Do not merge multiple new guarded mutation families into one undifferentiated implementation step; each path should leave isolated evidence.

## Scope

- `P0`: define the expansion boundary from guarded issue-conclusion apply to broader guarded lifecycle apply
- `P1`: add one guarded relationship-attach path behind the same pre-gate
- `P2`: evaluate whether PR creation or PR-body mutation should become the next guarded apply family
- `P3`: validate one representative real closed-loop sample that uses more than one guarded mutation family under the same gate policy

## Success Criteria (DoD)

- `S0E-5A` remains the source of truth for audit and decision semantics, while `S0E-5B` only expands guarded apply coverage.
- At least one new mutation family beyond issue conclusion is wired behind the same pre-gate and validated on live GitHub state.
- Evidence clearly shows where apply was allowed, where it stopped, and which remediation artifacts were emitted for blocked paths.

## Stability (what stable means)

- This log can be marked `stable` when:
  - guarded relationship attach and guarded PR-body rewrite have both been validated on live GitHub state;
  - at least one representative sample proves those guarded mutation families can coexist on the same issue/PR pair without breaking final closed-loop convergence;
  - the remaining open question is no longer whether guarded apply works for in-place mutations, but whether guarded `PR create` deserves its own follow-up slice.

## Current Status

- `S0E-5A` has finished one full real lifecycle on itself: issue `#305`, merged PR `#306`, sidebar relationship attach, and final issue conclusion are all complete.
- `P0` is now fixed: relationship attach is the first mutation family that may continue from a `stop-for-remediation` gate decision, but only when the remediation output contains planned `attach-parent-relationship` steps and nothing outside that family.
- `P1` is now implemented and validated: live issue `#307` was created for `S0E-5B`, the guarded relationship path attached it to parent issue `#248`, and the same command shape stopped on a frozen mixed-remediation sample without applying anything.
- `P2` is now completed with `PR body rewrite` as the next guarded mutation family: merged PR `#306` was rewritten in place behind an `allow-apply` gate, while the archived blocked fixture still stopped before any PR mutation.
- `P3` is now completed on one real sample: issue `#307` was first attached through the guarded relationship path, then delivered by merged PR `#308`, and that same merged PR was rewritten through the guarded PR-body path before the issue was concluded in place.
- `S0E-5B` now has one representative closed-loop sample that carries two distinct guarded mutation families on the same issue/PR pair instead of proving them only on separate drills.
- `S0E-5B` is now `stable`: the guarded apply expansion for in-place lifecycle mutations has been validated end to end, and the remaining work has been intentionally split into a new `S0E-5C` follow-up for guarded `PR create` rather than being stretched into this slice.

## P0 (Expansion boundary | v1)

### P0-C1-S1 (Targeted remediation continuation rule | v1)

- `S0E-5A` keeps ownership of the generic lifecycle audit, decision, and remediation-planning semantics.
- `S0E-5B` introduces one mutation-family-specific rule: a guarded relationship-attach command may continue even when the generic gate decision is `stop-for-remediation`, but only if the remediation plan says the requested item is fixable exclusively through planned `attach-parent-relationship` steps.
- If lifecycle remediation includes any other planned action kinds, any manual follow-up, or any ambiguous/multiple downstream relationship manifests, the guarded relationship command must stop before apply.

## P1 (Guarded relationship attach | v1)

### P1-C1-S1 (Guarded apply entrypoint implemented | v1)

- `apply_issue_relationships_with_pre_gate.py` now runs the same lifecycle pre-gate used by guarded issue conclusion, then inspects the remediation output before deciding whether relationship apply is eligible.
- The guarded relationship path derives its relationship manifest from lifecycle remediation output by default instead of requiring the operator to manually splice together a second input.
- The command wrapper now enforces a bounded timeout for `gh` subprocess calls so a stalled GitHub CLI call fails closed instead of hanging indefinitely.

### P1-C1-S2 (Live pass and frozen stop validation | v1)

- The live pass sample uses real issue `#307`, where the generic lifecycle gate returns `stop-for-remediation` because the sidebar parent relationship is still missing, yet the guarded command is allowed to continue because the only planned remediation is `attach-parent-relationship`.
- The guarded pass sample converges by attaching `#307` under parent issue `#248` and recording `applied-after-pre-gate` in the guarded result artifact.
- The frozen stop sample reuses the archived `S0E-5A` fixture audit plan; because that remediation set mixes relationship repair with issue-conclusion refresh, the guarded relationship command stops before apply with `blocked-mixed-remediation`.

## P2 (Guarded PR-body rewrite | v1)

### P2-C1-S1 (PR-body rewrite selected as the next guarded family | v1)

- `PR body rewrite` is the next guarded mutation family after relationship attach because it mutates a single live GitHub object in place and can reuse existing `pr-create` traceability artifacts without re-entering branch/materialization risk.
- Unlike guarded relationship attach, the PR-body rewrite path does not introduce a targeted-remediation continuation exception; it continues only when the generic lifecycle pre-gate result is `allow-apply`.
- The current `P2` contract therefore stays narrower than `PR create`: the guard protects a post-create PR body rewrite path, not branch preparation or initial PR publication.

### P2-C1-S2 (Live pass and frozen stop validation | v1)

- The live pass sample uses converged `S0E-5A` issue `#305` as the gate input and merged PR `#306` as the mutation target, so the gate returns `allow-apply` and the PR body rewrite can proceed without any targeted-remediation exception.
- The guarded PR-body rewrite path fetches the live PR body, rewrites checklist/evidence sections from the current source-log scope, and writes the new body back through `gh pr edit`.
- The same command shape stops before apply on the archived `S0E-5A` blocked fixture because the generic gate result remains `stop-for-remediation`; unlike relationship attach, no narrow continuation rule exists for PR-body mutation.

## P3 (Combined live closed loop | v1)

### P3-C1-S1 (Same-sample guarded mutation composition | v1)

- The representative sample for `P3` is `S0E-5B` itself: live issue `#307` plus live PR `#308`.
- The sample reuses the guarded relationship attach already validated on `#307`, then continues on the same issue to a real PR, merge, guarded PR-body rewrite, and final issue conclusion.
- `P3` therefore validates composition, not a new mutation family: the key question is whether distinct guarded mutation families still remain traceable and safe when they are exercised on the same lifecycle sample.

### P3-C1-S2 (Closed-loop convergence on one representative sample | v1)

- The combined sample is considered successful only if the final issue is closed with exact-ID merged PR evidence, the parent sidebar relationship remains intact, and the merged PR body can be rewritten from the final log scope after the lifecycle completes.
- The PR body rewrite in this phase is intentionally run after the representative sample reaches merged/closed-loop state so the final PR description reflects `P0-P3` rather than the narrower scope that existed when PR `#308` was first opened.
- The sample remains fail-closed because the PR-body rewrite still runs behind a fresh lifecycle pre-gate on `#307`; if the issue state had drifted after merge, the body rewrite would stop instead of silently rewriting the PR.

## Plan (draft)

- `P0-C1-S1`: fix the exact mutation families that are in-scope for the first guarded apply expansion
- `P1-C1-S1`: connect the lifecycle pre-gate to one relationship-attach apply path
- `P1-C1-S2`: validate one live pass sample and one stop-before-apply sample for the guarded relationship path
- `P2-C1-S1`: decide whether PR creation, PR body rewrite, or another mutation family is the next guarded target
- `P2-C1-S2`: validate one live pass sample and one stop-before-apply sample for the chosen PR-side mutation family
- `P3-C1-S1`: choose one real sample that already exercised guarded relationship attach and continue it through PR lifecycle on the same issue/PR pair
- `P3-C1-S2`: verify that the same sample still converges after guarded PR-body rewrite and final issue conclusion

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: expansion boundary fixed
- [x] `P1-C1-S1`: guarded relationship-attach path implemented
- [x] `P1-C1-S2`: pass and stop validation recorded
- [x] `P2-C1-S1`: next guarded mutation family selected
- [x] `P2-C1-S2`: pass and stop validation recorded for the chosen PR-side mutation family
- [x] `P3-C1-S1`: same-sample guarded mutation composition recorded
- [x] `P3-C1-S2`: representative closed-loop sample converged after both guarded mutation families

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the live issue anchor, gate outputs, guarded apply results, and frozen stop evidence for the first guarded relationship path.

### P0-C1-S1 (targeted relationship remediation continuation rule fixed | 2026-03-30)

- headSha: `<git sha>`
- artifacts:
  - `scripts/issues/apply_issue_relationships_with_pre_gate.py`
  - `scripts/issues/gen_issue_draft.py`
  - `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
- expected:
  - relationship attach should be the first guarded mutation family that may continue from `stop-for-remediation` without weakening the generic pre-gate
  - the guarded path should stop when remediation includes any non-relationship action family or manual follow-up
- observed:
  - the new guarded relationship entrypoint now allows apply only when lifecycle remediation is exclusively planned `attach-parent-relationship`, and otherwise fails closed before mutation

### P1-C1-S1S2 (guarded relationship path exercised on live pass and frozen stop samples | 2026-03-30)

- headSha: `<git sha>`
- artifacts:
  - `docs/issues/issue-S0E-5B-guarded-lifecycle-apply-expansion.md`
  - `docs/issues/issue-S0E-5B-guarded-lifecycle-apply-expansion.json`
  - `docs/issues/lifecycle-audit-S0E-5B-p1-pass-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-5B-p1-pass-plan.json`
  - `docs/issues/lifecycle-gate-S0E-5B-p1-pass-decision.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p1-pass-plan.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p1-pass-relationship-manifest.json`
  - `docs/issues/issue-relationship-S0E-5B-p1-pass-plan.json`
  - `docs/issues/issue-relationship-S0E-5B-p1-pass-parent-248-child-307-apply-result.json`
  - `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`
  - `docs/issues/lifecycle-gate-S0E-5B-p1-stop-decision.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p1-stop-plan.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p1-stop-relationship-manifest.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p1-stop-issue-conclusion-manifest.json`
  - `docs/issues/issue-relationship-S0E-5B-p1-stop-guarded-apply-result.json`
- expected:
  - the live pass sample should continue from `stop-for-remediation` only because relationship attach is the sole planned remediation family
  - the frozen stop sample should refuse to apply because mixed remediation would exceed the guarded relationship command boundary
- observed:
  - live issue `#307` was created and then attached to parent issue `#248` through the guarded relationship path, with `guarded_eligibility = allowed-via-targeted-relationship-remediation`
  - the archived fixture sample stopped before apply with `guarded_eligibility = blocked-mixed-remediation` because the remediation output also contained `plan-issue-conclusion-refresh`

### P2-C1-S1S2 (guarded PR-body rewrite exercised on live pass and frozen stop samples | 2026-03-30)

- headSha: `<git sha>`
- artifacts:
  - `scripts/issues/apply_pr_body_scope_with_pre_gate.py`
  - `scripts/issues/rewrite_pr_body_scope_from_log.py`
  - `docs/issues/lifecycle-audit-S0E-5B-p2-pass-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-5B-p2-pass-plan.json`
  - `docs/issues/lifecycle-gate-S0E-5B-p2-pass-decision.json`
  - `docs/issues/pr-prep-S0E-5A-real-live-body.md`
  - `docs/issues/pr-prep-S0E-5A-real-rewritten-body.md`
  - `docs/issues/pr-prep-S0E-5A-real-rewrite-apply-result.json`
  - `docs/issues/pr-prep-S0E-5A-real-guarded-pr-body-rewrite-result.json`
  - `docs/issues/lifecycle-gate-S0E-5B-p2-stop-decision.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p2-stop-plan.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p2-stop-relationship-manifest.json`
  - `docs/issues/lifecycle-remediation-S0E-5B-p2-stop-issue-conclusion-manifest.json`
  - `docs/issues/pr-prep-S0E-5A-real-stop-guarded-pr-body-rewrite-result.json`
- expected:
  - the chosen PR-side guarded family should only continue when the generic lifecycle pre-gate returns `allow-apply`
  - the same guarded PR-body rewrite command should stop cleanly on a frozen blocked fixture without mutating any PR body
- observed:
  - merged PR `#306` was rewritten in place through the guarded path against converged `S0E-5A` issue state, and the apply result records `body_changed = true`
  - the archived blocked fixture stopped before any PR edit with `mutation blocked by lifecycle pre-gate decision: stop-for-remediation`

### P3-C1-S1S2 (same-sample guarded mutation composition converged on S0E-5B | 2026-03-30)

- headSha: `<git sha>`
- artifacts:
  - `docs/issues/pr-prep-S0E-5B-real-manifest.json`
  - `docs/issues/pr-prep-S0E-5B-real-plan.json`
  - `docs/issues/pr-prep-S0E-5B-real-create-body.md`
  - `docs/issues/pr-prep-S0E-5B-real-create-result.json`
  - `docs/issues/lifecycle-audit-S0E-5B-p3-pass-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-5B-p3-pass-plan.json`
  - `docs/issues/lifecycle-gate-S0E-5B-p3-pass-decision.json`
  - `docs/issues/pr-prep-S0E-5B-real-live-body.md`
  - `docs/issues/pr-prep-S0E-5B-real-rewritten-body.md`
  - `docs/issues/pr-prep-S0E-5B-real-rewrite-apply-result.json`
  - `docs/issues/pr-prep-S0E-5B-real-guarded-pr-body-rewrite-result.json`
  - `docs/issues/issue-conclusion-S0E-5B-live-manifest.json`
  - `docs/issues/issue-conclusion-S0E-5B-live-plan.json`
  - `docs/issues/issue-conclusion-S0E-5B-live-s0e-5b-body.md`
  - `docs/issues/issue-conclusion-S0E-5B-live-s0e-5b-apply-body.md`
  - `docs/issues/issue-conclusion-S0E-5B-live-s0e-5b-apply-result.json`
- expected:
  - one representative sample should carry both guarded relationship attach and guarded PR-body rewrite on the same issue/PR pair, then still converge on merged PR plus closed issue output
  - the final PR body should reflect the completed `P0-P3` scope rather than the narrower PR-open snapshot
- observed:
  - issue `#307` first exercised guarded relationship attach, then moved through real PR `#308`, merge, guarded PR-body rewrite, and final issue conclusion without leaving the same sample
  - the final issue body now records `#308` in DoD, while merged PR `#308` has been rewritten from the final `S0E-5B` log scope after the combined sample closed

## Recent changes (for traceability, optional)

- 2026-03-30: created `S0E-5B` as the follow-up slice for expanding guarded pre-gate enforcement beyond the issue-conclusion mutation path validated in `S0E-5A`.
- 2026-03-30: created live issue `#307` for `S0E-5B` and wrote the exact GitHub issue link back to this source log.
- 2026-03-30: completed `P0` by fixing the targeted-remediation continuation rule for guarded relationship attach instead of reusing the generic `allow-apply` rule unchanged.
- 2026-03-30: completed `P1` by implementing `apply_issue_relationships_with_pre_gate.py`, attaching `#307` to parent issue `#248` through the guarded pass path, and validating a frozen mixed-remediation stop drill.
- 2026-03-30: completed `P2` by selecting PR-body rewrite as the next guarded PR-side family, rewriting merged PR `#306` behind an `allow-apply` gate, and validating a frozen stop-before-edit drill on the archived blocked fixture.
- 2026-03-30: completed `P3` by using `#307` plus merged PR `#308` as one representative closed-loop sample, then rewriting that merged PR through the guarded PR-body path and concluding the issue in place.
- 2026-03-30: marked `S0E-5B` as `stable` and split guarded `PR create` investigation into the new `S0E-5C` follow-up instead of continuing to overload this slice.