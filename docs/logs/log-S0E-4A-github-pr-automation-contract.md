# log-S0E-4A (Phase 4A: GitHub PR Automation Contract)

---

**id**: `S0E-4A`
**kind**: `log`
**title**: `GitHub pull request automation contract v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, PR, Automation, epic/s0, sub/0e4a`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/293`
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
  **reference_log_1**: `docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
  **reference_log_2**: `docs/logs/_template-log-parent-epic-spine.md`
  **reference_log_3**: `docs/logs/_template-log-phase-drills-evidence.md`
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
**pr_labels**: `EVOLUTION`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/293`
**created**: `2026-03-29`
**updated**: `2026-03-29`

---

## Decision / Outcome

**Decision**:

- `S0E-4A` defines PR automation as a separate contract instead of hiding it inside issue automation.
- v1 treats PR creation as its own object model: commit selection, PR metadata, project assignment, milestone assignment, development linking, and human-readable PR description.
- The stable workflow preserves day-to-day work on mixed branches while still allowing ID-scoped PRs to be created safely.

**Default choices (phase defaults / v1)**:

- PR automation should default to a dry-run or PR-prep mode before any real PR creation mode exists.
- The most stable commit-selection strategy is `prepare a clean PR branch from the target base, then cherry-pick the ID-scoped commits`, not `open a PR directly from a mixed working branch`.
- PR titles should reuse the same ID prefix as the underlying logs and issues.
- PR descriptions should prioritise the child-log execution checklist in a clean human-readable block; the PR timeline remains the detailed mechanical history.

## Definitions (optional)

- **ID-scoped PR**: a pull request whose selected commits all belong to one exact ID prefix such as `S0E-2B`.
- **PR-prep branch**: a clean branch created from the target base for one PR, populated only with the selected commits.
- **Mixed working branch**: a branch that contains commits for multiple IDs or scopes.
- **Development link**: the issue/PR relationship shown in GitHub Development panels and linked references.

## Constraints

- Do not rely on GitHub to filter commits by commit-message prefix inside one mixed branch.
- Do not make PR automation depend on manual copy/paste of labels, milestones, or project names when frontmatter can carry them explicitly.
- Do not let PR creation rewrite or hide the original working branch history.
- Do not treat PR timeline details as a replacement for a clean human-readable PR description.

## Scope

- `P0`: contract for commit selection, PR metadata fields, and description structure
- `P1`: template field updates for PR metadata extraction
- `P2`: dry-run PR prep flow from mixed branch to clean PR-prep branch
- `P3`: real PR creation and metadata assignment with issue/development linkage

## Current Status

- `P0` is complete: the stable PR-prep strategy, metadata precedence, description boundary, and development-link boundary are now fixed in this log.
- `P1` is complete: the parent and phase log templates now expose final `pr_*` field guidance plus explicit PR summary/checklist/evidence scaffold inputs.
- `P2` is complete: a manifest-driven dry-run PR-prep planner now selects exact ID-scoped commits from the mixed working branch and emits both a structured plan and a body preview artifact.
- The next gap is no longer PR-prep planning; it is whether the same boundary can survive a real PR creation path with metadata assignment and Development linkage.
- `S0E-4A` remains `draft` because the contract has not yet been exercised by a real PR create run.

## Success Criteria (DoD)

- The contract explicitly defines a stable commit-selection strategy for ID-scoped PRs.
- Log templates expose enough PR metadata for automation to extract labels, projects, milestone, base branch, and development issue.
- PR descriptions have one simple, repeatable structure that can be generated from child-log execution checklists.
- The contract explains how PR automation coexists with a constantly updated working branch without losing unrelated scope work.

## Stability (what stable means)

- This log can be marked `stable` when:
  - commit selection, PR metadata extraction, PR description generation, and development-link semantics are fixed and exercised;
  - operators can create an ID-scoped PR from a mixed working branch without losing access to the rest of their ongoing work.

## P0 (Contract | v1)

### P0-C1-S1 (Commit selection strategy | v1)

- The stable strategy is: start from the target base branch, create a clean PR-prep branch, and cherry-pick only the commits that belong to the requested ID.
- A mixed working branch may stay as the main day-to-day branch; PR automation must not require the operator to abandon it.
- Commit-selection evidence should always record the selected commit SHAs and the ID that justified their inclusion.
- Commit selection must stay fail-closed: if the operator cannot produce an explicit ID or if candidate commits are ambiguous, automation should stop at a dry-run report instead of preparing a PR branch.
- The selected commit set belongs to one exact PR scope at a time; if one working branch contains both `S0E-4A` and unrelated commits, the PR-prep result must include only the commits that match the requested scope.
- Cherry-pick conflict handling is outside automated resolution in v1; automation may surface the failing SHA and stop, but it must not silently rewrite commit content.

### P0-C1-S2 (PR metadata and description contract | v1)

- PR automation should extract `pr_labels`, `pr_projects`, `pr_milestone`, `pr_base`, and `pr_development_issue` from frontmatter when present.
- PR titles should reuse the log or issue ID prefix and follow the same naming discipline minus the `log-` filename prefix.
- PR descriptions should start from the child-log execution checklist and preserve a concise, human-readable summary.
- Frontmatter stays the source of truth for machine-applied PR metadata; if a `pr_*` field is blank, automation must leave that field blank instead of copying issue metadata by guesswork.
- PR description generation should produce one stable human-facing structure: short summary, execution checklist block, explicit links back to the source log and issue, and a machine-readable evidence footer when artifacts exist.
- The generated PR body should summarise the selected scope, not replay the full commit timeline; low-level commit chronology remains visible in git and the PR timeline.

### P0-C1-S3 (Development link and review boundary | v1)

- PR automation may prepare the Development link metadata, but merge approval remains a human review step.
- The PR should link back to its issue through explicit metadata and body references, not guesswork.
- No automatic merge is part of v1.
- `pr_development_issue` is the only approved source for Development linkage in v1; if it is blank or unresolved, automation should create a PR without the link rather than invent a relationship.
- Reviewers, approvals, and merge execution remain outside automation scope even after real PR creation exists; v1 only prepares or creates the PR object and its metadata.
- PR automation must preserve traceability back to the originating log, selected commit SHAs, and target base branch so human reviewers can audit why this PR exists.

## P0 (Contract closure | v1)

### P0-C1-S4 (Evidence contract | v1)

- Evidence for this slice should prove:
  - one requested ID can be narrowed to an explicit commit set without disturbing the mixed working branch;
  - frontmatter is sufficient to decide `pr_*` metadata or to leave it deliberately blank;
  - the resulting PR description structure is predictable and links back to the source log and issue.

### P0-C1-S5 (Default operating mode | v1)

- The default operator path is `inspect -> dry-run PR prep -> human confirm -> real PR create`; real creation should never be the silent default.
- `P0` does not require any branch mutation or network write; it only fixes the decision contract that later dry-run and real-run tooling must follow.

## P1 (Template and metadata updates | v1)

### P1-C1-S1 (PR metadata template contract | v1)

- Parent and phase log templates must expose `pr_labels`, `pr_projects`, `pr_milestone`, `pr_base`, and `pr_development_issue` with fail-closed comments that preserve blank-as-blank behavior.
- `pr_base` is the only template-level source for base branch selection in v1; if blank, later dry-run tooling may report a missing base but must not infer another branch name.
- Parent and phase templates should share the same `pr_*` semantics so a PR generator does not need different metadata precedence rules per log type.

### P1-C1-S2 (PR description scaffold contract | v1)

- Templates must expose one explicit input area for generated PR descriptions: short reviewer-facing summary bullets, checklist source guidance, and explicit links/evidence footer placeholders.
- Child phase logs are the default source for generated PR checklist blocks; parent/spine logs may only override that when they intentionally aggregate multiple child logs into one PR.
- The scaffold must stay concise enough that a generator can emit a predictable PR body without scraping arbitrary prose sections.

## P2 (Dry-run PR preparation | v1)

### P2-C1-S1 (ID-scoped selection planner | v1)

- Dry-run PR prep should accept an explicit manifest item containing at least `requested_id`, `source_log_path`, and a base branch boundary.
- The planner must inspect the branch-exclusive commit range and select only commits whose subjects start with the exact requested ID prefix.
- Every branch-exclusive commit in the inspected range should be reported as either `selected` or `skipped` so the operator can audit why each SHA was or was not included.

### P2-C1-S2 (Clean PR-prep branch validation | v1)

- Dry-run output must include the candidate clean PR-prep branch name, merge-base SHA, selected commit list, and generated PR body preview path.
- Validation succeeds when the selected commits form a coherent ID-scoped set without mutating any branch or creating any remote PR.
- Missing optional PR metadata such as `pr_milestone` or `pr_development_issue` should remain blank in the dry-run output rather than being guessed.

## PR Summary Inputs

**PR summary bullets**:

- Fix the PR automation contract around ID-scoped commit selection, metadata precedence, and development-link ownership.
- Roll final `pr_*` fail-closed semantics and PR body scaffold inputs into the parent and phase log templates.
- Validate that a future PR-prep generator can describe the `S0E-4A` scope without scraping arbitrary prose from the mixed working branch.

**PR checklist source**:

- Default source: reuse the checked items from this log's execution checklist so the PR body reflects the completed contract and template steps.
- No parent/spine override is needed for this sample because the selected scope is one direct phase log.

**PR links / evidence footer**:

- Log: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/293`
- Runbook: ``
- Evidence artifact: `docs/issues/pr-prep-S0E-4A-sample-plan.json`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-4A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S0E-4A` may use the active `S0E-*` branch for contract work, but dry-run PR prep should prove a separate clean PR-prep branch strategy before any real PR creation is attempted.

**Commit discipline (recommended)**:

- Fix the commit-selection contract first, then wire PR metadata fields into templates, then validate dry-run branch preparation, then attempt real PR creation.

## Plan (draft)

### P1 (Template and metadata updates)

- P1-C1-S1: finalise PR metadata fields in log templates
- P1-C1-S2: define PR description generation from child-log execution checklists

### P2 (Dry-run PR preparation)

- P2-C1-S1: implement ID-scoped commit selection from a mixed working branch
- P2-C1-S2: validate clean PR-prep branch generation without disturbing the main working branch

### P3 (Real PR automation)

- P3-C1-S1: create one real PR with labels, milestone, project, and development linkage
- P3-C1-S2: verify that human review and merge remain outside automation scope

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: commit selection strategy fixed
- [x] `P0-C1-S2`: PR metadata and description contract fixed
- [x] `P0-C1-S3`: development-link and review boundary fixed
- [x] `P0-C1-S4`: evidence contract fixed
- [x] `P0-C1-S5`: default operating mode fixed

### P1 (Template and metadata updates)

- [x] `P1-C1-S1`: PR metadata fields finalised in templates
- [x] `P1-C1-S2`: PR description structure fixed

### P2 (Dry-run PR preparation)

- [x] `P2-C1-S1`: ID-scoped commit selection implemented
- [x] `P2-C1-S2`: clean PR-prep branch generation validated

## Evidence

- `P0-C1-S1`: this log now fixes the clean PR-prep branch strategy as the only stable selection path for ID-scoped PRs from a mixed working branch.
- `P0-C1-S2`: this log now fixes the precedence rule that `pr_*` frontmatter fields are authoritative and blank fields must remain blank.
- `P0-C1-S2`: this log now fixes the expected PR body shape around summary, execution checklist, explicit links, and optional evidence footer.
- `P0-C1-S3`: this log now fixes that Development linkage can only come from explicit `pr_development_issue`, while review and merge stay human-owned.
- `P0-C1-S4` / `P0-C1-S5`: this log now fixes the proof boundary and the default `dry-run first` operating mode that later `P1-P3` tooling must preserve.
- `P1-C1-S1`: `docs/logs/_template-log-phase-drills-evidence.md` now carries final fail-closed comments for every `pr_*` metadata field.
- `P1-C1-S1`: `docs/logs/_template-log-parent-epic-spine.md` now mirrors the same `pr_*` semantics so parent/spine logs do not diverge from child phase logs.
- `P1-C1-S2`: both templates now expose `PR Summary Inputs` blocks that define summary bullets, checklist source rules, and links/evidence footer placeholders for future PR body generation.
- `P2-C1-S1`: `scripts/issues/plan_pr_prep.py` now provides a manifest-driven PR-prep dry-run planner that reports `selected` and `skipped` branch-exclusive commits by exact ID prefix.
- `P2-C1-S2`: `docs/issues/pr-prep-S0E-4A-sample-manifest.json` defines the sample dry-run input boundary for `S0E-4A`.
- `P2-C1-S2`: `docs/issues/pr-prep-S0E-4A-sample-plan.json` confirms that the dry-run selected `2` `S0E-4A` commits from the mixed working branch, used merge-base `4ffb71f697ae080fabd087e081eef5f504331764`, and planned candidate branch `pr-prep/s0e-4a` with no warnings.
- `P2-C1-S2`: `docs/issues/pr-prep-S0E-4A-sample-body.md` now previews the generated PR body using the log's summary bullets, checked execution checklist items, and evidence footer.

## Recent changes (for traceability, optional)

- 2026-03-29: opened `S0E-4A` to separate PR automation from issue automation and to define a stable ID-scoped PR workflow.
- 2026-03-29: completed `P0` by fixing commit-selection semantics, `pr_*` metadata precedence, PR description boundaries, Development linkage ownership, and the default dry-run-first operating mode.
- 2026-03-29: completed `P1` by writing final `pr_*` metadata rules and PR description scaffold inputs back into the parent and phase log templates.
- 2026-03-29: completed `P2` by adding a manifest-driven PR-prep dry-run planner, generating a sample commit-selection plan, and previewing the resulting PR body without mutating any branch.