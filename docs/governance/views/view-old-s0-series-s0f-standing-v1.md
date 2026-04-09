# Old S0 Series S0F Standing v1

## Purpose

- This view is the third bounded series drill-down surface for old-`S0` absorption reading.
- It exists so readers can inspect `S0F` log by log and see which rows are already surfaced, which current reading home they now use, and which rows still remain outside the surfaced set.

## Series Boundary

- This third bounded drill-down covers `S0F` only.
- `S0F` is used as the third pilot because it is the current review-scope series with the highest mixed density: surfaced `contract` rows, surfaced `view` rows, and unresolved remainder all coexist inside one real series.

## Drill-Down Model

| field | job |
| --- | --- |
| `source log` | exact old-`S0` source log in this series |
| `series` | fixed series bucket for this drill-down surface |
| `currently surfaced` | whether the row is already admitted into the current old-`S0 -> DOC` surfaced set |
| `reader-facing standing` | one bounded current-reading classification from the `S0F-6B/P1` vocabulary |
| `current family` | current owning family when known |
| `current reading home` | current contract body, current `view`, or unresolved state |
| `history role` | bounded historical role such as source-owner contract, supporting history row, promotion-map row, or unresolved |
| `notes` | short reader-facing explanation |

## S0F Drill-Down

| source log | series | currently surfaced | reader-facing standing | current family | current reading home | history role | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0F-1A` | `S0F` | `yes` | `current-contract` | `DOC` | `DOC-ICR-0001` | `supporting source-owner contract` | `already admitted into the surfaced set as the fail-closed entrypoint boundary now concentrated in DOC-ICR-0001` |
| `S0F-1B` | `S0F` | `yes` | `current-contract` | `DOC` | `DOC-ICT-0001` | `supporting source-owner contract` | `already admitted into the surfaced set as the authoring-path context boundary now concentrated in DOC-ICT-0001` |
| `S0F-1C` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-1D` | `S0F` | `yes` | `current-contract` | `DOC` | `DOC-ICR-0001` and `DOC-ICL-0001` | `supporting source-owner contract` | `already admitted into the surfaced set as lifecycle completeness semantics already absorbed across issue-creation and issue-conclusion contracts` |
| `S0F-1G` | `S0F` | `yes` | `current-contract` | `DOC` | `DOC-IID-0001` and `DOC-IID-0002` | `source-owner contract` | `already admitted into the surfaced set as the issue-identity source-owner row now concentrated across the DOC-IID contract pair` |
| `S0F-1H` | `S0F` | `no` | `non-doc` | `GC current registry` | `GC-PRR-0001` | `non-DOC current-registry source-owner row` | `currently outside the DOC surfaced set because current rule meaning now concentrates in the narrow GC reviewer-classification record; the reviewer-owned runbook remains the stable operator path rather than a second current contract` |
| `S0F-1I` | `S0F` | `no` | `retained-evidence` | `GC current registry` | `GC-PRG-0001` + `run-S0F-1H-pr-body-completeness-review.md` | `retained convergence evidence` | `the support-only retained body now survives mainly as convergence evidence and bridge context; current gate semantics read through GC-PRG-0001 and stable operator procedure reads through the reviewer-owned runbook` |
| `S0F-1J` | `S0F` | `no` | `non-doc` | `GC current registry` | `GC-PRG-0001` | `non-DOC current-registry source-owner row` | `currently outside the DOC surfaced set because current gate meaning now concentrates in the narrow GC standard-check record; repo task and workflow-dispatch surfaces remain enforcement packaging rather than a second current rule family` |
| `S0F-1K` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-2A` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-2B` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3A` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3B` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3C` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3D` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3E` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3F` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3G` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3H` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3I` | `S0F` | `yes` | `current-contract` | `DOC` | `DOC-TAX-0001` | `source-owner contract` | `already admitted into the surfaced set as the taxonomy and placement source-owner row now concentrated in DOC-TAX-0001` |
| `S0F-3J` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3K` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3L` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-3M` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-4A` | `S0F` | `yes` | `current-contract` | `DOC` | `DOC-DRB-0001` | `source-owner contract` | `already admitted into the surfaced set as the first promoted DOC source-owner contract row` |
| `S0F-4B` | `S0F` | `yes` | `current-contract` | `DOC` | `DOC-SLC-0001` | `source-owner contract` | `already admitted into the surfaced set as the source-log compatibility source-owner contract row now concentrated in DOC-SLC-0001` |
| `S0F-4C` | `S0F` | `yes` | `current-contract` | `DOC` | `DOC-FDT-0001` | `source-owner contract` | `already admitted into the surfaced set as the family-front-door transition source-owner contract row now concentrated in DOC-FDT-0001` |
| `S0F-4D` | `S0F` | `yes` | `current-view` | `DOC` | `view-doc-history-and-lineage-v1` | `supporting history row` | `already admitted into the surfaced set as the DOC current-home and legacy-GC-triage milestone now concentrated in the DOC history reader surface` |
| `S0F-4E` | `S0F` | `yes` | `current-view` | `DOC` | `view-doc-history-and-lineage-v1` | `supporting history row` | `already admitted into the surfaced set as the first DOC promotion-event milestone now concentrated in the DOC history reader surface` |
| `S0F-4F` | `S0F` | `yes` | `current-view` | `DOC` | `view-doc-history-and-lineage-v1` | `supporting history row` | `already admitted into the surfaced set as the reader-consolidation milestone now concentrated in the DOC history reader surface` |
| `S0F-4G` | `S0F` | `yes` | `current-view` | `DOC` | `view-doc-history-and-lineage-v1` | `supporting history row` | `already admitted into the surfaced set as the history-publication gate now concentrated in the DOC history reader surface` |
| `S0F-4H` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0F-4I` | `S0F` | `yes` | `current-view` | `DOC` | `view-doc-contract-promotion-map-v1` | `promotion-map row` | `already admitted into the surfaced set as the bounded issue-governance extension packet now concentrated in the DOC promotion-map reader surface` |
| `S0F-5A` | `S0F` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `inside S0F, what is the standing of each old log now?` | `view-old-s0-series-s0f-standing-v1.md` | this surface is the bounded per-log standing answer for the `S0F` series |
| `how much of old S0 is surfaced by series overall?` | `view-old-s0-absorption-coverage-overview-v1.md` | aggregate counts and distribution are not repeated here |
| `which admitted rows exist across all series?` | `view-old-s0-migration-ledger-v1.md` | cross-series admitted-row projection stays in the migration ledger |
| `how did one current DOC surface emerge from this history?` | `view-old-s0-contract-history-chain-doc-drb-0001-v1.md` or the later matching chain view | current-surface-first evolution reading belongs in the history-chain layer, not in the series standing table |

## Reader Notes

- Read this view when the question is `inside S0F, what is the standing of each old log now?`
- Use `view-old-s0-absorption-coverage-overview-v1.md` when the question is still aggregate and series-level only.
- Use `view-old-s0-migration-ledger-v1.md` when the question is `which rows are already admitted into the surfaced set across all series?`
- This third `S0F` surface proves the same row contract can carry the current highest-density mixed series without becoming a support-only working ledger.
- The `S0F-1H` / `S0F-1I` / `S0F-1J` packet now shows that `outside the DOC surfaced set` does not automatically mean `unreviewed`: a row may now resolve as `non-doc` or `retained-evidence` once its current home is defended elsewhere.

## Source Refs

- `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
- `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
- `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `docs/governance/views/support-only/inventory-old-s0-migration-working-ledger-v1.md`
- `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
- `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
- `docs/logs/log-S0F-1D-creation-pr-conclusion-completeness-audit.md`
- `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
- `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
- `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
- `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
- `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`
- `docs/logs/log-S0F-4F-doc-reader-surface-consolidation-after-first-promotion-quartet.md`
- `docs/logs/log-S0F-4G-doc-history-surface-and-extraction-before-cleanup-gate.md`
- `docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md`
- `docs/logs/log-S0F-5C-priority-packet-decomposition-and-cleanup-admission.md`