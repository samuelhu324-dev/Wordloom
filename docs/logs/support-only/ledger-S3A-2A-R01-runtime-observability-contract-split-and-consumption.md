# ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption

```yaml
support_only_contract_release_row_flow_ledger:
  row_flow_ledger_id: ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption
  ledger_kind: support-only-contract-release-row-flow-ledger
  status: draft
  owner_lane: S4G-1B
  created_at: 2026-04-26
  reviewed_at: 2026-04-26
  accepted_at: pending
  writeback_started_at: 2026-04-26
  writeback_completed_at: 2026-04-26
  parent_ledger_id: ledger-S3A-2A-combo-observability-triage
  parent_source_id: S3A-2A
  parent_row_scope: S3A-2A-R01
  parent_row_ref: docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md
  source_scope: split and absorption accounting for the S3A-2A-R01 runtime observability row before and during the opening of DOC-RUNTIME-OBSERVABILITY-0001
  target_reading_goal: show exactly how parent row S3A-2A-R01 was decomposed into current contract-facing derived rows, which adjacent parent rows sharpened those derived rows, and what remains deferred outside the current contract release
```

## Decision Frame

- This attached ledger exists because `S3A-2A-R01` could no longer remain one undivided parent row once the lane needed to make entrypoint, proof-path, and runbook-boundary decisions reviewable.
- The current draft default is:
  - keep `ledger-S3A-2A-combo-observability-triage` as the owner of the original parent row identity;
  - move derived-row accounting for that row into this attached ledger;
  - keep `S4G-1B` as the decision and evolution log only;
  - resolve `D01` through `D05` into `DOC-RUNTIME-OBSERVABILITY-0001`;
  - leave `D06` deferred for a later runtime-owned runbook packet.
- The purpose of this ledger is to stop the current contract from reading like one control-log prose export and to make the split or absorption chain reviewable at the ledger layer.

## Current Governance State

| governed surface | owner team | current steward | approval state | reviewed by | approved by | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption` | `docs-governance` | `role:workflow-ledger-maintainer` | `attached-row-review-pending-final-acceptance` | `role:workflow-reviewer` | `role:docs-governance-approver` | This attached ledger is the current accounting surface for how `S3A-2A-R01` splits into contract-facing and runbook-facing derived rows. |
| `ledger-S3A-2A-combo-observability-triage` | `docs-governance` | `role:workflow-ledger-maintainer` | `parent-review-pending-final-acceptance` | `role:workflow-reviewer` | `role:docs-governance-approver` | The parent ledger remains the owner of the original mixed-packet routing state and the original `S3A-2A-R01` identity. |
| `S4G-1B` | `S4 runtime governance` | `role:s4-history-packet-maintainer` | `packet-review-in-progress` | `role:workflow-reviewer` | `role:docs-governance-approver` | `S4G-1B` now records preliminary extraction and decision lineage, but no longer acts as the durable owner of row split accounting. |
| `DOC-RUNTIME-OBSERVABILITY-0001` | `docs-governance` | `delegated:runtime-observability-contract-maintainer` | `reviewed-awaiting-approval` | `role:workflow-reviewer` | `role:docs-governance-approver` | The current runtime observability contract now consumes derived rows from this attached ledger rather than reading as one direct control-log mutation. |

## Derived Row And Consumption Table

| derived row id | parent row ids | derivation kind | meaning owned here | downstream owner | target release action | derivation status | applied-to surface | resolution status | resolved by surface | resolved by contract id | consumed scope | parent write-back state | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-2A-R01-D01` | `S3A-2A-R01` | `semantic-claim` | one admitted runtime handling chain should remain diagnosable through metrics, tracing, and structured logs via shared pivots and auditable evidence | `contract` | `new-family` | `split-from-parent` | `search outbox projection worker diagnostics` | `applied` | `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` | `DOC-RUNTIME-OBSERVABILITY-0001` | `full` | `written-back` | This is the minimum semantic row split out of the parent packet root before any narrower code attachment is stated. |
| `S3A-2A-R01-D02` | `S3A-2A-R01` | `boundary-bridge` | the current bounded owner surface is the search outbox projection worker for `projection=search_index_to_elastic` | `contract` | `new-family` | `split-from-parent` | `backend/scripts/search_outbox_worker.py` worker surface | `applied` | `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` | `DOC-RUNTIME-OBSERVABILITY-0001` | `full` | `written-back` | This row carries the applied-to boundary that the parent row could not defend by itself. |
| `S3A-2A-R01-D03` | `S3A-2A-R01` | `entrypoint-bridge` | the current stable entrypoint is `backend/scripts/search_outbox_worker.py`, with stable drill-facing entry id `search_outbox_worker@v1` and bounded switches `SEARCH_OUTBOX_WORKER_ENABLED` plus `SEARCH_OUTBOX_RUNNER` | `contract` | `new-family` | `split-from-parent` | `backend/scripts/search_outbox_worker.py` | `applied` | `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` | `DOC-RUNTIME-OBSERVABILITY-0001` | `full` | `written-back` | Adjacent code and historical drill evidence sharpen this row, but the parent row identity still remains `S3A-2A-R01`. |
| `S3A-2A-R01-D04` | `S3A-2A-R01; S3A-2A-R02` | `boundary-bridge` | the minimum shared pivots and required signals are `trace_id/traceparent`, `claim_batch_id`, `outbox event id`, worker labels such as `projection` and `op`, `outbox_*` metrics, worker tracing spans, and worker structured logs | `contract` | `new-family` | `split-from-parent-plus-absorbs-adjacent` | `search outbox projection worker telemetry surface` | `applied` | `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` | `DOC-RUNTIME-OBSERVABILITY-0001` | `full` | `written-back` | `S3A-2A-R02` sharpens the shared-pivot portion of the same chain rather than opening one independent current reader here. |
| `S3A-2A-R01-D05` | `S3A-2A-R01; S3A-2A-R03; S3A-2A-R04; S3A-2A-R08; S3A-2A-R10` | `proof-binding` | the first defended proof path is `es_write_block_4xx`, with deterministic drill start, verify, and evidence-bundle expectations on the same worker surface | `contract` | `new-family` | `split-from-parent-plus-absorbs-adjacent` | `backend/scripts/cli.py labs run|verify es_write_block_4xx` | `applied` | `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` | `DOC-RUNTIME-OBSERVABILITY-0001` | `full` | `written-back` | Adjacent drill rows sharpen proof semantics, but the contract-facing current reader remains one derived child of `R01` rather than one free-standing labs packet here. |
| `S3A-2A-R01-D06` | `S3A-2A-R01; S3A-2A-R13` | `runbook-boundary` | fallback, switch, shadow or dual-run, and coexistence-window procedures belong in a later runtime-owned runbook packet rather than in the current contract release | `runbook` | `new-release` | `split-from-parent-plus-absorbs-adjacent` | `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` | `deferred` | `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` | `none` | `none` | `written-back` | `S3A-2A-R13` sharpens the operator surface, but this round does not yet open the narrower runtime-owned runbook packet. |

## Parent Write-Back Table

| parent row id | attached-ledger effect | derived row ids | parent-ledger action | downstream impact | write-back status | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `S3A-2A-R01` | `split-plus-adjacent-absorption` | `S3A-2A-R01-D01; S3A-2A-R01-D02; S3A-2A-R01-D03; S3A-2A-R01-D04; S3A-2A-R01-D05; S3A-2A-R01-D06` | `rewrite-parent-row` | `contract-opened plus runbook-deferred` | `applied` | The parent ledger should now say that `R01` remains the packet root, but its current contract-facing and runbook-facing meanings are accounted for through this attached ledger rather than through the control log directly. |

## Row Id Map

- `S3A-2A-R01-D01`: diagnosable chain semantic claim
- `S3A-2A-R01-D02`: bounded owner surface
- `S3A-2A-R01-D03`: stable entrypoint and switches
- `S3A-2A-R01-D04`: shared pivots and required signals
- `S3A-2A-R01-D05`: defended proof path
- `S3A-2A-R01-D06`: runbook boundary and deferred operator packet

## Adjacent Absorbed Rows

- `S3A-2A-R02` sharpens shared pivots and required signals for `D04`.
- `S3A-2A-R03`, `S3A-2A-R04`, `S3A-2A-R08`, and `S3A-2A-R10` sharpen proof semantics for `D05`.
- `S3A-2A-R13` sharpens the deferred operator boundary for `D06`.

## Row Chronology Audit

| derived row id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-2A-R01-D01` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `parent issue #37 remains the only defended source root` | The semantic claim remains as weakly timed as the parent row itself. |
| `S3A-2A-R01-D02` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `the code boundary is current-state defended first, not issue-time defended first` | The contract can defend the current boundary even though the original parent-row chronology is still weak. |
| `S3A-2A-R01-D03` | `unknown` | `2026-02-13` | `2026-02-13` | `ongoing` | `day` | `stable entrypoint evidence is sharpened by later surviving local code and docs` | This derived row relies on current code and defended day-level historical references rather than on issue-only chronology. |
| `S3A-2A-R01-D04` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `shared-pivot support remains issue-first` | The shared-pivot row is content-defended first and chronology-defended later. |
| `S3A-2A-R01-D05` | `unknown` | `2026-02-14` | `2026-02-14` | `ongoing` | `day` | `proof-path evidence is sharpened by surviving drill logs and labs material` | The current proof row now has day-level chronology through the surviving drill surfaces even though the parent row itself is issue-first. |
| `S3A-2A-R01-D06` | `unknown` | `2026-02-15` | `2026-02-15` | `ongoing` | `day` | `runbook boundary is sharpened by the retained operator runbook surface` | The operator-facing row has a stronger day-level chronology than the semantic parent row. |

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-2A-R01-GOV-01` | `contribution-event` | `S3A-2A-R01 parent row` | `unknown` | `none-current-state` | `2026-04-25` | `GitHub issue #37 as routed by ledger-S3A-2A-combo-observability-triage` | The parent row remains the original source identity even after decomposition. |
| `S3A-2A-R01-GOV-02` | `derived-row-accounting-opened` | `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption` | `role:packet-reviewer` | `derived-row-split-fixed` | `2026-04-26` | `S4G-1B/P3-C2-S1S2` | Derived-row accounting now lives in this attached ledger rather than only in the control log. |
| `S3A-2A-R01-GOV-03` | `parent-writeback-event` | `ledger-S3A-2A-combo-observability-triage` | `role:packet-reviewer` | `parent-row-r01-now-points-to-attached-ledger` | `2026-04-26` | `S3A-2A-R01-D01 through S3A-2A-R01-D06` | The parent row is now explicitly rewritten as partially consumed through the attached ledger. |
| `S3A-2A-R01-GOV-04` | `contract-source-rewrite-event` | `DOC-RUNTIME-OBSERVABILITY-0001` | `role:packet-reviewer` | `contract-now-reads-from-attached-ledger` | `2026-04-26` | `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption; DOC-RUNTIME-OBSERVABILITY-0001` | The contract source basis is now ledger-first rather than control-log-first. |

## Current Reader Handoff

- `S3A-2A-R01-D01` through `S3A-2A-R01-D05` now read through `DOC-RUNTIME-OBSERVABILITY-0001`.
- `S3A-2A-R01-D06` remains deferred and currently reads only as one later runbook-facing boundary note.
- `S4G-1B` remains the evolution and decision log for how this split was chosen, but not the durable owner of the split itself.

## Reader Notes

- Read the parent ledger first when the question is `what was the original packet-owned row?`
- Read this attached ledger next when the question is `how did that parent row split, what adjacent rows sharpened it, and which derived rows were actually consumed?`
- Read `DOC-RUNTIME-OBSERVABILITY-0001` only after this ledger when the question is `what current contract now owns the consumed derived rows?`