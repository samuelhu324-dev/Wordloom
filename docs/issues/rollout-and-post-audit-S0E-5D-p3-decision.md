# S0E-5D/P3 Rollout And Post-Audit Decision

## Decision

- Recommended rollout is `gate-first + post-apply live verify + selective historical rewrite`.
- Do not choose rewrite-first as the primary strategy.
- Do not wire GitHub Actions directly to mutation apply before the post-apply verification link exists.

## Why This Order

- `gate-first` stops new drift immediately.
- `post-apply live verify` catches drift introduced by live write paths, GitHub-side body normalization, or commands that bypass preview artifacts.
- `selective historical rewrite` should then repair only the smallest set needed to bring representative live history back under the same contract.

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

## Post-Apply Audit Chain

### Recommended chain

1. Pre-apply gate:
   - run create-time or rewrite-time contract checks on preview bodies before mutation
   - fail closed on section-order, link-category, footer-shape, and footer-eligibility defects
2. Apply:
   - perform the live GitHub mutation only if the pre-apply gate passes
3. Post-apply live verify:
   - fetch the live PR body and validate it again against the same contract
   - fetch the live issue body and validate it through lifecycle/body-shape audit
4. Report:
   - publish pass/fail JSON artifacts that GitHub Actions can treat as hard gates

### Why a post-apply chain is needed

- Preview success alone is not enough once a command mutates live GitHub state.
- Live bodies can still drift because of:
  - stale rewrite scripts;
  - future direct `gh` edits that bypass preview generation;
  - GitHub-side normalization or human edits after merge.

## GitHub Actions Fit

- Yes, GitHub Actions can reject these problems.
- The practical model is:
  - use preview/body-contract checks as pre-merge or pre-apply jobs;
  - use live verification as a post-merge or post-apply job;
  - fail the workflow when the JSON result is `fail`.

## Footer Eligibility Rule

- Yes, `Evidence Footer` can be rejected when the source log is not drills/evidence eligible.
- Current enforcement now derives eligibility from source-log `tags`, `pr_labels`, and `title`.
- If the source log is not eligible, these should fail:
  - `Evidence Footer Source` present in the log
  - rendered `Evidence Footer` present in the PR body

## Immediate Next Step After P3

- Implement one operator-safe historical rewrite slice that repairs the representative PR set first: `#299`, `#302`, `#306`, `#308`.
- Then repair the inspected closed-issue set under the new issue-conclusion contract.
- After that, wire the same check scripts into GitHub Actions.