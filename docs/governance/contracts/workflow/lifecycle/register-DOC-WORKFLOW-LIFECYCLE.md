# DOC-WORKFLOW-LIFECYCLE release transition register

```yaml
contract_release_transition_register:
  register_family_id: DOC-WORKFLOW-LIFECYCLE
  register_id: register-DOC-WORKFLOW-LIFECYCLE
  register_kind: contract-release-transition-register
  status: draft
  owner_lane: S0G-3G
  created_at: 2026-04-24
  reviewed_at: pending
  accepted_at: pending
  family_path: docs/governance/contracts/workflow/lifecycle
  current_reader_goal: Explain which DOC-WORKFLOW-LIFECYCLE release should be opened first now, why DOC-WORKFLOW-LIFECYCLE-0001 still remains reader-relevant, and why the later integrated lifecycle reader now includes S0C-2A-derived retirement clauses.
```

## Purpose

- This register is the family-level release coexistence surface for `DOC-WORKFLOW-LIFECYCLE`.
- It exists so readers do not have to reconstruct current release standing only from scattered notes across `DOC-WORKFLOW-LIFECYCLE-0001` and `DOC-WORKFLOW-LIFECYCLE-0002`.
- It does not replace either release-local contract body, the source-owned ledgers, or the source-owner logs.

## Current Family State

- Current family: `DOC-WORKFLOW-LIFECYCLE`
- Open first now: `DOC-WORKFLOW-LIFECYCLE-0002`
- Current family state summary:
  - `DOC-WORKFLOW-LIFECYCLE-0002` is the current-primary lifecycle-family release for semantic reading now.
  - `DOC-WORKFLOW-LIFECYCLE-0001` remains reader-relevant as one historical-retained release because `0002` carries forward its earlier continuity and cutover body while also introducing explicit retirement and replacement-coverage clauses from `S0C-2A`.
  - No active fallback-only or coexistence-window release is currently defended for this family sample; the earlier release remains historical, not one open rollback surface.

## Release State Table

| contract id | release state | semantic standing | transition role | valid from | valid until | first open now | replaced by | transition note | evidence refs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LIFECYCLE-0002` | `current-primary` | `current-release-reader` | `primary current lifecycle-family reader` | `2026-04-24` | `ongoing` | `yes` | `none` | Read this release first for the integrated current lifecycle-family meaning: carried-forward continuity clauses, amended family boundary, and introduced test-retirement governance. | `DOC-WORKFLOW-LIFECYCLE-0002`; `DOC-WORKFLOW-LIFECYCLE-0002 Current Reader Shape`; `ledger-S0C-2A-legacy-integration-suite-retired.md` |
| `DOC-WORKFLOW-LIFECYCLE-0001` | `historical-retained` | `superseded-historical-release` | `earlier lifecycle-family release retained for historical reading and clause ancestry` | `2026-04-24` | `ongoing` | `no` | `DOC-WORKFLOW-LIFECYCLE-0002` | Read this release when the reader needs the earlier narrower docs-lifecycle rule set before explicit active-test-retirement governance entered the family current reader. | `DOC-WORKFLOW-LIFECYCLE-0001`; `DOC-WORKFLOW-LIFECYCLE-0002`; `S0G-3G` |

## Transition Window Table

| window id | from release | to release | window state | opened at | target close at | closed at | reason | close condition | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LIFECYCLE-TW-01` | `DOC-WORKFLOW-LIFECYCLE-0001` | `DOC-WORKFLOW-LIFECYCLE-0002` | `closed` | `2026-04-24` | `2026-04-24` | `2026-04-24` | The family needed one explicit reader transition from the first narrow docs-lifecycle release to the later integrated lifecycle reader once `S0C-2A` was admitted into the family current reader. | `DOC-WORKFLOW-LIFECYCLE-0002` became the first-open release and `DOC-WORKFLOW-LIFECYCLE-0001` was reclassified as one retained historical release rather than one active fallback or coexistence reader. | `DOC-WORKFLOW-LIFECYCLE-0001`; `DOC-WORKFLOW-LIFECYCLE-0002`; `S0G-3G`; `ledger-S0C-2A-legacy-integration-suite-retired.md` | This is a historical transition-window record, not one still-open release overlap. |

## Statement Transition Table

- No statement-transition rows are currently opened for this sample.
- Reason:
  - `DOC-WORKFLOW-LIFECYCLE-0002` contains mixed `carried-forward`, `amended`, and `introduced` clauses, but the current sample does not yet defend one live statement-level `dual-write`, `dual-read`, `fallback-read`, or `shadow-only` rollout state.
  - Under this rule, the mixed statement chronology remains in `DOC-WORKFLOW-LIFECYCLE-0002` through `Current Reader Shape` plus `Statement Evolution Table`, while this family register remains release-level only for now.

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `which release should I read first for current lifecycle-family meaning?` | `DOC-WORKFLOW-LIFECYCLE-0002` | It is the current-primary lifecycle-family reader. |
| `why does DOC-WORKFLOW-LIFECYCLE-0001 still matter?` | `register-DOC-WORKFLOW-LIFECYCLE.md` | This register explains that `0001` is retained for historical reading and clause ancestry rather than as an active fallback. |
| `what exactly did the first lifecycle-family release mean before test-retirement governance was made explicit?` | `DOC-WORKFLOW-LIFECYCLE-0001` | The earlier release-local semantic reading still belongs in the earlier release contract. |
| `why are test-retirement clauses visible inside DOC-WORKFLOW-LIFECYCLE-0002?` | `DOC-WORKFLOW-LIFECYCLE-0002` | Its `Current Reader Shape` and `Statement Evolution Table` explain the mixed clause set inside the current release. |
| `why did the family current reader move from 0001 to 0002?` | `S0G-3G` | The downstream family verdict in `S0G-3G` explains why `S0C-2A` was admitted into the later integrated lifecycle reader now. |

## Usage Rules

- Use this register to answer release-level coexistence questions only.
- Do not copy the clause registry, statement evolution, or source-routing tables into this file.
- When a later `DOC-WORKFLOW-LIFECYCLE` release opens, update this register even if the older releases remain on disk unchanged.
- If a future lifecycle-family release temporarily leaves an older release as `fallback-only` or `coexistence-window`, update that state here rather than hiding it only in notes on the current release.