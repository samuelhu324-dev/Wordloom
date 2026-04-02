## Metadata

- Requested ID: S0E-7C
- Base branch: main
- Candidate PR-prep branch: pr-prep/s0e-7c-runtime-closure
- Source log: docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md
- Labels: EVOLUTION, s0/knowledge system, sub/1
- Development issue: 

## Summary

- Remove the historical review planner's runtime dependency on ody_contract.py so the mirror workflow can run from main.
- Keep the footer-row validation local to the planner because only the canonical footer line regex is required here.
- Unblock the default-branch workflow_dispatch path that previously failed before producing its plan artifact.

## Execution Checklist

- [x] P4-C1-S3: planner runtime closure dependency removed

## Links

- Log: docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md
- Issue: `
- Runbook: `
- Evidence artifact: scripts/issues/plan_historical_log_review.py
