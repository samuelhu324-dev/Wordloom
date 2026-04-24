# ledger-SUP-S0A-2A-003-adr-decision-summaries-and-boundary-shape

```yaml
support_only_contract_release_ledger_supplement:
  supplement_series_id: ledger-SUP-S0A-2A
  supplement_sequence: 003
  supplement_id: ledger-SUP-S0A-2A-003-adr-decision-summaries-and-boundary-shape
  supplement_kind: support-only-contract-release-ledger-supplement
  status: completed
  owner_lane: S0G-4A
  created_at: 2026-04-22
  reviewed_at: 2026-04-22
  accepted_at: 2026-04-22
  writeback_started_at: 2026-04-22
  writeback_completed_at: 2026-04-22
  parent_ledger_id: ledger-S0A-2A-tools-workflow-log-lab-runbook-adr
  parent_source_id: S0A-2A
  parent_source_ref: GitHub issue S0A-2A (#24) (issue-only source; no local log exists in workspace)
  supplement_scope: third direct-evidence SUP round for the S0A-2A ADR layer, using the retained Chronicle and outbox-worker ADRs to test whether the ADR slice should remain deferred background or move into explicit DOC-WORKFLOW-ADR child review
  target_reading_goal: show whether the retained ADR evidence now sharpens S0A-2A-R05 enough to justify parent-ledger rewrite, one first ADR child-opening packet, and parent-contract boundary write-back
```

## Decision Frame

- This SUP ledger is attached only to parent row `S0A-2A-R05`.
- When this round opened, the parent-ledger judgment still kept the ADR layer as bounded background because the broad issue-level source was not treated as strong enough direct owner evidence by itself.
- The review question for this completed round was narrower:
  - do the retained ADRs merely support the existing background reading
  - or do they revise the current verdict enough that the ADR layer should now enter explicit child-opening review
- This round is sequenced after the runbook and labs rounds because the repo now has one defended reader model for parent boundaries versus narrow current readers and can therefore test ADR extraction without reopening the earlier structure question.

## Evidence Table

| supplement item id | parent row id | evidence ref | evidence type | attachment ids | verification status | effect on current verdict | proposed parent-ledger action | contract impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A-2A-R05-SUP-01` | `S0A-2A-R05` | `legacy/from_structured_docs/from-adrs/adr-001-chronicle-projection-chronicle-events-to-entries.md` | `md` | `none` | `verified` | `revises-existing` | `rewrite-parent-row` | `open-new-release` | This ADR keeps Chronicle at the decision-summary layer rather than replaying the full lab or runbook execution path: it fixes context, decision, alternatives considered, consequences, and links back to the source operator and experiment surfaces. The file therefore shows one durable ADR reader shape beyond the broad issue-level mention alone. |
| `S0A-2A-R05-SUP-02` | `S0A-2A-R05` | `legacy/from_structured_docs/from-adrs/adr-002-evolution-worker-to-daemon.md` | `md` | `none` | `verified` | `revises-existing` | `rewrite-parent-row` | `open-new-release` | This ADR does the same on a cross-projection rule family: it distills the worker-to-daemon evolution into context, decision, alternatives considered, consequences, and links, while explicitly leaving implementation and SOP details to labs and runbooks. Together with `ADR-001`, it proves that the ADR layer had already become a bounded decision-summary surface rather than only workflow background. |

## Actor and Provenance Review Table

| supplement item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A-2A-R05-SUP-01` | `unknown` | `role:packet-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-markdown-inspection` | `role:docs-governance-approver` | `accepted-for-packet` | The retained ADR preserves enough bounded decision-summary detail to defend the ADR-layer extraction at packet level. | The repo preserves the source markdown path and the packet review chain explicitly, but the original named submitter is not defended by surviving issue-only history. |
| `S0A-2A-R05-SUP-02` | `unknown` | `role:packet-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-markdown-inspection` | `role:docs-governance-approver` | `accepted-for-packet` | The retained ADR preserves enough reusable decision-boundary detail to defend ADR-family child opening rather than leaving the layer as broad background only. | The repo preserves the source markdown path and the packet review chain explicitly, but the original named submitter is not defended by surviving issue-only history. |

## Governance Position Note

- The `Actor and Provenance Review Table` in this supplement is a packet-level event and accountability surface.
- These rows defend who maintained, reviewed, verified, and accepted the ADR-direct-evidence packet; they do not replace the current-state governance reading for the parent ledger, the ADR child contract, or the broader workflow parent contract.
- Under `S0G-4A/P4`, current ownership, stewardship, and approval reading belongs on the parent-ledger and contract surfaces, while this supplement remains the historical evidence chain for direct-markdown review and write-back.

## Parent-Ledger Rows To Update

- `S0A-2A-R05`: revise the ADR-layer row from `bounded-background` only into one explicit direct-evidence review surface, because the retained ADRs now prove durable decision-summary extraction beyond the broad workflow issue summary alone.

## Contract Changes Deferred Until Parent Write-Back

- `DOC-WORKFLOW-ADR` candidate: if the parent-ledger rewrite is accepted, the ADR layer should move from deferred background toward explicit child-opening review, with one first `DOC-WORKFLOW-ADR-0001` release acting as the narrow current-governance surface while the broader workflow parent keeps only the high-level ADR layer boundary.

## Preliminary Reading

- The two retained ADRs do not overturn the broad workflow-pipeline reading already owned by `DOC-WORKFLOW-0001`.
- They do revise the current ADR-layer verdict materially enough that `S0A-2A-R05` should no longer read as issue-only bounded background by default.
- The resulting recommendation for this round was therefore:
  - keep the broad workflow parent contract in place
  - rewrite the parent ADR-layer row to acknowledge direct ADR evidence
  - open one first `DOC-WORKFLOW-ADR` child packet
  - then bridge the broader parent ADR boundary back to that new narrower current reader

## Reader Notes

- `ADR-001` is treated here as direct evidence because it keeps Chronicle at the decision-summary layer: it states the source-of-truth versus projection boundary, stable pagination rule, alternatives considered, consequences, and links back to labs, runbooks, and operator evidence rather than replaying those materials inline.
- `ADR-002` is treated here as direct evidence because it fixes one reusable worker-to-daemon decision boundary across projections while still leaving runtime procedures, experiments, and operational recovery detail to runbooks and labs.
- This `003` SUP round now also proves that the repo can execute the full `SUP -> parent ledger -> child contract -> parent contract` bridge on an ADR sample without widening the ledgers into contract-reader tables.