# ledger-run-PATCH-002-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline

```yaml
runbook_run_patch_ledger:
  patch_ledger_id: ledger-run-PATCH-002-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline
  patch_kind: runbook-run-ledger-patch
  status: active
  owner_lane: S0G-2B
  parent_runbook_id: run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline
  parent_runbook_ref: docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md
  parent_run_ledger_id: ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline
  parent_run_ledger_ref: docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md
  parent_run_row_id: RUN-001
  patch_sequence: 002
  created_at: 2026-04-21
  reviewed_at: 2026-04-21
  accepted_at: pending
  writeback_started_at: 2026-04-21
  writeback_completed_at: 2026-04-21
  patch_scope: bind the second bounded repair packet surface for WORKFLOW-GITHUB-ISSUES-001 to RUN-001 after the later S4F follow-up packet exposed milestone-title and follow-up PR selection/title gaps.
  patch_reason_class: mixed-bounded-repair
  approval_boundary: runbook-bound patch packets should remain reviewable and approvable before they rewrite admitted run accounting or source-log conclusions.
  target_reading_goal: show how the second runbook-bound repair packet for WORKFLOW-GITHUB-ISSUES-001 attached to RUN-001 after the S4F follow-up PR packet exposed bounded milestone and PR-prep selection/title repairs.
```

## Decision Frame

- This patch packet is still bound to `RUN-001`, because the repair surface was exposed only while closing the same first admitted S4F sample batch.
- The repaired behavior remains bounded: live milestone-title resolution for issue draft generation and explicit commit-scope selection/title shaping for follow-up PR prep.
- The patch does not change the defended runbook release; it only repairs local workflow automation surfaces needed to complete the already admitted run packet cleanly.

## Patch Change Table

| patch item id | parent run row id | target artifact or path | change class | evidence refs | verification status | approval status | effect on current runbook release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-002-I01` | `RUN-001` | `scripts/issues/gen_issue_draft.py` | `milestone-title-resolution-repair` | `artifacts/_tmp_s4f_1a_issue_draft_validation.json` | `verified` | `pending` | `no-release-bump` | `append-patch-ref` | `unblock-s4f-milestone-convergence` | Roadmap-derived milestone values now resolve to the live GitHub milestone title when the target repository uses a `road-xxx-yy: ...` title instead of the bridge shorthand. |
| `PATCH-002-I02` | `RUN-001` | `scripts/issues/plan_pr_prep.py` | `explicit-follow-up-selection-repair` | `artifacts/_tmp_s4f_followup_pr_plan.json` | `verified` | `pending` | `no-release-bump` | `append-patch-ref` | `unblock-followup-pr-slicing` | PR-prep now accepts explicit `selected_commit_shas` so a later follow-up PR packet can select only the remaining exact units instead of all branch-visible exact-ID commits. |
| `PATCH-002-I03` | `RUN-001` | `scripts/issues/plan_pr_prep.py` | `explicit-follow-up-title-scope-repair` | `artifacts/_tmp_s4f_followup_pr_plan.json` | `verified` | `pending` | `no-release-bump` | `append-patch-ref` | `unblock-followup-pr-title-contract` | PR-prep now prioritizes explicit selected follow-up units over checklist-phase fallback so follow-up PR titles stay scoped to the actual `P4` units being merged. |

## Attachment Review Table

| attachment id | patch item id | click-through asset ref | review status | approval basis | review note |
| --- | --- | --- | --- | --- | --- |
| `PATCH-002-I01-ATT-01` | `PATCH-002-I01` | `artifacts/_tmp_s4f_1a_issue_draft_validation.json` | `accepted-for-packet` | The validation draft for `S4F-1A` returned the live GitHub milestone title instead of the roadmap shorthand. | Checked the dry-run issue draft after the milestone-title resolution repair. |
| `PATCH-002-I02-ATT-01` | `PATCH-002-I02` | `artifacts/_tmp_s4f_followup_pr_plan.json` | `accepted-for-packet` | The combined follow-up PR plan shows each item using the explicitly selected commit set instead of all exact-ID commits on the branch. | Checked the post-repair follow-up PR plan for narrowed selected-commit scope. |
| `PATCH-002-I03-ATT-01` | `PATCH-002-I03` | `artifacts/_tmp_s4f_followup_pr_plan.json` | `accepted-for-packet` | The combined follow-up PR plan now emits titles such as `S4F-1A/P4-C1-S1+P4-C2-S1` and `S4F-2B/P4-C1-S1+P4-C1-S2+P4-C2-S1`. | Checked the post-repair follow-up PR plan for explicit selected-unit title shaping. |

## Actor and Provenance Review Table

| patch item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-002-I01` | `role:workflow-operator` | `role:workflow-maintainer` | `pending` | `role:evidence-verifier` | `issue-draft-replay-against-live-milestone-catalog` | `pending` | `pending` | The repair is bounded to live milestone-title normalization and preserves explicit source-log milestone override precedence. | This row was opened when the S4F follow-up milestone convergence showed that roadmap shorthand values did not match the live GitHub milestone title catalog. |
| `PATCH-002-I02` | `role:workflow-operator` | `role:workflow-maintainer` | `pending` | `role:evidence-verifier` | `followup-pr-plan-replay-with-explicit-selected-commit-shas` | `pending` | `pending` | The repair is bounded to follow-up PR planning and does not relax any issue or PR body validation rules. | This row was opened when the S4F follow-up PR packet could not be sliced correctly because PR-prep defaulted to all exact-ID commits on the branch. |
| `PATCH-002-I03` | `role:workflow-operator` | `role:workflow-maintainer` | `pending` | `role:evidence-verifier` | `followup-pr-plan-replay-with-explicit-title-scope-check` | `pending` | `pending` | The repair is bounded to title-shaping priority and preserves the existing exact-ID naming scheme. | This row was opened when the first narrowed follow-up PR plan still collapsed back to broad checklist-phase titles instead of the selected `P4` unit scope. |

## Reader Notes

- `PATCH-002` records the second bounded repair packet attached to `RUN-001` after the later S4F follow-up work exposed new workflow gaps.
- The admitted repair surface for this packet is limited to milestone-title normalization and follow-up PR-prep commit/title selection.
- No runbook release bump is justified by this packet; the fixes remain bounded to the same defended release used by `RUN-001`.