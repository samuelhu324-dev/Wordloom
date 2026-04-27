# run-ledger-template-WORKFLOW-GITHUB-ISSUES-v1

Use this template for the canonical parent ledger of the `WORKFLOW-GITHUB-ISSUES` family.
Its job is to separate current state from chronology and replay history.

## Minimal Header

```yaml
runbook_run_ledger:
  run_ledger_id: <ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-summary>
  ledger_kind: runbook-run-ledger
  status: <draft|active|completed>
  owner_lane: <S0G-3E>
  runbook_family: <WORKFLOW-GITHUB-ISSUES>
  runbook_release: <001>
  runbook_id: <run-WORKFLOW-GITHUB-ISSUES-001-summary>
  runbook_ref: <docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-summary.md>
  run_sequence: <001>
  workflow_profiles:
    - <child-issue-full-lifecycle>
    - <parent-issue-light-lifecycle>
  strong_structure_status: chronology-target-stage-attempt-active
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  target_reading_goal: <what later readers should understand>
```

## Lifecycle Field Rule

- `created_at`, `reviewed_at`, and `accepted_at` are required header fields; keep them present even when the defended value is still `unknown` or `pending`.
- Round and attempt time columns in this template are required when their tables are present; unknown values are acceptable, omission is not.

## Current Run Status Summary

| run row id | operational convergence | accounting status | approval status | target convergence count | target partial count | target blocked count | latest chronology round | latest updated from packet | reader verdict | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001>` | `<converged|partial|blocked>` | `<converged|backfill-in-progress|partial>` | `<pending|accepted|rejected>` | `<4/4>` | `<0>` | `<0>` | `<RUN-001-R03>` | `<SUP-002>` | `<one-line reader answer>` | `<optional>` |

## Execution Round Table

| execution round id | run row id | round sequence | entry packet id | entry packet kind | target scope | stage scope attempted | round started at | round completed at | round verdict | delta entry ref | crosswalk ref | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001-R01>` | `<RUN-001>` | `<01>` | `<RUN-001>` | `<ledger>` | `<T01-T04 + parent>` | `<CREATION, PR_PENDING, PR_MERGED, CONCLUSION>` | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | `<completed_with_follow_up>` | `<not-applicable>` | `<not-applicable>` | `<optional>` |

## Current Target Status Table

| target row id | run row id | target ref key | target kind | workflow profile | first_seen_in_round | first_seen_from_packet | current_status | current_stage_completion | latest_updated_in_round | latest_updated_from_packet | latest delta ref | latest delta focus | latest_updated_at | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001-T01>` | `<RUN-001>` | `<S4F-2A>` | `<child-issue-log>` | `<child-issue-full-lifecycle>` | `<RUN-001-R01>` | `<RUN-001>` | `<converged>` | `<CREATION, PR_PENDING, PR_MERGED, CONCLUSION>` | `<RUN-001-R03>` | `<SUP-002>` | `<SUP-002 / RUN-001-SUP-05>` | `<conclusion dual-PR DoD convergence>` | `<YYYY-MM-DD>` | `<optional>` |

## Target Stage Attempt Table

| attempt id | target row id | stage row id | stage name | round id | source packet id | source packet kind | attempt ordinal | started at | completed at | status | blocking reason | supersedes attempt id | current? | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<RUN-001-T01-STG-CONCLUSION-A02>` | `<RUN-001-T01>` | `<RUN-001-T01-STG-CONCLUSION>` | `<CONCLUSION>` | `<RUN-001-R03>` | `<SUP-002>` | `<SUP>` | `<02>` | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | `<completed>` | `<none>` | `<RUN-001-T01-STG-CONCLUSION-A01>` | `<yes>` | `<optional>` |

## Evidence and Review Tables

- Keep evidence extraction, actor/provenance review, and optional time audit after the four primary surfaces above.
- Evidence/support tables must not be the only carrier of chronology.

## Required Rules

- Keep one stable row per run, target, and stage slot.
- Record chronology in `Execution Round Table` and `Target Stage Attempt Table` only.
- Every history row must expose `source_packet_id`, `source_packet_kind`, `source_packet_sequence`, or an equivalent explicit source on the row.