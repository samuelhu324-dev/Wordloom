# runbook-release-operational-register-issue-template

Use this template for one active or retained runbook-family release issue on the release board.

## Context

- Release identity: `<RUN-RELEASE/WORKFLOW-GITHUB-ISSUES-001>`
- Release summary: `<GitHub Issues full-auto pipeline>`
- Current standing: `<Drafting|Active|Retained>`
- Current reader goal: `<what a reader should understand about this release right now>`
- Scope note:
  - `<what this release currently owns>`
  - `<what is still out of scope or deferred>`

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

## Open Follow-ups

- `<next bounded revision or open PR still expected for this release>`
- `<optional retained historical backfill still worth doing later>`

## Usage Rules

- Keep stable artifact identity unchanged; update `current revision` instead of renaming the artifact.
- Use `R01`, `R01-R03`, and `R01/R03` only in reader-facing revision fields, not in file paths.
- Keep this issue focused on current effective release state; do not replay full source-log reasoning here.
- When one PR updates multiple artifacts, record that PR in each affected DoD or revision row instead of opening duplicate release issues.