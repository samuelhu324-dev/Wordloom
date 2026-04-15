# ledger-SUP-S0A-2A-001-tools-workflow-log-lab-runbook-adr

```yaml
support_only_contract_release_ledger_supplement:
  supplement_series_id: ledger-SUP-S0A-2A
  supplement_sequence: 001
  supplement_id: ledger-SUP-S0A-2A-001-tools-workflow-log-lab-runbook-adr
  supplement_kind: support-only-contract-release-ledger-supplement
  status: completed
  owner_lane: S0F-7D
  created_at: 2026-04-12
  reviewed_at: 2026-04-12
  accepted_at: 2026-04-12
  writeback_started_at: 2026-04-12
  writeback_completed_at: 2026-04-12
  parent_ledger_id: ledger-S0A-2A-tools-workflow-log-lab-runbook-adr
  parent_source_id: S0A-2A
  parent_source_ref: GitHub issue S0A-2A (#24) (issue-only source; no local log exists in workspace)
  supplement_scope: first runbook-direct-evidence SUP for the S0A-2A runbook layer, using the earliest long-lived projection SOPs to test whether the runbook slice should remain bounded background or move into direct child-promotion review
  target_reading_goal: show whether later direct runbook evidence is now strong enough to revise the S0A-2A runbook-layer verdict from deferred bounded background toward explicit DOC-WORKFLOW-RUNBOOK child review
```

## Decision Frame

- This SUP ledger is attached only to parent row `S0A-2A-R04`.
- When this round opened, the parent-ledger judgment still kept the runbook layer as bounded background because the broad issue-level source was not treated as strong enough direct owner evidence by itself.
- The review question for this completed round was narrower:
  - do the earliest long-lived projection SOPs merely support the existing background reading
  - or do they revise the current verdict enough that the runbook layer should now enter direct child-promotion review
- This round is prioritized because broader roadmap/log skeleton reorganization is still under review, while earlier workflow-layer contract extraction can keep progressing through defended direct evidence packets.

## Evidence Table

| supplement item id | parent row id | evidence ref | evidence type | attachment ids | verification status | effect on current verdict | proposed parent-ledger action | contract impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A-2A-R04-SUP-01` | `S0A-2A-R04` | `legacy/from_structured_docs/from-runbook/run-001-search-projection.md` | `md` | `none` | `verified` | `revises-existing` | `rewrite-parent-row` | `open-new-release` | This SOP shows that once the search projection path had succeeded, the next durable operator question became whether projection failure, replay, rebuild, readiness, and runtime guardrails could be operated safely rather than only experimented with in labs. The file carries long-lived operator guidance across startup, migration, rebuild, metrics, failure handling, replay, and regression checks, so the runbook layer is no longer only a broad issue-level background mention. |
| `S0A-2A-R04-SUP-02` | `S0A-2A-R04` | `legacy/from_structured_docs/from-runbook/run-003-chronicle-projection.md` | `md` | `none` | `verified` | `revises-existing` | `rewrite-parent-row` | `open-new-release` | This SOP shows the same long-lived operator extraction pattern for the chronicle projection path: once the projection path existed, the durable need moved to rebuildability, daemon runtime checks, replay, observability, and failure handling, with explicit operator steps and acceptance language. Together with `run-001`, it demonstrates that runbooks were already being extracted from experimental labs content into reusable operator-facing workflow guidance. |

## Actor and Provenance Review Table

| supplement item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A-2A-R04-SUP-01` | `unknown` | `role:packet-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-markdown-inspection` | `role:docs-governance-approver` | `accepted-for-packet` | The retained runbook preserves enough durable operator detail to defend the runbook-layer extraction at packet level. | The repo preserves the source markdown path and the packet review chain explicitly, but the original named submitter is not defended by surviving issue-only history. |
| `S0A-2A-R04-SUP-02` | `unknown` | `role:packet-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-markdown-inspection` | `role:docs-governance-approver` | `accepted-for-packet` | The retained runbook preserves enough durable operator detail to defend the chronicle projection runbook extraction at packet level. | The repo preserves the source markdown path and the packet review chain explicitly, but the original named submitter is not defended by surviving issue-only history. |

## Governance Position Note

- The `Actor and Provenance Review Table` in this supplement is a packet-level event and accountability surface.
- These rows defend who maintained, reviewed, verified, and accepted the runbook-direct-evidence packet; they do not replace the current-state governance reading for the parent ledger or the runbook child contract.
- Under `S0F-9A/P3` second-sample work, current ownership, stewardship, and approval reading belongs on the parent-ledger and child-contract surfaces, while this supplement remains the historical evidence chain for direct-markdown review and write-back.

## Parent-Ledger Rows To Update

- `S0A-2A-R04`: revise the runbook-layer row from `bounded-background` only into one explicit direct-evidence review surface, because the earliest projection SOPs now prove durable operator-facing runbook extraction beyond the broad issue summary alone.

## Contract Changes Deferred Until Parent Write-Back

- `DOC-WORKFLOW-RUNBOOK` candidate: if the parent-ledger rewrite is accepted, the runbook layer should move from deferred background toward explicit child-promotion review, with a later release-opening decision based on the defended runbook packet rather than on issue-level wording alone.

## Preliminary Reading

- The two runbooks do not overturn the broad workflow-pipeline reading already owned by `DOC-WORKFLOW-0001`.
- They do revise the current runbook-layer verdict materially enough that `S0A-2A-R04` should no longer read as issue-only bounded background by default.
- The resulting recommendation for this round was therefore:
  - keep the broad workflow parent contract unchanged for now
  - rewrite the parent runbook-layer row to acknowledge direct runbook evidence
  - then review whether a `DOC-WORKFLOW-RUNBOOK` child-opening packet should follow

## Reader Notes

- These two legacy runbooks are treated here as direct evidence because they already convert projection success, failure-management labs, and runtime-verification learning into durable operator SOPs.
- This `001` SUP round intentionally did not force immediate child-contract creation; it first asked the parent ledger to stop treating the runbook layer as background-only before `DOC-WORKFLOW-RUNBOOK-0001` was later opened.
- This supplement now also acts as the packet-level proof that review, evidence verification, and final approval can be separated cleanly on a markdown-evidence-backed sample without turning the supplement into the current governance surface.