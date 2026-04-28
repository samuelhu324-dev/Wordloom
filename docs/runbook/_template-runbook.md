# runbook-template-v3

Use this template when one workflow or operator lane has become stable enough to deserve one durable
current-reader runbook surface, but still needs explicit ledger binding for repeated execution,
release-scoped evidence intake, and later audit.
Keep the runbook thin: it owns the current operator meaning, the admitted scenario surface,
the release decision gate, and the run-ledger binding.
Do not replay full phase history inside the runbook; link back to logs, contracts, release ledgers,
and run ledgers instead.

---

```yaml
runbook_record:
  runbook_family: <RUNBOOK-FAMILY>
  runbook_release: <001>
  runbook_id: <run-RUNBOOK-FAMILY-001-summary>
  record_kind: code-first-runbook
  status: <draft|active|deprecated|superseded|retired>
  release_action: <initial|simple-revision|merge|split-parent|split-child|absorption|consolidation|historical-backfill>
  release_change_summary: <why this runbook release exists and what materially changed>
  summary: <effective operator meaning at this runbook state>
  governance_area: <workflow|ops-runtime|evidence-pipeline|other>
  applies_to: <what operator surface or family this runbook governs>
  operator_surface_summary: <what operators may currently rely on in this release>
  entry_surface: <workflow|script|task|dispatch|manual>
  evidence_surface: <summary.json|result.json|run-ledger|other>
  owner_team: <docs-governance|ops-runtime|delegated team>
  current_steward: <role:runbook-maintainer|delegated:runbook-maintainer|other>
  approval_state: <draft|review-pending|reviewed-awaiting-approval|approved|retired>
  reviewed_by: <role:workflow-reviewer|pending|unknown>
  approved_by: <role:docs-governance-approver|pending|unknown>
  release_ledger_binding:
    parent_release_ledger: <docs/runbook/support-only/ledger-runbook-RUNBOOK-FAMILY-001-summary.md>
    supplementary_ledger_series: <docs/runbook/support-only/ledger-runbook-SUP-001-RUNBOOK-FAMILY-001-summary.md>
    patch_ledger_series: <docs/runbook/support-only/ledger-runbook-PATCH-001-RUNBOOK-FAMILY-001-summary.md>
    intended_use: <release-scoped evidence intake and staged write-back before or alongside run-level accounting>
  ledger_binding:
    parent_run_ledger: <docs/runbook/support-only/ledger-run-001-RUNBOOK-FAMILY-001-summary.md>
    supplementary_ledger_series: <docs/runbook/support-only/ledger-run-SUP-001-RUNBOOK-FAMILY-001-summary.md>
    patch_ledger_series: <docs/runbook/support-only/ledger-run-PATCH-001-RUNBOOK-FAMILY-001-summary.md>
    minimum_evidence_files:
      - <summary.json>
      - <result.json>
    minimum_admitted_fields:
      - <result>
      - <failureClass>
  code_evidence_binding:
    required: <yes|no|conditional>
    stable_entry_refs:
      - <backend/scripts/... or workflow/task id>
    operator_surface_refs:
      - <worker path|workflow file|task label>
    switch_checkpoint_refs:
      - <switch or checkpoint surface ref>
    disable_boundary_refs:
      - <disabled state or stop-condition ref>
    scenario_registry_ref: <section or file that owns the scenario list>
    evidence_contract_ref: <section or file that owns evidence-bundle rules>
    non_ownership_refs:
      - <linked log, contract, or sibling runbook ref>
    minimum_supported_failure_classes:
      - <es_429|timeout|deterministic_exception>
    release_gate_required: <yes|no>
  recorded_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  effective_from: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>
  effective_until: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>
  introduced_by: <first decisive source anchor>
  last_changed_by: <most recent source anchor>
  source_refs:
    - <direct decisive source reference for this runbook release>
  cumulative_source_refs:
    - <all source refs carried forward into this runbook's current release state>
  supporting_evidence_refs:
    - <optional retained evidence>
  lineage:
    supersedes:
      - <optional earlier runbook id replaced by this release>
    superseded_by:
      - <optional later runbook id that replaces this release>
    split_from:
      - <optional broader earlier runbook id if this record is a split child>
    split_into:
      - <optional narrower later runbook ids if this record later splits>
    absorbed_from:
      - <optional earlier runbook id whose meaning is partly absorbed here>
    absorbed_into:
      - <optional later runbook id that absorbs meaning from this record>
    retires:
      - <optional earlier runbook id explicitly ended by this release>
    retired_by:
      - <optional later runbook id or decision that retires this record>
  notes:
    - <optional clarification>
```

---

## Naming Rule

- Name runbooks as `run-<RUNBOOK-FAMILY>-<RELEASE>-<summary>.md`.
- `<RUNBOOK-FAMILY>` should follow contract-like long-path grammar and remain stable across revisions.
- `<RELEASE>` is append-only inside one stable runbook family.
- A new release number is only one possible split outcome. If the semantic split is really a title split,
  sibling lane, or narrower family extraction, open the new file or folder shape that best matches reader meaning
  instead of forcing a numeric bump mechanically.
- Preferred example shape:
  - `run-WORKFLOW-FAMILY-001-operator-surface.md`

## Lifecycle Field Rule

- `recorded_at` records when this runbook release entered the repo as a defended operator surface.
- `reviewed_at` records when this runbook release passed defended review; use `pending` when the review has not happened yet.
- `effective_from` and `effective_until` describe the best currently known historical-effective range for this operator surface.
- `recorded_at`, `reviewed_at`, `effective_from`, and `effective_until` are required fields in every runbook record; when a defended value is not known yet, keep the field present and use `unknown`, `pending`, or `ongoing` rather than omitting it.
- New values should prefer canonical UTC second timestamps such as `2026-04-20T14:55:00Z`.
- Legacy day-only values may remain where finer audit precision is not defended.

## Governance State Rule

- `owner_team`, `current_steward`, `approval_state`, `reviewed_by`, and `approved_by` are the current-state governance fields for the runbook surface itself.
- Keep these fields on the runbook when the runbook is expected to survive as a maintained operator surface rather than only as a retained historical note.
- Run-ledger `submitted by` / `evidence owner` / `verified by` fields remain execution-accounting surfaces; they do not replace the runbook's current governance state.

## Release Ledger Binding Rule

- Use `release_ledger_binding` when one runbook release needs its own durable reader-first intake surface for staged evidence admission, scenario write-back, boundary notes, or later release-scoped supplements and patches.
- `release_ledger_binding` does not replace `ledger_binding`:
  - `release_ledger_binding` is for the runbook release object itself;
  - `ledger_binding` remains for repeatable run execution accounting under that runbook.
- Prefer `release_ledger_binding` when evidence is extracted from source logs, code, labs, or weak-structure channels before it can honestly be admitted into the runbook body.
- Prefer `ledger_binding` when the evidence belongs to one concrete admitted run such as `RUN-001`.
- When both layers exist, later run-level ledgers may cite the runbook release ledger, but should not replace it as the write-back surface for runbook-release meaning.
- The release ledger is the first default intake surface for code-first runbooks. Add a dedicated extra support ledger only if the release ledger cannot keep operator-surface extraction, scenario routing, and write-back decisions separated cleanly.

## Code Evidence Binding Rule

- Use `code_evidence_binding` whenever one runbook depends on stable code or workflow entrypoints, bounded switches, admitted drill scenarios, or explicit evidence contracts rather than on prose-only operator guidance.
- `stable_entry_refs` identify the exact executable entrypoints the runbook claims to govern.
- `operator_surface_refs` identify the broader executable surface, for example a worker shim, workflow file, or task.
- `switch_checkpoint_refs` list bounded operator-facing switches, checkpoints, or recovery branches that the runbook may name without implying that every adjacent procedure is already defended.
- `disable_boundary_refs` list the exact state boundaries that stop or narrow the runbook's positive operator claims.
- `scenario_registry_ref` points to the table or file that enumerates admitted drills or failure classes for this runbook.
- `evidence_contract_ref` points to the section or file that owns required evidence-bundle rules.
- `non_ownership_refs` point to nearby logs, contracts, or sibling runbooks that still own meaning not admitted here.
- `release_gate_required=yes` means the runbook body should include an explicit release-decision table rather than inferring split decisions from prose.
- When a runbook opens `Current Operator Faces`, `Code Evidence Attachments`, `Scenario Registry`, `Operator Chronology`, or `Release Decision Table`, all time-window and event-time columns defined by the template are required; `unknown`, `pending`, and `ongoing` are valid values, omission is not.

## Current Governance State

- Add this section when the runbook is a live operator surface rather than only a retained historical stub.
- Preferred table shape:

| governed surface | owner team | current steward | approval state | reviewed by | approved by | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `<runbook id>` | `<owner_team>` | `<current_steward>` | `<approval_state>` | `<reviewed_by>` | `<approved_by>` | `<bounded current-state note>` |

## 1) Purpose

- State the operator goal in one paragraph or 2 to 4 bullets.
- Answer what this runbook helps someone run, verify, recover, inspect, or conclude.

## 2) Scope

- State what is covered.
- State what is explicitly out of scope.
- Link 3 to 7 deeper sources that still own history or contract detail.

## 3) Current Operator Faces

- Use this section to describe the runbook's current operator meaning through stable faces rather than one mixed bridge-plus-coverage stack.
- The runbook should open only faces it is willing to defend as current reader meaning.
- Preferred face kinds:
  - `stable-entrypoint`
  - `switch-checkpoint-surface`
  - `disable-state-boundary`
  - `proof-path-recipe`
  - `evidence-contract`
  - `admitted-scenario-surface`
  - `non-ownership-boundary`

| face id | face kind | current operator meaning | code evidence refs | admitted scenario ids | source release row id | current standing | recorded at | effective from | effective until | effective status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `OF-01` | `<stable-entrypoint>` | `<what operators may currently rely on here>` | `<CEA-01; CEA-03>` | `<SC-01; none>` | `<RBL-01|unknown>` | `<defended-now|narrowed-now|not-owned-here>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<in-force|no-longer-in-force|pending-review>` | `<bounded face note>` |

## 4) Code Evidence Attachments

- Use this section to attach executable anchors, evidence hooks, and bounded switch surfaces without automatically turning each code fact into a positive operator promise.
- This table is current-reader-only: it records what evidence supports the current runbook now, not every historical implementation detail.

| evidence id | evidence kind | stable ref | supported face ids | operator meaning supported here | source release row id | source scenario row ids | current standing | recorded at | effective from | effective until | effective status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CEA-01` | `<workflow|worker|task|script|metric|log-field|trace-hook>` | `<path or entry id>` | `<OF-01; OF-03>` | `<what this evidence supports without widening meaning>` | `<RBL-01|unknown>` | `<RBL-02-SC-01|none>` | `<defended-now|code-anchor-only|pending-writeback>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<in-force|no-longer-in-force|pending-review>` | `<bounded evidence note>` |

## 5) Scenario Registry

- Use this section when the runbook governs multiple admitted failure classes, drill scenarios, or execution branches.
- A runbook should not imply full operator coverage only through narrative paragraphs; list the admitted scenarios explicitly.

| scenario id | failure class | default system behavior | operator action class | prod relevance | cadence class | evidence minimum | current owned meaning | source release row id | source scenario row ids | recorded at | effective from | effective until | effective status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SC-01` | `<es_429|timeout|duplicate_delivery>` | `<retry|terminal-failed|draining>` | `<observe-only|manual-replay|fallback-switch|defer>` | `<periodic-drill|pre-change-drill|incident-only|lab-only>` | `<weekly|per-release|before-risky-change|after-incident|none>` | `<_result.json|metrics|logs|trace export>` | `<defended-now|partial-code-support|gap-owned|not-owned-here>` | `<RBL-01|unknown>` | `<RBL-02-SC-01|none>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>` | `<in-force|no-longer-in-force|pending-review>` | `<bounded scenario note>` |

- When `current owned meaning` is not `defended-now`, the runbook should link the owning gap packet, contract note, or deferred owner explicitly.

## 6) Operator Chronology

- Use this section to record how current operator faces and admitted scenarios became what they are now.
- Keep chronology append-only and event-shaped. Do not duplicate every code-evidence row here.

| chronology id | affected surface ids | change action | actor value | source release row id | source scenario row ids | effective at | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `OC-01` | `<OF-01; SC-01>` | `<introduced|amended|narrowed|rerouted|retired|history-backfilled>` | `<role:packet-reviewer|unknown>` | `<RBL-01|unknown>` | `<RBL-02-SC-01|none>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>` | `<source refs>` | `<bounded chronology note>` |

## 7) Release Decision Table

- Use this section whenever the runbook needs to distinguish same-release write-back from new release, sibling lane, or deeper family split.
- Numbering is only one release outlet. If the semantic change is better expressed as a new title, narrower family, or sibling file/folder, record that outlet explicitly instead of assuming `002`.

| decision id | affected surface ids | current release semantic | candidate semantic | delta class | reader visible change | release action | target release or outlet | decision basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RD-01` | `<OF-01; SC-01>` | `<what this release currently promises>` | `<candidate changed meaning>` | `<evidence-only|clarification-only|semantic-change|boundary-restructure>` | `<yes|no>` | `<same-release-evidence-writeback|new-release-required|split-family-required|move-to-sibling-lane|retain-in-chronology-only>` | `<run-...-002-*|new title/file/folder|sibling lane|same release>` | `<why this is or is not a new release>` | `<bounded decision note>` |

## 8) Run Ledger Binding

### 8.1 Parent ledger

- Name the canonical run ledger file for this runbook family.
- All ledger-class files should live under `docs/runbook/support-only/`.
- State whether each execution appends one new run row or opens a new ledger file.

### 8.2 Run and evidence ids

- Name the stable run-row shape as `RUN-<nnn>` or another defended family-specific format.
- Name the stable evidence-item shape as `E<nn>` or another defended format attached to one run row.
- Name attachment ids explicitly when screenshots, exports, or transcript files need approval-facing review.

### 8.3 Admission and write-back rule

- State the minimum evidence files required before a run may be admitted into the parent run ledger.
- State when a later evidence packet should open a SUP ledger instead of rewriting the original run row directly.
- State when a bounded repair packet should open a `PATCH` ledger instead of using a general SUP ledger.
- State where downstream write-back should land: parent ledger, SUP ledger, source log `Evidence`, maintenance log, or another explicit surface.

## 9) Evidence Bundle

### 9.1 Output roots

- List the snapshot, artifact, ledger, or workflow output roots.
- Call out the minimum evidence files that must exist, for example `_result.json`, `_recipe.json`, `_logs/`, `_metrics/`.

### 9.2 Admitted fields

- List the minimum fields the ledger will extract from those evidence files.
- Keep this section short and machine-facing.

## 10) Local or One-click Operation

### 10.1 Prerequisites

- List the minimum runtime, infra, env vars, permissions, and services.

### 10.2 Commands

- Show the default local or one-click command path.
- Prefer one canonical command sequence over many alternatives.
- If there is a Windows-specific example, keep it aligned with repo usage.

## 11) Troubleshooting

- List the 3 to 6 highest-value failure modes.
- For each one, point to the first evidence file, ledger row, or command to inspect.
- Prefer stable symptoms and actions over long explanations.

## 12) Notes and Boundaries

- State what this runbook deliberately does not try to be.
- State when the operator should drop into linked logs, ledgers, labs, or contracts.
- Record the next likely expansion point only if it changes operator expectations.

## Boundary Note

- Distinguish three cases explicitly when the runbook is code-coupled:
  - `defended operator procedure`: the runbook may instruct operators to use it now.
  - `code anchor only`: code exposes a switch or path, but operator procedure is not yet defended.
  - `gap-owned semantics`: the runbook must route the reader elsewhere instead of inventing missing procedure.

## Thinness Rules

- Keep one top-level runbook per stable operator family by default.
- Do not turn the runbook into a second source of truth for execution history.
- Do not copy full phase timelines, raw evidence histories, or recurring run rows into the runbook body.
- Put repeated execution accounting in the parent run ledger and later evidence refinement in SUP ledgers.
- If a child phase only supplies contract or implementation detail, link it instead of promoting it to its own runbook.# Runbook template (v1)

Use this template only when a top-level scope already has a stable operator workflow.
Keep the runbook thin: purpose, scope, evidence roots, one-click or local entry,
troubleshooting, and boundaries. Link out to logs, labs, ADRs, and workflows instead
of copying full phase history into the runbook.

---

**id**: `SxY-summary`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/SxY-summary`
**status**: `draft`          # draft | stable | archived
**scope**: `SxY`
**decision_date**: `YYYY-MM-DD`
**context_issue**:
  **DoD**: ``
  **Labs**: ``
**decision**: `State the operator-facing decision in one sentence.`
  **positive**: `"Repeatable operator entry", "Machine-verifiable evidence", "Stable troubleshooting path"`
  **negative**: `"Extra maintenance for commands and evidence paths", "Need to keep contracts stable"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- State the operator goal in one paragraph or 2 to 4 bullets.
- Answer: what this runbook helps someone run, verify, recover, or inspect.

## 2) Scope

- State what is covered.
- State what is explicitly out of scope.
- Link the 3 to 7 source materials that still hold the deeper history or contracts.

## 3) Evidence Bundle

### 3.1 Output roots

- List the snapshot, artifact, ledger, or workflow output roots.
- Call out the minimum evidence files that must exist, for example `_result.json`, `_recipe.json`, `_logs/`, `_metrics/`.

### 3.2 Summary or ledger

- If the workflow appends to a summary ledger, document the file and the minimum fields.
- If there is no ledger, say where the operator should look instead.

## 4) One-click Automation

Include this section only if there is already a stable one-click entry such as a workflow,
task, wrapper script, or dispatch button.

### 4.1 What it does

- Explain the high-level flow in 3 to 6 bullets.

### 4.2 Operator instructions

- Show the stable entrypoint.
- List the inputs or knobs that an operator is allowed to change.
- State what success and failure look like.

## 5) Local Operation

### 5.1 Prerequisites

- List the minimum runtime, infra, env vars, and services.

### 5.2 Commands

- Show the default local command path.
- Prefer one canonical command sequence over many alternatives.
- If there is a Windows-specific example, keep it aligned with repo usage.

## 6) Troubleshooting

- List the 3 to 6 highest-value failure modes.
- For each one, point to the first evidence file or command to inspect.
- Prefer stable symptoms and actions over long explanations.

## 7) Notes and Boundaries

- State what this runbook deliberately does not try to be.
- State when the operator should drop into linked logs, labs, or ADRs.
- Record the next likely expansion point only if it changes operator expectations.

## Thinness rules

- Keep one top-level runbook per scope by default.
- Do not turn the runbook into a second source of truth.
- Do not copy full phase timelines, taxonomy tables, or raw evidence histories.
- If a child phase only supplies contract or implementation detail, link it instead of promoting it to its own runbook.