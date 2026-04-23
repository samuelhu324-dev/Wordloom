# DOC-WORKFLOW-LABS-0001 tools labs and snapshots

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-LABS
  contract_release: 0001
  contract_id: DOC-WORKFLOW-LABS-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Preserve the first labs-family release from S0B-1A while aligning the file to the current chronology-first contract structure and fixed-width family numbering.
  summary: Treat lab snapshots as governed test assets with explicit classes, minimal retention, and safe-to-purge cleanup rules so iterative debugging does not collapse into either artifact hoarding or evidence loss.
  governance_area: workflow labs and snapshots governance
  applies_to: lab snapshot folders, retained lab evidence sets, golden fixtures, diff snapshots, ad-hoc dumps, and lab cleanup decisions
  enforcement_surface: manual
  violation_semantics: warning
  owner_team: docs-governance
  current_steward: delegated:workflow-labs-contract-maintainer
  approval_state: superseded-historical-release
  reviewed_by: role:workflow-reviewer
  approved_by: role:docs-governance-approver
  recorded_at: 2026-04-11
  reviewed_at: pending
  effective_from: 2026-02-08T09:14:31Z
  effective_until: ongoing
  introduced_by: GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
  last_changed_by: GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
  source_refs:
    - GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
  cumulative_source_refs:
    - GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
  supporting_evidence_refs:
    - docs/logs/support-only/ledger-S0B-1A-tools-labs-and-snapshots.md
    - legacy/from_structured_docs/from-logs/v2-logs/log-S3A-lab-snapshots-management.md
  lineage:
    supersedes: []
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This draft sits at the narrower `WORKFLOW-LABS` family layer beneath the broader workflow path.
    - That broader-vs-narrower family reading is taxonomy only; this record no longer claims a split lineage from `DOC-WORKFLOW-0001`.
    - The local repo currently has no S0B/1A source log, so this draft stays explicit about issue-only sourcing.
    - Current-state governance now reads through owner_team/current_steward/approval_state/reviewed_by/approved_by, while later family current state moves through `DOC-WORKFLOW-LABS-0002` and the parent ledgers remain the routing and event-history surfaces that explain the transition.
    - `effective_from` is anchored to the source issue creation time `2026-02-08T09:14:31Z` because the issue body itself already defends the labs asset, retention, and cleanup-rule boundary later preserved by the repaired parent ledger chronology.
```

## Current Governance State

- The current governed state of this release file is carried in frontmatter through `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- In this file, `approval_state: superseded-historical-release` means the first `DOC-WORKFLOW-LABS-0001` release remains a governed historical release, but the current family reader has moved to `DOC-WORKFLOW-LABS-0002`.
- Older fields such as `introduced_by`, `last_changed_by`, `source_refs`, and `cumulative_source_refs` remain chronology/source metadata for this release family; they should not be read as current ownership or approval identity.
- This contract therefore remains the governed current-state surface for the historical `0001` release artifact, while `DOC-WORKFLOW-LABS-0002` carries the later family current-state reader and the parent ledgers preserve the routing and event-history chain.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LABS-0001-GOV-01` | `contribution-event` | `DOC-WORKFLOW-LABS-0001` | `unknown` | `family-introduced` | `2026-02-08T09:14:31Z` | `GitHub issue S0B/1A (#36)` | The issue-only source introduced the first labs-family release on the issue creation date, but it does not by itself prove the current steward or approval chain for the retained release artifact. |
| `DOC-WORKFLOW-LABS-0001-GOV-02` | `routing-writeback-event` | `DOC-WORKFLOW-LABS-0001` | `role:packet-reviewer` | `historical-release-state-fixed` | `2026-04-11` | `ledger-S0B-1A-tools-labs-and-snapshots.md` | The parent ledger fixed that `DOC-WORKFLOW-LABS-0001` remains the first accepted labs release for the original packet even though later family current state moved to `DOC-WORKFLOW-LABS-0002`. |
| `DOC-WORKFLOW-LABS-0001-GOV-03` | `superseded-release-event` | `DOC-WORKFLOW-LABS-0001` | `role:packet-reviewer` | `superseded-historical-release` | `2026-04-10` | `DOC-WORKFLOW-LABS-0002` | The first labs release is now explicitly retained as a governed historical release because `DOC-WORKFLOW-LABS-0002` superseded it as the current family reader. |
| `DOC-WORKFLOW-LABS-0001-GOV-04` | `review-approval-separation-event` | `DOC-WORKFLOW-LABS-0001` | `role:workflow-reviewer; role:docs-governance-approver` | `historical-release-governance-separated` | `2026-04-15` | `S0F-9A/P4 third-cycle round` | The retained historical release now records review and approval as distinct governance acts rather than leaving the historical file unguided by the current control-plane rule. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LABS-0001-ST-01` | `Labs as test assets` | `active` | `introduced` | `S0B-1A-R01` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `2026-02-08T09:14:31Z` | `ongoing` | `in-force` | Lab snapshot folders must be governed as test assets rather than left to accumulate as an unbounded debugging heap. | First defended labs-family framing clause. |
| `DOC-WORKFLOW-LABS-0001-ST-02` | `Snapshot class taxonomy` | `active` | `introduced` | `S0B-1A-R01` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `2026-02-08T09:14:31Z` | `ongoing` | `in-force` | Snapshot outputs should be classified into explicit roles: golden fixtures, diff snapshots, and ad-hoc dumps. | Parent classification clause sourced from the snapshot-asset-classes ledger row. |
| `DOC-WORKFLOW-LABS-0001-ST-03` | `Golden fixtures` | `active` | `introduced` | `S0B-1A-R01` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `2026-02-08T09:14:31Z` | `ongoing` | `in-force` | Golden fixtures are small, high-signal retained artifacts that stay in git as the replayable regression baseline. | Narrow child clause beneath the asset-classes row. |
| `DOC-WORKFLOW-LABS-0001-ST-04` | `Diff snapshots` | `active` | `introduced` | `S0B-1A-R01` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `2026-02-08T09:14:31Z` | `ongoing` | `in-force` | Diff snapshots are short-lived comparison artifacts used during iteration and removable once conclusions are stabilized. | Narrow child clause beneath the asset-classes row. |
| `DOC-WORKFLOW-LABS-0001-ST-05` | `Ad-hoc dumps` | `active` | `introduced` | `S0B-1A-R01` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `2026-02-08T09:14:31Z` | `ongoing` | `in-force` | Ad-hoc dumps are disposable debugging output that should not become retained contract evidence by default. | Narrow child clause beneath the asset-classes row. |
| `DOC-WORKFLOW-LABS-0001-ST-06` | `Minimal evidence retention` | `active` | `introduced` | `S0B-1A-R02` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `2026-02-08T09:14:31Z` | `ongoing` | `in-force` | Each lab should keep only one minimal evidence set needed to replay or verify the conclusion confidently. | Minimal-retention clause directly linked to the retained ledger row. |
| `DOC-WORKFLOW-LABS-0001-ST-07` | `Cleanup retention boundary` | `active` | `introduced` | `S0B-1A-R02` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `2026-02-08T09:14:31Z` | `ongoing` | `in-force` | Cleanup decisions must still preserve the minimum evidence set needed to replay or verify the conclusion confidently. | Narrower cleanup-boundary clause split out from the earlier combined cleanup sample. |
| `DOC-WORKFLOW-LABS-0001-ST-08` | `Safe-to-purge cleanup` | `active` | `introduced` | `S0B-1A-R03` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `2026-02-08T09:14:31Z` | `ongoing` | `in-force` | Once conclusions are codified into repeatable scripts and verifiable assertions, historical diff/ad-hoc artifacts should become safe to purge rather than remain indefinitely. | Safe-to-purge cleanup clause now stands on its own direct evidence basis. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LABS-0001-CH-01` | `DOC-WORKFLOW-LABS-0001` | `split` | `DOC-WORKFLOW-LABS-0001-ST-07-draft-combined` | `DOC-WORKFLOW-LABS-0001-ST-07; DOC-WORKFLOW-LABS-0001-ST-08` | `2026-02-08T09:14:31Z` | `2026-04-11` | The earlier combined cleanup clause mixed retention boundary and purge semantics too tightly for clean review, so it was decomposed into two narrower clauses. | `S0B-1A-R02; S0B-1A-R03` | Sample split event: statement lineage is recorded here, while the statement table now keeps only the current narrower clauses. |

## Release Change

- This release preserves the first labs-family contract extracted from `S0B-1A`.
- The current repair does not change the owned meaning; it aligns the file to the current chronology-first contract structure and fixed-width release numbering.
- The semantic start of this historical release is now anchored to the source issue creation time `2026-02-08T09:14:31Z`, while the release record itself entered repo chronology later on `2026-04-11`.
- The release continues to own labs-layer governance for:
  - snapshot asset classes
  - minimal retained evidence
  - cleanup boundaries
  - safe-to-purge discipline after conclusions are codified

## Contract Statement

- The table above is the clause registry for this release; the readable statement below preserves the same effective meaning in prose form.
- `DOC-WORKFLOW-LABS-001-ST-01`: Lab snapshot folders must be governed as test assets rather than left to accumulate as an unbounded debugging heap.
- `DOC-WORKFLOW-LABS-001-ST-02`: Snapshot outputs should be classified into explicit roles:
  - `DOC-WORKFLOW-LABS-001-ST-03`: `Golden fixtures` are small, high-signal retained artifacts that stay in git as the replayable regression baseline.
  - `DOC-WORKFLOW-LABS-001-ST-04`: `Diff snapshots` are short-lived comparison artifacts used during iteration and removable once conclusions are stabilized.
  - `DOC-WORKFLOW-LABS-001-ST-05`: `Ad-hoc dumps` are disposable debugging output that should not become retained contract evidence by default.
- `DOC-WORKFLOW-LABS-001-ST-06`: Each lab should keep only one minimal evidence set needed to replay or verify the conclusion confidently.
  - `DOC-WORKFLOW-LABS-001-ST-07`: Cleanup decisions must still preserve the minimum evidence set needed to replay or verify the conclusion confidently.
  - `DOC-WORKFLOW-LABS-001-ST-08`: Once conclusions are codified into repeatable scripts and verifiable assertions, historical diff/ad-hoc artifacts should become safe to purge rather than remain indefinitely.

## Current Reading

- Read this contract when the question is `what labs-layer rule governed snapshots, retention, and cleanup before later drills or observability replacements appeared?`
- Read the broader workflow contract first only if the reader still needs the higher-level `log -> lab -> runbook -> adr` pipeline boundary.

## Reader Notes

- This draft is sourced from issue `S0B/1A`, not from a local source log.
- It intentionally captures the labs/snapshots governance layer as its own contract rather than hiding it inside the broader `DOC-WORKFLOW-0001` contract.
- `DOC-WORKFLOW-LABS` now reads as one narrower workflow family, not as a split child release from `DOC-WORKFLOW-0001`.
- The `Contract Statement Table` demonstrates one clause-level registry model: source routing still lives in the parent ledger, while the contract keeps one long-form statement id plus one short statement label per effective clause.
- The `Statement Evolution Table` demonstrates the paired clause-history model: `source basis` stays evidence-facing, while split/merge/replacement history is recorded as statement lineage rather than packed into the basis field.
- The file now uses the current fixed-width release numbering and chronology-first metadata fields while preserving the same first release meaning.