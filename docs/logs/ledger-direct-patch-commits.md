# Direct Patch Commit Ledger

Use this ledger only for tiny direct patch commits that do not have a dedicated slice log, family patch note under `docs/logs/patch/`, or ops-maintenance log under `docs/logs/maintenance/`.

If a change still belongs to one family such as `S0F`, prefer `docs/logs/patch/_template-log-patch-note.md` and a family-bound patch ID such as `S0F-P1`.

If the work is recurring or operator-facing maintenance, prefer `docs/logs/maintenance/_template-log-maintenance-sweep.md` and reserve this ledger for the truly no-log path only.

| Date | Commit | Area | Why now | Validation | Follow-up |
| --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | `<sha>` | `<area>` | `<one sentence>` | `<command or manual check>` | `<none or follow-up log>` |

