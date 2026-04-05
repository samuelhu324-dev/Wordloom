## Metadata

- Requested ID: `S0F-1J`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0f-1j`
- Source log: `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #382

## Summary

- Package the stable PR body completeness check behind one repo-owned task and one workflow-dispatch CI surface.
- Keep all classification and failure semantics single-sourced in the existing reviewer and standard wrapper.
- Prove the reviewer-owned runbook is usable by replaying the packaged local and CI surfaces and retaining their evidence.

## Execution Checklist

- [x] `P0-C1-S1`: `S0F-1J` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: reviewer-owned packaging boundary fixed
- [x] `P1-C1-S1`: repo-owned standard check task exposed
- [x] `P2-C1-S1`: workflow-dispatch standard check gate exposed
- [x] `P3-C1-S1`: runbook replayed successfully through the local repo task
- [x] `P3-C1-S2`: runbook replayed successfully through the workflow-dispatch CI gate
- [x] `P4-C1-S1`: live issue created and source-log issue ownership written back

## Links

- Log: `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`

Closes #382
