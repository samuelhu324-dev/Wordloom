# S6A-4A: evidence/fault suite hard-gate and evidence JSON

## Metadata

- Title: `S6A-4A: evidence/fault suite hard-gate and evidence JSON`
- Labels: `EVOLUTION`, `s6/evidence & drills`, `sub/1`, `drills`
- Milestone: ``
- Source log: `docs/logs/log-S6A-4A-hard-gate-evidence-json.md`
- Parent issue: ``

## Context

- Productize fault-suite CI checks into hard gates whose PASS/FAIL outcome is machine-decidable.
- Fix a stable evidence contract around `snapshot_dir/_result.json` so failures can be understood from artifacts without screenshots or log hunting.
- Keep artifacts minimal and self-explaining: enough to reconstruct what failed, what was expected, and which run parameters mattered.
- Preserve a single fact source for CI gate decisions rather than introducing a second summary standard.

## Definition of Done (DoD)

- The hard-gate PASS/FAIL semantics are explicit and tied to `verify` exit status plus `_result.json.ok`.
- The minimum evidence JSON schema is explicit.
- The minimum artifacts contract is explicit.
- The issue wording preserves that CI gate evidence must remain machine-decidable and self-explaining.
- This sample confirms that `evidence` is the correct fixed keyword for `S6A-4A`, while `drills` stays a label-level functional suggestion rather than replacing the title keyword.
- The sample confirms that `s6/evidence & drills` and `drills` can coexist without collapsing scope labeling and function labeling into one field.

## Links

- Log: `docs/logs/log-S6A-4A-hard-gate-evidence-json.md`
- Runbook: `docs/runbook/run-S6A-evidence-drills-spine.md`
- Parent log: `docs/logs/log-S6A-evidence-drills-spine.md`
- Previous log: `docs/logs/log-S6A-3A-failure-taxonomy-hard-interface.md`
- Reference log 1: `docs/logs/log-S0C-3A-2A-artifacts-contract-packing.md`
- Reference log 2: `docs/logs/log-S0C-4A-1A-catalog-driven-suites-&-guardrails.md`
- Reference log 3: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
