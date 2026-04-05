## Metadata

- Requested ID: `S0F-1B`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0f-1b`
- Source log: `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #366

## Summary

- Replace deterministic issue Context template assembly with LLM-authored Context generation grounded in the corresponding source log.
- Tighten the Context shape contract to exact sentence counts: four for child issues and five for top-level parent issues.
- Remove silent template fallback from the canonical issue-conclusion Context generation path so invalid output fails closed instead of reverting to old stock phrasing.
- Keep create-time issue Context structurally present but empty while the first LLM rollout is limited to issue conclusion authoring.
- Remove the retired deterministic Context template builders from the shared contract surface so the canonical paths cannot drift back toward template assembly.
- Retain representative historical rewrite artifacts and prove that the guarded conclusion path can replace legacy deterministic Context blocks on already-closed issues without reopening them.

## Execution Checklist

- [x] `P0-C1-S1`: exact child-versus-parent sentence-count contract fixed
- [x] `P0-C1-S2`: deterministic style requirements removed from the canonical Context contract
- [x] `P1-C1-S1`: issue-conclusion Context generation switched to an LLM-authored path
- [x] `P1-C1-S2`: one representative conclusion sample retained without template fallback
- [x] `P2-C1-S1`: silent template fallback removed from the canonical conclusion path
- [x] `P3-C1-S1`: draft preview create-time Context remains empty by default and draft-side one-item generation is retired
- [x] `P4-C1-S1`: retired deterministic Context builder surface removed and v1 contract marked stable
- [x] `P5-C1-S1`: single-item LLM normalization now tolerates one-item multi-sentence array compression
- [x] `P5-C1-S2`: representative historical S6B preview artifacts retained under `S0F-1B`
- [x] `P5-C1-S3`: closed issues `#357/#358/#359` rewritten through the guarded conclusion remediation path
- [x] `P5-C1-S4`: dotted-path false positives removed from the Context gate and post-refresh verification retained

## Links

- Log: `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
- Runbook: ``
- Evidence artifact: `docs/issues/issue-conclusion-S0F-1B-p5-live-summary.json`

Closes #366
