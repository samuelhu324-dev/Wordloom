# Run-S0E: log to issue creation（validated sample -> manual creation -> future script entry）

---

**id**: `S0E-log-to-issue-creation`
**kind**: `runbook`
**title**: `run/S0E-log-to-issue-creation`
**status**: `draft`
**scope**: `S0E`
**decision_date**: `2026-03-28`
**context_issue**:
  **DoD**: `S0E-2A/P3-C1-S1S2`
  **Labs**: `S0E-2A, S4E-5B sample, S6A-4A sample`
**decision**: `Provide one thin operator procedure for turning a validated issue scaffold into a real GitHub issue, while fixing the future script input/output contract without mixing creation-side automation into the contract phase.`
  **positive**: `"Repeatable manual issue creation path", "Stable handoff from log/sample to issue", "Future scripting can target one contract instead of reverse-engineering markdown"`
  **negative**: `"Still requires human review for summary quality and module labels", "Does not yet create GitHub issues automatically"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Give operators one thin, repeatable path from validated `log -> issue scaffold` samples to real GitHub issues.
- Fix the exact boundary between what must be reviewed manually now and what a future script may generate later.
- Prevent the contract phase from silently turning into creation-side automation before the input/output shape is stable.

## 2) Scope

- Covered:
  - how to select a validated sample artifact
  - how to review title, labels, milestone, and body before creating the real issue
  - how to treat blank fields conservatively
  - the minimum future script input/output contract
- Out of scope:
  - direct GitHub API or CLI automation
  - automatic label creation
  - automatic module-impact inference
- Primary source materials:
  - `docs/logs/log-S0E-2A-semi-automated-git-issue-creation.md`
  - `docs/issues/issue-S0E-2A-semi-automated-git-issue-creation.md`
  - `docs/issues/issue-S4E-5B-execution-layer-enforcement-and-controlled-exceptions.md`
  - `docs/issues/issue-S6A-4A-hard-gate-evidence-json.md`

## 3) Evidence Bundle

### 3.1 Output roots

- Validated sample issue artifacts live under:
  - `docs/issues/issue-S0E-2A-semi-automated-git-issue-creation.md`
  - `docs/issues/issue-S4E-5B-execution-layer-enforcement-and-controlled-exceptions.md`
  - `docs/issues/issue-S6A-4A-hard-gate-evidence-json.md`
- Minimum operator evidence for manual creation:
  - source log path
  - final issue title
  - final labels set
  - final body markdown
  - created issue URL or number once the real issue exists

### 3.2 Summary or ledger

- During `S0E-2A`, the phase log remains the main ledger for validation evidence.
- Once a real issue is created, the created issue URL should be written back to the source log `links.issue` field in a later tracked update.

## 4) One-click Automation

- Real create-side automation now lives in `S0E-2B`, but it is still explicit opt-in rather than one-click-by-default.
- The stable safety rule remains: draft generation is the default path, and real GitHub issue creation only happens under explicit `--create`.

## 5) Local Operation

### 5.1 Prerequisites

- The target log already exists and is stable enough to become an issue.
- At least one validated sample issue artifact exists for the same pattern or neighboring pattern.
- Required GitHub labels already exist in the repository.
- The operator knows whether a parent issue already exists.
- Python is available for the local `draft-generation` script path.

### 5.2 Draft-generation command

- Canonical local entry:
  - `python scripts/issues/gen_issue_draft.py <log_path>`
- Example:
  - `python scripts/issues/gen_issue_draft.py docs/logs/log-S0E-2B-real-github-issue-creation-automation.md`
- Outputs:
  - markdown draft under `docs/issues/issue-<log-slug>.md`
  - structured JSON sidecar under `docs/issues/issue-<log-slug>.json`
  - stdout JSON summary for quick inspection

### 5.3 Create-issue command

- Explicit create entry:
  - `python scripts/issues/gen_issue_draft.py <log_path> --create --repo <owner/repo>`
- Current prerequisites:
  - `gh` CLI installed
  - `gh auth status` succeeds
  - all derived labels already exist in the target repo
  - if a milestone is provided, it already exists in the target repo
  - no existing issue already uses the same title
- Create-side outputs:
  - updated JSON sidecar with `issue_number`, `issue_url`, `created_at`, and `mode=create-issue`
  - no automatic write-back to the source log

### 5.4 Batch dry-run planning command

- `S0E-2C` adds a batch planning entry that stays in dry-run mode by default.
- Canonical local entry:
  - `python scripts/issues/plan_issue_batch.py <manifest_path>`
- Example:
  - `python scripts/issues/plan_issue_batch.py docs/issues/issue-batch-S0E-2C-sample-manifest.json`
- Outputs:
  - per-log markdown drafts and JSON sidecars for selected logs
  - one batch plan artifact under `docs/issues/issue-batch-<manifest-stem>-plan.json`
  - stdout JSON summary with `planned_items`, `warnings`, and per-item `planned_action`
- Safety rules:
  - batch planning does not call GitHub create APIs
  - if a source log already has `links.issue`, the planner must mark it as `skip-existing-issue`
  - parent-child linking, milestone apply, and write-back remain later explicit phases, not part of `P1`

### 5.5 Relationship dry-run planning command

- `S0E-2C/P2-C1-S2` adds a relationship planner that reads only an explicit relationship manifest and never writes GitHub state.
- Canonical local entry:
  - `python scripts/issues/plan_issue_relationships.py <manifest_path>`
- Example:
  - `python scripts/issues/plan_issue_relationships.py docs/issues/issue-relationship-S0E-2C-sample-manifest.json`
- Outputs:
  - one relationship plan artifact under `docs/issues/issue-relationship-<manifest-stem>-plan.json`
  - stdout JSON summary with `planned_items`, top-level `warnings`, and per-item `planned_action`, `status`, and `warnings`
- Dry-run semantics:
  - `planned` means both sides are explicitly identified and any optional traceability fields agree with them
  - `skipped` means the item was explicitly marked skip in the manifest
  - `error` means one side is missing or invalid as an explicit issue reference
  - `reconciliation` means explicit issue references conflict with optional traceability fields and must be resolved manually before apply mode exists

### 5.6 Manual issue-creation procedure

- Step 1: choose the source log and, when possible, start from the nearest validated sample issue artifact.
- Step 2: confirm the issue title uses `SxY-ZA: <fixed-keyword>/<specific subject>`.
- Step 3: confirm the fixed keyword is from the controlled vocabulary and is not being replaced by ad-hoc wording.
- Step 4: confirm labels in this order:
  - top-level label, for example `EVOLUTION`
  - scope label, for example `s4/ops` or `s6/evidence & drills`
  - sub label, for example `sub/1`
  - function label such as `drills` only when the source log explicitly supports it
  - module labels only when the source log explicitly proves them
- Step 5: if milestone or module labels are blank in the sample, keep them blank unless a human can justify them from the source log.
- Step 6: review `Context` and `Definition of Done (DoD)` for human readability; preserve the contract structure but improve wording only when it does not change scope.
- Step 7: create the real GitHub issue through the normal repository UI path.
- Step 8: after creation, record the issue URL back into the source log in a later tracked docs update.

## 6) Future Script Entry Contract

### 6.1 Minimum inputs

- Required:
  - `log_path`: absolute or repo-relative path to one source log
- Optional:
  - `output_path`: where to write a markdown issue draft; default should be `docs/issues/issue-<log-slug>.md`
  - `parent_issue`: explicit override when the parent issue already exists
  - `milestone_override`: explicit override when milestone must be set manually
  - `module_labels_override`: explicit override for human-confirmed module labels
  - `strict_label_check`: when true, fail if a requested label is not in the allowed label set

### 6.2 Minimum outputs

- Required output object:
  - `title`: final issue title string
  - `top_labels`: array of top-level labels
  - `scope_labels`: array of scope and sub labels
  - `function_labels`: array of optional functional labels such as `drills`
  - `module_labels`: array of confirmed module labels
  - `milestone`: string or `null`
  - `parent_issue`: string or `null`
  - `body_markdown`: markdown body with `Context`, `Definition of Done (DoD)`, and `Links`
  - `warnings`: array of conservative fallback warnings, for example `issue_milestone missing`, `module labels left blank`
- Optional output files:
  - markdown issue draft under `docs/issues/`
  - JSON sidecar for machine use in a later `S0E-2B` phase

### 6.3 Failure contract

- The future script must fail closed, not fail open.
- If the fixed keyword cannot be chosen conservatively from the contract, the script should stop and emit a warning instead of guessing.
- If a label is not pre-created, the script should emit a warning or fail under `strict_label_check`; it must not create labels.
- If milestone is absent, output `null` and continue.
- If module impact is not explicit, output an empty module-label array and continue.
- Real GitHub issue creation must remain a separate opt-in mode, not the default behavior of the draft-generation mode.

### 6.4 Batch manifest and plan contract

- `S0E-2C/P0` fixes one conservative batch manifest shape:
  - `version`: manifest schema version
  - `selection_filters`: optional filter block for `include_globs`, `exclude_globs`, and future skip/apply toggles
  - `defaults`: shared defaults such as `strict_label_check`, `parent_issue`, or `milestone_override`
  - `items`: explicit per-log entries; each item must include `log_path` and may override defaults
- Minimal planner item fields:
  - `log_path`
  - optional `output_path`
  - optional `result_path`
  - optional `parent_issue`
  - optional `milestone_override`
  - optional `module_label_overrides`
- Batch plan output contract:
  - top-level fields: `mode`, `manifest_path`, `selection_input`, `operation`, `total_items`, `planned_items`, `warnings`, `result`
  - per-item fields: `source_log`, `draft_path`, `result_path`, `issue_number`, `issue_url`, `planned_action`, `applied_action`, `status`, `title`, `warnings`
- `planned_action` is conservative:
  - `create-issue` when the source log does not yet have `links.issue`
  - `skip-existing-issue` when the source log already has `links.issue`
- Batch planning may generate fresh draft artifacts, but it must not create issues, attach parent-child relationships, apply milestones, or write back into source logs.

### 6.5 Relationship input contract

- `S0E-2C/P2-C1-S1` fixes one conservative relationship manifest shape:
  - `version`: manifest schema version
  - `mode`: default `relationship-dry-run`
  - `defaults`: optional shared defaults such as `relationship_type`
  - `items`: explicit relationship items only
- Each relationship item must identify both sides explicitly. Accepted issue references are:
  - `parent_issue_number` or `parent_issue_url`
  - `child_issue_number` or `child_issue_url`
- Optional traceability-only fields may be included, but they do not replace explicit issue references:
  - `parent_log_path`
  - `child_log_path`
  - `reason`
- Accepted relationship types for v1 should stay narrow:
  - `child-of`
  - `parent-of`
- Forbidden inference rules:
  - no title-based matching
  - no body-text similarity matching
  - no automatic resolution from `log_path` alone when an explicit issue reference is absent
- Conflict handling:
  - if either side is missing an explicit issue reference, the item must remain in dry-run/error state
  - if a provided issue reference conflicts with the traceability fields, the tool must stop at reconciliation rather than overwrite GitHub state
- Sample contract file:
  - `docs/issues/issue-relationship-S0E-2C-sample-manifest.json`
- Relationship dry-run output contract:
  - top-level fields: `mode`, `manifest_path`, `selection_input`, `operation`, `total_items`, `planned_items`, `warnings`, `result`
  - per-item fields: `relationship_type`, `parent_issue_number`, `parent_issue_url`, `child_issue_number`, `child_issue_url`, `parent_log_path`, `child_log_path`, `planned_action`, `applied_action`, `status`, `warnings`, `reason`
- Current planned-action vocabulary:
  - `link-child-to-parent`
  - `link-parent-to-child`
  - `skip-relationship`
  - `error-missing-reference`
  - `error-self-reference`
  - `reconcile-relationship-input`

## 7) Troubleshooting

- Keyword feels ambiguous:
  - inspect the source log `Decision / Outcome` and compare with the validated neighbor sample before choosing a different keyword.
- Label set feels too aggressive:
  - remove module labels first; keep top-level, scope, and sub labels stable.
- Milestone is unclear:
  - leave it blank and record a warning rather than inferring from nearby logs.
- Body sounds too vague:
  - refine `Context` and `DoD`, but do not rewrite the scope beyond what the source log proves.

## 8) Notes and Boundaries

- This runbook is intentionally thin; the log remains the source of truth for naming policy and evidence.
- `S0E-2A` fixes the contract and manual creation path.
- If real GitHub issue creation is pursued, the recommended follow-up slice is `S0E-2B`, not a late expansion of `S0E-2A`.
- If batch issue planning, parent-child linking, or milestone/backfill tooling is pursued, the next follow-up slice is `S0E-2C`.
