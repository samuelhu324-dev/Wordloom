# Old S0 Series S0D Standing v1

## Purpose

- This view is the third bounded series drill-down surface for old-`S0` absorption reading.
- It exists so readers can inspect `S0D` log by log and see which rows are already surfaced, which current reading home they now use, and which rows still remain outside the surfaced set.

## Series Boundary

- This third bounded drill-down covers `S0D` only.
- `S0D` is the next smallest unfinished old-`S0` series after `S0B`, so publishing its standing surface is the lowest-risk way to make the next unresolved remainder reviewable before the larger `S0C` follow-up.

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

## S0D Drill-Down

| source log | series | currently surfaced | reader-facing standing | current family | current reading home | history role | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0D-1A` | `S0D` | `yes` | `current-view` | `DOC` | `view-doc-history-and-lineage-v1` | `structural prerequisite` | `already admitted into the surfaced set as one pre-DOC structural prerequisite for current DOC history reading` |
| `S0D-2A` | `S0D` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0D-3A` | `S0D` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0D-4A` | `S0D` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0D-5A` | `S0D` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |
| `S0D-6A` | `S0D` | `no` | `unreviewed` | `unresolved` | `not yet fixed` | `unresolved` | `currently outside the surfaced set; later review must decide whether this row becomes DOC-related history, retained evidence, non-DOC, or another bounded outcome` |

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `inside S0D, what is the standing of each old log now?` | `view-old-s0-series-s0d-standing-v1.md` | this surface is the bounded per-log standing answer for the `S0D` series |
| `how much of old S0 is surfaced by series overall?` | `view-old-s0-absorption-coverage-overview-v1.md` | aggregate counts and distribution are not repeated here |
| `which admitted rows exist across all series?` | `view-old-s0-migration-ledger-v1.md` | cross-series admitted-row projection stays in the migration ledger |
| `how did one current DOC surface emerge from this history?` | `view-old-s0-contract-history-chain-doc-drb-0001-v1.md` or the later matching chain view | current-surface-first evolution reading belongs in the history-chain layer, not in the series standing table |

## Reader Notes

- Read this view when the question is `inside S0D, what is the standing of each old log now?`
- Use `view-old-s0-absorption-coverage-overview-v1.md` when the question is still aggregate and series-level only.
- Use `view-old-s0-migration-ledger-v1.md` when the question is `which rows are already admitted into the surfaced set across all series?`
- This third `S0D` surface makes the next smaller unfinished series reviewable without forcing readers to replay aggregate-only counts or improvise a per-log row contract.
- `S0D-1A` remains the only already surfaced row in the series, while `S0D-2A` through `S0D-6A` remain intentionally unresolved until the bounded `P4` review classifies their current reading homes.

## Source Refs

- `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
- `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
- `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `docs/logs/log-S0F-5E-small-series-review-sequencing-and-standing-surface-completion.md`
- `docs/logs/log-S0D-1A-log-entries-orchestration.md`
- `docs/logs/log-S0D-2A-drills-evidence-automation.md`
- `docs/logs/log-S0D-3A-runbook-stub.md`
- `docs/logs/log-S0D-4A-UI-layered-fix-notes.md`
- `docs/logs/log-S0D-5A-drills-evidence-packing-unification.md`
- `docs/logs/log-S0D-6A-structured-roadmap-and-demo.md`