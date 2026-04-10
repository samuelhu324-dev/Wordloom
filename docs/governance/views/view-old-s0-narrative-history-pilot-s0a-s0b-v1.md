# Old S0 Narrative History Pilot S0A S0B v1

## Purpose

- This view is the first reader-facing narrative-history pilot for old-`S0`.
- It exists so readers can understand why the early `S0A + S0B` packet appeared, what problems it addressed, what results it left behind, and where those results later read now.
- It complements standing and routing views; it does not replace them.

## Pilot Boundary

- This pilot covers one bounded five-item mixed set only:
  - `S0A` legacy carry-forward anchor
  - `S0B` parent ADR anchor
  - `S0B-2A`
  - `S0B-3A`
  - `S0B-1A` unresolved issue-only placeholder
- It intentionally combines counted `S0B` mainline reading with supplemental `S0A / S0B` ancestry reading.
- It does not yet widen to `S0C`, `S0D`, `S0E`, or `S0F`.

## Narrative Model

| field | job |
| --- | --- |
| `source log` | the exact historical source or bounded ancestry item under review |
| `why it appeared` | the trigger or pressure that caused the item to exist |
| `scoped problem` | the boundary or problem the item tried to repair |
| `decision / result` | the result, decision, or stabilized outcome it left behind |
| `what changed after it` | the later inheritance or concentration path |
| `current historical role` | the current reader-facing role of the historical item |
| `current first-open home` | where readers should open next after understanding the row |
| `reader note` | compact ambiguity, exclusion, or caution note |

## Narrative History Rows

| source log | why it appeared | scoped problem | decision / result | what changed after it | current historical role | current first-open home | reader note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A` legacy carry-forward anchor | `once search and chronicle both needed replay safety, DLQ plus replay stopped being one projection-specific concern and became a shared platform pressure` | `failure handling, replay semantics, operator workflow, and SLO language would drift if each projection solved them separately` | `the retained `S0A` anchor defines DLQ/replay as one shared platform capability with a common contract, common operator mental model, shared SLO vocabulary, and control-group diagnosis framing` | `later repo-local worker, replay, and operational surfaces carry the implementation-level result, but no counted old-S0 row currently concentrates this early platform framing into the counted overview` | `supplemental direct history` | `view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md` | `this row remains outside the counted old-S0 overview even though it is now readable inside the supplemental ancestry branch` |
| `S0B` parent ADR anchor | `after script sprawl, snapshot sprawl, and fragile path memory had already become chronic repo friction, the line needed one parent decision rather than only local fixes` | `the repo lacked one stable decision on directory taxonomy, front matter, cutover rules, snapshot roots, and stub preservation` | `the ADR adopts docs-management v2 as the parent decision: stable taxonomy, stable entrypoint, unified snapshot roots, front matter metadata, and cutover plus stub policy` | `counted `S0B-2A` and `S0B-3A` later act as execution-level children that apply and refine this parent decision inside the counted old-S0 mainline` | `supplemental lineage-support anchor` | `legacy/from_structured_docs/from-adrs/adr-S0B-docs-management-v2.md` | `this anchor is outside counted scope because it survives as a legacy ADR rather than a counted root log` |
| `S0B-2A` | `cleanup of scripts and experiment outputs repeatedly exposed the same uncontrolled growth pattern` | `without taxonomy, stable entrypoint, unified snapshot roots, and cutover rules, the repo would fall back into script swamp and snapshot garbage accumulation` | `the row establishes the working governance skeleton for tools/scripts and snapshots management: species taxonomy, single CLI entry, unified evidence roots, cutover, and stub discipline` | `its current operational meaning now reads through `backend/scripts/cli.py`, script-area layout, and `docs/labs/_snapshot/` plus `docs/runbook/_snapshot/` rather than through the row as one current DOC surface` | `retained governance evidence` | `backend/scripts/cli.py` plus `docs/labs/_snapshot/` and `docs/runbook/_snapshot/`` | `this is counted `S0B` mainline history, but it remains outside the surfaced DOC set because the live repo surfaces now carry the active result` |
| `S0B-3A` | `once directory and workflow evolution accelerated, naming, chronology, module identity, and mechanical metadata could no longer stay coupled` | `the repo needed one scheme that decoupled time order from delivery identity and made metadata mechanically maintainable across logs, labs, issues, runbooks, and ADRs` | `the row fixes unified indices, legacy taxonomy handling, and front matter as the stable naming-and-metadata model for later governance evolution` | `that result later survives as one structural prerequisite in current DOC history reading rather than as an unresolved standalone old row` | `structural prerequisite inside counted mainline` | `view-doc-history-and-lineage-v1.md` | `this row is already surfaced into the current DOC history view because later DOC reading depends on the naming and front-matter model it stabilized` |
| `S0B-1A` unresolved issue-only placeholder | `the early docs-management line appears to have one more historically relevant child item before the counted `S0B` mainline fully stabilizes` | `the repo does not currently have one local source log, local issue artifact, or equivalent retained packet that can defend a stronger historical statement` | `no defended decision or result should be claimed yet; the correct result is currently an explicit unresolved placeholder` | `a later bounded issue-only evidence packet is required before this row can be upgraded from placeholder into direct history or lineage support` | `unresolved supplemental ancestry` | `view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md` | `this row is intentionally visible so the narrative pilot does not fake completeness where source evidence is still missing` |

## Reader Summary

- `S0A` explains the pre-counted platform pressure: DLQ/replay became infrastructure rather than one narrow script fix.
- The `S0B` parent ADR turns that pressure into one governance decision package for taxonomy, metadata, cutover, and snapshot roots.
- `S0B-2A` applies that package as concrete tooling and evidence-governance structure.
- `S0B-3A` tightens the naming/index/front-matter side and later becomes a structural prerequisite for current DOC history reading.
- `S0B-1A` remains the explicit early gap: historically relevant, but still not materially reconstructable from local source-owned evidence.

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `why did the early S0A + S0B packet exist, and what did it leave behind?` | `view-old-s0-narrative-history-pilot-s0a-s0b-v1.md` | this pilot is the first reader-facing answer to that narrative question |
| `which exact early anchors exist outside counted scope?` | `view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md` | the supplemental detail view remains the exact-anchor inventory |
| `inside counted S0B, what is the current standing of each row?` | `view-old-s0-series-s0b-standing-v1.md` | the counted series standing view remains the current-state answer |
| `how much of old S0 is surfaced overall?` | `view-old-s0-absorption-coverage-overview-v1.md` | aggregate absorption remains a separate count-first question |

## Reader Notes

- This pilot exists to answer `why / problem / result / inheritance`, not merely `current home`.
- Narrative history and standing classification are complementary:
  - use this pilot when the reader needs the change story
  - use standing or routing views when the reader needs current placement, surfaced status, or manual-screening state
- The unresolved `S0B-1A` row is part of the pilot by design so the field model proves it can represent missing historical evidence honestly.

## Source Refs

- `docs/logs/log-S0F-5H-old-s0-narrative-history-view-pilot.md`
- `legacy/from_structured_docs/from-logs/v2-logs/log-S0A-dlq-replay-platform.md`
- `legacy/from_structured_docs/from-adrs/adr-S0B-docs-management-v2.md`
- `docs/logs/log-S0B-2A-scripts-snapshots-management.md`
- `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md`
- `docs/governance/views/view-old-s0-series-s0b-standing-v1.md`
- `docs/governance/views/view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md`