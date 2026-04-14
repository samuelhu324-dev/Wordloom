# OPS Current Front Door v1

## Purpose

- This view is the first current front door for the `OPS` contract family.
- It exists so readers can find current operator-facing and release/runtime-governance meaning without first translating those surfaces into the older governance-registry vocabulary.

## Current Model

- Read `OPS` as the family for deploy, verify, rollback, release operations, runtime operating model, and operator path contracts.
- The current `OPS` front door is family-first:
  - start here for current reading
  - then follow the stable spine, runbook, and phase surfaces that currently hold the strongest operational meaning
- Under this model, current `OPS` reading is not limited to `docs/governance/INDEX.md`, because most active operational meaning lives in runtime spines, runbooks, workflows, and operator entrypoints rather than in narrow governance registry records.

## Active Contracts

- `SYSTEMS-PLATFORM-OPERATIONS-RUNTIME-FOUNDATION`:
  - current primary source: `docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md`
  - current role: fixes the broad runtime-foundation operator family and its phase decomposition
- `CLOUD-RUNTIME-DEPLOY-VERIFY-ROLLBACK`:
  - current primary source: `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  - current role: fixes deploy, verify, rollback, and release-operations runtime semantics
- `RELEASE-CONTROL-PLANE-OPERATING-MODEL-TRIGGER-POLICY-AND-GOVERNANCE-BOUNDARY`:
  - current primary source: `docs/logs/log-S4E-release-operating-model-and-governance.md`
  - current role: fixes trigger policy, approval boundary, promotion, and release-governance control-plane semantics
- `CLOUD-RUNTIME-RELEASE-OPERATIONS-RUNBOOK`:
  - current primary source: `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
  - current role: keeps the stable operator-facing procedure for release execution and inspection

## Reader Notes

- This front door is intentionally a family view rather than a new registry record.
- `OPS` is mixed by design: current meaning spans spines, runbooks, workflow entrypoints, and scripts.
- Later family cleanup may still add a more concentrated `OPS` entry surface, but the family-first reading model should exist before any later naming reform or registry admission work.

## Source Refs

- `docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md`
- `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
- `docs/logs/log-S4E-release-operating-model-and-governance.md`
- `docs/runbook/run-S4D-cloud-runtime-release-operations.md`
- `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`