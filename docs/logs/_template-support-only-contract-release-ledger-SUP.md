# support-only-contract-release-ledger-SUP-template

## Purpose

- Use this ledger when later evidence needs to strengthen, sharpen, narrow, revise, or reopen one routing verdict that already lives in an existing source-owned support-only contract-release ledger.
- This SUP ledger owns `evidence admission, verdict refinement, and parent-ledger write-back recommendation`.
- Do not use this SUP ledger to bypass the parent ledger and write directly into contracts; the parent ledger remains the owner of source-slice routing.

## Naming Rule

- Name SUP ledgers as `ledger-SUP-<source-id>-<sequence>-<source-summary>.md`.
- The `<source-id>` must match the attached parent ledger.
- The `<source-summary>` should summarize the supplement round itself and does not need to duplicate the parent-ledger summary when a narrower evidence packet name is clearer.
- The `<sequence>` must be one append-only three-digit supplement round such as `001`, `002`, or `003` inside one stable supplement series.
- Preferred example shapes:
  - `ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
  - `ledger-SUP-S0B-2A-002-tools-scripts-and-snapshots-management.md`

- The stable parent binding is carried by `supplement_series_id` plus `parent_ledger_id`; readers should not rely on the filename summary alone to infer attachment.

## Minimal Header

```yaml
support_only_contract_release_ledger_supplement:
  supplement_series_id: <ledger-SUP-S0A-1A>
  supplement_sequence: <001>
  supplement_id: <ledger-SUP-S0A-1A-001-source-summary>
  supplement_kind: support-only-contract-release-ledger-supplement
  status: <draft|active|completed>
  owner_lane: <S0F-7D>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  parent_ledger_id: <ledger-S0A-1A-source-summary>
  parent_source_id: <S0A-1A>
  parent_source_ref: <issue/log/support-only source already owned by the parent ledger>
  supplement_scope: <what later evidence this supplement is admitting>
  target_reading_goal: <what later reader should understand after this supplement is applied>
```

## Lifecycle Field Rule

- `supplement_series_id` is the stable sequence family for repeated supplement rounds attached to one parent source.
- `supplement_sequence` is the append-only round number inside that series; do not reuse or renumber older rounds once admitted.
- New writes should use canonical UTC second timestamps such as `2026-04-12T15:18:05Z` for supplement-lifecycle fields.
- Legacy day-only values may remain when older rounds do not yet have defended second-level audit timestamps.
- Local-time display belongs in an optional mirror field or prose note only; the canonical stored timestamp should remain UTC when second-level precision is available.
- `created_at` records when this supplement file was first created in the repo.
- `reviewed_at` records when this supplement round first reached defended review state.
- `accepted_at` records when the row-level verdicts are accepted for parent-ledger write-back.
- `writeback_started_at` records when the accepted parent-ledger or contract write-back begins.
- `writeback_completed_at` records when that write-back is complete in the repo.
- These fields are artifact-lifecycle timestamps only; historical-effective rule timing belongs in contract chronology fields, not here.

## Asset and Item Id Rule

- Every SUP row must carry one `supplement_item_id`.
- Name it as `<parent-row-id>-SUP-<n>`.
- Every attachment beneath one SUP row must carry one stable `attachment_id`.
- Use `<supplement-item-id>-ATT-<n>` for generic assets and `<supplement-item-id>-SHOT-<n>` when the asset is specifically a screenshot.
- When a stable repo-local file exists, the attachment reference should be rendered as one clickable markdown link rather than as bare path prose only.

## Evidence Table Shape

| supplement item id | parent row id | evidence ref | evidence type | attachment ids | verification status | effect on current verdict | proposed parent-ledger action | contract impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<S0A-1A-R02-SUP-01>` | `<S0A-1A-R02>` | `<code path|md path|issue|oral note|other evidence anchor>` | `<code|md|issue|log|oral|screenshot|other>` | `<S0A-1A-R02-SUP-01-SHOT-01>` | `<pending|verified|rejected>` | `<supports-existing|sharpens-existing|narrows-existing|revises-existing|conflicts-needs-review>` | `<no-change|add-supporting-evidence|rewrite-parent-row|split-parent-row|reopen-routing>` | `<none|rewrite-current-draft|open-new-release|defer-contract-change>` | `<why this evidence should or should not change the parent-ledger reading>` |

## Approval-Facing Attachment Review Rule

- Keep the main `Evidence Table` focused on routing and verdict semantics; do not turn it into an image gallery.
- When screenshot or other attached-file evidence materially supports the SUP verdict, add one `Attachment Review Table`.
- The attachment ref in that review table should be one clickable markdown link whenever a stable repo-local asset exists.
- `review status` records whether the attachment is merely listed, accepted as sufficient for this packet, still too weak, or rejected.
- `approval basis` should stay short and claim-facing: it explains why the visible attachment is good enough to support the packet judgment.
- `review note` should stay compact and reviewer-facing: record what was checked, what was visible, or why the evidence is still insufficient.

## Attachment Review Table

Use this when screenshot or other file-backed evidence needs direct reviewer access from the packet.

| attachment id | supplement item id | click-through asset ref | review status | approval basis | review note |
| --- | --- | --- | --- | --- | --- |
| `<S0A-1A-R02-SUP-01-SHOT-01>` | `<S0A-1A-R02-SUP-01>` | `[open asset](./S0A-1A-R02-SUP-01-SHOT-01-projects-status-board.png)` | `<pending|accepted-for-packet|needs-better-evidence|rejected>` | `<why this attachment is good enough, or not good enough, for the current packet>` | `<what the reviewer checked or what remains missing>` |

## Optional Evidence Time Audit

Use this when one supplement row needs explicit audit of source execution time, source recording time, or historical-effective range.

| supplement item id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<S0A-1A-R02-SUP-01>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone or offset note>` | `<why this evidence time audit matters>` |

- `source observed at` is the best known time the evidence event, experiment, or source snapshot was executed or observed.
- `source recorded at` is the best known time the evidence document itself was written or admitted.
- `source effective from` and `source effective until` describe the best known historical-effective range for the rule signal carried by that evidence row.
- `time precision` must remain evidence-bound; if the source proves only a day, keep `day` rather than inventing seconds.

## Required Rules

- Every SUP row must point to one existing `parent row id`; a SUP ledger may not invent free-floating new slices.
- `supplement_item_id` is required for every admitted evidence item.
- `attachment ids` should stay empty when no attached asset is needed; when assets exist, each asset should receive one stable id rather than being referenced only by prose.
- Screenshot-backed verdicts should prefer one `Attachment Review Table` row per attachment whenever direct reviewer click-through matters.
- `verification status` records whether the evidence is merely proposed, verified enough for judgment, or rejected for this SUP round.
- `effect on current verdict` states how the admitted evidence relates to the current parent-ledger judgment.
- `proposed parent-ledger action` states what the parent ledger should do if that effect is accepted.
- `contract impact` is downstream-only guidance; it may not be applied before the parent ledger is updated or explicitly left unchanged.

## Escalation Rule

- When the effect is `supports-existing` or `sharpens-existing`, prefer `add-supporting-evidence` or another minimal parent-ledger write-back.
- When the effect is `narrows-existing` or `revises-existing`, prefer `rewrite-parent-row` or `split-parent-row` before any contract rewrite.
- When the effect is `conflicts-needs-review`, prefer `reopen-routing`; do not write directly into contract release fields.
- If a SUP row cannot be tied to one existing parent row id, open a new bounded source or continuation packet instead of forcing the evidence into this SUP ledger.

## Completion Rule

- A SUP ledger may be marked `completed` only when every admitted evidence row has one explicit `verification status` and one explicit proposed parent-ledger action.
- A SUP ledger is not complete merely because evidence has been collected; the row verdicts must be explicit.

## Optional Rollup

- `parent-ledger rows to update`:
  - list the exact parent row ids that should be rewritten or supplemented
- `attachment inventory`:
  - list screenshot, transcript, export, or similar asset ids admitted in this round
- `contract changes deferred until parent write-back`:
  - list any contract records that may need change only after the parent ledger is updated
- `rejected evidence`:
  - list proposed evidence rows that were intentionally not admitted in this round