## Metadata

- Requested ID: `S0F-2A`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0f-2a`
- Source log: `docs/logs/log-S0F-2A-maintenance-lanes-and-direct-patch-ledger.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/2, drills`
- Development issue: #384

## Summary

- Define a three-lane policy for standard slice work, maintenance sweep bundles, and direct patch commits.
- Add one thin operator-facing runbook so lane selection, naming, and escalation rules do not need to be reinvented during mixed cleanup work.
- Publish one shared direct-patch ledger and one minimal maintenance-log template so small work can remain traceable without forcing every fix into the full issue/log lifecycle.

## Execution Checklist

- [x] `P0-C1-S1`: `S0F-2A` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: lane-governance boundary fixed
- [x] `P1-C1-S1`: standard slice, maintenance sweep, and direct patch lanes defined
- [x] `P1-C1-S2`: lane escalation rule defined
- [x] `P2-C1-S1`: future maintenance-log naming standardized
- [x] `P2-C1-S2`: patch-log placement and direct-patch boundary standardized
- [x] `P3-C1-S1`: thin lane-policy runbook published
- [x] `P3-C1-S2`: shared direct-patch ledger plus maintenance/patch templates published

## Links

- Log: `docs/logs/log-S0F-2A-maintenance-lanes-and-direct-patch-ledger.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`

Closes #384
