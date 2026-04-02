## Metadata

- Requested ID: `S0E-2B`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-2b`
- Source log: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #288

## Summary

- Backfill the finalized PR metadata for the `S0E-2B` automation slice after the original merged PR was created with an incomplete body.
- Preserve the distinction between `draft-generation` and explicit `create-issue` while linking the log to the real issue and merged PR evidence.
- Keep the historical write-back auditable so later issue conclusion can close `#288` against the exact merged automation PR.

## Execution Checklist

- [x] `P0-C1-S1`: mode boundary and default safety fixed
- [x] `P0-C1-S2`: script input/output contract fixed
- [x] `P0-C1-S3`: creation evidence and write-back contract fixed
- [x] `P1-C1-S1`: local draft-generation path implemented
- [x] `P1-C1-S2`: structured draft result emitted
- [x] `P2-C1-S1`: explicit create mode and prerequisite checks implemented
- [x] `P2-C1-S2`: real GitHub issue creation path implemented
- [x] `P3-C1-S1`: one draft-generation run and one create-issue run validated
- [x] `P3-C1-S2`: write-back discipline recorded after successful creation

## Links

- Log: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/pr-prep-S0E-2B-remediation-plan.json`
