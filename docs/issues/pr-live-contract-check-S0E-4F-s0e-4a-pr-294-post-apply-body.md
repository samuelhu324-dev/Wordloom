## Metadata

- Requested ID: `S0E-4A`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-4a`
- Source log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #293

## Summary

- Fix the PR automation contract around ID-scoped commit selection, metadata precedence, and development-link ownership.
- Roll final `pr_*` fail-closed semantics and PR body scaffold inputs into the parent and phase log templates.
- Validate that a future PR-prep generator can describe the `S0E-4A` scope without scraping arbitrary prose from the mixed working branch.

## Execution Checklist

- [x] `P0-C1-S1`: commit selection strategy fixed
- [x] `P0-C1-S2`: PR metadata and description contract fixed
- [x] `P0-C1-S3`: development-link and review boundary fixed
- [x] `P0-C1-S4`: evidence contract fixed
- [x] `P0-C1-S5`: default operating mode fixed
- [x] `P1-C1-S1`: PR metadata fields finalised in templates
- [x] `P1-C1-S2`: PR description structure fixed
- [x] `P2-C1-S1`: ID-scoped commit selection implemented
- [x] `P2-C1-S2`: clean PR-prep branch generation validated
- [x] `P3-C1-S1`: create one real PR with labels, optional metadata fields, and development linkage
- [x] `P3-C1-S2`: verify that human review and merge remain outside automation scope
- [x] `P3-C2-S1`: Development issue fallback to source log issue fixed
- [x] `P3-C2-S2`: multiple Development issues formatting fixed

## Links

- Log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Runbook: ``
- Evidence artifact: `docs/issues/pr-prep-S0E-4A-sample-plan.json`
