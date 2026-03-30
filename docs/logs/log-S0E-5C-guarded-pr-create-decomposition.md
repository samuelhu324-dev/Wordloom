# log-S0E-5C (Phase 5C: Guarded PR Create Decomposition)

---

**id**: `S0E-5C`
**kind**: `log`
**title**: `guarded PR create decomposition v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, PR, Automation, Drills, Evidence, epic/s0, sub/0e5c`
**links**: ``
  **issue**: ``
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
**pr_development_issue**: ``
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

## P0 (PR create stage map | v1)

### P0-C1-S1 (Stage decomposition and failure boundaries fixed | v1)

- The current `PR create` implementation is now decomposed into seven stages across the existing `plan_pr_prep.py` and `create_pr_from_plan.py` path, with the stage map recorded in `docs/issues/pr-create-S0E-5C-p0-stage-map.json`.
- `S1-S3` are pre-publication stages: dry-run input resolution, exact-ID scope selection plus preview generation, and create-time preflight validation. These stages must fail before any local branch mutation, remote push, or live PR publication occurs.
- `S4` is the first local mutation boundary: an isolated worktree and prepared branch are materialized, selected commits are cherry-picked, and snapshot fallback may rebuild the branch from the source-head snapshot when cherry-pick conflicts occur.
- `S5` is the first irreversible remote git write: the prepared branch is pushed to `origin`. This boundary is materially different from later GitHub PR publication and therefore cannot be hidden under the same guarded yes/no decision.
- `S6` is the live GitHub object publication boundary: the final create body is rendered and `gh pr create` publishes the PR with title, body, labels, milestone, project, and draft state.
- `S7` is post-create cleanup and evidence finalization: worktree cleanup and local result serialization happen after publication, so failures here must be modeled as traceability defects after a real PR already exists, not as a no-op create path.
- `P0` therefore fixes the core decomposition outcome for `S0E-5C`: guarded `PR create` cannot be responsibly designed as one atomic mutation family; it must at least separate preflight checks, local materialization, remote branch publication, live PR publication, and post-create evidence handling.

## Plan (draft)

- `P1-C1-S1`: map those stages against existing lifecycle pre-gate semantics and identify where extra targeted rules would be required
- `P2-C1-S1`: run one representative sample through the decomposed path without yet claiming full guarded rollout

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: guarded `PR create` stage map fixed
- [ ] `P1-C1-S1`: reuse-vs-new-rule boundary fixed
- [ ] `P2-C1-S1`: representative decomposition sample recorded

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

## Recent changes (for traceability, optional)

- 2026-03-30: created `S0E-5C` as the dedicated follow-up for guarded `PR create` decomposition after `S0E-5B` reached stable state on in-place guarded mutation families.
- 2026-03-30: completed `P0` by decomposing the current `PR create` path into seven explicit stages and fixing the failure boundaries between dry-run planning, local branch materialization, remote publish, live PR publication, and post-create evidence finalization.