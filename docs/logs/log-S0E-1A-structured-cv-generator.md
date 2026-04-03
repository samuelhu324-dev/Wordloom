# log-S0E-1A (Phase 1: Structured CV generator v1)

---

**id**: `S0E-1A`
**kind**: `log`               # log | lab | runbook | adr | note
**title**: `structured CV generator（md → template → rendered CV） v1`
**status**: `draft`           # draft | stable | archived
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Tooling, CV, Demo, Drills, Evidence, epic/s0e, sub/1a`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/316`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/249`
  **runbook**: ``
  **parent_log**: `docs/logs/log-S0D-6A-docs-management-v4.md`
  **previous_log**: ``
  **reference_log_1**: `docs/logs/log-S0D-6A-structured-roadmap-and-demo.md`
  **reference_log_2**: `docs/logs/log-S1-1-gov-role-minimal-ops-loop.md`
**created**: `2026-03-22`
**updated**: `2026-04-02`

---

## Decision / Outcome

**Decision**:

- Build a small, reusable Python-based CV generator that treats CV content as structured markdown + metadata and applies a stable template to produce rendered CV outputs（以 markdown 为主）。
- Make `docs/demo/demo-001/_cv` the first structured container, and ensure the generator can target different CV variants (for example, generic backend vs. government-role systems/platform engineer) by swapping metadata files rather than copy-pasting text.
- 明确 trade-off：保留“从现有精美 docx 模板中抽取出来的 markdown CV 文本”作为长期模板与生成源，不再在 v1 阶段追求自动生成具有复杂文本框版式的 docx，仅在需要时从 markdown 手工导出/排版 docx。

**Default choices (phase defaults / v1)**:

- Source of truth for CV content is markdown + a small YAML/JSON metadata file; generated artifacts are never committed to git.
- Template layer is explicit and versioned (e.g. `docs/demo/templates/cv-template-en.md`), so wording and layout can be evolved without rewriting scripts.
- Python is the primary implementation language, using a light templating library (e.g. Jinja2) and plain CLI entrypoints under `scripts/cv/`.
- demo containers follow the `demo-001` contract from S0D-6A; future demos can reuse the same generator with different inputs.
- 对于高阶排版（多文本框+固定间距等），仍以手工维护的 docx 模板为主；本 phase 只保证 markdown 版本可读、结构化，docx 自动化属于可选后续实验（见 S0E-1B），不作为 v1 的必需能力。

## Definitions

- **CV source markdown**: curated markdown files (`cv-001-backend-p1.md`, `cv-001-backend-p2.md`, etc.) that hold the textual CV sections.
- **CV metadata**: a small YAML/JSON file describing name, contact, target role/JD mapping, and which sections/pages to include.
- **CV template**: a markdown or HTML file with placeholders used by the generator to build a final rendered CV.
- **rendered CV**: the generated markdown/HTML file ready for export/print; docx/pdf is optional and may rely on pandoc or external tooling.

## Constraints

- Generated artifacts must not be committed to the repository; only source markdown, metadata and templates are versioned.
- The generator should not depend on heavy external services; optional pandoc integration must degrade gracefully if pandoc is not installed.
- The first phase focuses on a single-language CV (English) and a single demo (`demo-001`); multi-language and multi-demo support can be added later.
- 不尝试在脚本中重建或操作复杂的 Word 文本框版式；针对 docx 的更精细排版工作默认在 Word 模板里人工完成，S0E-1A 只负责生成结构化文本（markdown）供人工或其他工具再利用。

## Scope

- `P0`: contract（目录约定、模板与数据分层、命名与 evidence 规则）。
- `P1`: implementation（Python 脚本 + Jinja2 模板 wiring，支持 demo-001）。
- `P2`: drill / verify（针对 demo-001 跑通至少 1 次生成，记录 headSha + 输入/输出路径）。
- `P3`: adoption（把本工具接到后续 demo 或 JD-specific CV 变体上；可选）。

## Success Criteria (DoD)

- 有一份清晰的目录与命名 contract，说明 CV 源数据、模板、生成结果分别放在哪里，以及如何命名（demo id / variant id）。
- `scripts/cv/` 下存在一个 Python CLI，可针对 demo-001 从 markdown+metadata 生成至少一种 rendered CV（markdown 或 HTML）。
- 至少一次成功运行被记录在 Evidence 区域，包含 `headSha`、输入路径与输出路径。
- demo-001 的 CV 内容可以通过“改 metadata + 少量文本”快速生成针对某个 JD 的版本，而不是手工复制。

## Stability (what stable means)

- 本 log 标记为 `stable` 时：
  - P0 合同不再大改（仅允许小幅补充字段）；
  - Python 脚本可以稳定从 demo-001 源数据生成 rendered CV，并在至少一次 Evidence 中被验证；
  - 后续新增 demo 或 JD 变体不需要修改脚本，只需新增源 markdown/metadata 与可选模板。

## P0 (Contract | v1)

### P0-C1-S1（目录与命名约定）

- 源数据：
  - 按 demo 容器存放在 `docs/demo/demo-<id>/_cv/` 下，例如 demo-001 使用 `docs/demo/demo-001/_cv/`。
  - 页面级 markdown：`cv-<profile>-p1.md`、`cv-<profile>-p2.md`，例如 `cv-001-backend-p1.md` / `cv-001-backend-p2.md`。
- 模板：
  - 统一放在 `docs/demo/templates/` 下，例如 `cv-template-en.md`；后续可按语言或布局命名（`cv-template-en-compact.md` 等）。
- 输出：
  - 默认输出目录为 `docs/demo/demo-<id>/_cv/out/`，文件名如 `cv-001-backend-en.md` / `cv-001-backend-en.html`。

### P0-C1-S2（metadata 与 variant 约定）

- 每个 CV 变体有一个 metadata 文件（YAML/JSON），例如：
  - `docs/demo/demo-001/_cv/cv-001-backend-meta.yaml`（通用 backend 版）。
  - 未来可新增 `cv-001-systems-platform-gov-meta.yaml`（对准政府 systems/platform JD）。
- metadata 至少包含：
  - `name / contact / location`；
  - `target_role` 与可选 `target_jd_ref`（指向 intake 样本文件）；
  - `pages` / `sections` 配置：决定从哪些 markdown 源文件、哪些段落组装最终 CV。

### P0-C1-S3（Evidence contract | v1）

- 每次运行生成脚本时，应在 stdout 中打印一行 summary，例如：
  - `[OK] Generated CV variant <variant_id> from <src_dir> to <out_file>`。
- Evidence 记录至少包括：
  - `headSha=<git sha>`；
  - `variant_id=<id>`（例如 `cv-001-backend-en` 或 `cv-001-systems-platform-gov-en`）；
  - `src_dir=<relative path>`（如 `docs/demo/demo-001/_cv/`）；
  - `out_file=<relative path>`（如 `docs/demo/demo-001/_cv/out/cv-001-backend-en.md`）。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-1A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- 本 phase 隶属于 `S0E` scope，相关改动优先落在 `S0E-*` 分支上（本次为 `S0E-docs-management-v5`）。

**Commit discipline (recommended)**:

- 完成每个 `P*-C*-S*` 单元后，尽量在 `S0E-*` 分支上及时 `commit/push`；
- 体量较小时可以让 P0/P1 合同与最小实现共享同一条提交，但优先保持信息清晰。

## Plan (draft)

### P1（Implementation）

- P1-C1-S1：在 `scripts/cv/` 下新增 Python CLI（例如 `gen_cv.py`），读取 metadata + markdown 并通过 Jinja2 模板生成 rendered CV（markdown）。
- P1-C1-S2：为 demo-001 配置首个 metadata 文件与模板，并确保脚本可以从命令行运行（例如 `python scripts/cv/gen_cv.py demo-001 cv-001-backend-en`）。

### P2（Drill / Verify）

- P2-C1-S1：针对 demo-001 跑通至少一次生成流程，将 stdout summary 与输出文件路径记录到本 log 的 Evidence 区。

### P3（Adoption）

- P3-C1-S1：为至少一个 JD（例如当前政府 systems/platform 岗位）新增一个 variant metadata，并验证脚本可以生成对应 CV 版本。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`：目录与命名约定固定
- [x] `P0-C1-S2`：metadata 与 variant 约定固定
- [x] `P0-C1-S3`：Evidence contract 固化

### P1（Implementation）

- [x] `P1-C1-S1`：Python CLI 初版落地
- [x] `P1-C1-S2`：demo-001 首个 metadata + 模板配置完成

### P2（Drill / Verify）

- [ ] `P2-C1-S1`：demo-001 CV 生成 drill 入账

### P3（Adoption）

- [ ] `P3-C1-S1`：至少一个 JD-specific variant 入账

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P0-C1-S1（Structured CV generator contract established｜2026-03-22）

- headSha: `<TBD-after-first-commit>`
- artifacts:
  - `docs/logs/log-S0E-1A-structured-cv-generator.md`
  - `docs/demo/demo-001/_cv/`（现有 CV markdown 源文件）
- expected:
  - S0E-1A 明确 structured CV 工具的目录约定与 evidence 合同，为后续实现提供稳定边界。
- observed:
  - 本 log 已经写明上述 contract，并在 Execution Checklist 中勾选 P0 项，后续提交会记录 headSha。

## Recent changes (for traceability, optional)

- 2026-03-22：初始化 `S0E-1A`，定义 structured CV generator 的合同、命名与 evidence 规则，作为 docs-management v5 下的新子 phase。
- 2026-03-22：记录 trade-off：仅保留从手工 docx 模板中抽取的 markdown CV 作为长期模板与生成源，暂不推进“复杂版式 docx 自动生成”，相关 PoC 见 `log-S0E-1B-md-to-docx-minimal-sample.md`。