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