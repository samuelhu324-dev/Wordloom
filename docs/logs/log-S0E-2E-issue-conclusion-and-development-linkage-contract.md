# log-S0E-2E (Phase 2E: Issue Conclusion and Development Linkage Contract)

---

**id**: `S0E-2E`
**kind**: `log`
**title**: `issue conclusion and development linkage contract v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, PR, Automation, epic/s0, sub/0e2e`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/324`
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **reference_log_1**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
  **reference_log_3**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
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
**updated**: `2026-04-03`

---

## Decision / Outcome

**Decision**:

- `S0E-2E` defines issue conclusion as a separate post-merge slice instead of leaving issue closure as an informal manual step.
- v1 requires the final issue conclusion to carry explicit PR linkage to the merged PR or PR set that delivered the same ID-scoped work.
- The final issue-conclusion content must be English-only and should close the lifecycle that started with issue creation.
- The lifecycle order is fixed as: `Issue Creation -> Logs completed -> PR -> human merge -> Issue Conclusion`.

**Default choices (phase defaults / v1)**:

- Issue conclusion happens only after merge; draft PRs or unmerged PRs are not sufficient to trigger final conclusion output.
- GitHub auto-closing an issue via `Closes #...` is only the state transition; it does not by itself mean the final conclusion body has been written back.
- The final body no longer renders a separate `Development` section; merged PR linkage should instead surface as short PR references in `Definition of Done (DoD)` plus explicit PR URLs under `Links`.
- `Definition of Done (DoD)` in the conclusion should enumerate only short merged PR references such as `#298`, not replay the original contract bullets or restate full PR titles.
- If conclusion `Context` is retained, its closing sentence should describe the resulting closure state or stable handoff left by the slice, rather than repeat merged PR evidence that already belongs in `Definition of Done (DoD)`.
- Conclusion content must stay English-only.
- Merge approval remains a human review step outside automation scope even when conclusion generation exists.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Define post-merge issue conclusion as a dedicated contract instead of leaving issue closure as an informal manual step.
- Add deterministic dry-run conclusion planning from exact-ID merged PR evidence while keeping the final issue body English-only and DoD-led.
- Materialise the contract with a real issue-conclusion write-back path that updates the live issue body and closes open post-merge issues when appropriate.

**PR checklist source**:

- Default source: reuse this log's checked execution checklist items for the generated PR checklist block.

**PR links / evidence footer**:

- Log: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/324`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/issue-conclusion-S0E-2E-sample-plan.json`

## Definitions (optional)

- **Issue conclusion**: the final structured close-out content written back to an issue after the associated development PRs have merged.
- **Development linkage**: the explicit relationship from an issue to the PR or PR set that implemented the work.
- **Short PR reference**: a compact GitHub pull request reference such as `#298` used inside the final `Definition of Done (DoD)` ledger.
- **Merged PR evidence**: the set of merged PR numbers, titles, and URLs that prove the issue's implementation path is complete.
- **ID-scoped PR set**: the merged PRs whose titles or commit scopes use the same exact log/issue ID prefix, such as `S0E-2B`.

## Constraints

- Do not conclude an issue before the relevant PR is merged.
- Do not infer unrelated PRs by loose keyword matching; exact ID prefix matching remains the default boundary.
- Do not keep the conclusion body bilingual.
- Do not reuse the original issue-creation `Definition of Done (DoD)` bullets as the final conclusion text.
- Do not let automation perform the merge; merge approval remains human-owned.

## Scope

- `P0`: contract for lifecycle order, post-merge boundary, development linkage, and English conclusion body rules
- `P1`: final issue-conclusion body shape and PR-selection rules
- `P2`: dry-run conclusion planning from merged PR metadata
- `P3`: real issue-conclusion write-back after a human-approved merge

## Success Criteria (DoD)

- The issue-conclusion contract only activates after merge.
- The final issue content includes explicit merged PR linkage for the same exact ID scope without requiring a dedicated `Development` section.
- `Definition of Done (DoD)` in the conclusion uses short merged PR references such as `#298` rather than generic prose.
- The conclusion body is English-only.
- The contract explains how merged PR titles/IDs are selected and how multiple PRs are ordered when one issue spans more than one review slice.

## Stability (what stable means)

- This log can be marked `stable` when:
  - post-merge issue conclusion rules, Development linkage rules, and English conclusion body structure are fixed and validated through at least one dry-run plus one real write-back;
  - issue closure no longer depends on operator memory to find and format the merged PR evidence.

## Current Status

- `P0` is complete: lifecycle order, the merge boundary, and the exact-ID merged-PR linkage boundary are now fixed.
- `P1` is complete: the final English conclusion body shape and the exact-ID PR selection plus ordering rules are now fixed.
- `P1-C1-S3` is complete: retained conclusion `Context` blocks now end on outcome wording, while exact merged-PR evidence remains only in `Definition of Done (DoD)` and `Links`.
- `P2` is complete: a manifest-driven dry-run planner now emits ordered merged-PR evidence plus final issue-conclusion body previews without writing GitHub state.
- `P3` is complete: the apply path now updates one real issue body from a dry-run plan and closes the issue when it was still open after merge.
- Real issue `#297` now carries the final conclusion body and is closed with `reason=completed`, proving the dry-run output can be materialised on GitHub.
- `S0E-2E` is now `stable` because lifecycle boundary, exact-ID selection, dry-run planning, and one real write-back have all been exercised end-to-end.

## P0 (Contract | v1)

### P0-C1-S1 (Lifecycle order and merge boundary | v1)

- Issue conclusion is the last operator-facing documentation step after merge.
- The required order is:
  - issue creation
  - logs completed
  - PR created
  - merge completed by human review
  - issue conclusion written back
- A PR being open, draft, or approved is not enough; merge completion is the minimum trigger.
- An issue that GitHub already marked `closed` through PR keywords may still require a post-merge body update; closed state and concluded state are not treated as synonyms in v1.

### P0-C1-S2 (Development linkage and PR selection | v1)

- The conclusion's merged-PR set should come from PRs whose titles start with the same exact issue/log prefix, for example `S0E-4A/` for issue `S0E-4A`.
- Exact ID prefix matching is the default selection rule; overrides may only come from explicit operator input or a later conclusion manifest and must stay traceable.
- Candidate PRs must already be merged; open PRs, draft PRs, or keyword-linked PR references without merge evidence are not eligible.
- If multiple merged PRs belong to the same issue, they must be ordered deterministically rather than by arbitrary search result order.
- If no merged PR exists yet, the issue cannot enter final conclusion mode.

### P0-C1-S3 (English conclusion body and DoD rule | v1)

- The final issue-conclusion body should use English-only headings and content.
- The final body must preserve the issue's create-time `Metadata` block and then append or replace the remaining body with conclusion-specific sections.
- The recommended conclusion structure is:

```md
## Metadata

...

## Definition of Done (DoD)

- #294

## Links

- Log: `docs/logs/log-S0E-2B-...md`
- Issue: `https://github.com/.../issues/...`
- PR: `https://github.com/.../pull/...`
```

- `Definition of Done (DoD)` in the conclusion is a short merged-PR reference ledger, not a replay of the original contract acceptance bullets.
- If a short `Context` section is retained in the final conclusion body, it must stay English-only and reflect closure state rather than re-explaining the original contract.
- If a retained `Context` section ends with a closing sentence, that sentence should summarize the lasting result, reusable baseline, or handoff state left by the slice, and should not restate PR numbers, PR titles, or "closed through #..." wording that already appears in `Definition of Done (DoD)`.

### P1-C2-S1 (Remove Development section | v1)

- The final conclusion body no longer renders a dedicated `Development` section.
- Merged PR linkage remains required as a contract concept, but the user-facing body now expresses it through `Definition of Done (DoD)` short refs and `Links` PR URLs.

### P1-C2-S2 (DoD short PR refs | v1)

- `Definition of Done (DoD)` should list only short PR references such as `- #298`.
- Full PR titles should stay out of the final body text; they may remain in dry-run plan JSON and evidence artifacts.

## P1 (Conclusion body and PR-selection rules | v1)

### P1-C1-S1 (Final English issue-conclusion body shape | v1)

- The create-time `Metadata` block should be preserved so labels, project, milestone, and parent issue remain visible after closure, while deterministic log navigation stays in `Links`.
- `Context` becomes optional during conclusion v1; if retained, it should be one short English closure note rather than a replay of the original contract scope.
- When `Context` is retained, its final sentence should carry outcome wording such as "left a stable baseline" or "left the path in a reusable live form" instead of repeating PR evidence that belongs in `Definition of Done (DoD)`.
- `Definition of Done (DoD)` is mandatory in the final conclusion body and should list the ordered short PR refs as the final delivery ledger.
- `Links` should preserve deterministic references such as log path, optional roadmap, parent log, optional previous log, and one PR URL line per merged PR in the same order used by the selected merged-PR set.
- The final body shape is:

```md
## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`
- Projects: `wordloom Board`
- Milestone: ``
- Parent issue: #248

## Definition of Done (DoD)

- #298

## Links

- Log: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/297`
- PR: `https://github.com/samuelhu324-dev/wordloom-v3/pull/298`
- Parent log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous log: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
```

### P1-C1-S2 (Exact-ID PR selection and ordering rules | v1)

- The default candidate set is the merged PRs whose titles start with the exact issue/log ID prefix followed by `/`, such as `S0E-4A/`.
- If an explicit override is recorded later, it may narrow or expand the candidate set, but the override must be written explicitly and reported in evidence.
- When candidate PR titles expose parseable `P*`, `C*`, and `S*` units, ordering should prefer the lowest phase number first and then the lower cycle/step tuple before merge time.
- When phase or unit parsing is unavailable or mixed, ordering falls back to `mergedAt` ascending and then PR number ascending.
- The same ordered PR list must be reused consistently in `Definition of Done (DoD)` and `Links`.
- Current same-family merged samples prove the boundary is viable: `S0E-4A -> #294`, `S0E-4B -> #296`, and `S0E-2D -> #298`.

### P1-C1-S3 (Context ending stays out of the DoD evidence lane | v1)

- If a final conclusion body retains `Context`, its last sentence should describe the lasting result, reusable baseline, or handoff state left by the slice.
- Exact merged-PR evidence remains user-facing only in `Definition of Done (DoD)` short refs and `Links` PR URLs, rather than being repeated in the `Context` ending.

## P2 (Dry-run conclusion planning | v1)

### P2-C1-S1 (Merged-PR conclusion planner | v1)

- Dry-run issue conclusion now uses an explicit manifest and never writes back to GitHub.
- The planner requires `requested_id`, `source_log_path`, and an explicit issue reference.
- Candidate PRs default to merged PRs whose titles start with the exact requested ID prefix followed by `/`, unless explicit merged-PR overrides are supplied.
- The planner preserves the existing issue `Metadata`, omits blank `Context`, rewrites `Definition of Done (DoD)` from ordered short PR refs, and appends deterministic `Issue` plus `PR` lines under `Links`.
- The planner emits both a structured plan JSON and one body preview markdown file per requested ID.

### P2-C1-S2 (Representative merged-sample validation | v1)

- Representative dry-run validation now covers three real closed issues: `S0E-4A -> #293`, `S0E-4B -> #295`, and `S0E-2D -> #297`.
- `S0E-4A` validates the multi-PR case because the exact-ID selector now returns merged PRs `#294` and `#299` in deterministic order.
- `S0E-4B` and `S0E-2D` validate the single-PR case and confirm the same body shape still works when only one merged PR exists.
- All three previews confirm that the existing blank create-time `Context` and `Definition of Done (DoD)` scaffold can be replaced by final merged-PR evidence without touching GitHub state.

### P2-C2-S1 (Format revision sample regeneration | v1)

- After the format revision, regenerated previews must omit the `Development` section entirely.
- The revised previews must render `Definition of Done (DoD)` as short PR refs only, for example `- #296` and `- #298`.

## P3 (Real issue-conclusion write-back | v1)

### P3-C1-S1 (Real write-back apply path | v1)

- Real issue-conclusion write-back now consumes a planned item from the dry-run plan rather than re-querying GitHub ad hoc.
- The apply path copies the planned body preview into a dedicated apply artifact, writes that body back to the target GitHub issue, and then closes the issue with `reason=completed` when the issue is still open.
- If the issue is already closed, the apply path must still allow an in-place body update so GitHub close state and final conclusion body remain decoupled.

### P3-C1-S2 (First real attachment accounting | v1)

- The first real write-back target is `S0E-2D -> issue #297`.
- The attached merged PR set for this real run is one-item and exact-ID scoped: `#298` only.
- The real run also proves that some post-merge issues may still be `OPEN` when no closing keyword was materialised earlier; conclusion write-back must therefore be able to close the issue after body update instead of assuming GitHub already did so.

### P3-C2-S1 (Closed issue follow-up sample | v1)

- The second real write-back target is `S0E-4B -> issue #295` as the next cycle under the revised final-body format.
- This cycle validates that the same apply path still works when the final body omits `Development` and uses only short PR refs in `Definition of Done (DoD)`.

### P3-C2-S2 (Second attachment accounting | v1)

- The attached merged PR set for this second real run is one-item and exact-ID scoped: `#296` only.
- This cycle also validates the open-issue path again because issue `#295` remained open before the revised write-back was applied.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-2E/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S0E-2E` work should stay on the active `S0E-*` branch until conclusion automation needs an isolated review slice.

**Commit discipline (recommended)**:

- Fix the merge-boundary and PR-selection contract first, then validate dry-run conclusion planning, then perform one real issue-conclusion write-back after merge.

## Plan (draft)

### P1 (Conclusion body and PR-selection rules)

- P1-C1-S1: define the final English issue-conclusion body shape
- P1-C1-S2: define exact-ID PR selection and multi-PR ordering rules
- P1-C1-S3: keep retained conclusion Context endings on outcome wording rather than DoD evidence wording
- P1-C2-S1: remove the final `Development` section from the user-facing issue body
- P1-C2-S2: reduce final `Definition of Done (DoD)` entries to short PR refs only

### P2 (Dry-run conclusion planning)

- P2-C1-S1: plan conclusion output from merged PR metadata without writing back to GitHub
- P2-C1-S2: verify Development and DoD formatting against representative merged PR samples
- P2-C2-S1: regenerate representative previews against the revised body format

### P3 (Real issue-conclusion write-back)

- P3-C1-S1: update one real issue with the final conclusion body after merge
- P3-C1-S2: record which merged PRs were attached and how the final DoD block was rendered
- P3-C2-S1: update one additional real issue under the revised final-body format
- P3-C2-S2: record the second cycle's attached merged PR refs and open-to-closed behavior

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: lifecycle order and merge boundary fixed
- [x] `P0-C1-S2`: development linkage and PR selection rules fixed
- [x] `P0-C1-S3`: English conclusion body and DoD rule fixed

### P1 (Conclusion body and PR-selection rules)

- [x] `P1-C1-S1`: final English issue-conclusion body shape defined
- [x] `P1-C1-S2`: exact-ID PR selection and ordering rules fixed
- [x] `P1-C1-S3`: retained conclusion Context endings kept out of the DoD evidence lane
- [x] `P1-C2-S1`: final Development section removed from user-facing body
- [x] `P1-C2-S2`: final DoD short-PR-reference rendering fixed

### P2 (Dry-run conclusion planning)

- [x] `P2-C1-S1`: dry-run conclusion planning completed
- [x] `P2-C1-S2`: Development and DoD formatting validated against merged PR samples
- [x] `P2-C2-S1`: revised body-format previews regenerated

### P3 (Real issue-conclusion write-back)

- [x] `P3-C1-S1`: one real issue-conclusion write-back completed after merge
- [x] `P3-C1-S2`: merged PR attachment accounting recorded
- [x] `P3-C2-S1`: additional revised-format real issue write-back completed
- [x] `P3-C2-S2`: second-cycle merged PR attachment accounting recorded

## Evidence

- Artifacts remain the preferred source of truth for dry-run and write-back evidence; this log records the contract decisions and the live samples that fixed them.
- `P0-C1-S1`: live issues `#293`, `#295`, and `#297` are already `CLOSED`, but their bodies still retain the create-time empty `Context` and `Definition of Done (DoD)` scaffold, proving that GitHub close state alone does not satisfy issue conclusion.
- `P0-C1-S2` / `P1-C1-S2`: merged PRs `#294`, `#296`, and `#298` each expose the exact-ID title prefix pattern `S0E-4A/`, `S0E-4B/`, and `S0E-2D/`, providing real selector samples for deterministic exact-ID PR matching.
- `P0-C1-S3` / `P1-C1-S1`: this log now fixes the final conclusion body to preserve `Metadata` while turning `Definition of Done (DoD)` and `Links` into the user-facing merged-PR ledger instead of leaving the create-time blank scaffold in place.
- `P1-C1-S1` / `P1-C1-S2`: `docs/runbook/run-S0E-log-to-issue-creation.md` now records the same post-merge conclusion procedure, exact-ID PR selection rules, and deterministic link/body ordering for operators.
- `P1-C1-S3`: live issues `#288` and `#289` now show the retained `Context` / `DoD` split in practice: `Context` ends on outcome wording, while exact merged-PR evidence stays in `Definition of Done (DoD)` only.
- `P2-C1-S1`: `scripts/issues/plan_issue_conclusion.py` now provides a manifest-driven dry-run planner that reads explicit issue references, resolves exact-ID merged PR evidence from GitHub, and emits one structured plan JSON plus per-item body previews without writing GitHub state.
- `P2-C1-S1`: `docs/issues/issue-conclusion-S0E-2E-sample-plan.json` records a successful three-item dry-run with `planned_items=3` and no reconciliation or error items.
- `P2-C1-S2`: `docs/issues/issue-conclusion-S0E-2E-sample-s0e-4a-body.md` proves the multi-PR case by rendering short refs `#294` and `#299` in `Definition of Done (DoD)` while omitting `Development` entirely.
- `P2-C1-S2`: `docs/issues/issue-conclusion-S0E-2E-sample-s0e-4b-body.md` and `docs/issues/issue-conclusion-S0E-2E-sample-s0e-2d-body.md` prove the same revised body shape for single-PR issues `#295` and `#297`.
- `P3-C1-S1`: `scripts/issues/apply_issue_conclusion_from_plan.py` now provides the real apply path that updates an issue body from a planned preview and closes the issue when it is still open.
- `P3-C1-S1`: `docs/issues/issue-conclusion-S0E-2E-sample-s0e-2d-apply-result.json` records a successful real write-back for issue `#297`, including the state transition `OPEN -> CLOSED` and `close_reason=completed`.
- `P3-C1-S2`: `docs/issues/issue-conclusion-S0E-2E-sample-s0e-2d-apply-body.md` is the exact body written back to live issue `#297`, showing revised DoD short ref `#298` and no `Development` section.
- `P3-C1-S2`: live issue `#297` now shows the final conclusion body and no longer retains the create-time blank `Context` / `Definition of Done (DoD)` scaffold.
- `P3-C2-S1` / `P3-C2-S2`: live issue `#295` was updated under the revised format and closed after write-back, proving the second-cycle real sample for short-ref-only DoD rendering.

## Recent changes (for traceability, optional)

- 2026-03-29: opened `S0E-2E` to define post-merge issue conclusion, Development linkage, and final English DoD rendering as a separate slice from issue creation and PR creation.
- 2026-03-30: completed `P0` by fixing the lifecycle boundary, exact-ID merged-PR linkage rule, and the distinction between GitHub closed state versus final issue conclusion.
- 2026-03-30: completed `P1` by defining the final English conclusion body shape, deterministic multi-PR ordering rules, and the shared operator procedure in the runbook.
- 2026-03-30: completed `P2` by adding `scripts/issues/plan_issue_conclusion.py`, generating `S0E-2E` dry-run artifacts for `#293`, `#295`, and `#297`, and validating both single-PR and multi-PR conclusion-body rendering.
- 2026-03-30: completed `P3` by adding `scripts/issues/apply_issue_conclusion_from_plan.py`, writing the final conclusion body back to live issue `#297`, and closing that issue with `reason=completed`.
- 2026-03-30: revised the final body format in `P1-C2` so `Development` is removed and `Definition of Done (DoD)` keeps only short PR refs; regenerated dry-run samples and completed a second real cycle on issue `#295`.
- 2026-04-01: completed `P1-C1-S3` by fixing the retained conclusion `Context` ending rule so outcome wording stays in `Context` while exact PR evidence stays only in `Definition of Done (DoD)` and `Links`.
