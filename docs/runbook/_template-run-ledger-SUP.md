# run-ledger-supplement-template-v1

Use this supplement when later evidence needs to strengthen, refine, narrow, or reopen one verdict already admitted in an existing run ledger.
This SUP file owns later evidence admission and review for one run-ledger row; it does not replace the parent run ledger.

## Naming Rule

- Name SUP ledgers as `ledger-run-SUP-<sequence>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- `<sequence>` is the append-only supplement round for the bound runbook release.
- Preferred example shape:
  - `ledger-run-SUP-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`

## Minimal Header

```yaml
runbook_run_ledger_supplement:
  supplement_series_id: <ledger-run-SUP-WORKFLOW-GITHUB-001-summary>
  supplement_sequence: <001>
  supplement_id: <ledger-run-SUP-001-WORKFLOW-GITHUB-001-summary>
  supplement_kind: runbook-run-ledger-supplement
  status: <draft|active|completed>
  owner_lane: <S0G-2A>
  parent_run_ledger_id: <ledger-run-001-WORKFLOW-GITHUB-001-summary>
  parent_runbook_id: <run-WORKFLOW-GITHUB-001-summary>
  parent_run_row_id: <RUN-001>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  affected_bridge_ids:
    - <RB-01|none>
  affected_coverage_ids:
    - <SC-01|none>
  supplement_scope: <what later evidence this packet is admitting>
  target_reading_goal: <what later readers should understand after this supplement is applied>
```

## Evidence Table

| supplement item id | parent run row id | evidence ref | evidence type | attachment ids | verification status | effect on current verdict | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001-SUP-01>` | `<RUN-001>` | `<artifact path|workflow url|screenshot path>` | `<json|log|screenshot|transcript|other>` | `<RUN-001-SUP-01-ATT-01>` | `<pending|verified|rejected>` | `<supports-existing|sharpens-existing|narrows-existing|revises-existing|conflicts-needs-review>` | `<no-change|append-evidence|rewrite-run-row|reopen-run-verdict>` | `<none|rewrite-source-log|rewrite-contract|defer>` | `<why this evidence matters>` |

## Attachment Review Table

| attachment id | supplement item id | click-through asset ref | review status | approval basis | review note |
| --- | --- | --- | --- | --- | --- |
| `<RUN-001-SUP-01-ATT-01>` | `<RUN-001-SUP-01>` | `[open asset](./asset-name.png)` | `<pending|accepted-for-packet|needs-better-evidence|rejected>` | `<why this attachment is sufficient or insufficient>` | `<what the reviewer checked>` |

## Actor and Provenance Review Table

| supplement item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001-SUP-01>` | `<unknown|pending|role:operator|name>` | `<unknown|pending|role:runbook-maintainer|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-artifact-inspection|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-packet|needs-better-evidence|rejected>` | `<why the approval state is defended>` | `<why any actor fields remain partial>` |

## Required Rules

- Every SUP row must point to one existing `parent run row id`.
- `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at` are required header fields; keep them present even when the defended value is still `unknown` or `pending`.
- SUP rows may strengthen or revise a prior verdict, but they may not invent a free-floating new run outside the parent ledger.
- `affected_bridge_ids` and `affected_coverage_ids` are optional reference lists for audited bridge/coverage write-back only; they must not replace the actual bridge or coverage semantics on the runbook or contract surfaces.
- Write into contracts or source logs only after the parent run ledger is updated or explicitly left unchanged.

## Completion Rule

- A SUP ledger may be marked `completed` only when every admitted evidence row has one explicit `verification status` and one explicit proposed parent-ledger action.