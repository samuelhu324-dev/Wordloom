## Metadata

- Requested ID: `S0F-2B`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0f-2b`
- Source log: `docs/logs/log-S0F-2B-family-patch-and-ops-maintenance-model.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/2, drills`
- Development issue: #385

## Summary

- Refine the earlier small-work policy into family patch, ops maintenance, and tiny direct patch.
- Upgrade the maintenance template into a heavier ops-maintenance template with trigger, environment, entrypoint, precheck, postcheck, findings, evidence, and report summary sections.
- Decide and document that GitHub `MAINTENANCE` is a reserved top-level label for true ops-maintenance work, not for ordinary family patches.

## Execution Checklist

- [x] `P0-C1-S1`: `S0F-2B` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: refinement boundary against `S0F-2A` fixed
- [x] `P1-C1-S1`: family patch lane defined
- [x] `P1-C1-S2`: ops maintenance lane defined
- [x] `P1-C1-S3`: tiny direct patch lane narrowed and retained
- [x] `P2-C1-S1`: patch template upgraded to family-patch form
- [x] `P2-C1-S2`: maintenance template upgraded to ops-maintenance form
- [x] `P3-C1-S1`: `MAINTENANCE` label admission rule documented
- [x] `P4-C1-S1`: first real ops-maintenance sample published
- [x] `P5-C1-S1`: first real family patch sample published with current evidence and next-step triage fields

## Links

- Log: `docs/logs/log-S0F-2B-family-patch-and-ops-maintenance-model.md`
- Runbook: `docs/runbook/run-S0F-2B-family-patch-and-ops-maintenance-model.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`
- Roadmap: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`

Closes #385
