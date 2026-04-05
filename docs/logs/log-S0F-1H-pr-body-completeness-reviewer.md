# log-S0F-1H (Phase 1H: PR body completeness reviewer)

---

**id**: `S0F-1H`
**kind**: `log`
**title**: `PR body completeness reviewer v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Automation, Audit, Contract, Review, epic/s0, sub/1h`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
  **reference_log_1**: `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`
  **reference_log_2**: `docs/logs/log-S0F-1F-bucketed-audit-output-materialization.md`
  **reference_log_3**: `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
**issue_keyword**: `audit`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-05`
**updated**: `2026-04-05`

---

## Decision / Outcome

**Decision**:

- `S0F-1H` is the next `S0F` follow-up slice, and it packages one read-only PR body completeness reviewer that rebuilds the canonical expected PR body from the source log before comparing that output against the live GitHub PR body.
- v1 should separate three states explicitly instead of treating every byte-level mismatch as the same class of problem: exact match, formatting-only drift, and substantive drift after normalization.
- The reviewer must stay fail-closed on missing ownership inputs. If a source log leaves `links.pr` blank, `S0F-1H` should stop and report that ownership gap rather than guessing which live PR to review.
- The first target is review standardization, not live repair. `S0F-1H` should tell reviewers whether a PR body is complete, formatting-noisy, or unresolved because source-log ownership is incomplete.

**Default choices (phase defaults / v1)**:

- The source log remains the canonical owner of expected PR body scope.
- Expected-body rebuild should reuse the existing PR body rewrite contract instead of introducing a second summary or checklist renderer.
- Normalization should stay narrow and structural: line-ending and trailing-whitespace cleanup plus blank-line collapse are allowed, but semantic row differences must still surface as substantive drift.
- Missing `links.pr` is a review stop condition, not a silent skip, because the source log otherwise fails to name the canonical live PR under review.
- The first rollout stays read-only and artifact-first so later policy or CI use can depend on a retained review bundle before any enforcement is widened.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Add one read-only reviewer that rebuilds canonical expected PR bodies from source logs and compares them against live GitHub PR bodies.
- Separate exact matches, formatting-only drift, and substantive drift so blank-line noise no longer masks real completeness gaps.
- Retain one `S0F` sample review bundle that also reports stop conditions when source logs still omit canonical `links.pr` ownership.

**PR checklist source**:

- Default source: reuse this log's execution checklist for generated PR checklist blocks.

**PR links**:

- Log: `docs/logs/log-S0F-1H-pr-body-completeness-reviewer.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`

## Definitions (optional)

- `exact match`: the live PR body matches the source-log-derived expected body byte-for-byte.
- `formatting-only drift`: the live PR body differs byte-for-byte, but matches after narrow whitespace and blank-line normalization.
- `substantive drift`: the live PR body still differs from the source-log-derived expected body after normalization.
- `review stop`: the reviewer cannot resolve a canonical live PR because the source log does not provide deterministic PR ownership input such as `links.pr`.

## Constraints

- Do not guess a live PR when the source log leaves `links.pr` blank.
- Do not widen normalization until substantive checklist, metadata, links, or footer drift could be hidden by it.
- Do not introduce a second expected-body renderer that can drift from the canonical rewrite surface.
- Do not mix this slice with live PR body mutation or PR-link write-back repair.

## Scope

- `P0`: create `S0F-1H`, wire it into the `S0F` spine, and fix the reviewer boundary
- `P1`: add the read-only expected-body rebuild plus normalized-diff reviewer
- `P2`: retain one `S0F` sample review bundle and classify exact, formatting-only, and stop states
- `P3`: package the operator-facing review standard and retained artifact surface

## Success Criteria (DoD)

- Reviewers can distinguish exact match, formatting-only drift, and substantive drift without manually rebuilding expected PR bodies.
- The reviewer stops explicitly on missing canonical PR ownership input instead of guessing the live PR.
- At least one retained result bundle proves the reviewer can classify a real `S0F` set.
- The retained output is read-only and can be reused later for standard review or CI policy if needed.

## Stability (what stable means)

- This log can be marked `stable` when:
  - one canonical read-only reviewer exists and reuses the existing expected-body rewrite contract;
  - one retained sample bundle proves formatting-only drift can be separated from substantive drift;
  - unresolved source-log ownership gaps are reported explicitly as stop states instead of being hidden as silent skips.

## Current Status

- `S0F-1H` is now opened as the next `S0F` follow-up slice for standardizing PR body completeness review around the source log as canonical ownership.
- `P0` is now complete: `S0F-1H` is wired into the spine, the reviewer boundary is fixed as read-only, and the next follow-up is `P1` canonical expected-body rebuild plus normalized comparison.
- `P1` is now complete: `scripts/issues/review_pr_body_completeness.py` rebuilds the canonical expected PR body from each source log by reusing `rewrite_pr_body_scope_from_log.py`, validates the live PR body contract, and classifies exact versus normalized drift without mutating GitHub state.
- `P2` is now complete: `artifacts/s0f-1h-pr-body-completeness-review-s0f.json` retains one live `S0F` sample bundle showing `S0F-1F` as an exact match, `S0F-1A` as formatting-only drift, and no substantive drift in the currently reviewable set.
- The same retained bundle also makes the remaining ownership blocker explicit instead of hiding it: `S0F-1B`, `S0F-1C`, `S0F-1D`, `S0F-1E`, and `S0F-1G` all stop under `stop-missing-pr-link` because their source logs still leave `links.pr` blank.
- `P3` is now complete: the reviewer now retains live-body, expected-body, and diff artifacts under `artifacts/s0f-1h-pr-body-completeness-review-s0f-files/`, and `S0F-1H` is stable as the read-only review standard for this lane.

## P3 Operator Review Packaging (completed)

- `S0F-1H` now packages PR body completeness review as one operator-facing retained artifact surface instead of leaving it as an ad hoc shell snippet.
- v1 keeps that package intentionally narrow: it is read-only, source-log-owned, and explicit about unresolved `links.pr` ownership gaps.

### P3-C1-S1 (Retained reviewer artifact surface fixed | v1)

- `artifacts/s0f-1h-pr-body-completeness-review-s0f.json` now retains the per-item review result set for the current `S0F` sample run.
- `artifacts/s0f-1h-pr-body-completeness-review-s0f-files/` now retains the fetched live PR bodies, rebuilt expected bodies, and raw diff output needed to inspect any non-exact result without rerunning the reviewer first.
- The retained `S0F-1A` raw diff confirms the current normalized-only drift boundary is appropriately narrow: the observed delta is blank-line noise only, not a missing checklist, summary, link, or footer row.

## P2 Sample Review Classification (completed)

- `S0F-1H` now proves the review taxonomy on a real `S0F` set instead of only describing it in prose.
- v1 keeps the sample small but meaningful: it includes one exact match, one formatting-only drift case, and one stop-state family caused by missing canonical PR ownership in source logs.

### P2-C1-S1 (Exact, formatting-only, and stop-state classification retained on one live sample set | v1)

- The retained `S0F` review bundle now classifies `S0F-1F/#375` as `exact-match`, proving the earlier merged-PR body repair has converged to the source-log-owned expected body exactly.
- The same bundle classifies `S0F-1A/#365` as `formatting-only-drift`, proving byte-level mismatch can now be downgraded safely when normalization removes the observed noise.
- The same bundle records zero `substantive-drift` items in the currently reviewable `S0F` set.

### P2-C1-S2 (Missing source-log PR ownership now reports as an explicit review stop | v1)

- The retained sample now reports `S0F-1B`, `S0F-1C`, `S0F-1D`, `S0F-1E`, and `S0F-1G` as `stop-missing-pr-link` because their canonical source logs still do not write back `links.pr`.
- This keeps the review surface honest: those items are no longer silently omitted from the sweep, but they are also not guessed from live GitHub search heuristics.
- The remaining follow-up for those items belongs outside this slice: source-log PR-link write-back must converge before the reviewer can evaluate those PR bodies canonically.

## P1 Read-Only Reviewer Implementation (completed)

- `S0F-1H` now lands the first dedicated read-only reviewer for PR body completeness under the existing docs/GitHub lifecycle tooling family.
- v1 deliberately composes existing stable surfaces instead of reimplementing them: it fetches the live PR body, rebuilds the expected body through the canonical rewrite entrypoint, validates the live contract, and then classifies drift.

### P1-C1-S1 (Canonical expected-body rebuild reused for review | v1)

- `scripts/issues/review_pr_body_completeness.py` now scans phase-style source logs by requested-ID prefix, fetches the canonical live PR body named by each log's `links.pr`, and rebuilds the expected body by reusing `rewrite_pr_body_scope_from_log.py`.
- This keeps review ownership single-sourced: summary, checklist, links, and closing-footer expectations are still derived by the same rewrite logic already used for bounded PR body repair work.
- The same reviewer also validates the live PR body against `body_contract.py`, so result bundles retain both semantic completeness classification and canonical contract status for each reviewed PR.

### P1-C1-S2 (Normalized comparison boundary fixed without hiding semantic drift | v1)

- The reviewer now performs two comparisons per item: a raw byte-level comparison and a normalized comparison that strips trailing whitespace, normalizes line endings, trims outer blank space, and collapses blank-line runs.
- A PR body therefore classifies as `formatting-only-drift` only when the normalized forms match exactly; any surviving row or content difference remains a `substantive-drift` item.
- The reviewer also stops explicitly when `links.pr` is blank or invalid, so normalization never becomes an excuse for reviewing the wrong live PR.

## P0 Reviewer Boundary and Spine Wiring (completed)

- `S0F-1H` now owns the read-only PR body completeness review lane under the `S0F` spine instead of leaving that review standard as an implicit operator habit.
- v1 fixes the boundary deliberately: this slice reviews live PR bodies against source-log-owned expected bodies, but it does not mutate GitHub state and it does not backfill missing `links.pr` metadata.

### P0-C1-S1 (Spine wiring fixed | v1)

- `S0F-1H` is now the canonical `S0F` follow-up for standardizing read-only PR body completeness review after `S0F-1G` stabilized issue identity governance.
- The parent `S0F` spine now points to `S0F-1H` explicitly and records it as the next follow-up slice after `S0F-1G`.

### P0-C1-S2 (Read-only reviewer boundary fixed | v1)

- `S0F-1H` fixes the ownership split clearly: this slice reviews canonical PR body completeness, while any future `links.pr` write-back repair remains a separate follow-up.
- The first stable stop taxonomy is also explicit here: unresolved source-log PR ownership is a review finding in its own right rather than a reason to guess or silently skip a live PR.

## Plan (draft)

### P0 (Reviewer boundary and spine wiring)

- P0-C1-S1: create `S0F-1H` and wire it into the `S0F` parent spine as the next follow-up slice
- P0-C1-S2: fix the review boundary as read-only canonical PR body completeness

### P1 (Read-only reviewer implementation)

- P1-C1-S1: rebuild expected PR bodies from source logs through the canonical rewrite surface
- P1-C1-S2: classify raw versus normalized drift without hiding substantive differences

### P2 (Sample result retention)

- P2-C1-S1: retain one real `S0F` sample review bundle with exact, formatting-only, and zero-substantive findings states
- P2-C1-S2: retain explicit stop-state reporting for missing `links.pr` ownership gaps

### P3 (Operator packaging)

- P3-C1-S1: retain reviewer output files and diff artifacts as the operator-facing review surface

## Execution Checklist (unchecked)

### P0 (Reviewer boundary and spine wiring)

- [x] `P0-C1-S1`: `S0F-1H` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: read-only reviewer boundary fixed

### P1 (Read-only reviewer implementation)

- [x] `P1-C1-S1`: canonical expected-body rebuild reused for review
- [x] `P1-C1-S2`: normalized comparison boundary fixed without hiding semantic drift

### P2 (Sample result retention)

- [x] `P2-C1-S1`: real `S0F` sample review bundle retained
- [x] `P2-C1-S2`: explicit stop-state reporting retained for missing `links.pr`

### P3 (Operator packaging)

- [x] `P3-C1-S1`: reviewer output files and diff artifacts retained

## Notes (optional)

- `S0F-1H` intentionally stops short of any live repair path. If a reviewer surfaces substantive drift later, that repair should still go through the existing bounded PR body rewrite surfaces rather than through this reviewer.
- The current `S0F` run proves the standard is useful even before PR-link write-back converges everywhere: it can already separate the one exact PR body from the one formatting-only body while naming the unresolved ownership gaps explicitly.

## Evidence

- `scripts/issues/review_pr_body_completeness.py` now provides the dedicated read-only reviewer surface for this slice.
- `scripts/issues/rewrite_pr_body_scope_from_log.py` remains the canonical expected-body rebuild surface reused by the reviewer instead of duplicated logic.
- `artifacts/s0f-1h-pr-body-completeness-review-s0f.json` retains the current `S0F` sample review bundle with exact, formatting-only, and stop-state classifications.
- `artifacts/s0f-1h-pr-body-completeness-review-s0f-files/s0f-1f-live-body.md` and `artifacts/s0f-1h-pr-body-completeness-review-s0f-files/s0f-1f-expected-body.md` prove the `S0F-1F/#375` exact-match state directly.
- `artifacts/s0f-1h-pr-body-completeness-review-s0f-files/s0f-1a-raw.diff` proves the `S0F-1A/#365` mismatch is currently formatting-only rather than substantive.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-1H/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
