# contract-release-ledger-patch-template-v1

Use this patch ledger when one stable contract release needs a bounded repair packet that should remain under the same release instead of forcing a new release.

## Naming Rule

- Name contract release patch ledgers as `ledger-PATCH-<sequence>-<CONTRACT-ID>-<summary>.md`.
- Preferred example shape:
  - `ledger-PATCH-001-DOC-RUNTIME-OBSERVABILITY-0001-release-ledger-bootstrap.md`

## Minimal Header

```yaml
contract_release_patch_ledger:
  patch_ledger_id: <ledger-PATCH-001-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  patch_kind: contract-release-ledger-patch
  status: <draft|active|completed>
  owner_lane: <S4G-1G>
  parent_contract_id: <DOC-DOMAIN-SUBDOMAIN-0001>
  parent_contract_ref: <docs/governance/contracts/...md>
  parent_release_ledger_id: <ledger-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  parent_row_id: <CRL-01|pending|not-applicable>
  patch_sequence: <001>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  affected_statement_ids:
    - <DOC-...-ST-01|none>
  affected_bridge_ids:
    - <DOC-...-CB-01|none>
  affected_coverage_ids:
    - <DOC-...-COV-01|none>
  patch_scope: <what bounded repair this packet admits>
  patch_reason_class: <docs-fix|binding-fix|evidence-fix|mixed-bounded-repair>
  target_reading_goal: <what later readers should understand after this patch ledger is applied>
```

## Patch Change Table

| patch item id | parent row id | target artifact or path | change class | evidence refs | verification status | approval status | effect on current contract release | proposed parent-ledger action | downstream impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<PATCH-001-I01>` | `<CRL-01|pending|not-applicable>` | `<docs/governance/contracts/...>` | `<docs-fix|binding-fix|evidence-fix|mixed-bounded-repair>` | `<diff|log|other>` | `<pending|verified|rejected>` | `<pending|accepted-for-patch|needs-better-evidence|rejected>` | `<no-release-bump|candidate-release-bump-needs-log>` | `<no-change|append-patch-ref|rewrite-parent-row|open-sup-ledger>` | `<none|rewrite-current-draft|open-new-release|defer>` | `<why this patch matters>` |

## Required Rules

- Use a contract release patch only for bounded repair on the contract release object itself.
- Do not use this surface to bypass a new release when semantic contract meaning materially changes.