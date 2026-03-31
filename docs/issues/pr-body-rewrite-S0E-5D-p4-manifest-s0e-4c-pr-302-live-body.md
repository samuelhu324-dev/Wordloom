## Metadata

- Requested ID: `S0E-4C`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-4c-p5`
- Source log: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #300

## Summary

- Harden `create_pr_from_plan.py` so a long-lived mixed working branch can still produce a clean PR-prep branch when raw cherry-picks conflict on selected commits.
- Keep PR-prep planning and create-path execution aligned around the current remote-tracking base and the source-head final file state used for the prep branch.
- Re-run one real `S0E-4C` follow-up PR and update issue `#300` so the extra merged PR is reflected in the final DoD ledger.

## Execution Checklist

- [x] `P5-C1-S1`: create-path cherry-pick conflict hardening implemented

## Links

- Log: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/300`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/pr-prep-S0E-4C-p5-plan.json`
- Generated PR body should keep `Summary`, `Evidence Footer`, and `Development Link` as separate sections.
- `Summary` must not degrade to `<placeholder>` on a live PR create path.

## Evidence Footer

- `P5-C1-S1`: `scripts/issues/create_pr_from_plan.py` now records the current `origin/<base>` merge-base at apply time and, on cherry-pick conflict, rebuilds the prep branch from the source-head snapshot of the selected path set instead of failing immediately.

## Development Link

- Closes #300
