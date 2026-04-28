# contract-release-transition-register-template

Use this template for one family-level transition register that tracks how multiple releases inside the same stable contract family currently coexist.

## Purpose

- Use this register when more than one release in the same stable family still matters to readers at the same time, for example one `current-primary` release plus one `fallback-only`, `coexistence-window`, or `historical-retained` release.
- This register owns `family-level release coexistence and transition-window state`.
- Do not use this register to replace release-local semantic contracts, parent ledgers, supplement ledgers, or source logs.

## Naming Rule

- Name the file as `register-<contract_family>.md`.
- Keep the file in the same family directory as the release contracts it governs.
- Example shape for the labs family:
  - `docs/governance/contracts/workflow/labs/register-DOC-WORKFLOW-LABS.md`

## Register Boundary

- This register should answer:
  - which releases are currently `primary`, `fallback-only`, `coexistence-window`, `historical-retained`, `lineage-only`, or `retired`
  - which release a reader should open first now
  - whether one transition window is open between releases
  - what evidence or closure condition is still required before one older release leaves that active coexistence state
- This register may also answer one narrower question when release-level state alone is not enough:
  - whether specific statements inside the current family releases are currently `primary`, `dual-write`, `dual-read`, `fallback-read`, `shadow-only`, `historical-carried`, or `retired`
- This register should not answer:
  - full clause meaning for any one release
  - full statement lineage or statement-level history
  - source routing or supplement admission details already owned by ledgers
  - full execution reasoning already owned by source logs

## Minimal Header

```yaml
contract_release_transition_register:
  register_family_id: <DOC-WORKFLOW-LABS>
  register_id: <register-DOC-WORKFLOW-LABS>
  register_kind: contract-release-transition-register
  status: <draft|active|completed>
  owner_lane: <S0G-4B>
  created_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  accepted_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  family_path: <docs/governance/contracts/workflow/labs>
  current_reader_goal: <what a reader should understand about the family release state right now>
```

## Lifecycle Field Rule

- `created_at`, `reviewed_at`, and `accepted_at` are artifact-lifecycle fields for the register itself, not historical-effective timestamps for any release.
- `created_at`, `reviewed_at`, and `accepted_at` are required header fields for the register; when a defended value is not known yet, keep the field present and use `unknown` or `pending` rather than omitting it.
- New writes should prefer canonical UTC-second timestamps such as `2026-04-23T14:12:05Z`.
- Legacy day-only values may remain when finer audit precision is unnecessary or unavailable.

## Current Family State

- Current family: `<DOC-WORKFLOW-LABS>`
- Open first now: `<DOC-WORKFLOW-LABS-0002>`
- Current family state summary:
  - `<which release is primary>`
  - `<whether any fallback or coexistence window remains open>`
  - `<what older releases still remain reader-relevant and why>`

## Release State Values

Use these values consistently in `release state`.

- `current-primary`:
  - this is the first-open current family release for semantic reading now
- `fallback-only`:
  - this release is no longer the first-open current reader, but it is still intentionally retained as one temporary fallback or transition-safe surface
- `coexistence-window`:
  - this release remains in one bounded active overlap window with a newer release while closure conditions are still open
- `historical-retained`:
  - this release remains reader-visible as one retained historical release but is no longer part of active transition-safe fallback use
- `lineage-only`:
  - this release still matters for deterministic lineage or redirect reading but is no longer expected to act as current or fallback reading
- `retired`:
  - this release is fully ended as an active or fallback reading surface and remains only as a retired release record

## Release State Table

| contract id | release state | semantic standing | transition role | valid from | valid until | first open now | replaced by | transition note | evidence refs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<DOC-WORKFLOW-LABS-0002>` | `<current-primary>` | `<current-release>` | `<primary current reader>` | `<YYYY-MM-DD|unknown>` | `<ongoing|unknown>` | `<yes>` | `<none>` | `<why this is the current first-open release>` | `<contract/local log/register refs>` |
| `<DOC-WORKFLOW-LABS-0001>` | `<historical-retained>` | `<superseded-historical-release>` | `<earlier release retained for family archaeology>` | `<YYYY-MM-DD|unknown>` | `<ongoing|YYYY-MM-DD|unknown>` | `<no>` | `<DOC-WORKFLOW-LABS-0002>` | `<why this release still matters, if at all>` | `<contract/local log/register refs>` |

## Release State Field Rule

- `contract id` is the stable anchor for the row; do not use statement ids, ledger row ids, or supplement item ids as the primary row key in this table.
- `release state` answers current family-level coexistence standing.
- `semantic standing` is the release-local semantic standing already defended by the release contract, such as `current-release`, `superseded-historical-release`, or another defended local standing phrase.
- `transition role` is a short reader-facing explanation of why this release still matters now.
- `valid from` and `valid until` are the best defended dates or timestamps for the release's current coexistence standing inside this register, not necessarily the release's full historical-effective range.
- `valid from` and `valid until` are required columns in every `Release State Table` row; use `unknown` or `ongoing` when the defended coexistence window edge is not known yet.
- Do not derive `valid from` or `valid until` mechanically from the release contract `effective_from` or `effective_until`; register validity belongs to reader/coexistence standing, not to the release's whole semantic lifespan.
- When the current standing is defended but the start or end point is not, keep `unknown` or `ongoing` rather than fabricating a more precise coexistence date.
- `first open now` should stay `yes` for only one `current-primary` row at a time.
- `replaced by` should name the newer release if one later release is already the current first-open reader.
- `evidence refs` should stay low-cardinality and point to the release contract, this register, and any directly relevant bounded log or ledger note.
- Order the table for reader-first use, not historical-first archaeology:
  - put the newest first-open or `current-primary` release first
  - then list any `fallback-only` or `coexistence-window` releases
  - then list `historical-retained`, `lineage-only`, and `retired` releases

## Optional Statement Transition Table

Use this section only when release-level coexistence is no longer enough to describe current reader behavior because different statements inside the same family are transitioning at different speeds.

| statement anchor | current host release | rollout state | previous statement anchors | next target state | valid from | target close at | closed at | reader path now | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<DOC-WORKFLOW-LABS-0002-ST-01>` | `<DOC-WORKFLOW-LABS-0002>` | `<primary>` | `<DOC-WORKFLOW-LABS-0001-ST-01>` | `<primary>` | `<YYYY-MM-DD|unknown>` | `<n/a|YYYY-MM-DD|pending>` | `<n/a|YYYY-MM-DD|pending>` | `<read this statement through DOC-WORKFLOW-LABS-0002>` | `<contract/register/log refs>` | `<short bounded note>` |

## Statement Transition Values

Use these values consistently in `rollout state`.

- `primary`:
  - this statement now reads fully through its current host release
- `dual-read`:
  - readers still need to interpret old and new statement surfaces together for one bounded overlap period
- `dual-write`:
  - the statement meaning is currently being maintained in more than one active write-facing surface for one bounded overlap period
- `shadow-only`:
  - the statement is present only for shadow comparison or readiness checking, not as one defended primary reader path
- `fallback-read`:
  - the older statement remains intentionally readable as one bounded fallback path while a newer statement is already the primary reader
- `historical-carried`:
  - the statement remains visible for historical or carried-forward context but is not in one active dual-read or fallback rollout state
- `retired`:
  - the statement no longer participates in active rollout or reader coexistence

## Statement Transition Rule

- Open this section only when statement-level rollout differences are materially real for the family; do not add it merely because the release contains mixed `change action` values such as `history-backfilled`, `carried-forward`, `amended`, or `introduced`.
- `change action` still answers `how the statement entered the current release`; it does not by itself answer the statement's current rollout state.
- Keep the stable row anchor as `statement anchor`, typically one release-local statement id.
- Do not restate full statement text here; the semantic meaning still belongs in the release-local contract.
- If no statement-level rollout divergence is currently defended, omit the table entirely or replace it with one short note that no statement-transition rows are currently open.

## Transition Window Table

Use this section when one bounded coexistence or cutover window is still open or was explicitly closed.

| window id | from release | to release | window state | opened at | target close at | closed at | reason | close condition | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<DOC-WORKFLOW-LABS-TW-01>` | `<DOC-WORKFLOW-LABS-0001>` | `<DOC-WORKFLOW-LABS-0002>` | `<open|closed|abandoned>` | `<YYYY-MM-DD|unknown>` | `<YYYY-MM-DD|pending|unknown>` | `<YYYY-MM-DD|pending|n/a>` | `<why the overlap exists>` | `<what must become true before the older release leaves fallback/coexistence standing>` | `<log/ledger/contract refs>` | `<short bounded explanation>` |

## Transition Window Rule

- Open a transition-window row only when readers still need one explicit family-level explanation for why more than one release remains concurrently relevant.
- Do not open a transition-window row merely because one earlier release still exists on disk.
- Do not open a transition-window row for one single-release family or for one historical-retained release that has no active fallback/coexistence duty now.
- If coexistence is real but the open or close timing is not yet defended, keep `opened at`, `target close at`, or `closed at` as `unknown` or `pending` rather than inventing dates from release chronology alone.
- `opened at`, `target close at`, and `closed at` are required columns whenever `Transition Window Table` is present; if the timing is not defended, keep the field and use `unknown`, `pending`, or `n/a`.
- `window state` should stay one of:
  - `open`
  - `closed`
  - `abandoned`
- `close condition` should stay short and reviewable, for example:
  - `reader migration completed`
  - `parent-ledger writeback completed`
  - `bridged contract reconciliation completed`
  - `historical release reclassified from fallback-only to historical-retained`

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `which release should I read first for current meaning?` | `<DOC-WORKFLOW-LABS-0002>` | `<the current primary release is the first-open semantic reader>` |
| `why does an older release still matter?` | `<register-DOC-WORKFLOW-LABS.md>` | `<the family transition register explains coexistence or retained historical standing>` |
| `what exactly does one release mean?` | `<DOC-WORKFLOW-LABS-0002>` | `<release-local semantic meaning still belongs in the release contract>` |
| `why did this release-state change happen?` | `<bounded source log>` | `<full packet reasoning remains in the source-owner log or ledger chain>` |

## Usage Rules

- Keep this register family-level and release-level only.
- Do not replay full source-log or ledger reasoning here.
- Do not treat this register as one second contract body.
- Update this register when release coexistence or transition-window standing changes, even if no new contract release is minted.
- Do not open one new register per release; one stable family should normally keep one stable register file.
- When the family has only one clearly current release and no meaningful coexistence, this register may remain absent until the first real coexistence problem exists.

## Writeback Trigger Rule

- A source log that may affect family reader standing should declare `transition register update` explicitly in its `Required Processing Chain` before execution.
- Update this register when any of the following becomes true:
  - one new release becomes `current-primary`
  - one older release is reclassified as `fallback-only`, `coexistence-window`, `historical-retained`, `lineage-only`, or `retired`
  - one routing rewrite changes which existing release should be opened first now
  - one family-boundary decision changes which family owns the current reader or how reader-relevant releases coexist across families
- Do not update this register for evidence-only sharpening, chronology cleanup, or contract-local wording clarification when family-level reader standing is unchanged.
- If the source log classified the packet as `routing rewrite`, it should still answer explicitly whether family-level standing changed; do not treat routing-only packets as automatic no-op here.