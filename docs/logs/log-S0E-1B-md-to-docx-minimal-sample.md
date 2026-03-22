# log-S0E-1B (Phase 1B: CV markdown → docx minimal sample)

---

**id**: `S0E-1B`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `CV markdown → Page1/Page2 docx minimal sample (PoC archived)`
**status**: `archived`        # draft | stable | archived
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Tooling, CV, Demo, Drills, Evidence, epic/s0e, sub/1b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S0D-6A-docs-management-v4.md`
  **previous_log**: `docs/logs/log-S0E-1A-structured-cv-generator.md`
  **reference_log_1**: `docs/logs/log-S0D-6A-structured-roadmap-and-demo.md`
  **reference_log_2**: `docs/logs/log-S1-1-gov-role-minimal-ops-loop.md`
**created**: `2026-03-22`
**updated**: `2026-03-22`

---

## Decision / Outcome

**Decision**:

- Build a minimal Python-based path from existing CV markdown + metadata (from S0E-1A) to Page1/Page2 `.docx` files using `python-docx`，作为一次性 PoC。
- 本 PoC 已完成并验证可行，但由于与现有精致 docx 版式（多文本框 + 固定间距）差异过大，不作为当前 CV 生成链路的正式路径，仅保留脚本以备将来参考。

**Default choices (phase defaults / v1)**:

- Reuse S0E-1A contracts: markdown + JSON metadata remain the source of truth; generated `.docx` files are not committed to git.
- Use a small, explicit CLI under `scripts/cv/` that reads an existing variant (e.g. `cv-001-backend-en`) and emits one `.docx` per page (Page1 = HR, Page2 = engineering supplement).
- Keep formatting simple (headings + bullet lists) to minimise coupling; per-JD wording and layout tweaks stay in markdown for now.

## Definitions

- **CV markdown page**: the same page-level markdown files used by S0E-1A (for example, `cv-001-backend-p1.md`, `cv-001-backend-p2.md`).
- **CV variant metadata**: JSON metadata file describing a variant (for example, `cv-001-backend-en-meta.json`), including pages and output basename.
- **docx generator CLI**: a Python script (using `python-docx`) that reads one variant and renders each page into a `.docx` file.

## Constraints

- Generated `.docx` files must not be committed to git; they live under the `_cv/out/` directory and can be safely regenerated.
- The minimal sample should not depend on any private or heavy services; it only needs the local Python environment and `python-docx`.
- This phase focuses on demo-001 + the backend-en variant; JD-specific variants and styled templates belong to future phases.

## Scope

- `P0`: contract（最小样板的目标、输入/输出目录和 evidence 约定）。
- `P1`: implementation（Python 脚本 + python-docx wiring，支持 demo-001 backend-en variant）。
- `P2`: drill / verify（针对 demo-001 跑通至少 1 次 md → docx 生成，并记录 Evidence）。

## Success Criteria (DoD)

- 有一份清晰的 contract 说明：对 demo-001，如何从现有 markdown+metadata 生成 Page1/Page2 `.docx` 文件，以及放在哪个目录。
- `scripts/cv/` 下存在一个 Python CLI，可以针对 demo-001 读取 `cv-001-backend-en` 变体，生成 Page1/Page2 对应的 `.docx` 文件。
- 至少一次成功运行被记录在 Evidence 区域，包含 `headSha`、`variant_id`、输入目录和输出文件路径。

## Stability (what stable means)

- 本 log 已标记为 `archived`：
  - PoC 已经完成并在 Evidence 中记录；
  - 未来如需重新启用 docx 自动化，应新开 phase（例如 `S0E-2A`）并参考本 PoC 的脚本与约束。

## P0 (Contract | v1)

### P0-C1-S1（目录与命名约定）

- 源数据与 metadata：
  - 复用 S0E-1A 的约定：`docs/demo/demo-<id>/_cv/` 下的 markdown 与 `*-meta.json`。
  - 本 phase 以 `demo-001` + `cv-001-backend-en-meta.json` 为最小样板。
- 输出 `.docx`：
  - 目录：`docs/demo/demo-<id>/_cv/out/`（若不存在则自动创建）。
  - 文件名：基于 metadata 的 `output_basename`，按页面后缀输出，例如：
    - Page1（HR）：`<output_basename>-p1.docx`；
    - Page2（engineering）：`<output_basename>-p2.docx`。

### P0-C1-S2（CLI 与参数约定）

- CLI 入口位于 `scripts/cv/` 下，例如 `md_to_docx.py`。
- 最小参数：
  - `demo_id`（如 `demo-001`）。
  - `variant_id`（如 `cv-001-backend-en`）。
- 可选参数：
  - `--page`：`p1` / `p2` / `all`（默认 `all`），用于只生成单页或两页。

### P0-C1-S3（Evidence contract | v1）

- 每次运行生成脚本时，在 stdout 中为每个生成的页面打印一行 summary，例如：
  - `[OK] Generated DOCX variant <variant_id> page <page_label> from <src_dir> to <out_file>`。
- Evidence 记录至少包括：
  - `headSha=<git sha>`；
  - `variant_id=<id>`；
  - `pages=<generated pages>`；
  - `src_dir=<relative path>`；
  - `out_files=<relative paths>`。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-1B/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可为单步（例如 `...-S1`）或同一 phase/cycle 内的多步组合（例如 `...-S1S2`）。

**Branch convention**:

- 本 phase 隶属于 `S0E` scope，相关改动优先落在 `S0E-*` 分支上（当前为 `S0E-docs-management-v5`）。

**Commit discipline (recommended)**:

- 完成每个 `P*-C*-S*` 单元后，优先在 `S0E-*` 分支上及时 `commit/push`；
- 体量较小的改动可以让 P0/P1 合同与实现共享提交，但需保持信息清晰。

## Plan (draft)

### P1（Implementation）

- P1-C1-S1：在 `scripts/cv/` 下新增 `md_to_docx.py`，使用 `python-docx` 读取 variant metadata+markdown，生成 Page1/Page2 `.docx`（简单 headings + bullet 映射）。
- P1-C1-S2：针对 `demo-001` + `cv-001-backend-en` 在本地跑通 CLI，观察输出路径是否符合 P0 约定。

### P2（Drill / Verify）

- P2-C1-S1：记录至少一次成功运行的 Evidence（headSha、variant_id、pages、输入输出路径）。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`：目录与命名约定固定
- [x] `P0-C1-S2`：CLI 与参数约定固定
- [x] `P0-C1-S3`：Evidence contract 固化

### P1（Implementation）

- [x] `P1-C1-S1`：`md_to_docx.py` 初版落地
- [x] `P1-C1-S2`：demo-001 backend-en 变体本地跑通

### P2（Drill / Verify）

- [x] `P2-C1-S1`：demo-001 md → docx drill 入账

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P0-C1-S1（CV markdown → docx contract established｜2026-03-22）

- headSha: `<TBD-after-first-commit>`
- artifacts:
  - `docs/logs/log-S0E-1B-md-to-docx-minimal-sample.md`
  - `scripts/cv/md_to_docx.py`
- expected:
  - S0E-1B 明确 demo-001 md → docx 最小样板的 contract，为后续实现提供稳定边界。
- observed:
  - 本 log 已经写明上述 contract，并在 Execution Checklist 中勾选 P0 项。

### P2-C1-S1（demo-001 backend-en md → docx drill｜2026-03-22）

- headSha: `<TBD-after-first-commit>`
- variant_id: `cv-001-backend-en`
- pages: `["p1", "p2"]`
- src_dir: `docs/demo/demo-001/_cv/`
- out_files:
  - `docs/demo/demo-001/_cv/out/cv-001-backend-en-p1.docx`
  - `docs/demo/demo-001/_cv/out/cv-001-backend-en-p2.docx`
- expected:
  - CLI 能根据 metadata 生成 Page1/Page2 `.docx` 文件，stdout 打印 summary 行，输出路径符合 P0 约定。
- observed:
  - 运行 `c:/python314/python.exe scripts/cv/md_to_docx.py demo-001 cv-001-backend-en`：
    - `[OK] Generated DOCX variant cv-001-backend-en page p1 from docs\\demo\\demo-001\\_cv to docs\\demo\\demo-001\\_cv\\out\\cv-001-backend-en-p1.docx`
    - `[OK] Generated DOCX variant cv-001-backend-en page p2 from docs\\demo\\demo-001\\_cv to docs\\demo\\demo-001\\_cv\\out\\cv-001-backend-en-p2.docx`
  - 生成的 `.docx` 文件可在本地打开查看，结构与 Page1（HR）/Page2（engineering supplement）对应。

## Recent changes (for traceability, optional)

- 2026-03-22：初始化 `S0E-1B`，定义 demo-001 CV markdown → docx 最小样板的合同与执行计划。
- 2026-03-22：将 S0E-1B 标记为 `archived`，保留 PoC 记录和脚本，但删除 demo-001 生成的 `.docx` 文件，正式路径仍以 S0E-1A 的 markdown 生成链路为主。