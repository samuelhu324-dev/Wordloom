# Contract Family Inventory v1

## Purpose

- This view concentrates the first repo-wide contract inventory draft after `S0F-3I` fixed the seven-family taxonomy.
- It exists so readers can scan representative current contracts across `DOM/PRO/INT/OPS/SEC/EVD/DOC` without widening the `GC-*` registry front door into a mixed universal ledger.

## Current Model

- Read each row in this order:
  - `family`: what kind of contract it is
  - `representative surface`: one current example or concentrated surface for that family
  - `primary SoT`: where current authority should be read first
  - `affected levels`: which `S0-S6` levels this contract currently affects
  - `registry status`: whether the surface is already registry-admitted, remains family-owned outside the registry, or mixes both roles today
- This is a first-draft inventory, not an exhaustive catalog.
- It is allowed to list code-first and doc-first contracts together because taxonomy and placement are now separate axes.

## Family Inventory

| family | representative surface | primary SoT | affected levels | registry status |
| --- | --- | --- | --- | --- |
| `DOC` | `source-log compatibility and weak-structure export discipline` | `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md` | `S0` | `family-owned (non-registry)` |
| `DOC` | `governance contract taxonomy and placement model` | `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md` | `S0` | `family-owned (non-registry)` |
| `PRO` | `projection onboarding hard gate entrypoint and CI` | `docs/logs/log-S2D-3A-projection-onboarding-hard-gate-entrypoint+CI.md` plus projection gate code and tests | `S2, S6` | `family-owned (non-registry)` |
| `PRO` | `unified outbox table merge` | `docs/logs/log-S2B-6A-unified-outbox-table-merge.md` plus projection or outbox write-path code, schema, and tests | `S1, S2` | `family-owned (non-registry)` |
| `INT` | `artifacts contract packing` | `docs/logs/log-S0C-3A-2A-artifacts-contract-packing.md` plus `backend/scripts/cli_app/common.py` and dependent contract checks | `S0, S4, S6` | `family-owned (non-registry)` |
| `INT` | `dispatch-only argparse extraction` | `docs/logs/log-S0C-3A-3A-dispatch-only-argparse-extraction.md` plus CLI entrypoint code and help or exit-code checks | `S0, S4` | `family-owned (non-registry)` |
| `OPS` | `cloud runtime deploy verify rollback path` | `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md` and `docs/runbook/run-S4D-cloud-release-gate-map.md` | `S4, S6` | `family-owned (non-registry)` |
| `OPS` | `release trigger policy and governance boundary` | `docs/logs/log-S4E-1A-release-trigger-policy-and-governance-boundary.md` plus release runbooks and runtime entrypoints | `S4, S5` | `family-owned (non-registry)` |
| `SEC` | `authcontext policy audit` | `docs/logs/log-S5A-1A-authcontext-policy-audit.md` plus code, policy checks, and tests for auth context enforcement | `S1, S5, S6` | `family-owned (non-registry)` |
| `SEC` | `search query authorization drills` | `docs/logs/log-S5B-4A-search-query-authorization-drills.md` plus authorization code and hard-gate evidence | `S2, S5, S6` | `family-owned (non-registry)` |
| `EVD` | `stable entry contract` | `docs/logs/log-S6A-1A-stable-entry-contract.md` and `docs/runbook/run-S6A-evidence-drills-spine.md` | `S4, S6` | `family-owned (non-registry)` |
| `EVD` | `hard-gate evidence JSON` | `docs/logs/log-S6A-4A-hard-gate-evidence-json.md` plus gate scripts, evidence schema, and CI checks | `S4, S6` | `family-owned (non-registry)` |
| `GC current registry` | `issue creation metadata english body` | `docs/governance/contracts/GC-ICR-0001-issue-creation-metadata-english-body.md` | `S0` | `registry-admitted` |
| `GC current registry` | `PR creation ID-scoped commit selection` | `docs/governance/contracts/GC-PRA-0001-pr-creation-id-scoped-commit-selection.md` | `S0` | `registry-admitted` |
| `GC current registry` | `workflow failure taxonomy and handling` | `docs/governance/contracts/GC-WF-0001-publish-verify-remediation-failure-taxonomy-and-handling.md` | `S0, S6` | `registry-admitted` |

## Placement Notes

- `DOC` contracts normally keep their primary SoT in logs, templates, runbooks, or documentation-specific automation surfaces.
- `PRO`, `INT`, `OPS`, `SEC`, and `EVD` may all remain outside one unified folder because their primary SoT often lives partly in code, scripts, workflows, tests, and retained artifacts.
- `GC current registry` is intentionally narrow: it is the concentrated current governance front door, not the place where every contract family must physically live.

## Reader Notes

- The seven-family taxonomy and the `GC-*` narrowing rule come from `S0F-3I`; this view only applies them to representative current surfaces.
- The affinities shown here do not make `S0-S6` a substitute for family. They only show where these representative contracts currently concentrate.
- If a future row needs more than one plausible primary SoT, that is a signal to fix SoT ownership first rather than to widen the inventory with duplicated rows by default.
- For the directory-level placement answer, use `docs/governance/views/view-contract-family-placement-map-v1.md`; this inventory stays focused on representative contract rows rather than full path mapping.
- For the current `DOC` family reader entry, use `docs/governance/views/view-doc-current-front-door-v1.md` before scanning the underlying source-owner logs individually.
- For the current `OPS` family reader entry, use `docs/governance/views/view-ops-current-front-door-v1.md` before scanning the underlying runtime spines, runbooks, and workflow-owned surfaces individually.

## Source Refs

- `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- `docs/logs/INDEX.md`
- `docs/governance/INDEX.md`