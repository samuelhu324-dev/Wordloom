# ledger-SUP-S0A-2A-002-labs-early-failure-management-and-pre-drills-shape

```yaml
support_only_contract_release_ledger_supplement:
  supplement_series_id: ledger-SUP-S0A-2A
  supplement_sequence: 002
  supplement_id: ledger-SUP-S0A-2A-002-labs-early-failure-management-and-pre-drills-shape
  supplement_kind: support-only-contract-release-ledger-supplement
  status: completed
  owner_lane: S0F-7E
  created_at: 2026-04-12
  reviewed_at: 2026-04-12
  accepted_at: 2026-04-12
  writeback_started_at: 2026-04-12
  writeback_completed_at: 2026-04-12
  parent_ledger_id: ledger-S0A-2A-tools-workflow-log-lab-runbook-adr
  parent_source_id: S0A-2A
  parent_source_ref: GitHub issue S0A-2A (#24) (issue-only source; no local log exists in workspace)
  supplement_scope: second direct-evidence SUP round for the S0A-2A labs layer, using the early failure-management experiments and search projection closure labs to test whether the labs slice should remain deferred background or move into explicit DOC-WORKFLOW-LABS historical review
  target_reading_goal: show whether the earlier labs evidence now sharpens S0A-2A-R03 enough to justify a parent-ledger rewrite before any DOC-WORKFLOW-LABS historical-backfill release is considered
```

## Decision Frame

- This SUP ledger is attached only to parent row `S0A-2A-R03`.
- When this round opened, the parent-ledger judgment still kept the labs layer as bounded background because the broad issue-level source was not treated as strong enough direct owner evidence by itself.
- The review question for this completed round was narrower:
  - do these earlier labs only support the existing background reading
  - or do they revise the current verdict enough that the labs layer should now enter explicit historical review rather than staying deferred by default
- This round is sequenced after the `001` runbook round because the repo now needs one concrete sample showing that repeated SUP packets under the same parent can separate runbook extraction from earlier labs archaeology.

## Evidence Table

| supplement item id | parent row id | evidence ref | evidence type | attachment ids | verification status | effect on current verdict | proposed parent-ledger action | contract impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A-2A-R03-SUP-01` | `S0A-2A-R03` | `legacy/from_structured_docs/from-labs/labs-004-worker-failure-management-v1-v4.md` | `md` | `none` | `verified` | `revises-existing` | `rewrite-parent-row` | `defer-contract-change` | This labs packet is explicitly framed as a hand-controlled experiment set that should be run before later runbook codification. It captures stuck recovery, retry convergence, replay, failed-state auditability, and daemon runtime engineering as executable lab work rather than as broad issue prose, so the labs layer is no longer supported only by the mixed issue summary. |
| `S0A-2A-R03-SUP-02` | `S0A-2A-R03` | `legacy/from_structured_docs/from-labs/labs-006-search-projection-search-index-to-elastic.md` | `md` | `none` | `verified` | `revises-existing` | `rewrite-parent-row` | `defer-contract-change` | This labs packet closes the search projection loop around `search_index -> elastic`, explicitly reuses earlier labs rounds including `labs-004`, and states that the result should later settle into runbook material. It therefore preserves a distinct earlier labs-shaped layer before the later runbook extraction and strengthens the case for a defended labs-specific write-back on `S0A-2A-R03`. |

## Parent-Ledger Rows To Update

- `S0A-2A-R03`: revise the labs-layer row from `bounded-background` only into one explicit direct-evidence review surface, because the early failure-management and search projection lab packets now show durable experimental ownership beyond the broad issue summary alone.

## Contract Changes Deferred Until Parent Write-Back

- `DOC-WORKFLOW-LABS` candidate: if the parent-ledger rewrite is accepted, the labs layer should move from deferred background toward explicit historical review, with any later `historical-backfill` or other release-opening decision made only after the parent packet is accepted.

## Evidence Time Audit

| supplement item id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A-2A-R03-SUP-01` | `2026-02-03` | `unknown` | `2026-02-03` | `unknown` | `day` | `legacy source currently proves only a local execution date, not a defended offset or second-level timestamp` | `labs-004` explicitly records multiple experiment sections as executed on `2026-02-03`, so the earlier labs packet has at least defended day-level timing even though second-level chronology is still absent. |
| `S0A-2A-R03-SUP-02` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `legacy source currently exposes no defended execution timestamp in the retained packet` | `labs-006` is clearly earlier labs material, but the retained source still needs narrower time reconstruction before any stronger chronology claim is made. |

## Preliminary Reading

- These two labs do not overturn the broad workflow-pipeline reading already owned by `DOC-WORKFLOW-0001`.
- They do revise the current labs-layer verdict materially enough that `S0A-2A-R03` should no longer read as issue-only bounded background by default.
- The resulting recommendation for this round was therefore:
  - keep the broad workflow parent contract unchanged for now
  - rewrite the parent labs-layer row to acknowledge direct labs evidence
  - then review whether one `DOC-WORKFLOW-LABS` historical-backfill or other dedicated child-opening packet should follow

## Reader Notes

- `labs-004` is treated here as direct evidence because it explicitly says the experiments should precede later runbook stabilization rather than being read as already-final SOPs.
- `labs-006` is treated here as direct evidence because it closes the search projection lab loop while still pointing forward to later runbook codification, which keeps the labs-versus-runbook boundary readable.
- This `002` SUP round now stops after parent-ledger write-back and does not yet write into `DOC-WORKFLOW-LABS`.