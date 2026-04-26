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
  enforcement_surface: script
  violation_semantics: warning
  recorded_at: 2026-04-26
  reviewed_at: pending
  effective_from: 2026-04-26
  effective_until: ongoing
  introduced_by: docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md
  last_changed_by: docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md
  source_refs:
    - docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md
  cumulative_source_refs:
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
| `DOC-RUNTIME-OBSERVABILITY-0001-ST-01` | `Diagnosable chain requirement` | `active` | `introduced` | `S4G-1B/P0-C1-S1; S3A-2A-R01` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `2026-04-26` | `ongoing` | `in-force` | One admitted runtime handling chain should remain diagnosable through metrics, tracing, and structured logs via shared pivots and auditable evidence. | This is the narrow semantic core of the family. |
| `DOC-RUNTIME-OBSERVABILITY-0001-ST-02` | `Bounded owner surface` | `active` | `introduced` | `S4G-1B/P1-C1-S1S2` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `2026-04-26` | `ongoing` | `in-force` | The current bounded owner surface for this family is the search outbox projection worker for `projection=search_index_to_elastic`, with stable entrypoint `backend/scripts/search_outbox_worker.py`. | This clause prevents the family from floating above code with no bounded owner. |
| `DOC-RUNTIME-OBSERVABILITY-0001-ST-03` | `Minimum shared pivots and signals` | `active` | `introduced` | `S4G-1B/P1-C1-S2` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `2026-04-26` | `ongoing` | `in-force` | The current minimum shared pivots are `trace_id/traceparent`, `claim_batch_id`, `outbox event id`, and worker labels such as `projection` and `op`; the current minimum signals are `outbox_*` metrics, worker tracing spans, and worker structured logs. | Later releases may refine this field set, but should not weaken it silently. |
| `DOC-RUNTIME-OBSERVABILITY-0001-ST-04` | `Defended proof path` | `active` | `introduced` | `S4G-1B/P2-C1-S1S2` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `2026-04-26` | `ongoing` | `in-force` | The first defended proof path for this family is `es_write_block_4xx`, which must start `search_outbox_worker@v1`, verify expected before/after projection metrics and DB reason family movement, and retain worker-start, metrics, result, and worker-log evidence in one run-scoped bundle. | Tracing export completeness can still be hardened later without blocking this first release. |
| `DOC-RUNTIME-OBSERVABILITY-0001-ST-05` | `Runbook boundary` | `active` | `introduced` | `S4G-1B/P0-C1-S3; S4G-1B/P3-C1-S2` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `DOC-RUNTIME-OBSERVABILITY-0001` | `2026-04-26` | `2026-04-26` | `ongoing` | `in-force` | This release does not own fallback, switch, shadow or dual-run, or coexistence-window operator steps; those remain downstream runbook concerns once a narrower runbook bridge packet is justified. | Keeps semantic contract and operator procedure distinct. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-RUNTIME-OBSERVABILITY-0001-CH-01` | `DOC-RUNTIME-OBSERVABILITY-0001` | `introduced` | `none` | `DOC-RUNTIME-OBSERVABILITY-0001-ST-01; DOC-RUNTIME-OBSERVABILITY-0001-ST-02; DOC-RUNTIME-OBSERVABILITY-0001-ST-03; DOC-RUNTIME-OBSERVABILITY-0001-ST-04; DOC-RUNTIME-OBSERVABILITY-0001-ST-05` | `2026-04-26` | `2026-04-26` | The family is now explicit because S4G-1B already fixed one weak semantic claim, one bounded worker surface, one stable entrypoint, and one defended proof path strongly enough to support a current draft reader. | `S4G-1B/P0-C1-S1S2S3; S4G-1B/P1-C1-S1S2; S4G-1B/P2-C1-S1S2; S4G-1B/P3-C1-S1S2` | The release is deliberately narrow and should not be read as a repo-wide observability umbrella. |

## Release Change

- This release opens the first runtime observability contract from `S4G-1B`.
- The release fixes one current reader that was previously held only in the source log scaffold:
  - the minimum diagnostic chain requirement
  - the bounded owner surface and stable entrypoint
  - the minimum shared pivots and signals
  - the first defended proof path
- This release intentionally does not open a separate runbook bridge packet yet.

## Contract Statement

- `DOC-RUNTIME-OBSERVABILITY-0001-ST-01`: One admitted runtime handling chain should remain diagnosable through metrics, tracing, and structured logs via shared pivots and auditable evidence.
- `DOC-RUNTIME-OBSERVABILITY-0001-ST-02`: The current bounded owner surface for this family is the `search_index_to_elastic` projection worker with stable entrypoint `backend/scripts/search_outbox_worker.py`.
- `DOC-RUNTIME-OBSERVABILITY-0001-ST-03`: The minimum shared pivots and signals for this family are `trace_id/traceparent`, `claim_batch_id`, `outbox event id`, `projection/op`, `outbox_*` metrics, worker tracing spans, and worker structured logs.
- `DOC-RUNTIME-OBSERVABILITY-0001-ST-04`: The first defended proof path is `es_write_block_4xx`, with run-scoped evidence that retains worker-start, metrics, result, and worker-log artifacts on the same worker surface.
- `DOC-RUNTIME-OBSERVABILITY-0001-ST-05`: Fallback, switch, shadow or dual-run, and coexistence-window procedures remain downstream runbook concerns rather than current contract clauses.

## Current Reading

- Read this release when the question is `what is the current runtime observability rule for the first defended worker chain under S4G?`
- Read [docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md](d:/Project/wordloom-v3/docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md) when the question is `how was this contract staged, bounded, and proven before release?`
- Read [docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md](d:/Project/wordloom-v3/docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md) when the question is `what operator steps currently exist around the same drill family?`

## Reader Notes

- This family is `runtime` first and `observability` second: observability is the diagnostic subdomain owned under one runtime worker chain here.
- The first release is draft because the proof path is defended, but trace-export completeness and a narrower runbook bridge may still be hardened later.
- Later sibling families should stay under `DOC-RUNTIME-*` when runtime remains the governing owner surface.