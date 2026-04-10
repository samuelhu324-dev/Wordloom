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
- It also intentionally excludes the supplemental `issue-only reconstructed ancestry` branch for early `S0A` / `S0B` anchors that are reader-relevant but not yet part of the counted root-log scope.

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

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `how much of old S0 has been absorbed so far?` | `view-old-s0-absorption-coverage-overview-v1.md` | aggregate totals and series distribution live here |
| `if I want to judge what can later enter contract and what should remain history, where should I start?` | `view-old-s0-contract-judgment-front-door-v1.md` | the contract-judgment front door now routes readers across surfaced migration, narrative packets, and remaining-line screening without merging those layers |
| `where should I start if I want the old-S0 narrative packet set as a whole?` | `view-old-s0-narrative-history-routing-v1.md` | the aggregate narrative router is now the first-open entry across published packet views |
| `what is the full old-S0 remainder after the current surfaced DOC set?` | `view-old-s0-remaining-history-line-routing-v1.md` | the remainder-routing view is now the first-open surface for the non-surfaced old-`S0` line |
| `what earlier S0A or issue-only S0B ancestry exists outside the counted root-log overview?` | `view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md` | the supplemental reconstruction-routing view makes that exclusion boundary explicit |
| `which exact early S0A / S0B supplemental anchors are currently known, and what evidence do they have?` | `view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md` | the supplemental detail view expands the excluded ancestry branch into exact known anchors and gaps |
| `why did the early S0A + S0B packet exist, and what did it leave behind?` | `view-old-s0-narrative-history-pilot-s0a-s0b-v1.md` | the narrative pilot is the first reader-facing answer for emergence, problem, result, and inheritance across the early mixed packet |
| `which remaining old-S0 rows should now be screened manually for possible contract or view concentration?` | `view-old-s0-remaining-history-line-manual-screening-v1.md` | the manual-screening view is now the first-open surface for human challenge of the non-surfaced remainder buckets |
| `inside one series, what is the standing of each old log?` | `view-old-s0-series-s0b-standing-v1.md` or the later matching series drill-down view | per-log standing is a series-bounded question, not an aggregate one |
| `how did one current DOC surface emerge from older logs?` | `view-old-s0-contract-history-chain-doc-drb-0001-v1.md` or the later matching current-surface chain view | current-surface-first historical reading belongs in the contract-history chain layer |
| `which exact rows are already in the surfaced DOC set across all series?` | `view-old-s0-migration-ledger-v1.md` | the migration ledger remains the canonical admitted-row projection |

## Reader Notes

- Read this view first when the question is `how much of old S0 has been absorbed so far, and how is that distributed by series?`
- Use `view-old-s0-migration-ledger-v1.md` when the question is `which exact old logs are already admitted into the current surfaced set?`
- Use `view-old-s0-remaining-history-line-routing-v1.md` when the question is `what still remains outside the surfaced set, and how should I route into that remainder?`
- Use later `series drill-down` surfaces when the question becomes `what is the standing of each individual old log inside one series?`
- Use later `contract-history chain` surfaces when the question becomes `how did one current DOC surface emerge from older logs?`
- Use `view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md` when the question is about historically relevant early `S0A` / `S0B` anchors that are not yet counted in this overview.
- `remaining outside surfaced set` does not mean only `unreviewed`:
  - some of that remainder may later become `retained-evidence`, `history-lineage`, `retired-lineage`, `no-op`, or `non-doc`
  - this first aggregate overview does not decide those finer standings yet
- The totals in this view remain correct for the current counted root-log review scope even though the repo now separately acknowledges some supplemental early ancestry outside that scope.

## Source Refs

- `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
- `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `docs/governance/views/view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md`
- `docs/governance/views/view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md`
- `docs/governance/views/view-old-s0-narrative-history-pilot-s0a-s0b-v1.md`
- `docs/governance/views/view-doc-current-front-door-v1.md`
- `docs/governance/views/view-doc-history-and-lineage-v1.md`
- `docs/governance/views/view-doc-contract-promotion-map-v1.md`