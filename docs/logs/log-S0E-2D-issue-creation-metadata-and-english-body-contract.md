# log-S0E-2D (Phase 2D: Issue Creation Metadata and English Body Contract)

---

**id**: `S0E-2D`
**kind**: `log`
**title**: `issue creation metadata enrichment and English body contract v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Automation, epic/s0, sub/0e2d`
**links**: ``
  **issue**: ``
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
**updated**: `2026-03-29`

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
- `issue_projects` is authoritative when explicitly populated; otherwise the existing `docs/logs/* -> wordloom Board` default still applies.
- Generated issue bodies must be English-only even when the source log is bilingual.
- The generated issue body should keep the section structure `Metadata -> Context -> Definition of Done (DoD) -> Links`, but automation should only fill metadata and deterministic links by default.
- `Context` and `Definition of Done (DoD)` remain intentionally unexpanded during creation v1 unless an operator supplies explicit overrides.

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
- `Links` contain only deterministic references such as source log, runbook, roadmap, parent log, and parent issue when those inputs are explicitly available.
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
- If a source log also carries deterministic parent-log or roadmap references, those may appear in `Links`, but they do not replace explicit `issue_parent` for GitHub-side relationship attachment.
- `issue_projects` is authoritative when present; otherwise the existing workspace default project rule remains the only allowed fallback.
- Missing relationship or project metadata must remain blank or skipped rather than guessed.

### P0-C1-S3 (English body scaffold and link boundary | v1)

- The generated issue body must use English section headings and English machine-filled content only.
- The body shape should be:

```md
## Metadata

- Title: `...`
- Labels: `...`
- Projects: `...`
- Milestone: `...`
- Source log: `...`
- Parent issue: `...`

## Context

## Definition of Done (DoD)

## Links

- Log: `...`
- Runbook: `...`
- Roadmap: `...`
- Parent log: `...`
- Parent issue: `...`
```

- `Context` and `Definition of Done (DoD)` remain intentionally empty unless the operator supplies explicit text.
- `Links` should only include deterministic references already known from frontmatter or controlled overrides.

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

### P2 (Dry-run validation)

- P2-C1-S1: validate enriched issue drafts against logs that already carry roadmap and relationship metadata
- P2-C1-S2: verify deterministic `Links` output and fail-closed blank handling for missing milestone/project/relationship fields

### P3 (Real issue-create validation)

- P3-C1-S1: create one real GitHub issue using the enriched metadata path
- P3-C1-S2: write back the resulting issue URL and record which milestone/project/relationship fields were applied versus skipped

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: milestone and roadmap bridge precedence fixed
- [x] `P0-C1-S2`: relationship and project attachment rules fixed
- [x] `P0-C1-S3`: English body scaffold and link boundary fixed

### P1 (Metadata and body rules)

- [x] `P1-C1-S1`: issue-create metadata precedence defined
- [x] `P1-C1-S2`: English-only issue-body scaffold fixed

### P2 (Dry-run validation)

- [ ] `P2-C1-S1`: enriched issue draft validation completed
- [ ] `P2-C1-S2`: deterministic links and blank-field fallback verified

### P3 (Real issue-create validation)

- [ ] `P3-C1-S1`: one real enriched issue-create run completed
- [ ] `P3-C1-S2`: write-back and applied/skipped metadata accounting recorded

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

- `P1-C1-S1`: `scripts/issues/gen_issue_draft.py` now resolves milestone precedence as `milestone_override -> issue_milestone -> exact roadmap bridge -> blank`, keeps `issue_parent` explicit, and preserves `issue_projects` as explicit-or-default metadata.
- `P1-C1-S2`: `scripts/issues/gen_issue_draft.py` now emits an English-only issue scaffold with intentionally blank `Context` and `Definition of Done (DoD)` sections instead of copying bilingual log prose.
- `P1-C1-S1` / `P1-C1-S2`: `docs/runbook/run-S0E-log-to-issue-creation.md` now records the same milestone, relationship, project, and English-body rules for operators.

## Recent changes (for traceability, optional)

- 2026-03-29: opened `S0E-2D` to bring milestone, relationship, project, and English issue-body rules into the issue-create contract after `S0E-2C` and `S0E-3A`.
- 2026-03-29: completed `P1` by updating the draft generator and runbook so issue creation now uses enriched metadata precedence and an English-only empty-body scaffold.
