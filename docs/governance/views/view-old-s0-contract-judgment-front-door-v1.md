# Old S0 Contract Judgment Front Door v1

## Purpose

- This view is the first-open contract-judgment front door for old-`S0`.
- It exists so one reader can decide, in a stable order, what already reads as current `DOC` contract/view concentration, what should remain history, and what is still too unresolved to judge for later contract entry.
- It does not replace the narrative router, migration ledger, or remaining-line manual-screening view; it routes readers across them.

## Boundary

- This front door covers the current old-`S0` judgment stack only:
  - published narrative packet reading
  - already-surfaced `DOC` migration reading
  - remaining-line manual screening for non-surfaced rows
  - unresolved-standing stop conditions for the still-unsettled `S0F` subset
- It does not merge outlet-management execution, contract-body authoring, or unresolved-standing adjudication into the same surface.

## Judgment Model

| judgment state | open first | why |
| --- | --- | --- |
| `already current DOC contract/view` | `view-old-s0-migration-ledger-v1.md` | the migration ledger is the canonical surfaced-row projection, so current `DOC` absorption should read there first |
| `needs historical why/problem/result reading before judgment` | `view-old-s0-narrative-history-routing-v1.md` | the narrative router is the first-open packet selector for understanding historical emergence and downstream consequence before later concentration judgment |
| `still non-surfaced but mature enough for human review` | `view-old-s0-remaining-history-line-manual-screening-v1.md` | the manual-screening view is the reader-facing human review layer for retained history, lineage-only, non-DOC, and possible later concentration questions |
| `still too unresolved for contract judgment` | `view-old-s0-series-s0f-standing-v1.md` and `view-old-s0-remaining-history-line-detail-v1.md` | unresolved `S0F` rows still lack defended standing, so judgment should stop there rather than pretending they are candidate contracts |

## Current Decision Baseline

- Current old-`S0 -> DOC` surfaced rows: `21`
- Current surfaced `DOC` contract rows: `11`
- Current surfaced `DOC` view rows: `10`
- Current remaining non-surfaced rows: `63`
- Current first-pass `candidate current-contract`: `0`
- Current first-pass `candidate current-view`: `0`
- Current still-unresolved standing-first rows: `18`, all in `S0F`

## Recommended Reading Order

1. Open `view-old-s0-migration-ledger-v1.md` if the question is `what is already in DOC now?`
2. Open `view-old-s0-narrative-history-routing-v1.md` if the question is `what historical packet should I understand before I judge later concentration?`
3. Open `view-old-s0-remaining-history-line-manual-screening-v1.md` if the question is `which non-surfaced rows should remain history, lineage, non-DOC, or later contract/view candidates?`
4. Stop and reopen standing work before contract judgment when a row is still inside the unresolved `S0F` standing-first subset.

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `what already reads as current DOC contract or current DOC view?` | `view-old-s0-migration-ledger-v1.md` | surfaced old-`S0 -> DOC` answers belong in the migration ledger |
| `what historical packet should I read before I decide whether a row should stay history or later concentrate elsewhere?` | `view-old-s0-narrative-history-routing-v1.md` | packet-level why/problem/result reading belongs in the narrative router and packet views |
| `which non-surfaced rows currently look like retain-as-history, lineage-only, or non-DOC rather than immediate contract candidates?` | `view-old-s0-remaining-history-line-manual-screening-v1.md` | the manual-screening view is the current human-first judgment layer for the remaining line |
| `which rows are still too unresolved to judge for contract entry?` | `view-old-s0-series-s0f-standing-v1.md` and `view-old-s0-remaining-history-line-detail-v1.md` | unresolved `S0F` rows still need standing defense before later contract judgment can be meaningful |
| `how much of old S0 is already surfaced versus still outside the surfaced set?` | `view-old-s0-absorption-coverage-overview-v1.md` | coverage remains the count-first entrypoint rather than the judgment front door |

## Reader Notes

- Read this front door first when the real question is `how should I judge old-S0 rows for current contract entry without mixing up history reading and unresolved backlog?`
- Empty first-pass `candidate current-contract` and `candidate current-view` buckets do not mean no later candidates exist.
- They mean the current repo has intentionally stopped at human-readable judgment routing before allowing one automatic candidate packet to front-run that review.
- The strongest current stop condition remains the unresolved `S0F` subset: until those rows have defended standing, they should not be treated as later contract candidates simply because they look dense or important.

## Source Refs

- `docs/governance/views/view-old-s0-narrative-history-routing-v1.md`
- `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `docs/governance/views/view-old-s0-remaining-history-line-routing-v1.md`
- `docs/governance/views/view-old-s0-remaining-history-line-manual-screening-v1.md`
- `docs/governance/views/view-old-s0-series-s0f-standing-v1.md`
- `docs/governance/views/view-old-s0-remaining-history-line-detail-v1.md`
- `docs/logs/log-S0F-5J-old-s0-contract-judgment-front-door-view.md`