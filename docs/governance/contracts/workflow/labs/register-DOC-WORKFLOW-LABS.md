# DOC-WORKFLOW-LABS release transition register

```yaml
contract_release_transition_register:
  register_family_id: DOC-WORKFLOW-LABS
  register_id: register-DOC-WORKFLOW-LABS
  register_kind: contract-release-transition-register
  status: draft
  owner_lane: S0G-4B
  created_at: 2026-04-23
  reviewed_at: pending
  accepted_at: pending
  family_path: docs/governance/contracts/workflow/labs
  current_reader_goal: Explain which DOC-WORKFLOW-LABS releases should be opened first now, why earlier releases still remain reader-relevant, and whether any active transition window still exists between them.
```

## Purpose

- This register is the family-level release coexistence surface for `DOC-WORKFLOW-LABS`.
- It exists so readers do not have to reconstruct current release standing only from scattered notes across `DOC-WORKFLOW-LABS-0001` and `DOC-WORKFLOW-LABS-0002`.
- It does not replace either release-local contract body, the parent ledgers, the accepted supplement packet, or the source-owner logs.

## Current Family State

- Current family: `DOC-WORKFLOW-LABS`
- Open first now: `DOC-WORKFLOW-LABS-0002`
- Current family state summary:
  - `DOC-WORKFLOW-LABS-0002` is the current-primary labs-family release for semantic reading now.
  - `DOC-WORKFLOW-LABS-0001` remains reader-relevant as one historical-retained release because `0002` carries forward and amends part of its earlier rule body rather than erasing the earlier release from family archaeology.
  - No active fallback-only or coexistence-window release is currently defended for this family sample; the earlier release remains historical, not one open rollback surface.

## Release State Table

| contract id | release state | semantic standing | transition role | valid from | valid until | first open now | replaced by | transition note | evidence refs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LABS-0002` | `current-primary` | `current-release-reader` | `primary current labs-family reader` | `2026-04-10` | `ongoing` | `yes` | `none` | Read this release first for the integrated current labs-family meaning: carried-forward `0001` clauses, amended evidence-package framing, introduced package-shape rules, and admitted earlier-history labs clauses. | `DOC-WORKFLOW-LABS-0002`; `DOC-WORKFLOW-LABS-0002 Current Reader Shape`; `ledger-SUP-S0A-2A-002-labs-early-failure-management-and-pre-drills-shape.md` |
| `DOC-WORKFLOW-LABS-0001` | `historical-retained` | `superseded-historical-release` | `earlier labs-family release retained for historical reading and clause ancestry` | `2026-04-10` | `ongoing` | `no` | `DOC-WORKFLOW-LABS-0002` | Read this release when the reader needs the earlier narrower labs/snapshots rule set before the later evidence-package framing and later admitted earlier-history clauses visible in `0002`. | `DOC-WORKFLOW-LABS-0001`; `DOC-WORKFLOW-LABS-0001-GOV-03`; `DOC-WORKFLOW-LABS-0002` |

## Transition Window Table

| window id | from release | to release | window state | opened at | target close at | closed at | reason | close condition | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LABS-TW-01` | `DOC-WORKFLOW-LABS-0001` | `DOC-WORKFLOW-LABS-0002` | `closed` | `2026-04-10` | `2026-04-10` | `2026-04-10` | The family needed one explicit reader transition from the first labs/snapshots release to the later evidence-package release once the `S0B-2A` labs slice was admitted into the family current reader. | `DOC-WORKFLOW-LABS-0002` became the first-open release and `DOC-WORKFLOW-LABS-0001` was reclassified as one retained historical release rather than one active fallback or coexistence reader. | `DOC-WORKFLOW-LABS-0001-GOV-03`; `DOC-WORKFLOW-LABS-0002 lineages.supersedes`; `ledger-S0B-1A-tools-labs-and-snapshots.md`; `log-S0G-4B-doc-contract-release-transition-register-and-writeback-chain-governance.md` | This is a historical transition-window record, not one still-open release overlap. |

## Statement Transition Table

- No statement-transition rows are currently opened for this sample.
- Reason:
  - `DOC-WORKFLOW-LABS-0002` contains mixed `history-backfilled`, `carried-forward`, `amended`, and `introduced` clauses, but the current sample does not yet defend one live statement-level `dual-write`, `dual-read`, `fallback-read`, or `shadow-only` rollout state.
  - Under this rule, the mixed statement chronology remains in `DOC-WORKFLOW-LABS-0002` through `Current Reader Shape` plus `Statement Evolution Table`, while this family register remains release-level only for now.
  - If one later labs-family packet proves that specific statements are transitioning at different rollout speeds, this section should convert from one note into one bounded statement-transition table rather than overloading the release-state rows above.

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `which release should I read first for current labs-family meaning?` | `DOC-WORKFLOW-LABS-0002` | It is the current-primary labs-family reader. |
| `why does DOC-WORKFLOW-LABS-0001 still matter?` | `register-DOC-WORKFLOW-LABS.md` | This register explains that `0001` is retained for historical reading and ancestry rather than as an active fallback. |
| `what exactly did the first labs-family release mean before the later evidence-package framing?` | `DOC-WORKFLOW-LABS-0001` | The earlier release-local semantic reading still belongs in the earlier release contract. |
| `why are earlier-history labs clauses visible inside DOC-WORKFLOW-LABS-0002?` | `DOC-WORKFLOW-LABS-0002` | Its `Current Reader Shape` and `Statement Evolution Table` explain the mixed clause set inside the current release. |
| `why did the family current reader move from 0001 to 0002?` | `DOC-WORKFLOW-LABS-0002` | The later release change and lineage state explain why the evidence-package revision became the first-open family reader. |

## Usage Rules

- Use this register to answer release-level coexistence questions only.
- Do not copy the clause registry, statement evolution, or source-routing tables into this file.
- When a later `DOC-WORKFLOW-LABS` release opens, update this register even if the older releases remain on disk unchanged.
- If a future labs-family release temporarily leaves an older release as `fallback-only` or `coexistence-window`, update that state here rather than hiding it only in notes on the current release.
- If a dedicated historical-backfill labs release is opened later for the earlier pre-runbook labs clauses now hosted in `0002`, update this register to add that release as one additional family row rather than overloading the `0002` row further.