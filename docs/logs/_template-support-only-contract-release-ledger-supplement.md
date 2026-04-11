# support-only-contract-release-ledger-supplement-template

## Purpose

- Use this ledger when later evidence needs to strengthen, sharpen, narrow, revise, or reopen one routing verdict that already lives in an existing source-owned support-only contract-release ledger.
- This supplement owns `evidence admission, verdict refinement, and parent-ledger write-back recommendation`.
- Do not use this supplement to bypass the parent ledger and write directly into contracts; the parent ledger remains the owner of source-slice routing.

## Naming Rule

- Name supplement ledgers as `ledger-supplement-<source-id>-<source-summary>.md`.
- The `<source-id>` and `<source-summary>` must match the attached parent ledger.
- Preferred example shapes:
  - `ledger-supplement-S0A-1A-tools-github-issues-projects-and-tags.md`
  - `ledger-supplement-S0B-2A-tools-scripts-and-snapshots-management.md`

## Minimal Header

```yaml
support_only_contract_release_ledger_supplement:
  supplement_id: <ledger-supplement-S0A-1A-source-summary>
  supplement_kind: support-only-contract-release-ledger-supplement
  status: <draft|active|completed>
  owner_lane: <S0F-7D>
  parent_ledger_id: <ledger-S0A-1A-source-summary>
  parent_source_id: <S0A-1A>
  parent_source_ref: <issue/log/support-only source already owned by the parent ledger>
  supplement_scope: <what later evidence this supplement is admitting>
  target_reading_goal: <what later reader should understand after this supplement is applied>
```

## Asset and Item Id Rule

- Every supplement row must carry one `supplement_item_id`.
- Name it as `<parent-row-id>-SUP-<n>`.
- Every attachment beneath one supplement row must carry one stable `attachment_id`.
- Use `<supplement-item-id>-ATT-<n>` for generic assets and `<supplement-item-id>-SHOT-<n>` when the asset is specifically a screenshot.

## Evidence Table Shape

| supplement item id | parent row id | evidence ref | evidence type | attachment ids | verification status | effect on current verdict | proposed parent-ledger action | contract impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<S0A-1A-R02-SUP-01>` | `<S0A-1A-R02>` | `<code path|md path|issue|oral note|other evidence anchor>` | `<code|md|issue|log|oral|screenshot|other>` | `<S0A-1A-R02-SUP-01-SHOT-01>` | `<pending|verified|rejected>` | `<supports-existing|sharpens-existing|narrows-existing|revises-existing|conflicts-needs-review>` | `<no-change|add-supporting-evidence|rewrite-parent-row|split-parent-row|reopen-routing>` | `<none|rewrite-current-draft|open-new-release|defer-contract-change>` | `<why this evidence should or should not change the parent-ledger reading>` |

## Required Rules

- Every supplement row must point to one existing `parent row id`; a supplement may not invent free-floating new slices.
- `supplement_item_id` is required for every admitted evidence item.
- `attachment ids` should stay empty when no attached asset is needed; when assets exist, each asset should receive one stable id rather than being referenced only by prose.
- `verification status` records whether the evidence is merely proposed, verified enough for judgment, or rejected for this supplement round.
- `effect on current verdict` states how the admitted evidence relates to the current parent-ledger judgment.
- `proposed parent-ledger action` states what the parent ledger should do if that effect is accepted.
- `contract impact` is downstream-only guidance; it may not be applied before the parent ledger is updated or explicitly left unchanged.

## Escalation Rule

- When the effect is `supports-existing` or `sharpens-existing`, prefer `add-supporting-evidence` or another minimal parent-ledger write-back.
- When the effect is `narrows-existing` or `revises-existing`, prefer `rewrite-parent-row` or `split-parent-row` before any contract rewrite.
- When the effect is `conflicts-needs-review`, prefer `reopen-routing`; do not write directly into contract release fields.
- If a supplement row cannot be tied to one existing parent row id, open a new bounded source or continuation packet instead of forcing the evidence into this supplement.

## Completion Rule

- A supplement may be marked `completed` only when every admitted evidence row has one explicit `verification status` and one explicit proposed parent-ledger action.
- A supplement is not complete merely because evidence has been collected; the row verdicts must be explicit.

## Optional Rollup

- `parent-ledger rows to update`:
  - list the exact parent row ids that should be rewritten or supplemented
- `attachment inventory`:
  - list screenshot, transcript, export, or similar asset ids admitted in this round
- `contract changes deferred until parent write-back`:
  - list any contract records that may need change only after the parent ledger is updated
- `rejected evidence`:
  - list proposed evidence rows that were intentionally not admitted in this round