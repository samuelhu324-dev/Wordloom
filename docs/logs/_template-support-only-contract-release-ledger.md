# support-only-contract-release-ledger-template

## Purpose

- Use this ledger when one source issue, log, or retained support-only body is being split across multiple contract families, release actions, or retained-only destinations.
- This ledger owns `source routing, extraction accounting, and later consumption tracking`.
- Do not use contract lineage fields to replace this ledger; lineage stays contract-to-contract, while this ledger explains how mixed source material was mapped into later contract work.

## Naming Rule

- Name ledgers as `ledger-<source-id>-<source-summary>.md`.
- The `<source-id>` should match the source log or issue identifier being routed.
- The `<source-summary>` should reuse the source summary itself, normalized to filename shape rather than inventing a second naming scheme.
- Preferred example shapes:
  - `ledger-S0B-2A-tools-scripts-and-snapshots-management.md`
  - `ledger-S0A-2A-structured-doc-refinement-pipeline.md`

## Minimal Header

```yaml
support_only_contract_release_ledger:
  ledger_id: <ledger-S0B-2A-source-summary>
  ledger_kind: support-only-contract-release-ledger
  status: <draft|active|completed>
  owner_lane: <S0F-7B>
  created_at: <YYYY-MM-DD|pending>
  reviewed_at: <YYYY-MM-DD|pending>
  accepted_at: <YYYY-MM-DD|pending>
  source_id: <S0B-2A>
  source_ref: <issue/log/support-only source being split>
  source_scope: <what portion of the source this ledger covers>
  target_reading_goal: <what later reader should understand after this ledger is applied>
```

## Lifecycle Field Rule

- `created_at` records when this ledger file was first created in the repo.
- `reviewed_at` records when the ledger routing was first reviewed tightly enough to count as one defended packet rather than one raw staging draft.
- `accepted_at` records when the ledger is accepted as the current parent routing surface for later supplement or contract work.
- These fields are artifact-lifecycle timestamps only; they do not claim to describe when the underlying historical rule first became effective.

## Routing Table Shape

| row id | source slice | meaning owned here | target family | target release action | contract lineage impact | retained-only action | resolution status | resolved by contract id | consumed scope | resolution notes | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `<S0A-1A-R01>` | `<source heading or bounded paragraph set>` | `<what rule/boundary the slice carries>` | `<DOC-WORKFLOW-LABS>` | `<new-release|revise-release|new-family|no-contract>` | `<supersede|split|absorb|retire|none-source-only>` | `<keep-in-log|support-only|defer>` | `<draft|applied|partially-applied|deferred|retained-support-only|re-routed|rejected>` | `<DOC-WORKFLOW-LABS-0002|none>` | `<full|partial|none>` | `<how this slice was finally consumed or why it was not>` | `<why this routing is correct>` |

## Required Rules

- `row id` is required for every routed slice and should stay stable even when the prose wording in `source slice` tightens later.
- Name `row id` as `<source-id>-R<n>` with zero-padded sequence numbers inside one ledger.
- `target family` names the stable semantic family, not one specific release number.
- `target release action` states what the receiving contract work should do:
  - `new-family`
  - `new-release`
  - `revise-release`
  - `no-contract`
- `contract lineage impact` may stay `none-source-only` when the source slice is new material that is not itself one earlier contract.
- `retained-only action` is required when a source slice is not promoted into a contract release.
- `resolution status` records the terminal or current consumption state of that slice:
  - `draft`
  - `applied`
  - `partially-applied`
  - `deferred`
  - `retained-support-only`
  - `re-routed`
  - `rejected`
- `resolved by contract id` should name the later release that consumed the slice when consumption actually happened.
- `consumed scope` states whether the slice was consumed fully, partially, or not at all.
- If one later release absorbs new non-contract source material, record that fact here and carry the source forward in the later release metadata; do not fabricate `absorbed_from` links to sources that were never contracts.

## Completion Rule

- A ledger may be marked `completed` only when every source slice has one explicit resolution state.
- Leaving a row undecided is not completion.
- A slice counts as resolved only when it is marked as one of:
  - `applied`
  - `partially-applied`
  - `deferred`
  - `retained-support-only`
  - `re-routed`
  - `rejected`
- Under this rule, the ledger remains the durable place to answer `what was consumed`, `what was not consumed`, and `where each slice ended up later`.

## Optional Rollup

- `new releases expected`:
  - list the release records that should exist after this ledger is applied
- `row id map`:
  - list any stable row ids whose prose labels were tightened after initial creation
- `cumulative sources to carry forward`:
  - list the sources that later release metadata must keep visible
- `deferred slices`:
  - list source slices that still need judgment later
- `unconsumed slices`:
  - list source slices that were intentionally not promoted into a release