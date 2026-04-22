# ledger-SUP-S0A-2A-004-legacy-logs-earliest-structured-shape

```yaml
support_only_contract_release_ledger_supplement:
  supplement_series_id: ledger-SUP-S0A-2A
  supplement_sequence: 004
  supplement_id: ledger-SUP-S0A-2A-004-legacy-logs-earliest-structured-shape
  supplement_kind: support-only-contract-release-ledger-supplement
  status: completed
  owner_lane: S0G-1B
  created_at: 2026-04-22
  reviewed_at: 2026-04-22
  accepted_at: 2026-04-22
  writeback_started_at: 2026-04-22
  writeback_completed_at: 2026-04-22
  parent_ledger_id: ledger-S0A-2A-tools-workflow-log-lab-runbook-adr
  parent_source_id: S0A-2A
  parent_source_ref: GitHub issue S0A-2A (#24) (issue-only source; no local log exists in workspace)
  supplement_scope: fourth direct-evidence SUP round for the S0A-2A logs layer, using the two earliest retained structured logs to test whether the logs slice should remain deferred background or move into explicit DOC-WORKFLOW-LEGACY-LOGS historical review with a reciprocal bridge back to DOC-WORKFLOW-LOGS-0001
  target_reading_goal: show whether the retained earliest structured-log evidence now sharpens S0A-2A-R02 enough to justify parent-ledger rewrite, one historical-only DOC-WORKFLOW-LEGACY-LOGS child release, and one current-family bridge note on DOC-WORKFLOW-LOGS-0001
```

## Decision Frame

- This SUP ledger is attached only to parent row `S0A-2A-R02`.
- When this round opened, the parent-ledger judgment for the logs layer had already been rewritten, but that rewrite had not yet been defended through a dedicated packet-level accountability surface in the same way as the accepted `001`, `002`, and `003` rounds.
- The review question for this completed round was therefore procedural and semantic at the same time:
  - do the two earliest retained structured logs merely add background color to the existing logs story
  - or do they defend one independently judgeable earlier logs reader shape that justifies a dedicated historical-only child release plus explicit parent-ledger write-back
- This round is sequenced after the runbook, labs, and ADR rounds because the repo first needed the narrower parent-versus-child reader model and the explicit legacy-logs family decision before it could package the logs-layer evidence as one bounded SUP packet.

## Evidence Table

| supplement item id | parent row id | evidence ref | evidence type | attachment ids | verification status | effect on current verdict | proposed parent-ledger action | contract impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A-2A-R02-SUP-01` | `S0A-2A-R02` | `legacy/from_structured_docs/from-logs/v2-logs/log-S0A-dlq-replay-platform.md` | `md` | `none` | `verified` | `revises-existing` | `rewrite-parent-row` | `open-new-release` | This retained log opens with one capability thesis and then keeps its main reader body under numbered `What/How to do` operational blocks, which shows an earlier logs-shaped rule body that is materially different from the later `structured log identity and front matter` reader. It therefore sharpens the logs slice beyond issue-level background only. |
| `S0A-2A-R02-SUP-02` | `S0A-2A-R02` | `legacy/from_structured_docs/from-logs/v2-logs/log-S0B-graceful-termination+heathz-readyz+alert-threshold.md` | `md` | `none` | `verified` | `revises-existing` | `rewrite-parent-row` | `open-new-release` | This retained log repeats the same low-structure reader shape through one runtime-hardening thesis, numbered operational rule blocks, draft-to-adopted transitions, and a separate executable appendix. Together with `SUP-01`, it defends one earlier historical logs reader shape rather than merely extra background for the later current logs family. |

## Actor and Provenance Review Table

| supplement item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0A-2A-R02-SUP-01` | `unknown` | `role:packet-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-markdown-inspection` | `role:docs-governance-approver` | `accepted-for-packet` | The retained legacy log preserves enough bounded structural detail to defend an earlier logs-reader shape at packet level. | The repo preserves the source markdown path and the packet review chain explicitly, but the original named submitter is not defended by surviving issue-only history. |
| `S0A-2A-R02-SUP-02` | `unknown` | `role:packet-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-markdown-inspection` | `role:docs-governance-approver` | `accepted-for-packet` | The retained legacy log preserves enough repeated structural detail to defend a historical-only logs-family release plus a current-family bridge without clause carry-forward. | The repo preserves the source markdown path and the packet review chain explicitly, but the original named submitter is not defended by surviving issue-only history. |

## Governance Position Note

- The `Actor and Provenance Review Table` in this supplement is a packet-level event and accountability surface.
- These rows defend who maintained, reviewed, verified, and accepted the logs-direct-evidence packet; they do not replace the current-state governance reading for the parent ledger, the historical-only legacy child contract, or the later current logs-family contract.
- Under `S0G-1B`, current ownership, stewardship, and approval reading belongs on the parent-ledger and contract surfaces, while this supplement remains the historical evidence chain for direct-markdown review and write-back.

## Parent-Ledger Rows To Update

- `S0A-2A-R02`: revise the logs-layer row so it is defended through one accepted logs SUP round rather than a direct source-path write-back only, and keep the row as one explicit historical-review surface under `DOC-WORKFLOW-LEGACY-LOGS-0001`.

## Contract Changes Deferred Until Parent Write-Back

- `DOC-WORKFLOW-LEGACY-LOGS-0001`: if the parent-ledger rewrite is accepted, the earlier logs layer should remain recorded as one historical-only legacy release whose packet-level evidence chain is now `SUP-004 -> parent ledger -> child contract`.
- `DOC-WORKFLOW-LOGS-0001`: if the parent-ledger rewrite is accepted, the current logs-family reader should add one explicit bridge note pointing back to `DOC-WORKFLOW-LEGACY-LOGS-0001` as predecessor context without implying clause absorption.

## Preliminary Reading

- The two retained legacy logs do not overturn the later current logs-family reading already owned by `DOC-WORKFLOW-LOGS-0001`.
- They do revise the current logs-layer verdict materially enough that `S0A-2A-R02` should no longer read as issue-only bounded background or as a direct write-back without packet-level accountability.
- The resulting recommendation for this round was therefore:
  - keep the later current logs-family contract in place
  - rewrite the parent logs-layer row so it points to accepted `SUP-004`
  - retain `DOC-WORKFLOW-LEGACY-LOGS-0001` as the historical-only child release for the earliest structured-log reader shape
  - then add the reciprocal bridge note on `DOC-WORKFLOW-LOGS-0001`

## Reader Notes

- `log-S0A-dlq-replay-platform.md` is treated here as direct evidence because it keeps the logs layer at one capability-thesis plus numbered operational-rule-block reader shape rather than at identity or front-matter governance.
- `log-S0B-graceful-termination+heathz-readyz+alert-threshold.md` is treated here as direct evidence because it repeats the same earlier structured-reader shape while still leaving the later current logs-family identity/front-matter rule body untouched.
- This `004` SUP round now restores the full `SUP -> parent ledger -> child contract -> parent contract` chain for the `S0A-2A` logs slice.