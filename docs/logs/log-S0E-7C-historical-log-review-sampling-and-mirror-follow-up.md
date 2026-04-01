# log-S0E-7C (Phase 7C: historical log review sampling and mirror follow-up)

---

**id**: `S0E-7C`
**kind**: `log`
**title**: `workflow/historical log review sampling and mirror follow-up v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Actions, Automation, Workflow, Audit, Review, epic/s0, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md`
  **reference_log_1**: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  **reference_log_2**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  **reference_log_3**: `docs/logs/log-S0E-6B-log-stability-and-gate-strategy.md`
  **reference_log_4**: `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  **reference_log_5**: `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md`
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
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-01`
**updated**: `2026-04-01`

---

## Decision / Outcome

**Decision**:

- `S0E-7C` is now the dedicated follow-up slice for reviewing historical logs that never completed the full `issue -> PR -> merge -> conclusion` lifecycle under the current `S0E` contract.
- v1 separates `review` from `apply`: it plans and classifies historical logs, but it does not mutate GitHub issues, PRs, or source logs.
- The first execution surface should be manifest-driven and sample-first, so old logs can be audited in batches before any targeted backfill or guarded apply path is chosen.

**Default choices (phase defaults / v1)**:

- Historical review should classify each log into a bounded set of states such as `concluded`, `merged-open`, `issue-open-no-pr`, and `log-only` instead of asking operators to infer lifecycle gaps from prose.
- The review planner should also check a narrow set of log-structure contract surfaces already fixed by `S0E-6B`, especially required sections, `PR Summary Inputs`, `Evidence Footer Source`, and stable-status contradictions.
- GitHub Actions may mirror the same review planner through `workflow_dispatch`, but that mirror remains secondary: local review planning is still the primary owner.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.
- `Evidence Footer Source` does not replace `Evidence`: the footer source feeds PR/gate automation, while `Evidence` remains the human ledger.

**PR summary bullets**:

- Add one manifest-driven planner that reviews historical logs for both structure drift and lifecycle completeness.
- Validate several representative samples so old logs can be split into closed-loop, issue-open-no-pr, and log-only follow-up buckets before any apply path starts.
- Add one manual GitHub Actions mirror workflow that reruns the same review planner and retains structured audit artifacts without becoming the primary owner.
- Add one first full-series `S0E` batch manifest and retained review plan so the historical backlog is measured before live Actions replay starts.

**PR checklist source**:

- Default source: reuse this log's execution checklist after `P0` is reviewed.

**PR links**:

- Log: `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
- Issue: ``
- Runbook: ``
- Evidence artifact: `docs/issues/historical-log-review-S0E-series-plan.json`

**PR body notes**:

- Keep artifact detail in the human-facing `Evidence` section of the source log instead of rendering an `Evidence Footer` block for this workflow-oriented slice.
- Generated PR body should keep `Development Link` omitted unless a development issue is explicitly present.

## Definitions (optional)

- `historical log review`: a dry-run classification pass over old source logs that inspects current contract shape plus lifecycle completeness.
- `review-only follow-up`: a planner result that proposes the next targeted action without mutating GitHub or source logs.
- `mirror review`: a GitHub Actions replay of the same planner used locally, retaining summary and JSON artifacts for visibility.

## Constraints

- Do not turn `S0E-7C` into a bulk apply slice; v1 stops at review, classification, and retained evidence.
- Do not guess missing issue or PR links from prose-only hints; lifecycle classification must remain bounded by explicit structured links and live GitHub reads when available.
- Do not let GitHub Actions become the primary owner of historical review decisions; it may mirror and surface results only.

## Scope

- `P0`: fix the ownership boundary for historical log review versus later backfill/apply work
- `P1`: implement a manifest-driven historical log review planner
- `P2`: validate representative samples across several old-log lifecycle states
- `P3`: add a manual GitHub Actions mirror workflow for the same review planner
- `P4`: establish the first full-series `S0E` backlog baseline and then use it to enable one real mirror replay path

## Success Criteria (DoD)

- The repo has one planner that reads an explicit manifest and emits per-log lifecycle classification plus structure-review findings.
- At least one representative sample proves the planner can distinguish a fully concluded log, an issue-open-no-pr log, and a log with no issue/PR links yet.
- The repo has one manual GitHub Actions mirror workflow that reruns the same planner and retains summary plus JSON artifacts.
- The repo has one explicit full-series `S0E` manifest and retained plan artifact that quantifies the historical backlog before any live mirror replay is attempted.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the ownership boundary, review planner, representative samples, and manual mirror workflow
  - the Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## Current Status

- `S0E-7C` is now opened as the dedicated review-first follow-up for historical logs that never completed the current issue-flow contract.
- `P0` is now completed: review-only ownership is explicitly separated from later targeted backfill/apply mutation families.
- `P1` is now completed: the repo now has `scripts/issues/plan_historical_log_review.py`, which classifies historical logs by lifecycle completeness and narrow contract drift.
- `P2` is now completed: the repo now has one representative sample manifest and retained plan covering a closed-loop log, an issue-open-no-pr log, and a log-only sample.
- `P3` is now completed: the repo now has a manual `workflow_dispatch` mirror workflow that reruns the same planner and uploads retained review artifacts.
- `P4-C1-S1` is now completed: the repo now has one explicit full-series `S0E` manifest and retained review plan that measures the current historical backlog before live Actions replay is attempted.

## P0 (Boundary contract | v1)

### P0-C1-S1 (Review-versus-apply boundary fixed | v1)

- `S0E-7C` owns review and classification only: it decides what kind of lifecycle gap a historical log currently has and what targeted next action should be considered.
- Any later mutation such as issue creation, PR creation, PR-body rewrite, relationship attach, or issue conclusion stays with the existing apply families instead of being absorbed into this slice.

### P0-C1-S2 (Local-first / mirror-later execution policy fixed | v1)

- The primary execution surface for historical log review remains local and manifest-driven.
- GitHub Actions may mirror the same review planner through a manual dispatch workflow, but the workflow should surface retained evidence rather than become the first owner of truth.

## P1 (Historical log review planner | v1)

### P1-C1-S1 (Manifest-driven review entrypoint implemented | v1)

- `scripts/issues/plan_historical_log_review.py` now accepts one explicit manifest of source logs and emits one structured review plan JSON.
- Each item is classified from structured links and live GitHub reads when available, with bounded lifecycle states such as `concluded`, `merged-open`, `issue-open-no-pr`, `pr-open`, and `log-only`.

### P1-C1-S2 (Narrow structure review contract implemented | v1)

- The planner now checks a small deterministic set of log surfaces before treating a historical log as clean enough for downstream automation:
  - required frontmatter fields;
  - required contract sections;
  - `PR Summary Inputs` presence;
  - `Evidence Footer Source` row shape;
  - placeholder hygiene and `stable` versus unchecked-checklist contradiction.
- This keeps historical review aligned with `S0E-6B` without widening into prose linting.

## P2 (Representative samples | v1)

### P2-C1-S1 (Representative sample manifest fixed | v1)

- `docs/issues/historical-log-review-S0E-7C-sample-manifest.json` now fixes one explicit sample set for historical review.
- The first sample set intentionally spans three review buckets:
  - one closed-loop sample;
  - one issue-open-no-pr sample;
  - one log-only sample with no issue/PR links yet.

### P2-C1-S2 (Representative sample plan retained | v1)

- `docs/issues/historical-log-review-S0E-7C-sample-plan.json` now records the review planner output for the representative sample set.
- The retained plan makes the next targeted action explicit per log rather than leaving operators to rediscover the lifecycle gap manually.

## P3 (GitHub Actions mirror workflow | v1)

### P3-C1-S1 (Manual dispatch mirror workflow added | v1)

- `.github/workflows/s0e-historical-log-review-mirror.yml` now reruns the same historical log review planner from `workflow_dispatch`.
- The workflow accepts an explicit manifest path and optional repo override, mirroring the local planner interface instead of inventing a second contract.

### P3-C1-S2 (Retained mirror artifacts and fail policy fixed | v1)

- The workflow now retains the input manifest, planner console output, structured plan JSON, and one workflow summary markdown.
- By default the workflow stays advisory and does not fail on `review-required` findings; operators may opt into failing on findings explicitly.

## P4 (Full-series backlog baseline and live mirror enablement | v1)

### P4-C1-S1 (Full-series `S0E` historical review baseline retained | v1)

- `docs/issues/historical-log-review-S0E-series-manifest.json` now fixes one explicit full-series `S0E` batch review input spanning the current child logs under the spine.
- `docs/issues/historical-log-review-S0E-series-plan.json` now retains the first full-series backlog reading so review-required items, pass-review items, and lifecycle-complete items are measured before any live mirror replay.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-7C/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0E-7C/P0-P3: historical log review sampling and mirror follow-up`
  - discontinuous phases: `S0E-7C/P0+P3: historical log review sampling and mirror follow-up`
  - mixed discontinuous + consecutive phases: `S0E-7C/P0+P2-P3: historical log review sampling and mirror follow-up`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `S0E-7C/P*-C*-S*: <one-sentence summary>`.

**Branch convention**:

- `S0E-7C` changes should usually stay on the existing `S0E-*` working branch because this slice is still part of the docs-management / GitHub automation spine.

## Plan (draft)

### P1 (Historical log review planner)

- [x] `P1-C1-S1`: implement the manifest-driven historical log review entrypoint
- [x] `P1-C1-S2`: define and validate the narrow structure-review contract surfaces

### P2 (Representative samples)

- [x] `P2-C1-S1`: fix a representative sample manifest for several old-log states
- [x] `P2-C1-S2`: retain one representative review plan artifact

### P3 (GitHub Actions mirror workflow)

- [x] `P3-C1-S1`: add one manual dispatch mirror workflow for historical log review
- [x] `P3-C1-S2`: retain summary and artifact output without making CI the primary owner

### P4 (Full-series backlog baseline and live mirror enablement)

- [x] `P4-C1-S1`: retain one explicit full-series `S0E` manifest and backlog plan artifact
- [ ] `P4-C1-S2`: land the mirror workflow on the default branch and record the first live replay evidence

## Execution Checklist (unchecked)

### P0 (Boundary contract)

- [x] `P0-C1-S1`: review-versus-apply boundary fixed
- [x] `P0-C1-S2`: local-first / mirror-later execution policy fixed

### P1 (Historical log review planner)

- [x] `P1-C1-S1`: manifest-driven historical log review entrypoint implemented
- [x] `P1-C1-S2`: narrow structure-review contract implemented

### P2 (Representative samples)

- [x] `P2-C1-S1`: representative sample manifest fixed
- [x] `P2-C1-S2`: representative sample plan retained

### P3 (GitHub Actions mirror workflow)

- [x] `P3-C1-S1`: manual dispatch mirror workflow added
- [x] `P3-C1-S2`: retained artifact and advisory fail policy fixed

### P4 (Full-series backlog baseline and live mirror enablement)

- [x] `P4-C1-S1`: full-series `S0E` manifest and backlog plan retained
- [ ] `P4-C1-S2`: first live mirror replay path enabled and evidenced

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.

### P0-C1-S1S2 (review boundary and mirror policy fixed | 2026-04-01)

- headSha: `e8a40025`
- artifacts:
  - `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
  - `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  - `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  - `docs/logs/log-S0E-6B-log-stability-and-gate-strategy.md`
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
- expected:
  - the repo should separate historical review planning from later targeted apply families, while keeping any GitHub Actions replay as a secondary mirror only

### P4-C1-S1 (full-series `S0E` backlog baseline retained | 2026-04-01)

- headSha: `cc48a05c`
- artifacts:
  - `docs/issues/historical-log-review-S0E-series-manifest.json`
  - `docs/issues/historical-log-review-S0E-series-plan.json`
- expected:
  - the repo should retain one explicit full-series `S0E` backlog measurement before any live historical-review mirror run is attempted
- observed:
  - `S0E-7C` now fixes that split directly: v1 review is manifest-driven and non-mutating, while later backfill or guarded apply remains outside this slice

### P1-C1-S1S2 (historical log review planner implemented | 2026-04-01)

- headSha: `e8a40025`
- artifacts:
  - `scripts/issues/plan_historical_log_review.py`
  - `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
  - `docs/logs/log-S0E-6B-log-stability-and-gate-strategy.md`
- expected:
  - the repo should gain one planner that reads an explicit manifest, checks narrow log-structure surfaces, and classifies lifecycle completeness from structured links plus live GitHub state when available
- observed:
  - the new planner now emits per-log lifecycle states, planned follow-up actions, and bounded structure-review findings in one machine-readable JSON plan

### P2-C1-S1S2 (representative historical review samples retained | 2026-04-01)

- headSha: `e8a40025`
- artifacts:
  - `docs/issues/historical-log-review-S0E-7C-sample-manifest.json`
  - `docs/issues/historical-log-review-S0E-7C-sample-plan.json`
- expected:
  - the repo should retain one representative review sample that distinguishes fully concluded, issue-open-no-pr, and log-only historical logs without mutating GitHub
- observed:
  - the retained sample manifest and plan now record one closed-loop sample, one issue-open-no-pr sample, and one log-only sample with explicit next-step classification

### P3-C1-S1S2 (manual mirror workflow added | 2026-04-01)

- headSha: `e8a40025`
- artifacts:
  - `.github/workflows/s0e-historical-log-review-mirror.yml`
  - `scripts/issues/plan_historical_log_review.py`
  - `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
- expected:
  - GitHub Actions should be able to rerun the same historical review planner through a manual dispatch path, retain artifacts, and remain advisory by default rather than primary
- observed:
  - the new workflow now mirrors the planner from `workflow_dispatch`, uploads the manifest/console/plan/summary artifacts, and only fails on findings when the operator opts into that behavior

## Recent changes (for traceability, optional)

- 2026-04-01: opened `S0E-7C` as the review-first follow-up for historical logs that never completed the current `S0E` issue-flow contract.
- 2026-04-01: completed `P1` by adding `scripts/issues/plan_historical_log_review.py`, which classifies lifecycle completeness and narrow structure drift from an explicit manifest.
- 2026-04-01: completed `P2` by retaining a representative sample manifest and plan spanning closed-loop, issue-open-no-pr, and log-only historical logs.
- 2026-04-01: completed `P3` by adding `.github/workflows/s0e-historical-log-review-mirror.yml` as a manual mirror for the same planner.