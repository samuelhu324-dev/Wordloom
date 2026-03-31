# S0E-5D/P3 Rollout And Post-Audit Decision

## Decision

- Recommended rewrite rollout inside `S0E-5D` is `gate-first + selective historical rewrite`.
- Historical rewrite execution should be tracked as a new phase step `P4` under `S0E-5D`, not as a new `C` under `P3`.
- Post-apply live verify should be deferred out of `S0E-5D` and handled later under `S0E-5C`, where live publish and post-publish ownership already belong.
- Do not choose rewrite-first as the primary strategy.
- Do not wire GitHub Actions directly to mutation apply before the later `S0E-5C` post-apply verification link exists.

## Why This Order

- `gate-first` stops new drift immediately.
- `selective historical rewrite` should then repair only the smallest set needed to bring representative live history back under the same contract.
- `S0E-5D` stays focused on contract and historical normalization instead of taking ownership of post-publish orchestration.
- `S0E-5C` is the better home for post-apply verification because that slice already owns the open question around live PR publication boundaries.

## Minimal Historical Rewrite Set

### Issue-side mandatory set

- All inspected representative closed issues are affected by the new issue-conclusion contract because they still omit substantive `Context` and still keep `Issue` / `PR` rows in `Links`.
- Minimum inspected rewrite set:
  - `#293`
  - `#295`
  - `#297`
  - `#300`
  - `#303`
  - `#305`
  - `#307`

### PR-side representative set

- The smallest representative rewrite set that covers all observed PR drift families is:
  - `#299`: old commit-style footer rows
  - `#302`: invalid prose rows in `Links`, ineligible `Evidence Footer`, and wrong footer line shape
  - `#306`: old phase-heading-style footer rows
  - `#308`: metadata blank-gap drift plus old footer rows

### PR-side full inspected set

- The full inspected merged-PR set currently affected by the new PR contract is:
  - `#299`
  - `#301`
  - `#302`
  - `#304`
  - `#306`
  - `#308`

## Deferred Post-Apply Audit Chain

### Deferred ownership

- `S0E-5D` now stops at pre-apply contract enforcement plus historical rewrite planning.
- The later post-apply chain is intentionally deferred to `S0E-5C` because it sits closer to:
  - live PR publication;
  - post-publish evidence finalization;
  - eventual GitHub Actions orchestration.

### Why the deferred chain is still needed later

- Preview success alone is not enough once a command mutates live GitHub state.
- Live bodies can still drift because of:
  - stale rewrite scripts;
  - future direct `gh` edits that bypass preview generation;
  - GitHub-side normalization or human edits after merge.

## GitHub Actions Fit

- Yes, GitHub Actions can reject these problems.
- The practical model is still:
  - use preview/body-contract checks as pre-merge or pre-apply jobs;
  - later add live verification as a post-merge or post-apply job under `S0E-5C` ownership;
  - fail the workflow when the JSON result is `fail`.

## Footer Eligibility Rule

- Yes, `Evidence Footer` can be rejected when the source log is not drills/evidence eligible.
- Current enforcement now derives eligibility from source-log `tags`, `pr_labels`, and `title`.
- If the source log is not eligible, these should fail:
  - `Evidence Footer Source` present in the log
  - rendered `Evidence Footer` present in the PR body

## Immediate Next Step After P3

- Open `S0E-5D/P4` as the execution phase for one operator-safe historical rewrite slice.
- Inside `P4`, repair the representative PR set first: `#299`, `#302`, `#306`, `#308`.
- Then repair the inspected closed-issue set under the new issue-conclusion contract.
- Keep post-apply verification and GitHub Actions wiring deferred to the later `S0E-5C` follow-up.