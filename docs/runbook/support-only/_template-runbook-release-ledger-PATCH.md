# runbook-release-ledger-patch-template-v1

Use this patch ledger when one stable runbook release needs a bounded repair packet that should remain under the same release instead of forcing a release bump.
This surface is release-scoped and support-only.

## Naming Rule

- Name runbook release patch ledgers as `ledger-runbook-PATCH-<sequence>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`.
- Preferred example shape:
  - `ledger-runbook-PATCH-001-RUNTIME-OBSERVABILITY-001-release-ledger-bootstrap.md`

## Minimal Header

```yaml
runbook_release_patch_ledger:
  patch_ledger_id: <ledger-runbook-PATCH-001-RUNBOOK-FAMILY-001-summary>
  patch_kind: runbook-release-ledger-patch
  status: <draft|active|completed>
  owner_lane: <S4G-1G>
  parent_runbook_id: <run-RUNBOOK-FAMILY-001-summary>
  parent_runbook_ref: <docs/runbook/run-RUNBOOK-FAMILY-001-summary.md>
  parent_release_ledger_id: <ledger-runbook-RUNBOOK-FAMILY-001-summary>
  parent_row_id: <RBL-01|pending|not-applicable>
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
  patch_reason_class: <docs-fix|binding-fix|evidence-fix|mixed-bounded-repair>
  target_reading_goal: <what later readers should understand after this patch ledger is applied>
```

## Patch Change Table

| patch item id | parent row id | target artifact or path | change class | evidence refs | verification status | approval status | effect on current runbook release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<RBL-01|pending|not-applicable>` | `<docs/runbook/...>` | `<docs-fix|binding-fix|evidence-fix|mixed-bounded-repair>` | `<diff|log|other>` | `<pending|verified|rejected>` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<no-release-bump|candidate-release-bump-needs-log>` | `<no-change|append-patch-ref|rewrite-parent-row|open-sup-ledger>` | `<none|rewrite-runbook|rewrite-contract-bridge|defer>` | `<why this patch matters>` |

## Required Rules

- Use a runbook release patch only for bounded repair on the runbook release object itself.
- Do not use this surface for per-run execution repairs; those belong to `ledger-run-PATCH-*`.
- If the repair materially changes runbook semantics, stop and open a new source log plus a new runbook release instead of continuing under the same patch series.