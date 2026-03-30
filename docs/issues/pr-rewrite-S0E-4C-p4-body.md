## Metadata

- Requested ID: `S0E-4C`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-4c`
- Source log: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #300

## Summary

- Normalize PR `Development issue` rendering to short refs such as `#297` and keep `Development Link` consistent with the same normalized target.
- Make PR summary bullets mandatory for real PR creation so live PRs no longer ship with `<placeholder>` in `Summary`.
- Add a real issue-relationship attach path so child issue sidebar `Relationships` matches the existing `Metadata -> Parent issue` contract.

## Execution Checklist

- [x] `P0-C1-S1`: PR development-issue short-ref rendering fixed in contract
- [x] `P0-C1-S2`: PR summary requiredness fixed in contract
- [x] `P0-C1-S3`: issue parent relationship attach boundary fixed in contract
- [x] `P0-C1-S4`: evidence contract fixed
- [x] `P1-C1-S1`: PR preview/create development-issue rendering normalized
- [x] `P1-C1-S2`: real PR create path blocks placeholder summaries
- [x] `P1-C1-S3`: issue relationship apply tooling added
- [x] `P2-C1-S1`: representative PR-prep artifacts regenerated and reviewed
- [x] `P2-C1-S2`: representative issue relationship artifacts regenerated and reviewed
- [x] `P3-C1-S1`: one real PR validated against the updated body contract
- [x] `P3-C1-S2`: one real child issue validated against the updated relationship attach path
- [x] `P3-C1-S3`: historical `S0E` PR audit completed and outdated live bodies remediated
- [x] `P4-C1-S1`: one full `issue creation -> PR -> issue conclusion` cycle completed under `S0E-4C`
- [x] `P4-C1-S2`: end-to-end artifacts reviewed for contract consistency

## Links

- Log: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/300`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/pr-prep-S0E-4C-p4-plan.json`
- Generated PR body should keep `Summary`, `Evidence Footer`, and `Development Link` as separate sections.
- `Summary` must not degrade to `<placeholder>` on a live PR create path.

## Evidence Footer

- `P1-C1-S1`: `scripts/issues/plan_pr_prep.py` now persists normalized short development-issue refs in plan output, and `scripts/issues/create_pr_from_plan.py` rewrites the metadata row to that same short-ref form before live PR creation.
- `P1-C1-S2`: `scripts/issues/create_pr_from_plan.py` now blocks live PR creation when the preview `Summary` still contains `- <placeholder>` or when the planned item carries zero explicit summary bullets.
- `P1-C1-S3`: `scripts/issues/apply_issue_relationships.py` now provides a real relationship apply path using GitHub GraphQL `addSubIssue`, including idempotent success when the requested parent-child link already exists and fail-closed behavior for conflicting parents.
- `P1-C1-S3`: the GitHub GraphQL mutation shape was verified against live `S0E` issue IDs while wiring the apply path, confirming that sidebar `Relationships` must be attached through sub-issue mutation instead of issue-body edits.
- `P2-C1-S1`: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md` now carries explicit `PR Summary Inputs`, and regenerated artifacts `docs/issues/pr-prep-S0E-2D-sample-plan.json` plus `docs/issues/pr-prep-S0E-2D-sample-body.md` confirm that `Summary` is now populated while `Development issue` remains the normalized short ref `#297`.
- `P2-C1-S1`: the regenerated `pr-prep-S0E-2D` plan now records `pr_development_issue: #297`, `pr_development_issue_refs: ["#297"]`, and `summary_bullet_count: 3`, proving the create-path fail-closed gate now has explicit structured input to consume.
- `P2-C1-S2`: `docs/issues/issue-relationship-S0E-4C-sample-plan.json` validates a representative `S0E` child relationship sample for `#248 -> #295` with clean traceability through `parent_log` and `child_log_path`.
- `P2-C1-S2`: `docs/issues/issue-relationship-S0E-4C-sample-apply-result.json` confirms the representative child issue was already attached to the requested parent and that the new apply path returns idempotent success as `already-linked-child-to-parent` instead of mutating or failing.
- `P3-C1-S1`: live PR `#296` was rewritten from the regenerated `docs/issues/pr-prep-S0E-4B-sample-body.md`, which now renders `Development issue: #295` as a plain short ref and keeps `Development Link` aligned as `Closes #295`.
- `P3-C1-S1`: live PR `#298` was rewritten from `docs/issues/pr-prep-S0E-2D-sample-body.md`, replacing the old `- <placeholder>` summary with explicit bullets and restoring the separate `Development Link` section.
- `P3-C1-S3`: the four historical merged PRs visible in the `S0E` list were audited as `#294`, `#296`, `#298`, and `#299`; only `#296` and `#298` required live body remediation, while `#294` and `#299` already matched the current contract.
- `P3-C1-S2`: live issue `#300` was created from `docs/issues/issue-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`, and `docs/issues/issue-relationship-S0E-4C-p4-apply-result.json` confirms the child issue is now attached to parent `#248` in GitHub sidebar `Relationships`.
- `P4-C1-S1`: live PR `#301` was created from clean branch `pr-prep/s0e-4c`, merged at `2026-03-30T03:44:43Z`, and auto-closed issue `#300` through `Closes #300` while preserving short-ref `Development issue` metadata in the PR body.
- `P4-C1-S2`: `docs/issues/issue-conclusion-S0E-4C-p4-plan.json`, `docs/issues/issue-conclusion-S0E-4C-p4-s0e-4c-body.md`, and `docs/issues/issue-conclusion-S0E-4C-p4-s0e-4c-apply-result.json` prove the final issue body now carries `DoD -> #301` plus deterministic `Issue` and `PR` links after the full closed loop.
- `P4-C1-S2`: `scripts/issues/plan_pr_prep.py` now compares commit selection against `origin/<base>` when available, aligning PR-prep dry-run selection with the real create-path worktree base used by `scripts/issues/create_pr_from_plan.py`.

## Development Link

- Closes #300
