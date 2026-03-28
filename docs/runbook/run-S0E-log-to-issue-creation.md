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

- No one-click creation entry exists yet.
- That work is intentionally deferred to a follow-up slice, recommended as `S0E-2B`, after the `S0E-2A` contract and manual procedure are stable.

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

### 5.3 Manual issue-creation procedure

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
