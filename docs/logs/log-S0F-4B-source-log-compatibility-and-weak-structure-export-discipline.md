# log-S0F-4B (Phase 4B: source-log compatibility and weak-structure export discipline)

---

**id**: `S0F-4B`
**kind**: `log`
**title**: `source-log compatibility and weak-structure export discipline v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Workflow, Automation, epic/s0, sub/4b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
  **reference_log_1**: `docs/logs/_template-log-parent-epic-spine.md`
  **reference_log_2**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_3**: `docs/logs/log-S0F-1K-lifecycle-exact-path-successor-package.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/4`
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
**created**: `2026-04-07`
**updated**: `2026-04-07`

---

## Decision / Outcome

**Decision**:

- `S0F-4B` fixes the compatibility rule between the old source-log templates and the `S0F-4A` six-outlet model.
- The canonical source-log families remain the old two templates only:
  - `docs/logs/_template-log-parent-epic-spine.md`
  - `docs/logs/_template-log-phase-drills-evidence.md`
- Six outlets now act only as weak-structure export ownership. They do not authorize replacing source-log strong structure with a mixed-role ledger shape.
- `S0F-1K` remains a bounded historical sample for one restructuring episode; it is not the default template for future issue-source or PR-source logs.
- The next follow-up should therefore split cleanly into two bounded lanes rather than reopening template shape drift:
  - one old-log weak-structure export inventory lane
  - one explicit script-side source-log admission and fail-closed gating lane

**Default choices (phase defaults / v1)** (optional, but recommended):

- Future parent/child source logs must still start from the old two canonical templates.
- Source-log strong structure should remain in place unless a later explicit automation contract authorizes a different reader model.
- Weak-structure content should move out first; source-log skeleton should remain automation-safe.
- When slimming historical logs, prefer `source skeleton retained + repeated weak structure exported` over `source log hollowed out + reader guesswork added`.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S0F-4B` fixes source-log compatibility rules that later documentation and automation work may reference directly.
- `PR Summary Inputs` remains an automation-facing source block and must not be replaced by outlet prose.
- `Evidence Footer Source` remains optional and must stay explicit; no footer lines may be inferred from narrative export notes.

**PR summary bullets**:

- Reaffirm the old parent/child templates as the only canonical source-log families for future issue and PR automation inputs.
- Narrow six outlets to weak-structure export ownership so logs can slim down without deleting automation-facing strong structure.
- Keep `S0F-1K` as a historical restructuring sample only, not as a future default source-log format.

**PR checklist source**:

- Default source: reuse this log's execution checklist for any future governance PR that publishes the compatibility rule.
- No outlet-export note may replace this checklist as the source for generated PR checklist rows.

**PR links**:

- Log: `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`
- Previous log: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`

## Exported Sections / Outlet Ownership (optional)

- This section governs only weak-structure export.
- The source-log minimum core for active automation-facing logs remains in the source log:
  - `Decision / Outcome`
  - `PR Summary Inputs`
  - `Execution Checklist`
  - `Current Status`
  - `Evidence`
- Old logs should slim by moving repeated narrative, operator detail, family summary, and placement discussion out to the correct outlets while retaining the strong-structure blocks in place.

**Outlet ownership**:

- `contract`: stable current rule text and long-form normative semantics
- `runbook`: stable repeatable operator procedure and troubleshooting steps
- `view`: bounded reader summary or family interpretation
- `index/front-door`: current navigation and entrypoint discovery
- `disposition/placement`: support-only, legacy, stub, and cleanup standing
- `log-retained core`: source-log metadata, decision, automation-facing source blocks, checklist, status, evidence, and minimum bridge notes

## S0F-1K Handling

- `S0F-1K` remains valid as one bounded restructuring ledger for the executed `S0F-1I` exact-path package.
- `S0F-1K` must not be reused as a positive template precedent for future issue-source or PR-source logs.
- Future readers should interpret `S0F-1K` as a historical sample that showed why six-outlet export needs to be narrowed back to weak-structure ownership under the old source-log families.
- If a future slice wants to cite `S0F-1K`, it should cite it only for the bounded restructuring result, not for source-log template selection.

## Definitions (optional)

- **strong structure**: the source-log blocks automation or lifecycle readers depend on directly
- **weak structure**: repeated narrative, explanations, summaries, or placement detail that can be exported without breaking automation
- **canonical source-log family**: one of the two old templates that remain the approved starting point for future parent/child logs

## Constraints

- Do not treat six outlets as permission to invent a third default source-log template.
- Do not delete or hollow out automation-facing source blocks during weak-structure export.
- Do not reuse `S0F-1K` as the default source-log shape for new slices.
- If a future automation reader wants to stop reading whole sections and switch to field-level extraction, that change must land first as an explicit automation contract rather than as silent documentation drift.

## Scope

- `P0`: compatibility contract for old templates versus six outlets
- `P1`: template updates that add thin export-ownership guidance without rewriting old strong-structure sections
- `P2`: fix the weak-structure export map and the retained source-log minimum core
- `P3`: leave one explicit follow-up boundary for future script-side source-log admission and fail-closed gating
- `P4`: record the immediate next-documentation lane as old-log weak-structure export inventory rather than another template experiment

## Success Criteria (DoD)

- The repo has one explicit written rule that future source logs must still start from the old two templates.
- Six outlets are documented as weak-structure export ownership rather than a replacement source-log format.
- The template updates stay thin and do not delete or semantically rewrite the old strong-structure sections.
- One explicit next-step boundary remains for script-side source-log admission rather than hiding that work inside template prose.
- One explicit next-step boundary remains for old-log weak-structure export inventory rather than mixing inventory work into this compatibility rule.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the canonical-template rule and weak-structure export rule are both written into the old template family and referenced from the active governance lineage
  - the next script-side admission/gating follow-up is explicitly bounded rather than implied

## P0 (Contract | v1)

### P0-C1-S1 (Canonical source-log family rule | v1)

- Future parent/child logs must continue to start from the old parent/spine and child/phase templates.
- `S0F-1K` does not become the third default source-log family; it remains a bounded historical restructuring sample only.

### P0-C1-S2 (Six-outlet compatibility rule | v1)

- Six outlets remain valid, but only as export destinations for weak-structure content.
- The outlet model must not be used to justify deleting strong-structure source-log sections that automation or lifecycle readers still consume.

### P0-C1-S3 (Evidence contract | v1)

- Template-level compatibility changes must record the exact files touched and retain one traceable source log for the rule itself.
- Later script-side admission or fail-closed gate work should open as a separate follow-up instead of being hidden inside this same compatibility edit.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `<ID>/P0-P3: <log title>`
  - discontinuous phases: `<ID>/P0+P3: <log title>`
  - mixed discontinuous + consecutive phases: `<ID>/P0+P3-P4: <log title>`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `<ID>/P*-C*-S*: <one-sentence summary>`.

**Branch convention**:

- For logs tied to a specific scope/index (for example, `S5B-3A` belongs to `S5B`, and `S0D-2A` belongs to `S0D`), prefer making P* code and documentation changes on a working branch with the same prefix:
  - For example, `S5B-3A` changes should usually land on an `S5B-*` branch such as `S5B-security-governance-hard-gates`.
  - `S0D-2A` style meta/docs/automation changes should usually land on an `S0D-*` branch such as `S0D-docs-management-v4`.
- If a single PR touches multiple scopes/indexes, prefer splitting it into multiple PRs so each PR stays focused on one scope/index and its corresponding branch for easier aggregation and traceability.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.
- The normal rhythm is: accumulate commits on the matching scope branch at `P*-C*-S*` granularity, then periodically open a PR from that branch into `main` for human review and merge.

## Plan (draft)

### P1 (Template compatibility)

- P1-C1-S1: add one thin export-ownership block to the old parent/spine template
- P1-C1-S2: add one thin export-ownership block and one status reminder to the old child/phase template

### P2 (Minimum core and export discipline)

- P2-C1-S1: define source-log minimum core versus weak-structure export boundary
- P2-C1-S2: record `S0F-1K` as a historical sample only, not a default future format

### P3 (Later automation admission follow-up)

- P3-C1-S1: open one later script-side source-log admission and fail-closed gate follow-up

### P4 (Later weak-structure export inventory)

- P4-C1-S1: inventory which existing old logs still carry exportable weak-structure narrative without touching their strong-structure automation blocks

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: canonical source-log family rule fixed
- [x] `P0-C1-S2`: six-outlet compatibility rule fixed
- [x] `P0-C1-S3`: evidence and follow-up boundary fixed

### P1 (Template compatibility)

- [x] `P1-C1-S1`: old parent/spine template now carries thin export-ownership guidance
- [x] `P1-C1-S2`: old child/phase template now carries thin export-ownership guidance plus active status reminder

### P2 (Minimum core and export discipline)

- [x] `P2-C1-S1`: source-log minimum core versus weak-structure export boundary fixed
- [x] `P2-C1-S2`: `S0F-1K` recorded as historical restructuring sample only

### P3 (Later automation admission follow-up)

- [ ] `P3-C1-S1`: script-side source-log admission and fail-closed gate follow-up opened

### P4 (Later weak-structure export inventory)

- [ ] `P4-C1-S1`: old-log weak-structure export inventory opened

## Current Status (recommended)

- `S0F-4B` now records the compatibility rule that future source logs should still use the old two templates while six outlets only own weak-structure exports.
- The documentation side is now bounded: old template family stays canonical, `S0F-1K` is demoted to historical sample status, and future work should move next to script-side source-log admission rather than inventing another documentation shape.
- taxonomy and placement questions are now split out to `S0F-3I`, so `S0F-4B` no longer needs to overload template compatibility with repo-wide contract-family classification.
- The next two bounded follow-ups are now explicit as well:
  - one script-side admission and fail-closed gate lane so automation stops trusting arbitrary `source_log_path` inputs
  - one old-log weak-structure export inventory lane so historical source logs can slim down without losing automation-facing strong structure

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.

### P0-C1-S1 through P2-C1-S2 (source-log compatibility and weak-structure export rule fixed | 2026-04-07)

- headSha: `f3a0ee9ce418c7e6778513e315b8b0eee1d2577a`
- artifacts: `docs/logs/_template-log-parent-epic-spine.md`
- artifacts: `docs/logs/_template-log-phase-drills-evidence.md`
- artifacts: `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- artifacts: `docs/logs/log-S0F-docs-management-v6.md`
- artifacts: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
- artifacts: `docs/logs/log-S0F-1K-lifecycle-exact-path-successor-package.md`
- expected:
  - future source logs should still start from the old two template families, while weak-structure content can be exported through six outlets without deleting the source-log skeleton
- observed:
  - the old templates now carry thin export-ownership guidance, the retained source-log minimum core is explicit, `S0F-1K` is bounded back to historical-sample status, and `S0F-4B` leaves script-side admission plus old-log weak-structure inventory as the next separate lanes

## Recent changes (for traceability, optional)

- 2026-04-07: opened `S0F-4B` to reconcile the old source-log templates with the six-outlet model, keeping the old template family canonical while narrowing six outlets to weak-structure export ownership.
- 2026-04-07: extended `S0F-4B` to record the two immediate next lanes explicitly (`source-log admission gate` and `old-log weak-structure export inventory`) and to demote `S0F-1K` from any future default-template role to historical sample status only.