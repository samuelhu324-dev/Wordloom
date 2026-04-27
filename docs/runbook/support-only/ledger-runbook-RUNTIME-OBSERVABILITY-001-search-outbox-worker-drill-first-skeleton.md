# ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton

```yaml
runbook_release_ledger:
  ledger_id: ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton
  ledger_kind: runbook-release-ledger
  status: active
  owner_lane: S4G-1G
  runbook_family: RUNTIME-OBSERVABILITY
  runbook_release: 001
  runbook_id: run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton
  runbook_ref: docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md
  created_at: 2026-04-27
  reviewed_at: pending
  accepted_at: pending
  source_of_authority:
    - docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md
    - docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md
    - docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md
  target_reading_goal: Make runbook-release-scoped evidence admission and staged scenario or boundary write-back reviewable without overloading the source log or the per-run ledgers.
```

## Decision Frame

- This ledger is the reader-object-first intake surface for `run-RUNTIME-OBSERVABILITY-001`.
- It does not replace `S4G-1F` or `S4G-1G`; those logs still own mixed-source extraction and control-lane history.
- It does not replace future `ledger-run-*` execution accounting; those remain run-scoped.

## Intake and Write-Back Table

| row id | evidence anchor | evidence class | semantic area | intended landing surface | current verdict | affected bridge ids | affected coverage ids | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RBL-01` | `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md#P6-C1-S1` | `source-log` | `bounded current skeleton opening` | `runbook-body` | `applied-current-release` | `RB-OBS-01; RB-OBS-02; RB-OBS-03; RB-OBS-04` | `SC-OBS-01; SC-OBS-02; SC-OBS-03; SC-OBS-04` | `This row records the current defended runbook release basis that has already landed in the runbook body.` |
| `RBL-02` | `docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md#P1; #P2` | `mixed` | `scenario inventory wider than current family` | `scenario-registry; notes-and-boundaries; defer` | `classified-awaiting-write-back` | `none` | `none` | `P2 now classifies worker-chain scenarios as current-family, supporting corroboration scenarios as support-only, and search verification or dual-run scenarios as sibling-family; concrete write-back still waits for P3.` |
| `RBL-03` | `docs/runbook/support-only/ledger-run-001-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md` | `runbook` | `run-level accounting boundary` | `defer` | `deferred` | `none` | `none` | `Per-run accounting remains reserved for future admitted runs; this ledger does not collapse object and run scopes.` |

## Scenario Family Classification Table

| scenario name | classified standing | smallest defensible reason | runbook release standing | intended next landing |
| --- | --- | --- | --- | --- |
| `es_429_inject` | `current-family` | `same search outbox worker diagnostic chain` | `not yet written into the runbook body` | `possible later scenario-registry widening in P3` |
| `es_write_block_4xx` | `current-family` | `already admitted proof path on the current worker chain` | `already present in the runbook` | `no new write-back required` |
| `es_down_connect` | `current-family` | `same search outbox worker diagnostic chain` | `not yet written into the runbook body` | `possible later scenario-registry widening in P3` |
| `es_timeout` | `current-family` | `same search outbox worker diagnostic chain` | `not yet written into the runbook body` | `possible later scenario-registry widening in P3` |
| `es_bulk_partial` | `current-family` | `same search outbox worker diagnostic chain` | `not yet written into the runbook body` | `possible later scenario-registry widening in P3` |
| `db_claim_contention` | `current-family` | `same search outbox worker claim/recovery chain` | `not yet written into the runbook body` | `possible later scenario-registry widening in P3` |
| `stuck_reclaim` | `current-family` | `same search outbox worker claim/recovery chain` | `not yet written into the runbook body` | `possible later scenario-registry widening in P3` |
| `duplicate_delivery` | `current-family` | `same search outbox worker idempotency chain` | `not yet written into the runbook body` | `possible later scenario-registry widening in P3` |
| `projection_version` | `current-family` | `same search outbox worker rule-version chain` | `not yet written into the runbook body` | `possible later scenario-registry widening in P3` |
| `collector_down` | `support-only` | `supporting observability infra rather than the owned worker chain itself` | `retain outside the runbook body` | `stay in object ledger and source log` |
| `shadow_verify_shared_keys` | `support-only` | `cross-surface corroboration aid rather than primary runbook-owned scenario` | `retain outside the runbook body` | `stay in object ledger and source log` |
| `shadow_verify_search_index_write_gate` | `sibling-family` | `search gate semantics rather than current runtime observability ownership` | `do not land in this runbook release` | `route to sibling lane in P3` |
| `shadow_verify_search_index_paging_stability` | `sibling-family` | `search verification semantics rather than current runtime observability ownership` | `do not land in this runbook release` | `route to sibling lane in P3` |
| `rehearsal_search_read_switch_smoke` | `sibling-family` | `read-switch rehearsal semantics rather than current runtime observability ownership` | `do not land in this runbook release` | `route to sibling lane in P3` |
| `shadow_verify_dual_run_readiness_gate` | `sibling-family` | `dual-run readiness semantics explicitly outside current narrow ownership` | `do not land in this runbook release` | `route to sibling lane in P3` |
| `shadow_verify_dual_run_stage1` | `sibling-family` | `dual-run stage semantics explicitly outside current narrow ownership` | `do not land in this runbook release` | `route to sibling lane in P3` |
| `shadow_verify_dual_run_stage2` | `sibling-family` | `dual-run stage semantics explicitly outside current narrow ownership` | `do not land in this runbook release` | `route to sibling lane in P3` |
| `shadow_verify_dual_run_window` | `sibling-family` | `coexistence-window semantics explicitly outside current narrow ownership` | `do not land in this runbook release` | `route to sibling lane in P3` |
| `shadow_verify_canary_dual_write` | `sibling-family` | `dual-write cutover semantics rather than current runtime observability ownership` | `do not land in this runbook release` | `route to sibling lane in P3` |
| `shadow_verify_dual_write_sampling` | `sibling-family` | `dual-write evidence semantics rather than current runtime observability ownership` | `do not land in this runbook release` | `route to sibling lane in P3` |

## Actor and Provenance Review Table

| row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RBL-01` | `role:s4g-packet-maintainer` | `role:runbook-maintainer` | `pending` | `pending` | `direct-markdown-inspection` | `pending` | `pending` | `Current bounded runbook release already landed through S4G-1F.` | `The release body exists, but this ledger is newly opened as its object-level intake surface.` |
| `RBL-02` | `role:s4g-packet-maintainer` | `role:runbook-maintainer` | `pending` | `pending` | `source-path-check` | `pending` | `pending` | `The extracted scenarios are strong enough to admit into the object ledger, but not yet to widen the runbook.` | `This row intentionally holds code/labs extraction pending family classification.` |
| `RBL-03` | `role:s4g-packet-maintainer` | `role:runbook-maintainer` | `pending` | `pending` | `direct-markdown-inspection` | `pending` | `pending` | `Run-level accounting boundary remains explicit.` | `This row is a boundary note, not a semantic widening claim.` |