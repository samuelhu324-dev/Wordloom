# run-ledger-patch-template-v1

Use this patch ledger when one stable runbook release needs a bounded repair packet that should remain under the same runbook release instead of forcing a release bump.
This patch ledger is a support-only, supplement-class surface: it owns patch-level evidence admission, review, approval, and downstream write-back for one existing run, target, or target-stage repair surface inside one runbook family.

## Naming Rule

- Name patch ledgers as `ledger-run-PATCH-<patch-sequence>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- `ledger-run-PATCH-<patch-sequence>` is the fixed prefix and records the append-only patch round for one stable runbook release.
- `<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>` must match the bound runbook suffix exactly.
- Preferred example shape:
  - `ledger-run-PATCH-001-WORKFLOW-FAMILY-001-operator-surface.md`

## Minimal Header

```yaml
runbook_run_patch_ledger:
  patch_ledger_id: <ledger-run-PATCH-001-RUNBOOK-FAMILY-001-summary>
  patch_kind: runbook-run-ledger-patch
  status: <draft|active|completed>
  owner_lane: <S0G-3C>
  parent_runbook_id: <run-RUNBOOK-FAMILY-001-summary>
  parent_runbook_ref: <docs/runbook/run-RUNBOOK-FAMILY-001-summary.md>
  parent_run_ledger_id: <ledger-run-001-RUNBOOK-FAMILY-001-summary>
  parent_run_ledger_ref: <docs/runbook/support-only/ledger-run-001-RUNBOOK-FAMILY-001-summary.md>
  parent_run_row_id: <RUN-001|pending|not-yet-bound>
  parent_target_row_id: <RUN-001-T01|pending|not-applicable>
  parent_target_stage_row_id: <RUN-001-T01-STG-CREATION|pending|not-applicable>
  parent_target_stage_attempt_id: <RUN-001-T01-STG-CREATION-A01|not-used>
  target_ref_key: <S4F-2A>
  target_ref_path: <docs/logs/log-S4F-2A-...md>
  patch_sequence: <001>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  affected_bridge_ids:
    - <RB-01|none>
  affected_coverage_ids:
    - <SC-01|none>
  patch_scope: <what bounded repair this packet admits>
  patch_reason_class: <docs-fix|script-fix|manifest-fix|evidence-fix|mixed-bounded-repair>
  approval_boundary: <who must approve this patch before it may update ledgers, logs, or live artifacts>
  target_reading_goal: <what later readers should understand after this patch ledger is applied>
```

## Strong-Structure Bridge Rule

- Every PATCH packet must attach to one existing `parent_run_row_id` when the repair is triggered by or admitted against an existing batch.
- When the repair is target-specific, it must also attach to one existing `parent_target_row_id`.
- When the repair is stage-specific, it must also attach to one existing `parent_target_stage_row_id`.
- `parent_target_stage_attempt_id` is optional and should be used only when one repair truly belongs to a defended replay attempt below the stable stage row.
- Structural ids should stay sequence-only and machine-stable; semantic identity such as `S4F-2A` should stay in `target_ref_key` and `target_ref_path` rather than being embedded into the structural key itself.

## Patch Change Table

| patch item id | parent run row id | target row id | target stage row id | target stage attempt id | target artifact or path | change class | evidence refs | verification status | approval status | effect on current runbook release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<RUN-001|pending>` | `<RUN-001-T01|pending|not-applicable>` | `<RUN-001-T01-STG-CREATION|pending|not-applicable>` | `<RUN-001-T01-STG-CREATION-A01|not-used>` | `<artifact path|script path|doc path>` | `<docs-fix|script-fix|manifest-fix|evidence-fix|mixed-bounded-repair>` | `<artifact path|diff|screenshot path>` | `<pending|verified|rejected>` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<no-release-bump|candidate-release-bump-needs-log>` | `<no-change|append-patch-ref|rewrite-run-row|rewrite-target-row|rewrite-target-stage-row|open-sup-ledger>` | `<none|rerun-required|rewrite-source-log|rewrite-runbook-binding>` | `<why this patch matters>` |

## Patch-to-Ledger Action Rule

- Use `proposed parent-ledger action` to say exactly what the repair changes in the parent accounting surface:
  - `no-change`
  - `append-patch-ref`
  - `rewrite-run-row`
  - `rewrite-target-row`
  - `rewrite-target-stage-row`
  - `open-sup-ledger`
- Prefer `rewrite-target-stage-row` when the repair only changes one lifecycle-stage reading or replay result rather than the whole batch row.
- Use `open-sup-ledger` when the repair diff also requires a separate admitted-reading follow-up packet under `SUP`.
- If a repair is not yet bound to one admitted stage, keep the target-stage fields explicit with `pending` or `not-applicable`; do not silently drop the structural attachment columns.

## Attachment Review Table

| attachment id | patch item id | click-through asset ref | review status | approval basis | review note |
| --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01-ATT-01>` | `<PATCH-001-I01>` | `[open asset](./asset-name.png)` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<why this attachment is sufficient or insufficient>` | `<what the reviewer checked>` |

## Actor and Provenance Review Table

| patch item id | run row id | target row id | target stage row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<RUN-001|pending|not-yet-bound>` | `<RUN-001-T01|pending|not-applicable>` | `<RUN-001-T01-STG-CREATION|pending|not-applicable>` | `<unknown|pending|role:operator|name>` | `<unknown|pending|role:runbook-maintainer|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-artifact-inspection|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<why this approval state is defended>` | `<why any actor fields remain partial>` |

## Optional Patch Time Audit

| patch item id | run row id | target row id | target stage row id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<RUN-001|pending|not-yet-bound>` | `<RUN-001-T01|pending|not-applicable>` | `<RUN-001-T01-STG-CREATION|pending|not-applicable>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone note>` | `<why this patch time audit matters>` |

## Write-Back Chain Rule

- The repair chain is `repair evidence -> PATCH -> parent runbook object or parent run ledger reference -> downstream consumer`.
- Use `open-sup-ledger` whenever the bounded repair also changes admitted chronology or verdict meaning.
- Readers should be able to tell what changed by comparing the patch row, patch time audit, parent ledger row, and any downstream consumer updates.

## Bridge Rule

- A patch ledger is supplement-class and support-only, but it is not the same as a general SUP ledger.
- Use a patch ledger when the repair is bounded, runbook-bound, and still within the same defended runbook release.
- `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at` are required header fields; keep them present even when the defended value is still `unknown` or `pending`.
- `affected_bridge_ids` and `affected_coverage_ids` are optional reference lists for audited bridge/coverage write-back only; they must not replace the actual bridge or coverage semantics on the runbook or contract surfaces.
- Use a general SUP ledger when the primary need is later evidence refinement for one admitted run verdict rather than a bounded repair packet.
- Keep PATCH bindings on the same structural keys already used by the parent ledger and any related SUP packet; do not fall back to prose-only matching once run/target/stage ids exist.
- If the patch materially changes operator semantics, evidence admission rules, or ledger binding, stop and open a new source log plus a new runbook release instead of continuing under the same patch series.

## Required Rules

- Every patch ledger must point to one existing parent runbook release.
- When the patch is triggered by one run outcome, it should also point to one explicit `parent run row id`; use `pending` only when the repair is being fixed before the first admitted run exists.
- Every target-specific patch row should also point to one explicit `parent target row id`.
- Every stage-specific patch row should also point to one explicit `parent target stage row id`.
- Every patch item must record one verification surface and one approval state.
- Patch ledgers may carry screenshots, transcripts, and rich attachments the same way SUP ledgers do.
- Sequence ids in the PATCH file must match the stable structural keys already present in the parent ledger; do not replace them with prose-only target names.
- If a bounded repair is admitted under one patch ledger, the implementation changes, the patch ledger write-back, and any directly dependent sample/accounting write-back should ship in the same bounded patch commit packet rather than being split into a later standalone script or docs commit.

## Completion Rule

- A patch ledger may be marked `completed` only when every admitted patch item has one explicit structural attachment point, one explicit `verification status`, one explicit `approval status`, and one explicit statement of whether the parent run ledger changed.