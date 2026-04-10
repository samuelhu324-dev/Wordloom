# Old S0 Remaining History-Line Routing v1

## Purpose

- This view is the first reader-facing routing surface for the remaining non-surfaced old-`S0` line.
- It exists so readers can inspect the full old-`S0` remainder after the current surfaced `DOC` set without dropping immediately into the support-only working ledger.
- It is not a current-rule surface, not a replacement for the per-series standing views, and not the final manual-screening packet.

## Remaining-Line Boundary

- The remaining history line uses the same root review-scope population already fixed by `view-old-s0-absorption-coverage-overview-v1.md`.
- It covers the current non-surfaced old-`S0` remainder only:
  - total non-surfaced remainder: `63` rows
  - already-adjudicated but still non-surfaced rows: `45`
  - still-unresolved rows: `18`
- This view intentionally excludes the `21` rows already surfaced into current `DOC` contracts or current `DOC` views.

## Routing Model

| field | job |
| --- | --- |
| `series` | one old-`S0` series bucket such as `S0B`, `S0C`, `S0D`, `S0E`, or `S0F` |
| `remaining rows` | current non-surfaced rows from that series |
| `already-adjudicated remainder` | rows from that series whose standing is already defended but not yet widened into one clearer history line |
| `still-unresolved remainder` | rows from that series whose standing and widened history routing are both still missing |
| `open first` | the first reader-facing surface to open for that bucket now |
| `why` | short routing rationale |

## Remaining-Line Snapshot

- Current remaining old-`S0` history line: `63` rows.
- Already-adjudicated remainder: `45` rows.
- Still-unresolved remainder: `18` rows.
- All current unresolved remainder now sits in `S0F`; `S0B`, `S0C`, `S0D`, and `S0E` have no generic unresolved remainder left.
- The remaining-line reading job therefore splits cleanly into two questions:
  - `which rows are already judged but still need one widened history/view route?`
  - `which rows still lack defended standing and must stay outside manual contract screening for now?`

## Series Routing Summary

| series | remaining rows | already-adjudicated remainder | still-unresolved remainder | open first | why |
| --- | --- | --- | --- | --- | --- |
| `S0B` | `1` | `1` | `0` | `view-old-s0-series-s0b-standing-v1.md` | the only remaining row in `S0B` is already adjudicated, so the series drill-down is currently enough until a later widened detail surface lands |
| `S0C` | `8` | `8` | `0` | `view-old-s0-series-s0c-standing-v1.md` | the full `S0C` remainder is already adjudicated and currently reads through the existing per-series standing surface |
| `S0D` | `5` | `5` | `0` | `view-old-s0-series-s0d-standing-v1.md` | the full `S0D` remainder is already adjudicated and currently reads through the existing per-series standing surface |
| `S0E` | `28` | `28` | `0` | `view-old-s0-series-s0e-standing-v1.md` | the full `S0E` remainder is already adjudicated after `S0F-5F`, but it still lacks one widened non-surfaced history line above the per-series standing surface |
| `S0F` | `21` | `3` | `18` | `view-old-s0-series-s0f-standing-v1.md` | `S0F` is the only remaining series that still mixes already-adjudicated non-surfaced rows with genuine unresolved remainder |

## Current Reader Routing

| question | open first | why |
| --- | --- | --- |
| `what is the full old-S0 remainder after the current surfaced DOC set?` | `view-old-s0-remaining-history-line-routing-v1.md` | this surface is the bounded first-open answer for the full non-surfaced remainder |
| `which remaining rows are already adjudicated versus still unresolved?` | `view-old-s0-remaining-history-line-routing-v1.md` | this surface fixes that split explicitly before later detail and manual screening views |
| `which exact remaining rows are already adjudicated and how do they read now?` | `view-old-s0-remaining-history-line-detail-v1.md` | the widened detail surface now expands the retained-history population and the unresolved `S0F` subset without collapsing them back into the working ledger |
| `inside one series, what is the standing of the remaining rows?` | `view-old-s0-series-s0b-standing-v1.md` or the later matching series drill-down view | the series drill-down layer remains the bounded per-log standing answer |
| `which rows are already in the surfaced DOC set instead of this remainder line?` | `view-old-s0-migration-ledger-v1.md` | the migration ledger remains the canonical surfaced-row projection |
| `how much of old S0 is surfaced versus still outside the surfaced set?` | `view-old-s0-absorption-coverage-overview-v1.md` | the aggregate overview remains the count-first entrypoint |

## Reader Notes

- Read this view first when the question is `what still remains outside the current surfaced DOC set?`
- This surface intentionally stops at routing and population shape:
  - it shows the current remainder split
  - it points readers at the existing series surfaces
  - it does not replace the later manual screening packet
- Use `view-old-s0-remaining-history-line-detail-v1.md` when the question moves from `how big is the remainder?` to `which exact rows are in that remaining line, and how do they currently read?`
- The support-only working ledger remains useful for mutable row notes, but not as the first-open reader surface for understanding the current remaining line.

## Source Refs

- `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`
- `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
- `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `docs/governance/views/view-old-s0-series-s0b-standing-v1.md`
- `docs/governance/views/view-old-s0-series-s0c-standing-v1.md`
- `docs/governance/views/view-old-s0-series-s0d-standing-v1.md`
- `docs/governance/views/view-old-s0-series-s0e-standing-v1.md`
- `docs/governance/views/view-old-s0-series-s0f-standing-v1.md`