# DOC-RUNTIME-OBSERVABILITY-0001 metrics tracing and structured logs diagnostic chain

```yaml
contract_record:
  contract_family: DOC-RUNTIME-OBSERVABILITY
  contract_release: 0001
  contract_id: DOC-RUNTIME-OBSERVABILITY-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first runtime observability contract by fixing one current diagnostically complete worker chain, its stable entrypoint, its minimum shared-pivot signal set, and its first defended proof path under S4G-1B.
  summary: One admitted runtime handling chain should remain diagnosable through metrics, tracing, and structured logs via shared pivots and auditable evidence, with the current bounded owner surface fixed to the search outbox projection worker and the current defended proof path fixed to es_write_block_4xx.
  governance_area: runtime observability for bounded worker handling chains
  applies_to: the search outbox projection worker surface, its stable entrypoint, its minimum shared-pivot signal set, and its first defended drill-backed diagnostic proof path
  entrypoint_ref: backend/scripts/search_outbox_worker.py
  parent_ledger_ref: docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md
  attached_row_flow_ledger_ref: docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md
  enforcement_surface: script
  violation_semantics: warning
  recorded_at: 2026-04-26
  reviewed_at: pending
  effective_from: 2026-04-26
  effective_until: ongoing
  introduced_by: docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md
  last_changed_by: docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md
  source_refs:
    - docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md
  cumulative_source_refs:
    - docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md
    - docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md
    - docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md
    - docs/logs/log-S3A-2A-2B-daemon-ready-worker-migration.md
    - docs/logs/log-S3A-2A-3B-automated-failure-drills.md
    - docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md
    - docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md
    - docs/logs/log-S6A-1A-stable-entry-contract.md
  supporting_evidence_refs:
    - backend/scripts/search_outbox_worker.py
    - backend/scripts/search_outbox_worker_impl.py
    - backend/infra/observability/outbox_metrics.py
    - backend/infra/observability/tracing.py
    - backend/scripts/cli_app/scenarios/es_write_block_4xx.py
    - docs/labs/lab-S3A-2A-3A-observability-failure-drills.md
  lineage:
    supersedes: []
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This first release is intentionally narrow and should be read as one runtime-owned observability contract for a single defended worker chain rather than as a repo-wide observability umbrella.
    - The contract is opened only after S4G-1B fixed the weak semantic claim, the search outbox worker boundary, and the first defended proof path through es_write_block_4xx.
    - Fallback, switch, shadow or dual-run, and coexistence-window operator instructions remain downstream runbook material and are not owned by this release yet.
```

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-RUNTIME-OBSERVABILITY-0001-ST-01` | `Diagnosable chain requirement` | `active` | `introduced` | `S3A-2A-R01-D01` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `2026-04-26` | `ongoing` | `in-force` | One admitted runtime handling chain should remain diagnosable through metrics, tracing, and structured logs via shared pivots and auditable evidence. | This is the narrow semantic core of the family. |
| `DOC-RUNTIME-OBSERVABILITY-0001-ST-02` | `Bounded owner surface` | `active` | `introduced` | `S3A-2A-R01-D02; S3A-2A-R01-D03` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `2026-04-26` | `ongoing` | `in-force` | The current bounded owner surface for this family is the search outbox projection worker for `projection=search_index_to_elastic`, with stable entrypoint `backend/scripts/search_outbox_worker.py`. | This clause prevents the family from floating above code with no bounded owner. |
| `DOC-RUNTIME-OBSERVABILITY-0001-ST-03` | `Minimum shared pivots and signals` | `active` | `introduced` | `S3A-2A-R01-D04` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `2026-04-26` | `ongoing` | `in-force` | The current minimum shared pivots are `trace_id/traceparent`, `claim_batch_id`, `outbox event id`, and worker labels such as `projection` and `op`; the current minimum signals are `outbox_*` metrics, worker tracing spans, and worker structured logs. | Later releases may refine this field set, but should not weaken it silently. |
| `DOC-RUNTIME-OBSERVABILITY-0001-ST-04` | `Defended proof path` | `active` | `introduced` | `S3A-2A-R01-D05` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `2026-04-26` | `ongoing` | `in-force` | The first defended proof path for this family is `es_write_block_4xx`, which must start `search_outbox_worker@v1`, verify expected before/after projection metrics and DB reason family movement, and retain worker-start, metrics, result, and worker-log evidence in one run-scoped bundle. | Tracing export completeness can still be hardened later without blocking this first release. |
| `DOC-RUNTIME-OBSERVABILITY-0001-ST-05` | `Runbook boundary` | `active` | `introduced` | `S3A-2A-R01-D06` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `2026-04-26` | `ongoing` | `in-force` | This release does not own fallback, switch, shadow or dual-run, or coexistence-window operator steps; those remain downstream runbook concerns once a narrower runbook bridge packet is justified. | Keeps semantic contract and operator procedure distinct. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-RUNTIME-OBSERVABILITY-0001-CH-01` | `DOC-RUNTIME-OBSERVABILITY-0001` | `introduced` | `none` | `DOC-RUNTIME-OBSERVABILITY-0001-ST-01; DOC-RUNTIME-OBSERVABILITY-0001-ST-02; DOC-RUNTIME-OBSERVABILITY-0001-ST-03; DOC-RUNTIME-OBSERVABILITY-0001-ST-04; DOC-RUNTIME-OBSERVABILITY-0001-ST-05` | `2026-04-26` | `2026-04-26` | The family is now explicit because the attached row-flow ledger already fixed one weak semantic claim, one bounded worker surface, one stable entrypoint, and one defended proof path strongly enough to support a current draft reader. | `S3A-2A-R01-D01; S3A-2A-R01-D02; S3A-2A-R01-D03; S3A-2A-R01-D04; S3A-2A-R01-D05; S3A-2A-R01-D06` | The release is deliberately narrow and should not be read as a repo-wide observability umbrella. |

## Code Bridge Table

| bridge id | owned statement ids | applied to surface | runtime boundary | entrypoint ref | drill-facing entry id | switch surface | reason for attachment | recorded at | effective from | effective until | replacement rule | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-RUNTIME-OBSERVABILITY-0001-CB-01` | `DOC-RUNTIME-OBSERVABILITY-0001-ST-02; DOC-RUNTIME-OBSERVABILITY-0001-ST-03; DOC-RUNTIME-OBSERVABILITY-0001-ST-04` | `search outbox projection worker diagnostics` | `search outbox projection worker for projection=search_index_to_elastic` | `backend/scripts/search_outbox_worker.py` | `search_outbox_worker@v1` | `SEARCH_OUTBOX_WORKER_ENABLED; SEARCH_OUTBOX_RUNNER` | `Current contract meaning is intentionally attached to one defended worker chain, one stable entrypoint, one minimum shared-signal set, and one defended proof path rather than to repo-wide observability in the abstract.` | `2026-04-26` | `2026-04-26` | `ongoing` | `Keep this row current until a later release changes the bounded owner surface, stable entrypoint, switch-surface naming, or defended proof path strongly enough that one replacement row or evolution table is required.` | `backend/scripts/search_outbox_worker.py; backend/scripts/search_outbox_worker_impl.py; backend/scripts/cli_app/scenarios/_failure_drill_shared.py; backend/scripts/cli_app/scenarios/es_write_block_4xx.py` | `This row records current code attachment only; it does not promote runbook-boundary semantics into positive contract meaning.` |

## Contract Coverage Table

| semantic area | current basis | coverage class | current standing | current owner / later owner | notes |
| --- | --- | --- | --- | --- | --- |
| `bounded owner surface` | `S3A-2A-R01-D02`; `DOC-RUNTIME-OBSERVABILITY-0001-ST-02` | `defended-now` | `Current release already fixes the worker surface and projection boundary.` | `DOC-RUNTIME-OBSERVABILITY-0001` contract | `Positive contract meaning.` |
| `stable entrypoint` | `S3A-2A-R01-D03`; `contract_record.entrypoint_ref` | `defended-now` | `Current release and current code agree on the stable entrypoint path.` | `DOC-RUNTIME-OBSERVABILITY-0001` contract | `Direct code-bridge field.` |
| `drill-facing entry id` | `S3A-2A-R01-D03`; `_failure_drill_shared.py` | `defended-now` | `Current defended drill surfaces already use one stable bridge identifier for the same worker chain.` | `DOC-RUNTIME-OBSERVABILITY-0001` contract | `Bridge-profile support field.` |
| `switch surface names` | `S3A-2A-R01-D03`; `backend/scripts/search_outbox_worker.py` | `defended-now` | `The current bounded switch names are already defendable as part of the code attachment profile.` | `DOC-RUNTIME-OBSERVABILITY-0001` contract | `Names only; not operator procedure.` |
| `minimum shared pivots and signals` | `S3A-2A-R01-D04`; `DOC-RUNTIME-OBSERVABILITY-0001-ST-03` | `defended-now` | `Current release already owns this minimum diagnostic signal set.` | `DOC-RUNTIME-OBSERVABILITY-0001` contract | `Positive contract meaning.` |
| `defended proof path` | `S3A-2A-R01-D05`; `DOC-RUNTIME-OBSERVABILITY-0001-ST-04` | `defended-now` | `Current release already binds the first proof path and its evidence bundle expectations.` | `DOC-RUNTIME-OBSERVABILITY-0001` contract | `Positive contract meaning.` |
| `fallback mode semantics` | `DOC-RUNTIME-OBSERVABILITY-0001-ST-05`; `backend/scripts/search_outbox_worker.py` | `code-anchor-only` | `A disable switch exists, but current release does not defend when disable or degraded mode is permitted or how that state is governed.` | `S4G-1D` retained gap; possible later runbook or code contract | `Do not promote this into current positive clauses.` |
| `switch procedure and reversal proof` | `DOC-RUNTIME-OBSERVABILITY-0001-ST-05`; `backend/scripts/search_outbox_worker.py` | `code-anchor-only` | `Code exposes the knobs, but current release does not defend who may change them, by what preconditions, or how reversal is proven.` | `S4G-1D` retained gap; possible later runbook | `Keep code anchor visible without inventing procedure.` |
| `coexistence window / shadow-dual-run / staged cutover` | `DOC-RUNTIME-OBSERVABILITY-0001-ST-05`; `docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md` | `not-owned-here` | `Neither current release meaning nor current code attachment yields a defendable contract clause for this area.` | `S4G-1D` retained gap; possible later runbook verdict | `Outside current contract ownership.` |

## Release Change

- This release opens the first runtime observability contract from `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption`.
- The release fixes one current reader that was previously held only in the source log scaffold:
  - the minimum diagnostic chain requirement
  - the bounded owner surface and stable entrypoint
  - the minimum shared pivots and signals
  - the first defended proof path
- This release now also exposes one explicit current-state `Code Bridge Table` row and one `Contract Coverage` table so readers can distinguish defended contract meaning from code-anchor-only or out-of-scope semantics.
- This release intentionally does not open a separate runbook bridge packet yet.

## Contract Statement

- `DOC-RUNTIME-OBSERVABILITY-0001-ST-01`: One admitted runtime handling chain should remain diagnosable through metrics, tracing, and structured logs via shared pivots and auditable evidence.
- `DOC-RUNTIME-OBSERVABILITY-0001-ST-02`: The current bounded owner surface for this family is the `search_index_to_elastic` projection worker with stable entrypoint `backend/scripts/search_outbox_worker.py`.
- `DOC-RUNTIME-OBSERVABILITY-0001-ST-03`: The minimum shared pivots and signals for this family are `trace_id/traceparent`, `claim_batch_id`, `outbox event id`, `projection/op`, `outbox_*` metrics, worker tracing spans, and worker structured logs.
- `DOC-RUNTIME-OBSERVABILITY-0001-ST-04`: The first defended proof path is `es_write_block_4xx`, with run-scoped evidence that retains worker-start, metrics, result, and worker-log artifacts on the same worker surface.
- `DOC-RUNTIME-OBSERVABILITY-0001-ST-05`: Fallback, switch, shadow or dual-run, and coexistence-window procedures remain downstream runbook concerns rather than current contract clauses.

## Current Reading

- Read this release when the question is `what is the current runtime observability rule for the first defended worker chain under S4G?`
- Read `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md` when the question is `which parent row splits and absorbed rows does this contract actually consume?`
- Read [docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md](d:/Project/wordloom-v3/docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md) when the question is `how was this contract staged, bounded, and proven before release?`
- Read [docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md](d:/Project/wordloom-v3/docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md) when the question is `what operator steps currently exist around the same drill family?`
- Read [docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md](d:/Project/wordloom-v3/docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md) when the question is `what operator semantics are still missing before a narrower runtime-owned runbook bridge can open?`

## Reader Notes

- This family is `runtime` first and `observability` second: observability is the diagnostic subdomain owned under one runtime worker chain here.
- The first release is draft because the proof path is defended, but trace-export completeness and a narrower runbook bridge may still be hardened later.
- Later sibling families should stay under `DOC-RUNTIME-*` when runtime remains the governing owner surface.