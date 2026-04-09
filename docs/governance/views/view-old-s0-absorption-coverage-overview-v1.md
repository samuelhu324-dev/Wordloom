# Old S0 Absorption Coverage Overview v1

## Purpose

- This view is the aggregate coverage overview for old-`S0` absorption reading.
- It exists so readers can answer how much of the current old-`S0` review-scope population is already absorbed into the surfaced `DOC` set without replaying the row-level migration ledger or the source logs manually.

## Population Boundary

- The first aggregate overview uses this review-scope population:
  - top-level root `docs/logs/log-S0*.md` source logs under `S0B` through `S0F`
  - excluding parent spines such as `S0E-docs-management-v5` and `S0F-docs-management-v6`
  - excluding the current absorption-tracking lanes `S0F-5B`, `S0F-6A`, and `S0F-6B`
- This boundary is intentionally narrower than every historical file that ever existed under `S0`.
- It is the first bounded reader-facing review scope for aggregate coverage, not a claim that every support-only or relocated historical artifact is counted here.

## Coverage Model

| field | job |
| --- | --- |
| `series` | one old-`S0` series bucket such as `S0B`, `S0C`, `S0D`, `S0E`, or `S0F` |
| `in-scope old logs` | total root review-scope logs currently counted for that series |
| `currently surfaced` | logs from that series already admitted into the current old-`S0 -> DOC` surfaced set |
| `current-contract` | surfaced rows from that series whose current reading home is one active `DOC` contract |
| `current-view` | surfaced rows from that series whose current reading home is one active `DOC` reader-facing `view` |
| `remaining outside surfaced set` | in-scope logs from that series not yet admitted into the current surfaced set |

## Aggregate Snapshot

- In-scope old-`S0` review population: `84`
- Currently surfaced into the old-`S0 -> DOC` set: `21`
- Surfaced into current `DOC` contracts: `11`
- Surfaced into current `DOC` views: `10`
- Remaining outside the current surfaced set: `63`

## Series Distribution

| series | in-scope old logs | currently surfaced | current-contract | current-view | remaining outside surfaced set |
| --- | --- | --- | --- | --- | --- |
| `S0B` | `2` | `1` | `0` | `1` | `1` |
| `S0C` | `9` | `1` | `0` | `1` | `8` |
| `S0D` | `6` | `1` | `0` | `1` | `5` |
| `S0E` | `33` | `5` | `3` | `2` | `28` |
| `S0F` | `34` | `13` | `8` | `5` | `21` |

## Reader Notes

- Read this view first when the question is `how much of old S0 has been absorbed so far, and how is that distributed by series?`
- Use `view-old-s0-migration-ledger-v1.md` when the question is `which exact old logs are already admitted into the current surfaced set?`
- Use later `series drill-down` surfaces when the question becomes `what is the standing of each individual old log inside one series?`
- Use later `contract-history chain` surfaces when the question becomes `how did one current DOC surface emerge from older logs?`
- `remaining outside surfaced set` does not mean only `unreviewed`:
  - some of that remainder may later become `retained-evidence`, `history-lineage`, `retired-lineage`, `no-op`, or `non-doc`
  - this first aggregate overview does not decide those finer standings yet

## Source Refs

- `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
- `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `docs/governance/views/view-doc-current-front-door-v1.md`
- `docs/governance/views/view-doc-history-and-lineage-v1.md`
- `docs/governance/views/view-doc-contract-promotion-map-v1.md`