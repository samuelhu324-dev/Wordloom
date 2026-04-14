# Old S0 Issue-Only Reconstructed Ancestry Routing v1

## Purpose

- This view is the first reader-facing routing surface for early old-`S0` ancestry that currently survives only through legacy carry-forward files or issue-only evidence.
- It exists so readers can see that the counted old-`S0` root-log review scope is intentionally bounded and does not yet equal the full earliest ancestry picture.
- It is a supplemental history/view surface, not a current `DOC` contract landing, not part of the counted `84`-row old-`S0` overview, and not part of the counted `63`-row non-surfaced remainder.

## Boundary

- This surface covers only ancestry that is currently outside the counted root-log review scope because it is missing from the present root-log population used by the old-`S0` overview views.
- It currently includes three reader-facing anchor classes:
  - legacy carry-forward `S0A` anchor that still exists on disk
  - legacy carry-forward `S0B` parent decision anchor that still exists on disk
  - known `S0B-1A` missing-log ancestry that currently needs issue-only reconstruction rather than root-log replay
- This surface does not change aggregate counts yet.
- Any future admission of these anchors into counted scope should happen only through one later explicit reconstruction packet.

## Current Supplemental Anchors

| ancestry anchor | evidence now | counted in old-S0 overview now | open first | why |
| --- | --- | --- | --- | --- |
| `S0A` legacy carry-forward anchor | `legacy/from_structured_docs/from-logs/v2-logs/log-S0A-dlq-replay-platform.md` | `no` | `view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md` | the repo still has one preserved pre-current-format `S0A` log, but the current overview intentionally counts only root `docs/logs/log-S0*.md` review-scope rows |
| `S0B` parent legacy decision anchor | `legacy/from_structured_docs/from-adrs/adr-S0B-docs-management-v2.md` | `no` | `view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md` | the repo still has one preserved `S0B` parent decision anchor, but it is an ADR carry-forward artifact rather than one counted current root log |
| `S0B-1A` issue-only missing-log ancestry | `issue-only evidence not yet materialized locally` | `no` | `view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md` | the ancestry is known to matter historically, but the repo does not currently hold one matching source log, so the next safe step is bounded issue-only reconstruction rather than fabricated source-log backfill |

## Reconstruction Rules

- Treat these anchors as supplemental reader support first, not as automatic counted-scope rows.
- Do not fabricate a fake historical root log just to make the overview totals look complete.
- If a later reconstruction packet lands, it should record:
  - what evidence exists locally versus only on GitHub
  - whether the result is retained direct history, lineage-only support, or some later counted-scope adjustment
  - why the reconstructed result still should or should not affect the counted old-`S0` overview totals

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `does the current old-S0 overview already include the earliest S0A and issue-only S0B ancestry?` | `view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md` | this surface makes the exclusion boundary explicit |
| `which known early anchors exist outside the counted 84-row old-S0 review scope?` | `view-old-s0-issue-only-reconstructed-ancestry-routing-v1.md` | the supplemental anchor list lives here |
| `which exact early anchors exist, what evidence do they have now, and which ones remain unresolved?` | `view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md` | the detail surface expands the current supplemental anchor set row by row |
| `why did the early S0A + S0B packet exist, and what results did it leave behind?` | `view-old-s0-narrative-history-pilot-s0a-s0b-v1.md` | the narrative-history pilot explains emergence, problem, result, and inheritance across the mixed early packet |
| `what is the counted old-S0 overview for the current root-log review scope?` | `view-old-s0-absorption-coverage-overview-v1.md` | the aggregate view remains the canonical counted-scope summary |
| `what is the counted non-surfaced remainder inside the current root-log review scope?` | `view-old-s0-remaining-history-line-routing-v1.md` | the remainder-routing view remains the canonical counted-scope remainder surface |

## Reader Notes

- This surface exists to prevent a false completeness impression.
- The current old-`S0` overview is still correct for its bounded counted scope.
- What it does not yet do is represent every earlier issue-only or legacy-only ancestry anchor.
- Use this view when the question is about that missing ancestry layer rather than about the already-counted root-log population.
- Use `view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md` when the question moves from `is there an excluded ancestry branch?` to `what exactly is currently known inside that branch?`

## Source Refs

- `docs/logs/log-S0F-5G-remaining-old-s0-history-line-expansion-and-manual-screening.md`
- `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
- `docs/governance/views/view-old-s0-remaining-history-line-routing-v1.md`
- `docs/governance/views/view-old-s0-issue-only-reconstructed-ancestry-detail-v1.md`
- `docs/governance/views/view-old-s0-narrative-history-pilot-s0a-s0b-v1.md`
- `legacy/from_structured_docs/from-logs/v2-logs/log-S0A-dlq-replay-platform.md`
- `legacy/from_structured_docs/from-adrs/adr-S0B-docs-management-v2.md`