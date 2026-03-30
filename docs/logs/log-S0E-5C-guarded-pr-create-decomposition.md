# log-S0E-5C (Phase 5C: Guarded PR Create Decomposition)

---

**id**: `S0E-5C`
**kind**: `log`
**title**: `guarded PR create decomposition v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, PR, Automation, Drills, Evidence, epic/s0, sub/0e5c`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/309`
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
  **reference_log_1**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
  **reference_log_3**: `docs/logs/log-S0E-4D-review-hold-and-full-auto-lifecycle-orchestration-follow-up.md`
  **reference_log_4**: `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
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
**pr_development_issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/309`
**created**: `2026-03-30`
**updated**: `2026-03-30`

---

## Decision / Outcome

**Decision**:

- `S0E-5C` exists as the follow-up after `S0E-5B`, focused specifically on whether guarded apply should expand from in-place mutation families to `PR create` itself.
- Unlike relationship attach or PR-body rewrite, `PR create` is not a single-object rewrite; it includes commit selection, branch materialization, fallback logic, remote branch publication, and live PR creation.
- The first task of this slice is decomposition, not immediate guarded rollout: the create path must be broken into smaller guardable units before it can safely join the existing guarded apply family set.

**Default choices (phase defaults / v1)**:

- `S0E-5C` should treat `PR create` as a multi-stage orchestration problem rather than as one opaque mutation command.
- The goal is to decide which stages belong under generic pre-gate protection, which stages need additional targeted rules, and which stages should remain explicitly operator-owned.
- This slice should stay independent from GitHub Actions rollout decisions until the guarded `PR create` boundary is technically stable.
- `P0` is now fixed around seven explicit stages: dry-run plan input resolution, dry-run scope selection and preview, create-time preflight validation, local branch materialization, remote branch publication, live PR publication, and post-create local evidence finalization.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Decompose guarded `PR create` into explicit stages instead of treating the entire create path as one atomic guarded mutation.
- Fix the reuse-vs-new-rule boundary so only create-time preflight may partially reuse the existing lifecycle pre-gate as an issue-readiness layer.
- Validate one bounded front-half sample that stops at `S1-S3`, proving pass/stop evidence can be emitted before any branch materialization or PR publication begins.

**PR checklist source**:

- Default source: reuse this log's execution checklist after `P0-P2` are reviewed.

**PR links / evidence footer**:

- Log: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/309`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/pr-create-S0E-5C-p1-boundary-map.json`

## Constraints

- Do not weaken the guarded apply boundaries already proven in `S0E-5B`.
- Do not equate a successful dry-run PR-prep plan with permission to publish a live PR.
- Do not hide branch materialization, cherry-pick fallback, or remote branch publication inside one uninspectable guarded yes/no step.

## Scope

- `P0`: decompose `PR create` into guardable sub-stages with explicit failure boundaries
- `P1`: identify which sub-stages can reuse the existing lifecycle pre-gate and which need extra targeted rules
- `P2`: validate one dry-run or partial real sample for the decomposed guarded `PR create` path
- `P3`: decide whether the decomposed `PR create` flow is mature enough for standalone guarded apply or better kept as a human-gated orchestration path

## Success Criteria (DoD)

- `S0E-5B` remains closed as the stable home for in-place guarded lifecycle mutations.
- `S0E-5C` makes the `PR create` problem smaller and more explicit instead of folding it into a single opaque command.
- The result clearly states whether guarded `PR create` should proceed, and under what stage boundaries, before any GitHub Actions rollout is attempted.

## Current Status

- `S0E-5B` is now `stable` and has finished its intended scope: guarded in-place lifecycle mutations plus one same-sample combined live drill.
- The remaining open question is no longer “does guarded apply work at all,” but “can the much broader `PR create` flow be decomposed into guardable stages without hiding orchestration risk.”
- `S0E-5C` is now the dedicated container for answering that question.
- `P0` is now completed: the current `PR create` path has been decomposed into seven concrete stages with explicit stop boundaries, and the main outcome is that remote branch publication and live PR publication cannot be treated as one undifferentiated guarded mutation.
- `P1` is now completed: no stage can reuse the existing lifecycle pre-gate unchanged as one all-purpose `PR create` gate; only create-time preflight can reuse it as an issue-readiness layer, and even that stage still needs create-specific targeted checks before any local mutation begins.
- `P2` is now completed: live issue `#309` has been created and attached under parent issue `#248`, and one bounded front-half sample now proves that `S1-S3` can emit both pass and stop results without entering local branch materialization or live PR publication.

## P0 (PR create stage map | v1)

### P0-C1-S1 (Stage decomposition and failure boundaries fixed | v1)

- The current `PR create` implementation is now decomposed into seven stages across the existing `plan_pr_prep.py` and `create_pr_from_plan.py` path, with the stage map recorded in `docs/issues/pr-create-S0E-5C-p0-stage-map.json`.
- `S1-S3` are pre-publication stages: dry-run input resolution, exact-ID scope selection plus preview generation, and create-time preflight validation. These stages must fail before any local branch mutation, remote push, or live PR publication occurs.
- `S4` is the first local mutation boundary: an isolated worktree and prepared branch are materialized, selected commits are cherry-picked, and snapshot fallback may rebuild the branch from the source-head snapshot when cherry-pick conflicts occur.
- `S5` is the first irreversible remote git write: the prepared branch is pushed to `origin`. This boundary is materially different from later GitHub PR publication and therefore cannot be hidden under the same guarded yes/no decision.
- `S6` is the live GitHub object publication boundary: the final create body is rendered and `gh pr create` publishes the PR with title, body, labels, milestone, project, and draft state.
- `S7` is post-create cleanup and evidence finalization: worktree cleanup and local result serialization happen after publication, so failures here must be modeled as traceability defects after a real PR already exists, not as a no-op create path.
- `P0` therefore fixes the core decomposition outcome for `S0E-5C`: guarded `PR create` cannot be responsibly designed as one atomic mutation family; it must at least separate preflight checks, local materialization, remote branch publication, live PR publication, and post-create evidence handling.

## P1 (Reuse-vs-new-rule boundary | v1)

### P1-C1-S1 (Stage classes mapped to gate ownership | v1)

- The `P1` boundary map is now recorded in `docs/issues/pr-create-S0E-5C-p1-boundary-map.json`.
- The strongest `P1` conclusion is negative: no `PR create` stage can reuse the existing lifecycle pre-gate unchanged as a single all-purpose publish gate.
- `S1` and `S2` stay outside guarded apply because they are dry-run planning stages with no live mutation; they should remain prerequisite planning layers rather than be forced into mutation-gate semantics.
- `S3` is the only stage that can reuse the existing lifecycle pre-gate, and even here the reuse is partial: the current gate can answer whether the source issue is structurally ready for create-time continuation, but it cannot replace create-specific checks for selected commits, prepared-branch collisions, label/milestone existence, or preview-body integrity.
- `S4` and `S5` need new targeted rules instead of recycled lifecycle-gate semantics: local branch materialization and remote branch publication are git-state transitions that the current issue-lifecycle audit model does not observe.
- `S6` remains operator-held in v1 even though it will eventually need its own targeted publish rule if guarded rollout continues. The current conclusion is that live PR publication cannot inherit authorization from an earlier preflight decision after local and remote state have already changed.
- `S7` stays outside guarded apply because it is post-create traceability. A failure here means local evidence did not serialize after a real PR already exists; it is not part of the publish authorization boundary.
- `P1` therefore fixes the first stable guard-boundary rule for `S0E-5C`: reuse the existing lifecycle pre-gate only as one prerequisite layer for create-time preflight, and do not pretend that this reuse automatically covers branch materialization, remote publish, or live PR publication.

## P2 (Bounded front-half sample | v1)

### P2-C1-S1 (Pass and stop evidence recorded before local materialization | v1)

- `P2` records one bounded front-half drill around `S1-S3` only: dry-run plan input resolution, scope selection plus preview generation, and create-time preflight validation. The new entrypoint is `scripts/issues/plan_pr_create_preflight_with_gate.py`.
- The representative live sample is `S0E-5C` itself. Live issue `#309` was created from this log, written back into `links.issue`, and attached to parent issue `#248` so the existing lifecycle pre-gate could evaluate a structurally ready `issue-created` item.
- The pass path uses `docs/issues/lifecycle-audit-S0E-5C-p2-pass-manifest.json` plus `docs/issues/pr-prep-S0E-5C-p2-pass-manifest.json`. It proves that the existing lifecycle pre-gate can return `allow-apply` for the live issue while create-specific preflight also passes selected-commit checks, label existence, branch availability, and preview-body integrity.
- The stop path uses the same live issue-readiness gate input but swaps in `docs/issues/pr-prep-S0E-5C-p2-stop-manifest.json`, which deliberately reuses the occupied branch name `pr-prep/s0e-5b`. The result stops at `S3` with `preflight_decision = stop-before-local-materialization` even though the lifecycle pre-gate itself still allows continuation.
- `P2` therefore proves the exact front-half shape fixed by `P1`: the lifecycle pre-gate is only one prerequisite layer, and create-specific preflight must still retain authority to stop the flow before `S4` when branch/publication preconditions are not safe.

## Plan (draft)

## Plan (draft)

- `P3-C1-S1`: decide whether the bounded front-half result is strong enough to keep `S6` operator-held while exploring targeted rules only for `S4/S5`, or whether `S0E-5C` should stop without deeper guarded rollout

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: guarded `PR create` stage map fixed
- [x] `P1-C1-S1`: reuse-vs-new-rule boundary fixed
- [x] `P2-C1-S1`: representative decomposition sample recorded

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log will record stage maps, decomposition outputs, and any representative create-path samples once work begins.

### P0-C1-S1 (guarded PR create stage map fixed | 2026-03-30)

- artifacts:
  - `docs/issues/pr-create-S0E-5C-p0-stage-map.json`
  - `docs/issues/pr-prep-S0E-5B-real-manifest.json`
  - `docs/issues/pr-prep-S0E-5B-real-plan.json`
  - `docs/issues/pr-prep-S0E-5B-real-create-result.json`
  - `scripts/issues/plan_pr_prep.py`
  - `scripts/issues/create_pr_from_plan.py`
- expected:
  - `PR create` should be decomposed into explicit stages with clear stop boundaries instead of being treated as one opaque guarded mutation
  - the decomposition should show where the first local mutation occurs, where the first remote git write occurs, and where the first live GitHub PR object write occurs
- observed:
  - the current path resolves into seven concrete stages, and the resulting stage map shows three materially different mutation boundaries: local branch materialization, remote branch publication, and live PR publication
  - the same map also shows that post-create local evidence write-back occurs after publication, so it cannot be merged into the publish decision without losing traceability

### P1-C1-S1 (reuse-vs-new-rule boundary fixed | 2026-03-30)

- artifacts:
  - `docs/issues/pr-create-S0E-5C-p1-boundary-map.json`
  - `docs/issues/pr-create-S0E-5C-p0-stage-map.json`
  - `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  - `scripts/issues/plan_lifecycle_pre_gate.py`
  - `scripts/issues/plan_pr_prep.py`
  - `scripts/issues/create_pr_from_plan.py`
- expected:
  - the stage map should clearly state which `PR create` stages can reuse the existing lifecycle pre-gate, which require new targeted rules, and which should remain outside guarded apply in v1
  - the result should prevent the current guarded work from over-claiming that one issue-lifecycle gate can safely authorize the whole create path
- observed:
  - no stage can reuse the existing lifecycle pre-gate unchanged as one all-purpose `PR create` gate
  - only `S3` can reuse the existing pre-gate as an issue-readiness prerequisite, while `S4` and `S5` require new targeted rules and `S6` remains operator-held as the live PR publication boundary in v1

### P2-C1-S1 (bounded front-half pass and stop samples recorded | 2026-03-30)

- artifacts:
  - `scripts/issues/plan_pr_create_preflight_with_gate.py`
  - `docs/issues/issue-S0E-5C-guarded-pr-create-decomposition.md`
  - `docs/issues/issue-S0E-5C-guarded-pr-create-decomposition.json`
  - `docs/issues/issue-relationship-S0E-5C-p2-pass-manifest.json`
  - `docs/issues/issue-relationship-S0E-5C-p2-pass-manifest-plan.json`
  - `docs/issues/issue-relationship-S0E-5C-p2-pass-manifest-parent-248-child-309-apply-result.json`
  - `docs/issues/lifecycle-audit-S0E-5C-p2-pass-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-5C-p2-pass-plan.json`
  - `docs/issues/lifecycle-gate-S0E-5C-p2-pass-decision.json`
  - `docs/issues/pr-prep-S0E-5C-p2-pass-manifest.json`
  - `docs/issues/pr-prep-S0E-5C-p2-pass-plan.json`
  - `docs/issues/pr-prep-S0E-5C-p2-pass-body.md`
  - `docs/issues/pr-create-S0E-5C-p2-pass-front-half-preflight-result.json`
  - `docs/issues/lifecycle-gate-S0E-5C-p2-stop-decision.json`
  - `docs/issues/lifecycle-audit-S0E-5C-p2-stop-plan.json`
  - `docs/issues/pr-prep-S0E-5C-p2-stop-manifest.json`
  - `docs/issues/pr-prep-S0E-5C-p2-stop-plan.json`
  - `docs/issues/pr-prep-S0E-5C-p2-stop-body.md`
  - `docs/issues/pr-create-S0E-5C-p2-stop-front-half-preflight-result.json`
- expected:
  - the bounded front half should prove that `S1-S3` can emit a clean pass result and a clean stop result without mutating local branches or publishing any PR object
  - the stop sample should fail because of a create-specific preflight defect even when the reused lifecycle pre-gate still returns `allow-apply`
- observed:
  - the pass sample on live issue `#309` returned `gate_decision = allow-apply` and `preflight_decision = allow-front-half-preflight`, with all create-specific checks passing and the result explicitly stopping before `S4-local-branch-materialization`
  - the stop sample reused the same live issue-readiness gate result but failed `branch-availability` on occupied branch `pr-prep/s0e-5b`, producing `preflight_decision = stop-before-local-materialization` while still avoiding any branch materialization or PR publication

## Recent changes (for traceability, optional)

- 2026-03-30: created `S0E-5C` as the dedicated follow-up for guarded `PR create` decomposition after `S0E-5B` reached stable state on in-place guarded mutation families.
- 2026-03-30: completed `P0` by decomposing the current `PR create` path into seven explicit stages and fixing the failure boundaries between dry-run planning, local branch materialization, remote publish, live PR publication, and post-create evidence finalization.
- 2026-03-30: completed `P1` by mapping those seven stages onto reuse-vs-new-rule ownership, concluding that only create-time preflight can partially reuse the existing lifecycle pre-gate while local materialization, remote publish, and live PR publication must remain separate boundaries.
- 2026-03-30: created live issue `#309` for `S0E-5C`, attached it under parent issue `#248`, and wrote the issue link back to this source log as the representative live front-half sample anchor.
- 2026-03-30: completed `P2` by adding a bounded front-half preflight entrypoint, then recording one live pass sample and one create-specific stop sample that both stop before `S4-local-branch-materialization`.