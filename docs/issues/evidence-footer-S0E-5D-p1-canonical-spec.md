# S0E-5D/P1 Canonical Evidence Footer Spec

## Applicability

- Evidence Footer applies only to drills/evidence-carrying PR bodies.
- If a log does not qualify for Evidence Footer, the entire `Evidence Footer` section must be omitted.
- Commit-footer fallback is forbidden.

## Single Extraction Source

- Evidence Footer must be rendered from one explicit log-owned source block named `Evidence Footer Source`.
- The source block must live under `PR Summary Inputs (optional)`.
- PR create and PR rewrite paths must consume only this source block.
- If the source block is absent, the renderer must omit the entire `Evidence Footer` section instead of inferring footer lines from commits, phase headings, or other evidence text.

## Canonical Source Shape

- Each source line must use exactly one bullet row.
- The stage token must be wrapped in inline code.
- The artifact path must be wrapped in inline code.
- The literal separator must be ` | artifact: `.

Canonical source block:

```md
## Evidence Footer Source

- `P1-C1-S1` | artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`
- `P2-C1-S1` | artifact: `docs/issues/pr-create-preflight-S0E-5C-p2-stop-branch-collision.json`
```

## Canonical Rendered PR Section

- The rendered `Evidence Footer` section must preserve the same line shape as the source block.
- No alternate footer styles are allowed.

Canonical rendered section:

```md
## Evidence Footer

- `P1-C1-S1` | artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`
- `P2-C1-S1` | artifact: `docs/issues/pr-create-preflight-S0E-5C-p2-stop-branch-collision.json`
```

## Parser / Renderer Rules

- Preserve source order exactly.
- Do not synthesize or normalize stage IDs beyond trimming outer whitespace.
- Do not rewrite artifact paths into URLs.
- Do not mix links, prose, commit subjects, or phase-summary bullets into `Evidence Footer`.
- If any source row does not match the canonical line shape, the safe behavior is to stop with a validation error instead of rendering a second style.