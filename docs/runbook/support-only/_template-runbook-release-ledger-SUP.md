# runbook-release-ledger-supplement-template-v1

Use this supplement when later evidence needs to sharpen, narrow, revise, or reopen one verdict already admitted in a runbook release ledger.
This SUP surface is release-scoped; it does not replace source logs and it does not replace run-level `ledger-run-SUP-*` packets.

## Naming Rule

- Name runbook release SUP ledgers as `ledger-runbook-SUP-<sequence>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- Preferred example shape:
  - `ledger-runbook-SUP-001-RUNTIME-OBSERVABILITY-001-scenario-family-intake.md`

## Minimal Header

```yaml
runbook_release_ledger_supplement:
  supplement_series_id: <ledger-runbook-SUP-RUNBOOK-FAMILY-001>
  supplement_sequence: <001>
  supplement_id: <ledger-runbook-SUP-001-RUNBOOK-FAMILY-001-summary>
  supplement_kind: runbook-release-ledger-supplement
  status: <draft|active|completed>
  owner_lane: <S4G-1G>
  parent_release_ledger_id: <ledger-runbook-RUNBOOK-FAMILY-001-summary>
  parent_runbook_id: <run-RUNBOOK-FAMILY-001-summary>
  parent_row_id: <RBL-01>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  affected_bridge_ids:
    - <RB-01|none>
  affected_coverage_ids:
    - <SC-01|none>
  supplement_scope: <what later evidence this supplement is admitting>
  target_reading_goal: <what later readers should understand after this supplement is applied>
```

## Evidence Table

| supplement item id | parent row id | evidence ref | evidence type | verification status | effect on current verdict | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RBL-01-SUP-01>` | `<RBL-01>` | `<log/code/labs/runbook anchor>` | `<md|code|labs|artifact|mixed>` | `<pending|verified|rejected>` | `<supports-existing|sharpens-existing|narrows-existing|revises-existing|conflicts-needs-review>` | `<no-change|append-evidence|rewrite-parent-row|reopen-ledger-verdict>` | `<none|rewrite-runbook|rewrite-contract-bridge|defer>` | `<why this evidence matters>` |

## Required Rules

- Every SUP row must point to one existing `parent row id` in the parent runbook release ledger.
- Use this surface when the follow-up changes release-scoped meaning or admission standing, not when it only sharpens one admitted run.
- Write into the runbook body only after the parent runbook release ledger is updated or explicitly left unchanged.