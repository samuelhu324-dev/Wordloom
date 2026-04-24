# patch-log-template-legacy-v1

Use this template only for historical or compatibility patch notes that are still log-first.
New runbook-bound patch packets should use `docs/runbook/support-only/_template-run-ledger-PATCH.md` instead.

## Bridge Rule

- If the patch belongs to one stable runbook family and should remain inside the same runbook release, open a support-only patch ledger:
  - `docs/runbook/support-only/ledger-run-PATCH-<sequence>-<RUNBOOK-FAMILY>-<RUNBOOK-RELEASE>-<summary>.md`
- A log-first patch note may still exist as origin narrative, but the canonical ownership, approval, timing, verification, and downstream write-back surface should live in the support-only patch ledger.
- If the patch materially changes operator semantics, do not use this legacy note shape; open a new source log and a new runbook release instead.

## Legacy Shape

# log-<family>-P<n>-<slug> (<short title>)

---

**id**: `<family>-P<n>`
**kind**: `log`
**title**: `<short title>`
**status**: `stable`
**scope**: `<family>`
**links**: ``
  **parent_log**: `<parent log path>`
  **origin_log**: `<origin slice or family log path>`

---

## Why This Family Patch Exists

- `<one short family-owned reason>`

## Patch Boundary

- This patch still belongs to `<family>` and does not justify a separate full slice.
- It is not an ops-maintenance run and should not use the GitHub `MAINTENANCE` top-level label.

## Change

- `<small local fix>`

## Current Evidence

- `<current failing run, diff, log, or other evidence>`

## Next Step

- `<immediate next action for this patch lane>`

## Validation

- `<command, check, or manual verification>`

## Commit

- `<commit sha / subject>`

## Naming

- Recommended file path:
  - `docs/logs/patch/log-<family>-P<n>-<slug>.md`
- Recommended patch ID examples:
  - `S0F-P1`
  - `S4D-P2`
  - `S5B-P3`