# Old S0 Issue-Only Reconstructed Ancestry Detail v1

## Purpose

- This view is the first reader-facing detail surface for early old-`S0` ancestry that currently sits outside the counted root-log review scope.
- It exists so readers can inspect each known `S0A` / `S0B` supplemental anchor, see what evidence actually exists locally, and see which parts still remain unresolved.
- It is a supplemental history/view surface, not a current `DOC` contract landing, not part of the counted `84`-row old-`S0` overview, and not part of the counted `63`-row non-surfaced remainder.

## Detail Boundary

- This surface expands the anchor set first declared in `view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md`.
- It covers only the currently known early anchors outside counted scope:
  - one preserved legacy `S0A` carry-forward log
  - one preserved legacy `S0B` parent ADR anchor
  - one known `S0B-1A` missing-log placeholder that still lacks local issue materialization
- It does not claim that the full early ancestry is already reconstructed.
- It does make the current evidence state explicit enough that later reconstruction work can be bounded rather than guessed.

## Detail Model

| field | job |
| --- | --- |
| `ancestry item` | the supplemental early-history anchor under review |
| `current evidence class` | whether the anchor currently survives as a legacy log, legacy ADR, or unresolved issue-only placeholder |
| `current local anchor` | the local path or local evidence state available now |
| `counted-scope status` | whether the anchor is already counted in the old-`S0` overview |
| `provisional reconstructed standing` | the best current reader-facing standing without fabricating missing evidence |
| `why this standing now` | short explanation for the provisional standing |
| `next safe reconstruction step` | the next bounded step if later reconstruction work proceeds |

## Supplemental Anchor Detail

| ancestry item | current evidence class | current local anchor | counted-scope status | provisional reconstructed standing | why this standing now | next safe reconstruction step |
| --- | --- | --- | --- | --- | --- | --- |
| `S0A` legacy carry-forward anchor | `legacy log carry-forward` | `legacy/from_structured_docs/from-logs/v2-logs/log-S0A-dlq-replay-platform.md` | `outside counted scope` | `retain as supplemental direct history` | `the repo holds one concrete early `S0A` text body, so readers can already inspect a real historical anchor without inventing missing logs or silently changing the counted overview` | `if needed, publish one later bounded reconstruction note that states how this legacy `S0A` anchor relates to later counted old-S0 governance lines without admitting it into counted scope by default` |
| `S0B` parent legacy decision anchor | `legacy ADR carry-forward` | `legacy/from_structured_docs/from-adrs/adr-S0B-docs-management-v2.md` | `outside counted scope` | `lineage-support anchor` | `the ADR is a stable parent-level decision surface with explicit docs-management v2 decision content and context issues `#43, #44`, but it is not one counted root `docs/logs/log-S0*.md` row` | `use it as the bounded parent decision anchor if one later reconstruction packet needs to explain how the counted `S0B-2A` / `S0B-3A` rows inherited earlier taxonomy and cutover decisions` |
| `S0B-1A` missing-log ancestry | `issue-only placeholder` | `no local source log or local issue artifact is materialized yet` | `outside counted scope` | `standing-first unresolved supplemental ancestry` | `the repo currently knows the anchor matters historically, but there is not yet one locally materialized issue body, issue summary, or source-log surrogate that can defend a stronger standing without fabrication` | `materialize one bounded issue-only evidence packet first, then decide whether the result should read as retained direct history, lineage-only support, or still remain outside counted scope` |

## Current Reader Conclusions

- `S0A` is now readable as real supplemental direct history because one concrete legacy text body exists locally.
- `S0B` parent ancestry is now readable as parent-level lineage support because one stable ADR anchor exists locally and exposes the decision boundary plus context-issue references.
- `S0B-1A` still cannot honestly be shown as more than unresolved supplemental ancestry until one issue-only evidence packet exists locally.
- This means the current supplemental branch is already useful for reader clarity even though it is not yet a complete reconstruction set.

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `which exact early S0A / S0B anchors exist outside counted scope, and what evidence do they currently have?` | `view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md` | this surface expands the supplemental anchor set row by row |
| `which earlier anchors exist outside the counted 84-row old-S0 review scope at all?` | `view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md` | the routing view remains the first-open boundary surface |
| `which counted S0B rows are already part of the current old-S0 review scope?` | `view-old-s0-series-s0b-standing-v1.md` | the counted `S0B` series standing remains separate from this supplemental ancestry layer |
| `what is the counted old-S0 overview for the current root-log review scope?` | `view-old-s0-absorption-coverage-overview-v1.md` | the aggregate overview remains the counted-scope summary |

## Reader Notes

- This detail surface is intentionally evidence-first.
- It prefers `known local anchor plus explicit gap` over speculative reconstruction.
- The provisional standings here are reader-facing support standings, not automatic promotion decisions.
- If later reconstruction work lands, it should update this detail surface before asking the counted overview to absorb any new rows.

## Source Refs

- `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`
- `docs/governance/views/view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md`
- `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
- `docs/governance/views/view-old-s0-series-s0b-standing-v1.md`
- `legacy/from_structured_docs/from-logs/v2-logs/log-S0A-dlq-replay-platform.md`
- `legacy/from_structured_docs/from-adrs/adr-S0B-docs-management-v2.md`