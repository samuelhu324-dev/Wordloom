# Run-S0F-2A: maintenance lanes and direct patch ledger

---

**id**: `S0F-2A-maintenance-lanes-and-direct-patch-ledger`
**kind**: `runbook`
**title**: `run/S0F-2A-maintenance-lanes-and-direct-patch-ledger`
**status**: `stable`
**scope**: `S0F-2A`
**decision_date**: `2026-04-05`
**context_issue**:
  **DoD**: ``
  **Labs**: ``
**decision**: `Provide one thin policy surface for deciding when work should remain a standard slice, when it should be grouped into one maintenance sweep log, and when a tiny direct patch commit is allowed without a dedicated slice log.`
  **positive**: `"Clear lane selection", "Less fake slice naming", "Small-fix traceability without forcing every patch into the full lifecycle"`
  **negative**: `"Adds one more procedural surface", "Requires discipline not to hide real contract work in maintenance bundles", "Direct patch lane still needs manual judgment"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Give operators one stable answer when work is too small, too mixed, or too incidental for the full slice lifecycle.
- Preserve the existing log-driven system as the default path instead of replacing it.
- Keep tiny fixes traceable without inventing fake issue titles or bloated child logs.

## 2) The Three Lanes

### 2.1 Standard slice lane

- Use this lane when the change has its own contract, success criteria, replay path, or retained evidence surface.
- Typical signals:
  - the change introduces or fixes a named boundary
  - the change needs a real DoD paragraph
  - the change may later need full-auto issue or PR lifecycle treatment
  - the change will likely be referenced by later slices
- Surface:
  - one normal phase log such as `S0F-1J`
  - optional runbook, artifacts, issue, PR, and full lifecycle evidence as needed

### 2.2 Maintenance sweep lane

- Use this lane when several small fixes belong together because they came from the same replay, cleanup pass, or operator session, but none of them deserves its own full slice.
- Typical signals:
  - the changes are same-source fallout from one run or one repair pass
  - each fix is small, but together they need one why/what/not-in-scope explanation
  - reviewer context matters more than individual mini-DoDs
- Surface:
  - one lightweight maintenance log named `family-M<n>-<slug>`
  - one commit or one short burst of commits tied to that same bounded bundle

### 2.3 Direct patch lane

- Use this lane only for tiny, local, obvious fixes that do not deserve even a maintenance log.
- Typical signals:
  - typo or wording correction
  - path fix or small script flag fix
  - ledger write-back or tiny metadata correction
  - no new contract, no retained evidence, no multi-step reasoning
- Surface:
  - a direct commit without a dedicated slice log
  - one row appended to `docs/logs/ledger-direct-patch-commits.md`

## 3) Escalation Rule

- Start in the smallest lane that is honest.
- Escalate from direct patch to maintenance log as soon as one of these becomes true:
  - the fix set needs a short narrative explaining why these items belong together
  - the fix spans multiple unrelated directories or ownership areas
  - the change is no longer obviously local and low-risk
  - reviewer context cannot be reconstructed from the diff alone
- Escalate from maintenance log to full slice as soon as one of these becomes true:
  - the work introduces or repairs a real repo contract
  - the work adds a new automation or operator surface
  - the work needs retained evidence to prove correctness
  - the work may reasonably need live issue or PR lifecycle treatment later

## 4) Naming Rules

### 4.1 Maintenance log naming

- Format:

```text
docs/logs/log-<family>-M<n>-<slug>.md
```

- Examples:
  - `docs/logs/log-S0F-M1-post-lifecycle-fallout-cleanup.md`
  - `docs/logs/log-S4D-M2-runner-script-hygiene-sweep.md`

- Rules:
  - `M` means maintenance sweep, not a new formal slice lineage
  - `<family>` should point to the owning spine or family, not to every touched child
  - `<slug>` should describe why the changes were grouped, not list every file

### 4.2 Direct patch commit subject

- Preferred subject shapes:

```text
patch(<area>): <summary>
hygiene(<area>): <summary>
ledger(<area>): <summary>
```

- Examples:
  - `patch(docs): fix broken runbook path`
  - `hygiene(scripts): remove stale temp output reference`
  - `ledger(logs): write back missing PR URL`

- Do not use an `S*` slice ID in a direct patch commit unless the work actually belongs to an existing live slice and is already accounted for there.

## 5) Direct Patch Boundary

- Allowed:
  - tiny local corrections
  - low-risk naming or path fixes
  - obvious metadata or ledger write-backs
  - mechanical cleanup that does not alter system semantics
- Not allowed:
  - new contracts
  - new operator or automation surfaces
  - behavior changes that need explanation beyond one or two sentences
  - grouped mixed fixes discovered by a broader replay
  - anything that would look suspicious if reviewed without extra prose

## 6) Shared Ledger

- All direct patch commits should append one short row to `docs/logs/ledger-direct-patch-commits.md`.
- Minimum row fields:
  - date
  - commit
  - area
  - why now
  - validation
  - follow-up needed or `none`

## 7) Minimal Maintenance Template

- Use this only for maintenance sweeps, not for full slice logs.

```md
# log-<family>-M<n> (<short title>)

---

**id**: `<family>-M<n>`
**kind**: `log`
**title**: `<short title>`
**status**: `stable`
**scope**: `<family>`
**links**:
  **parent_log**: `<parent log path>`

---

## Why This Bundle Exists

- These fixes were grouped because `<same replay / same cleanup pass / same operator session>`.

## Included

- `<small fix 1>`
- `<small fix 2>`
- `<small fix 3>`

## Not Included

- `<anything intentionally left out or escalated elsewhere>`

## Validation

- `<command, check, or manual verification>`

## Commit

- `<commit sha / subject>`
```

## 8) First-Response Guidance

- If you can explain the work honestly in one direct diff sentence, use the direct patch lane.
- If you need one short paragraph to explain why several small fixes belong together, use a maintenance log.
- If the work would later deserve a link from another slice, open a real slice now instead of hiding it in maintenance.

## 9) Source Materials

- `docs/logs/log-S0F-2A-maintenance-lanes-and-direct-patch-ledger.md`
- `docs/logs/log-S0F-docs-management-v6.md`
- `docs/logs/ledger-direct-patch-commits.md`
