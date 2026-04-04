## Metadata

- Requested ID: `S0E-7D`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-7d`
- Source log: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #341

## Summary

- Define one explicit failure taxonomy for the current docs/GitHub automation path, split into strong-structure and weak-structure failure families.
- Fix one ordered replay/backfill contract so issue and PR remediation can be replayed through the same deterministic pipeline instead of ad hoc manual repair.
- Define the handling semantics for each failure class, including `block`, `replayable`, `manual`, and `reconciliation`.

## Execution Checklist

- [x] `P0-C1-S1`: failure taxonomy fixed
- [x] `P0-C1-S2`: replay / backfill order fixed
- [x] `P0-C1-S3`: handling semantics fixed
- [x] `P0-C1-S4`: evidence contract fixed
- [x] `P1-C1-S1`: failure surfaces split into strong-structure versus weak-structure families
- [x] `P1-C1-S2`: default handling semantic mapped per failure family
- [x] `P2-C1-S1`: representative manifest retained across all four handling classes
- [x] `P2-C1-S2`: structured audit summary retained
- [x] `P3-C1-S1`: replayable remediation/apply contract fixed
- [x] `P3-C1-S2`: post-apply verify and incomplete-convergence stop rules fixed
- [x] `P4-C1-S1`: future publish/verify/remediation gate surface scoped and named

## Links

- Log: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
- Runbook: ``
- Evidence artifact: ``

Closes #341
