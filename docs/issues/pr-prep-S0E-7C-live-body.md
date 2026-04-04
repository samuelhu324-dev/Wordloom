## Metadata

- Requested ID: `S0E-7C`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-7c`
- Source log: `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: 

## Summary

- Add one manifest-driven planner that reviews historical logs for both structure drift and lifecycle completeness.
- Validate several representative samples so old logs can be split into closed-loop, issue-open-no-pr, and log-only follow-up buckets before any apply path starts.
- Add one manual GitHub Actions mirror workflow that reruns the same review planner and retains structured audit artifacts without becoming the primary owner.
- Add one first full-series `S0E` batch manifest and retained review plan so the historical backlog is measured before live Actions replay starts.

## Execution Checklist

- [x] `P0-C1-S1`: review-versus-apply boundary fixed
- [x] `P0-C1-S2`: local-first / mirror-later execution policy fixed
- [x] `P1-C1-S1`: manifest-driven historical log review entrypoint implemented
- [x] `P1-C1-S2`: narrow structure-review contract implemented
- [x] `P2-C1-S1`: representative sample manifest fixed
- [x] `P2-C1-S2`: representative sample plan retained
- [x] `P3-C1-S1`: manual dispatch mirror workflow added
- [x] `P3-C1-S2`: retained artifact and advisory fail policy fixed
- [x] `P4-C1-S1`: full-series `S0E` manifest and backlog plan retained

## Links

- Log: `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
- Issue: ``
- Runbook: ``
- Evidence artifact: `docs/issues/historical-log-review-S0E-series-plan.json`

## Evidence Footer

- `P0-C1-S1S2` | artifact: `docs/logs/log-S0E-7C-historical-log-review-sampling-and-mirror-follow-up.md`
- `P1-C1-S1S2` | artifact: `scripts/issues/plan_historical_log_review.py`
- `P2-C1-S1S2` | artifact: `docs/issues/historical-log-review-S0E-7C-sample-plan.json`
- `P3-C1-S1S2` | artifact: `.github/workflows/s0e-historical-log-review-mirror.yml`
- `P4-C1-S1` | artifact: `docs/issues/historical-log-review-S0E-series-plan.json`
- Keep footer rows low-cardinality: prefer one representative artifact per relevant unit instead of replaying the full artifact inventory.
- Generated PR body should keep `Evidence Footer` and `Development Link` as separate sections.
- `Evidence Footer` rows must be copied only from `Evidence Footer Source` and must keep the same line shape.
