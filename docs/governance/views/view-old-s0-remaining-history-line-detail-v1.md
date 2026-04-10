# Old S0 Remaining History-Line Detail v1

## Purpose

- This view is the widened reader-facing detail surface for the remaining non-surfaced old-`S0` line.
- It exists so readers can inspect the already-adjudicated retained-history population and the still-unresolved `S0F` subset together without replaying the support-only working ledger row by row.
- It is not yet the manual screening packet for contract admission or six-outlet adjustment.

## Population Boundary

- This detail surface covers the full current non-surfaced old-`S0` remainder fixed by `view-old-s0-remaining-history-line-routing-v1.md`:
  - `63` rows total
  - `45` already-adjudicated rows
  - `18` still-unresolved `S0F` rows
- It intentionally excludes the `21` rows already surfaced into current `DOC` contracts or current `DOC` views.

## Detail Model

| field | job |
| --- | --- |
| `source log` | exact old-`S0` source log in the remaining line |
| `series` | fixed series bucket |
| `current standing now` | the best current standing already visible from the landed series views, or `unreviewed` for the unresolved `S0F` subset |
| `history-line route` | bounded remainder-line reading route such as `retain-direct-history`, `lineage-only`, `external-current-home`, or `standing-first unresolved` |
| `strongest current reading home now` | strongest current home already known for the row |
| `why it still stays in the remaining line` | short reader-facing explanation for why the row is still outside the surfaced `DOC` set |

## Already-Adjudicated Direct-History Line

| source log | series | current standing now | history-line route | strongest current reading home now | why it still stays in the remaining line |
| --- | --- | --- | --- | --- | --- |
| `S0B-2A` | `S0B` | `retained-evidence` | `retain-direct-history` | `backend/scripts/cli.py` plus `docs/labs/_snapshot/` and `docs/runbook/_snapshot/` | `the row remains bounded tooling-governance history while current tooling and evidence-root behavior already read through live repo surfaces rather than through one surfaced DOC target` |
| `S0C-3A` | `S0C` | `retained-evidence` | `retain-direct-history` | `backend/scripts/cli.py` and `backend/scripts/cli_app/` | `the row remains readable CLI-thinning and scenario-decomposition history while current behavior already reads through the landed thin entry and execution modules` |
| `S0C-3A-1A` | `S0C` | `retained-evidence` | `retain-direct-history` | `backend/scripts/cli.py` and `backend/scripts/cli_app/` | `the migration bridge remains bounded retained history rather than one current surfaced target` |
| `S0C-3A-2A` | `S0C` | `retained-evidence` | `retain-direct-history` | `backend/scripts/cli_app/common.py` plus workflow-side artifact helpers | `the row remains direct artifact-contract convergence history while current helper behavior already reads elsewhere` |
| `S0C-3A-3A` | `S0C` | `retained-evidence` | `retain-direct-history` | `backend/scripts/cli.py` and `backend/scripts/cli_app/parser.py` | `the dispatch-thinning cutover remains bounded retained history rather than one current DOC-facing route` |
| `S0C-4A` | `S0C` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0C-scenarios-taxonomy.md` and `docs/labs/scenarios/catalog.yml` | `the row remains direct scenario-taxonomy history while operator discovery already reads through the stable runbook and catalog surfaces` |
| `S0C-4A-1A` | `S0C` | `retained-evidence` | `retain-direct-history` | `docs/labs/scenarios/catalog.yml`, `backend/scripts/ci/validate_scenario_catalog.py`, and `.github/workflows/ci-scenario-guardrails.yml` | `the row remains direct catalog-guardrail history while live validation and workflow references already read through current guardrail surfaces` |
| `S0D-2A` | `S0D` | `retained-evidence` | `retain-direct-history` | `backend/scripts/ci/workflow_artifacts.py` plus `docs/labs/_snapshot/auto/` and `artifacts/*runs*.json` | `the row remains direct drills/evidence automation history while current artifact discovery and bookkeeping already read through live helper and ledger surfaces` |
| `S0D-3A` | `S0D` | `retained-evidence` | `retain-direct-history` | `docs/runbook/_template-runbook.md` plus current operator-entry runbooks | `the row remains direct runbook-governance history while current runbook entry behavior already reads through the live template and adopted operator surfaces` |
| `S0D-4A` | `S0D` | `retained-evidence` | `retain-direct-history` | `docs/UI&UX/README.md`, `docs/UI&UX/UI-FIX-NOTE-TEMPLATE.md`, and `docs/UI&UX/assets/README.md` | `the row remains direct UI evidence-lite governance history while current usage already reads through the UI note and asset surfaces` |
| `S0D-5A` | `S0D` | `retained-evidence` | `retain-direct-history` | `.github/workflows/reusable-labs-scenario-runner.yml` plus `backend/scripts/ci/workflow_artifacts.py` and `.github/workflows/drill-failures.yml` | `the row remains direct evidence-packing history while current workflow packing behavior already reads through live workflow and helper surfaces` |
| `S0D-6A` | `S0D` | `retained-evidence` | `retain-direct-history` | `docs/roadmap/road-template-main-roadmap.md` plus `docs/roadmap/road-template-branch-roadmap.md` and `docs/demo/demo-001/` | `the row remains direct roadmap/demo container history while current roadmap and demo reading already reads through templates and structured demo roots` |
| `S0E-2A` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus `scripts/issues/gen_issue_draft.py` | `the row remains direct issue-creation history while current operator reading already starts from the runbook and draft-generation surfaces` |
| `S0E-2B` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus `scripts/issues/gen_issue_draft.py --create` | `the row remains direct create-mode automation history while current behavior already reads through the live runbook and create entrypoint` |
| `S0E-2C` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus issue batch and relationship planners | `the row remains direct batch/backfill orchestration history while current planning behavior already reads through the runbook and planning scripts` |
| `S0E-3B` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus live label-preflight paths | `the row remains direct live-label preflight history while current enforcement already reads through the runbook and script-level preflight paths` |
| `S0E-4A` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus live PR planning/create surfaces | `the row remains direct PR-automation history while current PR planning and create behavior already reads through the runbook and live helpers` |
| `S0E-4B` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus PR body/title helper surfaces | `the row remains direct PR-formatting history while current body and label behavior already reads through the runbook and helper surfaces` |
| `S0E-4C` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus relationship planners/apply helpers | `the row remains direct PR-linkage history while current relationship apply behavior already reads through the runbook and planning surfaces` |
| `S0E-4D` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus lifecycle planners | `the row remains direct lifecycle-orchestration history while current operator reading already reads through runbook procedure and live planners` |
| `S0E-4F` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus current PR body helpers | `the row remains direct PR-body cleanup history while current body generation already reads through runbook and current helpers` |
| `S0E-5B` | `S0E` | `retained-evidence` | `retain-direct-history` | `scripts/issues/plan_lifecycle_remediation.py` plus `docs/runbook/run-S0E-log-to-issue-creation.md` | `the row remains direct guarded-lifecycle expansion history while current planning already reads through live lifecycle planners and runbook procedure` |
| `S0E-5C` | `S0E` | `retained-evidence` | `retain-direct-history` | `scripts/issues/plan_pr_create_preflight_with_gate.py` plus `docs/runbook/run-S0E-log-to-issue-creation.md` | `the row remains direct guarded PR-create history while current gate behavior already reads through live preflight and runbook surfaces` |
| `S0E-5D` | `S0E` | `retained-evidence` | `retain-direct-history` | `scripts/issues/plan_body_completeness_check_wrapper.py`, `scripts/issues/verify_live_pr_body_contract.py`, and `docs/runbook/run-S0E-log-to-issue-creation.md` | `the row remains direct body-contract normalization history while current check and verification behavior already reads through live helper surfaces` |
| `S0E-6D` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus issue-context authoring and refresh helpers | `the row remains direct issue-context rendering history while current authoring behavior already reads through the runbook and live helpers` |
| `S0E-6E` | `S0E` | `retained-evidence` | `retain-direct-history` | issue-context refresh artifacts plus the runbook's single-item authoring procedure | `the row remains direct context-authoring boundary history while current preserve-versus-author behavior already reads through live refresh workflow and authoring procedure` |
| `S0E-6F` | `S0E` | `retained-evidence` | `retain-direct-history` | `docs/runbook/run-S0E-log-to-issue-creation.md` plus current issue-body helpers | `the row remains direct issue-body boundary history while current rendering already reads through the runbook and current helper surfaces` |
| `S0E-7B` | `S0E` | `retained-evidence` | `retain-direct-history` | `scripts/issues/resolve_pr_source_log_attribution.py` plus workflow-side attribution hooks | `the row remains direct attribution-handoff implementation history while current operational reading already starts from the resolver and workflow hooks` |
| `S0E-7C` | `S0E` | `retained-evidence` | `retain-direct-history` | `scripts/issues/plan_lifecycle_audit.py` plus current audit planning artifacts | `the row remains direct historical-review audit history while current audit behavior already reads through live planning surfaces` |

## Already-Adjudicated Lineage-Only Line

| source log | series | current standing now | history-line route | strongest current reading home now | why it still stays in the remaining line |
| --- | --- | --- | --- | --- | --- |
| `S0C-2A` | `S0C` | `retired-lineage` | `lineage-only` | current-library integration and invariant-focused tests | `the row remains historical retirement lineage rather than one retained current-reading surface` |
| `S0C-5A` | `S0C` | `history-lineage` | `lineage-only` | `docs/logs/log-S0D-1A-log-entries-orchestration.md` plus the parent and phase templates | `the row remains lineage into the current log-orchestration grammar rather than one surfaced target on its own` |
| `S0E-1B` | `S0E` | `retired-lineage` | `lineage-only` | `docs/logs/log-S0E-1B-md-to-docx-minimal-sample.md` plus preserved export scripts | `the row remains archive lineage only and does not act as one current reader surface` |
| `S0E-4E` | `S0E` | `history-lineage` | `lineage-only` | `scripts/issues/resolve_pr_source_log_attribution.py` plus `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md` | `the row remains attribution-boundary lineage rather than one direct current-reading target` |
| `S0E-5E` | `S0E` | `history-lineage` | `lineage-only` | `docs/logs/log-S0E-6F-issue-body-metadata-links-boundary-follow-up.md` plus current issue-body procedures | `the row remains parent-issue ordering lineage into later issue-body surfaces rather than one direct retained history surface` |
| `S0E-6B` | `S0E` | `history-lineage` | `lineage-only` | `docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md` plus later gate procedures | `the row remains log-stability and gate-strategy lineage rather than one direct retained current-reading surface` |
| `S0E-7A` | `S0E` | `history-lineage` | `lineage-only` | `docs/logs/log-S0E-7B-attribution-handoff-implementation-and-auto-mirroring-integration.md` plus later workflow packet surfaces | `the row remains workflow-enforcement lineage rather than one first-open current-reading surface` |

## Already-Adjudicated External-Current-Home Line

| source log | series | current standing now | history-line route | strongest current reading home now | why it still stays in the remaining line |
| --- | --- | --- | --- | --- | --- |
| `S0E-1A` | `S0E` | `non-doc` | `external-current-home` | `docs/demo/demo-001/_cv/` plus `scripts/cv/` | `the row belongs to the demo/tooling line rather than to the current DOC surfaced set` |
| `S0E-5A` | `S0E` | `retained-evidence` | `external-current-home` | `GC-COMPL-0001` plus `scripts/issues/plan_lifecycle_pre_gate.py` | `the row remains a planner-shell history row while the strongest current meaning already lives in the narrow GC completeness record` |
| `S0E-7D` | `S0E` | `non-doc` | `external-current-home` | `GC-WF-0001` | `the row's current workflow-failure rule meaning already lives outside DOC in the narrow GC registry surface` |
| `S0E-7E` | `S0E` | `retained-evidence` | `external-current-home` | `GC-WF-0001` plus retained support-only thin-gate body | `the row remains workflow-support history while the strongest current rule home already lives in the narrow GC record` |
| `S0E-7F` | `S0E` | `retained-evidence` | `external-current-home` | `GC-WF-0001` plus retained support-only wrapper body | `the row remains wrapper history while the strongest current rule home already lives in the narrow GC record` |
| `S0E-7G` | `S0E` | `retained-evidence` | `external-current-home` | `GC-WF-0001` plus retained support-only workflow-dispatch body | `the row remains transport history while the strongest current rule home already lives in the narrow GC record` |
| `S0F-1H` | `S0F` | `non-doc` | `external-current-home` | `GC-PRR-0001` | `the row's current reviewer-classification meaning already lives outside DOC in the narrow GC reviewer record` |
| `S0F-1I` | `S0F` | `retained-evidence` | `external-current-home` | `GC-PRG-0001` plus `run-S0F-1H-pr-body-completeness-review.md` | `the row remains convergence history while current gate semantics and operator procedure already read through external current homes` |
| `S0F-1J` | `S0F` | `non-doc` | `external-current-home` | `GC-PRG-0001` | `the row's current gate meaning already lives outside DOC in the narrow GC gate record` |

## Standing-First Unresolved S0F Line

| source log | series | current standing now | history-line route | strongest current reading home now | why it still stays in the remaining line |
| --- | --- | --- | --- | --- | --- |
| `S0F-1C` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-1K` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-2A` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-2B` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3A` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3B` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3C` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3D` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3E` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3F` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3G` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3H` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3J` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3K` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3L` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-3M` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-4H` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |
| `S0F-5A` | `S0F` | `unreviewed` | `standing-first unresolved` | `not yet fixed` | `the row still lacks defended standing in the old-S0 remainder view and therefore must stay outside manual contract screening for now` |

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `which exact remaining rows are already adjudicated and how do they read now?` | `view-old-s0-remaining-history-line-detail-v1.md` | this is the widened detail answer for the already-adjudicated retained-history population and the unresolved `S0F` subset together |
| `which remaining rows still lack standing and must stay outside manual screening?` | `view-old-s0-remaining-history-line-detail-v1.md` | the unresolved `18`-row `S0F` subset is explicit here rather than implied through counts only |
| `which remaining rows should now enter manual screening for possible contract or view concentration?` | `view-old-s0-remaining-history-line-manual-screening-v1.md` | the manual-screening surface now sits on top of this widened detail layer and keeps first-pass candidate buckets explicit |
| `what is the aggregate shape of the remaining line?` | `view-old-s0-remaining-history-line-routing-v1.md` | the routing view remains the count-first and series-first entrypoint |
| `inside one series, what is the standing of each row now?` | `view-old-s0-series-s0b-standing-v1.md` or the later matching series drill-down view | the per-series standing surfaces remain the row-level standing source |

## Reader Notes

- Read this detail surface after `view-old-s0-remaining-history-line-routing-v1.md` when the question moves from counts to exact remaining rows.
- This view intentionally stops short of manual screening for contract admission:
  - it widens the readable history line
  - it separates direct retained history, lineage-only, external current-home rows, and unresolved rows
  - it does not yet decide candidate current-contract or candidate current-view writes
- Use `view-old-s0-remaining-history-line-manual-screening-v1.md` when the question changes from `how do these rows currently read?` to `which of these rows should I challenge manually for later concentration or outlet adjustment?`

## Source Refs

- `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`
- `docs/governance/views/view-old-s0-remaining-history-line-routing-v1.md`
- `docs/governance/views/view-old-s0-series-s0b-standing-v1.md`
- `docs/governance/views/view-old-s0-series-s0c-standing-v1.md`
- `docs/governance/views/view-old-s0-series-s0d-standing-v1.md`
- `docs/governance/views/view-old-s0-series-s0e-standing-v1.md`
- `docs/governance/views/view-old-s0-series-s0f-standing-v1.md`