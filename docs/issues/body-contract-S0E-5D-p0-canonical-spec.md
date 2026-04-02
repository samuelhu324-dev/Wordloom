# S0E-5D/P0 Canonical Body Spec

## Global Formatting Rules

- Metadata-like bullet rows must be contiguous.
- No blank paragraph is allowed between adjacent bullet rows inside the same section.
- Canonical example:

```md
- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: ``
- Parent issue: #248
```

- Invalid example:

```md
- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`

- Projects: `wordloom Board`

- Milestone: ``

- Source log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`

- Parent issue: #248
```

## Inline Code Rules

- Metadata values must use inline code markers by default.
- Exception: GitHub short refs such as `#248`, `#299`, `#300`, `#307` must remain plain refs without backticks when used as Parent issue or Development issue style values.
- Links path/url refs must use inline code markers.

## Issue Creation Canonical Body

Section order:

1. `Metadata`
2. `Context`
3. `Definition of Done (DoD)`
4. `Links`

Canonical notes:

- `Context` must remain present even when empty.
- `Definition of Done (DoD)` must remain present even when empty.
- `Definition of Done (DoD)` must remain present even when empty for child issues.
- Top-level parent issues omit `Parent issue` from `Metadata`, omit `Parent log` from `Links`, and may render known child issue short refs in `Definition of Done (DoD)`.
- `Metadata` rows must stay contiguous with no blank rows between bullets.
- `Metadata` must not render `Source log`; deterministic log navigation belongs in `Links`.

Canonical child shape:

```md
## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: ``
- Parent issue: #248

## Context

## Definition of Done (DoD)

## Links

- Log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Parent log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous log: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
```

Canonical top-level parent shape:

```md
## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/0`
- Projects: `wordloom Board`
- Milestone: ``

## Context

## Definition of Done (DoD)

- #288
- #289

## Links

- Log: `docs/logs/log-S0E-docs-management-v5.md`
- Roadmap: `docs/roadmap/draft.md`
```

## Issue Conclusion Canonical Body

Section order:

1. `Metadata`
2. `Context`
3. `Definition of Done (DoD)`
4. `Links`

Canonical notes:

- `Context` must remain present and contain substantive conclusion-stage content.
- `Definition of Done (DoD)` must contain the related PR refs as short refs.
- Child-issue `Definition of Done (DoD)` must contain the related PR refs as short refs.
- Top-level parent issues keep the same section order, but their `Definition of Done (DoD)` remains a child-issue short-ref ledger instead of a merged-PR ledger.
- If multiple related PRs exist, each PR ref must be one bullet line.
- `Links` must not add issue or PR lines in the conclusion body contract.

Canonical child-conclusion shape:

```md
## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: ``
- Parent issue: #248

## Context

- Final lifecycle state has converged and the issue body now reflects the completed delivery set.

## Definition of Done (DoD)

- #299
- #300

## Links

- Log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Parent log: `docs/logs/log-S0E-docs-management-v5.md`
- Previous log: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
```

Canonical top-level parent refresh shape:

```md
## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/0`
- Projects: `wordloom Board`
- Milestone: ``

## Context

- This parent issue keeps the S0E spine aligned while the attached child issue set carries the delivery slices.

## Definition of Done (DoD)

- #288
- #289

## Links

- Log: `docs/logs/log-S0E-docs-management-v5.md`
- Roadmap: `docs/roadmap/draft.md`
```

## PR Canonical Body

Section order:

1. `Metadata`
2. `Summary`
3. `Execution Checklist`
4. `Links`
5. `Evidence Footer` when applicable

Canonical notes:

- `Metadata` rows must stay contiguous with no blank rows between bullets.
- `Metadata` is the only user-facing owner for development-issue identity in PR bodies.
- `Links` must keep deterministic navigation rows only and must not repeat the development issue as an `Issue` row.
- `Evidence Footer` is reserved for drills/evidence-carrying logs only.
- If the log does not qualify for Evidence Footer, the whole section must be omitted.
- Fallback to commit footer is not allowed.
- `Evidence Footer` must be rendered only from the log-owned `Evidence Footer Source` block.
- Each Evidence Footer row must keep the canonical source shape with inline-code-wrapped stage token and inline-code-wrapped artifact path.

Canonical shape:

```md
## Metadata

- Requested ID: `S0E-5B`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-5b`
- Source log: `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
- Labels: `drills, EVOLUTION, s0/knowledge system, sub/1`
- Development issue: #307

## Summary

- <summary bullet>

## Execution Checklist

- [x] `P0-C1-S1`: <checklist text>

## Links

- Log: `docs/logs/log-S0E-5B-guarded-lifecycle-apply-expansion.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`

## Evidence Footer

- `P1-C1-S1` | artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`
- `P2-C1-S1` | artifact: `docs/issues/pr-create-preflight-S0E-5C-p2-stop-branch-collision.json`
```

## P0-Locked Inputs For P1

- Evidence Footer applies only to drills/evidence class.
- Evidence Footer must be omitted entirely when not applicable.
- Commit-footer fallback is forbidden.

## Evidence Footer Source Contract

- The canonical source block name is `Evidence Footer Source`.
- The source block must live under `PR Summary Inputs (optional)`.
- Each source line must use this exact shape:

```md
- `P1-C1-S1` | artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`
```

- The stage token must use inline code.
- The artifact path must use inline code.
- The rendered PR `Evidence Footer` section must preserve the same line shape and order.
- Full details are recorded in `docs/issues/evidence-footer-S0E-5D-p1-canonical-spec.md`.