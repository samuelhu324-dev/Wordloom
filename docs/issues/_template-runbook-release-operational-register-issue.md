# runbook-release-operational-register-issue-template

Use this template for one active or retained runbook-family release issue on the release board.

## Context

- Release identity: `<RUN-RELEASE/WORKFLOW-GITHUB-ISSUES-001>`
- Release summary: `<GitHub Issues full-auto pipeline>`
- Board state: `<Drafting|Active|Retained>`
- Current reader goal: `<what a reader should understand about this release right now>`
- Scope note:
  - `<what this release currently owns>`
  - `<what is still out of scope or deferred>`

## Board State

- Current board state: `<Drafting|Active|Retained>`
- State note:
  - `Drafting`: `<release shape still being assembled or corrected; current register may still be incomplete>`
  - `Active`: `<release is the live operational register for ongoing revisions or follow-up PRs>`
  - `Retained`: `<release is no longer the live working register, but remains worth keeping as a reader-facing retained record>`

## Definition of Done (DoD)

### Release

- [ ] Artifact: `<run-WORKFLOW-GITHUB-ISSUES-001-...md>`
  - Stable identity: `<RUN-RELEASE/WORKFLOW-GITHUB-ISSUES-001>`
  - Current revision: `<R01>`
  - Current standing: `<branch-only|pr-open|merged-to-main>`
  - PR refs:
    - `<PR #...>`

### Ledger

- [ ] Artifact: `<ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-...md>`
  - Stable identity: `<RUN-LEDGER-001>`
  - Current revision: `<R01>`
  - Current standing: `<branch-only|pr-open|merged-to-main>`
  - PR refs:
    - `<PR #...>`

### Supplement Ledger (SUP)

- [ ] Artifact: `<ledger-run-SUP-001-WORKFLOW-GITHUB-ISSUES-001-...md>`
  - Stable identity: `<RUN-LEDGER-SUP-001>`
  - Current revision: `<R01>`
  - Current standing: `<branch-only|pr-open|merged-to-main>`
  - PR refs:
    - `<PR #...>`

- [ ] Artifact: `<ledger-run-SUP-002-WORKFLOW-GITHUB-ISSUES-001-...md>`
  - Stable identity: `<RUN-LEDGER-SUP-002>`
  - Current revision: `<R01>`
  - Current standing: `<branch-only|pr-open|merged-to-main>`
  - PR refs:
    - `<PR #...>`

### Patch

- [ ] Artifact: `<ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-...md>`
  - Stable identity: `<RUN-LEDGER-PATCH-001>`
  - Current revision: `<R01|R02>`
  - Current standing: `<branch-only|pr-open|merged-to-main>`
  - PR refs:
    - `<PR #...>`

- [ ] Artifact: `<ledger-run-PATCH-002-WORKFLOW-GITHUB-ISSUES-001-...md>`
  - Stable identity: `<RUN-LEDGER-PATCH-002>`
  - Current revision: `<R01>`
  - Current standing: `<branch-only|pr-open|merged-to-main>`
  - PR refs:
    - `<PR #...>`

## Canonical Artifacts

- Release:
  - `<docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-...md>`
- Parent ledger:
  - `<docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-...md>`
- Active SUP set:
  - `<docs/runbook/support-only/ledger-run-SUP-001-WORKFLOW-GITHUB-ISSUES-001-...md>`
  - `<docs/runbook/support-only/ledger-run-SUP-002-WORKFLOW-GITHUB-ISSUES-001-...md>`
- Active PATCH set:
  - `<docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-...md>`
  - `<docs/runbook/support-only/ledger-run-PATCH-002-WORKFLOW-GITHUB-ISSUES-001-...md>`

## Revision Register

| stable artifact identity | current revision | revision span in play | current standing | latest PR refs | notes |
| --- | --- | --- | --- | --- | --- |
| `<RUN-RELEASE/WORKFLOW-GITHUB-ISSUES-001>` | `<R01>` | `<R01>` | `<merged-to-main>` | `<PR #...>` | `<optional>` |
| `<RUN-LEDGER-001>` | `<R01>` | `<R01>` | `<merged-to-main>` | `<PR #...>` | `<optional>` |
| `<RUN-LEDGER-SUP-001>` | `<R01>` | `<R01>` | `<merged-to-main>` | `<PR #...>` | `<optional>` |
| `<RUN-LEDGER-SUP-002>` | `<R01>` | `<R01>` | `<merged-to-main>` | `<PR #...>` | `<optional>` |
| `<RUN-LEDGER-PATCH-001>` | `<R02>` | `<R01-R02>` | `<merged-to-main>` | `<PR #...>, <PR #...>` | `<optional>` |
| `<RUN-LEDGER-PATCH-002>` | `<R01>` | `<R01>` | `<merged-to-main>` | `<PR #...>` | `<optional>` |

## Mainline State

- Current mainline standing: `<branch-only|pr-open|merged-to-main>`
- Branch note: `<which working branch currently carries the newest revision if not yet merged>`
- Reader rule:
  - `branch-only`: the newest revision exists only on the working branch
  - `pr-open`: the newest revision is published for review but not yet merged
  - `merged-to-main`: the newest revision is now visible on `main`

## State Coordination Rule

- Prefer `Drafting` when the release issue is still being materially assembled, even if one artifact row is already `branch-only` or `pr-open`.
- Prefer `Active` when the issue already acts as the maintained operational register for the release, regardless of whether the newest artifact revision is still `branch-only`, already `pr-open`, or fully `merged-to-main`.
- Prefer `Retained` when the release is no longer the active working register and future change is expected to land on a newer release issue or a different active operating surface.
- Keep `Board state` at the issue level and `Current standing` / `Current mainline standing` at the artifact or revision level; do not collapse them into one field.

## Open Follow-ups

- `<next bounded revision or open PR still expected for this release>`
- `<optional retained historical backfill still worth doing later>`

## Usage Rules

- Keep stable artifact identity unchanged; update `current revision` instead of renaming the artifact.
- Use `R01`, `R01-R03`, and `R01/R03` only in reader-facing revision fields, not in file paths.
- Keep this issue focused on current effective release state; do not replay full source-log reasoning here.
- Treat `Drafting`, `Active`, and `Retained` as board-placement semantics, not as substitutes for `branch-only`, `pr-open`, or `merged-to-main`.
- When one PR updates multiple artifacts, record that PR in each affected DoD or revision row instead of opening duplicate release issues.