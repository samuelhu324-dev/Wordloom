# UI Evidence Assets

This directory stores screenshots, GIFs, and short recordings used by notes in `docs/UI&UX/`.

## Naming Rule

Use filenames that are easy to sort and match back to a note:

- `YYYYMMDD-short-name-before.png`
- `YYYYMMDD-short-name-after.png`
- `YYYYMMDD-short-name-flow.gif`
- `YYYYMMDD-short-name-mobile-before.png`
- `YYYYMMDD-short-name-mobile-after.png`

Examples:

- `20260313-book-timeline-empty-before.png`
- `20260313-book-timeline-empty-after.png`
- `20260313-library-context-flow.gif`

## Minimal Rule

- Use `before` and `after` when the issue is visual.
- Use `flow` for a short GIF or recording of an interaction.
- Add `mobile` when the capture is viewport-specific.
- Keep one problem family under one short name so the note and assets are easy to match.

## Note Linkage

When a note references assets, prefer listing them in the note's `Evidence` section with relative paths under `docs/UI&UX/assets/`.

## Scope

This folder is for durable evidence worth keeping in Git. Do not put large throwaway recordings here.