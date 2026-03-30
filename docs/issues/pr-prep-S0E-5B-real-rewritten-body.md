## Metadata

- Requested ID: `S0E-5B`



- Base branch: `main`



- Candidate PR-prep branch: `pr-prep/s0e-5b`



- Source log: `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`



- Labels: `drills, EVOLUTION, s0/knowledge system, sub/1`



- Development issue: #307

## Summary

- Expand guarded lifecycle apply beyond issue conclusion by adding one targeted-remediation continuation rule for relationship attach while keeping the generic pre-gate as the source of truth.



- Add one guarded PR-body rewrite path that only proceeds on `allow-apply`, then validate it against a real merged PR and a frozen blocked fixture.



- Use `S0E-5B` itself as the representative sample so relationship attach, PR lifecycle, and post-merge close-out can all be traced on one real issue instead of isolated drills.

## Execution Checklist

- [x] `P0-C1-S1`: expansion boundary fixed
- [x] `P1-C1-S1`: guarded relationship-attach path implemented
- [x] `P1-C1-S2`: pass and stop validation recorded
- [x] `P2-C1-S1`: next guarded mutation family selected
- [x] `P2-C1-S2`: pass and stop validation recorded for the chosen PR-side mutation family
- [x] `P3-C1-S1`: same-sample guarded mutation composition recorded
- [x] `P3-C1-S2`: representative closed-loop sample converged after both guarded mutation families

## Links

- Log: `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`



- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/307`



- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`



- Evidence artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`

## Evidence Footer

- P0-C1-S1 (targeted relationship remediation continuation rule fixed | 2026-03-30)
- P1-C1-S1S2 (guarded relationship path exercised on live pass and frozen stop samples | 2026-03-30)
- P2-C1-S1S2 (guarded PR-body rewrite exercised on live pass and frozen stop samples | 2026-03-30)
- P3-C1-S1S2 (same-sample guarded mutation composition converged on S0E-5B | 2026-03-30)

## Development Link

- Closes #307
