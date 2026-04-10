# Old S0 Narrative History Routing v1

## Purpose

- This view is the aggregate narrative-routing surface for old-`S0`.
- It exists so readers can choose the right narrative-history packet without inferring packet boundaries from standing views, ancestry routes, or aggregate coverage tables.
- It complements the existing packet views; it does not replace them.

## Boundary

- This routing surface covers the currently published old-`S0` narrative packet set:
  - supplemental early `S0A + S0B` narrative pilot
  - counted `S0D + S0C` packet
  - counted `S0E` packet
- It also records the current not-yet-published boundary for the reviewed `S0F` subset so readers do not mistake the current packet set for full counted-series completeness.

## Packet Set Snapshot

| packet | scope now | open first | why |
| --- | --- | --- | --- |
| `early supplemental packet` | early `S0A + S0B` ancestry outside counted root-log scope | `view-old-s0-narrative-history-pilot-s0a-s0b-v1.md` | this packet explains the earliest pressure, parent decision, counted `S0B` execution anchors, and the still-unresolved `S0B-1A` gap |
| `first counted packet` | counted `S0D + S0C` | `view-old-s0-narrative-history-packet-s0d-s0c-v1.md` | this packet explains the first bounded counted-series rollout across structural prerequisites, retained governance evidence, retired lineage, and history-lineage |
| `second counted packet` | counted `S0E` | `view-old-s0-narrative-history-packet-s0e-v1.md` | this packet explains the large mixed issue/PR/lifecycle/workflow automation series where current-contract, current-view, retained-evidence, lineage, retired-lineage, and non-DOC rows coexist |
| `reviewed S0F subset` | not yet published as one narrative packet | `view-old-s0-series-s0f-standing-v1.md` plus `view-old-s0-remaining-history-line-detail-v1.md` | the current repo has standing and remainder routing for `S0F`, but one separate bounded narrative packet for the reviewed subset has not yet been published |

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `where should I start if I want the old-S0 narrative packet set as a whole?` | `view-old-s0-narrative-history-routing-v1.md` | this surface is the first-open narrative router across the currently published packet set |
| `what is the earliest old-S0 narrative packet, including ancestry outside counted scope?` | `view-old-s0-narrative-history-pilot-s0a-s0b-v1.md` | the early pilot remains the first answer for supplemental ancestry and early packet emergence |
| `what is the first counted narrative packet after the early pilot?` | `view-old-s0-narrative-history-packet-s0d-s0c-v1.md` | the combined `S0D + S0C` packet is the first counted-series rollout |
| `what is the large mixed counted automation packet?` | `view-old-s0-narrative-history-packet-s0e-v1.md` | `S0E` is the first large counted mixed packet with multiple standing/result shapes |
| `what is the current state of S0F before a later narrative packet exists?` | `view-old-s0-series-s0f-standing-v1.md` and `view-old-s0-remaining-history-line-detail-v1.md` | `S0F` currently reads through standing plus remainder detail rather than through one published narrative packet |
| `how much of old S0 is surfaced overall?` | `view-old-s0-absorption-coverage-overview-v1.md` | aggregate absorption remains a separate count-first question |

## Reader Notes

- Separate packet views are no longer sufficient as the only first-open narrative entry, because there is now more than one published packet and the packet set spans both supplemental and counted scope.
- This router intentionally does not claim full narrative completeness for all old-`S0` rows.
- The reviewed `S0F` subset remains an explicit later follow-up boundary rather than an implied missing row inside the current packet set.

## Source Refs

- `docs/governance/views/view-old-s0-narrative-history-pilot-s0a-s0b-v1.md`
- `docs/governance/views/view-old-s0-narrative-history-packet-s0d-s0c-v1.md`
- `docs/governance/views/view-old-s0-narrative-history-packet-s0e-v1.md`
- `docs/governance/views/view-old-s0-series-s0f-standing-v1.md`
- `docs/governance/views/view-old-s0-remaining-history-line-detail-v1.md`
- `docs/logs/log-S0F-5I-old-s0-narrative-history-widening-across-counted-series.md`