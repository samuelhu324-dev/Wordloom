# Outlet And Lifecycle Observability Detail S0F Live Child Set v1

## Purpose

- This view is the first bounded per-item observability surface for outlet and lifecycle reading.
- It exists so readers can inspect each item in the first admitted `S0F` live child-set population without reconstructing current lifecycle state, current reading home, and next-open routing from scattered contracts and retained logs.

## Population Boundary

- This first detail surface uses the same bounded population admitted in the aggregate overview:
  - `S0F-1A`
  - `S0F-1B`
  - `S0F-1C`
  - `S0F-1D`
  - `S0F-1G`
  - `S0F-1H`
  - `S0F-1J`
- Every item in this first set already has:
  - a real GitHub issue written back in source
  - a real GitHub PR written back in source
  - a converged current reading home outside the retained source log

## Per-Item Standing

| source log | live issue | live PR | practical lifecycle stage | lifecycle standing | dominant current outlet | current reading home | stop reason | next owner | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `S0F-1A` | `#364` | `#365` | `concluded` | `complete` | `contract` | `DOC-ICR-0001` | `completed` | `DOC-ICR-0001` | current reading concentrates issue-creation current meaning; `GC-PRA-0001` remains adjacent create-time PR-path clarification rather than the first-open home |
| `S0F-1B` | `#366` | `#371` | `concluded` | `complete` | `contract` | `DOC-ICT-0001` | `completed` | `DOC-ICT-0001` | current reading concentrates issue Context sentence-count and shape under the family-owned DOC contract |
| `S0F-1C` | `#367` | `#372` | `concluded` | `complete` | `contract` | `GC-REMED-0001` | `completed` | `GC-REMED-0001` | current reading concentrates batch remediation stage ownership; `run-S0F-1C-guarded-multi-item-remediation.md` remains a secondary operator path, not the first current home |
| `S0F-1D` | `#368` | `#373` | `concluded` | `complete` | `contract` | `GC-COMPL-0001` | `completed` | `GC-COMPL-0001` | current reading concentrates lifecycle completeness audit; `DOC-ICR-0001` and `DOC-ICL-0001` remain adjacent current rule surfaces rather than the primary completeness home |
| `S0F-1G` | `#376` | `#377` | `concluded` | `complete` | `contract` | `DOC-IID-0001` + `DOC-IID-0002` | `completed` | `DOC-IID-0001` + `DOC-IID-0002` | current reading is split across the two issue-identity current contracts: sidebar ordering and controlled title vocabulary |
| `S0F-1H` | `#378` | `#379` | `concluded` | `complete` | `contract` | `GC-PRR-0001` | `completed` | `GC-PRR-0001` | current reading concentrates canonical reviewer classification; `run-S0F-1H-pr-body-completeness-review.md` remains the stable operator path when procedure, not rule meaning, is the reader question |
| `S0F-1J` | `#382` | `#383` | `concluded` | `complete` | `contract` | `GC-PRG-0001` | `completed` | `GC-PRG-0001` | current reading concentrates gate semantics and packaged standard-check meaning; reviewer procedure still routes secondarily through the `S0F-1H` runbook |

## Reader Notes

- This first detail surface is intentionally narrow and converged.
- It does not try to show incomplete, blocked, replayable, or manual states yet because the first admitted population is the current `S0F` live child set that already converged through the real lifecycle path.
- The detail view still adds value over the aggregate overview because it shows where each item now reads first:
  - `S0F-1A` -> `DOC-ICR-0001`
  - `S0F-1B` -> `DOC-ICT-0001`
  - `S0F-1C` -> `GC-REMED-0001`
  - `S0F-1D` -> `GC-COMPL-0001`
  - `S0F-1G` -> `DOC-IID-0001` + `DOC-IID-0002`
  - `S0F-1H` -> `GC-PRR-0001`
  - `S0F-1J` -> `GC-PRG-0001`
- When the reader question is about present-day rule meaning, open the named `current reading home` first.
- When the reader question is about historical chronology or live execution evidence, open the retained source log after the current home has oriented the rule boundary.

## Source Refs

- `docs/logs/log-S0F-6C-outlet-and-lifecycle-observability.md`
- `docs/governance/views/view-outlet-and-lifecycle-observability-overview-v1.md`
- `docs/governance/contract/DOC-ICR-0001-issue-creation-metadata-english-body.md`
- `docs/governance/contract/DOC-ICT-0001-issue-context-sentence-count-main-vs-child.md`
- `docs/governance/contract/DOC-IID-0001-parent-sidebar-ordering-ownership.md`
- `docs/governance/contract/DOC-IID-0002-issue-title-keyword-controlled-vocabulary.md`
- `docs/governance/contracts/GC-REMED-0001-guarded-batch-multi-item-remediation-stages.md`
- `docs/governance/contracts/GC-COMPL-0001-lifecycle-three-stage-completeness-audit.md`
- `docs/governance/contracts/GC-PRR-0001-pr-body-canonical-review-classification.md`
- `docs/governance/contracts/GC-PRG-0001-pr-body-standard-check-fail-on-substantive-drift.md`
- `docs/runbook/run-S0F-1H-pr-body-completeness-review.md`