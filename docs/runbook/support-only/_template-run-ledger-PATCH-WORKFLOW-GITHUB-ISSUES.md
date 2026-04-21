# run-ledger-patch-template-WORKFLOW-GITHUB-ISSUES-v1

Use this template for bounded repairs inside the active `WORKFLOW-GITHUB-ISSUES` release when no release bump is justified.

## Minimal Header

```yaml
runbook_run_patch_ledger:
  patch_ledger_id: <ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-summary>
  patch_kind: runbook-run-ledger-patch
  status: <draft|active|completed>
  owner_lane: <S0G-3E>
  parent_runbook_id: <run-WORKFLOW-GITHUB-ISSUES-001-summary>
  parent_runbook_ref: <docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-summary.md>
  parent_run_ledger_id: <ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-summary>
  parent_run_ledger_ref: <docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-summary.md>
  parent_run_row_id: <RUN-001|pending>
  parent_target_row_id: <RUN-001-T01|pending|not-applicable>
  parent_target_stage_row_id: <RUN-001-T01-STG-CREATION|pending|not-applicable>
  parent_target_stage_attempt_id: <RUN-001-T01-STG-CREATION-A01|not-used|pending>
  patch_sequence: <001>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  patch_scope: <what bounded repair is admitted>
  patch_reason_class: <docs-fix|script-fix|manifest-fix|evidence-fix|mixed-bounded-repair>
  target_reading_goal: <what later readers should understand>
```

## Patch Change Table

| patch item id | parent run row id | target row id | target stage row id | target stage attempt id | target artifact or path | change class | verification status | effect on current runbook release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<RUN-001>` | `<RUN-001-T01|not-applicable>` | `<RUN-001-T01-STG-CREATION|not-applicable>` | `<not-used>` | `<script path>` | `<script-fix>` | `<verified>` | `<no-release-bump>` | `<append-patch-ref|open-sup-ledger>` | `<optional>` | `<optional>` |

## Family-specific Rules

- PATCH remains repair-first. It should not become an execution round by itself unless the parent ledger explicitly admits a changed chronology reading because of that repair.
- If a repair changes the admitted reading of one run, target, or stage, pair the PATCH packet with the corresponding SUP write-back.
- Keep the same stable structural ids already used by the parent ledger.