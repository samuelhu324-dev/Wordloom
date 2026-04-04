## Metadata

- Requested ID: `S0E-6A`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-6a`
- Source log: `docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #332

## Summary

- Normalize logs to one dual-track structure where `PR Summary Inputs` stays automation-facing while `Evidence` remains the human ledger.
- Fix the structured-input boundary so `PR links` and `Evidence Footer Source` stop drifting into mixed legacy shapes.
- Retain template and migration guidance that lets later log families adopt the same structure without inventing new semantics per slice.

## Execution Checklist

- [x] `P0-C1-S1`: dual-track evidence model fixed
- [x] `P0-C1-S2`: section ownership fixed
- [x] `P1-C1-S1`: mandatory structured input blocks fixed
- [x] `P1-C1-S2`: prose-only non-goal blocks fixed
- [x] `P2-C1-S1`: minimum evidence ledger shape fixed
- [x] `P2-C1-S2`: footer-to-ledger relationship fixed
- [x] `P3-C1-S1`: parent template guidance target fixed
- [x] `P3-C1-S2`: phase template guidance target fixed
- [x] `P4-C1-S1`: historical migration priority fixed

## Links

- Log: `docs/logs/log-S0E-6A-log-structure-normalization-and-dual-track-evidence-contract.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`

Closes #332
