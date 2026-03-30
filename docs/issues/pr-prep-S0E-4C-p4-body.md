## Metadata

- Requested ID: `S0E-4C`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0e-4c`
- Source log: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #300

## Summary

- Normalize PR `Development issue` rendering to short refs such as `#297` and keep `Development Link` consistent with the same normalized target.
- Make PR summary bullets mandatory for real PR creation so live PRs no longer ship with `<placeholder>` in `Summary`.
- Add a real issue-relationship attach path so child issue sidebar `Relationships` matches the existing `Metadata -> Parent issue` contract.

## Execution Checklist

- [x] `P0-C1-S1`: PR development-issue short-ref rendering fixed in contract
- [x] `P0-C1-S2`: PR summary requiredness fixed in contract
- [x] `P0-C1-S3`: issue parent relationship attach boundary fixed in contract
- [x] `P0-C1-S4`: evidence contract fixed
- [x] `P1-C1-S1`: PR preview/create development-issue rendering normalized
- [x] `P1-C1-S2`: real PR create path blocks placeholder summaries
- [x] `P1-C1-S3`: issue relationship apply tooling added
- [x] `P2-C1-S1`: representative PR-prep artifacts regenerated and reviewed
- [x] `P2-C1-S2`: representative issue relationship artifacts regenerated and reviewed
- [x] `P3-C1-S1`: one real PR validated against the updated body contract
- [x] `P3-C1-S3`: historical `S0E` PR audit completed and outdated live bodies remediated

## Links

- Log: `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
- Issue: `https://github.com/samuelhu324-dev/wordloom-v3/issues/300`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`
- Evidence artifact: `docs/issues/pr-prep-S0E-4C-p4-plan.json`
- Generated PR body should keep `Summary`, `Evidence Footer`, and `Development Link` as separate sections.
- `Summary` must not degrade to `<placeholder>` on a live PR create path.

## Evidence Footer

- `18fbfe40` / `S0E-4C` / `P0-P1`: normalize PR summary gate and relationship apply
- `cc72eb91` / `S0E-4C` / `P2-P3`: regenerate artifacts and reconcile legacy PRs
- `7468d552` / `S0E-4C` / `P4-C1-S1`: create live issue and attach parent
- `db1f26e3` / `S0E-4C` / `P4-C1-S1`: add live PR prep artifacts

## Development Link

- Closes #300
