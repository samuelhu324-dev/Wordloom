# log-S0F-1G (Phase 1G: parent issue sidebar ordering and title keyword governance)

---

**id**: `S0F-1G`
**kind**: `log`
**title**: `parent issue sidebar ordering and title keyword governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Automation, Audit, Contract, Governance, epic/s0, sub/1g`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-1F-bucketed-audit-output-materialization.md`
  **reference_log_1**: `docs/logs/log-S0E-docs-management-v5.md`
  **reference_log_2**: `docs/logs/log-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
  **reference_log_3**: `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`
  **reference_log_4**: `docs/logs/log-S0F-1E-completeness-classification-buckets-and-audit-output-taxonomy.md`
  **reference_log_5**: `docs/logs/log-S0F-1F-bucketed-audit-output-materialization.md`
**issue_keyword**: `audit`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1g`
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

- `S0F-1G` is the next `S0F` follow-up slice, and it concentrates two governance gaps that are now clearly related: the still-blocked top-level parent issue sidebar ordering drift and the lack of hard enforcement on live issue title keyword prefixes.
- v1 should treat these as one ownership lane rather than as two unrelated cleanup tasks. Both problems come from the same contract weakness: source-log-owned deterministic issue identity is not yet enforced strongly enough on the final GitHub issue surface.
- The first target is governance closure, not bulk repair. `S0F-1G` should first fix what the canonical ordering source is for top-level parent sub-issue relationships and what the controlled vocabulary source is for issue title keywords before any wider migration or rewrite work starts.
- The rollout should stay fail-closed. If a parent issue's expected child ordering cannot be derived deterministically from the source log, or if a title keyword is outside the controlled vocabulary, live mutation and lifecycle audit should stop rather than silently accept drift.

**Default choices (phase defaults / v1)**:

- The source log remains the canonical owner of parent-child ordering for top-level parent issues; GitHub sidebar order is an audited projection of that ledger, not an independent source of truth.
- `issue_keyword` should become a controlled vocabulary input for real issue creation rather than a merely required free-text field.
- Title keyword governance should land in two layers: create-time hard-fail validation and lifecycle-audit drift detection against the canonical source-log-derived expectation.
- Existing live issues with historically wrong title prefixes may remain temporarily, but they should become explicitly classifiable drift rather than silently acceptable state.
- `S0F-1G` should not widen into generic issue-title rewriting across the whole repository before the vocabulary contract, audit semantics, and migration boundary are fixed.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Open one focused `S0F` slice for the remaining parent sidebar ordering gap and the missing hard governance around issue title keyword prefixes.
- Fix the contract boundary so source-log-owned ordering and title keyword vocabulary become deterministic, fail-closed audit surfaces instead of soft conventions.
- Prepare the next follow-up path for controlled parent issue repair and explicit title-prefix enforcement without mixing policy design with blind bulk rewrites.

**PR checklist source**:

- Default source: reuse this log's execution checklist for generated PR checklist blocks.

**PR links**:

- Log: `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`

## Definitions (optional)

- `parent sidebar ordering`: the ordered GitHub sub-issue relationship set rendered on a top-level parent issue.
- `title keyword`: the prefix token in `ID: keyword/subject`, sourced from `issue_keyword`.
- `controlled vocabulary`: the explicitly allowed keyword set for real live issue titles.
- `identity drift`: any mismatch where live GitHub issue ordering or title prefix no longer matches the deterministic source-log-owned expectation.

## Constraints

- Do not treat GitHub's current sidebar order as authoritative when it disagrees with the source-log-owned child ledger.
- Do not allow create-time fallback or inferred issue keywords to continue as acceptable live issue title input.
- Do not bulk-rewrite historical live issue titles before the controlled vocabulary and audit contract are fixed.
- Do not mix this slice with unrelated PR-body or conclusion-body remediation work.

## Scope

- `P0`: create `S0F-1G`, wire it into the `S0F` spine, and fix the governance boundary
- `P1`: fix top-level parent issue sidebar ordering ownership and repair contract
- `P2`: fix create-time controlled vocabulary enforcement for `issue_keyword`
- `P3`: fix lifecycle-audit title-prefix validation and bucket attribution
- `P4`: package retained migration inventory and controlled repair path for historical drift

## Success Criteria (DoD)

- The repo has one explicit `S0F` slice that owns both parent sidebar ordering drift and title keyword governance.
- Create-time issue creation can fail closed on disallowed title keywords instead of merely requiring the field to be non-empty.
- Lifecycle audit can fail when a live issue title prefix does not match the canonical source-log-owned expectation.
- The remaining parent issue ordering drift has one explicit repair contract instead of lingering as an unowned blocked audit item.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the canonical ownership of top-level parent sidebar ordering is fixed and enforced;
  - title keyword governance is enforced at both create-time and lifecycle-audit time;
  - one retained repair or migration package shows how historical drift is handled without reopening guess-first behavior.

## Current Status

- `S0F-1G` is now opened as the next `S0F` follow-up slice for the two remaining governance gaps that still leak through current docs/GitHub lifecycle controls.
- The first gap is already concrete in live evidence: parent issue `#248` is no longer blocked by prose, DoD, or link coverage, but only by GitHub sidebar child ordering drift against the source-log-owned expected order.
- The second gap is also now concrete in code inspection: real issue creation requires an explicit `issue_keyword`, but current tooling does not yet enforce a controlled vocabulary or audit fail condition for semantically wrong title prefixes such as `inventory`, `naming`, or `coexistence`.
- `P0` is now complete: `S0F-1G` is wired into the spine, the shared governance boundary is fixed, and the next follow-up is `P1` top-level parent sidebar ordering ownership and repair semantics.
- `P1` is now complete: lifecycle audit now preserves the real GitHub sub-issue sidebar order instead of sorting it away, one controlled reprioritize path is retained under `scripts/issues/reprioritize_parent_subissues.py`, and the live `#248` parent sidebar can now be repaired back to the canonical source-log-owned order without destructive remove/re-add behavior.
- The live `#248` repair is now complete and re-verified: the retained reprioritize result under `artifacts/` converged to the expected child order, and a focused rerun of `plan_lifecycle_audit.py` now passes the parent `sidebar-child-relationships` check instead of leaving `S0E` blocked on an ordering mismatch.

## P1 Parent Sidebar Ordering (completed)

- `S0F-1G` now fixes the ownership boundary for top-level parent sub-issue order at the same contract layer that already owns canonical parent child-ledger order in the source log and issue body contract.
- v1 therefore makes two changes together: the lifecycle audit must read the real live sidebar order as-is, and the live repair path must reuse the same canonical source-log ordering instead of accepting ad hoc manual GitHub drag-and-drop.

### P1-C1-S1 (Real sidebar-order audit semantics fixed | v1)

- `scripts/issues/plan_lifecycle_audit.py` no longer sorts the live GitHub sub-issue numbers before comparing them to the canonical parent child ledger.
- The `sidebar-child-relationships` check now audits the actual live GitHub sidebar order, which closes the earlier semantic gap where order drift could be partially hidden by accidental sorting before comparison.
- The canonical expected order remains source-log-owned through `ordered_parent_child_issue_refs(...)`, so audit now compares the correct live order against the correct deterministic contract.

### P1-C1-S2 (Controlled parent ordering repair path retained | v1)

- `scripts/issues/reprioritize_parent_subissues.py` now retains one controlled parent repair path that derives expected child order from the parent source log, fetches live GitHub sub-issues, fails closed when the live child set does not match the canonical set, and only then plans or applies ordered `reprioritizeSubIssue` mutations.
- This repair path is intentionally non-destructive: it reorders existing GitHub sub-issue relationships in place instead of removing and re-adding child issues.
- The retained result output defaults to `artifacts/`, which keeps this repair path aligned with the new local scratch-output hygiene boundary rather than reopening `docs/issues` commit noise.
- The first live use of this repair path has now been completed against parent issue `#248`, and the subsequent focused lifecycle-audit rerun confirms the parent ordering blocker is cleared under the corrected audit semantics.

## P0 Governance Boundary (completed)

- `S0F-1G` should first fix that the parent issue sidebar ordering drift and title keyword prefix drift belong to the same governance lane: deterministic issue identity on live GitHub surfaces.
- The first implementation owner should remain the existing docs/GitHub lifecycle stack rather than an external migration script, because both ordering and title-prefix expectations already originate from source logs and lifecycle audit rules.
- Wider repair should follow only after the ownership boundary is explicit: live GitHub issue state must be projected from source-log-owned ordering and keyword contracts rather than accepted as self-authoritative drift.

### P0-C1-S1 (Spine wiring fixed | v1)

- `S0F-1G` is now the canonical `S0F` follow-up for the remaining parent issue sidebar ordering gap and the missing title keyword governance contract.
- The parent `S0F` spine now points to `S0F-1G` explicitly and records it as the next child slice after `S0F-1F` stabilized read-only bucketed audit output.

### P0-C1-S2 (Shared governance boundary fixed | v1)

- Top-level parent sidebar ordering drift is now explicitly treated as a source-log-owned identity projection problem rather than as a one-off GitHub cleanup task.
- Title keyword drift is now explicitly treated as a controlled-vocabulary governance problem rather than as an informal naming preference.
- `S0F-1G` therefore fixes one shared rule for both surfaces: when live GitHub issue identity cannot be derived from the canonical source contract or violates that contract, create/apply/audit flows should fail closed instead of accepting soft drift.

## Plan (draft)

### P0 (Governance boundary and spine wiring)

- P0-C1-S1: create `S0F-1G` and wire it into the `S0F` parent spine
- P0-C1-S2: fix the shared governance boundary for parent ordering and title keyword identity

### P1 (Parent sidebar ordering)

- P1-C1-S1: fix top-level parent sub-issue ordering source-of-truth and audit semantics
- P1-C1-S2: retain one controlled repair path for the remaining parent ordering drift

### P2 (Create-time title keyword governance)

- P2-C1-S1: fix controlled vocabulary input rules for `issue_keyword`
- P2-C1-S2: hard-fail real issue creation on disallowed title keywords

### P3 (Lifecycle audit title keyword enforcement)

- P3-C1-S1: derive canonical expected title prefix from source-log-owned issue keyword state
- P3-C1-S2: emit deterministic lifecycle-audit failure and bucket attribution for title-prefix drift

### P4 (Historical drift packaging)

- P4-C1-S1: retain one migration inventory for existing historical title-prefix and parent-ordering drift
- P4-C1-S2: package the controlled repair boundary for later historical cleanup

## Execution Checklist (unchecked)

### P0 (Governance boundary and spine wiring)

- [x] `P0-C1-S1`: `S0F-1G` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: shared governance boundary fixed for parent ordering and title keyword identity

### P1 (Parent sidebar ordering)

- [x] `P1-C1-S1`: top-level parent sub-issue ordering source-of-truth and audit semantics fixed
- [x] `P1-C1-S2`: one controlled repair path retained for remaining parent ordering drift

### P2 (Create-time title keyword governance)

- [ ] `P2-C1-S1`: controlled vocabulary input rules fixed for `issue_keyword`
- [ ] `P2-C1-S2`: real issue creation hard-fails on disallowed title keywords

### P3 (Lifecycle audit title keyword enforcement)

- [ ] `P3-C1-S1`: canonical expected title prefix derived from source-log-owned keyword state
- [ ] `P3-C1-S2`: lifecycle audit emits deterministic title-prefix drift failure and bucket attribution

### P4 (Historical drift packaging)

- [ ] `P4-C1-S1`: migration inventory retained for historical title-prefix and parent-ordering drift
- [ ] `P4-C1-S2`: controlled repair boundary packaged for later cleanup

## Notes (optional)

- `S0F-1G` is intentionally narrow: it owns the governance contract first, not immediate bulk historical rewrite.
- If `P1` lands before `P2` and `P3`, parent ordering repair may close the remaining `#248` blocker earlier, but title keyword governance should still remain inside the same slice until both enforcement layers are fixed.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths after concrete repair or enforcement work begins.
- `P0` is intentionally contract-first, so retained execution evidence begins with later implementation or repair phases rather than with this initial opening step.