# UI Evidence Lite

This directory defines the lightweight evidence track for frontend fixes.

Use this track when a frontend problem is worth recording but does not belong in the repository's heavier backend evidence flow.

## Goal

Capture enough proof to:

- explain what was broken,
- show what changed,
- verify the affected workflow still works,
- preserve interview and demo-ready evidence,
- avoid forcing every UI fix through logs, drills, and hard gates.

## Two-track rule

Keep the existing heavy track for backend and system-evolution work:

- contracts,
- drills,
- hard gates,
- evidence artifacts,
- CI summaries.

Use this lightweight track for frontend repair work:

- UI fixes,
- UX workflow fixes,
- state/rendering fixes,
- presentation-only fixes,
- small demo-polish fixes.

## What to record here

Record a lightweight note when at least one of these is true:

- the bug broke a real page or workflow,
- the fix is likely to be mentioned in a demo, README, or interview,
- the bug was non-obvious and will be hard to reconstruct later,
- the fix needs before/after screenshots or a short GIF to make sense,
- the UI was inconsistent with backend state and could mislead users.

Skip a note when the change is trivial and self-evident from the commit alone, such as pure spacing or wording cleanup with no workflow impact.

## When to escalate to the heavy track

Escalate out of evidence-lite if any of these are true:

- the issue affects a key workflow such as create, edit, search, save, or navigation,
- the issue affects permission boundaries, visibility, tenant scope, or security understanding,
- the UI state diverges from backend truth in a way that can mislead user action,
- the issue is likely to regress and would be expensive if it does,
- the fix is strong enough to become a reusable engineering artifact or demo story.

## Required note fields

Each UI fix note should capture:

- issue,
- impact,
- reproduction path,
- fix summary,
- evidence,
- validation checklist,
- related commit or PR,
- escalation decision.

Use the template in [docs/UI&UX/UI-FIX-NOTE-TEMPLATE.md](docs/UI&UX/UI-FIX-NOTE-TEMPLATE.md).

## Suggested naming

Store notes in this directory with names like:

- `UI-FIX-YYYYMMDD-short-name.md`
- `WORKFLOW-FIX-YYYYMMDD-short-name.md`
- `UX-BUG-YYYYMMDD-short-name.md`

Keep screenshot or GIF assets beside the note in an `assets/` subfolder if needed.

Asset naming and storage guidance lives in [docs/UI&UX/assets/README.md](docs/UI&UX/assets/README.md).

## Minimal operating rule

For routine frontend work, this is enough:

1. Create one short note from the template.
2. Attach before/after screenshot or GIF when the difference is visual.
3. Fill the validation checklist for the affected states.
4. If the issue crosses workflow, scope, or consistency boundaries, promote it to the heavier evidence flow.

This keeps frontend evidence usable without turning small UI work into process overhead.

## Current note set

The first wave of evidence-lite notes now includes:

- `UI-FIX-20260313-book-timeline-chronicle-empty.md`
- `UI-FIX-20260313-library-context-propagation.md`
- `UI-FIX-20260313-bookshelf-link-recovery.md`
- `UI-FIX-20260313-library-tags-limit-guard.md`