# REMED Admission Package v1

## Purpose

- This view explains why the `A1` lane under `S0F-3F` admits one new current remediation-governance area and one current record instead of keeping `S0F-1C` as a support-only log.
- It exists so readers can distinguish the newly admitted current remediation-stage contract from broader workflow taxonomy and from family-specific guarded apply wrappers.

## Area Choice

- Chosen area code:
  - `REMED`
- Chosen current record:
  - `GC-REMED-0001`
- Chosen contract id:
  - `GUARDED-BATCH-MULTI-ITEM-REMEDIATION-STAGES`
- Why `REMED` was reused instead of inventing a narrower new code:
  - the current surface already spans preview planning, guarded apply delegation, and preserve-existing post-verify across more than one mutation family
  - the admitted surface is narrower than the broader `publish-verify-remediation` taxonomy, but broader than any single issue-conclusion, relationship, or PR-body apply wrapper
  - `REMED` was already the defended shortlist name in `S0F-3C`, and `A1` confirms that the name is still precise enough once the contract boundary is compressed explicitly

## Current Boundary

- `GC-REMED-0001` owns:
  - preview-first planning as the only allowed entry into multi-item remediation
  - family-owned guarded apply as the only allowed live mutation path
  - split-before-mutation when one remediation plan spans more than one live-mutation family
  - mandatory preserve-existing post-verify before a remediation batch is complete
- `GC-REMED-0001` does not own:
  - the broader publish-verify-remediation taxonomy or future gate naming from `S0E-7D`
  - one family-specific continuation exception such as targeted relationship-only continuation under `S0E-5B`
  - runtime packaging or retained artifact layout by itself

## Executed Admission Writes

- Add `REMED` to the front-door glossary and controlled area-code dictionary in `INDEX.md`
- Add one current front-door row for `GC-REMED-0001`
- Create the current record file `GC-REMED-0001-guarded-batch-multi-item-remediation-stages.md`
- Update the `S0F-1` family sweep surfaces so `A1` reads as executed instead of blocked

## Reader Notes

- This view is an admission explanation surface, not the current registry itself.
- `INDEX.md` remains the front door for current-state reading.
- `GC-REMED-0001` is the current contract body.
- `S0F-1C` remains the primary semantic source log behind this admitted current record.

## Source Refs

- `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
- `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
- `docs/logs/log-S0F-3C-governance-contract-series-audit-and-admission.md`
- `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`