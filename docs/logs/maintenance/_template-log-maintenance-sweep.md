# log-<family>-M<n> (<ops maintenance title>)

---

**id**: `<family>-M<n>`
**kind**: `log`
**title**: `<ops maintenance title>`
**status**: `stable`
**scope**: `<family>`
**links**: ``
  **parent_log**: `<parent log path>`
  **previous_log**: ``
  **runbook**: `<runbook or entrypoint path>`

---

## Trigger

- `<scheduled cadence / operator request / post-change verification / maintenance window>`

## Scope

- `<target system / environment / workflow / runner / backup / audit surface>`

## Environment Or Target

- `<environment, repo, runner group, VM, database, service, or operational scope>`

## Entry Point

- `<workflow dispatch / script / runbook / command>`

## Precheck

- `<health check, inventory check, dry-run, or prerequisite validation>`

## Action Performed

- `<what was actually run or maintained>`

## Postcheck

- `<post-run validation or verification>`

## Findings

- `<findings, drift, warnings, or none>`

## Evidence

- `<artifact paths, run URL, summary file, evidence bundle>`

## Follow-up

- `<none or explicit follow-up owner/log>`

## Report Summary

- Trigger: `<why this run happened now>`
- Result: `<pass/fail/partial>`
- Next action: `<none or next step>`

## Validation

- `<command, check, or manual verification>`

## Commit

- `<commit sha / subject>`
