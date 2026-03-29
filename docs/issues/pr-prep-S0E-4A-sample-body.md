# S0E-4A: GitHub pull request automation contract v1

## Metadata

- Requested ID: `S0E-4A`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-4a`
- Source log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Development issue: ``

## Summary

- Fix the PR automation contract around ID-scoped commit selection, metadata precedence, and development-link ownership.
- Roll final `pr_*` fail-closed semantics and PR body scaffold inputs into the parent and phase log templates.
- Validate that a future PR-prep generator can describe the `S0E-4A` scope without scraping arbitrary prose from the mixed working branch.

## Execution Checklist

- [x] P0-C1-S1: commit selection strategy fixed
- [x] P0-C1-S2: PR metadata and description contract fixed
- [x] P0-C1-S3: development-link and review boundary fixed
- [x] P0-C1-S4: evidence contract fixed
- [x] P0-C1-S5: default operating mode fixed
- [x] P1-C1-S1: PR metadata fields finalised in templates
- [x] P1-C1-S2: PR description structure fixed

## Links

- Log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Issue: ``
- Runbook: ``
- Evidence artifact: `docs/issues/pr-prep-S0E-4A-sample-plan.json`

## Evidence Footer

- `8f99ca5d` S0E-4A/P0-C1-S1S2S3S4S5: fix PR automation contract
- `10f2bcfe` S0E-4A/P1-C1-S1S2: roll PR metadata and scaffold into templates

