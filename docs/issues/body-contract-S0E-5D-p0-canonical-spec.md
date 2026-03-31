# S0E-5D/P0 Canonical Body Spec

## Global Formatting Rules

- Metadata-like bullet rows must be contiguous.
- No blank paragraph is allowed between adjacent bullet rows inside the same section.
- Canonical example:

```md
- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: ``
- Source log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
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
- `Metadata` rows must stay contiguous with no blank rows between bullets.

Canonical shape:

```md
## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: ``
- Source log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Parent issue: #248

## Context

## Definition of Done (DoD)

## Links

- Log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Parent log: `docs/logs/log-S0E-docs-management-v5.md`
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
- If multiple related PRs exist, each PR ref must be one bullet line.
- `Links` must not add issue or PR lines in the conclusion body contract.

Canonical shape:

```md
## Metadata

- Labels: `EVOLUTION`, `s0/knowledge system`, `sub/1`, `drills`
- Projects: `wordloom Board`
- Milestone: ``
- Source log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
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
```

## PR Canonical Body

Section order:

1. `Metadata`
2. `Summary`
3. `Execution Checklist`
4. `Links`
5. `Evidence Footer` when applicable
6. `Development Link` only when an issue exists

Canonical notes:

- `Metadata` rows must stay contiguous with no blank rows between bullets.
- `Development Link` appears only when a development issue exists.
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
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/307`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`

## Evidence Footer

- `P1-C1-S1` | artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`
- `P2-C1-S1` | artifact: `docs/issues/pr-create-preflight-S0E-5C-p2-stop-branch-collision.json`

## Development Link

- Closes #307
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