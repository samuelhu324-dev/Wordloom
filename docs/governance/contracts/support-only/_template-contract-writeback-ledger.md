# contract-writeback-ledger-template-v1

Use this ledger when candidate face, evidence, and chronology changes have already been extracted and the remaining question is exactly what should be written back to the current contract release, a new release, or another outlet.

## Naming Rule

- Name these ledgers as `ledger-CONTRACT-WRITEBACK-<CONTRACT-ID>-<summary>.md`.
- Preferred example shape:
  - `ledger-CONTRACT-WRITEBACK-DOC-RUNTIME-OBSERVABILITY-0001-face-and-chronology-writeback.md`

## Minimal Header

```yaml
contract_writeback_ledger:
  writeback_ledger_id: <ledger-CONTRACT-WRITEBACK-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  ledger_kind: contract-writeback-ledger
  status: <draft|active|completed>
  owner_lane: <S0G-5B>
  target_contract_family: <DOC-DOMAIN-SUBDOMAIN>
  current_contract_id: <DOC-DOMAIN-SUBDOMAIN-0001>
  current_contract_ref: <docs/governance/contracts/...md>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_started_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_completed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  writeback_scope: <what current contract mutations are being decided>
  target_reading_goal: <what later readers should understand after the writeback decision>
```

## Lifecycle Field Rule

- `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, and `writeback_completed_at` are packet-lifecycle fields only.
- Keep semantic-effective timing on the contract or chronology rows themselves.

## Face Writeback Table

| writeback item id | face id | current semantic | candidate semantic | delta class | reader visible change | contract action | target release or outlet | writeback status | basis refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<CWB-01>` | `<DOC-...-FACE-01>` | `<current face text>` | `<candidate face text>` | `<evidence-only|clarification-only|semantic-change|boundary-restructure>` | `<yes|no>` | `<no-release|same-release-evidence-writeback|new-release-required|split-family-required|move-to-runbook|retain-in-chronology-only>` | `<DOC-...-0001|DOC-...-0002|runbook|chronology-only>` | `<planned|applied|deferred|rejected>` | `<stable ids or packet refs>` | `<bounded writeback note>` |

## Chronology Writeback Table

| chronology item id | face id | chronology action | target chronology row | writeback status | basis refs | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `<CWB-CHR-01>` | `<DOC-...-FACE-01>` | `<append|replace-order-key|retain-outside-current-contract>` | `<DOC-...-CHR-01|pending>` | `<planned|applied|deferred|rejected>` | `<chronology packet refs>` | `<bounded chronology writeback note>` |

## Approval and Provenance Review Table

| writeback item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<CWB-01>` | `<unknown|pending|role:packet-maintainer|name>` | `<unknown|pending|role:evidence-owner|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-markdown-inspection|source-path-check|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-writeback|needs-better-evidence|rejected>` | `<why this state is defended>` | `<why any actor values remain partial>` |

## Write-Back Chain Rule

- Default chain: `face extraction and chronology sharpening -> contract writeback ledger -> current contract or new release`.
- Use this ledger to decide whether the packet mutates the current release, opens a new release, or routes the material elsewhere.
- Do not hide `new-release-required` verdicts inside same-release wording cleanup.

## Completion Rule

- A contract writeback ledger may be marked `completed` only when every writeback item has one explicit `contract action` and one explicit `writeback status`.