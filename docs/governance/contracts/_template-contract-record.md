# governance-contract-record-template

```yaml
contract_record:
  contract_family: <stable-governance-family-id>
  contract_release: <0001|0002|...>
  contract_id: <contract_family-contract_release>
  record_kind: chronology-first-contract
  status: <draft|active|deprecated|superseded|retired>
  release_action: <initial|simple-revision|merge|split-parent|split-child|absorption|consolidation>
  release_change_summary: <why this release exists and what materially changed>
  summary: <effective contract meaning at this contract state>
  governance_area: <governed area>
  applies_to: <targets governed by this contract>
  enforcement_surface: <workflow|script|runbook|adapter|manual>
  violation_semantics: <fail|warning|report-only|neutral>
  recorded_at: <YYYY-MM-DD|unknown>
  reviewed_at: <YYYY-MM-DD|pending>
  effective_from: <YYYY-MM-DD|unknown>
  effective_until: <YYYY-MM-DD|ongoing|unknown>
  introduced_by: <first source anchor>
  last_changed_by: <most recent source anchor>
  source_refs:
    - <direct decisive source reference for this release>
  cumulative_source_refs:
    - <all source refs carried forward into this family's current release state>
  supporting_evidence_refs:
    - <optional retained chronology or validation evidence>
  lineage:
    supersedes:
      - <optional earlier release id replaced by this release>
    superseded_by:
      - <optional later release id that replaces this release>
    split_from:
      - <optional broader earlier release id if this record is a split child>
    split_into:
      - <optional narrower later release id if this record later splits>
    absorbed_from:
      - <optional earlier release id whose meaning is partly absorbed here>
    absorbed_into:
      - <optional later release id that absorbs meaning from this record>
    retires:
      - <optional earlier release id explicitly ended by this record>
    retired_by:
      - <optional later release id or decision that retires this record>
  notes:
    - <optional clarification>
```

## Guidance

- Keep `contract_family` semantic and stable; do not encode slice IDs, run IDs, or implementation filenames into it.
- Canonical chronology-first `contract_family` values should use one long-path grammar rather than opaque short abbreviations:
  - `DOC-<DOMAIN>-<SUBDOMAIN>-...-<CATEGORY>`
  - Example family shapes: `DOC-WORKFLOW-GITHUB-ISSUES`, `DOC-WORKFLOW-GITHUB-ISSUES-TITLE`, `DOC-WORKFLOW-GITHUB-ISSUES-TAGS`
- `contract_release` is the fixed-width release counter inside one stable family.
- `contract_id` should therefore read as `<contract_family>-<contract_release>`, for example `DOC-WORKFLOW-GITHUB-ISSUES-0001`.
- The category path inside `contract_family` should stay human-readable enough that readers can understand the contract family without opening a separate glossary.
- Keep the file title or filename summary readable, but treat `contract_family` as the stable semantic identity and `contract_id` as one specific release record.
- Use this template only when the record is the clearest owner of one governance rule or boundary state in chronology-first rebuild.
- Do not use this template for rows that are only validation evidence, migration mechanics, wrapper transport, or chronology support without primary rule ownership.
- `release_action` should state how this release relates to earlier releases, such as `initial`, `simple-revision`, `merge`, `split-child`, `split-parent`, or `absorption`.
- `contract_release` remains append-only registry order inside one family; it should not be treated as guaranteed historical-effective order.
- `recorded_at` should capture when this release record entered the repo as one defended contract record.
- `reviewed_at` should capture when this release record passed its current defended review state; use `pending` when that review has not happened yet.
- `effective_from` and `effective_until` should capture the best currently known historical-effective range for the rule state owned by this release.
- `release_change_summary` should explain why this release exists; it is especially required when `contract_release` is later than `0001` or when lineage fields are non-empty.
- `summary` should describe the effective rule meaning at this contract state, not the full change history.
- `source_refs` should stay minimal and point only to the decisive sources that justify this release itself.
- `cumulative_source_refs` should carry forward all source material that remains materially present in this family's current release state; later releases should not silently shrink this history.
- `supporting_evidence_refs` may capture retained evidence that helps verify chronology without promoting every evidence row into a contract.
- Use `notes` or a nearby prose section to make the human-readable distinction explicit when a contract is functioning as either:
  - one `parent contract` that owns mechanism introduction, `why`, and boundary
  - one `child contract` that owns one independently judgeable narrow rule body beneath that parent
- Use `supersedes` / `superseded_by` at the release level; one later release may supersede one or more earlier releases when it becomes the clearer effective reader surface.
- Use `split_from` / `split_into` only when one broader release decomposes into narrower children that each own one independently judgeable part of the earlier broader rule body.
- A split parent may later read as an earlier broader state while its children become the narrower current readers; split does not require many children, only a real decomposition boundary.
- Use `absorbed_from` / `absorbed_into` when rule meaning is carried forward into another release without a pure whole-rule replacement.
- Do not use lineage fields to describe how issue-only, log-only, or support-only source slices were routed; record that work in the support-only ledger.
- Use `retires` / `retired_by` when a release state ends explicitly without one clean direct successor.
- `notes` may clarify operator context, but should never override structured fields.

## Recommended Body Shape

- Keep the prose body readable as both `what changed in this release` and `what the current effective state now is`.
- When one contract family is likely to evolve through repeated clause-level amendment, consider adding one `## Contract Statement Table` ahead of the readable prose body so each effective clause has one stable statement id and one explicit source-basis anchor.
- Preferred section order:
  - `## Contract Statement Table` (optional but recommended when clause-level traceability matters)
  - `## Release Change`
  - `## Contract Statement`
  - `## Current Reading`
  - `## Reader Notes`
- `## Release Change` should summarize the material delta for this release, especially when `contract_release` is later than `0001`.
- `## Contract Statement` should restate the current effective rule meaning in full; do not force readers to reconstruct the current state by diffing against earlier releases.
- When one later release absorbs new non-contract source material, mention that source carry-forward in `## Release Change`, while keeping release-to-release relationships in `lineage` and source-routing details in the support-only ledger.

## Optional Contract Statement Table

- Use this section when the release needs clause-level identity and carry-forward tracking without turning the contract itself into a source-owned ledger.
- Recommended statement-id naming:
  - `<contract_id>-ST-<nn>`
- Statement ids are release-local:
  - later releases should mint new statement ids under the later `contract_id`
  - do not reuse earlier-release statement ids as the current ids for a later release
  - carry-forward, amendment, split, merge, or replacement relationships should be recorded through the statement-evolution surface
- Recommended columns:
  - `statement id`
  - `statement label`
  - `clause status`
  - `change action`
  - `source basis`
  - `first effective release`
  - `first effective at`
  - `last changed release`
  - `last changed at`
  - `effective from`
  - `effective until`
  - `effective status`
  - `statement text`
  - `notes`
- `statement label` should be a short human-readable clause title for the current contract meaning; it is the contract-facing quick label, not a copy of the source-owned `source slice` field from the ledger.
- `source basis` may contain one or more stable anchors when the clause truly depends on multiple upstream bases.
- `first effective at` should capture the best currently known historical time at which the clause first became effective, independent of the append-only registry release number.
- `last changed at` should capture the best currently known historical time for the latest semantic change represented in this release's reading of the clause.
- `effective from` and `effective until` should capture the active historical range for the clause as currently read in this release; use `ongoing` when the clause remains in force without a known end date.
- `source basis` should prefer stable ledger or supplement anchors such as:
  - one `parent row id` such as `S0B-1A-R02`
  - one `supplement item id` such as `S0A-1A-R02-SUP-01`
  - one earlier `statement id` when the current clause is carried forward or amended from an earlier release
- `source basis` is evidence-facing only:
  - use stable ids rather than raw file paths
  - reserve the field for directly decisive anchors rather than general supporting evidence
  - do not use the field to encode statement lineage, split/merge causality, or release-to-release replacement logic
  - when multiple anchors are needed, a plain semicolon-delimited shape such as `S0B-1A-R02; S0B-1A-R03` is recommended for Markdown tables
- Recommended `clause status` values:
  - `active`
  - `superseded`
  - `retired`
  - `conflicted-review`
- Recommended `change action` values:
  - `introduced`
  - `carried-forward`
  - `amended`
  - `replaced`
  - `split`
  - `merged`
- Recommended `effective status` values:
  - `in-force`
  - `no-longer-in-force`
  - `pending-review`
- Recommended ordering for the current `Contract Statement Table`:
  - sort by `first effective release` ascending so clauses with older semantic origins appear earlier
  - when `first effective release` is the same and reliable `first effective at` values exist, sort by `first effective at` ascending
  - when `first effective release` is the same, sort `change action` as `carried-forward`, then `amended`, then `introduced`
  - after that, keep one reader-friendly order inside each action bucket rather than forcing purely lexical id ordering
- The contract statement table does not replace source routing or supplement admission:
  - the parent ledger still owns source slicing and routing verdicts
  - the supplement ledger still owns later evidence admission and write-back recommendations
  - the contract statement table only tracks the effective clause state inside one contract release

## Optional Statement Evolution Table

- Use this section when statement-level split, merge, replacement, retirement, or carry-forward history needs to remain readable without overloading `source basis`.
- Recommended change-id naming:
  - `<contract_id>-CH-<nn>`
- Recommended columns:
  - `change id`
  - `release id`
  - `change action`
  - `input statement ids`
  - `output statement ids`
  - `effective at`
  - `recorded at`
  - `reason`
  - `source basis`
  - `notes`
- Recommended `change action` values:
  - `introduced`
  - `amended`
  - `replaced`
  - `split`
  - `merged`
  - `retired`
  - `carried-forward`
- In this table:
  - `input statement ids` and `output statement ids` carry statement lineage and causality
  - `effective at` records when the change is believed to have become historically effective
  - `recorded at` records when that change event was entered into the repo's chronology record
  - `source basis` still carries only the decisive evidence anchors for the change event
  - release-level lineage remains in contract frontmatter rather than moving into clause history tables

## Optional Legacy Redirect

- Use this only when the record is intentionally stored as non-active history and readers still need a deterministic path to the current interpretation.
- Keep this section near the top of the file, immediately after the YAML block.
- The section should state:
  - current standing such as `deprecated`, `superseded`, or `retired`
  - the lineage verb such as `absorbed into`, `split into`, or `superseded by`
  - the current release record or records a reader should consult now, if any
- Example shape:

```md
## Legacy Redirect

- Current standing:
  - `deprecated`
- Lineage:
  - `absorbed into DOC-WORKFLOW-LABS-0002`
- Read now:
  - `DOC-WORKFLOW-LABS-0002`
```

## Qualification Rule

- Treat a source-owned item as a chronology-first contract only when its primary historical result is one of these:
  - it introduces a new governance rule or decision state
  - it materially changes an existing governance rule or decision state
  - it stabilizes one governance boundary strongly enough that later history should read it as a named contract state
- Treat a source-owned item as evidence-only or lineage-support history when it mainly validates, packages, transports, audits, or narrates a rule whose clearest meaning lives elsewhere.