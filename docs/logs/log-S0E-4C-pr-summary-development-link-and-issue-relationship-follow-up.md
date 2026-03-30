# log-S0E-4C (Phase 4C: PR Summary, Development Link, and Issue Relationship Follow-up)

---

**id**: `S0E-4C`
**kind**: `log`
**title**: `PR summary, development-link rendering, and issue relationship follow-up v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, PR, Issues, Automation, epic/s0, sub/0e4c`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/300`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/302`
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
  **reference_log_1**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-03-30`
**updated**: `2026-03-30`

---

## Decision / Outcome

**Decision**:

- `S0E-4C` exists as the next narrow follow-up after `S0E-4B`, focused on three specific GitHub-facing mismatches that are still visible in live output.
- PR body metadata should render `Development issue` as a plain short issue reference such as `#297`, not as a raw URL and not as a code span.
- PR creation must not allow a final `<placeholder>` summary in the generated or live PR body; `PR Summary Inputs -> PR summary bullets` are required inputs for any real PR create path.
- Child issue `Metadata -> Parent issue` and GitHub sidebar `Relationships` should be aligned through an explicit relationship-attach path; `Parent issue` in body text is not sufficient by itself.

**Default choices (phase defaults / v1)**:

- PR follow-ups remain separate from issue-conclusion follow-ups; PR creation has only one body lifecycle, so required review-facing content such as `Summary` must be present before PR creation.
- If a source log has no `PR summary bullets`, dry-run may still show a warning preview, but real PR creation should fail closed instead of publishing `<placeholder>` into a live PR.
- `pr_development_issue` should normalize URLs or raw numbers into short GitHub issue references before body rendering and before `Closes ...` lines are emitted.
- Child issues may continue to show `Parent issue` only in `Metadata`, but GitHub-side `Relationships` for the same parent/child pair should be attached explicitly through a dedicated apply path.
- Top-level issues/logs still leave `issue_parent` blank and do not require a parent relationship attach.

## PR Summary Inputs (optional)

- Use this block because `S0E-4C` is expected to drive another PR automation follow-up directly.

**PR summary bullets**:

- Harden `create_pr_from_plan.py` so a long-lived mixed working branch can still produce a clean PR-prep branch when raw cherry-picks conflict on selected commits.
- Keep PR-prep planning and create-path execution aligned around the current remote-tracking base and the source-head final file state used for the prep branch.
- Re-run one real `S0E-4C` follow-up PR and update issue `#300` so the extra merged PR is reflected in the final DoD ledger.

**PR checklist source**:

- Default source: reuse this log's execution checklist once the contract, implementation, and real validation are complete.

**PR links / evidence footer**:

- Log: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/300`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/pr-prep-S0E-4C-p5-plan.json`

- Generated PR body should keep `Summary`, `Evidence Footer`, and `Development Link` as separate sections.
- `Summary` must not degrade to `<placeholder>` on a live PR create path.

## Definitions (optional)

- **Short issue reference**: a plain GitHub issue reference such as `#297` used in PR metadata or issue metadata without a code span and without a full URL.
- **PR summary input**: the `PR Summary Inputs -> PR summary bullets` block inside a source log that feeds the generated PR `Summary` section.
- **Relationship attach**: the GitHub-side operation that links a child issue to its parent so the sidebar `Relationships` panel reflects the same relation already carried in issue metadata.
- **Fail-closed PR create**: the rule that real PR creation stops when required structured inputs such as summary bullets are missing instead of silently shipping placeholders.

## Constraints

- Do not infer PR summary bullets from commit subjects or from the log title when the source log omitted explicit PR summary inputs.
- Do not treat issue body text as a substitute for GitHub sidebar relationships; sidebar state must come from a real attach path.
- Do not attach parent relationships for top-level issues that intentionally have no parent.
- Do not let URL-vs-short-ref formatting drift between `Metadata` and `Development Link` inside the same PR body.

## Scope

- `P0`: contract for PR summary requiredness, development-issue rendering, and parent-relationship attach boundary
- `P1`: planner/create-path implementation updates in PR and issue relationship tooling
- `P2`: dry-run regeneration and artifact validation against representative `S0E` samples
- `P3`: real GitHub validation against one PR sample and one child-issue relationship sample
- `P4`: one full end-to-end `issue creation -> PR -> issue conclusion` closed-loop drill under the `S0E-4C` rules
- `P5`: follow-up hardening for create-path cherry-pick conflicts on the long-lived mixed `S0E` working branch

## Success Criteria (DoD)

- Generated PR metadata renders `Development issue` as a plain short ref such as `#297`.
- Generated `Development Link` continues to use normalized short refs such as `Closes #297`.
- Real PR creation fails closed when `PR Summary Inputs -> PR summary bullets` are missing.
- Representative PR previews no longer emit `<placeholder>` summaries once required inputs are supplied.
- Child issues with `Parent issue: #248` can also show the same parent in GitHub sidebar `Relationships` after an explicit apply step.
- Top-level issues still omit both `Parent issue` metadata and parent relationship attach.
- The runbook distinguishes clearly between relationship planning and relationship apply, just as it already distinguishes dry-run from real apply in other slices.

## Stability (what stable means)

- This log can be marked `stable` when:
  - PR summary requiredness, short-ref development-link rendering, and issue-relationship attach rules are fixed in contract and implementation;
  - at least one real PR body and one real child issue relationship have been validated against the updated behavior.

## P0 (Contract | v1)

### P0-C1-S1 (PR development-issue rendering | v1)

- `pr_development_issue` may still accept a raw issue URL or raw number as input, but rendered PR metadata should normalize it to a plain short ref such as `#297`.
- The same normalized ref set should be reused consistently in `Metadata -> Development issue` and in `Development Link` lines.
- The rendered metadata row must not wrap the short ref in backticks.

### P0-C1-S2 (PR summary requiredness | v1)

- `PR Summary Inputs -> PR summary bullets` are optional at template level but mandatory for any real PR create path.
- Dry-run preview may warn when summary bullets are missing, but real PR creation should stop with an explicit error instead of using `- <placeholder>`.
- Commit subjects and log titles may support diagnostics, but they are not allowed to replace missing human-authored PR summary bullets automatically.

### P0-C1-S3 (Issue parent relationship attach boundary | v1)

- `Parent issue` in issue `Metadata` and GitHub sidebar `Relationships` refer to the same logical parent-child relation, but they are produced by different mechanisms.
- Body rendering alone does not attach a GitHub relationship; a separate relationship apply path is required.
- Child issues should be eligible for that attach path when an exact parent issue reference is already known.
- Top-level issues must remain excluded from parent attach behavior.

### P0-C1-S4 (Evidence contract | v1)

- Evidence JSON for this slice must include:
  - source log path and requested ID
  - normalized development issue refs used in preview/create output
  - whether PR summary bullets were present or missing
  - relationship plan/apply result paths for any live child-parent attach sample

## P1 (Implementation | v1)

### P1-C1-S1 (PR development-issue normalization | v1)

- `scripts/issues/plan_pr_prep.py` should persist normalized short issue refs so preview artifacts and later create/apply paths can reuse the same canonical display form.
- `scripts/issues/create_pr_from_plan.py` should rewrite the generated metadata row to the normalized short-ref form before publishing a live PR body.

### P1-C1-S2 (PR create fail-closed summary gate | v1)

- `scripts/issues/create_pr_from_plan.py` should refuse live PR creation when the preview body still contains `- <placeholder>` inside `Summary`.
- The same gate should also fire when the planned item reports zero explicit `PR Summary Inputs -> PR summary bullets`.

### P1-C1-S3 (Issue relationship apply path | v1)

- `scripts/issues/apply_issue_relationships.py` should consume a reviewed relationship plan item and attach the child issue to its parent through GitHub GraphQL sub-issue mutation.
- The apply path should be idempotent for already-correct relationships and fail closed when the child is already attached to a different parent.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-4C/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle.
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit.
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title.

**Branch convention**:

- `S0E` follow-up work should continue on `S0E-docs-management-v5` as the mixed authoring branch.
- Any review-ready PR for this slice may still be cut through a dedicated `pr-prep/s0e-4c` branch from the chosen base.

## Plan (draft)

### P1 (Implementation)

- P1-C1-S1: normalize PR development-issue rendering to short refs in preview/create paths
- P1-C1-S2: make real PR creation fail closed when PR summary bullets are missing
- P1-C1-S3: add issue relationship apply tooling for exact child-parent attach

### P2 (Drill / Verify)

- P2-C1-S1: regenerate representative PR-prep artifacts after short-ref and summary-requiredness changes
- P2-C1-S2: regenerate relationship plan/apply sample artifacts for one existing child issue under `S0E`

### P3 (Drill / Verify)

- P3-C1-S1: validate one real PR body against normalized development issue and non-placeholder summary rules
- P3-C1-S2: validate one real child issue so sidebar `Relationships` matches `Metadata -> Parent issue`
- P3-C1-S3: audit the four historical `S0E` PRs shown in the merged list and remediate any body drift against the current PR contract

### P4 (Closed-loop Drill)

- P4-C1-S1: run one full `issue creation -> PR -> issue conclusion` cycle under the post-`S0E-4C` contracts
- P4-C1-S2: verify that the same sample keeps short-ref metadata, non-placeholder PR summary, attached child relationship, and final issue conclusion consistency end to end

### P5 (Create-path Hardening)

- P5-C1-S1: harden `scripts/issues/create_pr_from_plan.py` so selected-commit cherry-pick conflicts can fall back to a source-head snapshot of the selected path set
- P5-C1-S2: validate the hardened create-path by opening one additional real `S0E-4C` PR and updating issue `#300` after merge

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: PR development-issue short-ref rendering fixed in contract
- [x] `P0-C1-S2`: PR summary requiredness fixed in contract
- [x] `P0-C1-S3`: issue parent relationship attach boundary fixed in contract
- [x] `P0-C1-S4`: evidence contract fixed

### P1 (Implementation)

- [x] `P1-C1-S1`: PR preview/create development-issue rendering normalized
- [x] `P1-C1-S2`: real PR create path blocks placeholder summaries
- [x] `P1-C1-S3`: issue relationship apply tooling added

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: representative PR-prep artifacts regenerated and reviewed
- [x] `P2-C1-S2`: representative issue relationship artifacts regenerated and reviewed

### P3 (Drill / Verify)

- [x] `P3-C1-S1`: one real PR validated against the updated body contract
- [x] `P3-C1-S2`: one real child issue validated against the updated relationship attach path
- [x] `P3-C1-S3`: historical `S0E` PR audit completed and outdated live bodies remediated

### P4 (Closed-loop Drill)

- [x] `P4-C1-S1`: one full `issue creation -> PR -> issue conclusion` cycle completed under `S0E-4C`
- [x] `P4-C1-S2`: end-to-end artifacts reviewed for contract consistency

### P5 (Create-path Hardening)

- [x] `P5-C1-S1`: create-path cherry-pick conflict hardening implemented
- [x] `P5-C1-S2`: one additional real `S0E-4C` PR validated and issue `#300` updated

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- Initial diagnosis before implementation:
  - live PR `#298` currently renders `Development issue: #297` correctly as plain text, but its `Summary` section is still `- <placeholder>` because the source log `S0E-2D` has no `PR Summary Inputs -> PR summary bullets` block.
  - current PR generator logic in `scripts/issues/plan_pr_prep.py` explicitly falls back to `- <placeholder>` when summary bullets are missing.
  - current relationship tooling stops at `scripts/issues/plan_issue_relationships.py`, which is a dry-run planner only and does not attach GitHub sidebar relationships.
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
- `P5-C1-S1`: `scripts/issues/create_pr_from_plan.py` now records the current `origin/<base>` merge-base at apply time and, on cherry-pick conflict, rebuilds the prep branch from the source-head snapshot of the selected path set instead of failing immediately.
- `P5-C1-S2`: `docs/issues/pr-prep-S0E-4C-p5-create-result.json` confirms that real PR creation for `#302` triggered the new fallback at conflicting SHA `18fbfe40`, rebuilt the branch successfully, and still published a live PR with short-ref `Development issue: #300`.
- `P5-C1-S2`: live PR `#302` merged at `2026-03-30T04:21:10Z` with merge commit `3c47e396`, and `docs/issues/issue-conclusion-S0E-4C-p5-plan.json` plus `docs/issues/issue-conclusion-S0E-4C-p5-s0e-4c-apply-result.json` prove issue `#300` now carries `DoD -> #301` and `#302`.

## Recent changes (for traceability, optional)

- 2026-03-30: opened `S0E-4C` to isolate the remaining GitHub-facing mismatches after `S0E-4B`, `S0E-2D`, and `S0E-2E` were otherwise stabilized.
- 2026-03-30: recorded that live PR `#298` still carries a placeholder summary because the source log omitted `PR summary bullets`, which means the next fix belongs in PR create-path requiredness rather than in issue conclusion.
- 2026-03-30: recorded that child issue body metadata already carries `Parent issue: #248`, but sidebar `Relationships` remains unattached because the repo currently has a relationship planner without a real apply path.
- 2026-03-30: completed `P0-P1` by fixing the contract, normalizing PR development-issue rendering in preview/create code paths, adding a fail-closed guard for placeholder PR summaries, and introducing a real relationship apply script for GitHub sidebar parent-child attachment.
- 2026-03-30: completed `P2` by regenerating `S0E-2D` PR-prep sample artifacts with explicit `PR Summary Inputs` and by producing canonical `S0E-4C` relationship plan/apply sample artifacts for existing child issue `#295` under parent `#248`.
- 2026-03-30: completed `P3-C1-S1` and `P3-C1-S3` by auditing historical merged PRs `#294/#296/#298/#299`, confirming that `#294` and `#299` were already compliant, rewriting live PR `#296` to use short-ref `Development issue: #295`, and rewriting live PR `#298` to use the regenerated non-placeholder Summary plus a separate `Development Link` section.
- 2026-03-30: completed `P4` by creating live issue `#300`, attaching it to parent `#248`, opening and merging PR `#301`, writing the final conclusion body back to the already-closed issue, and verifying that creation / PR / relationship / conclusion all now align under one `S0E-4C` sample.
- 2026-03-30: while running `P4`, fixed PR-prep base comparison so dry-run commit selection now prefers `origin/<base>` when available, preventing stale local base refs from diverging from the real create-path base.
- 2026-03-30: opened `P5` as a focused follow-up to harden `create_pr_from_plan.py` against cherry-pick conflicts on the long-lived mixed `S0E` working branch, with one more real PR and one more issue `#300` write-back as the proof path.
- 2026-03-30: completed `P5` by hardening `create_pr_from_plan.py` with a source-head snapshot fallback, creating and merging real PR `#302` through that path, and updating issue `#300` so its final DoD ledger now includes both `#301` and `#302`.