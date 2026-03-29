# log-S0E-2E (Phase 2E: Issue Conclusion and Development Linkage Contract)

---

**id**: `S0E-2E`
**kind**: `log`
**title**: `issue conclusion and development linkage contract v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, PR, Automation, epic/s0, sub/0e2e`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **reference_log_1**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-4B-pr-title-label-and-body-follow-up.md`
  **reference_log_3**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
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
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: ``
**pr_development_issue**: ``
**created**: `2026-03-29`
**updated**: `2026-03-29`

---

## Decision / Outcome

**Decision**:

- `S0E-2E` defines issue conclusion as a separate post-merge slice instead of leaving issue closure as an informal manual step.
- v1 requires the final issue conclusion to carry explicit Development linkage to the merged PR or PR set that delivered the same ID-scoped work.
- The final issue-conclusion content must be English-only and should close the lifecycle that started with issue creation.
- The lifecycle order is fixed as: `Issue Creation -> Logs completed -> PR -> human merge -> Issue Conclusion`.

**Default choices (phase defaults / v1)**:

- Issue conclusion happens only after merge; draft PRs or unmerged PRs are not sufficient to trigger final conclusion output.
- The Development block must point to the merged PR set that shares the same exact ID prefix as the issue, unless an explicit override is recorded.
- `Definition of Done (DoD)` in the conclusion should enumerate merged PR references and titles, not restate the original contract bullets.
- Conclusion content must stay English-only.
- Merge approval remains a human review step outside automation scope even when conclusion generation exists.

## Definitions (optional)

- **Issue conclusion**: the final structured close-out content written back to an issue after the associated development PRs have merged.
- **Development linkage**: the explicit relationship from an issue to the PR or PR set that implemented the work.
- **Merged PR evidence**: the set of merged PR numbers, titles, and URLs that prove the issue's implementation path is complete.
- **ID-scoped PR set**: the merged PRs whose titles or commit scopes use the same exact log/issue ID prefix, such as `S0E-2B`.

## Constraints

- Do not conclude an issue before the relevant PR is merged.
- Do not infer unrelated PRs by loose keyword matching; exact ID prefix matching remains the default boundary.
- Do not keep the conclusion body bilingual.
- Do not reuse the original issue-creation `Definition of Done (DoD)` bullets as the final conclusion text.
- Do not let automation perform the merge; merge approval remains human-owned.

## Scope

- `P0`: contract for lifecycle order, post-merge boundary, development linkage, and English conclusion body rules
- `P1`: final issue-conclusion body shape and PR-selection rules
- `P2`: dry-run conclusion planning from merged PR metadata
- `P3`: real issue-conclusion write-back after a human-approved merge

## Success Criteria (DoD)

- The issue-conclusion contract only activates after merge.
- The final issue content includes an explicit Development section that points to the merged PR or PR set for the same exact ID scope.
- `Definition of Done (DoD)` in the conclusion uses merged PR references such as `S0E-2B/P0-P3: ... #<pr>` rather than generic prose.
- The conclusion body is English-only.
- The contract explains how merged PR titles/IDs are selected and how multiple PRs are ordered when one issue spans more than one review slice.

## Stability (what stable means)

- This log can be marked `stable` when:
  - post-merge issue conclusion rules, Development linkage rules, and English conclusion body structure are fixed and validated through at least one dry-run plus one real write-back;
  - issue closure no longer depends on operator memory to find and format the merged PR evidence.

## P0 (Contract | v1)

### P0-C1-S1 (Lifecycle order and merge boundary | v1)

- Issue conclusion is the last operator-facing documentation step after merge.
- The required order is:
  - issue creation
  - logs completed
  - PR created
  - merge completed by human review
  - issue conclusion written back
- A PR being open, draft, or approved is not enough; merge completion is the minimum trigger.

### P0-C1-S2 (Development linkage and PR selection | v1)

- The conclusion's Development block should list merged PRs whose titles or scope identifiers share the same exact issue/log prefix.
- Exact ID prefix matching is the default selection rule; overrides must be explicit and traceable.
- If multiple merged PRs belong to the same issue, they should be ordered by phase span or merge order, not by arbitrary search result order.
- If no merged PR exists yet, the issue cannot enter final conclusion mode.

### P0-C1-S3 (English conclusion body and DoD rule | v1)

- The final issue-conclusion body should use English-only headings and content.
- The recommended structure is:

```md
## Development

- Merged PR: `S0E-2B/P0-P3: real GitHub issue creation automation (draft-generation -> create-issue) v1` #294

## Definition of Done (DoD)

- `S0E-2B/P0-P3: real GitHub issue creation automation (draft-generation -> create-issue) v1` #294

## Links

- Log: `docs/logs/log-S0E-2B-...md`
- Issue: `https://github.com/.../issues/...`
- PR: `https://github.com/.../pull/...`
```

- `Definition of Done (DoD)` in the conclusion is a merged-PR evidence block, not a replay of the original contract acceptance bullets.
- If a short `Context` section is retained in the final conclusion body, it must stay English-only and reflect closure state rather than re-explaining the original contract.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-2E/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S0E-2E` work should stay on the active `S0E-*` branch until conclusion automation needs an isolated review slice.

**Commit discipline (recommended)**:

- Fix the merge-boundary and PR-selection contract first, then validate dry-run conclusion planning, then perform one real issue-conclusion write-back after merge.

## Plan (draft)

### P1 (Conclusion body and PR-selection rules)

- P1-C1-S1: define the final English issue-conclusion body shape
- P1-C1-S2: define exact-ID PR selection and multi-PR ordering rules

### P2 (Dry-run conclusion planning)

- P2-C1-S1: plan conclusion output from merged PR metadata without writing back to GitHub
- P2-C1-S2: verify Development and DoD formatting against representative merged PR samples

### P3 (Real issue-conclusion write-back)

- P3-C1-S1: update one real issue with the final conclusion body after merge
- P3-C1-S2: record which merged PRs were attached and how the final DoD block was rendered

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: lifecycle order and merge boundary fixed
- [ ] `P0-C1-S2`: development linkage and PR selection rules fixed
- [ ] `P0-C1-S3`: English conclusion body and DoD rule fixed

### P1 (Conclusion body and PR-selection rules)

- [ ] `P1-C1-S1`: final English issue-conclusion body shape defined
- [ ] `P1-C1-S2`: exact-ID PR selection and ordering rules fixed

### P2 (Dry-run conclusion planning)

- [ ] `P2-C1-S1`: dry-run conclusion planning completed
- [ ] `P2-C1-S2`: Development and DoD formatting validated against merged PR samples

### P3 (Real issue-conclusion write-back)

- [ ] `P3-C1-S1`: one real issue-conclusion write-back completed after merge
- [ ] `P3-C1-S2`: merged PR attachment accounting recorded

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

## Recent changes (for traceability, optional)

- 2026-03-29: opened `S0E-2E` to define post-merge issue conclusion, Development linkage, and final English DoD rendering as a separate slice from issue creation and PR creation.
