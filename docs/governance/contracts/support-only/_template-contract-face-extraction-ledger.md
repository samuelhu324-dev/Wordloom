# contract-face-extraction-ledger-template-v1

Use this ledger when code-first or evidence-first review needs one bounded staging surface for candidate contract faces before any current contract release is rewritten.

## Naming Rule

- Name these ledgers as `ledger-CONTRACT-FACE-EXTRACTION-<CONTRACT-ID>-<summary>.md`.
- Preferred example shape:
  - `ledger-CONTRACT-FACE-EXTRACTION-DOC-RUNTIME-OBSERVABILITY-0001-search-outbox-worker-face-intake.md`

## Minimal Header

```yaml
contract_face_extraction_ledger:
  extraction_ledger_id: <ledger-CONTRACT-FACE-EXTRACTION-DOC-DOMAIN-SUBDOMAIN-0001-summary>
  ledger_kind: contract-face-extraction-ledger
  status: <draft|active|completed>
  owner_lane: <S0G-5B>
  target_contract_family: <DOC-DOMAIN-SUBDOMAIN>
  target_contract_id: <DOC-DOMAIN-SUBDOMAIN-0001|pending>
  target_contract_ref: <docs/governance/contracts/...md>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  extraction_scope: <what bounded current-semantic faces are being extracted>
  target_reading_goal: <what later readers should understand after this extraction ledger is applied>
```

## Lifecycle Field Rule

- `created_at`, `reviewed_at`, and `accepted_at` are packet-lifecycle fields only.
- Preserve weaker source chronology in the tables below rather than copying stronger packet times into semantic fields.

## Face Candidate Table

| face candidate id | face name | candidate semantic status | candidate semantic strength | candidate semantic text | code truth kind | primary code refs | supporting refs | source basis | release impact hint | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<FCE-01>` | `<owner-boundary>` | `<owned-now|partially-owned|boundary-only|not-owned-here>` | `<code-observed|code-anchored|evidence-supported|defended-now|historically-retained|superseded>` | `<current-semantic candidate>` | `<entrypoint|domain-flow|config-switch|schema-shape|signal-emission|verification-hook|mixed>` | `<repo refs>` | `<logs/labs/runbook/ledger refs>` | `<stable packet ids or anchors>` | `<same-release-evidence-writeback|new-release-required|move-to-runbook|pending>` | `<bounded extraction note>` |

## Supporting Evidence Table

| evidence item id | face candidate id | evidence kind | repo ref | symbol or block | observed semantic | confidence | observed at | recorded at | source packet or ledger | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<FCE-E01>` | `<FCE-01>` | `<entrypoint|domain-flow|config-switch|schema-shape|signal-emission|verification-hook>` | `<backend/...>` | `<symbol name or bounded block>` | `<what was observed>` | `<high|medium|low>` | `<YYYY-MM-DD|unknown>` | `<YYYY-MM-DD|unknown|pending>` | `<source packet>` | `<bounded evidence note>` |

## Pre-Writeback Release Decision Table

| face candidate id | current release semantic | candidate semantic | delta class | reader visible change | proposed contract action | target release or outlet | decision basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<FCE-01>` | `<current text or none>` | `<candidate text>` | `<evidence-only|clarification-only|semantic-change|boundary-restructure>` | `<yes|no>` | `<no-release|same-release-evidence-writeback|new-release-required|split-family-required|move-to-runbook|retain-in-chronology-only>` | `<DOC-...-0001|DOC-...-0002|runbook|chronology-only>` | `<why this action is justified>` | `<bounded release note>` |

## Actor and Provenance Review Table

| face candidate id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<FCE-01>` | `<unknown|pending|role:packet-maintainer|name>` | `<unknown|pending|role:evidence-owner|name>` | `<unknown|pending|role:workflow-reviewer|name>` | `<unknown|pending|role:evidence-verifier|name>` | `<direct-markdown-inspection|source-path-check|manual-replay|other>` | `<unknown|pending|role:approver|name>` | `<pending|accepted-for-writeback|needs-better-evidence|rejected>` | `<why this state is defended>` | `<why any actor values remain partial>` |

## Required Rules

- Use this ledger when the intake question is `what are the candidate current contract faces and what code facts support them?`
- Do not write current contract prose directly from raw code observations without first deciding the release action per face candidate.
- Keep code facts and current semantic candidates in separate tables so evidence does not silently become contract meaning.

## Completion Rule

- A face extraction ledger may be marked `completed` only when every face candidate row has one explicit release-impact hint or proposed contract action.