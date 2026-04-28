# semantic-chronology-sharpening-ledger-template-v1

Use this ledger when historical material needs to be inserted, clarified, or re-ordered in semantic chronology without forcing the current contract snapshot to absorb that history directly.

## Naming Rule

- Name these ledgers as `ledger-SEMANTIC-CHRONOLOGY-SHARPENING-<CONTRACT-ID>-<summary>.md`.
- Preferred example shape:
  - `ledger-SEMANTIC-CHRONOLOGY-SHARPENING-DOC-RUNTIME-OBSERVABILITY-0001-proof-path-history.md`

## Minimal Header

```yaml
semantic_chronology_sharpening_ledger:
  chronology_ledger_id: <ledger-SEMANTIC-CHRONOLOGY-SHARPENING-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  ledger_kind: semantic-chronology-sharpening-ledger
  status: <draft|active|completed>
  owner_lane: <S0G-5B>
  target_contract_family: <DOC-DOMAIN-SUBDOMAIN>
  target_contract_id: <DOC-DOMAIN-SUBDOMAIN-0001|pending>
  target_contract_ref: <docs/governance/contracts/...md>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  chronology_scope: <what semantic history is being sharpened>
  target_reading_goal: <what later readers should understand after chronology sharpening>
```

## Lifecycle Field Rule

- `created_at`, `reviewed_at`, and `accepted_at` are packet-lifecycle fields only.
- Preserve `effective_from`, `observed_at`, and `recorded_at` at the weakest defended precision supported by source material.

## Chronology Candidate Table

| chronology candidate id | face id | change type | semantic before | semantic after | effective from | effective until | observed at | recorded at | actor | basis refs | source release rows | source scenario rows | source routing event ids | proposed chronology order key | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<SCH-01>` | `<DOC-...-FACE-01>` | `<introduced|clarified|narrowed|widened|split|superseded|backfilled-audit>` | `<previous semantic or none>` | `<new semantic row>` | `<YYYY-MM-DD|unknown>` | `<YYYY-MM-DD|ongoing|unknown>` | `<YYYY-MM-DD|unknown>` | `<YYYY-MM-DD|unknown|pending>` | `<role or unknown>` | `<stable source anchors>` | `<CRL-01|none>` | `<CRL-02-SC-01|none>` | `<CRL-02-SC-E01|none>` | `<effective_from|observed_at|recorded_at|id>` | `<bounded chronology note>` |

## Insertion Point Table

| chronology candidate id | predecessor row | successor row | insertion verdict | justification | writeback impact | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `<SCH-01>` | `<existing chronology id|start>` | `<existing chronology id|end>` | `<insert-before|insert-after|replace-order-key-only|retain-outside-current-contract>` | `<why this insertion point is correct>` | `<append-current-contract-chronology|retain-in-ledger-only|needs-more-evidence>` | `<bounded insertion note>` |

## Chronology Writeback Decision Table

| chronology candidate id | changes current semantic snapshot | chronology-only writeback | current contract action | notes |
| --- | --- | --- | --- | --- |
| `<SCH-01>` | `<yes|no>` | `<required|optional|not-applicable>` | `<no-release|same-release-evidence-writeback|new-release-required|retain-in-ledger-only>` | `<bounded writeback note>` |

## Required Rules

- Use this ledger when the open question is `how should historical semantic rows be inserted or sharpened in time order?`
- Do not overload the current contract face table with historical narrative that belongs in chronology.
- `chronology_order_key` should be sortable without depending only on release id.

## Completion Rule

- A chronology sharpening ledger may be marked `completed` only when every chronology candidate row has one explicit insertion verdict and one explicit current-contract action.