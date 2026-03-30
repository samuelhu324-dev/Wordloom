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
- Extend that same path so a merged PR can later drive a final issue-conclusion write-back instead of leaving closed issues on the create-time empty scaffold.
- Fix the exact boundary between what must be reviewed manually now and what a future script may generate later.
- Prevent the contract phase from silently turning into creation-side automation before the input/output shape is stable.

## 2) Scope

- Covered:
  - how to select a validated sample artifact
  - how to review title, labels, milestone, and body before creating the real issue
  - how to conclude an already-closed or newly merged issue from exact-ID merged PR evidence
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

### 5.6 Milestone/write-back dry-run planning command

- `S0E-2C/P3` adds a backfill planner for milestone reconciliation and source-log issue-URL write-back planning.
- Canonical local entry:
  - `python scripts/issues/plan_issue_backfill.py <manifest_path>`
- Example:
  - `python scripts/issues/plan_issue_backfill.py docs/issues/issue-backfill-S0E-2C-sample-manifest.json`
- Outputs:
  - one backfill plan artifact under `docs/issues/issue-backfill-<manifest-stem>-plan.json`
  - stdout JSON summary with per-item `planned_action`, `status`, `warnings`, `current_milestone`, and `source_log_issue_url`
- Dry-run semantics:
  - `planned` means the issue and source log are explicit, and the next step is a clear no-conflict action such as `apply-milestone` or `write-back-issue-url`
  - `skipped` means there is no requested change, or the requested state already matches current state
  - `error` means a required explicit input is missing, such as the issue reference or the source log path required for write-back
  - `reconciliation` means the issue's current milestone or the source log's current issue URL conflicts with the desired input and must be resolved before any apply mode exists

### 5.7 Manual issue-creation procedure

- Step 1: choose the source log and, when possible, start from the nearest validated sample issue artifact.
- Step 2: confirm the issue title uses `SxY-ZA: <fixed-keyword>/<specific subject>`.
- Step 3: confirm the fixed keyword is from the controlled vocabulary and is not being replaced by ad-hoc wording.
- Step 4: confirm labels in this order:
  - top-level label, for example `EVOLUTION`
  - scope label, for example `s4/ops` or `s6/evidence & drills`
  - sub label, for example `sub/1`
  - function label such as `drills` only when the source log explicitly supports it
  - module labels only when the source log explicitly proves them
- Step 5: resolve milestone in this order: explicit `issue_milestone` first, then exact `roadmap_path + roadmap_milestone + roadmap_phase` bridge metadata, else leave it blank.
- Step 6: resolve parent issue in this order: explicit `issue_parent`, then the parent log's `links.issue` when the source log declares `parent_log`; if neither exists, leave the child issue blank and warn instead of guessing.
- Step 7: if the source log is a top-level spine with no `parent_log`, omit the `Parent issue` row entirely.
- Step 8: when `Parent issue` is present, render it as plain text short GitHub issue reference such as `#248`, not a full URL and not a code span.
- Step 9: confirm `issue_projects`; if they are blank, keep them blank or use the existing `docs/logs/* -> wordloom Board` default rather than guessing from prose.
- Step 10: keep the generated issue body English-only, start directly from `## Metadata`, and do not repeat the issue title inside the body.
- Step 11: leave `Context` plus `Definition of Done (DoD)` intentionally blank unless a human is ready to supply explicit final text.
- Step 12: create the real GitHub issue through the normal repository UI path.
- Step 13: after creation, record the issue URL back into the source log in a later tracked docs update.

### 5.8 Manual issue-conclusion procedure

- Step 1: confirm the target issue already exists and the relevant delivery PR is actually merged; open, draft, or merely approved PRs are not enough.
- Step 2: treat GitHub auto-close as state evidence only. A closed issue may still need a final body write-back if it still shows the create-time empty scaffold.
- Step 3: collect candidate PRs by exact ID prefix from merged PR titles, for example `S0E-2D/` for issue `S0E-2D`; do not expand the set by prose similarity.
- Step 4: if multiple merged PRs match, order them by parsed `P*` then `C*`/`S*` units when available; otherwise order them by `mergedAt` ascending and then PR number ascending.
- Step 5: preserve the existing `Metadata` block from issue creation.
- Step 6: write a final `Development` section that lists the merged PR evidence in the chosen order.
- Step 7: write `Definition of Done (DoD)` as the same ordered merged-PR ledger, not as a replay of the original contract bullets.
- Step 8: update `Links` so they include deterministic issue/log references plus one PR link line per merged PR in the same order.
- Step 9: if the issue is already closed, edit it in place rather than treating the closed state as a blocker.
- Step 10: if the issue is still open after merge, write the final body first and then close the issue with `reason=completed`.

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
  - `issue_projects`: array of explicit or default project names
  - `body_markdown`: markdown body that starts at `Metadata`, keeps `Context` and `Definition of Done (DoD)` structurally present but blank by default, and includes deterministic `Links`
  - `warnings`: array of conservative fallback warnings, for example `issue_milestone missing`, `module labels left blank`
- Optional output files:
  - markdown issue draft under `docs/issues/`
  - JSON sidecar for machine use in a later `S0E-2B` phase

### 6.3 Failure contract

- The future script must fail closed, not fail open.
- If the fixed keyword cannot be chosen conservatively from the contract, the script should stop and emit a warning instead of guessing.
- If a label is not pre-created, the script should emit a warning or fail under `strict_label_check`; it must not create labels.
- If milestone is absent, output `null` and continue.
- If roadmap bridge metadata is complete and `issue_milestone` is blank, milestone may be derived from that exact bridge and reported explicitly in warnings.
- If `parent_log` exists and its `links.issue` is populated, child issue drafts may derive `issue_parent` from that exact link and report the derivation explicitly in warnings.
- If the source log has no `parent_log`, the issue is treated as a top-level issue for creation-body purposes and must omit the `Parent issue` row entirely.
- If a parent issue is rendered, it must appear only in `Metadata` and use a plain-text short GitHub reference such as `#248`.
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

### 6.6 Milestone and write-back reconciliation contract

- `S0E-2C/P3-C1-S1` fixes one conservative backfill manifest shape:
  - `version`: manifest schema version
  - `mode`: default `backfill-dry-run`
  - `defaults`: optional shared defaults such as `repo`, `desired_milestone`, and `write_back_issue_url`
  - `items`: explicit backfill items only
- Each backfill item must identify the target issue explicitly via:
  - `issue_number` or `issue_url`
- Optional fields:
  - `source_log_path`
  - `desired_milestone`
  - `write_back_issue_url`
  - `reason`
- Required behavior:
  - if `desired_milestone` is blank, milestone stays unmanaged and the planner must not infer one
  - if `desired_milestone` is provided but the issue already has a different non-empty milestone, the item must enter `reconciliation`
  - if `write_back_issue_url=true` and `source_log_path` is missing, the item must enter `error`
  - if `write_back_issue_url=true` and the source log already contains a different issue URL, the item must enter `reconciliation`
- Backfill dry-run output contract:
  - top-level fields: `mode`, `manifest_path`, `selection_input`, `operation`, `total_items`, `planned_items`, `warnings`, `result`
  - per-item fields: `issue_number`, `issue_url`, `source_log_path`, `source_log_issue_url`, `desired_milestone`, `current_milestone`, `write_back_issue_url`, `planned_action`, `applied_action`, `status`, `warnings`, `reason`
- Current planned-action vocabulary:
  - `apply-milestone`
  - `write-back-issue-url`
  - `apply-milestone+write-back-issue-url`
  - `skip-no-change`
  - `error-missing-issue-reference`
  - `error-missing-source-log`
  - `error-missing-milestone`
  - `reconcile-backfill-input`
  - `reconcile-milestone-or-writeback`
- Sample contract file:
  - `docs/issues/issue-backfill-S0E-2C-sample-manifest.json`

### 6.7 Issue-conclusion planning contract

- `S0E-2E/P0-P1` fixes one conservative post-merge conclusion boundary before any planner or write-back mode exists.
- Canonical local entry:
  - `c:/python314/python.exe scripts/issues/plan_issue_conclusion.py <manifest_path>`
- Example:
  - `c:/python314/python.exe scripts/issues/plan_issue_conclusion.py docs/issues/issue-conclusion-S0E-2E-sample-manifest.json`
- Minimum future inputs:
  - `source_log_path`
  - `issue_number` or `issue_url`
  - `requested_id`
- Optional future inputs:
  - `merged_pr_overrides`
  - `body_output_path`
  - `allow_closed_issue_edit`
- Required future planner outputs:
  - ordered `merged_prs` entries with `number`, `title`, `url`, and `merged_at`
  - `body_markdown` that preserves `Metadata` and renders final `Development`, `Definition of Done (DoD)`, and `Links`
  - `warnings` describing any explicit override or fallback ordering path
- Current dry-run artifacts:
  - `docs/issues/issue-conclusion-S0E-2E-sample-plan.json`
  - `docs/issues/issue-conclusion-S0E-2E-sample-s0e-4a-body.md`
  - `docs/issues/issue-conclusion-S0E-2E-sample-s0e-4b-body.md`
  - `docs/issues/issue-conclusion-S0E-2E-sample-s0e-2d-body.md`
- Failure contract:
  - if no merged PR can be proven for the exact requested ID, planning must stop instead of guessing
  - if candidate PRs are open or draft, planning must stop instead of treating them as final delivery evidence
  - if the issue is already closed but still has the create-time empty scaffold, planner output may still proceed because closed-state write-back is valid in v1

### 6.8 Issue-conclusion apply contract

- Canonical local entry:
  - `c:/python314/python.exe scripts/issues/apply_issue_conclusion_from_plan.py <plan_path> --item-index <n>`
- Example:
  - `c:/python314/python.exe scripts/issues/apply_issue_conclusion_from_plan.py docs/issues/issue-conclusion-S0E-2E-sample-plan.json --item-index 2`
- Current real-run artifacts:
  - `docs/issues/issue-conclusion-S0E-2E-sample-s0e-2d-apply-body.md`
  - `docs/issues/issue-conclusion-S0E-2E-sample-s0e-2d-apply-result.json`
- Apply semantics:
  - use the existing dry-run preview as the body source of truth
  - update the live issue body first
  - if the target issue is still open, close it with `reason=completed` after the body update
  - if the target issue is already closed, leave it closed and only update the body in place

## 7) Troubleshooting

- Keyword feels ambiguous:
  - inspect the source log `Decision / Outcome` and compare with the validated neighbor sample before choosing a different keyword.
- Label set feels too aggressive:
  - remove module labels first; keep top-level, scope, and sub labels stable.
- Milestone is unclear:
  - leave it blank and record a warning rather than inferring from nearby logs.
- Body sounds too vague:
  - refine `Context` and `DoD`, but do not rewrite the scope beyond what the source log proves.
- Issue already closed but still blank inside:
  - treat the close event as delivery evidence only and update the closed issue body in place with the final conclusion sections.

## 8) Notes and Boundaries

- This runbook is intentionally thin; the log remains the source of truth for naming policy and evidence.
- `S0E-2A` fixes the contract and manual creation path.
- If real GitHub issue creation is pursued, the recommended follow-up slice is `S0E-2B`, not a late expansion of `S0E-2A`.
- If batch issue planning, parent-child linking, or milestone/backfill tooling is pursued, the next follow-up slice is `S0E-2C`.
- If post-merge issue conclusion or merged-PR write-back is pursued, the next follow-up slice is `S0E-2E`.
