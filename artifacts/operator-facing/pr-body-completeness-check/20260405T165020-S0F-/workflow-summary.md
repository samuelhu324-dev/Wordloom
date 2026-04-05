## PR Body Completeness Standard Check

- Mode: `standard read-only check`
- Role: `primary local boundary`
- Trigger surface: `local-operator-facing`
- Requested ID prefixes: `S0F-`
- Result: `pass`
- Total logs reviewed: `9`
- Exact-match IDs: `S0F-1A, S0F-1B, S0F-1C, S0F-1D, S0F-1E, S0F-1F, S0F-1G`
- Formatting-only IDs: ``
- Substantive drift IDs: ``
- Stop IDs: ``
- Skip IDs: `S0F-1H, S0F-1I`
- Review result artifact: `artifacts/operator-facing/pr-body-completeness-check/20260405T165020-S0F-/review-result.json`
- Wrapper result artifact: `artifacts/operator-facing/pr-body-completeness-check/20260405T165020-S0F-/wrapper-result.json`

This wrapper is the standard local read-only check entrypoint for PR body completeness. It delegates all classification to the canonical reviewer and fails only when substantive drift or stop-state ownership gaps remain.
