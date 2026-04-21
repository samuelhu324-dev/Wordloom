# ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline

```yaml
runbook_run_patch_ledger:
  patch_ledger_id: ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline
  patch_kind: runbook-run-ledger-patch
  status: active
  owner_lane: S0G-2B
  parent_runbook_id: run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline
  parent_runbook_ref: docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md
  parent_run_ledger_id: ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline
  parent_run_ledger_ref: docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md
  parent_run_row_id: RUN-001
  patch_sequence: 001
  created_at: 2026-04-21
  reviewed_at: 2026-04-21
  accepted_at: pending
  writeback_started_at: 2026-04-21
  writeback_completed_at: 2026-04-21
  patch_scope: bind the first bounded repair packet surface for WORKFLOW-GITHUB-001 to the first admitted four-sample run without forcing a runbook release bump.
  patch_reason_class: mixed-bounded-repair
  approval_boundary: runbook-bound patch packets should remain reviewable and approvable before they rewrite admitted run accounting or source-log conclusions.
  target_reading_goal: show how the first runbook-bound repair packet for WORKFLOW-GITHUB-001 attached to RUN-001 after the first real sample run exposed bounded fixes.
```

## Decision Frame

- This file still preserves the first canonical patch-ledger name for `WORKFLOW-GITHUB-001`, but it is no longer only a reserved surface.
- The patch ledger is now bound to `RUN-001`, because the first admitted live sample run exposed bounded repairs that were fixed without changing the defended runbook release.
- Future bounded repairs for this same release should still land here rather than in an unstructured log-first patch note.
- For this packet, the admitted script repairs, the patch ledger write-back, and the dependent S4F/run-accounting updates should be committed together as one bounded patch packet; they should not be split into a later standalone script-only commit.

## Patch Change Table

| patch item id | parent run row id | target artifact or path | change class | evidence refs | verification status | approval status | effect on current runbook release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-001-I01` | `RUN-001` | `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md` | `mixed-bounded-repair` | `docs/logs/log-S0G-2B-support-only-ledger-placement-and-patch-ledger-bridge.md` | `verified` | `pending` | `no-release-bump` | `append-patch-ref` | `none` | The first patch ledger entry now remains attached to the admitted run that consumed the support-only placement and patch-ledger bridge contract. |
| `PATCH-001-I02` | `RUN-001` | `scripts/issues/gen_issue_draft.py` | `operator-override-gap-repair` | `docs/issues/issue-S4F-1A-backend-only-access-subscription-deployable-cut.json` | `verified` | `pending` | `no-release-bump` | `append-patch-ref` | `unblock-first-s4f-sample-batch` | Add one explicit milestone-skip override so historical sample logs with roadmap-derived milestones can still enter live create mode when the target GitHub repo does not maintain matching milestone rows. |
| `PATCH-001-I03` | `RUN-001` | `scripts/issues/plan_pr_prep.py` | `multi-item-preview-body-repair` | `artifacts/_tmp_s4f_2a_front_half_preflight_result.json` | `verified` | `pending` | `no-release-bump` | `append-patch-ref` | `unblock-batched-s4f-pr-create` | Generate one preview body file per PR-prep item so multi-item manifests do not overwrite earlier item bodies and fail front-half preflight against the wrong sample. |

## Attachment Review Table

| attachment id | patch item id | click-through asset ref | review status | approval basis | review note |
| --- | --- | --- | --- | --- | --- |
| `PATCH-001-I01-ATT-01` | `PATCH-001-I01` | `docs/logs/log-S0G-2B-support-only-ledger-placement-and-patch-ledger-bridge.md` | `accepted-for-packet` | The patch ledger naming and bridge rule were fixed before the first live run and are now part of the admitted repair surface attached to `RUN-001`. | This attachment remains the contract-defining bridge evidence that allowed the first bounded repair packet to land in the support-only patch ledger. |
| `PATCH-001-I02-ATT-01` | `PATCH-001-I02` | `docs/issues/issue-S4F-1A-backend-only-access-subscription-deployable-cut.json` | `accepted-for-packet` | The first live S4F sample exposed a fail-closed milestone mismatch between roadmap-derived milestone names and the current GitHub milestone catalog. | Live create now succeeds under explicit milestone-skip override, so this repair is verified for the first S4F sample batch. |
| `PATCH-001-I03-ATT-01` | `PATCH-001-I03` | `artifacts/_tmp_s4f_2a_front_half_preflight_result.json` | `accepted-for-packet` | The first batched S4F PR-preflight exposed that earlier PR-prep items were reusing the last rendered preview body and therefore failed the body-shape contract against the wrong sample. | Re-running `S4F-2A` preflight after the per-item preview-path fix returned `allow-front-half-preflight`, confirming the bounded repair. |

## Actor and Provenance Review Table

| patch item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `PATCH-001-I01` | `role:workflow-operator` | `role:runbook-maintainer` | `pending` | `role:evidence-verifier` | `direct-doc-inspection` | `pending` | `pending` | The support-only patch surface is now attached to the first admitted run and remains pending only for explicit human approval. | This row records the contract bridge that allowed later bounded repairs in the same packet to attach cleanly to `RUN-001`. |
| `PATCH-001-I02` | `role:workflow-operator` | `role:workflow-maintainer` | `pending` | `role:evidence-verifier` | `live-create-replay-after-explicit-milestone-skip` | `pending` | `pending` | The repair is bounded to one explicit operator override path and preserves the default fail-closed milestone contract for normal create mode. | This row is opened by the first real S4F sample attempt, which failed closed on missing GitHub milestone `M1` before live issue creation could complete. |
| `PATCH-001-I03` | `role:workflow-operator` | `role:workflow-maintainer` | `pending` | `role:evidence-verifier` | `front-half-preflight-replay-after-per-item-preview-path-fix` | `pending` | `pending` | The repair is bounded to preview artifact generation for multi-item PR-prep manifests and does not relax any live create or body-contract checks. | This row was opened only after the first batched S4F PR-preflight showed `S4F-2A` reading `S4F-2C`'s preview body because all items shared one preview path. |

## Reader Notes

- Patch ledgers for `WORKFLOW-GITHUB-001` should remain under `docs/runbook/support-only/`.
- `PATCH-001` is now attached to parent run row `RUN-001`; later bounded repairs for this release should preserve that binding unless a new admitted run row becomes the true trigger.
- If a future repair is admitted under `PATCH-001`, keep the implementation diff and the patch/accounting write-back in the same patch-scoped commit packet unless a later source log explicitly reclassifies the work as a release bump or a different lane.
- If a future bounded repair changes runbook semantics materially, do not continue under this patch series; open a new source log and a new runbook release instead.