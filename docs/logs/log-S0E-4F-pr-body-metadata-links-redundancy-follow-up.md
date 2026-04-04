# log-S0E-4F (Phase 4F: PR body metadata-links redundancy follow-up)

---

**id**: `S0E-4F`
**kind**: `log`
**title**: `PR body metadata-links redundancy follow-up v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, PR, Automation, Contract, Formatting, epic/s0, sub/1`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/327`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/329`
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-6F-issue-body-metadata-links-boundary-follow-up.md`
  **reference_log_1**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
  **reference_log_3**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  **reference_log_4**: `docs/logs/log-S0E-6F-issue-body-metadata-links-boundary-follow-up.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: `road-002-projection-runtime-platformization-and-evidence-governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: `M5-P1`
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-02`
**updated**: `2026-04-03`

---

## Decision / Outcome

**Decision**:

- `S0E-4F` exists because the current PR body still carries two user-facing redundancies after the newer issue-body and PR-body contracts stabilized.
- The first redundancy is `Development Link`: the PR body still renders a dedicated `Development Link` section even though `Metadata` already records the development issue.
- The second redundancy is `Issue` inside `Links`: the PR body still renders an `Issue` link row even though `Metadata` already records the development issue.
- This slice narrows the PR body contract so those duplicate surfaces are removed rather than restated in two sections.
- The same slice also owns the historical review decision for the current `S0E` PR family so the repo can determine which live PRs need rewrite under the new boundary instead of silently leaving mixed old/new PR body shapes in place.

**Default choices (phase defaults / v1)**:

- `Metadata` remains the single user-facing owner for development-issue identity in PR bodies.
- The dedicated `Development Link` section should be removed from the canonical PR body family.
- `Links` should keep deterministic navigation rows only, so `Issue` should be removed from canonical PR `Links` because it duplicates development-issue identity already carried in `Metadata`.
- `Log`, `Runbook`, `Evidence artifact`, `Parent log`, and optional `Roadmap` remain valid PR-link categories when the source log declares them.
- Historical `S0E` PR review should use one explicit bounded inventory rather than ad hoc spot checks.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Remove the redundant `Development Link` section from canonical PR bodies because development issue identity already lives in `Metadata`.
- Remove the redundant `Issue` row from PR `Links` so `Links` returns to deterministic navigation only.
- Audit the full current `S0E` PR family and decide which live PR bodies require rewrite under the narrowed PR contract.

**PR checklist source**:

- Default source: reuse this log's checked execution checklist once the PR-body contract change, live PR review inventory, and any bounded remediation plan are all complete.

**PR links**:

- Log: `docs/logs/log-S0E-4F-pr-body-metadata-links-redundancy-follow-up.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`

## Constraints

- Do not merge `Metadata` and `Links`; this slice narrows duplicated rows, not the full PR body family.
- Do not move `Metadata`, `Summary`, `Execution Checklist`, or `Links`; section order remains owned by the existing PR body contract.
- Do not remove `Development issue` from `Metadata`; this slice only removes duplicated development-issue surfaces elsewhere in the body.
- Do not widen `Links` into a catch-all section for identity rows or review prose.
- Do not silently rewrite historical PR bodies without an explicit review inventory and remediation decision.

## Scope

- `P0`: define the narrower PR-body ownership boundary for development-issue identity versus deterministic links
- `P1`: align canonical spec, gate surfaces, and renderer wording to the new PR-body boundary
- `P2`: review the current `S0E` PR inventory and decide which live PR bodies need rewrite
- `P3`: execute the bounded live PR rewrite batch and re-verify the full audited set
- `P4`: close the remaining GitHub metadata completeness gap for live PR Development/labels and backfill missing historical issues where the source log had never been written back
- `P5`: repair footer-scope convergence so PR titles, checklist selection, and Evidence Footer all describe the same merge-content scope in both preview and live rewrite paths

## Success Criteria (DoD)

- Canonical PR bodies stop rendering the dedicated `Development Link` section.
- Canonical PR `Links` stop rendering the `Issue` row.
- `Metadata` remains the single user-facing owner for development-issue identity in PR bodies.
- PR hard-gate/body-contract checks describe the same narrower boundary as the canonical spec.
- The full current `S0E` PR set is reviewed through one explicit inventory, with any needed live rewrite scope made explicit.
- The bounded live rewrite batch is applied successfully and the same `17` audited PRs re-verify as pass under the narrowed contract.
- The same `17` live `S0E` PRs all expose GitHub-recognized Development linkage and deterministic labels, not just canonical body text.
- Historical audited logs that previously lacked any issue write-back now have explicit GitHub issues, source-log `links.issue` write-back, and closed issue-conclusion bodies.
- Follow-up scope rewrites stop over-showing Evidence Footer rows when a PR title narrows review scope to a phase span or exact `P-C-S` unit.
- The affected live PRs `#320`, `#321`, and `#323` are rewritten so their footer rows match the same merge-content scope already used by the title and Execution Checklist.

## Stability (what draft means now)

- This log can be marked `stable` when:
  - the PR-body ownership boundary is fixed in `S0E-4A`, `S0E-4B`, and the shared body-contract owner surfaces;
  - representative PR body generation and validation prove the narrower contract locally;
  - the current `S0E` PR inventory has been reviewed and any chosen live rewrite scope has been explicitly recorded.

- `S0E-4F` is now `stable` because `P0-P2` are complete: the contract/gate/renderers are aligned locally, the full current `17`-PR `S0E` inventory has been audited, and the bounded rewrite scope is now fixed explicitly.

## Current Status

- `S0E-4F` has now completed `P0-P1` locally across the shared PR body contract, preview/create renderers, rewrite path, owner specs, and log templates.
- The canonical PR body family now keeps development issue identity only in `Metadata` and no longer renders `Development Link` or `Links -> Issue`.
- `P2` has now audited the full current `17` live `S0E` PR set: `#249`, `#287`, `#290`, `#291`, `#292`, `#294`, `#296`, `#298`, `#299`, `#301`, `#302`, `#304`, `#306`, `#308`, `#310`, `#311`, `#312`.
- The live audit result is `17/17 fail` against the narrowed PR body contract, so this slice no longer has any ambiguity about whether remediation is needed.
- The rewrite scope was fixed as one explicit bounded batch over all `17` audited PRs, grouped by drift family instead of left as ad hoc future spot-fixes.
- `P3` has now completed the live rewrite rollout itself: all `17` audited PRs were rewritten in bounded batches, and post-apply verification now returns `17/17 pass`.
- This rollout required multiple cycles rather than one monolithic apply step: one unblocking cycle for parser/source-log cleanup, one lower-risk metadata-links-only rewrite batch, one heavier canonical rebuild batch, and one final post-apply verify cycle.
- `P4` has now closed the remaining GitHub metadata gap: all `17` audited live `S0E` PRs now expose GitHub-recognized Development linkage through explicit close-link footer lines, all deterministic PR labels are present live, and the previously issue-less logs `S0E-1A`, `S0E-2C`, `S0E-3A`, and `S0E-7C` now have written-back GitHub issues that were concluded and closed.
- `P5` is now complete: the shared PR-prep preview path and the live PR rewrite path both filter `Evidence Footer` through the same title-derived scope selector that already owns `Execution Checklist`, and the affected live PRs `#320`, `#321`, and `#323` have been rewritten to that converged scope.
- The latest full-auto live cycle is now closed end to end on the live path: issue `#327` was created, remediated to pass lifecycle gates, carried by merged PR `#329`, and then updated in place with the final issue-conclusion body.
- Exact-ID merged PR selection for `S0E-4F` resolves to one-item set `#329`, and live issue `#327` now remains in `CLOSED` state with final DoD short ref `#329`.

## P0 (PR-body ownership boundary | v1)

### P0-C1-S1 (Development issue identity lives only in Metadata | v1)

- `Metadata` keeps the development-issue identity row.
- The dedicated `Development Link` section is removed from the canonical PR body family.
- The same ownership rule should apply to both PR preview generation and any historical PR-body rewrite path.

### P0-C1-S2 (Links keep deterministic navigation only | v1)

- PR `Links` keep deterministic navigation rows such as `Log`, `Runbook`, `Evidence artifact`, `Parent log`, and optional `Roadmap`.
- `Issue` is removed from the canonical PR `Links` section because it duplicates development-issue identity already present in `Metadata`.
- Link omission stays fail-closed: blank optional rows must still be omitted rather than guessed.

### P0-C1-S3 (Historical PR review scope stays explicit | v1)

- This slice reviews the current live `S0E` PR family as one explicit set.
- The initial review inventory is:
  - `#249` `S0E-1A/P0-P2: structured cv generator`
  - `#287` `S0E-2A/P0-P3: semi-automated Git issue creation contract v1`
  - `#290` `S0E-2B/P0-P3: real GitHub issue creation automation v1`
  - `#291` `S0E-2C/ P0-P3: batch issue creation and backfill tooling`
  - `#292` `S0E-3A/P0-P3: roadmap milestone log bridge`
  - `#294` `S0E-4A/P0-P3: GitHub pull request automation contract v1`
  - `#296` `S0E-4B/P0-P3: PR title compression, structural label inheritance, and body scope alignment follow-up v1`
  - `#298` `S0E-2D/P0-P3: issue creation metadata enrichment and English body contract v1`
  - `#299` `S0E-4A/P3-C2-S1S2: derive development issue fallback and multi-issue formatting`
  - `#301` `S0E-4C/P0-P4: PR summary, development-link rendering, and issue relationship follow-up v1`
  - `#302` `S0E-4C/P5-C1-S1: harden create-path cherry-pick fallback`
  - `#304` `S0E-4D/P0-P2: review-hold, full-auto, and lifecycle orchestration follow-up v1`
  - `#306` `S0E-5A/P0-P5: lifecycle audit gate and dry-run planner v1`
  - `#308` `S0E-5B/P0-P3: guarded lifecycle apply expansion v1`
  - `#310` `S0E-5C/P0-P4: guarded PR create decomposition v1`
  - `#311` `S0E-7C/P0-P4: workflow/historical log review sampling and mirror follow-up v1`
  - `#312` `S0E-7C/P4-C1-S3: remove planner runtime closure dependency`

## P1 (Spec, gate, and renderer alignment | v1)

### P1-C1-S1 (Canonical PR body family updated | v1)

- Update the canonical PR body family so section order becomes:
  - `Metadata -> Summary -> Execution Checklist -> Links -> Evidence Footer (when applicable)`.
- Remove `Development Link` from the canonical family.

### P1-C1-S2 (PR Links categories narrowed | v1)

- Remove `Issue` from the allowed PR-link categories.
- Keep `Roadmap` as an optional PR-link category when the source log declares it.

### P1-C1-S3 (Hard gate and rewrite paths aligned | v1)

- Update PR body contract checks so they stop expecting `Development Link`.
- Update PR preview/create and historical PR rewrite paths so they stop rendering `Issue` inside `Links`.

## P2 (Historical S0E PR review and rewrite decision | v1)

### P2-C1-S1 (Review the current S0E PR inventory | v1)

- Inspect the current `17` live `S0E` PRs against the narrowed PR-body boundary.
- Record which PRs already match the new contract and which still carry redundant `Development Link` and/or `Links -> Issue` rows.

### P2-C1-S2 (Fix bounded rewrite scope explicitly | v1)

- The rewrite scope is fixed as one explicit bounded batch covering all `17` audited `S0E` PRs, because none of the live PRs currently pass the narrowed PR-body contract.
- Execution should still be grouped by drift family so repair order stays auditable:
  - family A: legacy pre-canonical PRs missing the canonical sections entirely (`#249`, `#291`, `#292`);
  - family B: canonical-body PRs that still carry `Development Link`, `Links -> Issue`, and stale/non-canonical Evidence Footer drift (`#287`, `#290`, `#294`, `#296`, `#298`, `#301`, `#302`, `#304`);
  - family C: canonical-body PRs that now only need the narrowed metadata-links cleanup (`#299`, `#306`, `#308`, `#310`);
  - family D: otherwise-canonical PRs that only retain an invalid `Links -> Issue` row (`#311`, `#312`).
- The bounded batch manifest is now recorded so the later rewrite step no longer needs to rediscover scope.

## P3 (Bounded live rewrite rollout | v1)

### P3-C1-S1 (Rewrite path unblocked for mixed historical logs | v1)

- `Evidence Footer Source` parsing is now restricted to the contiguous bullet rows immediately under its heading, so later explanatory bullets do not get misread as footer-source rows.
- `S0E-4C` no longer carries a stale non-eligible `Evidence Footer Source` block in `PR Summary Inputs`, which was the last source-log-level blocker for replaying `#301` and `#302` under the narrowed PR contract.

### P3-C2-S1 (Low-risk metadata-links cleanup batch applied | v1)

- The first bounded live apply cycle covers the lower-risk PRs whose main drift is the narrowed metadata-links boundary.
- This batch rewrites `#299`, `#306`, `#308`, `#310`, `#311`, and `#312` from manifest `docs/issues/pr-body-rewrite-S0E-4F-p3-c2-manifest.json`.

### P3-C3-S1 (Canonical rebuild batch applied | v1)

- The second bounded live apply cycle covers the remaining historical PRs that required full canonical replay rather than a narrow links cleanup.
- This batch rewrites `#249`, `#287`, `#290`, `#291`, `#292`, `#294`, `#296`, `#298`, `#301`, `#302`, and `#304` from manifest `docs/issues/pr-body-rewrite-S0E-4F-p3-c3-manifest.json`.

### P3-C4-S1 (Post-apply live verify closed | v1)

- After both rewrite batches landed, the same `17` audited live `S0E` PRs were re-fetched from GitHub and revalidated against the narrowed PR body contract.
- The post-apply verification result is now `17/17 pass`.

## P4 (GitHub metadata completeness and historical issue backfill | v1)

### P4-C1-S1 (Future PR path emits GitHub-recognized development linkage | v1)

- The shared PR preview/create/rewrite path now appends deterministic `Closes #...` footer lines whenever a source log resolves a PR development issue.
- This keeps `Development issue` human-readable in `Metadata` while also giving GitHub a machine-recognized linkage surface for the right-hand `Development` sidebar.

### P4-C2-S1 (Live PR metadata backfill converged | v1)

- The two existing rewrite manifests were replayed through the updated live apply path so canonical PR bodies now also carry the close-link footer lines.
- The same live apply path now backfills any missing deterministic PR labels during historical rewrite instead of limiting itself to body text.
- Post-backfill live audit now shows the full `17`-PR audited set with expected labels present, `Development issue` metadata rendered, and GitHub `closingIssuesReferences` populated.

### P4-C3-S1 (Previously issue-less historical logs backfilled | v1)

- The previously issue-less audited logs `S0E-1A`, `S0E-2C`, `S0E-3A`, and `S0E-7C` now have live GitHub issues `#316`, `#313`, `#314`, and `#315` respectively.
- Their source logs now carry explicit `links.issue` write-back, and the primary audited PR links for `S0E-1A`, `S0E-2C`, and `S0E-3A` are no longer blank.

### P4-C4-S1 (Backfilled issue lifecycle closed | v1)

- Newly created backfill issues were attached to parent issue `#248` where applicable (`#313`, `#314`, `#315`) and then concluded from merged PR evidence.
- Final issue states are now closed for `#313`, `#314`, `#315`, and `#316`.

## P5 (Footer-scope convergence follow-up | v1)

### P5-C1-S1 (Preview and rewrite selectors converge | v1)

- The shared PR-prep dry-run path and the live PR rewrite path must both scope `Evidence Footer` through the same title-derived selector already used for `Execution Checklist`.
- A PR title that resolves to `P0-P2` may keep only the `P0/P1/P2` footer rows; a title that resolves to `P3-C1-S1` may keep only the exact `P3-C1-S1` footer row.
- Lifecycle bookkeeping such as `P4-C1-S1` remains source-log accounting and must not leak into PR footer/body scope unless the PR title itself intentionally reviews that lifecycle unit.

### P5-C2-S1 (Affected live PR bodies rewritten and re-verified | v1)

- The merged `S0E-7G` PRs `#320` and `#321` must be rewritten so their live bodies retain only footer rows that match their existing PR titles.
- The open `S0E-3B` PR `#323` must keep merge-content scope `P0-P2` in its title/body/footer, while `P4-C1-S1` stays recorded only in the source log ledger and evidence.
- Post-apply verification must confirm all three rewritten live PR bodies pass the canonical PR body contract after the footer-scope fix.

## Execution Checklist (unchecked)

### P0 (PR-body ownership boundary)

- [x] `P0-C1-S1`: development issue identity narrowed to `Metadata` only
- [x] `P0-C1-S2`: PR `Links` narrowed to deterministic navigation only
- [x] `P0-C1-S3`: full current `S0E` PR review inventory fixed

### P1 (Spec, gate, and renderer alignment)

- [x] `P1-C1-S1`: canonical PR body family updated
- [x] `P1-C1-S2`: PR link categories narrowed
- [x] `P1-C1-S3`: hard gate and rewrite paths aligned

### P2 (Historical S0E PR review and rewrite decision)

- [x] `P2-C1-S1`: current `S0E` PR inventory reviewed
- [x] `P2-C1-S2`: bounded rewrite scope fixed explicitly

### P3 (Bounded live rewrite rollout)

- [x] `P3-C1-S1`: rewrite path unblocked for mixed historical logs
- [x] `P3-C2-S1`: low-risk metadata-links cleanup batch applied
- [x] `P3-C3-S1`: canonical rebuild batch applied
- [x] `P3-C4-S1`: post-apply live verify closed

### P4 (GitHub metadata completeness and historical issue backfill)

- [x] `P4-C1-S1`: future PR path emits GitHub-recognized development linkage
- [x] `P4-C2-S1`: live PR metadata backfill converged
- [x] `P4-C3-S1`: previously issue-less historical logs backfilled
- [x] `P4-C4-S1`: backfilled issue lifecycle closed

### P5 (Footer-scope convergence follow-up)

- [x] `P5-C1-S1`: preview and rewrite selectors converge
- [x] `P5-C2-S1`: affected live PR bodies rewritten and re-verified

## Evidence

- `P0-C1-S1` / `P1-C1-S3`: `scripts/issues/body_contract.py` now removes `Development Link` from canonical PR optional sections, removes `Issue` from allowed PR link labels, and rejects any rendered `Development Link` section.
- `P0-C1-S1` / `P1-C1-S3`: `scripts/issues/plan_pr_prep.py`, `scripts/issues/create_pr_from_plan.py`, and `scripts/issues/rewrite_pr_body_scope_from_log.py` now keep development issue identity only in `Metadata`, stop rendering `Development Link`, and stop defaulting PR `Links` to `Issue` rows.
- `P1-C1-S1` / `P1-C1-S2`: `docs/issues/body-contract-S0E-5D-p0-canonical-spec.md` and `docs/issues/hard-gate-shape-S0E-5D-p2-canonical-spec.md` now describe the narrowed PR body family with deterministic `Links` only.
- `P1-C1-S1` / `P1-C1-S2`: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`, `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`, `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`, and the parent/phase log templates now align to the same metadata-only development-issue contract.
- `P2-C1-S1`: `docs/issues/pr-live-contract-check-S0E-4F-summary.json` records the full `17`-PR live audit result as `0 pass / 17 fail` under the narrowed PR body contract.
- `P2-C1-S1`: the per-PR audit artifacts `docs/issues/pr-live-contract-check-S0E-4F-*-result.json` and matching `*-body.md` files now preserve the exact live failure reasons for each audited PR.
- `P2-C1-S2`: `docs/issues/pr-body-rewrite-S0E-4F-p2-manifest.json` fixes the bounded rewrite scope as all `17` audited PRs, grouped into four explicit drift families.
- `P3-C1-S1`: `scripts/issues/body_contract.py` now treats `Evidence Footer Source` as the contiguous bullet block immediately under its heading, and `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md` no longer carries the stale non-eligible footer-source block that had blocked `#301/#302` replay.
- `P3-C2-S1`: `docs/issues/pr-body-rewrite-S0E-4F-p3-c2-manifest.json` and `docs/issues/pr-body-rewrite-S0E-4F-p3-c2-manifest-result.json` record the first live apply cycle for `#299/#306/#308/#310/#311/#312`, with per-PR `*-live-body.md`, `*-rewritten-body.md`, and `*-apply-result.json` artifacts.
- `P3-C3-S1`: `docs/issues/pr-body-rewrite-S0E-4F-p3-c3-manifest.json` and `docs/issues/pr-body-rewrite-S0E-4F-p3-c3-manifest-result.json` record the second live apply cycle for `#249/#287/#290/#291/#292/#294/#296/#298/#301/#302/#304`, with per-PR `*-live-body.md`, `*-rewritten-body.md`, and `*-apply-result.json` artifacts.
- `P3-C4-S1`: `docs/issues/pr-live-contract-check-S0E-4F-post-apply-summary.json` records the final post-apply verify result as `17 pass / 0 fail`, and the matching `*-post-apply-result.json` files preserve each live PR's final pass check.
- `P4-C1-S1`: `scripts/issues/body_contract.py`, `scripts/issues/plan_pr_prep.py`, `scripts/issues/rewrite_pr_body_scope_from_log.py`, and `scripts/issues/apply_pr_body_rewrite_batch.py` now emit and verify deterministic `Closes #...` footer lines for PR development linkage and backfill missing PR labels during historical live rewrite.
- `P4-C2-S1`: `docs/issues/pr-body-rewrite-S0E-4F-p4-c2-manifest-result.json`, `docs/issues/pr-body-rewrite-S0E-4F-p4-c3-manifest-result.json`, and `docs/issues/pr-metadata-completeness-S0E-4F-p4-summary.json` record the live PR metadata replay and final `17/17` metadata-complete audit.
- `P4-C3-S1`: `docs/issues/issue-S0E-1A-structured-cv-generator.json`, `docs/issues/issue-S0E-2C-batch-issue-creation-and-backfill-tooling.json`, `docs/issues/issue-S0E-3A-roadmap-milestone-log-bridge.json`, and `docs/issues/issue-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.json` record the four newly created historical backfill issues.
- `P4-C4-S1`: `docs/issues/issue-conclusion-S0E-4F-p4-backfill-plan.json`, the four matching `issue-conclusion-S0E-4F-p4-backfill-*-apply-result.json` files, and `docs/issues/issue-backfill-S0E-4F-p4-summary.json` record the final issue-conclusion and close-state convergence for `#313/#314/#315/#316`.
- `P5-C1-S1`: `scripts/issues/plan_pr_prep.py`, `scripts/issues/rewrite_pr_body_scope_from_log.py`, and `scripts/issues/body_contract.py` now filter and verify `Evidence Footer` through the same title-derived scope selector already used for `Execution Checklist`, removing the earlier full-footer leakage from scope-limited PR previews, rewrites, and live verification.
- `P5-C2-S1`: `docs/issues/pr-body-rewrite-S0E-4F-p5-c1-manifest.json` and `docs/issues/pr-body-rewrite-S0E-4F-p5-c1-manifest-result.json` record the bounded historical rewrite of merged PRs `#320/#321`, while `docs/issues/pr-prep-S0E-3B-live-manifest-guarded-pr-body-rewrite-result.json` preserves the retained gate-stop artifact for open PR `#323` and `docs/issues/pr-prep-S0E-3B-live-manifest-rewrite-apply-result.json` records the final single-item live rewrite apply.
- `P5-C2-S1`: `docs/issues/pr-live-contract-check-320-result.json`, `docs/issues/pr-live-contract-check-321-result.json`, and `docs/issues/pr-live-contract-check-323-result.json` preserve the post-apply live contract verification results for the three affected PRs.

## Recent changes (for traceability, optional)

- 2026-04-03: resumed `S0E-4F` after review, confirmed PR `#329` merged, generated the single-item conclusion preview from exact-ID merged PR evidence, and wrote the final conclusion body back to already-closed live issue `#327` in place.
- 2026-04-03: created live issue `#327`, refreshed its single-generated Context, attached the expected sidebar parent relationship to `#248`, and opened ready-for-review PR `#329`; full-auto now pauses at the human merge boundary before any later issue-conclusion step.
- 2026-04-02: opened `S0E-4F` to narrow duplicated development-issue surfaces out of the PR body family after the issue-body redundancy cleanup in `S0E-6F` stabilized.
- 2026-04-02: fixed the first review inventory as the current `17` live `S0E` PRs so later remediation decisions can be made against one explicit set instead of ad hoc spot checks.
- 2026-04-02: completed `P0-P1` locally by updating the canonical PR spec, hard gate, PR preview/create path, PR rewrite path, and log templates so PR bodies keep development issue identity only in `Metadata`.
- 2026-04-02: completed `P2` by auditing all `17` current live `S0E` PRs, confirming `17/17` still drift from the narrowed PR body contract, and fixing the later rewrite scope as one explicit bounded batch grouped by four drift families.
- 2026-04-02: completed `P3-C1-S1` by tightening `Evidence Footer Source` extraction to the contiguous bullet block and removing the stale non-eligible footer-source block from `S0E-4C`, which unblocked the last mixed historical rewrite path.
- 2026-04-02: completed `P3-C2-S1` by live-rewriting the lower-risk metadata-links cleanup batch `#299/#306/#308/#310/#311/#312`.
- 2026-04-02: completed `P3-C3-S1` by live-rewriting the remaining canonical rebuild batch `#249/#287/#290/#291/#292/#294/#296/#298/#301/#302/#304`.
- 2026-04-02: completed `P3-C4-S1` by re-verifying all `17` audited live `S0E` PRs to `17/17 pass` under the narrowed PR body contract.
- 2026-04-02: completed `P4-C1-S1` by teaching the shared PR preview/create/rewrite path to emit deterministic `Closes #...` footer lines and by teaching the live rewrite batch to backfill missing PR labels.
- 2026-04-02: completed `P4-C2-S1` by replaying both bounded PR rewrite manifests so the same `17` audited live `S0E` PRs now expose GitHub-recognized Development linkage and deterministic labels.
- 2026-04-02: completed `P4-C3-S1` by creating and writing back the previously missing historical issues `#316` (`S0E-1A`), `#313` (`S0E-2C`), `#314` (`S0E-3A`), and `#315` (`S0E-7C`).
- 2026-04-02: completed `P4-C4-S1` by attaching `#313/#314/#315` to parent `#248`, concluding all four backfilled issues from merged PR evidence, and closing `#313/#314/#315/#316`.
- 2026-04-03: completed `P5-C1-S1` by fixing the shared footer-scope selector so PR preview generation and live PR rewrite both scope `Evidence Footer` to the same merge-content scope already used by PR titles and checked checklist rows.
- 2026-04-03: completed `P5-C2-S1` by rewriting live PRs `#320`, `#321`, and `#323` to their title-derived footer scope and re-verifying all three bodies against the canonical PR body contract.