## Metadata

- Requested ID: `S0E-6C`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-6c`
- Source log: `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #334

## Summary

- Fix issue-body `Context` to a deterministic English sentence contract with `5` lines for main logs and `4` lines for child logs.
- Reuse the same sentence contract in issue draft generation, issue conclusion rendering, and lifecycle audit gate checks.
- Make the rendered `Context` sentences source-log-derived so different issues no longer receive the same generic wording.
- Re-run the real `S0E-5C/#309` conclusion path and audit so the new `Context` gate is exercised on a live concluded issue.

## Execution Checklist

- [x] `P0-C1-S1`: main-log vs child-log Context sentence-count contract fixed
- [x] `P0-C1-S2`: one-sentence-per-line Context rule fixed
- [x] `P1-C1-S1`: issue draft Context renderer fixed
- [x] `P1-C1-S2`: issue conclusion Context renderer fixed
- [x] `P2-C1-S1`: issue Context sentence-count gate fixed
- [x] `P2-C1-S2`: closed-issue gate alignment fixed
- [x] `P3-C1-S1`: real conclusion replay and re-audit completed for `S0E-5C/#309`

## Links

- Log: `docs/logs/log-S0E-6C-issue-context-sentence-contract-and-gate.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/lifecycle-audit-S0E-5C-context-gate-plan.json`

Closes #334
