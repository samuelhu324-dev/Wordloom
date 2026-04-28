# run-ledger-patch-template-WORKFLOW-GITHUB-ISSUES-v1

Use this template for bounded repairs inside the active `WORKFLOW-GITHUB-ISSUES` release when no release bump is justified.

## Minimal Header

```yaml
runbook_run_patch_ledger:
  patch_ledger_id: <ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-summary>
  patch_kind: runbook-run-ledger-patch
  status: <draft|active|completed>
  owner_lane: <S0G-3E>
  parent_runbook_id: <run-WORKFLOW-GITHUB-ISSUES-001-summary>
  parent_runbook_ref: <docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-summary.md>
  parent_run_ledger_id: <ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-summary>
  parent_run_ledger_ref: <docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-summary.md>
  parent_run_row_id: <RUN-001|pending>
  parent_target_row_id: <RUN-001-T01|pending|not-applicable>
  parent_target_stage_row_id: <RUN-001-T01-STG-CREATION|pending|not-applicable>
  parent_target_stage_attempt_id: <RUN-001-T01-STG-CREATION-A01|not-used|pending>
  patch_sequence: <001>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  affected_bridge_ids:
    - <RB-ISSUES-01|none>
  affected_coverage_ids:
    - <SC-ISSUES-01|none>
  patch_scope: <what bounded repair is admitted>
  patch_reason_class: <docs-fix|script-fix|manifest-fix|evidence-fix|mixed-bounded-repair>
  target_reading_goal: <what later readers should understand>
```

## Lifecycle Field Rule

- `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at` are required header fields; keep them present even when the defended value is still `unknown` or `pending`.
- `affected_bridge_ids` and `affected_coverage_ids` are optional reference lists for audited bridge/coverage write-back only; they must not replace the actual bridge or coverage semantics on the runbook or contract surfaces.

## Patch Time Audit

| patch item id | parent run row id | target row id | target stage row id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<RUN-001>` | `<RUN-001-T01|not-applicable>` | `<RUN-001-T01-STG-CREATION|not-applicable>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<second|day|month|year|unknown>` | `<optional source-local zone note>` | `<why this patch time audit matters>` |

## Patch Packet Summary

| patch ledger id | patch sequence | parent run row id | repair scope | packet verdict | current release effect | admitted chronology effect | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001>` | `<001>` | `<RUN-001>` | `<issue draft milestone override and PR-prep preview-path repair>` | `<completed>` | `<no-release-bump>` | `<no-direct-chronology-change>` | `<optional>` |

## Repair Delta Table

| patch item id | target artifact or path | repair class | prior defect reading | new defended repair reading | effect on admitted chronology | requires paired SUP? | paired SUP ref | parent-ledger writeback | primary evidence ref | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<script path>` | `<script-fix>` | `<operator flow failed closed or mis-shaped bounded repair surface>` | `<bounded repair now completes with defended guardrails retained>` | `<no-direct-chronology-change>` | `<no>` | `<not-required>` | `<append-patch-ref>` | `<artifact path>` | `<optional>` |

## Patch Change Table

| patch item id | parent run row id | target row id | target stage row id | target stage attempt id | target artifact or path | change class | verification status | effect on current runbook release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<RUN-001>` | `<RUN-001-T01|not-applicable>` | `<RUN-001-T01-STG-CREATION|not-applicable>` | `<not-used>` | `<script path>` | `<script-fix>` | `<verified>` | `<no-release-bump>` | `<append-patch-ref|open-sup-ledger>` | `<optional>` | `<optional>` |

## Family-specific Rules

- PATCH remains repair-first. It should not become an execution round by itself unless the parent ledger explicitly admits a changed chronology reading because of that repair.
- If a repair changes the admitted reading of one run, target, or stage, pair the PATCH packet with the corresponding SUP write-back.
- Keep the same stable structural ids already used by the parent ledger.
- `Repair Delta Table` should explain whether a repair changes admitted chronology directly, only enables a later `SUP`, or stays purely local to the repair packet.
- Keep `Patch Change Table` focused on implementation/evidence review and approval support rather than carrying the full before/after repair explanation by itself.

## Write-Back Chain Rule

- The family repair chain is `repair evidence -> family PATCH -> parent runbook object or parent run ledger reference -> downstream consumer`.
- `Repair Delta Table` explains semantic effect; `Patch Time Audit` explains when the repaired signal was observed, recorded, and effective.
- If chronology meaning changes, the paired `SUP` packet owns the admitted-reading delta while the PATCH row keeps the bounded repair trace.