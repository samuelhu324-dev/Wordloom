# log-S0E-2D (Phase 2D: Issue Creation Metadata and English Body Contract)

---

**id**: `S0E-2D`
**kind**: `log`
**title**: `issue creation metadata enrichment and English body contract v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Automation, epic/s0, sub/0e2d`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/297`
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  **reference_log_1**: `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
  **reference_log_2**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **reference_log_3**: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
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
**pr_base**: ``
**pr_development_issue**: ``
**created**: `2026-03-29`
**updated**: `2026-04-02`

---

## Decision / Outcome

**Decision**:

- `S0E-2D` reopens the issue-automation line after `S0E-2C` so issue creation can carry richer pre-create metadata instead of stopping at draft generation plus dry-run reconciliation.
- v1 promotes milestone, relationship, and project ownership into the issue-create contract before the real GitHub issue is created.
- Generated GitHub issue content must be English-only, and the body should stay structurally present without auto-writing final `Context` or `Definition of Done (DoD)` prose.
- The lifecycle order is fixed as: `Issue Creation -> Logs completed -> PR -> human merge -> Issue Conclusion`.

**Default choices (phase defaults / v1)**:

- `issue_milestone` remains the first-class explicit source; if it is blank, automation may only derive a milestone from exact `roadmap_path + roadmap_milestone + roadmap_phase` bridge data fixed by `S0E-3A`.
- Relationship ownership must come from explicit metadata such as `issue_parent` or a controlled issue/log mapping; title similarity and prose similarity remain out of scope.
- For child logs that already declare `parent_log`, issue creation may derive `issue_parent` from the parent log's exact `links.issue`; top-level issues with no `parent_log` omit the `Parent issue` field entirely.
- When rendered, `Parent issue` belongs only in `Metadata` and should use plain-text short GitHub issue reference form such as `#248`.
- `issue_projects` is authoritative when explicitly populated; otherwise the existing `docs/logs/* -> wordloom Board` default still applies.
- Generated issue bodies must be English-only even when the source log is bilingual.
- The generated issue body should keep the section structure `Metadata -> Context -> Definition of Done (DoD) -> Links`, but automation should only fill metadata and deterministic links by default.
- `Metadata` should keep issue-state rows only, while deterministic navigation rows such as `Log`, `Runbook`, `Roadmap`, `Parent log`, and optional `Previous log` belong in `Links`.
- `Context` and `Definition of Done (DoD)` remain intentionally unexpanded during creation v1 unless an operator supplies explicit overrides.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Enrich issue creation so milestone, parent issue, project, and body-shape metadata are resolved deterministically before a real GitHub issue is created.
- Keep generated issue bodies English-only and structurally complete while leaving `Context` and `Definition of Done (DoD)` intentionally blank at creation time.
- Align child issue metadata with parent-log inheritance so `Parent issue` can be rendered as a stable short GitHub ref such as `#248`.

**PR checklist source**:

- Default source: reuse this log's checked execution checklist items for the generated PR checklist block.

**PR links / evidence footer**:

- Log: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/297`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/pr-prep-S0E-2D-sample-plan.json`

## Definitions (optional)

- **Issue creation metadata**: the machine-applied issue fields decided before the real GitHub issue exists, such as milestone, parent issue, project, labels, and source-log links.
- **Relationship**: an explicit parent/child or tracking link between issues or between a source log and its known parent issue.
- **English-only issue body**: the rule that generated GitHub issue markdown uses English headings and English machine-filled content even if the source log mixes Chinese and English.
- **Deterministic links**: links that can be copied directly from stable metadata such as source log path, runbook path, roadmap path, parent issue URL, or parent log path.

## Constraints

- Do not infer milestone from prose when the roadmap bridge is blank or ambiguous.
- Do not infer relationships from naming similarity or body text.
- Do not auto-write bilingual or Chinese issue body text.
- Do not auto-summarise final `Context` or `Definition of Done (DoD)` prose during issue creation.
- Do not treat project assignment as PR metadata; this slice remains issue-creation-only.

## Scope

- `P0`: contract for milestone, relationship, project, language, and body-structure rules at issue-creation time
- `P1`: metadata resolution and English issue-body scaffold rules
- `P2`: dry-run validation against representative logs that already carry roadmap and relationship metadata
- `P3`: real issue-create validation plus explicit write-back of enriched issue metadata

## Success Criteria (DoD)

- The issue-create contract can carry milestone, parent issue/relationship, and project data before real GitHub issue creation.
- Milestone derivation is explicitly tied to frontmatter or exact roadmap bridge fields rather than prose guessing.
- The generated issue body is English-only.
- `Context` and `Definition of Done (DoD)` remain structurally present but are not auto-written as final prose during creation.
- `Links` contain only deterministic references such as log, runbook, roadmap, parent log, and optional previous log when those inputs are explicitly available.
- `Parent issue` remains metadata-only and must not be repeated inside `Links`.
- The contract explains how enriched issue creation still stays fail-closed when milestone, relationship, or project data is missing.

## Stability (what stable means)

- This log can be marked `stable` when:
  - milestone, relationship, project, and English-body rules are fixed and exercised through at least one dry-run plus one real issue-create path;
  - issue creation no longer depends on ad hoc operator memory for milestone/project/relationship attachment.

## P0 (Contract | v1)

### P0-C1-S1 (Milestone and roadmap bridge precedence | v1)

- `issue_milestone` is the explicit first-choice field when the operator already knows the target GitHub milestone.
- If `issue_milestone` is blank, automation may only consult exact roadmap bridge metadata from `S0E-3A`; no prose-only fallback is allowed.
- If neither explicit milestone nor exact bridge metadata exists, the issue milestone must remain blank and the run should report that gap explicitly.

### P0-C1-S2 (Relationship and project attachment | v1)

- `issue_parent` is the primary explicit relationship field for issue-create v1.
- If `issue_parent` is blank but the source log declares `parent_log`, issue creation may derive the parent issue from that parent log's exact `links.issue`.
- Top-level logs with no `parent_log` do not render a `Parent issue` row in the issue body.
- If rendered, `Parent issue` appears only in `Metadata`, not in `Links`, and uses plain-text short GitHub issue reference form.
- `issue_projects` is authoritative when present; otherwise the existing workspace default project rule remains the only allowed fallback.
- Missing relationship or project metadata must remain blank or skipped rather than guessed.

### P0-C1-S3 (English body scaffold and link boundary | v1)

- The generated issue body must use English section headings and English machine-filled content only.
- The body shape should be:

```md
## Metadata

- Labels: `...`
- Projects: `...`
- Milestone: `...`
- Parent issue: #248

## Context

## Definition of Done (DoD)

## Links

- Log: `...`
- Runbook: `...`
- Roadmap: `...`
- Parent log: `...`
- Previous log: `...`
```

- `Context` and `Definition of Done (DoD)` remain intentionally empty unless the operator supplies explicit text.
- `Links` should only include deterministic references already known from frontmatter or controlled overrides, excluding `Parent issue` which belongs only in `Metadata` and excluding log-only `reference_log_*` rows.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-2D/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S0E-2D` work should stay on the active `S0E-*` branch until the enriched issue-create path needs its own focused review slice.

**Commit discipline (recommended)**:

- Fix metadata precedence and English body structure first, then validate dry-run issue output, then attempt real enriched issue creation and write-back.

## Plan (draft)

### P1 (Metadata and body rules)

- P1-C1-S1: define milestone, project, and relationship precedence for issue creation
- P1-C1-S2: define the English-only body scaffold with empty `Context` and `Definition of Done (DoD)` sections
- P1-C2-S1: derive child `issue_parent` from explicit metadata first and then from the parent log's exact `links.issue`
- P1-C2-S2: omit `Parent issue` from top-level issue bodies that have no `parent_log`
- P1-C2-S3: render `Parent issue` only in `Metadata` and normalize it to short GitHub issue reference form
- P1-C2-S4: render `Parent issue` as plain text instead of code-formatted text

### P2 (Dry-run validation)

- P2-C1-S1: validate enriched issue drafts against representative logs that already carry exact roadmap bridge metadata
- P2-C1-S2: verify deterministic `Links` output and fail-closed blank handling for missing milestone/project/relationship fields, including the current blank `issue_parent` baseline

### P3 (Real issue-create validation)

- P3-C1-S1: audit one legacy real issue-create artifact against the current creation-body contract and remove obsolete body content
- P3-C2-S1: create one real GitHub issue using the current enriched metadata path
- P3-C2-S2: write back the resulting issue URL and record which milestone/project/relationship fields were applied versus skipped
- P3-C3-S1: validate child parent-issue derivation against the real `S0E` issue and confirm top-level issue bodies omit `Parent issue`
- P3-C3-S2: audit existing sibling `S0E` child issues and align metadata-only parent-issue formatting plus structural labels where the current contract requires them
- P3-C3-S3: update live child issues so `Parent issue` renders as plain text instead of a code span

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: milestone and roadmap bridge precedence fixed
- [x] `P0-C1-S2`: relationship and project attachment rules fixed
- [x] `P0-C1-S3`: English body scaffold and link boundary fixed

### P1 (Metadata and body rules)

- [x] `P1-C1-S1`: issue-create metadata precedence defined
- [x] `P1-C1-S2`: English-only issue-body scaffold fixed
- [x] `P1-C2-S1`: child parent-issue derivation fixed
- [x] `P1-C2-S2`: top-level parent-issue suppression fixed
- [x] `P1-C2-S3`: parent-issue rendering placement and format fixed
- [x] `P1-C2-S4`: parent-issue plain-text rendering fixed

### P2 (Dry-run validation)

- [x] `P2-C1-S1`: enriched issue draft validation completed
- [x] `P2-C1-S2`: deterministic links and blank-field fallback verified

### P3 (Real issue-create validation)

- [x] `P3-C1-S1`: legacy real issue-create artifact audited and remediated against the current body contract
- [x] `P3-C2-S1`: one real enriched issue-create run completed
- [x] `P3-C2-S2`: write-back and applied/skipped metadata accounting recorded
- [x] `P3-C3-S1`: child parent-issue derivation and top-level omission verified
- [x] `P3-C3-S2`: sibling `S0E` child-issue audit and remediation completed
- [x] `P3-C3-S3`: live child-issue plain-text parent rendering completed

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

- `P1-C1-S1`: `scripts/issues/gen_issue_draft.py` now resolves milestone precedence as `milestone_override -> issue_milestone -> exact roadmap bridge -> blank`, keeps `issue_parent` explicit, and preserves `issue_projects` as explicit-or-default metadata.
- `P1-C1-S2`: `scripts/issues/gen_issue_draft.py` now emits an English-only issue scaffold with intentionally blank `Context` and `Definition of Done (DoD)` sections instead of copying bilingual log prose.
- `P1-C1-S1` / `P1-C1-S2`: `docs/runbook/run-S0E-log-to-issue-creation.md` now records the same milestone, relationship, project, and English-body rules for operators.
- `P1-C2-S1` / `P1-C2-S2`: `scripts/issues/gen_issue_draft.py` now derives child `issue_parent` from the parent log's exact `links.issue` when available, while omitting the `Parent issue` row entirely for top-level logs with no `parent_log`.
- `P1-C2-S1` / `P1-C2-S2`: `docs/runbook/run-S0E-log-to-issue-creation.md` now records the same parent-issue precedence and top-level omission rules for operators.
- `P1-C2-S3`: `scripts/issues/gen_issue_draft.py` now renders `Parent issue` only in `Metadata` and normalizes GitHub issue URLs or raw numbers to short references such as `#248`.
- `P1-C2-S3`: `docs/runbook/run-S0E-log-to-issue-creation.md` now records the same metadata-only placement and short-reference formatting rule.
- `P1-C2-S4`: `scripts/issues/gen_issue_draft.py` now renders `Parent issue` as plain text `#248` instead of wrapping it in code formatting.
- `P1-C2-S4`: `docs/runbook/run-S0E-log-to-issue-creation.md` and this log now record the same plain-text rendering rule.
- `P2-C1-S1`: `docs/issues/issue-S4E-5B-execution-layer-enforcement-and-controlled-exceptions.md` and [docs/issues/issue-S4E-5B-execution-layer-enforcement-and-controlled-exceptions.json](docs/issues/issue-S4E-5B-execution-layer-enforcement-and-controlled-exceptions.json) now validate a mainline-roadmap sample where milestone `M5` is derived from exact bridge metadata and deterministic links remain limited to log, runbook, and parent log.
- `P2-C1-S1`: `docs/issues/issue-S4A-1A-ops-scripting-baseline.md` and [docs/issues/issue-S4A-1A-ops-scripting-baseline.json](docs/issues/issue-S4A-1A-ops-scripting-baseline.json) now validate a branch-roadmap sample where milestone `M1` is derived from exact bridge metadata and the English-only empty-body scaffold remains stable.
- `P2-C1-S2`: both representative runs kept `issue_parent` blank and emitted explicit warnings instead of guessing a parent relationship, proving the current fail-closed baseline for missing relationship metadata.
- `P3-C1-S1`: live issue `#288` (`S0E-2B`) was audited against the current creation-body contract and updated so the body no longer repeats the top-level title and no longer carries prefilled `Context` or `Definition of Done (DoD)` prose.
- `P3-C2-S1`: `docs/issues/issue-S0E-2D-issue-creation-metadata-and-english-body-contract.json` now records a real `create-issue` run that created issue `#297` on `wordloom Board` with the current English-only empty-body scaffold.
- `P3-C2-S2`: `links.issue` now points to `#297`, and the applied-vs-skipped metadata outcome is explicit: applied labels `EVOLUTION`, `s0/knowledge system`, `sub/1` plus project `wordloom Board`; skipped milestone and parent relationship remained blank by contract.
- `P3-C3-S1`: `docs/logs/log-S0E-docs-management-v5.md` now records the real top-level issue `#248`; regenerated child artifacts for `S0E-2B` and `S0E-2D` now derive `Parent issue` from that exact link, while `artifacts/_tmp_issue-S0E-docs-management-v5.json` confirms top-level `S0E` issue bodies omit the `Parent issue` row entirely.
- `P3-C3-S2`: sibling live issues `#289`, `#293`, and `#295` were audited and remediated to the same creation-body contract: no duplicated title, no prefilled `Context/DoD`, metadata-only `Parent issue: #248`, and no repeated parent issue inside `Links`; issue `#293` also received the `drills` label to match current structural-label derivation.
- `P3-C3-S3`: live child issues `#288`, `#289`, `#293`, `#295`, and `#297` were updated so `Parent issue` stays metadata-only and renders as plain text `#248` rather than a code span.

## Recent changes (for traceability, optional)

- 2026-03-29: opened `S0E-2D` to bring milestone, relationship, project, and English issue-body rules into the issue-create contract after `S0E-2C` and `S0E-3A`.
- 2026-03-29: completed `P1` by updating the draft generator and runbook so issue creation now uses enriched metadata precedence and an English-only empty-body scaffold.
- 2026-03-29: completed `P1-C2` by teaching issue creation to derive child parent issues from parent-log `links.issue` and to omit `Parent issue` entirely for top-level issues.
- 2026-03-29: completed `P1-C2-S3` by moving `Parent issue` to `Metadata` only and normalizing it to short GitHub issue references such as `#248`.
- 2026-03-29: completed `P1-C2-S4` by rendering `Parent issue` as plain text `#248` instead of code-formatted text.
- 2026-03-29: completed `P2` by validating enriched draft output against `S4E-5B` and `S4A-1A`, confirming roadmap-derived milestones, deterministic links, and blank relationship fallback.
- 2026-03-29: completed `P3` by auditing legacy issue `#288` against the current creation-body contract and creating the current `S0E-2D` real sample as issue `#297` with write-back recorded.
- 2026-03-29: completed follow-up `P1-C2` / `P3-C3` validation by wiring child issues to the real top-level `S0E` issue `#248` through `parent_log.links.issue` and confirming top-level issue bodies omit `Parent issue`.
- 2026-03-29: completed sibling issue audit for `#289`, `#293`, and `#295`, aligning them to metadata-only short parent-issue formatting and updating `#293` labels to match current `drills` derivation.
- 2026-03-29: updated live child issues `#288`, `#289`, `#293`, `#295`, and `#297` so `Parent issue` now renders as plain text `#248`.
- 2026-03-30: added explicit `PR Summary Inputs` so regenerated `S0E-2D` PR-prep artifacts no longer depend on placeholder `Summary` content.
- 2026-03-30: sidebar parent-child relationship `#248 -> #297` was attached during the `S0E-4D/P4` audit, confirming that metadata-only `Parent issue: #248` in the body was not sufficient proof of a live GitHub sidebar relationship.
