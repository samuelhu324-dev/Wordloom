# Run-S0F-2B: family patch and ops maintenance model

---

**id**: `S0F-2B-family-patch-and-ops-maintenance-model`
**kind**: `runbook`
**title**: `run/S0F-2B-family-patch-and-ops-maintenance-model`
**status**: `stable`
**scope**: `S0F-2B`
**decision_date**: `2026-04-05`
**context_issue**:
  **DoD**: ``
  **Labs**: ``
**decision**: `Refine the earlier small-work policy into three sharper lanes: family patch, ops maintenance, and tiny direct patch, and reserve the GitHub MAINTENANCE label for true ops-maintenance work only.`
  **positive**: `"Sharper ownership", "More realistic maintenance reporting", "Less confusion between repair work and operational care work"`
  **negative**: `"One more policy distinction to remember", "Ops maintenance template is intentionally heavier", "MAINTENANCE stays intentionally narrow"`
**supersedes**: `docs/runbook/run-S0F-2A-maintenance-lanes-and-direct-patch-ledger.md`
**superseded_by**: `null`

---

## 1) Purpose

- Distinguish family-owned repair work from true ops-maintenance work.
- Keep tiny direct patches available without letting them swallow broader repair bundles.
- Define when the already-live GitHub `MAINTENANCE` top-level label should be used and when it should stay unused.

## 2) The Refined Lanes

### 2.1 Family patch

- Use this lane when the change is still owned by one family or slice lineage.
- Typical examples:
  - `S0F` policy fallout fix
  - `S4D` runner readme correction
  - `S5B` audit wording or helper-script patch
- Surface:
  - one short patch log under `docs/logs/patch/`
  - family-bound patch ID shape such as `S0F-P1-<slug>`
- This lane is not maintenance. It is repair or follow-up work that still belongs to a family.

### 2.2 Ops maintenance

- Use this lane when the work is recurring, operator-triggered, or environment-scoped care work.
- Typical examples:
  - CI/CD workflow health checks
  - runner upkeep
  - backup/restore verification
  - credential or certificate rotation
  - environment smoke checks
  - audit/export/reporting cycles
- Surface:
  - one heavier maintenance log under `docs/logs/maintenance/`
  - explicit trigger, environment, entrypoint, precheck, postcheck, findings, evidence, and follow-up sections
- This is the only lane that should normally use the GitHub `MAINTENANCE` top-level label.

### 2.3 Tiny direct patch

- Use this lane only for truly local, obvious, no-log fixes.
- Surface:
  - direct commit
  - one row in `docs/logs/ledger-direct-patch-commits.md`
- If the change needs even a short note, move up to family patch.

## 3) Lane Selection Rule

- Ask first: does this belong to an existing family or slice? If yes, prefer family patch.
- Ask second: is this recurring or operator maintenance with environment and report expectations? If yes, use ops maintenance.
- Only if both answers are no, and the change is tiny and obvious, use the direct patch ledger path.

## 4) Template Paths

- Family patch template:
  - `docs/logs/patch/_template-log-patch-note.md`
- Ops maintenance template:
  - `docs/logs/maintenance/_template-log-maintenance-sweep.md`
- Tiny direct patch ledger:
  - `docs/logs/ledger-direct-patch-commits.md`

## 5) GitHub `MAINTENANCE` Label Rule

- Current live state:
  - the GitHub label `MAINTENANCE` already exists in `samuelhu324-dev/wordloom-v3`
- Admission rule:
  - use `MAINTENANCE` only for true ops-maintenance issues
  - do not use it for family patch logs or ordinary evolution follow-ups
- A log or issue should normally qualify for `MAINTENANCE` only when all of these are true:
  - it has a clear operator or scheduled trigger
  - it names an environment or operational target
  - it has a concrete entrypoint such as a script, runbook, or workflow dispatch
  - it expects precheck and postcheck structure
  - it produces evidence and a reportable result
- If those are missing, default back to `EVOLUTION` or another existing family-appropriate top label.

## 6) Reporting Shape For Ops Maintenance

- A good ops-maintenance report should answer at least these fields:
  - trigger
  - cadence or reason now
  - environment or target
  - entrypoint used
  - precheck result
  - action performed
  - postcheck result
  - findings
  - evidence path
  - follow-up owner

## 7) First-Response Guidance

- If the work reads as `fixing S0F fallout`, it is family patch.
- If the work reads as `running or verifying an operator maintenance procedure`, it is ops maintenance.
- If the work reads as `one local obvious correction`, it is tiny direct patch.

## 8) Source Materials

- `docs/logs/log-S0F-2B-family-patch-and-ops-maintenance-model.md`
- `docs/logs/patch/_template-log-patch-note.md`
- `docs/logs/maintenance/_template-log-maintenance-sweep.md`
- `docs/logs/ledger-direct-patch-commits.md`
