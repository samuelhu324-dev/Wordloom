# governance-contract-record: GC-PRA-0001

- `record_id`: `GC-PRA-0001`
- `contract_id`: `PR-CREATION-ID-SCOPED-COMMIT-SELECTION`
- `title`: `PR creation uses exact ID-scoped commit selection and explicit metadata precedence`

```yaml
contract_record:
  contract_id: PR-CREATION-ID-SCOPED-COMMIT-SELECTION
  status: active
  summary: PR creation must prepare a clean PR-prep branch from the target base, select only exact ID-scoped commits, and apply PR metadata only from explicit frontmatter or the bounded development-issue fallback path.
  governance_area: pr-creation-governance
  applies_to: PR preparation and creation flows that derive one PR from one exact source-log or issue ID while the operator may still work on a mixed branch
  enforcement_surface: PR prep planners, create-time preflight, and the bounded guarded PR-create path that preserves explicit stage boundaries before publication
  violation_semantics: fail
  introduced_by: S0E-4A/P0-C1-S1
  last_changed_by: S0F-3F/P4-C1-S1
  source_refs:
    - docs/logs/log-S0E-4A-github-pr-automation-contract.md
    - docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md
    - docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md
  supersedes: []
  superseded_by: []
  notes:
    - S0E-5C refines the create-time boundary by showing that lifecycle pre-gate reuse is partial and does not authorize the whole PR-create flow as one opaque mutation.
    - Reviewed again in S0F-3E/P6-C2 and retained as one concentrated current contract because exact commit scoping, metadata precedence, and create-time stage ownership still read as one coherent PR-create boundary.
    - S0F-3F/P4 adds S0F-1A as the fail-closed PR-create front-half clarification without widening this record into a second parallel create contract.
```

## Reader Notes

- Current active meaning:
  - PR creation must select commits by exact ID scope.
  - PR metadata remains blank when blank in frontmatter except for the bounded development-issue fallback from the same source log.
  - The create path stays stage-aware rather than collapsing branch prep and live publication into one implicit step.

## Traceability

- Stable contract owner:
  - `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
- Current fail-closed boundary clarification:
  - `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
- Current boundary clarification:
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`