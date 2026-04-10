# DOC-WORKFLOW-LABS-0002 labs snapshot evidence package governance

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-LABS
  contract_release: 0002
  contract_id: DOC-WORKFLOW-LABS-0002
  record_kind: chronology-first-contract
  status: draft
  release_action: simple-revision
  release_change_summary: Extend the first labs-family release by absorbing the labs-only snapshot-policy slice from S0B-2A, so the family now governs not only snapshot classes and purge semantics but also the evidence-root layout and per-run evidence-package shape.
  summary: Govern labs outputs as replayable evidence packages with one stable labs snapshot root, one per-run evidence folder shape, explicit snapshot classes, and minimal-retention cleanup rules.
  governance_area: workflow labs snapshot and evidence-package governance
  applies_to: labs snapshot roots, run-id evidence folders, retained lab evidence sets, golden fixtures, diff snapshots, ad-hoc dumps, and lab cleanup decisions
  enforcement_surface: manual
  violation_semantics: warning
  introduced_by: GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
  last_changed_by: docs/logs/log-S0B-2A-scripts-snapshots-management.md
  source_refs:
    - docs/logs/log-S0B-2A-scripts-snapshots-management.md
    - GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
  cumulative_source_refs:
    - GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
    - docs/logs/log-S0B-2A-scripts-snapshots-management.md
  supporting_evidence_refs:
    - legacy/from_structured_docs/from-logs/v2-logs/log-S3A-lab-snapshots-management.md
  lineage:
    supersedes:
      - DOC-WORKFLOW-LABS-0001
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This draft keeps the stable DOC-WORKFLOW-LABS family and treats 0002 as the later effective release state.
    - This release intentionally absorbs only the labs-specific slice from S0B-2A rather than the full scripts-taxonomy or cutover material tracked in the ledger.
    - The broader `DOC-WORKFLOW` family path remains taxonomy only; this release does not claim one split lineage from `DOC-WORKFLOW-0001`.
    - The local repo still has no direct S0B/1A source log, so the family continues to carry issue-only sourcing from that first release alongside the later S0B-2A log source.
```

## Release Change

- This release supersedes `DOC-WORKFLOW-LABS-0001` by keeping its earlier snapshot-governance core while adding the labs-only slice from `S0B-2A` that makes the evidence-package layout explicit.
- Relative to `0001`, this release now fixes three additional points:
  - labs outputs should land under one stable evidence root: `docs/labs/_snapshot/`
  - each execution should produce one per-run folder with a repeatable evidence-package shape rather than one loose pile of files
  - retention and cleanup should be judged against the package's replay and audit value, not against ad hoc file accumulation
- This release intentionally does not absorb the broader scripts taxonomy, stable entrypoint, runbook snapshot-root split, cutover rules, or stub policy from the `S0B-2A` ledger draft.

## Contract Statement

- Labs outputs must be governed as replayable evidence packages rather than left to accumulate as an unbounded debugging heap.
- Labs evidence should land under one stable root:
  - `docs/labs/_snapshot/`
- Each run should produce one bounded run-id folder that makes the evidence package readable and auditable, typically including:
  - `_exports/` for trace or external exports such as Jaeger output
  - `_logs/` for stdout, stderr, or other captured run logs
  - `_metrics/` for metrics or query output that should not be recopied by hand
  - `_notes.md` for acceptance checks, conclusions, and next steps
- Snapshot outputs inside that package should still be classified into explicit roles:
  - `Golden fixtures`: small, high-signal retained artifacts that stay in git as the replayable regression baseline
  - `Diff snapshots`: short-lived comparison artifacts used during iteration and removable once conclusions are stabilized
  - `Ad-hoc dumps`: disposable debugging output that should not become retained contract evidence by default
- Each lab should keep only the minimum evidence package needed to replay or verify the conclusion confidently.
- Once conclusions are codified into repeatable scripts and verifiable assertions, historical diff/ad-hoc artifacts should become safe to purge rather than remain indefinitely.
- Retention decisions should preserve replay and audit value, not file volume for its own sake.

## Current Reading

- Read this release when the question is `what is the later labs-family rule once labs snapshot governance also fixes the evidence-root and per-run evidence-package layout?`
- Read `DOC-WORKFLOW-LABS-0001` only when the reader needs the narrower earlier release before the `S0B-2A` snapshot-policy slice was absorbed into the labs family.
- Read the `S0B-2A` ledger draft when the question is `which parts of S0B-2A entered this release and which parts remained deferred or support-only?`

## Reader Notes

- This draft is the first release-style sample under the `family + release` model; it is not committed as the accepted next state yet.
- It intentionally fuses the earlier labs-family contract with only the labs-specific `S0B-2A` slice that strengthens snapshot and evidence-package governance.
- It does not yet claim to resolve the future `workflow/scripts governance` family question or the possible OPS-side evidence family question tracked in the ledger.