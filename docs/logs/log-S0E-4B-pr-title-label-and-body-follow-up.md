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
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/296`
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
- Stacked PRs should be interpreted by their compare base and `Files changed` delta, not by GitHub's full head-branch commit ancestry list.

**Default choices (phase defaults / v1)**:

- PR label derivation should inherit `issue_top_labels`, `issue_scope_labels`, and `issue_module_labels`, then append any extra `pr_labels`.
- Issue creation under `docs/logs/` should default to project `wordloom Board` unless an explicit project override is present.
- PRs should not inherit the issue project by default; PR project assignment stays blank unless explicitly requested.
- If one PR aggregates multiple whole phases, the PR title should compress them to a phase-range string such as `P0-P3` or `P0+P3-P4`.
- Phase-range title derivation should prefer the source log's completed checklist coverage over the selected commit phase set; selected commits define branch content, not the user-facing completion span.
- If a PR is a later incremental follow-up rather than a one-shot aggregate, the title should use the exact `P*-C*-S*` unit plus a one-sentence summary.
- The long-lived `S0E-*` working branch remains the mixed authoring lane for the spine and its child logs; `pr-prep/*` branches are derived review artifacts, not replacements for the working branch.

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
- Do not treat GitHub's stacked PR commit timeline as the authoritative review delta when the PR base is another unmerged PR branch.

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
- Stacked PR review guidance makes clear that `Files changed` and compare-base semantics are authoritative, while full commit ancestry is only traceability context.
- Parent/spine logs and child phase logs have a clear branch-lifecycle policy instead of creating ad hoc permanent top-level branches for every PR.

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

### P3-C1-S7 (Stacked PR review semantics | v1)

- When one PR targets another PR-prep branch, GitHub may show upstream commits from the head branch ancestry in the `Commits` tab or timeline.
- In that stacked state, the authoritative review scope is the compare relation `base <- head`, as reflected by the base branch, compare UI, and `Files changed`, not every ancestor commit shown in the timeline.
- Operators should treat repeated upstream commits in a stacked PR as ancestry context unless the compare delta itself still contains those changes.

### P3-C1-S8 (Title phase-span precedence | v1)

- Aggregate PR titles should derive their phase span from the source log's completed execution coverage first, not from the subset of commits created during the latest push.
- Selected commits still decide what lands on the PR branch, but they must not make an already-completed `P0-P2` contract log look like a `P3`-only delivery.
- If the completed checklist spans multiple phases, the title should render the compressed phase range even when the selected commits only belong to the last implementation phase.

### P3-C1-S9 (Working branch and spine-log policy | v1)

- The long-lived `S0E-docs-management-v5` branch remains useful as the mixed authoring branch for the active spine and its child logs; it is the place where parent/spine ledger updates naturally accumulate.
- `pr-prep/*` branches are short-lived review branches created from an explicit base for one PR; they should not replace the mixed working branch and should not be used as the general place to continue authoring the whole spine.
- Parent/spine logs should default to landing on the mixed working branch first; if the parent itself needs a reviewable slice, create either an explicit child phase/follow-up log or an intentional aggregate PR from that working branch rather than inventing another permanent top-level branch.

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
- P3-C1-S7: record stacked PR review semantics so duplicate upstream commits are not misread as duplicated delivery
- P3-C1-S8: make title phase-span derivation prefer completed checklist coverage over selected commit phases
- P3-C1-S9: clarify the role of the mixed working branch versus short-lived `pr-prep/*` review branches

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
- [x] `P3-C1-S7`: stacked PR review semantics documented against GitHub's ancestry-heavy commit views
- [x] `P3-C1-S8`: title phase-span derivation switched to prefer completed checklist coverage
- [x] `P3-C1-S9`: mixed working branch and parent-log landing policy clarified

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
- `P3-C1-S7`: the `S0E-4B` validation PR exposed that GitHub's stacked PR commit views can repeat already-reviewed upstream commits from the base PR branch ancestry; the review contract now treats compare-base semantics and `Files changed` as authoritative.
- `P3-C1-S8`: `scripts/issues/plan_pr_prep.py` now prefers checked execution-checklist phase coverage when deriving aggregate PR titles, so logs that already completed `P0-P2` at creation time still render `P0-P3` after the implementation-phase commits land.
- `P3-C1-S9`: the branch policy is now explicit: `S0E-docs-management-v5` remains the mixed authoring branch for the spine and parent-log ledger work, while `pr-prep/*` branches are short-lived review artifacts for one PR each.
- `P3-C1-S8`: live PR `#296` has been retitled from the commit-only `P3-C1-...` form to the checklist-derived aggregate form `S0E-4B/P0-P3: PR title compression, structural label inheritance, and body footer follow-up v1`.

## Recent changes (for traceability, optional)

- 2026-03-29: opened `S0E-4B` as a narrow follow-up to `S0E-4A` after reviewing the first real PR output and identifying title, label, and body-format drift.
- 2026-03-29: regenerated the `S0E-4A` sample artifacts and verified that title compression, structural PR labels, and the updated body footer/link layout now match the intended output.
- 2026-03-29: updated the project policy so `wordloom Board` defaults only on issue creation, not on PR creation, then reconciled live PR `#294` to remove default project noise.
- 2026-03-29: aligned generated PR checklist formatting so checklist IDs render as `` `P*-C*-S*` `` instead of plain text.
- 2026-03-29: removed duplicated top-of-body title headings from generated issue and PR bodies so body structure starts at `Metadata`.
- 2026-03-29: attempted a real `S0E-4B` issue create after enabling project reads; GitHub now exposes the exact remaining blocker: the token still lacks the `project` write scope needed to add the issue to `wordloom Board`.
- 2026-03-29: attempted a real `S0E-4B` PR from `main`, observed a cherry-pick conflict against the unmerged `S0E-4A` baseline, and switched the validation base to `pr-prep/s0e-4a`.
- 2026-03-29: clarified that stacked PR commit timelines may repeat upstream commits from the base PR ancestry, so review scope should be read from the compare base and `Files changed` instead.
- 2026-03-29: changed aggregate PR title derivation to prefer the source log's completed checklist phases, preventing already-completed earlier phases from disappearing from the title just because the latest push only added `P3` commits.
- 2026-03-29: fixed the branch policy wording so the mixed `S0E-docs-management-v5` branch remains the authoring lane for spine/parent-log work, while `pr-prep/*` branches stay temporary review-only branches.
- 2026-03-29: wrote back the live validation PR link `#296` and aligned its title to the new checklist-first phase-span rule.