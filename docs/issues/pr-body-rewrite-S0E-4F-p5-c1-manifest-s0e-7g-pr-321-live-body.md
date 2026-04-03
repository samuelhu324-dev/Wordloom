## Metadata

- Requested ID: `S0E-7G`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-7g-p3`
- Source log: `docs/logs/log-S0E-7G-publish-verify-remediation-gate-workflow-dispatch-wrapper-surface.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: 

## Summary

- Retain one representative `workflow_dispatch` pass run over the shared read-only wrapper with uploaded artifact evidence and no delegated apply ownership.
- Retain one representative `workflow_dispatch` stop run for frozen `pr-create-preflight` replay while preserving `S4-local-branch-materialization` and fail-after-upload semantics.
- Harden the GitHub-side manual wrapper workflow so frozen audit-plan and frozen precomputed PR-prep plan inputs replay correctly on GitHub runners.

## Execution Checklist

- [x] `P3-C1-S1`: representative pass and stop workflow dispatches retained

## Links

- Log: `docs/logs/log-S0E-7G-publish-verify-remediation-gate-workflow-dispatch-wrapper-surface.md`
- Runbook: ``
- Evidence artifact: `docs/issues/publish-verify-remediation-gate-S0E-7G-p3-c1-representative-validation.json`

## Evidence Footer

- `P0-C1-S1S2 / P1-C1-S1S2` | artifact: `docs/issues/publish-verify-remediation-gate-S0E-7G-p0-p1-workflow-dispatch-surface-contract.json`
- `P2-C1-S1` | artifact: `.github/workflows/s0e-publish-verify-remediation-gate-read-only-wrapper-dispatch.yml`
- `P3-C1-S1` | artifact: `docs/issues/publish-verify-remediation-gate-S0E-7G-p3-c1-representative-validation.json`
- `P3-C1-S1` | artifact: `docs/issues/publish-verify-remediation-gate-S0E-7G-p3-c1-dispatch-visibility-check.json`
