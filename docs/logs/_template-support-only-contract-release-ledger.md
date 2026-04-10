# support-only-contract-release-ledger-template

## Purpose

- Use this ledger when one source issue, log, or retained support-only body is being split across multiple contract families, release actions, or retained-only destinations.
- This ledger owns `source routing and extraction accounting` only.
- Do not use contract lineage fields to replace this ledger; lineage stays contract-to-contract, while this ledger explains how mixed source material was mapped into later contract work.

## Naming Rule

- Name ledgers as `ledger-<owner-lane-id>-<summary>.md`.
- The `<summary>` should say what source was routed and what kind of module/release split is being tracked.
- Preferred example for the first sample in `S0F-7B`:
  - `ledger-S0F-7B-s0a-2a-contract-release-routing.md`

## Minimal Header

```yaml
support_only_contract_release_ledger:
  ledger_id: <ledger-S0F-7B-summary>
  ledger_kind: support-only-contract-release-ledger
  status: <draft|active|completed>
  owner_lane: <S0F-7B>
  source_ref: <issue/log/support-only source being split>
  source_scope: <what portion of the source this ledger covers>
  target_reading_goal: <what later reader should understand after this ledger is applied>
```

## Routing Table Shape

| source slice | meaning owned here | target family | target release action | contract lineage impact | retained-only action | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `<source heading or bounded paragraph set>` | `<what rule/boundary the slice carries>` | `<DOC-WORKFLOW-LABS>` | `<new-release|revise-release|new-family|no-contract>` | `<supersede|split|absorb|retire|none-source-only>` | `<keep-in-log|support-only|defer>` | `<why this routing is correct>` |

## Required Rules

- `target family` names the stable semantic family, not one specific release number.
- `target release action` states what the receiving contract work should do:
  - `new-family`
  - `new-release`
  - `revise-release`
  - `no-contract`
- `contract lineage impact` may stay `none-source-only` when the source slice is new material that is not itself one earlier contract.
- `retained-only action` is required when a source slice is not promoted into a contract release.
- If one later release absorbs new non-contract source material, record that fact here and carry the source forward in the later release metadata; do not fabricate `absorbed_from` links to sources that were never contracts.

## Optional Rollup

- `new releases expected`:
  - list the release records that should exist after this ledger is applied
- `cumulative sources to carry forward`:
  - list the sources that later release metadata must keep visible
- `deferred slices`:
  - list source slices that still need judgment later