# ledger-SUP-S0A-2A-tools-workflow-log-lab-runbook-adr

```yaml
support_only_contract_release_ledger_supplement:
  supplement_id: ledger-SUP-S0A-2A-tools-workflow-log-lab-runbook-adr
  supplement_kind: support-only-contract-release-ledger-supplement
  status: draft
  owner_lane: S0F-7D
  parent_ledger_id: ledger-S0A-2A-tools-workflow-log-lab-runbook-adr
  parent_source_id: S0A-2A
  parent_source_ref: GitHub issue S0A-2A (#24) (issue-only source; no local log exists in workspace)
  supplement_scope: first runbook-direct-evidence SUP for the S0A-2A runbook layer, using the earliest long-lived projection SOPs to test whether the runbook slice should remain bounded background or move into direct child-promotion review
  target_reading_goal: show whether later direct runbook evidence is now strong enough to revise the S0A-2A runbook-layer verdict from deferred bounded background toward explicit DOC-WORKFLOW-RUNBOOK child review
```

## Decision Frame

- This SUP ledger is attached only to parent row `S0A-2A-R04`.
- The current parent-ledger judgment keeps the runbook layer as bounded background because the broad issue-level source was not treated as strong enough direct owner evidence by itself.
- The current review question is narrower:
  - do the earliest long-lived projection SOPs merely support the existing background reading
  - or do they revise the current verdict enough that the runbook layer should now enter direct child-promotion review
- This round is prioritized because broader roadmap/log skeleton reorganization is still under review, while earlier workflow-layer contract extraction can keep progressing through defended direct evidence packets.

## Evidence Table

| supplement item id | parent row id | evidence ref | evidence type | attachment ids | verification status | effect on current verdict | proposed parent-ledger action | contract impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A-2A-R04-SUP-01` | `S0A-2A-R04` | `legacy/from_structured_docs/from-runbook/run-001-search-projection.md` | `md` | `none` | `verified` | `revises-existing` | `rewrite-parent-row` | `open-new-release` | This SOP shows that once the search projection path had succeeded, the next durable operator question became whether projection failure, replay, rebuild, readiness, and runtime guardrails could be operated safely rather than only experimented with in labs. The file carries long-lived operator guidance across startup, migration, rebuild, metrics, failure handling, replay, and regression checks, so the runbook layer is no longer only a broad issue-level background mention. |
| `S0A-2A-R04-SUP-02` | `S0A-2A-R04` | `legacy/from_structured_docs/from-runbook/run-003-chronicle-projection.md` | `md` | `none` | `verified` | `revises-existing` | `rewrite-parent-row` | `open-new-release` | This SOP shows the same long-lived operator extraction pattern for the chronicle projection path: once the projection path existed, the durable need moved to rebuildability, daemon runtime checks, replay, observability, and failure handling, with explicit operator steps and acceptance language. Together with `run-001`, it demonstrates that runbooks were already being extracted from experimental labs content into reusable operator-facing workflow guidance. |

## Parent-Ledger Rows To Update

- `S0A-2A-R04`: revise the runbook-layer row from `bounded-background` only into one explicit direct-evidence review surface, because the earliest projection SOPs now prove durable operator-facing runbook extraction beyond the broad issue summary alone.

## Contract Changes Deferred Until Parent Write-Back

- `DOC-WORKFLOW-RUNBOOK` candidate: if the parent-ledger rewrite is accepted, the runbook layer should move from deferred background toward explicit child-promotion review, with a later release-opening decision based on the defended runbook packet rather than on issue-level wording alone.

## Preliminary Reading

- The two runbooks do not overturn the broad workflow-pipeline reading already owned by `DOC-WORKFLOW-0001`.
- They do revise the current runbook-layer verdict materially enough that `S0A-2A-R04` should no longer read as issue-only bounded background by default.
- The current draft recommendation is therefore:
  - keep the broad workflow parent contract unchanged for now
  - rewrite the parent runbook-layer row to acknowledge direct runbook evidence
  - then review whether a `DOC-WORKFLOW-RUNBOOK` child-opening packet should follow

## Reader Notes

- These two legacy runbooks are treated here as direct evidence because they already convert projection success, failure-management labs, and runtime-verification learning into durable operator SOPs.
- The current SUP round intentionally does not force immediate child-contract creation; it first asks the parent ledger to stop treating the runbook layer as background-only.