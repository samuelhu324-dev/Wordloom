# run-ledger-supplement-template-v1

Use this supplement when later evidence needs to strengthen, refine, narrow, or reopen one verdict already admitted in an existing run ledger.
This SUP file owns later evidence admission and review for one existing run, target, or target-stage row; it does not replace the parent run ledger.

## Naming Rule

- Name SUP ledgers as `ledger-run-SUP-<sequence>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- `<sequence>` is the append-only supplement round for the bound runbook release.
- Preferred example shape:
  - `ledger-run-SUP-001-WORKFLOW-FAMILY-001-operator-surface.md`

## Minimal Header

```yaml
runbook_run_ledger_supplement:
  supplement_series_id: <ledger-run-SUP-RUNBOOK-FAMILY-001-summary>
  supplement_sequence: <001>
  supplement_id: <ledger-run-SUP-001-RUNBOOK-FAMILY-001-summary>
  supplement_kind: runbook-run-ledger-supplement
  status: <draft|active|completed>
  owner_lane: <S0G-3C>
  parent_run_ledger_id: <ledger-run-001-RUNBOOK-FAMILY-001-summary>
  parent_runbook_id: <run-RUNBOOK-FAMILY-001-summary>
  parent_run_row_id: <RUN-001>
  parent_target_row_id: <RUN-001-T01>
  parent_target_stage_row_id: <RUN-001-T01-STG-CREATION>
  parent_target_stage_attempt_id: <RUN-001-T01-STG-CREATION-A01|not-used>
  target_ref_key: <S4F-2A>
  target_ref_path: <docs/logs/log-S4F-2A-...md>
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

## Strong-Structure Bridge Rule

- Every SUP packet must attach to one existing `parent_run_row_id`.
- When the follow-up is target-specific, it must also attach to one existing `parent_target_row_id`.
- When the follow-up changes or sharpens one lifecycle stage, it must also attach to one existing `parent_target_stage_row_id`.
- `parent_target_stage_attempt_id` is optional and should be used only when the defended reading truly needs one replay/attempt layer below the stable target-stage row.
- Structural ids should stay sequence-only and machine-stable; semantic identity such as `S4F-2A` should stay in `target_ref_key` and `target_ref_path` rather than being embedded into the structural key itself.

## Evidence Table

| supplement item id | parent run row id | target row id | target stage row id | target stage attempt id | evidence ref | evidence type | attachment ids | verification status | effect on current verdict | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001-SUP-01>` | `<RUN-001>` | `<RUN-001-T01>` | `<RUN-001-T01-STG-CREATION>` | `<RUN-001-T01-STG-CREATION-A01|not-used>` | `<artifact path|workflow url|screenshot path>` | `<json|log|screenshot|transcript|other>` | `<RUN-001-SUP-01-ATT-01>` | `<pending|verified|rejected>` | `<supports-existing|sharpens-existing|narrows-existing|revises-existing|conflicts-needs-review>` | `<no-change|append-evidence|rewrite-run-row|rewrite-target-row|rewrite-target-stage-row|reopen-run-verdict>` | `<none|rewrite-source-log|rewrite-contract|defer>` | `<why this evidence matters>` |

## Target-Stage Reading Rule

- Use `effect on current verdict` to describe how the new evidence changes the defended reading.
- Use `proposed parent-ledger action` to say exactly which parent surface should move:
  - `no-change`
  - `append-evidence`
  - `rewrite-run-row`
  - `rewrite-target-row`
  - `rewrite-target-stage-row`
  - `reopen-run-verdict`
- If a follow-up only sharpens one existing stage while leaving the batch verdict intact, prefer `rewrite-target-stage-row` over broader parent-ledger actions.
- If one real follow-up also contains a repair diff, do not overload the SUP row to carry that repair meaning by itself; pair it with the corresponding `PATCH` packet instead.

## Attachment Review Table

| attachment id | supplement item id | click-through asset ref | review status | approval basis | review note |
| --- | --- | --- | --- | --- | --- |
| `<RUN-001-SUP-01-ATT-01>` | `<RUN-001-SUP-01>` | `[open asset](./asset-name.png)` | `<pending|accepted-for-packet|needs-better-evidence|rejected>` | `<why this attachment is sufficient or insufficient>` | `<what the reviewer checked>` |

## Actor and Provenance Review Table

| supplement item id | run row id | target row id | target stage row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001-SUP-01>` | `<RUN-001>` | `<RUN-001-T01>` | `<RUN-001-T01-STG-CREATION>` | `<unknown|pending|role:operator|name>` | `<unknown|pending|role:runbook-maintainer|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-artifact-inspection|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-packet|needs-better-evidence|rejected>` | `<why the approval state is defended>` | `<why any actor fields remain partial>` |

## Optional Evidence Time Audit

| supplement item id | run row id | target row id | target stage row id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001-SUP-01>` | `<RUN-001>` | `<RUN-001-T01>` | `<RUN-001-T01-STG-CREATION>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone note>` | `<why this evidence time audit matters>` |

## Write-Back Chain Rule

- The run follow-up chain is `evidence -> SUP -> parent run ledger -> downstream consumer`.
- `effect on current verdict` explains how the new evidence changes the already admitted reading.
- `proposed parent-ledger action` explains whether the parent run row, target row, or target-stage row should stay unchanged or be rewritten.
- `downstream impact` explains whether any source log, contract, or reader surface should move after the parent run ledger is updated.

## Required Rules

- Every SUP row must point to one existing `parent run row id`.
- Every target-specific SUP row must point to one existing `parent target row id`.
- Every stage-specific SUP row must point to one existing `parent target stage row id`.
- `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at` are required header fields; keep them present even when the defended value is still `unknown` or `pending`.
- SUP rows may strengthen or revise a prior verdict, but they may not invent a free-floating new run outside the parent ledger.
- `affected_bridge_ids` and `affected_coverage_ids` are optional reference lists for audited bridge/coverage write-back only; they must not replace the actual bridge or coverage semantics on the runbook or contract surfaces.
- Sequence ids in the SUP file must match the stable structural keys already present in the parent ledger; do not create ad hoc prose-only target names in place of those keys.
- Write into contracts or source logs only after the parent run ledger is updated or explicitly left unchanged.

## Completion Rule

- A SUP ledger may be marked `completed` only when every admitted evidence row has one explicit `verification status`, one explicit structural attachment point, and one explicit proposed parent-ledger action.