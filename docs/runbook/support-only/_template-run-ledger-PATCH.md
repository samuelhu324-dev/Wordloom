# run-ledger-patch-template-v1

Use this patch ledger when one stable runbook release needs a bounded repair packet that should remain under the same runbook release instead of forcing a release bump.
This patch ledger is a support-only, supplement-class surface: it owns patch-level evidence admission, review, approval, and downstream write-back for one runbook family.

## Naming Rule

- Name patch ledgers as `ledger-run-PATCH-<patch-sequence>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- `ledger-run-PATCH-<patch-sequence>` is the fixed prefix and records the append-only patch round for one stable runbook release.
- `<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>` must match the bound runbook suffix exactly.
- Preferred example shape:
  - `ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`

## Minimal Header

```yaml
runbook_run_patch_ledger:
  patch_ledger_id: <ledger-run-PATCH-001-WORKFLOW-GITHUB-001-summary>
  patch_kind: runbook-run-ledger-patch
  status: <draft|active|completed>
  owner_lane: <S0G-2B>
  parent_runbook_id: <run-WORKFLOW-GITHUB-001-summary>
  parent_runbook_ref: <docs/runbook/run-WORKFLOW-GITHUB-001-summary.md>
  parent_run_ledger_id: <ledger-run-001-WORKFLOW-GITHUB-001-summary>
  parent_run_ledger_ref: <docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-summary.md>
  parent_run_row_id: <RUN-001|pending|not-yet-bound>
  patch_sequence: <001>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  patch_scope: <what bounded repair this packet admits>
  patch_reason_class: <docs-fix|script-fix|manifest-fix|evidence-fix|mixed-bounded-repair>
  approval_boundary: <who must approve this patch before it may update ledgers, logs, or live artifacts>
  target_reading_goal: <what later readers should understand after this patch ledger is applied>
```

## Patch Change Table

| patch item id | parent run row id | target artifact or path | change class | evidence refs | verification status | approval status | effect on current runbook release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<RUN-001|pending>` | `<artifact path|script path|doc path>` | `<docs-fix|script-fix|manifest-fix|evidence-fix|mixed-bounded-repair>` | `<artifact path|diff|screenshot path>` | `<pending|verified|rejected>` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<no-release-bump|candidate-release-bump-needs-log>` | `<no-change|append-patch-ref|rewrite-run-row|open-sup-ledger>` | `<none|rerun-required|rewrite-source-log|rewrite-runbook-binding>` | `<why this patch matters>` |

## Attachment Review Table

| attachment id | patch item id | click-through asset ref | review status | approval basis | review note |
| --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01-ATT-01>` | `<PATCH-001-I01>` | `[open asset](./asset-name.png)` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<why this attachment is sufficient or insufficient>` | `<what the reviewer checked>` |

## Actor and Provenance Review Table

| patch item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<unknown|pending|role:operator|name>` | `<unknown|pending|role:runbook-maintainer|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-artifact-inspection|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<why this approval state is defended>` | `<why any actor fields remain partial>` |

## Bridge Rule

- A patch ledger is supplement-class and support-only, but it is not the same as a general SUP ledger.
- Use a patch ledger when the repair is bounded, runbook-bound, and still within the same defended runbook release.
- Use a general SUP ledger when the primary need is later evidence refinement for one admitted run verdict rather than a bounded repair packet.
- If the patch materially changes operator semantics, evidence admission rules, or ledger binding, stop and open a new source log plus a new runbook release instead of continuing under the same patch series.

## Required Rules

- Every patch ledger must point to one existing parent runbook release.
- When the patch is triggered by one run outcome, it should also point to one explicit `parent run row id`; use `pending` only when the repair is being fixed before the first admitted run exists.
- Every patch item must record one verification surface and one approval state.
- Patch ledgers may carry screenshots, transcripts, and rich attachments the same way SUP ledgers do.
- If a bounded repair is admitted under one patch ledger, the implementation changes, the patch ledger write-back, and any directly dependent sample/accounting write-back should ship in the same bounded patch commit packet rather than being split into a later standalone script or docs commit.

## Completion Rule

- A patch ledger may be marked `completed` only when every admitted patch item has one explicit `verification status`, one explicit `approval status`, and one explicit statement of whether the parent run ledger changed.