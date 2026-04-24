# DOC-WORKFLOW-LABS-0002 labs snapshot evidence package governance

```yaml
contract_record:
  contract_family: DOC-WORKFLOW-LABS
  contract_release: 0002
  contract_id: DOC-WORKFLOW-LABS-0002
  record_kind: chronology-first-contract
  status: draft
  release_action: simple-revision
  release_change_summary: Keep the later S0B-2A snapshot-package revision as the current release while also admitting the accepted S0A-2A-R03 labs packet as history-backfilled earlier-labs clauses inside the same current reader.
  summary: Govern workflow labs as replayable evidence packages, including earlier pre-runbook failure-management and projection-closure labs plus later snapshot-root, run-folder, and retention-package rules.
  owner_team: docs-governance
  current_steward: delegated:workflow-labs-contract-maintainer
  approval_state: reviewed-awaiting-approval
  reviewed_by: role:workflow-reviewer
  approved_by: role:docs-governance-approver
  governance_area: workflow labs historical evidence, snapshot governance, and evidence-package governance
  applies_to: earlier executable labs that precede runbook codification, labs snapshot roots, run-id evidence folders, retained lab evidence sets, golden fixtures, diff snapshots, ad-hoc dumps, and lab cleanup decisions
  enforcement_surface: manual
  violation_semantics: warning
  recorded_at: 2026-04-10
  reviewed_at: pending
  effective_from: 2026-02-13
  effective_until: ongoing
  introduced_by: GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
  last_changed_by: docs/logs/support-only/ledger-SUP-S0A-2A-002-labs-early-failure-management-and-pre-drills-shape.md
  source_refs:
    - docs/logs/log-S0B-2A-scripts-snapshots-management.md
    - docs/logs/support-only/ledger-SUP-S0A-2A-002-labs-early-failure-management-and-pre-drills-shape.md
  cumulative_source_refs:
    - GitHub issue S0B/1A (#36) (issue-only source; no local log exists in workspace)
    - docs/logs/log-S0B-2A-scripts-snapshots-management.md
    - docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md
    - docs/logs/support-only/ledger-SUP-S0A-2A-002-labs-early-failure-management-and-pre-drills-shape.md
  supporting_evidence_refs:
    - docs/logs/support-only/ledger-S0B-1A-tools-labs-and-snapshots.md
    - docs/logs/support-only/ledger-S0B-2A-tools-scripts-and-snapshots-management.md
    - legacy/from_structured_docs/from-logs/v2-logs/log-S3A-lab-snapshots-management.md
    - legacy/from_structured_docs/from-labs/labs-004-worker-failure-management-v1-v4.md
    - legacy/from_structured_docs/from-labs/labs-006-search-projection-search-index-to-elastic.md
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
    - This local draft also carries one accepted earlier-labs history bucket from `S0A-2A-R03` without opening a separate historical-backfill release yet.
    - The broader `DOC-WORKFLOW` family path remains taxonomy only; this release does not claim one split lineage from `DOC-WORKFLOW-0001`.
    - The local repo still has no direct S0B/1A source log, so the family continues to carry issue-only sourcing from that first release alongside the later S0B-2A log source.
    - `effective_from` is anchored to the later `S0B-2A` source log date `2026-02-13` because `0002` is the release where the labs family first absorbs the snapshot-policy evidence-package semantics, even though some history-backfilled clauses inside the same current reader preserve earlier defended dates.
```

## Current Governance State

- The current effective governance state of this contract is carried in frontmatter through `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by`.
- Older fields such as `introduced_by`, `last_changed_by`, `source_refs`, and `cumulative_source_refs` remain chronology/source metadata for this release family; they should not be read as current ownership or approval identity.
- This contract therefore acts as the narrow current-state governance surface for the active `DOC-WORKFLOW-LABS-0002` release reader, while the parent ledger and `SUP-002` preserve the route and evidence-history chain that led here.
- The current steward is intentionally delegated rather than implicitly identical to the owner team, which keeps day-to-day labs contract maintenance distinct from durable family ownership.

## Governance Event Table

| event id | event kind | affected surface | actor value | effective state impact | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LABS-0002-GOV-01` | `contribution-event` | `DOC-WORKFLOW-LABS family` | `unknown` | `none-current-state` | `2026-02-13` | `GitHub issue S0B/1A (#36); docs/logs/log-S0B-2A-scripts-snapshots-management.md` | The earlier issue-only labs packet and the later S0B-2A log remain the defended contribution sources for the current family reader, with the later `0002` release start anchored to the S0B-2A source-log date rather than to the later repo recording date. |
| `DOC-WORKFLOW-LABS-0002-GOV-02` | `evidence-sharpening-event` | `DOC-WORKFLOW-LABS-0002` | `role:packet-reviewer` | `labs-direct-evidence-review-fixed` | `2026-04-12` | `ledger-SUP-S0A-2A-002-labs-early-failure-management-and-pre-drills-shape.md` | The accepted labs SUP round fixed the earlier-labs slice as a defended historical-review surface inside the active `0002` reader without changing durable owner-team identity. |
| `DOC-WORKFLOW-LABS-0002-GOV-03` | `delegated-stewardship-event` | `DOC-WORKFLOW-LABS-0002` | `role:docs-governance-approver` | `current-steward-delegated` | `2026-04-15` | `S0F-9A/P4 scoped backfill round` | Stewardship for the current labs contract reader is now explicitly delegated to the narrower labs contract maintainer role while final approval remains with the broader docs-governance approver role. |
| `DOC-WORKFLOW-LABS-0002-GOV-04` | `review-approval-separation-event` | `DOC-WORKFLOW-LABS-0002` | `role:workflow-reviewer; role:docs-governance-approver` | `reviewed-awaiting-approval-state-fixed` | `2026-04-15` | `S0F-9A/P4 scoped backfill round` | The current contract state now records review and approval as distinct governance actions instead of leaving both roles implicit or collapsed into one reviewer identity. |

## Contract Statement Table

| statement id | statement label | clause status | change action | source basis | first effective release | first effective at | last changed release | last changed at | effective from | effective until | effective status | statement text | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LABS-0002-ST-12` | `Pre-runbook failure-management labs` | `active` | `history-backfilled` | `S0A-2A-R03-SUP-01` | `DOC-WORKFLOW-LABS-0002` | `2026-02-03` | `DOC-WORKFLOW-LABS-0002` | `2026-04-12` | `2026-02-03` | `ongoing` | `in-force` | Labs may own executable failure-management experiments for stuck recovery, retry convergence, replay, failed-state auditability, and daemon runtime engineering before those lessons are later distilled into runbooks. | Later-recorded earlier clause admitted from the accepted `S0A-2A-R03` labs packet without opening a separate backfill release yet. |
| `DOC-WORKFLOW-LABS-0002-ST-13` | `Projection-closure labs before runbook codification` | `active` | `history-backfilled` | `S0A-2A-R03-SUP-02` | `DOC-WORKFLOW-LABS-0002` | `unknown` | `DOC-WORKFLOW-LABS-0002` | `2026-04-12` | `unknown` | `ongoing` | `in-force` | Labs may also own projection-closure and source-to-read-model validation work before those earlier experimental findings are reorganized into later operator-facing runbook codification. | This keeps the earlier search-projection closure labs visible as labs-family history rather than treating them as only pre-runbook background. |
| `DOC-WORKFLOW-LABS-0002-ST-08` | `Snapshot class taxonomy` | `active` | `carried-forward` | `S0B-1A-R01` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `2026-02-08T09:14:31Z` | `ongoing` | `in-force` | Snapshot outputs inside that package should still be classified into explicit roles: golden fixtures, diff snapshots, and ad-hoc dumps. | The taxonomy remains materially present in `0002`, but now reads inside the evidence-package framing. |
| `DOC-WORKFLOW-LABS-0002-ST-10` | `Safe-to-purge cleanup` | `active` | `carried-forward` | `S0B-1A-R03` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `2026-02-08T09:14:31Z` | `ongoing` | `in-force` | Once conclusions are codified into repeatable scripts and verifiable assertions, historical diff/ad-hoc artifacts should become safe to purge rather than remain indefinitely. | Earlier cleanup rule remains materially present without needing one new direct labs source beyond the carried-forward family state. |
| `DOC-WORKFLOW-LABS-0002-ST-01` | `Labs as replayable evidence packages` | `active` | `amended` | `S0B-1A-R01; S0B-2A-R03` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | Labs outputs must be governed as replayable evidence packages rather than left to accumulate as an unbounded debugging heap. | Later release restates the earlier labs-as-test-assets framing in the stronger evidence-package language introduced by the labs sub-slice from `S0B-2A`. |
| `DOC-WORKFLOW-LABS-0002-ST-09` | `Minimal evidence package retention` | `active` | `amended` | `S0B-1A-R02; S0B-2A-R03` | `DOC-WORKFLOW-LABS-0001` | `2026-02-08T09:14:31Z` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | Each lab should keep only the minimum evidence package needed to replay or verify the conclusion confidently. | Earlier minimal-retention rule is widened from evidence set to evidence package in the later release. |
| `DOC-WORKFLOW-LABS-0002-ST-02` | `Stable labs evidence root` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | Labs evidence should land under one stable root: `docs/labs/_snapshot/`. | New clause introduced by the absorbed labs sub-slice. |
| `DOC-WORKFLOW-LABS-0002-ST-03` | `Run-id evidence package` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | Each run should produce one bounded run-id folder that makes the evidence package readable and auditable. | Parent run-folder clause for the new evidence-package shape. |
| `DOC-WORKFLOW-LABS-0002-ST-04` | `Exports subfolder` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | The evidence package should provide `_exports/` for trace or external exports such as Jaeger output. | Narrow child clause beneath the run-id evidence-package rule. |
| `DOC-WORKFLOW-LABS-0002-ST-05` | `Logs subfolder` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | The evidence package should provide `_logs/` for stdout, stderr, or other captured run logs. | Narrow child clause beneath the run-id evidence-package rule. |
| `DOC-WORKFLOW-LABS-0002-ST-06` | `Metrics subfolder` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | The evidence package should provide `_metrics/` for metrics or query output that should not be recopied by hand. | Narrow child clause beneath the run-id evidence-package rule. |
| `DOC-WORKFLOW-LABS-0002-ST-07` | `Notes subfolder` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | The evidence package should provide `_notes.md` for acceptance checks, conclusions, and next steps. | Narrow child clause beneath the run-id evidence-package rule. |
| `DOC-WORKFLOW-LABS-0002-ST-11` | `Replay-and-audit retention test` | `active` | `introduced` | `S0B-2A-R03` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `DOC-WORKFLOW-LABS-0002` | `2026-02-13` | `2026-02-13` | `ongoing` | `in-force` | Retention decisions should preserve replay and audit value, not file volume for its own sake. | New retention-judgment clause introduced by the absorbed labs sub-slice. |

## Statement Evolution Table

| change id | release id | change action | input statement ids | output statement ids | effective at | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-WORKFLOW-LABS-0002-CH-06` | `DOC-WORKFLOW-LABS-0002` | `history-backfilled` | `none` | `DOC-WORKFLOW-LABS-0002-ST-12` | `2026-02-03` | `2026-04-12` | The accepted `S0A-2A-R03` labs packet shows that executable failure-management labs materially belonged to the labs family before later runbook codification, so the current release now keeps that earlier-history clause visible rather than treating it as only background. | `S0A-2A-R03-SUP-01` | This is recorded inside the current release reader pending any later decision to open a dedicated historical-backfill release. |
| `DOC-WORKFLOW-LABS-0002-CH-07` | `DOC-WORKFLOW-LABS-0002` | `history-backfilled` | `none` | `DOC-WORKFLOW-LABS-0002-ST-13` | `unknown` | `2026-04-12` | The accepted `S0A-2A-R03` search-projection closure labs packet shows one earlier labs-specific rule shape that should remain visible even though later runbooks took over the operator-facing codified reader. | `S0A-2A-R03-SUP-02` | This keeps the earlier labs-versus-runbook boundary readable inside the current `0002` contract sample. |
| `DOC-WORKFLOW-LABS-0002-CH-03` | `DOC-WORKFLOW-LABS-0002` | `carried-forward` | `DOC-WORKFLOW-LABS-001-ST-02; DOC-WORKFLOW-LABS-001-ST-03; DOC-WORKFLOW-LABS-001-ST-04; DOC-WORKFLOW-LABS-001-ST-05` | `DOC-WORKFLOW-LABS-0002-ST-08` | `2026-02-08T09:14:31Z` | `2026-04-10` | The earlier snapshot-class taxonomy remains in force inside the later evidence-package framing. | `S0B-1A-R01` | The later release condenses the earlier taxonomy cluster into one current-release parent clause while leaving the narrower earlier release available for readers who need its first statement decomposition. |
| `DOC-WORKFLOW-LABS-0002-CH-05` | `DOC-WORKFLOW-LABS-0002` | `carried-forward` | `DOC-WORKFLOW-LABS-001-ST-08` | `DOC-WORKFLOW-LABS-0002-ST-10` | `2026-02-08T09:14:31Z` | `2026-04-10` | The earlier safe-to-purge rule remains materially present in the later release. | `S0B-1A-R03` | Carried-forward clauses still receive new release-local statement ids in the later release. |
| `DOC-WORKFLOW-LABS-0002-CH-01` | `DOC-WORKFLOW-LABS-0002` | `amended` | `DOC-WORKFLOW-LABS-001-ST-01` | `DOC-WORKFLOW-LABS-0002-ST-01` | `2026-02-13` | `2026-04-10` | The later release reframes labs outputs from general test assets into replayable evidence packages because the absorbed `S0B-2A` labs sub-slice makes package semantics explicit. | `S0B-1A-R01; S0B-2A-R03` | The clause keeps the earlier labs-asset boundary while adopting the stronger later wording. |
| `DOC-WORKFLOW-LABS-0002-CH-04` | `DOC-WORKFLOW-LABS-0002` | `amended` | `DOC-WORKFLOW-LABS-001-ST-06; DOC-WORKFLOW-LABS-001-ST-07` | `DOC-WORKFLOW-LABS-0002-ST-09` | `2026-02-13` | `2026-04-10` | The later release widens minimal retention from one evidence set into one evidence package. | `S0B-1A-R02; S0B-2A-R03` | This later clause keeps the earlier retention boundary while adopting the package vocabulary from `S0B-2A`. |
| `DOC-WORKFLOW-LABS-0002-CH-02` | `DOC-WORKFLOW-LABS-0002` | `introduced` | `none` | `DOC-WORKFLOW-LABS-0002-ST-02; DOC-WORKFLOW-LABS-0002-ST-03; DOC-WORKFLOW-LABS-0002-ST-04; DOC-WORKFLOW-LABS-0002-ST-05; DOC-WORKFLOW-LABS-0002-ST-06; DOC-WORKFLOW-LABS-0002-ST-07; DOC-WORKFLOW-LABS-0002-ST-11` | `2026-02-13` | `2026-04-10` | The absorbed labs-only `S0B-2A` slice adds new evidence-root, package-shape, and replay-or-audit retention clauses that were absent from `0001`. | `S0B-2A-R03` | These are genuinely new release-local statement ids because statement ids are release-scoped rather than family-global. |

## Release Change

- This release supersedes `DOC-WORKFLOW-LABS-0001` by keeping its earlier snapshot-governance core while adding the labs-only slice from `S0B-2A` that makes the evidence-package layout explicit.
- This local draft also keeps the accepted `S0A-2A-R03` labs packet inside the current release as `history-backfilled` clause state rather than opening a separate historical-backfill release first.
- The current `0002` release now anchors its own semantic start to the later `S0B-2A` source-log date `2026-02-13`, while still preserving earlier defended clause history inside the same reader: `ST-12` keeps the narrower earlier labs date `2026-02-03`, and `ST-13` remains chronology-incomplete because current upstream evidence still does not defend one timestamp for that historical projection-closure slice.
- Relative to `0001`, this release now fixes three additional points:
  - earlier executable labs for failure management and projection closure remain readable as labs-family history before their later runbook codification
  - labs outputs should land under one stable evidence root: `docs/labs/_snapshot/`
  - each execution should produce one per-run folder with a repeatable evidence-package shape rather than one loose pile of files
  - retention and cleanup should be judged against the package's replay and audit value, not against ad hoc file accumulation
- This release intentionally does not absorb the broader scripts taxonomy, stable entrypoint, runbook snapshot-root split, cutover rules, or stub policy from the `S0B-2A` ledger draft.

## Contract Statement

- The tables above now separate current clause state from clause lineage; the readable statement below preserves the same current effective meaning in prose form.
- `DOC-WORKFLOW-LABS-0002-ST-12`: Labs may own executable failure-management experiments before those lessons are later distilled into runbooks.
- `DOC-WORKFLOW-LABS-0002-ST-13`: Labs may also own projection-closure and source-to-read-model validation work before those earlier findings are reorganized into later runbook codification.
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

## Current Reader Shape

- This file is one narrow current labs-family reader, not a broad parent contract with child-boundary delegation decisions like `DOC-WORKFLOW-0001`.
- Read the current clause set here in three layers:
  - `history-backfilled`: earlier pre-runbook labs history admitted into the current reader from `S0A-2A-R03`
  - `carried-forward` and `amended`: earlier labs-family rule bodies from `DOC-WORKFLOW-LABS-0001` that remain materially present in the current release
  - `introduced`: new evidence-package clauses added by the labs-specific `S0B-2A` slice
- Under this reader model, the contract does not need one parent-style `Current Boundary Map` because the problem here is not `who owns the narrow body now`; it is `which current clauses came from earlier history versus later family revision`.
- That chronology is therefore intentionally kept in `Statement Evolution Table` and reinforced in `Current Reading` and `Reader Notes`, rather than duplicated through one second boundary-ownership table.

## Current Reading

- Read this release when the question is `what is the current integrated labs-family reader once earlier pre-runbook labs history and later snapshot-package governance are both kept visible in one release?`
- Read `Current Reader Shape` first when the question is `why are history-backfilled, carried-forward, amended, and introduced clauses all visible together in one current reader, and how should that mix be interpreted?`
- Read `DOC-WORKFLOW-LABS-0001` only when the reader needs the narrower earlier release before the `S0B-2A` snapshot-policy slice was absorbed into the labs family.
- Read the `S0B-2A` ledger draft when the question is `which parts of S0B-2A entered this release and which parts remained deferred or support-only?`
- Read the accepted `S0A-2A` labs supplement packet when the question is `which earlier labs history was backfilled into the current release reader and why was it not left only as runbook prehistory?`

## Reader Notes

- This draft is the first release-style sample under the `family + release` model; it is not committed as the accepted next state yet.
- It intentionally fuses the earlier labs-family contract with only the labs-specific `S0B-2A` slice that strengthens snapshot and evidence-package governance.
- It now also demonstrates one second pattern under `S0F-7E`: a current later release may temporarily host `history-backfilled` clause rows from an earlier accepted ledger packet before the repo decides whether a dedicated historical-backfill release is still necessary.
- The mixed current clause set here is deliberate: the release is meant to be one integrated current labs reader, not one parent/child boundary map, so chronology stays in the evolution table rather than in a second ownership table.
- It does not yet claim to resolve the future `workflow/scripts governance` family question or the possible OPS-side evidence family question tracked in the ledger.
- The statement ids in this file are intentionally release-local `0002-ST-*` ids; earlier `0001-ST-*` ids remain history anchors in the statement-evolution table rather than being reused as the current ids.