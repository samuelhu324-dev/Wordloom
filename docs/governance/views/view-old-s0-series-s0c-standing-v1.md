# Old S0 Series S0C Standing v1

## Purpose

- This view is the fourth bounded series drill-down surface for old-`S0` absorption reading.
- It exists so readers can inspect `S0C` log by log and see which rows are already surfaced, which current reading home they now use, and which rows still remain outside the surfaced set.

## Series Boundary

- This fourth bounded drill-down covers `S0C` only.
- `S0C` is the larger unfinished small-series follow-up after `S0D`, so publishing its standing surface is the remaining prerequisite for bounded series review under the same drill-down model already proven for `S0B`, `S0D`, `S0E`, and `S0F`.

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

## S0C Drill-Down

| source log | series | currently surfaced | reader-facing standing | current family | current reading home | history role | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `S0C-1A` | `S0C` | `yes` | `current-view` | `DOC` | `view-doc-history-and-lineage-v1` | `structural prerequisite` | `already admitted into the surfaced set as one pre-DOC structural prerequisite for current DOC history reading` |
| `S0C-2A` | `S0C` | `no` | `retired-lineage` | `repo current-library test surfaces` | `backend/api/app/tests/test_library/test_integration_round_trip.py` and `backend/api/app/tests/test_integration_four_modules.py` (module-level skipped) | `retired legacy suite lineage` | `the row records the defended retirement of legacy integration narratives whose failures no longer indicate current-system regressions; the historical meaning survives, but current protection now reads through current library application, repository, and invariant-focused tests instead of through these suites as active quality gates` |
| `S0C-3A` | `S0C` | `no` | `retained-evidence` | `repo CLI and scenario execution surfaces` | `backend/scripts/cli.py` and `backend/scripts/cli_app/` | `retained CLI-structure governance evidence` | `the row remains bounded CLI thinning and scenario-handler decomposition governance, while current command behavior now reads through the live dispatch-only entry and `cli_app` execution modules rather than through one DOC-facing history surface` |
| `S0C-3A-1A` | `S0C` | `no` | `retained-evidence` | `repo CLI and scenario execution surfaces` | `backend/scripts/cli.py` and `backend/scripts/cli_app/` | `retained migration-bridge evidence` | `the row records the temporary double-parallel migration bridge that preserved CLI behavior while handlers moved into `cli_app`; current behavior now reads through the landed thin-entry and scenario modules rather than through the bridge log itself` |
| `S0C-3A-2A` | `S0C` | `no` | `retained-evidence` | `repo CLI artifact-contract and workflow evidence surfaces` | `backend/scripts/cli_app/common.py` plus workflow-side shared artifact helpers | `retained artifact-contract convergence evidence` | `the row remains bounded evidence-contract and packing convergence history, while current artifact write-path and packing behavior now read through the shared helper surfaces instead of through the old convergence log as a current rule source` |
| `S0C-3A-3A` | `S0C` | `no` | `retained-evidence` | `repo CLI parser and dispatch surfaces` | `backend/scripts/cli.py` and `backend/scripts/cli_app/parser.py` | `retained dispatch-thinning evidence` | `the row records the later dispatch-only and argparse-extraction cutover, while current parser and callback wiring now read through the thin CLI entry and parser module rather than through the historical cutover log` |
| `S0C-4A` | `S0C` | `no` | `retained-evidence` | `repo scenario catalog and operator-entry surfaces` | `docs/runbook/run-S0C-scenarios-taxonomy.md` and `docs/labs/scenarios/catalog.yml` | `retained scenario-taxonomy governance evidence` | `the row remains bounded taxonomy and suite-entry convergence history, while current operator discovery now reads through the stable runbook and catalog single source of truth rather than through one DOC-facing history surface` |
| `S0C-4A-1A` | `S0C` | `no` | `retained-evidence` | `repo scenario catalog, guardrail, and suite workflow surfaces` | `docs/labs/scenarios/catalog.yml`, `backend/scripts/ci/validate_scenario_catalog.py`, and `.github/workflows/ci-scenario-guardrails.yml` | `retained catalog-guardrail evidence` | `the row records the guardrail and catalog-driven suite closure that current drills already reuse, while live catalog validation and workflow references now read through the stable catalog and guardrail surfaces rather than through the old convergence log` |
| `S0C-5A` | `S0C` | `no` | `history-lineage` | `repo log-orchestration and naming surfaces` | `docs/logs/log-S0D-1A-log-entries-orchestration.md` plus `docs/logs/_template-log-parent-epic-spine.md` and `docs/logs/_template-log-phase-drills-evidence.md` | `lineage for current log grammar` | `the row is historically relevant because its step/cycle naming and PR-description discipline later concentrate into the parent-spine and template-based log-orchestration model; it remains outside the DOC surfaced set and does not justify a separate cleanup move` |

## Reader Routing

| question | open first | why |
| --- | --- | --- |
| `inside S0C, what is the standing of each old log now?` | `view-old-s0-series-s0c-standing-v1.md` | this surface is the bounded per-log standing answer for the `S0C` series |
| `why did the counted S0C packet exist, and what did it leave behind?` | `view-old-s0-narrative-history-packet-s0d-s0c-v1.md` | the counted narrative packet answers the change-story question that the standing table does not |
| `how much of old S0 is surfaced by series overall?` | `view-old-s0-absorption-coverage-overview-v1.md` | aggregate counts and distribution are not repeated here |
| `which admitted rows exist across all series?` | `view-old-s0-migration-ledger-v1.md` | cross-series admitted-row projection stays in the migration ledger |
| `how did one current DOC surface emerge from this history?` | `view-old-s0-contract-history-chain-doc-drb-0001-v1.md` or the later matching chain view | current-surface-first evolution reading belongs in the history-chain layer, not in the series standing table |

## Reader Notes

- Read this view when the question is `inside S0C, what is the standing of each old log now?`
- Use `view-old-s0-absorption-coverage-overview-v1.md` when the question is still aggregate and series-level only.
- Use `view-old-s0-migration-ledger-v1.md` when the question is `which rows are already admitted into the surfaced set across all series?`
- Use `view-old-s0-narrative-history-packet-s0d-s0c-v1.md` when the question is no longer current standing but `why did these S0C rows exist and what did they leave behind?`
- This fourth `S0C` surface closed the last missing small-series drill-down prerequisite before row-level review, and the bounded `P6` review now resolves the remaining eight rows without widening the current `DOC` surfaced set.
- `S0C-1A` remains the only already surfaced row in the series.
- `S0C-2A` now reads as retired legacy-suite lineage, `S0C-3A` through `S0C-4A-1A` now read as retained repo-local CLI/scenario governance evidence, and `S0C-5A` now reads as history-lineage for the current log-orchestration grammar rather than as one cleanup-admission candidate.

## Source Refs

- `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
- `docs/governance/views/view-old-s0-absorption-coverage-overview-v1.md`
- `docs/governance/views/view-old-s0-migration-ledger-v1.md`
- `docs/logs/log-S0F-5E-small-series-review-sequencing-and-standing-surface-completion.md`
- `docs/logs/log-S0C-1A-log-extensions.md`
- `docs/logs/log-S0C-2A-legacy-integration-suite-retired.md`
- `docs/logs/log-S0C-3A-cli-breakdown.md`
- `docs/logs/log-S0C-3A-1A-double-parallel.md`
- `docs/logs/log-S0C-3A-2A-artifacts-contract-packing.md`
- `docs/logs/log-S0C-3A-3A-dispatch-only-argparse-extraction.md`
- `docs/logs/log-S0C-4A-scenarios-taxonomy.md`
- `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
- `docs/logs/log-S0C-5A-Git-commit+push-descriptions.md`