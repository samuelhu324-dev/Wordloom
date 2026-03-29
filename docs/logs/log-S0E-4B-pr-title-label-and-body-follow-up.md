# log-S0E-4B (Phase 4B: PR Title, Label, and Body Follow-up)

---

**id**: `S0E-4B`
**kind**: `log`
**title**: `PR title compression, structural label inheritance, and body footer follow-up v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, PR, Automation, epic/s0, sub/0e4b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_1**: `docs/logs/_template-log-parent-epic-spine.md`
  **reference_log_2**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_3**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `pr-prep/s0e-4a`
**pr_development_issue**: ``
**created**: `2026-03-29`
**updated**: `2026-03-29`

---

## Decision / Outcome

**Decision**:

- `S0E-4B` exists as the narrow follow-up to `S0E-4A`, focused only on PR title naming, PR label inheritance, and PR body section formatting.
- Structural PR labels should no longer rely only on `pr_labels`; they should inherit explicit issue-side structural labels from the same log.
- PR body generation should match the newer log template shape, especially flat execution checklist parsing plus separate `Evidence Footer` and `Development Link` sections.

**Default choices (phase defaults / v1)**:

- PR label derivation should inherit `issue_top_labels`, `issue_scope_labels`, and `issue_module_labels`, then append any extra `pr_labels`.
- Issue creation under `docs/logs/` should default to project `wordloom Board` unless an explicit project override is present.
- PRs should not inherit the issue project by default; PR project assignment stays blank unless explicitly requested.
- If one PR aggregates multiple whole phases, the PR title should compress them to a phase-range string such as `P0-P3` or `P0+P3-P4`.
- If a PR is a later incremental follow-up rather than a one-shot aggregate, the title should use the exact `P*-C*-S*` unit plus a one-sentence summary.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Fix PR title generation so whole-phase aggregate PRs render compressed phase ranges instead of only `<ID>: <log title>`.
- Inherit structural PR labels from explicit issue-side fields so scope taxonomy does not disappear from the PR sidebar.
- Match the newer body shape around flat execution checklist parsing, structured evidence footer lines, and a separate development-link section.

**PR checklist source**:

- Default source: reuse this log's checked execution checklist items once implementation and sample regeneration are complete.
- No parent override is needed because this follow-up is one direct child phase.

**PR links / evidence footer**:

- Log: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
- Issue: ``
- Runbook: ``
- Evidence artifact: `docs/issues/pr-prep-S0E-4A-sample-plan.json`

## Constraints

- Do not infer PR labels from arbitrary prose; only explicit structured issue-side label fields may flow into PR labels.
- Do not invent a GitHub Project outside the explicit issue default `wordloom Board` rule for `docs/logs/` sources.
- Do not let title compression hide incremental follow-up units; phase-range titles are only for whole-phase aggregate PRs.

## Scope

- `P0`: contract corrections for PR title range compression, structural label inheritance, and body section boundaries
- `P1`: planner/body generator implementation changes
- `P2`: sample regeneration against the existing `S0E-4A` PR-prep artifacts
- `P3`: drills label policy, issue-only default `wordloom Board` project assignment, and live PR audit/write-back

## Success Criteria (DoD)

- Generated PR titles can distinguish whole-phase aggregate PRs from incremental `P*-C*-S*` follow-ups.
- Generated PR labels inherit at least the explicit top/scope/module labels from the same source log.
- Body generation can parse `Execution Checklist` sections even when the heading variant changes.
- `Evidence Footer` and `Development Link` remain separate sections in the generated PR body.
- Issue creation for logs under `docs/logs/` defaults to project `wordloom Board` unless an explicit project override is supplied.
- PR creation stays project-empty by default unless `pr_projects` is explicitly populated.
- Logs with substantive evidence/drill execution derive the `drills` label.

## Stability (what stable means)

- This log can be marked `stable` when:
  - title compression, label inheritance, and body section formatting rules are fixed and validated through regenerated sample artifacts;
  - remaining ambiguity is limited to GitHub auth/project-scope capability rather than local rule definition.

## P0 (Contract | v1)

### P0-C1-S1 (PR title compression rule | v1)

- Whole-phase aggregate PRs should compress contiguous phases as `P0-P3`, sparse phases as `P0+P3`, and mixed sparse/contiguous sets as `P0+P3-P4`.
- Incremental follow-up PRs should not reuse the aggregate style; they should surface the exact `P*-C*-S*` unit in the title.

### P0-C1-S2 (Structural PR labels | v1)

- PR labels should inherit explicit `issue_top_labels`, `issue_scope_labels`, and `issue_module_labels` from the source log before appending extra `pr_labels`.
- The `drills` label is now part of the fixed derivation rule whenever the source log contains substantive evidence/drill execution.

### P0-C1-S3 (Body section boundaries | v1)

- The body generator should treat any `## Execution Checklist...` heading variant as the checklist source section.
- `Evidence Footer` and `Development Link` must remain separate body sections.

## P3 (Projects, drills, and live PR audit | v1)

### P3-C1-S1 (Drills label policy | v1)

- Any log with substantive evidence/drill execution should cause PR label derivation to add `drills`.
- The derivation should stay fail-closed against the repository label set and use the exact existing label name `drills`.

### P3-C1-S2 (Default workspace project | v1)

- Issue creation for logs under `docs/logs/` in the `wordloom-v3` workspace should default to project `wordloom Board` unless an explicit project override is present.
- PR creation should stay project-empty by default; project assignment on PRs is opt-in only.
- Live issue project assignment remains dependent on GitHub CLI token scopes; missing project scopes are an environment/auth constraint, not a contract ambiguity.

### P3-C1-S3 (Live PR audit and correction | v1)

- PR `#294` should be audited against the updated title, label, project, and body-format rules.
- If the live PR drifts from the regenerated local output, title/body/labels should be corrected in place and any default-project noise should be removed from the body.

### P3-C1-S4 (Issue project path | v1)

- The issue-create path should carry the default `wordloom Board` project when the source log lives under `docs/logs/`.
- Real GitHub-side issue project assignment currently fails because the active token still lacks the `project` write scope required by GitHub's `addProjectV2ItemById` mutation.

### P3-C1-S5 (Body title deduplication | v1)

- Generated issue and PR bodies should not repeat the platform-level title as an extra top-level `# ...` heading.
- Mechanical readability should rely on the platform title plus the structured `Metadata` section, not a duplicated body title line.

### P3-C1-S6 (Stacked validation PR base | v1)

- The real `S0E-4B` validation PR currently has to base on `pr-prep/s0e-4a`, not `main`, because `main` does not yet contain the unmerged `S0E-4A` file baseline required for a conflict-free cherry-pick.
- Once `S0E-4A` lands on `main`, `S0E-4B` can later be rebased or re-planned against `main` as the long-term base.

## Plan (draft)

### P1 (Implementation)

- P1-C1-S1: update PR-prep planner title derivation and label/project inheritance
- P1-C1-S2: update body rendering for evidence footer and development-link formatting

### P2 (Validation)

- P2-C1-S1: regenerate `S0E-4A` sample plan/body artifacts with the new rules
- P2-C1-S2: inspect generated title, labels, and body sections for expected output

### P3 (Live audit / write-back)

- P3-C1-S1: roll `drills` auto-label semantics into generator rules
- P3-C1-S2: default docs/logs issue creation to project `wordloom Board`
- P3-C1-S3: audit live PR `#294` and reconcile title/body/labels
- P3-C1-S4: wire issue-create project assignment and record the remaining GitHub-side auth blocker
- P3-C1-S5: remove duplicated top-of-body title from generated issue and PR bodies
- P3-C1-S6: base the real validation PR on `pr-prep/s0e-4a` while `S0E-4A` remains unmerged

## Execution Checklist (unchecked)

- [x] `P0-C1-S1`: title compression rule fixed
- [x] `P0-C1-S2`: structural PR label inheritance fixed
- [x] `P0-C1-S3`: body section boundaries fixed
- [x] `P1-C1-S1`: planner metadata inheritance updated
- [x] `P1-C1-S2`: body renderer footer and development-link formatting updated
- [x] `P2-C1-S1`: sample artifacts regenerated
- [x] `P2-C1-S2`: regenerated output reviewed against expected sidebar/body semantics
- [x] `P3-C1-S1`: `drills` auto-label semantics fixed
- [x] `P3-C1-S2`: default issue-side `wordloom Board` project semantics fixed locally
- [x] `P3-C1-S3`: live PR `#294` reconciled against the new rules
- [x] `P3-C1-S4`: issue-create project path wired locally and GitHub-side blocker recorded
- [x] `P3-C1-S5`: duplicated top-of-body title removed from generated issue and PR bodies
- [x] `P3-C1-S6`: stacked validation PR base fixed to `pr-prep/s0e-4a`

## Evidence

- `P0-C1-S1` / `P1-C1-S1`: `scripts/issues/plan_pr_prep.py` now derives aggregate PR titles from the selected commit phase set instead of always using `<ID>: <log title>`.
- `P0-C1-S2` / `P1-C1-S1`: `scripts/issues/plan_pr_prep.py` now inherits PR labels from explicit issue-side structural labels and may reuse `issue_projects` when that field is explicitly populated.
- `P0-C1-S3` / `P1-C1-S2`: `scripts/issues/plan_pr_prep.py` and `scripts/issues/create_pr_from_plan.py` now preserve separate `Evidence Footer` and `Development Link` sections and accept broader `Execution Checklist` heading variants.
- `P2-C1-S1` / `P2-C1-S2`: `docs/issues/pr-prep-S0E-4A-sample-plan.json` now renders `S0E-4A/P0-P3: GitHub pull request automation contract v1`, carries `EVOLUTION, s0/knowledge system, sub/1`, and the matching body preview now shows separate `Evidence Footer` and `Development Link` sections.
- `P3-C1-S1`: `scripts/issues/plan_pr_prep.py` now adds `drills` when the source log contains substantive evidence/drill execution.
- `P3-C1-S2`: `scripts/issues/gen_issue_draft.py` now defaults issue projects for `docs/logs/*` sources to `wordloom Board`, while `scripts/issues/plan_pr_prep.py` leaves PR projects empty unless `pr_projects` is explicitly populated.
- `P3-C1-S3`: live PR `#294` now uses title `S0E-4A/P0-P3: GitHub pull request automation contract v1`, carries labels `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`, and has been updated to the regenerated body shape with separate `Execution Checklist`, `Evidence Footer`, and `Development Link` sections without default project noise.
- `P3-C1-S3`: generated `Execution Checklist` lines now preserve backticks around the `P*-C*-S*` identifier segment so the rendered PR body matches the log-side checklist style.
- `P3-C1-S4`: issue-create now has a real project-assignment path, but GitHub-side project resolution remains blocked in the current environment by project lookup/auth limitations.
- `P3-C1-S5`: generated issue and PR bodies now start directly at `## Metadata`, removing the redundant top-level title heading while keeping machine-readable structure intact.
- `P3-C1-S6`: a first attempt to create the real `S0E-4B` PR from `main` failed on cherry-pick because the selected commit depends on unmerged `S0E-4A` file changes; the validation PR base is therefore temporarily stacked on `pr-prep/s0e-4a`.
- `P3-C1-S4`: a real `S0E-4B` issue-create attempt now fails specifically on `addProjectV2ItemById`, proving that `read:project` alone is insufficient and the active token still needs the `project` write scope.

## Recent changes (for traceability, optional)

- 2026-03-29: opened `S0E-4B` as a narrow follow-up to `S0E-4A` after reviewing the first real PR output and identifying title, label, and body-format drift.
- 2026-03-29: regenerated the `S0E-4A` sample artifacts and verified that title compression, structural PR labels, and the updated body footer/link layout now match the intended output.
- 2026-03-29: updated the project policy so `wordloom Board` defaults only on issue creation, not on PR creation, then reconciled live PR `#294` to remove default project noise.
- 2026-03-29: aligned generated PR checklist formatting so checklist IDs render as `` `P*-C*-S*` `` instead of plain text.
- 2026-03-29: removed duplicated top-of-body title headings from generated issue and PR bodies so body structure starts at `Metadata`.
- 2026-03-29: attempted a real `S0E-4B` issue create after enabling project reads; GitHub now exposes the exact remaining blocker: the token still lacks the `project` write scope needed to add the issue to `wordloom Board`.
- 2026-03-29: attempted a real `S0E-4B` PR from `main`, observed a cherry-pick conflict against the unmerged `S0E-4A` baseline, and switched the validation base to `pr-prep/s0e-4a`.