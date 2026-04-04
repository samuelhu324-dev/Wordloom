# log-S6B-1B（Evidence naming baseline：retained-summary + tmp-scratch + snapshot run identity）

---

**id**: `S6B-1B`
**kind**: `log`
**title**: `evidence naming baseline (retained-summary + tmp-scratch + snapshot run identity) v1`
**status**: `draft`
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, Taxonomy, Naming, Retention, epic/s6, sub/1b`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/358`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/361`
  **runbook**: ``
  **roadmap**: `docs/roadmap/_draft/road-S2-.md`
  **parent_log**: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
  **previous_log**: `docs/logs/log-S6B-1A-evidence-surface-inventory-ledger.md`
  **reference_log_1**: `docs/logs/log-S6B-1A-evidence-surface-inventory-ledger.md`
  **reference_log_2**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_3**: `docs/logs/log-S0D-2A-drills-evidence-automation.md`
**issue_keyword**: `naming`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s6/evidence & drills, sub/1`
**issue_module_labels**: ``
**issue_milestone**: `road-S2`
**issue_parent**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/356`
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/_draft/road-S2-.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: `P3`
**roadmap_bridge_refs**: `S6B-1B -> road-S2 / M5 / P3`
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: `road-S2`
**pr_base**: `main`
**pr_development_issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/358`
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
- `P4`: bounded rename sample set（当前名字到目标名字的第一轮 mapping 样例）

## Success Criteria (DoD)

- 至少明确回答 retained-summary 文件名里必须出现哪些字段，且不再接受纯 `latest` / `runs` / `result` 这类裸名字作为稳定入口。
- 至少明确回答 tmp-scratch 文件名如何显式暴露 tmp 身份，避免被误认成 retained ledger。
- 至少明确回答 `docs/labs/_snapshot/**` 的 run identity 应主要由目录表达，而不是把 run 上下文散落到模糊文件名中。
- 至少保留一组 bounded rename sample mappings，回答“当前常见名字如果要收口，目标形态应该长什么样”。
- naming grammar 至少能让 operator 在不打开内容的前提下，大致判断：`这是什么`、`谁的`、`是 retained 还是 tmp`、`该从哪里看起`。

## Stability (what stable means)

- This log can be marked `stable` when:
  - the first naming baseline for `retained-summary`, `tmp-scratch`, and snapshot run identity is retained
  - later cleanup work can reference this naming baseline directly instead of renegotiating filename semantics every time

## PR Summary Inputs (optional)

**PR summary bullets**:

- Fix the first naming baseline for retained-summary, tmp-scratch, and snapshot run identity so operators can infer surface role before opening file contents.
- Retain a bounded current-to-target rename sample set for `artifacts/`, `_tmp_` / `_local_`, and `docs/labs/_snapshot/**` surfaces instead of leaving naming cleanup at abstract rules only.
- Start the first tracked retained-summary coexistence path by selecting `write_gate` as the candidate family, enabling dual-write, and migrating the first primary lookup surfaces.

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

## P4 (Bounded rename sample set | v1)

### P4-C1-S1 (Retained-summary sample mappings retained | v1)

| current name | target shape | notes |
| --- | --- | --- |
| `s5b3a-runs.json` | `s5b3a.runs.history.json` | 补上点分 grammar，并把裸 `runs` 收口为 retained summary history surface |
| `s2d-runs.json` | `s2d.runs.history.json` | 保留 owner family，明确这是 history-like summary，而不是原始事实源 |
| `s2b3a-baseline-runs.final.json` | `s2b3a.baseline.runs.final.json` | 把复合 purpose 拆成稳定字段顺序 |
| `p0c4_dual_run_window.view.json` | `p0c4.dual-run-window.view.json` | 把 retained summary 统一到点分命名，而不是混用下划线 |

### P4-C1-S2 (Tmp-scratch sample mappings retained | v1)

| current name | target shape | notes |
| --- | --- | --- |
| `_tmp_p3c2_write_gate_runs.json` | `_tmp_p3c2_write_gate_runs_20260404.json` | tmp 身份保留，同时补上最小时间或 run context |
| `_tmp_recent_write_gate_runs.json` | `_tmp_write_gate_recent_runs_20260404.json` | 避免只有“recent”这种局部语境，补足 purpose + date |
| `_tmp_pr_prep_s0e_2d_plan.json` | `_tmp_s0e_pr_prep_plan_2d_20260404.json` | 先写 owner，再写 purpose/context，避免词序漂移 |
| `_local_s2b6a/` | `_local_s2b6a_review_20260404/` | `_local_` 目录也应补足用途或上下文，而不是只剩 family id |

### P4-C1-S3 (Snapshot run-identity sample mappings retained | v1)

| current shape | target shape | notes |
| --- | --- | --- |
| `auto/S5B-3A/<run_id>/output.json` | `auto/S5B-3A/<run_id>/result.json` | run identity 由目录承担，文件名只表达角色 |
| `auto/S2B-2A-1A/<run_id>/manifest-output.json` | `auto/S2B-2A-1A/<run_id>/manifest.json` | 避免在单文件名里重复编码 output 语义 |
| `manual/_lab-S3A-2A-3A-expB/<run_id>/capture-context.json` | `manual/_lab-S3A-2A-3A-expB/<run_id>/context.json` | manual track 也应优先使用稳定角色名 |
| `auto/<scenario>/<run_id>/final-result.json` | `auto/<scenario>/<run_id>/result.json` | 若目录已表达 run identity，文件名应回到标准 role name |

### P4-C1-S4 (Bounded sample usage rules fixed | v1)

- 本节样例的目的不是要求今天立刻 repo-wide rename，而是给后续 bounded cleanup 一个明确目标形态。
- 若某个现有名字已经被外部脚本或 log 稳定引用，则后续真实 rename 应先进入 coexistence，再切换 lookup path，不应直接硬切。
- 样例优先覆盖当前最常见的三类 surface：`artifacts/` retained-summary、`artifacts/_tmp_*` / `_local_*`、`docs/labs/_snapshot/**`。
- 如果后续发现某个 family 的命名长期脱离本样例层，应优先先补 mapping，再决定是否真正执行 rename。

### P4-C2-S1 (First local bounded rename sample executed | v1)

| surface class | old path | new path | execution note |
| --- | --- | --- | --- |
| `retained-summary` | `artifacts/p0c4_dual_run_window.view.json` | `artifacts/p0c4.dual-run-window.view.json` | 选作第一条 retained-summary 实操样例，因为当前 repo 内未发现稳定的非-log 引用 |
| `tmp-scratch` | `artifacts/_tmp_recent_write_gate_runs.json` | `artifacts/_tmp_write_gate_recent_runs_20260404.json` | 保留 tmp 身份，同时补足 purpose + date |
| `tmp-scratch` | `artifacts/_tmp_p3c2_write_gate_runs.json` | `artifacts/_tmp_p3c2_write_gate_runs_20260404.json` | 保留 tmp 身份，同时补足最小时间上下文 |

### P4-C2-S2 (Ignored-surface execution boundary fixed | v1)

- 上述 rename 已在当前 workspace 本地执行。
- 这些样例文件位于 `artifacts/` ignored operator surface 下，默认受 `.gitignore` 覆盖，因此本次提交不会把 renamed artifact 本体推上远端。
- 这次提交会保留的是：
  - naming baseline 本身
  - current-to-target mapping 样例
  - “本地已执行一轮 bounded rename rehearsal”的记账结果
- 若后续要把某类 renamed artifacts 变成 repo-tracked retained surface，应先在 `S6B-1A` / `S6B-1B` 中明确它们不再属于 ignored operator scratch lane，再决定是否纳入版本控制。

### P4-C3-S1 (First repo-tracked coexistence candidate selected | v1)

| current tracked path | candidate target shape | owner family | why selected now |
| --- | --- | --- | --- |
| `artifacts/write_gate_runs.latest.json` | `artifacts/s2b.write-gate.runs.latest.json` | `S2B` write-gate family | 当前是 repo-tracked retained-summary，且 naming 含义最明显地偏向“generic latest file”而不是稳定 family-owned summary surface |

- 这条路径被选为 `C3` 候选，不是因为它最容易改，而是因为它最能代表“真实 tracked retained-summary rename 不能只改文件名，还要处理脚本 / runbook / log / quick-command 引用”的完整问题。

### P4-C3-S2 (Tracked coexistence prerequisites fixed | v1)

- 对 repo-tracked retained-summary，真实 rename 之前至少要满足以下前置条件：
  - generator 默认写入路径已切换到新名字
  - 旧路径在 coexistence 期间仍能被读取，或者存在清晰 alias / fallback 机制
  - 主要 operator lookup 文档已同步到新路径
  - 旧路径何时停止继续写入有明确 stop condition，而不是无限期双写
- 对 `artifacts/write_gate_runs.latest.json` 而言，当前至少涉及：
  - `scripts/p1_write_gate_regression.ps1`
  - 多份 `docs/runbook` / `docs/QUICK_COMMANDS`
  - 大量 `S2B-*` / `S0D-*` logs 中的 SoT 引用
- 因此 `C3` 的结论是：这条 tracked retained-summary 现在已经适合进入 coexistence 设计，但还不适合在没有 alias/fallback 的前提下直接 rename。

### P4-C3-S3 (Deferred execution boundary fixed | v1)

- `C3` 本轮不直接执行 `artifacts/write_gate_runs.latest.json` 的真实 rename。
- 原因不是 naming baseline 不够清楚，而是当前引用面过深，直接改名会同时破坏：
  - generator 默认输出路径
  - operator runbook lookup path
  - 大量历史 log 中的 SoT 文字引用
- 因此 `C3` 完成的不是 rename 本身，而是把第一条 tracked candidate、其目标形态、以及进入真实 coexistence 之前必须补齐的边界固定下来。
- 后续若继续做 `C4`，合理方向应是：
  - 先给 generator 增加新路径或 alias 支持
  - 再补一轮 docs / runbook / quick-command lookup migration
  - 最后才进入 bounded dual-write / dual-read coexistence 或正式切换

### P4-C4-S1 (Tracked alias/fallback coexistence enabled | v1)

- `scripts/p1_write_gate_regression.ps1` 现在默认写入新的 primary SoT：`artifacts/s2b.write-gate.runs.latest.json`。
- 同时保留 legacy alias 写入：`artifacts/write_gate_runs.latest.json`。
- 这意味着 generator 已进入 bounded dual-write coexistence，而不是继续只写旧路径。

### P4-C4-S2 (Primary lookup migration started | v1)

- 第一轮 operator-facing lookup migration 已覆盖最关键的最小面：
  - `docs/runbook/run-S2B-projection-table-merge.md`
  - `docs/QUICK_COMMANDS.md`
  - `docs/logs/log-S2B-projection-table-merge.md`
- 这些入口现在统一表达为：
  - primary SoT：`artifacts/s2b.write-gate.runs.latest.json`
  - legacy alias：`artifacts/write_gate_runs.latest.json`

### P4-C4-S3 (Tracked coexistence stop-condition still open | v1)

- `C4` 已完成 generator dual-write 和最小 lookup migration，但 stop condition 仍未满足。
- 当前还不能移除 legacy alias，原因是：
  - 旧路径在 repo 内仍有大量历史 log / runbook / helper references
  - 还未完成全量 lookup migration
  - 还未验证 downstream operator workflow 是否已稳定转向新 primary path
- 因此 `C4` 的结果是：tracked coexistence 已开始，但 cutover 仍处于 dual-write / dual-read 阶段。

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

### P4 (Bounded rename sample set)

- P4-C1-S1: retain first current-to-target sample mappings for retained-summary names
- P4-C1-S2: retain first current-to-target sample mappings for tmp-scratch names
- P4-C1-S3: retain first current-to-target sample mappings for snapshot run identity
- P4-C1-S4: fix bounded sample usage rules for later cleanup
- P4-C2-S1: execute one local bounded rename sample across low-risk retained-summary and tmp-scratch files
- P4-C2-S2: fix the execution boundary for ignored artifact surfaces
- P4-C3-S1: select the first repo-tracked retained-summary candidate for coexistence-oriented rename
- P4-C3-S2: fix prerequisites for a tracked retained-summary coexistence cutover
- P4-C3-S3: fix the deferred execution boundary for deep-reference tracked paths
- P4-C4-S1: enable tracked alias/fallback coexistence for the first retained-summary candidate
- P4-C4-S2: start the primary lookup migration for the first tracked retained-summary candidate
- P4-C4-S3: retain the open stop-condition boundary for tracked coexistence

## Execution Checklist (unchecked)

### P0 (Naming axes)

- [x] `P0-C1-S1`: naming fields fixed
- [x] `P0-C1-S2`: per-surface grammar split fixed

### P1 (Retained-summary naming)

- [x] `P1-C1-S1`: stable retained-summary grammar fixed
- [x] `P1-C1-S2`: retained-summary anti-patterns fixed
- [x] `P1-C1-S3`: retained-summary examples retained

### P2 (Tmp-scratch naming)

- [x] `P2-C1-S1`: tmp identity kept visible
- [x] `P2-C1-S2`: tmp anti-confusion rule fixed
- [x] `P2-C1-S3`: tmp examples retained

### P3 (Snapshot run identity)

- [x] `P3-C1-S1`: run identity belongs to directory first
- [x] `P3-C1-S2`: key file role names fixed
- [x] `P3-C1-S3`: snapshot naming anti-patterns fixed

### P4 (Bounded rename sample set)

- [x] `P4-C1-S1`: retained-summary sample mappings retained
- [x] `P4-C1-S2`: tmp-scratch sample mappings retained
- [x] `P4-C1-S3`: snapshot run-identity sample mappings retained
- [x] `P4-C1-S4`: bounded sample usage rules fixed
- [x] `P4-C2-S1`: first local bounded rename sample executed
- [x] `P4-C2-S2`: ignored-surface execution boundary fixed
- [x] `P4-C3-S1`: first repo-tracked coexistence candidate selected
- [x] `P4-C3-S2`: tracked coexistence prerequisites fixed
- [x] `P4-C3-S3`: deferred execution boundary fixed
- [x] `P4-C4-S1`: tracked alias/fallback coexistence enabled
- [x] `P4-C4-S2`: primary lookup migration started
- [x] `P4-C4-S3`: tracked coexistence stop-condition boundary retained

## Evidence (reserved)

- This log is the human-facing naming ledger for evidence surfaces; later script-side validators or rename plans should reference this baseline instead of redefining naming semantics ad hoc.
- Prefer one stable naming grammar per surface family rather than one universal pattern across all evidence kinds.

## Recent changes (for traceability, optional)

- 2026-04-04: opened `S6B-1B` to continue the screenshot-1 naming problem after `S6B-1A` fixed evidence families, retention, generator policy, and bounded cutover order.
- 2026-04-04: retained the first naming baseline for `artifacts/` retained-summary files, `_tmp_` / `_local_` scratch outputs, and `docs/labs/_snapshot/**` run identity so later cleanup can standardize names without collapsing all surfaces into one directory model.
- 2026-04-04: completed `P0/P1` v1 by fixing the naming fields, per-surface grammar split, retained-summary grammar, anti-pattern set, and first example set for stable summary names.
- 2026-04-04: completed `P2` v1 by fixing explicit tmp identity, anti-confusion rules between tmp and retained naming, and a first example set for `_tmp_` / `_local_` scratch outputs.
- 2026-04-04: completed `P3` v1 by fixing directory-first run identity, stable key file role names, and snapshot naming anti-patterns for `docs/labs/_snapshot/**` fact-source surfaces.
- 2026-04-04: completed `P4` v1 by retaining the first bounded current-to-target rename sample set for retained-summary, tmp-scratch, and snapshot run identity, so later cleanup work has concrete mapping examples instead of only abstract naming rules.
- 2026-04-04: executed a first local bounded rename rehearsal under `P4/C2` on one retained-summary artifact and two tmp artifacts, and fixed the rule that ignored operator surfaces are recorded in the naming ledger but not pushed as tracked artifact files by default.
- 2026-04-04: completed `P4/C3` by selecting `artifacts/write_gate_runs.latest.json` as the first repo-tracked coexistence candidate, fixing its target naming shape and cutover prerequisites, and explicitly deferring direct rename until alias / fallback and lookup migration boundaries are ready.
- 2026-04-04: completed `P4/C4` by enabling dual-write coexistence from `scripts/p1_write_gate_regression.ps1` to the new primary path `artifacts/s2b.write-gate.runs.latest.json`, starting the minimal lookup migration, and keeping legacy alias removal explicitly out of scope until broader references are migrated.