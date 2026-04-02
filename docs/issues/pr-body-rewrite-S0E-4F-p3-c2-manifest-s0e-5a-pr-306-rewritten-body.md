## Metadata

- Requested ID: `S0E-5A`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-5a`
- Source log: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
- Labels: `drills, EVOLUTION, s0/knowledge system, sub/1`
- Development issue: #305

## Summary

- Define one dedicated lifecycle pre-gate contract that checks live GitHub issue state before any downstream mutation is allowed to continue.
- Add one remediation-planning layer and one unified pre-gate decision entrypoint so warning and blocked findings can stop apply with reusable artifact output instead of relying on operator memory.
- Validate the same guarded pre-gate in front of one real issue-conclusion mutation path plus one frozen stop-before-apply drill, proving that gate decisions now control real mutation flow.

## Execution Checklist

- [x] `P0-C1-S1`: audit boundary and lifecycle stages fixed
- [x] `P0-C1-S2`: severity and blocking rules fixed
- [x] `P0-C1-S3`: structured evidence contract fixed
- [x] `P1-C1-S1`: lifecycle audit manifest and result shape fixed
- [x] `P1-C1-S2`: stage-aware dry-run checks implemented
- [x] `P2-C1-S1`: representative repaired `S0E` child-issue manifest prepared
- [x] `P2-C1-S2`: dry-run audit output recorded for the representative sample
- [x] `P3-C1-S1`: lifecycle-audit findings mapped into downstream dry-run remediation manifests
- [x] `P3-C1-S2`: archived historical defect fixture validated without mutating live GitHub state
- [x] `P4-C1-S1`: unified pre-gate entrypoint implemented and exercised on pass and stop samples
- [x] `P4-C1-S2`: v1 warning policy fixed as stop-and-plan-remediation instead of silent pass-through
- [x] `P5-C1-S1`: pre-gate connected to one real issue-conclusion apply path and validated on a live pass sample
- [x] `P5-C1-S2`: guarded issue-conclusion path halted before apply on one frozen stop sample

## Links

- Log: `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/issue-conclusion-S0E-5A-p5-pass-guarded-apply-result.json`
