## Metadata

- Requested ID: `S0E-2D`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-2d`
- Source log: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #297

## Summary

- Enrich issue creation so milestone, parent issue, project, and body-shape metadata are resolved deterministically before a real GitHub issue is created.
- Keep generated issue bodies English-only and structurally complete while leaving `Context` and `Definition of Done (DoD)` intentionally blank at creation time.
- Align child issue metadata with parent-log inheritance so `Parent issue` can be rendered as a stable short GitHub ref such as `#248`.

## Execution Checklist

- [x] `P0-C1-S1`: milestone and roadmap bridge precedence fixed
- [x] `P0-C1-S2`: relationship and project attachment rules fixed
- [x] `P0-C1-S3`: English body scaffold and link boundary fixed
- [x] `P1-C1-S1`: issue-create metadata precedence defined
- [x] `P1-C1-S2`: English-only issue-body scaffold fixed
- [x] `P1-C2-S1`: child parent-issue derivation fixed
- [x] `P1-C2-S2`: top-level parent-issue suppression fixed
- [x] `P1-C2-S3`: parent-issue rendering placement and format fixed
- [x] `P1-C2-S4`: parent-issue plain-text rendering fixed
- [x] `P2-C1-S1`: enriched issue draft validation completed
- [x] `P2-C1-S2`: deterministic links and blank-field fallback verified
- [x] `P3-C1-S1`: legacy real issue-create artifact audited and remediated against the current body contract
- [x] `P3-C2-S1`: one real enriched issue-create run completed
- [x] `P3-C2-S2`: write-back and applied/skipped metadata accounting recorded
- [x] `P3-C3-S1`: child parent-issue derivation and top-level omission verified
- [x] `P3-C3-S2`: sibling `S0E` child-issue audit and remediation completed
- [x] `P3-C3-S3`: live child-issue plain-text parent rendering completed

## Links

- Log: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/pr-prep-S0E-2D-sample-plan.json`

Closes #297
