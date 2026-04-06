# governance-contract-backfill: GC-PRB-0001

- `record_id`: `GC-PRB-0001`
- `contract_id`: `PR-BODY-HISTORICAL-DRIFT-FAIL-ON-FINDINGS`

## Target Contract

- `contract_id`: `PR-BODY-HISTORICAL-DRIFT-FAIL-ON-FINDINGS`

## Current Need

- `S0F-P1` exposed that the current workflow-dispatch replay is failing because historical merged PR `#383` still classifies as `substantive-drift`, so the repo now needs one explicit active contract record that states this is the current fail-on-findings behavior rather than an accidental workflow break.

## Backtrace Result

- `introduced_by`: `S0F-1I/P4-C1-S1`
- `last_changed_by`: `S0F-1J/P2-C1-S1`
- `source_refs`:
  - `docs/logs/log-S0F-1I-formatting-only-pr-body-convergence.md`
  - `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
  - `docs/logs/patch/log-S0F-P1-s0f-pr-body-completeness-standard-check-dispatch-failure-triage.md`

## Historical Gaps

- `S0F-1H` is the earlier reviewer-origin surface for substantive-drift classification, but this backfill treats `S0F-1I/P4-C1-S1` as the first sufficient source anchor for the current standard-check fail semantics because that phase fixed the wrapper-level pass/non-pass rule used later by `S0F-1J`.

## Decision

- This backfill is already sufficient for current-state use because the active question is not who first invented PR-body review in general, but which retained governance contract currently makes the standard check fail on substantive historical merged-PR drift.
- Reviewed again in `S0F-3E/P6-C2`: this file remains support-only contract backtrace, not a second current contract surface.
- After `S0F-3E/P6-C3`, this file now supports the deprecated legacy umbrella `GC-PRB-0001` and its successor current records rather than acting as a front-door current contract surface.

## Follow-up

- If the repo later splits live enforcement from historical audit reporting, this contract record should either be modified materially or superseded by separate live-gate and historical-audit records.