# run-ledger-supplement-template-WORKFLOW-GITHUB-ISSUES-v1

Use this template when later evidence changes the admitted reading of an existing `WORKFLOW-GITHUB-ISSUES` run, target, or stage.

## Minimal Header

```yaml
runbook_run_ledger_supplement:
  supplement_series_id: <ledger-run-SUP-WORKFLOW-GITHUB-ISSUES-001-summary>
  supplement_sequence: <001>
  supplement_id: <ledger-run-SUP-001-WORKFLOW-GITHUB-ISSUES-001-summary>
  supplement_kind: runbook-run-ledger-supplement
  status: <draft|active|completed>
  owner_lane: <S0G-3E>
  parent_run_ledger_id: <ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-summary>
  parent_runbook_id: <run-WORKFLOW-GITHUB-ISSUES-001-summary>
  parent_run_row_id: <RUN-001>
  parent_target_row_id: <RUN-001-T01|multiple>
  parent_target_stage_row_id: <RUN-001-T01-STG-CREATION|multiple>
  parent_target_stage_attempt_id: <RUN-001-T01-STG-CREATION-A01|not-used|multiple>
  source_round_id: <RUN-001-R02>
  target_ref_key: <S4F-2A>
  target_ref_path: <docs/logs/log-S4F-2A-...md>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  supplement_scope: <what later evidence is admitted>
  target_reading_goal: <what later readers should understand>
```

## Evidence Table

| supplement item id | parent run row id | target row id | target stage row id | target stage attempt id | source round id | evidence ref | verification status | effect on current verdict | proposed parent-ledger action | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001-SUP-01>` | `<RUN-001>` | `<RUN-001-T01>` | `<RUN-001-T01-STG-CREATION>` | `<RUN-001-T01-STG-CREATION-A01|not-used>` | `<RUN-001-R02>` | `<artifact path>` | `<verified>` | `<sharpens-existing>` | `<rewrite-current-target-and-append-stage-attempt>` | `<optional>` |

## Family-specific Rules

- For this family, a SUP packet should normally map to one explicit `source_round_id`.
- If the parent ledger already has a current stage attempt, the SUP write-back should append a new attempt row and update the corresponding current target row.
- Use `multiple` only when one bounded supplement truly touches several targets or stages at once.