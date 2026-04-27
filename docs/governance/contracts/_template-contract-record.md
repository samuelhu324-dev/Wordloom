# governance-contract-record-template

```yaml
contract_record:
  contract_family: <stable-governance-family-id>
  contract_release: <0001|0002|...>
  contract_id: <contract_family-contract_release>
  record_kind: chronology-first-contract
  status: <draft|active|deprecated|superseded|retired>
  release_action: <initial|simple-revision|merge|split-parent|split-child|absorption|consolidation|historical-backfill>
  release_change_summary: <why this release exists and what materially changed>
  summary: <effective contract meaning at this contract state>
  governance_area: <governed area>
  applies_to: <targets governed by this contract>
  enforcement_surface: <workflow|script|runbook|adapter|manual>
  violation_semantics: <fail|warning|report-only|neutral>
  owner_team: <docs-governance|ops-runtime|delegated team>
  current_steward: <role:contract-maintainer|delegated:contract-maintainer|other>
  approval_state: <draft|review-pending|reviewed-awaiting-approval|approved|retired>
  reviewed_by: <role:workflow-reviewer|pending|unknown>
  approved_by: <role:docs-governance-approver|pending|unknown>
  release_ledger_binding:
    parent_release_ledger: <docs/governance/contracts/support-only/ledger-DOC-DOMAIN-SUBDOMAIN-0001-summary.md>
    supplementary_ledger_series: <docs/governance/contracts/support-only/ledger-SUP-001-DOC-DOMAIN-SUBDOMAIN-0001-summary.md>
    patch_ledger_series: <docs/governance/contracts/support-only/ledger-PATCH-001-DOC-DOMAIN-SUBDOMAIN-0001-summary.md>
    intended_use: <release-scoped evidence intake and staged clause/bridge/coverage write-back>
  recorded_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  effective_from: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>
  effective_until: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>
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
- `release_action` should state how this release relates to earlier releases, such as `initial`, `simple-revision`, `merge`, `split-child`, `split-parent`, `absorption`, or `historical-backfill`.
- When one later current release temporarily carries earlier-discovered history without opening a separate backfill release yet, keep `release_action` tied to the release-level relationship and mark the clause-level rows or change events as `history-backfilled` instead.
- `contract_release` remains append-only registry order inside one family; it should not be treated as guaranteed historical-effective order.
- `recorded_at` should capture when this release record entered the repo as one defended contract record.
- `reviewed_at` should capture when this release record passed its current defended review state; use `pending` when that review has not happened yet.
- `effective_from` and `effective_until` should capture the best currently known historical-effective range for the rule state owned by this release.
- `recorded_at`, `reviewed_at`, `effective_from`, and `effective_until` are required fields in every contract record; when a defended value is not known yet, keep the field present and use `unknown`, `pending`, or `ongoing` rather than omitting it.
- Treat `recorded_at` and `reviewed_at` as artifact/chronology fields, not as substitutes for the contract's semantic-effective window.
- Unless stronger evidence proves an earlier or later start, a first release should default `effective_from` to the decisive source log's `created` time.
- Unless one defended successor, replacement, retirement, or explicit end-state is known, `effective_until` should default to `ongoing`.
- If one parent ledger or SUP packet later records acceptance or write-back chronology for the same source slice, treat that later ledger chronology as evidence-routing timing only unless it also defends a different source-side effective start.
- New artifact-lifecycle and recorded-chronology values should prefer canonical UTC second timestamps such as `2026-04-12T15:18:05Z`.
- Legacy day-only values may remain where older records do not yet have defended second-level audit timestamps.
- Historical-effective fields may legitimately stay at date precision when the source proves only the date; do not fabricate seconds to force format symmetry.
- When the source proves only lifecycle dates and no narrower effective event, reuse that defended date precision for `effective_from` rather than inventing a finer timestamp.
- If a later correction is needed, update the source-side or ledger/SUP evidence first and then revise the contract from that defended upstream change rather than patching `effective_from` in isolation.
- If a local-time display is needed for operators or reviewers, keep it as a mirror field or prose note rather than replacing the canonical UTC value.
- Use `historical-backfill` when a later-recorded release documents an earlier historical state discovered only after newer family releases already exist.
- A `historical-backfill` release must not trigger renumbering of already-admitted later family releases; the earlier state enters the family by new append-only registry id plus explicit lineage.
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
- When a later-recorded earlier state is admitted through `historical-backfill`, update the minimum lineage set rather than rewriting every neighboring release body immediately:
  - the backfilled release should name at least one nearest later relationship through `superseded_by`, `absorbed_into`, `split_into`, or `retired_by` unless it is still the current effective reader
  - the nearest later affected release should eventually add the reciprocal back-link through `supersedes`, `absorbed_from`, `split_from`, or `retires`
  - if the earlier state changes current clause history in one later release, update the later release's clause metadata or evolution rows, but do not renumber the family
- `notes` may clarify operator context, but should never override structured fields.

## Governance State Rule

- `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by` are the current-state governance fields for the contract surface itself.
- Keep these fields on the contract whenever the contract is a live reader surface rather than only a retained historical note.
- These fields are required in the record frontmatter; when the actor or state is not yet defended, keep the field present and use `pending` or `unknown` rather than dropping it.

## Release Ledger Binding Rule

- Use `release_ledger_binding` when one contract release needs its own durable release-first intake surface for evidence admission, clause routing, bridge/coverage write-back, or later supplements and patches that are centered on the contract object rather than on a source log.
- `release_ledger_binding` complements source-owned ledgers instead of replacing them:
  - source-owned ledgers still own source slicing and primary routing from logs/issues/support-only material;
  - contract release ledgers own contract-object intake, staged write-back, and later release-bound refinements once material is already justified for this contract family.
- Prefer a contract release ledger when new evidence is being extracted from code, labs, retained runbooks, or other strong-structure channels and the needed question is `how should this existing contract release absorb, defer, or reject it?`
- Do not use `release_ledger_binding` to bypass a still-required source-owned routing ledger when the real unresolved problem is source slicing rather than contract write-back.

## Recommended Body Shape

- Keep the prose body readable as both `what changed in this release` and `what the current effective state now is`.
- When one contract family is likely to evolve through repeated clause-level amendment, consider adding one `## Contract Statement Table` ahead of the readable prose body so each effective clause has one stable statement id and one explicit source-basis anchor.
- When the current reader problem is `which broad parent clauses are still owned here versus only summarized here while narrower child readers now exist`, consider adding one parent-only `## Current Boundary Map` after the statement table.
- When the current reader problem is instead `why earlier-history rows and later-family rows coexist in one narrow current reader`, prefer one brief `## Current Reader Shape` explanation rather than a parent-style boundary map.
- Preferred section order:
  - `## Current Governance State` (recommended for live readers)
  - `## Governance Event Table` (recommended when current-state governance matters)
  - `## Contract Statement Table` (optional but recommended when clause-level traceability matters)
  - `## Code Bridge Table` (optional but recommended when contract meaning is code-coupled)
  - `## Code Bridge Evolution Table` (optional but recommended when bridge rows may change over time)
  - `## Contract Coverage Table` (optional but recommended when current coverage/boundary standing must stay explicit)
  - `## Coverage Evolution Table` (optional but recommended when coverage rows may change over time)
  - `## Current Boundary Map` (optional; parent-reader surface only)
  - `## Current Reader Shape` (optional; narrow current-reader explanation only)
  - `## Statement Evolution Table` (optional but recommended when clause-flow history matters)
  - `## Release Change`
  - `## Contract Statement`
  - `## Current Reading`
  - `## Reader Notes`
- `## Release Change` should summarize the material delta for this release, especially when `contract_release` is later than `0001`.
- When `release_action` is `historical-backfill`, `## Release Change` should also explain why this earlier historical state is being recorded only now and which later release or releases already remained in effect before the backfill was added.
- `## Contract Statement` should restate the current effective rule meaning in full; do not force readers to reconstruct the current state by diffing against earlier releases.
- When one later release absorbs new non-contract source material, mention that source carry-forward in `## Release Change`, while keeping release-to-release relationships in `lineage` and source-routing details in the support-only ledger.
- When one release change also changes which release is `current-primary`, `fallback-only`, `coexistence-window`, `historical-retained`, `lineage-only`, or `retired`, record that family-level standing through the family transition register rather than overloading the release body itself.
- If the source log declared `transition register update` as `required` or `conditional`, the release write-back should preserve that answer explicitly instead of silently assuming the release file alone explains current family coexistence.

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
  - `current code standing`
  - `bridge refs`
  - `statement text`
  - `notes`
- `statement label` should be a short human-readable clause title for the current contract meaning; it is the contract-facing quick label, not a copy of the source-owned `source slice` field from the ledger.
- `statement label` names the clause's current meaning only:
  - do not encode parent/child routing, split history, absorbed history, return flow, or other lineage inside the label
  - keep chronology in `Statement Evolution Table` and current boundary standing in a separate reader-facing section when needed
- `source basis` may contain one or more stable anchors when the clause truly depends on multiple upstream bases.
- `first effective at` should capture the best currently known historical time at which the clause first became effective, independent of the append-only registry release number.
- `last changed at` should capture the best currently known historical time for the latest semantic change represented in this release's reading of the clause.
- `effective from` and `effective until` should capture the active historical range for the clause as currently read in this release; use `ongoing` when the clause remains in force without a known end date.
- `current code standing` should make the statement's current code relationship visible from the statement table itself, for example `bridged-now`, `indirect-bridge`, `code-anchor-only`, `contract-only`, or `boundary-only`.
- `bridge refs` should point to the current bridge ids when the statement is directly represented in the contract's code-bridge surface.
- The statement table's time fields are required columns whenever the table is present; if one defended timestamp or window edge is not known, keep the column and use `unknown` or `ongoing` explicitly.
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
  - `history-backfilled`
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
  - when `first effective release` is the same, sort `change action` as `history-backfilled`, then `carried-forward`, then `amended`, then `introduced`
  - after that, keep one reader-friendly order inside each action bucket rather than forcing purely lexical id ordering
- The contract statement table does not replace source routing or supplement admission:
  - the parent ledger still owns source slicing and routing verdicts
  - the supplement ledger still owns later evidence admission and write-back recommendations
  - the contract statement table only tracks the effective clause state inside one contract release

## Optional Current Boundary Map

- Use this section only on a broader parent contract when the current reader still needs help answering `which clauses are still owned here, and which now read only as delegated-summary or other boundary standings beneath narrower child readers?`
- Treat `Current Boundary Map` as parent-facing and reader-facing only:
  - it explains current boundary standing
  - it does not replace release lineage in frontmatter
  - it does not replace clause chronology in `Statement Evolution Table`
  - it does not replace source routing in parent ledgers or supplements
- Recommended columns:
  - `boundary id`
  - `broad clause`
  - `current reading mode`
  - `current narrow owner`
  - `parent keeps`
  - `notes`
- Recommended `current reading mode` values include:
  - `parent-owned`
  - `delegated-summary`
  - `child-owned`
  - `shared-reader`
  - `backfilled-history-only`
  - `no-child-relation`
- If the contract is not acting as a broader parent boundary, do not add this section just to restate chronology or mixed clause origins.

## Optional Current Reader Shape

- Use this section on a narrow current reader when the main ambiguity is not parent/child ownership but how one current release integrates earlier-admitted history, carried-forward family clauses, amendments, or newly introduced clauses.
- This section should explain the current reader shape in brief prose rather than introducing a second ownership table.
- Prefer this section when readers need help answering questions such as:
  - why `history-backfilled`, `carried-forward`, `amended`, and `introduced` rows coexist in one current reader
  - how to interpret mixed clause origins without confusing them with current ownership routing
- Keep the chronology itself in `Statement Evolution Table`; `Current Reader Shape` is only the reader-facing explanation of how to read that mixed current clause set.

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
  - `history-backfilled`
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
- When one later release carries earlier-discovered clauses inside the current reader, show those change rows as `history-backfilled` ahead of same-release `carried-forward`, `amended`, or `introduced` rows so readers see the earlier-history admission first.

## Optional Code Bridge Table

- Use this section when contract meaning depends on one bounded code or workflow attachment profile.
- Treat this table as the current active bridge surface; bridge-event chronology should stay in `Code Bridge Evolution Table`.
- Required columns:
  - `bridge id`
  - `owned statement ids`
  - `applied to surface`
  - `stable ref`
  - `current standing`
  - `recorded at`
  - `effective from`
  - `effective until`
  - `effective status`
  - `evidence refs`
  - `notes`
- Optional profile columns such as `runtime boundary`, `drill-facing entry id`, `switch surface`, or another bounded attachment field may be inserted between `stable ref` and `current standing` when the family needs them.
- Time-window fields are required whenever this table is present; unknown or ongoing values are allowed, omission is not.

## Optional Code Bridge Evolution Table

- Use this section when bridge rows may be introduced, revised, narrowed, replaced, retired, or backfilled over time.
- Recommended columns:
  - `bridge change id`
  - `affected bridge ids`
  - `change action`
  - `actor value`
  - `effective at`
  - `recorded at`
  - `source basis`
  - `notes`
- `effective at` records when the bridge change is believed to have become historically effective.
- `recorded at` records when the change event entered repo chronology.

## Optional Contract Coverage Table

- Use this section when the contract must distinguish defended current meaning from code-anchor-only, deferred, or not-owned-here surfaces.
- Treat this table as the current active coverage/boundary surface; coverage-event chronology should stay in `Coverage Evolution Table`.
- Required columns:
  - `coverage id`
  - `semantic area`
  - `current basis`
  - `coverage class`
  - `current standing`
  - `current owner / later owner`
  - `recorded at`
  - `effective from`
  - `effective until`
  - `effective status`
  - `notes`
- Time-window fields are required whenever this table is present; unknown or ongoing values are allowed, omission is not.

## Optional Coverage Evolution Table

- Use this section when coverage rows may be introduced, revised, narrowed, rerouted, reopened, or retired over time.
- Recommended columns:
  - `coverage change id`
  - `affected coverage ids`
  - `change action`
  - `actor value`
  - `effective at`
  - `recorded at`
  - `source basis`
  - `notes`
- Keep active window ownership on the coverage rows themselves; use this evolution table for change-event chronology only.

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