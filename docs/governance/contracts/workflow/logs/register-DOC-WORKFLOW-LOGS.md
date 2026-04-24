# DOC-WORKFLOW-LOGS release transition register

```yaml
contract_release_transition_register:
  register_family_id: DOC-WORKFLOW-LOGS
  register_id: register-DOC-WORKFLOW-LOGS
  register_kind: contract-release-transition-register
  status: draft
  owner_lane: S0G-3G
  created_at: 2026-04-24
  reviewed_at: pending
  accepted_at: pending
  family_path: docs/governance/contracts/workflow/logs
  current_reader_goal: Explain which DOC-WORKFLOW-LOGS release should be opened first now, why DOC-WORKFLOW-LOGS-0001 still remains reader-relevant, and whether any active coexistence window still exists between them.
```

## Purpose

- This register is the family-level release coexistence surface for `DOC-WORKFLOW-LOGS`.
- It exists so readers do not have to reconstruct current release standing only from scattered notes across `DOC-WORKFLOW-LOGS-0001` and `DOC-WORKFLOW-LOGS-0002`.
- It does not replace either release-local contract body, the source-owned ledgers, or the source-owner logs.

## Current Family State

- Current family: `DOC-WORKFLOW-LOGS`
- Open first now: `DOC-WORKFLOW-LOGS-0002`
- Current family state summary:
  - `DOC-WORKFLOW-LOGS-0002` is the current-primary logs-family release for semantic reading now.
  - `DOC-WORKFLOW-LOGS-0001` remains reader-relevant as one historical-retained release because `0002` carries forward part of its earlier rule body while also amending the frontmatter/body boundary and introducing explicit body-structure clauses.
  - No active fallback-only or coexistence-window release is currently defended for this family sample; the earlier release remains historical, not one open rollback surface.

## Release State Table

| contract id | release state | semantic standing | transition role | valid from | valid until | first open now | replaced by | transition note | evidence refs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LOGS-0002` | `current-primary` | `current-release-reader` | `primary current logs-family reader` | `2026-04-24` | `ongoing` | `yes` | `none` | Read this release first for the integrated current logs-family meaning: carried-forward identity and intake, amended frontmatter/body boundary, and introduced body-structure governance. | `DOC-WORKFLOW-LOGS-0002`; `DOC-WORKFLOW-LOGS-0002 Current Reader Shape`; `ledger-S0C-1A-log-extensions.md` |
| `DOC-WORKFLOW-LOGS-0001` | `historical-retained` | `superseded-historical-release` | `earlier logs-family release retained for historical reading and clause ancestry` | `2026-04-24` | `ongoing` | `no` | `DOC-WORKFLOW-LOGS-0002` | Read this release when the reader needs the earlier narrower logs-family rule set before explicit body-structure governance entered the family current reader. | `DOC-WORKFLOW-LOGS-0001`; `DOC-WORKFLOW-LOGS-0002`; `S0G-3G` |

## Transition Window Table

| window id | from release | to release | window state | opened at | target close at | closed at | reason | close condition | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LOGS-TW-01` | `DOC-WORKFLOW-LOGS-0001` | `DOC-WORKFLOW-LOGS-0002` | `closed` | `2026-04-24` | `2026-04-24` | `2026-04-24` | The family needed one explicit reader transition from the first narrow identity/front-matter reader to the later body-structure-aware current reader once `S0C-1A` was admitted directly into the family. | `DOC-WORKFLOW-LOGS-0002` became the first-open release and `DOC-WORKFLOW-LOGS-0001` was reclassified as one retained historical release rather than one active fallback or coexistence reader. | `DOC-WORKFLOW-LOGS-0001`; `DOC-WORKFLOW-LOGS-0002`; `S0G-3G`; `ledger-S0C-1A-log-extensions.md` | This is a historical transition-window record, not one still-open release overlap. |

## Statement Transition Table

- No statement-transition rows are currently opened for this sample.
- Reason:
  - `DOC-WORKFLOW-LOGS-0002` contains mixed `carried-forward`, `amended`, and `introduced` clauses, but the current sample does not yet defend one live statement-level `dual-write`, `dual-read`, `fallback-read`, or `shadow-only` rollout state.
  - Under this rule, the mixed statement chronology remains in `DOC-WORKFLOW-LOGS-0002` through `Current Reader Shape` plus `Statement Evolution Table`, while this family register remains release-level only for now.

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `which release should I read first for current logs-family meaning?` | `DOC-WORKFLOW-LOGS-0002` | It is the current-primary logs-family reader. |
| `why does DOC-WORKFLOW-LOGS-0001 still matter?` | `register-DOC-WORKFLOW-LOGS.md` | This register explains that `0001` is retained for historical reading and clause ancestry rather than as an active fallback. |
| `what exactly did the first logs-family release mean before body-structure governance was made explicit?` | `DOC-WORKFLOW-LOGS-0001` | The earlier release-local semantic reading still belongs in the earlier release contract. |
| `why are body-structure clauses visible inside DOC-WORKFLOW-LOGS-0002?` | `DOC-WORKFLOW-LOGS-0002` | Its `Current Reader Shape` and `Statement Evolution Table` explain the mixed clause set inside the current release. |
| `why did the family current reader move from 0001 to 0002?` | `S0G-3G` | The direct-opening verdict in `S0G-3G` explains why body-structure governance was admitted into the later current reader now. |

## Usage Rules

- Use this register to answer release-level coexistence questions only.
- Do not copy the clause registry, statement evolution, or source-routing tables into this file.
- When a later `DOC-WORKFLOW-LOGS` release opens, update this register even if the older releases remain on disk unchanged.
- If a future logs-family release temporarily leaves an older release as `fallback-only` or `coexistence-window`, update that state here rather than hiding it only in notes on the current release.