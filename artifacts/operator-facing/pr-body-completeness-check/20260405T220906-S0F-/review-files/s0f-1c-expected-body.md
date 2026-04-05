## Metadata

- Requested ID: `S0F-1C`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0f-1c`
- Source log: `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #367

## Summary

- Define a manifest-driven batch remediation contract for guarded multi-item live mutation work.
- Keep preview, guarded apply, and preserve-existing post-verify as three separate owned stages instead of collapsing them into one replay command.
- Require per-target evidence retention so multi-item runs do not hide which item drifted, stopped, or needed remediation.
- Use historical issue-conclusion Context refresh as the first representative sample without reopening raw mutation entrypoints.

## Execution Checklist

- [x] `P0-C1-S1`: `S0F-1C` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: batch-stage vocabulary fixed for preview, guarded apply, and preserve-existing post-verify
- [x] `P1-C1-S1`: representative multi-item manifest shape fixed
- [x] `P1-C1-S2`: preview-only multi-item sample retained
- [x] `P2-C1-S1`: per-target eligibility and remediation handoff rules fixed
- [x] `P2-C1-S2`: representative guarded multi-item live sample retained
- [x] `P3-C1-S1`: preserve-existing post-verify fixed as mandatory batch follow-up
- [x] `P3-C1-S2`: representative per-target drift report retained
- [x] `P4-C1-S1`: repeatable operator runbook retained

## Links

- Log: `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
- Runbook: `docs/runbook/run-S0F-1C-guarded-multi-item-remediation.md`
- Evidence artifact: `docs/issues/lifecycle-repeatability-S0F-1C-p4-summary.json`

Closes #367
