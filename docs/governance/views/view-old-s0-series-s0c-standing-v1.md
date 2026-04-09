# Old S0 Series S0C Standing v1

## Purpose

- This view is the fourth bounded series drill-down surface for old-`S0` absorption reading.
- It exists so readers can inspect `S0C` log by log and see which rows are already surfaced, which current reading home they now use, and which rows still remain outside the surfaced set.

## Series Boundary

- This fourth bounded drill-down covers `S0C` only.
- `S0C` is the larger unfinished small-series follow-up after `S0D`, so publishing its standing surface is the remaining prerequisite for bounded series review under the same drill-down model already proven for `S0B`, `S0D`, `S0E`, and `S0F`.

## Drill-Down Model

| field | job |
| --- | --- |
| `source log` | exact old-`S0` source log in this series |
| `series` | fixed series bucket for this drill-down surface |
| `currently surfaced` | whether the row is already admitted into the current old-`S0 -> DOC` surfaced set |
| `reader-facing standing` | one bounded current-reading classification from the `S0F-6B/P1` vocabulary |
| `current family` | current owning family when known |
| `current reading home` | current contract body, current `view`, or unresolved state |
| `history role` | bounded historical role such as structural prerequisite or unresolved |
| `notes` | short reader-facing explanation |

## S0C Drill-Down

| source log | series | currently surfaced | reader-facing standing | current family | current reading home | history role | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0C-1A` | `S0C` | `yes` | `current-view` | `DOC` | `view-doc-history-and-lineage-v1` | `structural prerequisite` | `already admitted into the surfaced set as one pre-DOC structural prerequisite for current DOC history reading` |
| `S0C-2A` | `S0C` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, retired-lineage, or another bounded outcome` |
| `S0C-3A` | `S0C` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, retired-lineage, or another bounded outcome` |
| `S0C-3A-1A` | `S0C` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, retired-lineage, or another bounded outcome` |
| `S0C-3A-2A` | `S0C` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, retired-lineage, or another bounded outcome` |
| `S0C-3A-3A` | `S0C` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, retired-lineage, or another bounded outcome` |
| `S0C-4A` | `S0C` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, retired-lineage, or another bounded outcome` |
| `S0C-4A-1A` | `S0C` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, retired-lineage, or another bounded outcome` |
| `S0C-5A` | `S0C` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, retired-lineage, or another bounded outcome` |

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `inside S0C, what is the standing of each old log now?` | `view-old-s0-series-s0c-standing-v1.md` | this surface is the bounded per-log standing answer for the `S0C` series |
| `how much of old S0 is surfaced by series overall?` | `view-old-s0-absorption-coverage-overview-v1.md` | aggregate counts and distribution are not repeated here |
| `which admitted rows exist across all series?` | `view-old-s0-migration-ledger-v1.md` | cross-series admitted-row projection stays in the migration ledger |
| `how did one current DOC surface emerge from this history?` | `view-old-s0-contract-history-chain-doc-drb-0001-v1.md` or the later matching chain view | current-surface-first evolution reading belongs in the history-chain layer, not in the series standing table |

## Reader Notes

- Read this view when the question is `inside S0C, what is the standing of each old log now?`
- Use `view-old-s0-absorption-coverage-overview-v1.md` when the question is still aggregate and series-level only.
- Use `view-old-s0-migration-ledger-v1.md` when the question is `which rows are already admitted into the surfaced set across all series?`
- This fourth `S0C` surface closes the last missing small-series drill-down prerequisite before the repo can review the larger remaining small-series backlog row by row.
- `S0C-1A` remains the only already surfaced row in the series, while `S0C-2A` through `S0C-5A` and the `S0C-3A-*` / `S0C-4A-*` child rows remain intentionally unresolved until the bounded `P6` review classifies their current reading homes.

## Source Refs

- `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
- `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
- `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `docs/logs/log-S0F-5E-small-series-review-sequencing-and-standing-surface-completion.md`
- `docs/logs/log-S0C-1A-log-extensions.md`
- `docs/logs/log-S0C-2A-legacy-integration-suite-retired.md`
- `docs/logs/log-S0C-3A-cli-breakdown.md`
- `docs/logs/log-S0C-3A-1A-double-parallel.md`
- `docs/logs/log-S0C-3A-2A-artifacts-contract-packing.md`
- `docs/logs/log-S0C-3A-3A-dispatch-only-argparse-extraction.md`
- `docs/logs/log-S0C-4A-scenarios-taxonomy.md`
- `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
- `docs/logs/log-S0C-5A-Git-commit+push-descriptions.md`