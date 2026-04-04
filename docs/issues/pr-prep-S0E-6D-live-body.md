## Metadata

- Requested ID: `S0E-6D`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-6d`
- Source log: `docs/logs/log-S0E-6D-natural-issue-context-rendering-and-weak-gate.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #335

## Summary

- Replace the rigid issue `Context` renderer with a natural summary builder driven by source-log facts and adjacent-slice relations.
- Relax the lifecycle gate from exact sentence-count slots to a bounded natural-summary contract that still checks English bullet rows, source-log anchors, and placeholder hygiene.
- Replay the recently audited closed `S0E` child issues so their live bodies reflect the new natural-summary `Context` style instead of the previous uniform template.

## Execution Checklist

- [x] `P0-C1-S1`: natural ledger-summary rule fixed
- [x] `P0-C1-S2`: weak deterministic gate fixed
- [x] `P1-C1-S1`: draft renderer switched to natural summary
- [x] `P1-C1-S2`: conclusion renderer switched to natural summary
- [x] `P2-C1-S1`: line-range gate fixed
- [x] `P2-C1-S2`: anchor and placeholder gate fixed
- [x] `P3-C1-S1`: representative live replay completed
- [x] `P4-C1-S1`: prose-first weak gate narrowed
- [x] `P4-C1-S2`: fact-pool selection and style-family rendering introduced
- [x] `P4-C1-S3`: representative replay refreshed under the prose-first rule

## Links

- Log: `docs/logs/log-S0E-6D-natural-issue-context-rendering-and-weak-gate.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/lifecycle-audit-S0E-7C-child-issues-context-natural-summary-refresh-manifest-plan.json`

Closes #335
