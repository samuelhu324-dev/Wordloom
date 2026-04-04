# log-S0F-1D (Phase 1D: creation / PR / conclusion completeness audit)

---

**id**: `S0F-1D`
**kind**: `log`
**title**: `creation, PR, and conclusion completeness audit v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Automation, Audit, Contract, epic/s0, sub/1d`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
  **reference_log_1**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_4**: `docs/logs/log-S0E-4F-pr-body-metadata-links-redundancy-follow-up.md`
  **reference_log_5**: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  **reference_log_6**: `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
  **reference_log_7**: `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
  **reference_log_8**: `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
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
**created**: `2026-04-04`
**updated**: `2026-04-04`

---

## Decision / Outcome

**Decision**:

- `S0F-1D` is the next follow-up slice under `S0F`, and it turns the current body-contract plus lifecycle tooling into one explicit completeness-audit model spanning `Creation -> PR -> Conclusion`.
- v1 should stop treating lifecycle review as one undifferentiated pass. The canonical audit surface should instead separate create-time issue completeness, PR-time development-linkage completeness, and conclusion-time close-out completeness.
- The first target is not live mutation. It is a read-only completeness matrix plus one audit entrypoint that can prove which lifecycle stage is incomplete and why.
- The most important missing surface is PR-side development-linkage completeness: current tooling can validate rendered PR body shape, but it does not yet fail a batch merely because the source log left `pr_development_issue` blank while the lifecycle clearly expects a development issue.

**Default choices (phase defaults / v1)**:

- `Creation audit`, `PR audit`, and `Conclusion audit` remain distinct stages even if one manifest later runs them together.
- Issue body `Metadata`, `Context`, `Definition of Done (DoD)`, and `Links` must be judged against the correct lifecycle stage rather than against one static final-state expectation.
- Right-hand GitHub sidebar state is part of completeness, not optional decoration; labels, projects, milestone, parent relationship, and PR development linkage all belong inside the audit boundary.
- `Development` is PR-owned for first materialization and Conclusion-owned for final re-check. It should not be modeled as a conclusion-only field.
- `Links` should omit blank optional rows instead of rendering empty placeholders; blank-as-omitted remains the canonical rule for both preview and live review.
- The first rollout should stay read-only and evidence-first so the repo can classify historical gaps before any repair or backfill path is widened.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Define one explicit completeness-audit contract for the three lifecycle stages: issue creation, PR development linkage, and issue conclusion.
- Fix the field-timing matrix so create-time, PR-time, and conclusion-time expectations are no longer inferred ad hoc during review.
- Add a dedicated PR development-linkage completeness lane that can detect source-log omissions instead of validating only rendered PR body structure.
- Keep the first rollout read-only so historical and active slices can be classified before remediation is introduced.

**PR checklist source**:

- Default source: reuse this log's execution checklist for generated PR checklist blocks.

**PR links**:

- Log: `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`

## Definitions (optional)

- `Creation audit`: a read-only review pass that checks whether create-time issue body and issue sidebar state match the source log and creation contract.
- `PR audit`: a read-only review pass that checks PR body structure, development issue identity, close-link footer rows, and GitHub-recognized development linkage.
- `Conclusion audit`: a read-only review pass that checks final issue Context, DoD merged-PR ledger, deterministic Links, and preserved sidebar state after merge/conclusion.
- `field-timing matrix`: the stage-by-stage rule that declares whether a field is required, optional, derived, blank-by-default, or conclusion-only.
- `development-linkage completeness`: the rule that source-log expectation, PR metadata row, `Closes #...` footer, and GitHub sidebar/linkage state must all agree.

## Constraints

- Do not collapse the three lifecycle stages into one final-state-only validator.
- Do not allow PR completeness to pass merely because the rendered body omitted `Development issue` consistently with a blank source field.
- Do not treat empty optional Links rows as valid canonical output.
- Do not postpone sidebar review until after conclusion when the field is already create-time or PR-time owned.
- Do not introduce live mutation in this slice until the read-only completeness matrix is stable enough to classify failures deterministically.

## Scope

- `P0`: define the lifecycle completeness matrix and wire `S0F-1D` into the `S0F` spine
- `P1`: fix the create-time issue completeness contract, including body and sidebar expectations
- `P2`: fix the PR-time completeness contract, especially development-linkage completeness
- `P3`: fix the conclusion-time completeness contract for final issue body plus sidebar re-check
- `P4`: package one read-only audit entrypoint and representative retained audit sample

## Success Criteria (DoD)

- Reviewers can classify a lifecycle gap as `creation`, `pr`, or `conclusion` incomplete instead of describing drift generically.
- The completeness matrix makes it explicit which fields are required, omitted, or intentionally blank at each lifecycle stage.
- PR completeness review can fail when development linkage is missing semantically, not only when body formatting is malformed.
- Issue completeness review includes both body state and right-hand GitHub sidebar state.
- One read-only audit path can emit enough evidence to decide whether follow-up work belongs in creation hardening, PR linkage repair, or conclusion repair.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the create-time, PR-time, and conclusion-time completeness matrix is fixed;
  - at least one read-only audit surface can classify representative items without requiring manual reinterpretation of field timing;
  - the repo no longer depends on ad hoc human memory to decide whether a missing field is acceptable at the current lifecycle stage.

## Current Status

- `S0F-1D` is now opened as the next `S0F` follow-up and narrows the next gap exposed after `S0F-1A` through `S0F-1C`: lifecycle review still lacks one explicit completeness model covering body plus sidebar state across all three stages.
- The current shared tooling already covers much of the structure space: issue creation body shape is fixed, conclusion-time Context and DoD contracts are fixed, and guarded live mutation ownership is fixed.
- The remaining gap is semantic completeness review, especially on the PR side: current body-contract checks can validate `Development issue` rendering and `Closes #...` rows when a source value exists, but they still permit source-log omission to pass as blank-as-blank instead of classifying that omission as an audit failure.
- `P0` is now complete: the field-timing matrix is fixed, the three-stage completeness ownership is explicit, and the next follow-up is `P1` create-time issue completeness for body plus sidebar state.
- `P1` is now complete: create-time issue completeness is fixed for issue body plus sidebar ownership, blank optional `Links` rows are explicitly non-canonical, and the next follow-up is `P2` PR development-linkage completeness.
- `P2` is now complete: PR completeness is fixed as a semantic audit surface rather than a render-only body check, development-linkage completeness is unified across source log, PR metadata, close-link footer, and GitHub linkage state, and the next follow-up is `P3` conclusion-time completeness.
- `P3` is now complete: conclusion-time completeness is fixed for final issue body plus sidebar re-check, child versus top-level parent close-out rules are explicit, and the next follow-up is `P4` read-only audit packaging.
- `P4` is now complete: the first stable read-only audit packaging is fixed around one live lifecycle-audit entrypoint plus one optional historical pre-screen, representative retained samples already exist, and no further phase is currently required inside this slice.

## P0 Lifecycle Completeness Matrix (completed)

- Creation-owned checks:
  - issue body `Metadata` rows: labels, projects, milestone, and parent issue when derivable
  - issue body `Context`: structurally present and intentionally empty
  - issue body `Definition of Done (DoD)`: empty for child issues, child-ledger only for top-level parent issues
  - issue body `Links`: deterministic non-empty rows only
  - live issue sidebar: labels, projects, milestone, and parent relationship where applicable
- PR-owned checks:
  - PR body `Metadata`, `Summary`, `Execution Checklist`, and `Links`
  - `Development issue` metadata row
  - `Closes #...` footer rows derived from the development issue set
  - GitHub-recognized PR development linkage and expected labels
- Conclusion-owned checks:
  - final issue `Context` with exact child/main sentence-count contract
  - final issue `Definition of Done (DoD)` matching exact-ID merged PR evidence
  - final issue `Links` re-checked against the current source-log frontmatter
  - sidebar state re-verified after merge/conclusion so create-time attachments and PR-time linkage have not drifted

### P0-C1-S1 (Spine wiring fixed | v1)

- `S0F-1D` is now the canonical `S0F` follow-up for lifecycle completeness review rather than a placeholder under the parent spine.
- The parent `S0F` spine now points to `S0F-1D` explicitly and records it as the next read-only contract slice after `S0F-1C` stabilized the multi-item remediation workflow.

### P0-C1-S2 (Three-stage completeness matrix fixed | v1)

- `Creation` owns create-time issue body completeness plus issue sidebar attachment surfaces that are already deterministically known before PR creation.
- `PR` owns development-linkage first materialization, PR body completeness, and PR-side live metadata completeness, including the semantic rule that render-only success is not enough when the lifecycle clearly expects an exact issue linkage.
- `Conclusion` owns final issue body close-out completeness and the re-check that previously attached sidebar state still matches the converged lifecycle result.
- Blank optional `Links` rows are now explicitly non-canonical at every stage; completeness review should treat missing values as omitted rows, not empty placeholder rows.
- `Development` is now fixed as PR-owned for first write and Conclusion-owned for re-check, which prevents future slices from modeling it as a conclusion-only surface.

## P1 Create-Time Completeness Rules (completed)

- `Metadata` fields are required when frontmatter or controlled derivation supplies them; otherwise they must stay blank rather than guessed.
- `Links` rows render only when the corresponding source-log value exists; empty `Runbook`, `Roadmap`, `Parent log`, or `Previous log` rows are non-canonical.
- Parent relationship completeness includes both body `Parent issue` rendering and live sidebar relationship state.
- Default project fallback, if retained, must be audited explicitly rather than treated as invisible behavior.

### P1-C1-S1 (Create-time field matrix fixed for issue body plus sidebar state | v1)

- Create-time issue body completeness now owns exactly four sections in one stage-correct shape: `Metadata -> Context -> Definition of Done (DoD) -> Links`.
- `Metadata` rows are complete only when they follow frontmatter or controlled derivation rules: labels from deterministic derivation, project from explicit `issue_projects` or the current docs/logs default, milestone from explicit `issue_milestone` or exact roadmap bridge metadata, and parent issue from explicit `issue_parent` or the parent log's exact `links.issue`.
- `Context` is complete at create time only when it remains structurally present and intentionally empty; substantive prose belongs to conclusion, not creation.
- `Definition of Done (DoD)` is complete at create time when child issues remain empty by default and top-level parent issues render only the deterministic child-issue ledger already owned by the parent body contract.
- Create-time sidebar completeness now includes labels, projects, milestone, and parent relationship whenever those surfaces are already deterministically known before PR creation.

### P1-C1-S2 (Blank-as-omitted Links review rule fixed | v1)

- `Links` completeness at create time now means deterministic non-empty rows only: `Log` is always present, while `Runbook`, `Roadmap`, `Parent log`, and `Previous log` render only when the corresponding source-log value exists.
- Empty optional `Links` rows such as `Runbook: `` ` are explicitly non-canonical and should fail completeness review rather than pass as harmless placeholders.
- `Parent issue` remains metadata-only and may not be repeated under `Links`, even when parent relationship completeness is also checked on the live sidebar surface.
- `reference_log_*` rows remain outside create-time `Links` completeness because they are traceability inputs for readers, not deterministic issue-body navigation rows.

## P2 PR-Time Completeness Rules (completed)

- PR completeness must distinguish `rendered correctly` from `semantically complete`.
- If the source log implies an exact issue owner for the PR lifecycle, a blank `pr_development_issue` must be auditable as a gap even if the body omitted the field consistently.
- `Development issue` metadata, `Closes #...` footer rows, and GitHub-recognized development linkage should be checked as one owned surface.
- PR labels remain a required completeness surface whenever the deterministic label set can be derived from the source log.

### P2-C1-S1 (PR development-linkage completeness fixed as a semantic audit surface | v1)

- PR completeness now distinguishes two different questions: whether the PR body renders consistently with its inputs, and whether those inputs are semantically complete for the lifecycle stage.
- A render-only pass is no longer sufficient when the source log already exposes an exact issue owner through explicit `pr_development_issue` or the same-ID `links.issue` fallback path.
- PR development-linkage completeness is now defined as one owned four-part surface:
  - source-log expectation for the development issue set;
  - rendered PR `Metadata -> Development issue` row;
  - rendered `Closes #...` footer rows;
  - GitHub-recognized PR development linkage state.
- A PR may still be structurally valid while failing completeness review if the source-log expectation is blank only because metadata was omitted rather than because the lifecycle truly has no owned development issue.

### P2-C1-S2 (PR labels and close-link footer completeness fixed | v1)

- Deterministic PR labels remain part of completeness whenever the source log can derive them; missing live labels are a completeness gap even when the PR body itself is structurally valid.
- `Closes #...` footer rows are no longer treated as a presentation detail; they are part of the same completeness lane as `Development issue` metadata because GitHub uses them to materialize live development linkage.
- The canonical PR-body contract still validates row shape and exact footer equality, but completeness review now layers on the semantic question of whether the expected development issue set itself was left blank incorrectly.
- Historical evidence already proves the unified lane is viable: the retained `S0E-4F/P4` metadata-completeness audit shows `17/17` PRs with expected development issue, metadata row, closing refs, labels, and GitHub linkage present after convergence.

## P3 Conclusion-Time Completeness Rules (completed)

- Child issue conclusion requires exact four-sentence Context; top-level parent issue conclusion requires exact five-sentence Context.
- Final DoD must match the exact-ID merged PR set for child issues and the owned child-issue ledger for top-level parent issues.
- Final Links must still obey blank-as-omitted rules while re-checking any newly written source-log references.
- Conclusion review should re-check existing sidebar state instead of assuming earlier creation/PR attachments remained valid.

### P3-C1-S1 (Final issue body completeness fixed | v1)

- Conclusion-time issue completeness now owns the final body shape `Metadata -> Context -> Definition of Done (DoD) -> Links` and evaluates that shape against the lifecycle state after merge rather than against create-time expectations.
- `Context` is conclusion-complete only when it satisfies the owned sentence-count contract: child issues require exactly four readable English bullet sentences, while top-level parent issues require exactly five.
- `Definition of Done (DoD)` is conclusion-complete only when it matches the correct owned ledger for the item kind: exact-ID merged PR short refs for child issues and the source-log-owned child-issue ledger for top-level parent issues.
- `Links` are conclusion-complete only when they still obey blank-as-omitted rules and cover the current deterministic navigation set derived from the source log, including any PR references or log-side writes introduced during convergence.
- Final issue body completeness now distinguishes open-versus-closed expectations explicitly: open issues may still defer substantive conclusion content, while closed issues must satisfy the full conclusion-grade body contract.

### P3-C1-S2 (Conclusion-time sidebar re-check fixed | v1)

- Conclusion review now re-checks previously attached sidebar state instead of assuming earlier create-time or PR-time attachments remained correct after convergence.
- For child issues, conclusion-time sidebar completeness includes the expected parent relationship, deterministic labels, and the requirement that merged PR evidence actually exists for the same exact ID scope.
- For top-level parent issues, conclusion-time sidebar completeness includes the absence of an unexpected parent relationship plus the expected ordered child-issue relationship set.
- Source-log write-back and source-log PR linkage remain part of the conclusion audit surface because a concluded issue is incomplete when its final live state no longer matches the source-log navigation and merged-PR evidence boundary.

## P4 Read-Only Audit Packaging (completed)

- The first stable entrypoint should accept one manifest and emit per-item classification across the three lifecycle stages.
- Output should preserve stage-local failures such as `creation-links-gap`, `pr-development-linkage-gap`, or `conclusion-dod-mismatch` instead of one generic drift bucket.
- The first retained sample should stay small and representative so reviewers can compare audit output against live GitHub state by hand.

### P4-C1-S1 (First stable read-only audit package fixed | v1)

- The first stable read-only completeness entrypoint is now fixed as `scripts/issues/plan_lifecycle_audit.py`, using `docs/issues/lifecycle-audit-*-manifest.json` as input and `docs/issues/lifecycle-audit-*-plan.json` as the retained result shape.
- This entrypoint is primary because it audits the live issue body, labels, parent/sub-issue sidebar state, exact-ID merged PR evidence, final DoD refs, and source-log write-back on the same item instead of classifying lifecycle state from markdown alone.
- The entrypoint already emits the stage boundary needed by this slice through `lifecycle_stage`, `status`, `planned_action`, and per-check names, so v1 packaging can preserve creation, PR, and conclusion completeness as one read-only evidence bundle without introducing a new mutation path.
- `scripts/issues/plan_historical_log_review.py` remains the optional batch pre-screen for logs that still need lifecycle-stage discovery or structure-only review before live completeness audit is meaningful; it is supporting packaging, not the primary completeness owner.
- Representative retained samples are now explicit: `docs/issues/lifecycle-audit-S0F-1A-live-manifest.json` plus `docs/issues/lifecycle-audit-S0F-1A-live-plan.json` demonstrate a live creation-stage completeness failure bundle, while `docs/issues/historical-log-review-S0E-7C-sample-manifest.json` plus `docs/issues/historical-log-review-S0E-7C-sample-plan.json` remain the compact historical pre-screen sample for mixed lifecycle states.

## Plan (draft)

### P0 (Contract and spine wiring)

- P0-C1-S1: create `S0F-1D` and wire it into the `S0F` parent spine as the next follow-up slice
- P0-C1-S2: define the three-stage completeness matrix covering body and sidebar ownership

### P1 (Creation completeness)

- P1-C1-S1: fix the create-time required-versus-optional field matrix for issue body and issue sidebar state
- P1-C1-S2: define blank-as-omitted review rules for deterministic Links rows

### P2 (PR completeness)

- P2-C1-S1: define PR development-linkage completeness as a semantic audit surface rather than a render-only check
- P2-C1-S2: define label and footer expectations for PR completeness review

### P3 (Conclusion completeness)

- P3-C1-S1: define final issue body completeness rules for Context, DoD, and Links
- P3-C1-S2: define conclusion-time sidebar re-check coverage

### P4 (Read-only audit entrypoint)

- P4-C1-S1: retain one representative read-only completeness audit sample with per-stage classification output

## Execution Checklist (unchecked)

### P0 (Contract and spine wiring)

- [x] `P0-C1-S1`: `S0F-1D` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: three-stage completeness matrix fixed

### P1 (Creation completeness)

- [x] `P1-C1-S1`: create-time field matrix fixed for issue body plus sidebar state
- [x] `P1-C1-S2`: blank-as-omitted Links review rule fixed

### P2 (PR completeness)

- [x] `P2-C1-S1`: PR development-linkage completeness rule fixed
- [x] `P2-C1-S2`: PR labels and close-link footer completeness rule fixed

### P3 (Conclusion completeness)

- [x] `P3-C1-S1`: final issue body completeness rule fixed
- [x] `P3-C1-S2`: conclusion-time sidebar re-check rule fixed

### P4 (Read-only audit entrypoint)

- [x] `P4-C1-S1`: representative read-only completeness audit sample retained

## Notes (optional)

- `S0F-1D` is the first `S0F` slice whose primary output is a review model rather than a mutation path.
- The intended follow-up after `S0F-1D` is not necessarily remediation; if the matrix still exposes ambiguous ownership, the next step should remain contract clarification rather than premature repair automation.

## Evidence

- `P0-C1-S1` / `P0-C1-S2`: `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md` now fixes the three-stage completeness matrix, including the ownership split for body versus sidebar state and the non-canonical status of blank optional `Links` rows.
- `P0-C1-S1`: `docs/logs/log-S0F-docs-management-v6.md` now records `S0F-1D` as the next explicit follow-up slice under the `S0F` spine and reflects `P0` as complete rather than leaving `1D` as a placeholder follow-up.
- `P1-C1-S1` / `P1-C1-S2`: `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md` now fixes create-time completeness ownership for issue body and sidebar state, including the rule that create-time `Context` remains intentionally empty while create-time labels/projects/milestone/parent attachment stay inside the audit boundary.
- `P1-C1-S1` / `P1-C1-S2`: `scripts/issues/gen_issue_draft.py` and `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md` remain the implementation and contract anchors for the create-time matrix recorded here: milestone derivation stays exact-bridge-only, parent issue may derive from `parent_log.links.issue`, top-level parent DoD may carry the child-issue ledger, and `Links` render only non-empty deterministic rows.
- `P2-C1-S1` / `P2-C1-S2`: `scripts/issues/body_contract.py`, `scripts/issues/plan_pr_prep.py`, and `scripts/issues/verify_live_pr_body_contract.py` remain the implementation anchors for PR completeness recorded here: the current contract validates rendered metadata/footer shape, derives development issue from explicit `pr_development_issue` or source-log `links.issue`, and therefore exposes exactly where render-only validation still differs from semantic completeness review.
- `P2-C1-S1` / `P2-C1-S2`: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`, `docs/logs/log-S0E-4F-pr-body-metadata-links-redundancy-follow-up.md`, and `docs/issues/pr-metadata-completeness-S0E-4F-p4-summary.json` remain the contract and evidence anchors for the unified PR completeness lane: development issue identity is metadata-owned, `Closes #...` rows and GitHub linkage must converge, and the retained historical audit already proves the lane is auditable on live PRs.
- `P3-C1-S1` / `P3-C1-S2`: `scripts/issues/plan_lifecycle_audit.py`, `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`, and `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md` remain the implementation and contract anchors for conclusion completeness recorded here: final issue body shape is validated against merged-PR evidence, child versus top-level parent DoD ownership stays explicit, and conclusion-time `Context` remains bound to the exact four/five sentence-count contract.
- `P3-C1-S1` / `P3-C1-S2`: the current lifecycle audit surface already proves the conclusion re-check lane is broader than body prose alone by reviewing label coverage, source-log write-back, parent/sub-issue relationships, merged-PR evidence, final DoD refs, Links coverage, and closed-body Context validity on the same live issue.
- `P4-C1-S1`: `scripts/issues/plan_lifecycle_audit.py`, `docs/issues/lifecycle-audit-S0F-1A-live-manifest.json`, and `docs/issues/lifecycle-audit-S0F-1A-live-plan.json` now anchor the first stable read-only completeness package recorded here: one manifest-driven live audit entrypoint emits lifecycle stage, gate status, planned action, and per-check results in a retained JSON bundle without mutating GitHub state.
- `P4-C1-S1`: `scripts/issues/plan_historical_log_review.py`, `docs/issues/historical-log-review-S0E-7C-sample-manifest.json`, and `docs/issues/historical-log-review-S0E-7C-sample-plan.json` remain the compact supporting sample for batch pre-screen packaging: they classify mixed lifecycle states (`log-only`, `issue-open-no-pr`, `concluded`) and preserve structure-review output before the primary live completeness audit is invoked.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-1D/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
