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

## P1 Create-Time Completeness Rules (planned)

- `Metadata` fields are required when frontmatter or controlled derivation supplies them; otherwise they must stay blank rather than guessed.
- `Links` rows render only when the corresponding source-log value exists; empty `Runbook`, `Roadmap`, `Parent log`, or `Previous log` rows are non-canonical.
- Parent relationship completeness includes both body `Parent issue` rendering and live sidebar relationship state.
- Default project fallback, if retained, must be audited explicitly rather than treated as invisible behavior.

## P2 PR-Time Completeness Rules (planned)

- PR completeness must distinguish `rendered correctly` from `semantically complete`.
- If the source log implies an exact issue owner for the PR lifecycle, a blank `pr_development_issue` must be auditable as a gap even if the body omitted the field consistently.
- `Development issue` metadata, `Closes #...` footer rows, and GitHub-recognized development linkage should be checked as one owned surface.
- PR labels remain a required completeness surface whenever the deterministic label set can be derived from the source log.

## P3 Conclusion-Time Completeness Rules (planned)

- Child issue conclusion requires exact four-sentence Context; top-level parent issue conclusion requires exact five-sentence Context.
- Final DoD must match the exact-ID merged PR set for child issues and the owned child-issue ledger for top-level parent issues.
- Final Links must still obey blank-as-omitted rules while re-checking any newly written source-log references.
- Conclusion review should re-check existing sidebar state instead of assuming earlier creation/PR attachments remained valid.

## P4 Read-Only Audit Packaging (planned)

- The first stable entrypoint should accept one manifest and emit per-item classification across the three lifecycle stages.
- Output should preserve stage-local failures such as `creation-links-gap`, `pr-development-linkage-gap`, or `conclusion-dod-mismatch` instead of one generic drift bucket.
- The first retained sample should stay small and representative so reviewers can compare audit output against live GitHub state by hand.

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

- [ ] `P1-C1-S1`: create-time field matrix fixed for issue body plus sidebar state
- [ ] `P1-C1-S2`: blank-as-omitted Links review rule fixed

### P2 (PR completeness)

- [ ] `P2-C1-S1`: PR development-linkage completeness rule fixed
- [ ] `P2-C1-S2`: PR labels and close-link footer completeness rule fixed

### P3 (Conclusion completeness)

- [ ] `P3-C1-S1`: final issue body completeness rule fixed
- [ ] `P3-C1-S2`: conclusion-time sidebar re-check rule fixed

### P4 (Read-only audit entrypoint)

- [ ] `P4-C1-S1`: representative read-only completeness audit sample retained

## Notes (optional)

- `S0F-1D` is the first `S0F` slice whose primary output is a review model rather than a mutation path.
- The intended follow-up after `S0F-1D` is not necessarily remediation; if the matrix still exposes ambiguous ownership, the next step should remain contract clarification rather than premature repair automation.

## Evidence

- `P0-C1-S1` / `P0-C1-S2`: `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md` now fixes the three-stage completeness matrix, including the ownership split for body versus sidebar state and the non-canonical status of blank optional `Links` rows.
- `P0-C1-S1`: `docs/logs/log-S0F-docs-management-v6.md` now records `S0F-1D` as the next explicit follow-up slice under the `S0F` spine and reflects `P0` as complete rather than leaving `1D` as a placeholder follow-up.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-1D/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
