# ledger-SUP-S3A-2A-001-legacy-failure-drills-and-early-s4a-lineage

```yaml
support_only_contract_release_ledger_supplement:
  supplement_series_id: ledger-SUP-S3A-2A
  supplement_sequence: 001
  supplement_id: ledger-SUP-S3A-2A-001-legacy-failure-drills-and-early-s4a-lineage
  supplement_kind: support-only-contract-release-ledger-supplement
  status: completed
  owner_lane: S4G-1E
  created_at: 2026-04-26
  reviewed_at: 2026-04-26
  accepted_at: 2026-04-26
  writeback_started_at: 2026-04-26
  writeback_completed_at: 2026-04-26
  parent_ledger_id: ledger-S3A-2A-combo-observability-triage
  parent_source_id: S3A-2A
  parent_source_ref: GitHub issue S3A-2A (#37) plus child issues #38, #39, #40, #41, #45, #46, #47, #48, #49, and #51
  supplement_scope: admit legacy observability triage, deterministic failure-drill, and early S4A daemon-lineage evidence for parent rows R02, R03, R04, and R06 without opening a separate code-driven contract lane
  target_reading_goal: show whether the surviving legacy logs and early issue lineage are strong enough to sharpen selected S3A-2A routing rows while keeping code-driven bridge meaning on downstream contract-local surfaces rather than on the SUP ledger itself
```

## Decision Frame

- This SUP ledger is attached only to parent rows `S3A-2A-R02`, `S3A-2A-R03`, `S3A-2A-R04`, and `S3A-2A-R06`.
- The review question for this round was narrow:
  - do the retained legacy logs and early S4A issues only add archaeology background
  - or do they sharpen the current parent-row reading enough that the parent ledger should stop reading those rows as issue-plus-later-survivor only
- This round keeps the current boundary intact:
  - source-owned routing and verdict refinement stay on the parent ledger plus this SUP
  - code-driven meaning stays on downstream contract-local surfaces such as attached row-flow ledgers, `Code Bridge Table`, and `Contract Coverage Table`
  - therefore no extra SUP-only columns or a separate template lane are required for code-driven contract layers in this packet

## Evidence Table

| supplement item id | parent row id | evidence ref | evidence type | attachment ids | verification status | effect on current verdict | proposed parent-ledger action | contract impact | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-2A-R02-SUP-01` | `S3A-2A-R02` | `legacy/from_structured_docs/from-logs/v2-logs/log-S2B-observability-triage.md` | `md` | `none` | `verified` | `sharpens-existing` | `rewrite-parent-row` | `defer-contract-change` | This retained triage log states the `metrics -> tracing -> structured logs` operating chain explicitly and names the shared-key split between low-cardinality pivots and high-cardinality forensic pivots, so `R02` no longer needs to read as issue support only. |
| `S3A-2A-R03-SUP-01` | `S3A-2A-R03` | `legacy/from_structured_docs/from-logs/v2-logs/log-S2C-observability-triage-failure-management.md` | `md` | `none` | `verified` | `sharpens-existing` | `rewrite-parent-row` | `defer-contract-change` | This retained failure-management log defends the outage-triage loop as one bounded reader surface rather than only as later lab support, so `R03` can be read as having direct legacy observability evidence. |
| `S3A-2A-R04-SUP-01` | `S3A-2A-R04` | `legacy/from_structured_docs/from-logs/v2-logs/log-S2C-1A-1A-expB-ES-429.md` | `md` | `none` | `verified` | `sharpens-existing` | `rewrite-parent-row` | `defer-contract-change` | This retained log preserves the deterministic ES-429 packet itself, including fault injection framing and evidence expectations, so the parent row should stop reading the deterministic path as issue-plus-lab only. |
| `S3A-2A-R04-SUP-02` | `S3A-2A-R04` | `legacy/from_structured_docs/from-logs/v2-logs/log-S2C-1A-labs-009-expB.md` | `md` | `none` | `verified` | `sharpens-existing` | `rewrite-parent-row` | `defer-contract-change` | This retained companion log keeps the `expB` packet tied to concrete lab execution shape, which strengthens the same deterministic injection row without forcing a new parent slice. |
| `S3A-2A-R06-SUP-01` | `S3A-2A-R06` | `GitHub issues #12, #16, and #31` | `issue` | `none` | `verified` | `sharpens-existing` | `rewrite-parent-row` | `defer-contract-change` | These earlier daemon and operability issues show that the later daemon-ready worker migration row already had a defended earlier runtime-engineering lineage, so `R06` should read as a sharpened lineage row rather than only one later local log plus one issue body. |

## Actor and Provenance Review Table

| supplement item id | submitted by | evidence owner | reviewed by | verified by | verification method | approved by | approval state | approval basis | provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-2A-R02-SUP-01` | `unknown` | `role:workflow-ledger-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-markdown-inspection` | `role:docs-governance-approver` | `accepted-for-packet` | The retained triage log is direct enough to sharpen the shared-key row at packet level. | The repo preserves the source markdown path and the packet review chain, but not one defended named original submitter. |
| `S3A-2A-R03-SUP-01` | `unknown` | `role:workflow-ledger-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-markdown-inspection` | `role:docs-governance-approver` | `accepted-for-packet` | The retained failure-management log is direct enough to sharpen the outage-drill row at packet level. | The repo preserves the source markdown path and the packet review chain, but not one defended named original submitter. |
| `S3A-2A-R04-SUP-01` | `unknown` | `role:workflow-ledger-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-markdown-inspection` | `role:docs-governance-approver` | `accepted-for-packet` | The retained deterministic-injection log is direct enough to sharpen the ES-429 experiment row at packet level. | The repo preserves the source markdown path and the packet review chain, but not one defended named original submitter. |
| `S3A-2A-R04-SUP-02` | `unknown` | `role:workflow-ledger-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `direct-markdown-inspection` | `role:docs-governance-approver` | `accepted-for-packet` | The retained `expB` companion log is direct enough to keep the deterministic packet grounded in one concrete lab execution shape. | The repo preserves the source markdown path and the packet review chain, but not one defended named original submitter. |
| `S3A-2A-R06-SUP-01` | `unknown` | `role:workflow-ledger-maintainer` | `role:workflow-reviewer` | `role:evidence-verifier` | `transcript-comparison` | `role:docs-governance-approver` | `accepted-for-packet` | The earlier daemon and operability issues are bounded enough to sharpen the migration row's historical lineage. | The repo preserves the public issue lineage and the packet review chain, but not one defended named original submitter. |

## Parent-Ledger Rows To Update

- `S3A-2A-R02`: rewrite the row so the shared-key slice explicitly cites the retained observability-triage log as direct legacy support.
- `S3A-2A-R03`: rewrite the row so the outage-drill slice explicitly cites the retained failure-management log as direct legacy support alongside the surviving lab.
- `S3A-2A-R04`: rewrite the row so the deterministic ES-429 slice explicitly cites the retained `expB` logs as direct legacy support alongside the surviving lab.
- `S3A-2A-R06`: rewrite the row so the daemon-ready migration slice explicitly records the earlier daemon and operability issue lineage.

## Contract Changes Deferred Until Parent Write-Back

- `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption`: no immediate row change is required from this SUP round, but later readers may use the parent write-back when re-evaluating how much early source evidence sits behind `R02`, `R03`, and `R04`.
- `DOC-RUNTIME-OBSERVABILITY-0001`: no direct contract mutation is opened by this SUP round; any code-driven reader expansion still belongs on the contract-local `Code Bridge Table` and `Contract Coverage Table`, not on the SUP ledger.

## Evidence Time Audit

| supplement item id | source observed at | source recorded at | source effective from | source effective until | time precision | timezone note | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S3A-2A-R02-SUP-01` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `the retained triage log is used here for packet meaning, not for second-level chronology reconstruction` | The legacy log is strong enough for row-sharpening, but this SUP round still keeps chronology conservative. |
| `S3A-2A-R03-SUP-01` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `the retained failure-management log is used here for packet meaning, not for second-level chronology reconstruction` | The legacy log is strong enough for row-sharpening, but this SUP round still keeps chronology conservative. |
| `S3A-2A-R04-SUP-01` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `the retained deterministic-injection log is used here for packet meaning, not for second-level chronology reconstruction` | The retained `expB` packet sharpens the row without yet defending second-level timing. |
| `S3A-2A-R04-SUP-02` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `the retained companion log is used here for packet meaning, not for second-level chronology reconstruction` | The retained companion packet strengthens lab-shape continuity, but chronology stays conservative. |
| `S3A-2A-R06-SUP-01` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `the earlier daemon issues are used here as lineage evidence only` | This row sharpens historical lineage without changing the defended chronology already carried by the later surviving local log. |

## Downstream Reading Note

- Broad parent summary unchanged: `S3A-2A` remains one parent-owned mixed issue packet.
- Narrow current reader clarified: `R02`, `R03`, and `R04` now have explicit retained legacy observability and deterministic-drill support, while `R06` now records earlier daemon lineage.
- Child-opening still deferred: no separate code-driven contract lane is opened by this supplement round because code-facing semantics remain owned by downstream contract-local tables.

## Preliminary Reading

- These retained legacy logs and earlier issues do not overturn the current `S3A-2A` parent boundary.
- They do sharpen selected child rows enough that the parent ledger should no longer describe those rows as issue-only or issue-plus-later-survivor only.
- The resulting recommendation for this round was therefore:
  - keep the parent packet boundary unchanged
  - apply narrow parent-row write-back on `R02`, `R03`, `R04`, and `R06`
  - keep direct contract mutation deferred
  - keep code-driven layer detail on downstream contract-local surfaces rather than adding SUP-specific fields

## Reader Notes

- This SUP round is intentionally narrow: it admits legacy evidence only where that evidence materially sharpens an already-existing parent row.
- The supplement is not used to open a new lane for code-driven contract work; it is used to improve parent-row readability and provenance only.
- The current template set is sufficient for this purpose because parent/SUP surfaces already carry routing, evidence, provenance, and deferred contract-impact fields, while the code-facing reader structure already lives elsewhere.