# Old S0 Series S0D Standing v1

## Purpose

- This view is the third bounded series drill-down surface for old-`S0` absorption reading.
- It exists so readers can inspect `S0D` log by log and see which rows are already surfaced, which current reading home they now use, and which rows still remain outside the surfaced set.

## Series Boundary

- This third bounded drill-down covers `S0D` only.
- `S0D` is the next smallest unfinished old-`S0` series after `S0B`, so publishing its standing surface is the lowest-risk way to make the next unresolved remainder reviewable before the larger `S0C` follow-up.

## Drill-Down Model

| field | job |
| --- | --- |
| `source log` | exact old-`S0` source log in this series |
| `series` | fixed series bucket for this drill-down surface |
| `currently surfaced` | whether the row is already admitted into the current old-`S0 -> DOC` surfaced set |
| `reader-facing standing` | one bounded current-reading classification from the `S0F-6B/P1` vocabulary |
| `current family` | current owning family when known |
| `current reading home` | current contract body, current `view`, or unresolved state |
| `history role` | bounded historical role such as structural prerequisite or unresolved |
| `notes` | short reader-facing explanation |

## S0D Drill-Down

| source log | series | currently surfaced | reader-facing standing | current family | current reading home | history role | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0D-1A` | `S0D` | `yes` | `current-view` | `DOC` | `view-doc-history-and-lineage-v1` | `structural prerequisite` | `already admitted into the surfaced set as one pre-DOC structural prerequisite for current DOC history reading` |
| `S0D-2A` | `S0D` | `no` | `retained-evidence` | `repo tooling and evidence surfaces` | `backend/scripts/ci/workflow_artifacts.py` plus `docs/labs/_snapshot/auto/` and `artifacts/*runs*.json` | `retained drills/evidence automation governance` | `run_dir discovery, summary-ledger shape, and hard-gate evidence bookkeeping now read through live artifact helper and snapshot/ledger surfaces; the old row remains bounded historical automation-governance detail rather than one DOC-history prerequisite` |
| `S0D-3A` | `S0D` | `no` | `retained-evidence` | `repo runbook and operator-entry surfaces` | `docs/runbook/_template-runbook.md` plus `docs/runbook/run-S5B-security-governance-hard-gates.md` and `docs/runbook/run-S6A-evidence-drills-spine.md` | `retained runbook-governance evidence` | `top-level runbook entry rules, thinness guidance, and validation expectations now read through the live runbook template and adopted operator entry surfaces; the old row remains bounded strategy and adoption history rather than one DOC-history row` |
| `S0D-4A` | `S0D` | `no` | `retained-evidence` | `repo UI evidence-lite surfaces` | `docs/UI&UX/README.md` plus `docs/UI&UX/UI-FIX-NOTE-TEMPLATE.md` and `docs/UI&UX/assets/README.md` | `retained UI evidence-lite governance` | `frontend light-track boundaries, note fields, and asset rules now read through the current UI evidence-lite surfaces and note corpus; the old row remains bounded governance history rather than one DOC-related current-reading target` |
| `S0D-5A` | `S0D` | `no` | `retained-evidence` | `repo drills packaging and workflow evidence surfaces` | `.github/workflows/reusable-labs-scenario-runner.yml` plus `backend/scripts/ci/workflow_artifacts.py` and `.github/workflows/drill-failures.yml` | `retained evidence-packing governance` | `minimal-success versus failure-bundle packing rules now read through the live workflow and artifact-helper surfaces; the old row remains bounded packaging-governance detail rather than one new DOC surface` |
| `S0D-6A` | `S0D` | `no` | `retained-evidence` | `repo roadmap and demo surfaces` | `docs/roadmap/road-template-main-roadmap.md` plus `docs/roadmap/road-template-branch-roadmap.md` and `docs/demo/demo-001/` | `retained roadmap/demo container governance` | `roadmap and demo-container organization now read through the current roadmap templates, bridge-aware roadmap surfaces, and structured demo container roots; the old row remains bounded container-evolution context and is secondary to the direct roadmap bridge contract in S0E-3A` |

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `inside S0D, what is the standing of each old log now?` | `view-old-s0-series-s0d-standing-v1.md` | this surface is the bounded per-log standing answer for the `S0D` series |
| `how much of old S0 is surfaced by series overall?` | `view-old-s0-absorption-coverage-overview-v1.md` | aggregate counts and distribution are not repeated here |
| `which admitted rows exist across all series?` | `view-old-s0-migration-ledger-v1.md` | cross-series admitted-row projection stays in the migration ledger |
| `how did one current DOC surface emerge from this history?` | `view-old-s0-contract-history-chain-doc-drb-0001-v1.md` or the later matching chain view | current-surface-first evolution reading belongs in the history-chain layer, not in the series standing table |

## Reader Notes

- Read this view when the question is `inside S0D, what is the standing of each old log now?`
- Use `view-old-s0-absorption-coverage-overview-v1.md` when the question is still aggregate and series-level only.
- Use `view-old-s0-migration-ledger-v1.md` when the question is `which rows are already admitted into the surfaced set across all series?`
- This third `S0D` surface now shows one mixed result: `S0D-1A` remains the only already surfaced `DOC` history row, while `S0D-2A` through `S0D-6A` resolve outside the surfaced set as retained governance evidence for repo-local tooling, runbook, UI, workflow-packing, and roadmap/demo surfaces.
- `S0D` therefore no longer carries generic unresolved remainder; later follow-up, if any, should begin from narrower cleanup or concentration questions rather than from another first-pass standing review.

## Source Refs

- `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
- `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
- `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `docs/logs/log-S0F-5E-small-series-review-sequencing-and-standing-surface-completion.md`
- `docs/logs/log-S0D-1A-log-entries-orchestration.md`
- `docs/logs/log-S0D-2A-drills-evidence-automation.md`
- `docs/logs/log-S0D-3A-runbook-stub.md`
- `docs/logs/log-S0D-4A-UI-layered-fix-notes.md`
- `docs/logs/log-S0D-5A-drills-evidence-packing-unification.md`
- `docs/logs/log-S0D-6A-structured-roadmap-and-demo.md`