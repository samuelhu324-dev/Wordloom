# Old S0 Series S0B Standing v1

## Purpose

- This view is the first bounded series drill-down surface for old-`S0` absorption reading.
- It exists so readers can inspect one series log by log and see which rows are already surfaced, which current reading home they now use, and which rows still remain outside the surfaced set.

## Series Boundary

- This first bounded drill-down covers `S0B` only.
- `S0B` is the smallest current review-scope series and therefore the safest first pilot for per-log standing.

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

## S0B Drill-Down

| source log | series | currently surfaced | reader-facing standing | current family | current reading home | history role | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0B-2A` | `S0B` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0B-3A` | `S0B` | `yes` | `current-view` | `DOC` | `view-doc-history-and-lineage-v1` | `structural prerequisite` | `already admitted into the surfaced set as one pre-DOC structural prerequisite for current DOC history reading` |

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `inside S0B, what is the standing of each old log now?` | `view-old-s0-series-s0b-standing-v1.md` | this surface is the bounded per-log standing answer for the `S0B` series |
| `how much of old S0 is surfaced by series overall?` | `view-old-s0-absorption-coverage-overview-v1.md` | aggregate counts and distribution are not repeated here |
| `which admitted rows exist across all series?` | `view-old-s0-migration-ledger-v1.md` | cross-series admitted-row projection stays in the migration ledger |
| `how did one current DOC surface emerge from this history?` | `view-old-s0-contract-history-chain-doc-drb-0001-v1.md` or the later matching chain view | current-surface-first evolution reading belongs in the history-chain layer, not in the series standing table |

## Reader Notes

- Read this view when the question is `inside S0B, what is the standing of each old log now?`
- Use `view-old-s0-absorption-coverage-overview-v1.md` when the question is still aggregate and series-level only.
- Use `view-old-s0-migration-ledger-v1.md` when the question is `which rows are already admitted into the surfaced set across all series?`
- This first `S0B` surface does not decide any later `contract-history chain` yet; it only shows the bounded current standing of the `S0B` rows.

## Source Refs

- `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
- `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
- `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `docs/logs/log-S0B-2A-scripts-snapshots-management.md`
- `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md`