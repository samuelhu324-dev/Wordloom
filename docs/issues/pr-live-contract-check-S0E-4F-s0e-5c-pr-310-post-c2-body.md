## Metadata

- Requested ID: `S0E-5C`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-5c`
- Source log: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
- Labels: `drills, EVOLUTION, s0/knowledge system, sub/1`
- Development issue: #309

## Summary

- Decompose guarded `PR create` into explicit stages instead of treating the entire create path as one atomic guarded mutation.
- Fix the reuse-vs-new-rule boundary so only create-time preflight may partially reuse the existing lifecycle pre-gate as an issue-readiness layer.
- Validate one bounded front-half sample that stops at `S1-S3`, proving pass/stop evidence can be emitted before any branch materialization or PR publication begins.

## Execution Checklist

- [x] `P0-C1-S1`: guarded `PR create` stage map fixed
- [x] `P1-C1-S1`: reuse-vs-new-rule boundary fixed
- [x] `P2-C1-S1`: representative decomposition sample recorded
- [x] `P3-C1-S1`: deferred publish-boundary decision fixed
- [x] `P3-C1-S2`: deferred post-apply verification ownership fixed
- [x] `P4-C1-S1S2`: live create path now runs inline post-apply verification and persists its result artifacts

## Links

- Log: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/pr-create-S0E-5C-p1-boundary-map.json`

## Evidence Footer

- `P1-C1-S1` | artifact: `docs/issues/pr-create-S0E-5C-p1-boundary-map.json`
- `P2-C1-S1` | artifact: `docs/issues/pr-create-S0E-5C-p2-pass-front-half-preflight-result.json`
- `P3-C1-S1S2` | artifact: `docs/issues/pr-create-S0E-5C-p3-publish-and-post-apply-decision.md`
- `P4-C1-S1S2` | artifact: `docs/issues/pr-prep-S0E-5B-real-post-apply-verify-result.json`
