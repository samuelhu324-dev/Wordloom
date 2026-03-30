## Metadata

- Requested ID: `S0E-4B`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-4b`
- Source log: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #295

## Summary

- Fix PR title generation so whole-phase aggregate PRs render compressed phase ranges instead of only `<ID>: <log title>`.
- Inherit structural PR labels from explicit issue-side fields so scope taxonomy does not disappear from the PR sidebar.
- Match the newer body shape around flat execution checklist parsing, structured evidence footer lines, and a separate development-link section.

## Execution Checklist

- [x] `P0-C1-S1`: title compression rule fixed
- [x] `P0-C1-S2`: structural PR label inheritance fixed
- [x] `P0-C1-S3`: body section boundaries fixed
- [x] `P1-C1-S1`: planner metadata inheritance updated
- [x] `P1-C1-S2`: body renderer footer and development-link formatting updated
- [x] `P2-C1-S1`: sample artifacts regenerated
- [x] `P2-C1-S2`: regenerated output reviewed against expected sidebar/body semantics
- [x] `P3-C1-S1`: `drills` auto-label semantics fixed
- [x] `P3-C1-S2`: default issue-side `wordloom Board` project semantics fixed locally
- [x] `P3-C1-S3`: live PR `#294` reconciled against the new rules
- [x] `P3-C1-S4`: issue-create project path wired locally and GitHub-side blocker recorded
- [x] `P3-C1-S5`: duplicated top-of-body title removed from generated issue and PR bodies
- [x] `P3-C1-S6`: stacked validation PR base fixed to `pr-prep/s0e-4a`
- [x] `P3-C1-S7`: stacked PR review semantics documented against GitHub's ancestry-heavy commit views
- [x] `P3-C1-S8`: title phase-span derivation switched to prefer completed checklist coverage
- [x] `P3-C1-S9`: mixed working branch and parent-log landing policy clarified
- [x] `P3-C1-S10`: real issue `#295` created and verified on `wordloom Board`
- [x] `P3-C1-S11`: live PR `#296` retargeted from the temporary stacked base back to `main`

## Links

- Log: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/295`
- Runbook: ``
- Evidence artifact: `docs/issues/pr-prep-S0E-4B-sample-plan.json`

## Evidence Footer

- `P0-C1-S1` / `P1-C1-S1`: `scripts/issues/plan_pr_prep.py` now derives aggregate PR titles from the selected commit phase set instead of always using `<ID>: <log title>`.
- `P0-C1-S2` / `P1-C1-S1`: `scripts/issues/plan_pr_prep.py` now inherits PR labels from explicit issue-side structural labels and may reuse `issue_projects` when that field is explicitly populated.
- `P0-C1-S3` / `P1-C1-S2`: `scripts/issues/plan_pr_prep.py` and `scripts/issues/create_pr_from_plan.py` now preserve separate `Evidence Footer` and `Development Link` sections and accept broader `Execution Checklist` heading variants.
- `P2-C1-S1` / `P2-C1-S2`: `docs/issues/pr-prep-S0E-4A-sample-plan.json` now renders `S0E-4A/P0-P3: GitHub pull request automation contract v1`, carries `EVOLUTION, s0/knowledge system, sub/1`, and the matching body preview now shows separate `Evidence Footer` and `Development Link` sections.
- `P3-C1-S1`: `scripts/issues/plan_pr_prep.py` now adds `drills` when the source log contains substantive evidence/drill execution.
- `P3-C1-S2`: `scripts/issues/gen_issue_draft.py` now defaults issue projects for `docs/logs/*` sources to `wordloom Board`, while `scripts/issues/plan_pr_prep.py` leaves PR projects empty unless `pr_projects` is explicitly populated.
- `P3-C1-S3`: live PR `#294` now uses title `S0E-4A/P0-P3: GitHub pull request automation contract v1`, carries labels `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`, and has been updated to the regenerated body shape with separate `Execution Checklist`, `Evidence Footer`, and `Development Link` sections without default project noise.
- `P3-C1-S3`: generated `Execution Checklist` lines now preserve backticks around the `P*-C*-S*` identifier segment so the rendered PR body matches the log-side checklist style.
- `P3-C1-S4`: issue-create now has a real project-assignment path, but GitHub-side project resolution remains blocked in the current environment by project lookup/auth limitations.
- `P3-C1-S5`: generated issue and PR bodies now start directly at `## Metadata`, removing the redundant top-level title heading while keeping machine-readable structure intact.
- `P3-C1-S6`: a first attempt to create the real `S0E-4B` PR from `main` failed on cherry-pick because the selected commit depends on unmerged `S0E-4A` file changes; the validation PR base is therefore temporarily stacked on `pr-prep/s0e-4a`.
- `P3-C1-S7`: the `S0E-4B` validation PR exposed that GitHub's stacked PR commit views can repeat already-reviewed upstream commits from the base PR branch ancestry; the review contract now treats compare-base semantics and `Files changed` as authoritative.
- `P3-C1-S8`: `scripts/issues/plan_pr_prep.py` now prefers checked execution-checklist phase coverage when deriving aggregate PR titles, so logs that already completed `P0-P2` at creation time still render `P0-P3` after the implementation-phase commits land.
- `P3-C1-S9`: the branch policy is now explicit: `S0E-docs-management-v5` remains the mixed authoring branch for the spine and parent-log ledger work, while `pr-prep/*` branches are short-lived review artifacts for one PR each.
- `P3-C1-S8`: live PR `#296` has been retitled from the commit-only `P3-C1-...` form to the checklist-derived aggregate form `S0E-4B/P0-P3: PR title compression, structural label inheritance, and body scope alignment follow-up v1`.
- `P3-C1-S10`: GitHub now shows real issue `#295` with labels `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`, and project item `wordloom Board / Backlog`, proving the issue-create project path works with the updated token scopes.
- `P3-C1-S11`: live PR `#296` is now retargeted to `main`, eliminating the temporary stacked-base review noise once upstream PR `#294` merged.

## Development Link

- Closes #295
