# runbook-template-WORKFLOW-GITHUB-ISSUES-v1

Use this template for the canonical `WORKFLOW-GITHUB-ISSUES` family only.
This family-specific runbook is the authority once the generic skeleton is no longer enough to express chronology-first ledger binding, strong-structure ids, and dual-surface `SUP` / `PATCH` follow-up.

---

```yaml
runbook_record:
  runbook_family: <WORKFLOW-GITHUB-ISSUES>
  runbook_release: <001>
  runbook_id: <run-WORKFLOW-GITHUB-ISSUES-001-summary>
  record_kind: ledger-aware-runbook
  status: <draft|active|deprecated|superseded|retired>
  release_action: <initial|simple-revision|identity-and-structure-rewrite|historical-backfill>
  release_change_summary: <why this release exists>
  summary: <effective operator meaning>
  governance_area: workflow
  applies_to: <GitHub Issues lifecycle automation surface>
  entry_surface: <script|task|manual>
  evidence_surface: run-ledger
  ledger_binding:
    parent_run_ledger: <docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-summary.md>
    supplementary_ledger_series: <docs/runbook/support-only/ledger-run-SUP-001-WORKFLOW-GITHUB-ISSUES-001-summary.md>
    patch_ledger_series: <docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-summary.md>
    minimum_evidence_files:
      - <docs/issues/*.json>
      - <docs/issues/*plan.json>
      - <docs/issues/*apply-result.json>
    minimum_admitted_fields:
      - <run_row_id>
      - <target_row_id>
      - <target_stage_row_id>
      - <stage_name>
      - <stage_status>
      - <blocking_reason_class>
  template_authority:
    family_runbook_template: docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md
    family_parent_ledger_template: docs/runbook/support-only/_template-run-ledger-WORKFLOW-GITHUB-ISSUES.md
    family_supplement_template: docs/runbook/support-only/_template-run-ledger-SUP-WORKFLOW-GITHUB-ISSUES.md
    family_patch_template: docs/runbook/support-only/_template-run-ledger-PATCH-WORKFLOW-GITHUB-ISSUES.md
  recorded_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  effective_from: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>
  effective_until: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>
  introduced_by: <first decisive source anchor>
  last_changed_by: <most recent decisive source anchor>
  source_refs:
    - <decisive source reference>
  cumulative_source_refs:
    - <carried source reference>
  notes:
    - <optional clarification>
```

---

## Naming Rule

- Name runbooks as `run-<RUNBOOK-FAMILY>-<RELEASE>-<summary>.md`.
- For this family, `RUNBOOK-FAMILY` is fixed to `WORKFLOW-GITHUB-ISSUES`.

## Workflow Profiles

- `child-issue-full-lifecycle`
  - `CREATION`
  - `PR_PENDING`
  - `PR_MERGED`
  - `CONCLUSION`
- `parent-issue-light-lifecycle`
  - `CREATION`
  - `CONCLUSION`

## Family-specific Binding Rules

- The canonical parent ledger is chronology-first and must expose:
  - `Current Run Status Summary`
  - `Execution Round Table`
  - `Current Target Status Table`
  - `Target Stage Attempt Table`
- Stable structural ids remain:
  - `RUN-001`
  - `RUN-001-T01`
  - `RUN-001-T01-STG-CREATION`
  - optional attempt id `RUN-001-T01-STG-CREATION-A01`
- Later evidence refinement belongs in `SUP`.
- Bounded repair packets belong in `PATCH`.

## Thinness Rules

- Keep the runbook as operator contract and ledger binding only.
- Do not duplicate chronology tables from the parent ledger inside the runbook body.
- Point future `WORKFLOW-GITHUB-ISSUES` packets to this family-specific quartet rather than the generic skeletons.