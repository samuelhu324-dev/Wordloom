## Metadata

- Requested ID: `S0E-6E`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-6e`
- Source log: `docs/logs/log-S0E-6E-single-item-context-authoring-and-batch-preserve-boundary.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #336

## Summary

- Define a new ownership boundary where `Context` prose is generated one log at a time while batch tools only preserve, discover, and warn.
- Add one explicit single-item `Context` draft entrypoint and move issue draft generation back to scaffold-first behavior by default.
- Change batch issue-conclusion planning so it preserves the live `Context` block unless an operator explicitly opts into single-item regeneration.

## Execution Checklist

- [x] `P0-C1-S1`: single-item authoring versus batch-preserve boundary fixed
- [x] `P0-C1-S2`: weak gate retained for discovery instead of batch authoring
- [x] `P1-C1-S1`: single-item `Context` draft entrypoint added
- [x] `P1-C1-S2`: issue draft generation returned to scaffold-first default
- [x] `P1-C1-S3`: single-generated conclusion wording aligned to the DoD boundary
- [x] `P2-C1-S1`: batch conclusion planning preserves live Context by default
- [x] `P2-C1-S2`: explicit single-generate opt-in retained for targeted cases
- [x] `P3-C1-S1`: single-item draft sample retained
- [x] `P3-C1-S2`: batch-preserve conclusion sample retained
- [x] `P4-C1-S1`: `S0E-2B` and `S0E-2A` refreshed one item at a time and re-audited
- [x] `P4-C1-S2`: remaining closed `S0E` child issues aligned to the same outcome-ending rule and re-audited

## Links

- Log: `docs/logs/log-S0E-6E-single-item-context-authoring-and-batch-preserve-boundary.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/issue-context-S0E-6E-sample-draft.json`

Closes #336
