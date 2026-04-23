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
| `<DOC-WORKFLOW-LABS-0001>` | `<historical-retained>` | `<superseded-historical-release>` | `<earlier release retained for family archaeology>` | `<YYYY-MM-DD|unknown>` | `<ongoing|YYYY-MM-DD|unknown>` | `<no>` | `<DOC-WORKFLOW-LABS-0002>` | `<why this release still matters, if at all>` | `<contract/local log/register refs>` |
| `<DOC-WORKFLOW-LABS-0002>` | `<current-primary>` | `<current-release>` | `<primary current reader>` | `<YYYY-MM-DD|unknown>` | `<ongoing|unknown>` | `<yes>` | `<none>` | `<why this is the current first-open release>` | `<contract/local log/register refs>` |

## Release State Field Rule

- `contract id` is the stable anchor for the row; do not use statement ids, ledger row ids, or supplement item ids as the primary row key in this table.
- `release state` answers current family-level coexistence standing.
- `semantic standing` is the release-local semantic standing already defended by the release contract, such as `current-release`, `superseded-historical-release`, or another defended local standing phrase.
- `transition role` is a short reader-facing explanation of why this release still matters now.
- `valid from` and `valid until` are the best defended dates or timestamps for the release's current coexistence standing inside this register, not necessarily the release's full historical-effective range.
- `first open now` should stay `yes` for only one `current-primary` row at a time.
- `replaced by` should name the newer release if one later release is already the current first-open reader.
- `evidence refs` should stay low-cardinality and point to the release contract, this register, and any directly relevant bounded log or ledger note.

## Transition Window Table

Use this section when one bounded coexistence or cutover window is still open or was explicitly closed.

| window id | from release | to release | window state | opened at | target close at | closed at | reason | close condition | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<DOC-WORKFLOW-LABS-TW-01>` | `<DOC-WORKFLOW-LABS-0001>` | `<DOC-WORKFLOW-LABS-0002>` | `<open|closed|abandoned>` | `<YYYY-MM-DD|unknown>` | `<YYYY-MM-DD|pending|unknown>` | `<YYYY-MM-DD|pending|n/a>` | `<why the overlap exists>` | `<what must become true before the older release leaves fallback/coexistence standing>` | `<log/ledger/contract refs>` | `<short bounded explanation>` |

## Transition Window Rule

- Open a transition-window row only when readers still need one explicit family-level explanation for why more than one release remains concurrently relevant.
- Do not open a transition-window row merely because one earlier release still exists on disk.
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