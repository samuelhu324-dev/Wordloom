# log-S6B-1B（Evidence naming baseline：retained-summary + tmp-scratch + snapshot run identity）

---

**id**: `S6B-1B`
**kind**: `log`
**title**: `evidence naming baseline (retained-summary + tmp-scratch + snapshot run identity) v1`
**status**: `draft`
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, Taxonomy, Naming, Retention, epic/s6, sub/1b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
  **previous_log**: `docs/logs/log-S6B-1A-evidence-surface-inventory-ledger.md`
  **reference_log_1**: `docs/logs/log-S6B-1A-evidence-surface-inventory-ledger.md`
  **reference_log_2**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_3**: `docs/logs/log-S0D-2A-drills-evidence-automation.md`
**issue_keyword**: ``
**issue_top_labels**: ``
**issue_scope_labels**: ``
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: ``
**pr_development_issue**: ``
**created**: `2026-04-04`
**updated**: `2026-04-04`

---

## Decision / Outcome

**Decision**:

- `S6B-1B` 承接 `S6B-1A` 已经固定的 evidence families / retention / cutover baseline，继续处理“看名字就能大致知道这是什么”的问题。
- 本 log 的 v1 目标不是立刻重命名全仓，而是先收口三类最容易混淆的命名面：
  - `artifacts/` 下的 `retained-summary`
  - `artifacts/_tmp_*` / `_local_*` 下的 `tmp-scratch`
  - `docs/labs/_snapshot/**` 下的 run directory 与关键事实源文件
- naming baseline 必须服务 operator lookup，而不是只服务脚本；人在不打开文件内容前，应先从名字大致判断它的 family、owner、用途和 retained/tmp 身份。

**Default choices (phase defaults / v1)**:

- 先统一 naming grammar，不先推动 repo-wide rename campaign。
- naming baseline 只覆盖当前最常见、最容易误解的 surfaces；少量历史例外后续再通过 bounded coexistence 处理。
- retained 和 tmp 必须用不同语法风格，让人一眼能看出“这是稳定入口”还是“这是临时调查物”。
- `docs/labs/_snapshot/**` 的主身份由 run directory 表达，不要求把所有上下文都挤进单文件名。

## Definitions (optional)

- `naming grammar`: 文件名或目录名应该稳定表达的字段顺序与分隔方式。
- `run identity`: 单次 run / drill 的唯一上下文标识，例如 scenario、track、run_id、manual/auto。
- `stable entry name`: 可以长期作为 lookup path 被引用的 retained 名称，不依赖临时缩写或局部口头知识。

## Constraints

- 不重开 `S6B-1A` 已经固定的 surface family 和 retention intent；`S6B-1B` 只处理 naming readability 和 naming discipline。
- 不要求一次性重命名历史 retained surfaces；先约束新写入，再为后续 bounded cleanup 提供目标样式。
- 不把 `docs/labs/_snapshot/**` 改成 summary ledger 风格；它仍然是 fact-source surface。
- 不允许把 tmp naming 做得像 retained naming；tmp 的目的就是防误认，而不是追求美观。

## Scope

- `P0`: naming axes（每类命名至少要表达哪些字段）
- `P1`: retained-summary naming baseline（`artifacts/` 稳定 ledger 命名）
- `P2`: tmp-scratch naming baseline（临时调查物命名）
- `P3`: snapshot run identity baseline（`docs/labs/_snapshot/**` run dir 与关键文件命名）

## Success Criteria (DoD)

- 至少明确回答 retained-summary 文件名里必须出现哪些字段，且不再接受纯 `latest` / `runs` / `result` 这类裸名字作为稳定入口。
- 至少明确回答 tmp-scratch 文件名如何显式暴露 tmp 身份，避免被误认成 retained ledger。
- 至少明确回答 `docs/labs/_snapshot/**` 的 run identity 应主要由目录表达，而不是把 run 上下文散落到模糊文件名中。
- naming grammar 至少能让 operator 在不打开内容的前提下，大致判断：`这是什么`、`谁的`、`是 retained 还是 tmp`、`该从哪里看起`。

## Stability (what stable means)

- This log can be marked `stable` when:
  - the first naming baseline for `retained-summary`, `tmp-scratch`, and snapshot run identity is retained
  - later cleanup work can reference this naming baseline directly instead of renegotiating filename semantics every time

## P0 (Naming axes | v1)

### P0-C1-S1 (Naming fields fixed | v1)

- v1 naming baseline 至少要求回答以下字段中的核心子集：
  - `owner family`
  - `purpose`
  - `scope or horizon`（例如 `latest`, `history`, `summary`, `manifest`）
  - `retained or tmp identity`
- 不同 surface 不要求同一套字段全部出现，但不能退化成只剩通用名词。

### P0-C1-S2 (Per-surface grammar split fixed | v1)

- `retained-summary`：优先采用点分命名，强调稳定入口与语义收口。
- `tmp-scratch`：优先采用下划线命名，显式保留 `_tmp_` / `_local_` 身份。
- `fact-source` snapshot：优先由目录表达 run identity，目录内关键文件用稳定角色名，不靠长文件名堆字段。

## P1 (Retained-summary naming baseline | v1)

### P1-C1-S1 (Stable retained-summary grammar fixed | v1)

- 推荐格式：`<owner>.<purpose>.<scope>.<format>`
- 其中：
  - `<owner>`: 如 `s0e`, `s2d`, `s5b3a`, `s6b`
  - `<purpose>`: 如 `write-gate`, `issue-sync`, `coverage`, `publish-verify`
  - `<scope>`: 如 `latest`, `history`, `summary`, `index`, `runs`
  - `<format>`: 真实扩展名，如 `json`, `md`, `txt`

### P1-C1-S2 (Retained-summary anti-patterns fixed | v1)

- 不再接受以下名字作为长期 retained 入口：
  - `latest.json`
  - `runs.json`
  - `result.json`
  - `summary.json`
- 原因不是这些词不能出现，而是它们不能脱离 owner 和 purpose 单独存在。

### P1-C1-S3 (Retained-summary examples retained | v1)

- 推荐示例：
  - `s6b.write-gate.runs.latest.json`
  - `s0e.issue-sync.history.json`
  - `s2d.coverage.summary.json`
  - `s5b4a.publish-verify.index.json`

## P2 (Tmp-scratch naming baseline | v1)

### P2-C1-S1 (Tmp identity must stay visible | v1)

- 推荐格式：`_tmp_<owner>_<purpose>_<context>_<date_or_runid>.<ext>`
- 若是本地临时人工调查，可保留 `_local_` 前缀，但也应继续带 owner / purpose / context。

### P2-C1-S2 (Tmp anti-confusion rule fixed | v1)

- tmp 名称必须显式保留 `tmp` / `local` 语义。
- tmp 名称不得伪装成稳定 ledger，例如：
  - 不应命名为 `s6b.write-gate.runs.latest.json`
  - 不应命名为 `coverage.summary.json`
- 即使内容以后可能升级为 retained，也应先在 tmp lane 中保持 tmp 语义，待 contract 被接受后再升级命名。

### P2-C1-S3 (Tmp examples retained | v1)

- 推荐示例：
  - `_tmp_s6b_write_gate_replay_20260404.json`
  - `_tmp_s0e_pr_prep_run_22750336329.json`
  - `_tmp_s4d4b_ci_inspect_23575789110.txt`
  - `_local_s2c_shadow_verify_20260404.md`

## P3 (Snapshot run identity baseline | v1)

### P3-C1-S1 (Run identity belongs to directory first | v1)

- `docs/labs/_snapshot/**` 的主身份应先由目录表达：
  - `auto/<scenario>/<run_id>/`
  - `manual/<drill_family>/<run_id>/`
- 目录名至少应让人知道：这是 auto 还是 manual、属于哪个 scenario/drill family、对应哪次 run。

### P3-C1-S2 (Key files should keep role names stable | v1)

- run 目录内的关键文件优先使用稳定角色名，而不是每个文件都重新编码全部上下文。
- 推荐角色名示例：
  - `result.json`
  - `manifest.json`
  - `context.json`
  - `stdout.log`
  - `stderr.log`
- 这样 operator 的认知负担由目录承担，目录内文件名只回答“它在这次 run 里扮演什么角色”。

### P3-C1-S3 (Snapshot anti-patterns fixed | v1)

- 不推荐只留下 `output.json`、`result.json` 在缺乏 run identity 的模糊目录里。
- 不推荐把 scenario、owner、run_id、status 全部堆进单个文件名中，导致 run 目录本身失去存在意义。
- 不推荐把 snapshot fact-source 文件命名成 retained-summary 风格，例如 `s3a.coverage.latest.json`。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S6B-1B/P<phase>-C<cycle>-S<steps>: <summary>`

## Plan (draft)

### P1 (Retained-summary naming)

- P1-C1-S1: fix the stable retained-summary naming grammar
- P1-C1-S2: define anti-patterns for ambiguous retained-summary names
- P1-C1-S3: retain a first example set for stable summary names

### P2 (Tmp-scratch naming)

- P2-C1-S1: fix explicit tmp naming identity
- P2-C1-S2: define anti-confusion rules between tmp and retained naming
- P2-C1-S3: retain a first example set for tmp naming

### P3 (Snapshot run identity)

- P3-C1-S1: fix run identity to directory-first naming
- P3-C1-S2: fix stable role names for key files inside snapshot run dirs
- P3-C1-S3: define snapshot naming anti-patterns

## Execution Checklist (unchecked)

### P0 (Naming axes)

- [x] `P0-C1-S1`: naming fields fixed
- [x] `P0-C1-S2`: per-surface grammar split fixed

### P1 (Retained-summary naming)

- [x] `P1-C1-S1`: stable retained-summary grammar fixed
- [x] `P1-C1-S2`: retained-summary anti-patterns fixed
- [x] `P1-C1-S3`: retained-summary examples retained

### P2 (Tmp-scratch naming)

- [ ] `P2-C1-S1`: tmp identity kept visible
- [ ] `P2-C1-S2`: tmp anti-confusion rule fixed
- [ ] `P2-C1-S3`: tmp examples retained

### P3 (Snapshot run identity)

- [ ] `P3-C1-S1`: run identity belongs to directory first
- [ ] `P3-C1-S2`: key file role names fixed
- [ ] `P3-C1-S3`: snapshot naming anti-patterns fixed

## Evidence (reserved)

- This log is the human-facing naming ledger for evidence surfaces; later script-side validators or rename plans should reference this baseline instead of redefining naming semantics ad hoc.
- Prefer one stable naming grammar per surface family rather than one universal pattern across all evidence kinds.

## Recent changes (for traceability, optional)

- 2026-04-04: opened `S6B-1B` to continue the screenshot-1 naming problem after `S6B-1A` fixed evidence families, retention, generator policy, and bounded cutover order.
- 2026-04-04: retained the first naming baseline for `artifacts/` retained-summary files, `_tmp_` / `_local_` scratch outputs, and `docs/labs/_snapshot/**` run identity so later cleanup can standardize names without collapsing all surfaces into one directory model.
- 2026-04-04: completed `P0/P1` v1 by fixing the naming fields, per-surface grammar split, retained-summary grammar, anti-pattern set, and first example set for stable summary names.