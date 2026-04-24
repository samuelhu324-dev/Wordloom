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
- If table-cell rendering is too weak for the active review surface, add one table-external `Attachment Quick Review` block with standalone links and optional inline previews.
- `review status` records whether the attachment is merely listed, accepted as sufficient for this packet, still too weak, or rejected.
- `approval basis` should stay short and claim-facing: it explains why the visible attachment is good enough to support the packet judgment.
- `review note` should stay compact and reviewer-facing: record what was checked, what was visible, or why the evidence is still insufficient.

## Recommended Rich Packet Shape

- The minimum valid SUP packet may stop at header plus `Decision Frame`, `Evidence Table`, one accountability surface, and the write-back rollups.
- Prefer a richer packet shape when reviewers are expected to audit the packet directly rather than only trust the resulting write-back.
- For screenshot-backed packets, the default richer shape should usually include:
  - `Attachment Inventory`
  - `Attachment Review Table`
  - optional `Attachment Quick Review`
  - optional `Evidence Time Audit`
- For markdown- or log-backed packets with no separate attachments, the default richer shape should usually include:
  - `Actor and Provenance Review Table`
  - `Evidence Time Audit`
  - one explicit downstream-reading or contract-deferred rollup
- Use the richer shape whenever the packet is expected to act as a first-class reviewer surface in later archaeology, not only as a minimal pass-through packet.

## Actor and Provenance Field Rule

- When packet-level evidence accountability matters, add one `Actor and Provenance Review Table` beneath the attachment-review surfaces.
- Keep this field set minimal: `submitted by`, `evidence owner`, `reviewed by`, `verified by`, `verification method`, `approved by`, `approval state`, and `approval basis`.
- These fields describe packet-level accountability only; they do not replace the routing verdict, the attachment review record, or any later permissions model.
- Historical packets may use defended partial values such as `unknown`, `pending`, role-based labels, or delegated labels instead of inventing named actors.
- Prefer one concise `provenance note` when the actor chain is incomplete but still bounded enough for the packet to remain useful.

## Incomplete-History Representation Rule

- Use `unknown` when the packet cannot currently defend the actor identity.
- Use `pending` when the actor or state is expected to be filled later but is not yet resolved.
- Use `role:<role-name>` when the packet can defend the responsible role but not the named person.
- Use `delegated:<role-name>` when the packet can defend that authority was delegated to one role boundary without yet naming the final actor.
- Do not fabricate named individuals or over-precise authority chains merely to fill the table.
- A packet may remain partially specified when the evidence remains useful and the missing actor detail is stated explicitly in `provenance note`.

## Actor and Provenance Review Table

Use this when the packet needs explicit accountability for submission, verification, and approval.

| supplement item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<S0A-1A-R02-SUP-01>` | `<unknown|pending|role:operator|delegated:review-lead|name>` | `<unknown|pending|role:workflow-owner|name>` | `<unknown|pending|role:reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-screenshot-inspection|direct-markdown-inspection|source-path-check|manual-replay|transcript-comparison|other>` | `<unknown|pending|role:approver|delegated:records-lead|name>` | `<pending|accepted-for-packet|needs-better-evidence|rejected>` | `<why this approval state is currently defended>` | `<why any actor fields remain partial or how the current provenance chain is bounded>` |

## Attachment Review Table

Use this when screenshot or other file-backed evidence needs direct reviewer access from the packet.

| attachment id | supplement item id | click-through asset ref | review status | approval basis | review note |
| --- | --- | --- | --- | --- | --- |
| `<S0A-1A-R02-SUP-01-SHOT-01>` | `<S0A-1A-R02-SUP-01>` | `[open asset](./S0A-1A-R02-SUP-01-SHOT-01-projects-status-board.png)` | `<pending|accepted-for-packet|needs-better-evidence|rejected>` | `<why this attachment is good enough, or not good enough, for the current packet>` | `<what the reviewer checked or what remains missing>` |

## Optional Attachment Quick Review

Use this when reviewers need one table-external place to open or visually inspect attachments directly.

- `Attachment`: `[S0A-1A-R02-SUP-01-SHOT-01](./S0A-1A-R02-SUP-01-SHOT-01-projects-status-board.png)`
- `Preview`:

  ![S0A-1A-R02-SUP-01-SHOT-01 preview](./S0A-1A-R02-SUP-01-SHOT-01-projects-status-board.png)

- `Review focus`: `<what the reviewer should confirm from this attachment>`

- Use this block only when direct human review readability matters enough to justify the extra vertical space.
- Keep the main packet verdict in `Evidence Table` and `Attachment Review Table`; this block is a review aid, not the canonical routing surface.

## Optional Evidence Time Audit

Use this when one supplement row needs explicit audit of source execution time, source recording time, or historical-effective range.

| supplement item id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<S0A-1A-R02-SUP-01>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone or offset note>` | `<why this evidence time audit matters>` |

- `source observed at` is the best known time the evidence event, experiment, or source snapshot was executed or observed.
- `source recorded at` is the best known time the evidence document itself was written or admitted.
- `source effective from` and `source effective until` describe the best known historical-effective range for the rule signal carried by that evidence row.
- `time precision` must remain evidence-bound; if the source proves only a day, keep `day` rather than inventing seconds.
- Prefer this section for markdown-evidence packets whenever the parent-ledger row chronology will later depend on the SUP packet rather than on the issue-only parent source alone.

## Required Rules

- Every SUP row must point to one existing `parent row id`; a SUP ledger may not invent free-floating new slices.
- `supplement_item_id` is required for every admitted evidence item.
- `attachment ids` should stay empty when no attached asset is needed; when assets exist, each asset should receive one stable id rather than being referenced only by prose.
- Screenshot-backed verdicts should prefer one `Attachment Review Table` row per attachment whenever direct reviewer click-through matters.
- When table-cell links are not sufficiently reviewable in the active editor or preview surface, prefer adding one `Attachment Quick Review` section rather than overloading the main evidence tables.
- When actor/provenance accountability matters, prefer one `Actor and Provenance Review Table` row per supplement item rather than scattering those fields across prose notes.
- `verification status` records whether the evidence is merely proposed, verified enough for judgment, or rejected for this SUP round.
- `effect on current verdict` states how the admitted evidence relates to the current parent-ledger judgment.
- `proposed parent-ledger action` states what the parent ledger should do if that effect is accepted.
- `contract impact` is downstream-only guidance; it may not be applied before the parent ledger is updated or explicitly left unchanged.
- Keep `contract impact` narrow: it states what kind of downstream contract action may follow, not the full current-reader explanation after write-back.
- If reviewers also need one concise note about whether the accepted evidence is expected to sharpen a broad parent summary, clarify one narrow current reader, or leave the downstream reader unchanged, prefer one optional rollup or reader note instead of adding a new evidence-table column.

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
- `attachment review table`:
  - use when stable repo-local assets or attached files are part of the approval-facing evidence surface
- `attachment quick review`:
  - use when direct reviewer click-through or inline preview materially improves the review surface
- `contract changes deferred until parent write-back`:
  - list any contract records that may need change only after the parent ledger is updated
- `rejected evidence`:
  - list proposed evidence rows that were intentionally not admitted in this round
- `downstream reading note`:
  - use this optional rollup when accepted evidence changes how a later reader should interpret the routed slice after parent-ledger write-back, for example `broad parent summary unchanged`, `narrow current reader clarified`, or `child-opening still deferred`
  - keep this note short and post-write-back facing; it complements `contract impact` but does not replace the evidence verdict, the proposed parent-ledger action, or later contract-local reading sections

## House Style Note

- The repo now treats the richer packet shape as the preferred default when one SUP file is expected to survive as a reusable reviewer surface.
- Do not read the optional sections above as discouraged; they are optional only because not every evidence type needs every review surface.
- If a current bounded sample already demonstrates a richer and cleaner packet shape for the same evidence class, prefer matching that sample rather than collapsing back to the minimum valid packet.