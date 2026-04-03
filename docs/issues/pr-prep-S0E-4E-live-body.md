## Metadata

- Requested ID: `S0E-4E`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-4e`
- Source log: `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #326

## Summary

- Open the dedicated slice for deterministic `PR event -> source_log_path` attribution.
- Separate source-log attribution ownership from `S0E-7A` secondary-enforcement workflow policy.
- Fix the first fail-closed boundary: automatic rollout is blocked until attribution becomes explicit and deterministic.

## Execution Checklist

- [x] `P0-C1-S1`: source-log attribution ownership boundary fixed
- [x] `P1-C1-S1`: define candidate source-log ownership surfaces
- [x] `P1-C1-S2`: define attribution precedence
- [x] `P2-C1-S1`: define ambiguity stop conditions
- [x] `P2-C1-S2`: define representative sample expectations
- [x] `P3-C1-S1`: define attribution output handoff contract
- [x] `P3-C1-S2`: define unblocking criteria for limited automatic rollout

## Links

- Log: `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
- Runbook: ``
- Evidence artifact: `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`

Closes #326
