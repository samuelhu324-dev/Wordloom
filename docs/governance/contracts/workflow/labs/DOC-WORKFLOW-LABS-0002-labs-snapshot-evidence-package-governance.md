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
    - docs/logs/support-only/ledger-S0B-1A-tools-labs-and-snapshots.md
    - docs/logs/support-only/ledger-S0B-2A-tools-scripts-and-snapshots-management.md
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

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | last changed release | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LABS-0002-ST-08` | `Snapshot class taxonomy` | `active` | `carried-forward` | `S0B-1A-R01` | `DOC-WORKFLOW-LABS-0001` | `DOC-WORKFLOW-LABS-0001` | `in-force` | Snapshot outputs inside that package should still be classified into explicit roles: golden fixtures, diff snapshots, and ad-hoc dumps. | The taxonomy remains materially present in `0002`, but now reads inside the evidence-package framing. |
| `DOC-WORKFLOW-LABS-0002-ST-10` | `Safe-to-purge cleanup` | `active` | `carried-forward` | `S0B-1A-R03` | `DOC-WORKFLOW-LABS-0001` | `DOC-WORKFLOW-LABS-0001` | `in-force` | Once conclusions are codified into repeatable scripts and verifiable assertions, historical diff/ad-hoc artifacts should become safe to purge rather than remain indefinitely. | Earlier cleanup rule remains materially present without needing one new direct labs source beyond the carried-forward family state. |
| `DOC-WORKFLOW-LABS-0002-ST-01` | `Labs as replayable evidence packages` | `active` | `amended` | `S0B-1A-R01; S0B-2A-R03` | `DOC-WORKFLOW-LABS-0001` | `DOC-WORKFLOW-LABS-0002` | `in-force` | Labs outputs must be governed as replayable evidence packages rather than left to accumulate as an unbounded debugging heap. | Later release restates the earlier labs-as-test-assets framing in the stronger evidence-package language introduced by the labs sub-slice from `S0B-2A`. |
| `DOC-WORKFLOW-LABS-0002-ST-09` | `Minimal evidence package retention` | `active` | `amended` | `S0B-1A-R02; S0B-2A-R03` | `DOC-WORKFLOW-LABS-0001` | `DOC-WORKFLOW-LABS-0002` | `in-force` | Each lab should keep only the minimum evidence package needed to replay or verify the conclusion confidently. | Earlier minimal-retention rule is widened from evidence set to evidence package in the later release. |
| `DOC-WORKFLOW-LABS-0002-ST-02` | `Stable labs evidence root` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `DOC-WORKFLOW-LABS-0002` | `in-force` | Labs evidence should land under one stable root: `docs/labs/_snapshot/`. | New clause introduced by the absorbed labs sub-slice. |
| `DOC-WORKFLOW-LABS-0002-ST-03` | `Run-id evidence package` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `DOC-WORKFLOW-LABS-0002` | `in-force` | Each run should produce one bounded run-id folder that makes the evidence package readable and auditable. | Parent run-folder clause for the new evidence-package shape. |
| `DOC-WORKFLOW-LABS-0002-ST-04` | `Exports subfolder` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `DOC-WORKFLOW-LABS-0002` | `in-force` | The evidence package should provide `_exports/` for trace or external exports such as Jaeger output. | Narrow child clause beneath the run-id evidence-package rule. |
| `DOC-WORKFLOW-LABS-0002-ST-05` | `Logs subfolder` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `DOC-WORKFLOW-LABS-0002` | `in-force` | The evidence package should provide `_logs/` for stdout, stderr, or other captured run logs. | Narrow child clause beneath the run-id evidence-package rule. |
| `DOC-WORKFLOW-LABS-0002-ST-06` | `Metrics subfolder` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `DOC-WORKFLOW-LABS-0002` | `in-force` | The evidence package should provide `_metrics/` for metrics or query output that should not be recopied by hand. | Narrow child clause beneath the run-id evidence-package rule. |
| `DOC-WORKFLOW-LABS-0002-ST-07` | `Notes subfolder` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `DOC-WORKFLOW-LABS-0002` | `in-force` | The evidence package should provide `_notes.md` for acceptance checks, conclusions, and next steps. | Narrow child clause beneath the run-id evidence-package rule. |
| `DOC-WORKFLOW-LABS-0002-ST-11` | `Replay-and-audit retention test` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `DOC-WORKFLOW-LABS-0002` | `in-force` | Retention decisions should preserve replay and audit value, not file volume for its own sake. | New retention-judgment clause introduced by the absorbed labs sub-slice. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LABS-0002-CH-01` | `DOC-WORKFLOW-LABS-0002` | `amended` | `DOC-WORKFLOW-LABS-001-ST-01` | `DOC-WORKFLOW-LABS-0002-ST-01` | The later release reframes labs outputs from general test assets into replayable evidence packages because the absorbed `S0B-2A` labs sub-slice makes package semantics explicit. | `S0B-1A-R01; S0B-2A-R03` | The clause keeps the earlier labs-asset boundary while adopting the stronger later wording. |
| `DOC-WORKFLOW-LABS-0002-CH-02` | `DOC-WORKFLOW-LABS-0002` | `introduced` | `none` | `DOC-WORKFLOW-LABS-0002-ST-02; DOC-WORKFLOW-LABS-0002-ST-03; DOC-WORKFLOW-LABS-0002-ST-04; DOC-WORKFLOW-LABS-0002-ST-05; DOC-WORKFLOW-LABS-0002-ST-06; DOC-WORKFLOW-LABS-0002-ST-07; DOC-WORKFLOW-LABS-0002-ST-11` | The absorbed labs-only `S0B-2A` slice adds new evidence-root, package-shape, and replay-or-audit retention clauses that were absent from `0001`. | `S0B-2A-R03` | These are genuinely new release-local statement ids because statement ids are release-scoped rather than family-global. |
| `DOC-WORKFLOW-LABS-0002-CH-03` | `DOC-WORKFLOW-LABS-0002` | `carried-forward` | `DOC-WORKFLOW-LABS-001-ST-02; DOC-WORKFLOW-LABS-001-ST-03; DOC-WORKFLOW-LABS-001-ST-04; DOC-WORKFLOW-LABS-001-ST-05` | `DOC-WORKFLOW-LABS-0002-ST-08` | The earlier snapshot-class taxonomy remains in force inside the later evidence-package framing. | `S0B-1A-R01` | The later release condenses the earlier taxonomy cluster into one current-release parent clause while leaving the narrower earlier release available for readers who need its first statement decomposition. |
| `DOC-WORKFLOW-LABS-0002-CH-04` | `DOC-WORKFLOW-LABS-0002` | `amended` | `DOC-WORKFLOW-LABS-001-ST-06; DOC-WORKFLOW-LABS-001-ST-07` | `DOC-WORKFLOW-LABS-0002-ST-09` | The later release widens minimal retention from one evidence set into one evidence package. | `S0B-1A-R02; S0B-2A-R03` | This later clause keeps the earlier retention boundary while adopting the package vocabulary from `S0B-2A`. |
| `DOC-WORKFLOW-LABS-0002-CH-05` | `DOC-WORKFLOW-LABS-0002` | `carried-forward` | `DOC-WORKFLOW-LABS-001-ST-08` | `DOC-WORKFLOW-LABS-0002-ST-10` | The earlier safe-to-purge rule remains materially present in the later release. | `S0B-1A-R03` | Carried-forward clauses still receive new release-local statement ids in the later release. |

## Release Change

- This release supersedes `DOC-WORKFLOW-LABS-0001` by keeping its earlier snapshot-governance core while adding the labs-only slice from `S0B-2A` that makes the evidence-package layout explicit.
- Relative to `0001`, this release now fixes three additional points:
  - labs outputs should land under one stable evidence root: `docs/labs/_snapshot/`
  - each execution should produce one per-run folder with a repeatable evidence-package shape rather than one loose pile of files
  - retention and cleanup should be judged against the package's replay and audit value, not against ad hoc file accumulation
- This release intentionally does not absorb the broader scripts taxonomy, stable entrypoint, runbook snapshot-root split, cutover rules, or stub policy from the `S0B-2A` ledger draft.

## Contract Statement

- The tables above now separate current clause state from clause lineage; the readable statement below preserves the same current effective meaning in prose form.
- `DOC-WORKFLOW-LABS-0002-ST-01`: Labs outputs must be governed as replayable evidence packages rather than left to accumulate as an unbounded debugging heap.
- `DOC-WORKFLOW-LABS-0002-ST-02`: Labs evidence should land under one stable root: `docs/labs/_snapshot/`.
- `DOC-WORKFLOW-LABS-0002-ST-03`: Each run should produce one bounded run-id folder that makes the evidence package readable and auditable, typically including:
  - `DOC-WORKFLOW-LABS-0002-ST-04`: `_exports/` for trace or external exports such as Jaeger output.
  - `DOC-WORKFLOW-LABS-0002-ST-05`: `_logs/` for stdout, stderr, or other captured run logs.
  - `DOC-WORKFLOW-LABS-0002-ST-06`: `_metrics/` for metrics or query output that should not be recopied by hand.
  - `DOC-WORKFLOW-LABS-0002-ST-07`: `_notes.md` for acceptance checks, conclusions, and next steps.
- `DOC-WORKFLOW-LABS-0002-ST-08`: Snapshot outputs inside that package should still be classified into explicit roles: golden fixtures, diff snapshots, and ad-hoc dumps.
- `DOC-WORKFLOW-LABS-0002-ST-09`: Each lab should keep only the minimum evidence package needed to replay or verify the conclusion confidently.
- `DOC-WORKFLOW-LABS-0002-ST-10`: Once conclusions are codified into repeatable scripts and verifiable assertions, historical diff/ad-hoc artifacts should become safe to purge rather than remain indefinitely.
- `DOC-WORKFLOW-LABS-0002-ST-11`: Retention decisions should preserve replay and audit value, not file volume for its own sake.

## Current Reading

- Read this release when the question is `what is the later labs-family rule once labs snapshot governance also fixes the evidence-root and per-run evidence-package layout?`
- Read `DOC-WORKFLOW-LABS-0001` only when the reader needs the narrower earlier release before the `S0B-2A` snapshot-policy slice was absorbed into the labs family.
- Read the `S0B-2A` ledger draft when the question is `which parts of S0B-2A entered this release and which parts remained deferred or support-only?`

## Reader Notes

- This draft is the first release-style sample under the `family + release` model; it is not committed as the accepted next state yet.
- It intentionally fuses the earlier labs-family contract with only the labs-specific `S0B-2A` slice that strengthens snapshot and evidence-package governance.
- It does not yet claim to resolve the future `workflow/scripts governance` family question or the possible OPS-side evidence family question tracked in the ledger.
- The statement ids in this file are intentionally release-local `0002-ST-*` ids; earlier `0001-ST-*` ids remain history anchors in the statement-evolution table rather than being reused as the current ids.