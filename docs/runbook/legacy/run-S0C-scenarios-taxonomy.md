# Run-S0C: scenarios taxonomy（scenario_id 查找 + catalog-driven suite 操作）

---

**id**: `S0C-scenarios-taxonomy`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/S0C-scenarios-taxonomy`
**status**: `stable`          # draft | stable | archived
**scope**: `S0C`
**decision_date**: `2026-02-23`
**context_issue**:
  **DoD**: `#83, #66`
  **Labs**: ``
**decision**: `Use the scenario catalog as the single operator entry for suite discovery and scenario_id selection, with a small helper for local lookup and optional suite triggering.`
  **positive**: `"Less workflow churn", "Catalog is auditable", "Operators can discover scenario ids quickly"`
  **negative**: `"GitHub UI loses dropdown options", "Need to keep helper and catalog references aligned"`
**supersedes**: `docs/runbook/run-S0C-docs-management-v3.md`
**superseded_by**: `null`

---

## 1) Purpose

- Give operators one thin entry for finding the right `scenario_id` before running GitHub Actions suites.
- Keep the single source of truth in `docs/labs/scenarios/catalog.yml` instead of scattered workflow options.
- Provide one default local lookup tool and one optional suite-trigger helper.

## 2) Scope

- Covered:
  - scenario catalog lookup and naming
  - local discovery via `list_scenarios.py`
  - optional GitHub Actions triggering and evidence backfill
- Out of scope:
  - per-scenario runtime semantics
  - suite implementation details already owned by the S0C logs and workflows
- Primary source materials:
  - `docs/logs/log-S0C-4A-scenarios-taxonomy.md`
  - `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
  - `docs/labs/scenarios/catalog.yml`

## 3) Evidence Bundle

### 3.1 Output roots

- Source of truth catalog:
  - `docs/labs/scenarios/catalog.yml`
- Operator helper scripts:
  - `backend/scripts/ci/list_scenarios.py`
  - `backend/scripts/ci/trigger_drill_suites_and_log.py`

### 3.2 Summary or ledger

- If suite runs are triggered and logged back automatically, the operator-facing evidence lands in:
  - `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
- If only local lookup is used, the catalog itself is the operator reference point.

## 4) One-click Automation

### 4.1 What it does

- Lists or filters canonical `scenario_id` values from the catalog.
- Optionally triggers suite workflows through `gh`.
- Optionally backfills run URLs and conclusions into the S0C evidence log.

### 4.2 Operator instructions

- Discover ids locally:
  - `python backend/scripts/ci/list_scenarios.py`
  - `python backend/scripts/ci/list_scenarios.py --intent verify`
  - `python backend/scripts/ci/list_scenarios.py --grep paging`
- Optionally trigger suites and backfill evidence:
  - `python backend/scripts/ci/trigger_drill_suites_and_log.py --dry-run`
  - `python backend/scripts/ci/trigger_drill_suites_and_log.py`
  - `python backend/scripts/ci/trigger_drill_suites_and_log.py --refresh-conclusions --wait-seconds 900`

## 5) Local Operation

### 5.1 Prerequisites

- Python 3
- `PyYAML` installed for `list_scenarios.py`
- `gh` installed and authenticated if using suite triggering

### 5.2 Commands

- Install dependency:
  - `python -m pip install PyYAML`
- Fallback grep when helper install is not available:
  - `rg "^\s*id:\s*" docs/labs/scenarios/catalog.yml`
  - `rg "^\s*id:\s*verify/" docs/labs/scenarios/catalog.yml`
  - `rg "shadow_verify_search_index" docs/labs/scenarios/catalog.yml`

## 6) Validated Decision Paths

### 6.1 Happy path

- Catalog lookup succeeds with a real operator query:
  - `python backend/scripts/ci/list_scenarios.py --intent verify`
- Guardrail baseline succeeds on the current repo catalog:
  - `python backend/scripts/ci/validate_scenario_catalog.py`
- Validated outcome:
  - `entry found`: verify scenarios and their aliases are listed directly from the catalog
  - `evidence found`: the catalog plus helper output are enough to pick the canonical `scenario_id`
  - `next action clear`: proceed with the canonical id or trigger the suite helper

### 6.2 Known failure

- Deterministic failure reproduction was validated against the real validator logic by cloning the catalog to a temporary file and reusing an existing alias `shadow_verify_search_index_write_gate` under a second scenario.
- The validator returns:
  - `duplicate aliases across catalog: ['shadow_verify_search_index_write_gate']`
- Validated outcome:
  - `failure classified`: this is a catalog uniqueness failure, not a workflow runtime failure
  - `next action clear`: fix the conflicting alias in `docs/labs/scenarios/catalog.yml`, then rerun `python backend/scripts/ci/validate_scenario_catalog.py` before touching workflow YAML

### 6.3 Ambiguity / legacy alias lookup

- Legacy or fuzzy lookup was validated with:
  - `python backend/scripts/ci/list_scenarios.py --grep shadow_verify_search_index_write_gate`
- The helper resolves that legacy alias back to canonical `verify/search/write_gate_idempotency`.
- Validated outcome:
  - `entry found`: operators can start from an old alias and still land on the current catalog entry
  - `next action clear`: use the canonical `scenario_id` in workflow dispatch or docs updates, and keep aliases only as migration bridges

## 7) Troubleshooting

- `PyYAML` missing:
  - install it first, or use the `rg` fallback directly on `docs/labs/scenarios/catalog.yml`
- canonical id versus alias confusion:
  - check `scenarios[].id` and `scenarios[].aliases[]` in the catalog before editing workflows
- suite trigger script cannot talk to GitHub:
  - verify `gh auth status` and confirm the target branch/ref is correct

## 8) Notes and Boundaries

- This runbook is a thin operator entry, not the full taxonomy history.
- Workflow decomposition, guardrails, and migration notes remain in the S0C logs.
- The previous filename `run-S0C-docs-management-v3.md` is superseded so the runbook suffix now matches the parent log name `scenarios-taxonomy`.