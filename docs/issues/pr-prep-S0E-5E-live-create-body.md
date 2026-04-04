## Metadata

- Requested ID: `S0E-5E`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-5e-live`
- Source log: `docs/logs/log-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #353

## Summary

- Fix the parent issue `Definition of Done (DoD)` child ledger to sort by child log `created` order instead of defaulting to issue-number order.
- Define one deterministic fallback chain for equal or missing child-log dates so replay remains stable.
- Add a bounded parent-body gate check so conclusion refreshes cannot silently drift back to a different child ordering.

## Execution Checklist

- [x] `P0-C1-S1`: parent issue DoD ordering source fixed
- [x] `P1-C1-S1`: deterministic fallback chain fixed
- [x] `P2-C1-S1`: renderer and conclusion planner share one ordering helper
- [x] `P3-C1-S1`: parent DoD ordering drift checked in audit and replayed once

## Links

- Log: `docs/logs/log-S0E-5E-parent-issue-dod-child-log-ordering-and-gate.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`

Closes #353
