## Metadata

- Requested ID: `S0E-3B`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-3b`
- Source log: `docs/logs/log-S0E-3B-github-label-inventory-and-live-preflight.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #322

## Summary

- Split GitHub label inventory and live preflight into a dedicated `S0E-3B` slice instead of keeping it implicit inside `S0E-2A`.
- Add an explicit live label preflight path to `gen_issue_draft.py` so draft generation can warn or fail before real issue creation.
- Retain one representative issue-draft sample proving that the derived labels exist in the live GitHub repository label catalog.

## Execution Checklist

- [x] `P0-C1-S1`: label inventory ownership fixed
- [x] `P0-C1-S2`: advisory vs fail-closed behavior fixed
- [x] `P0-C1-S3`: label-preflight evidence contract fixed
- [x] `P1-C1-S1`: issue draft live label preflight implemented
- [x] `P2-C1-S1`: representative issue draft sample retained
- [x] `P2-C1-S2`: live issue creation and source-log write-back retained

## Links

- Log: `docs/logs/log-S0E-3B-github-label-inventory-and-live-preflight.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/issue-S0E-3B-github-label-inventory-and-live-preflight.json`

Closes #322
