# DOC-WORKFLOW-LABS-001 tools labs and snapshots

```yaml
contract_record:
  contract_id: DOC-WORKFLOW-LABS-001
  record_kind: chronology-first-contract
  status: draft
  summary: Treat lab snapshots as governed test assets with explicit classes, minimal retention, and safe-to-purge cleanup rules so iterative debugging does not collapse into either artifact hoarding or evidence loss.
  governance_area: workflow labs and snapshots governance
  applies_to: lab snapshot folders, retained lab evidence sets, golden fixtures, diff snapshots, ad-hoc dumps, and lab cleanup decisions
  enforcement_surface: manual
  violation_semantics: warning
  introduced_by: GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
  last_changed_by: GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
  source_refs:
    - GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
  supporting_evidence_refs:
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
    - This draft sits at the narrower `WORKFLOW-LABS` layer beneath the broader workflow pipeline contract.
    - The local repo currently has no S0B/1A source log, so this draft stays explicit about issue-only sourcing.
```

## Contract Statement

- Lab snapshot folders must be governed as test assets rather than left to accumulate as an unbounded debugging heap.
- Snapshot outputs should be classified into explicit roles:
  - `Golden fixtures`: small, high-signal retained artifacts that stay in git as the replayable regression baseline
  - `Diff snapshots`: short-lived comparison artifacts used during iteration and removable once conclusions are stabilized
  - `Ad-hoc dumps`: disposable debugging output that should not become retained contract evidence by default
- Each lab should keep only one minimal evidence set needed to replay or verify the conclusion confidently.
- Once conclusions are codified into repeatable scripts and verifiable assertions, historical diff/ad-hoc artifacts should become safe to purge rather than remain indefinitely.

## Current Reading

- Read this contract when the question is `what labs-layer rule governed snapshots, retention, and cleanup before later drills or observability replacements appeared?`
- Read the broader workflow contract first only if the reader still needs the higher-level `log -> lab -> runbook -> adr` pipeline boundary.

## Reader Notes

- This draft is sourced from issue `S0B/1A`, not from a local source log.
- It intentionally captures the labs/snapshots governance layer as its own contract rather than hiding it inside the broader `DOC-WORKFLOW-0001` contract.