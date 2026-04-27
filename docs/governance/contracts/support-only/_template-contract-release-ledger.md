# contract-release-ledger-template-v1

Use this ledger when one stable contract release needs a durable, release-first intake surface for evidence, clause routing, bridge or coverage write-back, and later archaeology.
This ledger is centered on the contract object itself. It complements, and does not replace, source-owned routing ledgers.

## Naming Rule

- Name contract release ledgers as `ledger-<CONTRACT-ID>-<summary>.md`.
- The summary should normally match the bound contract filename suffix exactly.
- Preferred example shape:
  - `ledger-DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`

## Minimal Header

```yaml
contract_release_ledger:
  ledger_id: <ledger-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  ledger_kind: contract-release-ledger
  status: <draft|active|completed>
  owner_lane: <S4G-1G>
  contract_family: <DOC-DOMAIN-SUBDOMAIN>
  contract_release: <0001>
  contract_id: <DOC-DOMAIN-SUBDOMAIN-0001>
  contract_ref: <docs/governance/contracts/...md>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  source_of_authority:
    - <source ledger or source log anchor>
  target_reading_goal: <what later readers should understand after this ledger is applied>
```

## Intake and Write-Back Table

| row id | evidence anchor | evidence class | semantic area | intended landing surface | current verdict | affected statement ids | affected bridge ids | affected coverage ids | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<CRL-01>` | `<log/code/labs/runbook anchor>` | `<source-ledger|source-log|code|labs|runbook|mixed>` | `<clause intake|bridge intake|coverage note|boundary note|other>` | `<statement-table|code-bridge-table|coverage-table|release-change|defer>` | `<applied-current-release|pending-classification|deferred|rejected>` | `<DOC-...-ST-01|none>` | `<DOC-...-CB-01|none>` | `<DOC-...-COV-01|none>` | `<why this intake matters>` |

## Actor and Provenance Review Table

| row id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<CRL-01>` | `<unknown|pending|role:contract-maintainer|name>` | `<unknown|pending|role:evidence-owner|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-markdown-inspection|source-path-check|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-ledger|needs-better-evidence|rejected>` | `<why this state is defended>` | `<why any actor values remain partial>` |

## Required Rules

- Use this ledger when the question is `how should this contract release absorb, defer, or reject new release-scoped evidence?`
- Source-owned ledgers still own source slicing and initial routing; do not bypass them when the unresolved question is still source structure.
- Contract release ledgers are the correct landing surface when the new evidence comes from code, labs, retained runbooks, or other strong-structure channels and the target is an existing contract release.
- Keep clause, bridge, and coverage mutation deferred in the contract body until the ledger verdict is explicit.

## Completion Rule

- A contract release ledger may be marked `completed` only when every intake row has one explicit current verdict and one explicit intended landing surface.