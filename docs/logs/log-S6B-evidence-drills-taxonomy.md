# log-S6B（Evidence & Drills taxonomy：evidence families + retention classes + bounded cutover）

---

**id**: `S6B-evidence-drills-taxonomy`
**kind**: `log`
**title**: `evidence & drills taxonomy (evidence families + retention classes + bounded cutover) v1`
**status**: `draft`
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, Taxonomy, Artifacts, Retention, epic/s6, sub/6b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: ``
  **previous_log**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_1**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_2**: `docs/logs/log-S0D-2A-drills-evidence-automation.md`
  **reference_log_3**: `docs/logs/log-S0B-2A-scripts-snapshots-management.md`
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

- 新建 `S6B` 作为 `S6A` 之后的第二条 S6 spine，专门处理当前 repo 中“证据是什么、谁生成、应保留多久、应该放在哪一层看待”的 taxonomy 问题。
- `S6B` 的第一轮目标不是立刻搬目录，而是先固定 evidence families、retention classes、ownership boundary 与 bounded cutover 顺序，避免继续把 `fact source`、`retained summary`、`workflow-derived output` 与 `tmp scratch` 混称为 `artifacts`。
- `S6B-1A` 将作为本 spine 的第一条子 log，直接承接当前仓库的 evidence total table / inventory ledger，先把现状盘清楚，再讨论迁移与实施。

**Default choices (phase defaults / v1)**:

- taxonomy 先按“证据职能”分类，而不是按目录名或历史来源分类。
- v1 先固定六类 surface：`human-ledger`、`fact-source`、`retained-summary`、`workflow-derived`、`tmp-scratch`、`evidence-lite`。
- `P0-P1` 不移动现有文件，不回写历史目录；先定义类型、边界和实施顺序。
- 任何后续收口都必须保留 low-cardinality lookup path，避免把 operator 入口变成只能全文搜索的隐式知识。

## Definitions (optional)

- `human-ledger`: 面向人阅读的证据账本，记录 headSha、关键参数、artifact path 或 CI URL，但不是原始运行事实源。
- `fact-source`: 单次 run 或单次 drill 的原始事实源目录或结果文件，足以直接支撑 PASS/FAIL 判定。
- `retained-summary`: 面向历史追踪、dashboard、gate ledger 或 bounded reporting 的低基数汇总面。
- `workflow-derived`: docs/GitHub automation 过程中生成的 plan/manifest/apply-result/live-body snapshot 一类中间或派生产物。
- `tmp-scratch`: 临时抓取、一次性排查、下载物、重放中间文件、局部实验目录，不应默认视为长期 retained evidence。
- `evidence-lite`: 不进入 heavy drills/hard-gate 主链路、但仍需要可追溯记录的问题修复证据轨道。

## Constraints

- 不重开 `S6A` 已经稳定的 stable-entry、supply、reason-contract 与 hard-gate 设计；`S6B` 只处理 taxonomy、ownership 和 retention 问题。
- 不把 `docs/logs` 的 `Evidence` 区误判为底层事实源；它是 ledger，不是 run_dir 本身。
- 不把 `docs/issues` 里的 planner/result/live-body 一律当成 runtime evidence；它们默认属于 workflow-derived family。
- 不把 `artifacts/` 根目录等同于一种证据类型；同一目录里可以同时存在 retained summary 和 tmp scratch。
- 任何 cutover 都必须允许 bounded coexistence，不能要求一次性清空历史。

## Scope

- `P0`: taxonomy contract（evidence families、classification axes、ownership boundary）
- `P1`: current inventory（repo evidence total table、family counts、hotspot list）
- `P2`: retention and storage policy（哪类应 retained、哪类应 tmp、哪类应只保留 lookup surface）
- `P3`: generator and emission policy（哪些脚本应该直接写 fact-source、哪些只能写 retained summary、哪些只是 workflow-derived）
- `P4`: bounded cutover plan（目录收口、命名收口、历史 coexistence 与 stop conditions）

## Success Criteria (DoD)

- 仓库内存在一份明确的 evidence taxonomy，能解释当前主要 surfaces 的职责差异，而不再只靠 `artifacts` 一词泛称。
- 至少有一份 family-level total table，覆盖 `docs/logs`、`docs/labs/_snapshot`、`artifacts`、`docs/issues` 与 `docs/UI&UX` 的主要证据面。
- taxonomy 至少固定四个判断维度：`class`、`generator/owner`、`retention intent`、`operator lookup path`。
- 至少识别出当前 repo 最需要后续收口的混乱面，并把它们排进 bounded rollout 顺序，而不是只提出目录愿景。
- 后续子 logs 可以在不重开 taxonomy 争论的前提下，直接落单项治理工作。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P4` 已固定一版可重复使用的 taxonomy、inventory、retention policy、generator policy 与 bounded cutover 顺序
  - 后续 evidence-related work 已能直接引用 `S6B` 的分类与边界，而不再每次重新定义 “artifact 到底是什么”

## P0 (Contract | v1)

### P0-C1-S1 (Classification axes fixed | v1)

- 每个 evidence surface 在 v1 至少要回答四个问题：
  - `class`: 属于哪一类证据面
  - `generator/owner`: 谁生成、谁拥有 contract
  - `retention intent`: 应长期保留、条件保留，还是临时排查
  - `lookup path`: operator 应从哪里进入，而不是靠全文搜索

### P0-C1-S2 (Evidence family split fixed | v1)

- v1 先固定六类 family：
  - `human-ledger`
  - `fact-source`
  - `retained-summary`
  - `workflow-derived`
  - `tmp-scratch`
  - `evidence-lite`
- 这六类允许同仓共存，但后续 policy 必须明确哪些目录可混放、哪些不可混放。

### P0-C1-S3 (Cutover boundary fixed | v1)

- `P0-P1` 只允许 inventory 和 classification，不做目录迁移。
- `P2-P3` 才允许制定 retained/tmp 分层与 generator emission policy。
- `P4` 才讨论 bounded cutover；如果 taxonomy 和 inventory 还不稳定，不得先移动目录。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S6B/P<phase>-C<cycle>-S<steps>: <summary>`

## Plan (draft)

### P1 (Current inventory)

- P1-C1-S1: establish the first family-level evidence total table for the current repo
- P1-C1-S2: record current counts and representative file families per major surface
- P1-C1-S3: identify the first bounded hotspot list where retained and tmp are currently mixed

### P2 (Retention and storage policy)

- P2-C1-S1: define which families are authoritative fact sources versus lookup-only references
- P2-C1-S2: define retained versus tmp policy for `artifacts/` and CI inspection bundles
- P2-C1-S3: define how `docs/issues` should be treated relative to runtime evidence and logs

### P3 (Generator policy)

- P3-C1-S1: define which script families may emit fact-source outputs directly
- P3-C1-S2: define which script families may only append retained summaries or workflow-derived outputs
- P3-C1-S3: define naming/ownership expectations for future evidence surfaces

### P4 (Bounded cutover)

- P4-C1-S1: propose a bounded rollout order for evidence surface cleanup
- P4-C1-S2: define coexistence rules and stop conditions so cutover does not break existing lookup paths

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: classification axes fixed
- [ ] `P0-C1-S2`: evidence family split fixed
- [ ] `P0-C1-S3`: cutover boundary fixed

### P1 (Current inventory)

- [ ] `P1-C1-S1`: first evidence total table retained
- [ ] `P1-C1-S2`: current counts and family samples retained
- [ ] `P1-C1-S3`: hotspot list retained

### P2 (Retention and storage policy)

- [ ] `P2-C1-S1`: authoritative versus lookup-only boundaries fixed
- [ ] `P2-C1-S2`: retained versus tmp policy fixed
- [ ] `P2-C1-S3`: `docs/issues` relative position fixed

### P3 (Generator policy)

- [ ] `P3-C1-S1`: fact-source emission policy fixed
- [ ] `P3-C1-S2`: retained-summary and workflow-derived emission policy fixed
- [ ] `P3-C1-S3`: naming and ownership expectations fixed

### P4 (Bounded cutover)

- [ ] `P4-C1-S1`: bounded rollout order fixed
- [ ] `P4-C1-S2`: coexistence and stop conditions fixed

## Evidence (reserved)

- Artifacts are the source of truth for machine-facing evidence; this log records the classification contract, retained inventories, and later cutover artifacts.
- This section is the human-facing ledger and should remain separate from future retained inventory JSON or table artifacts.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

## Recent changes (for traceability, optional)

- 2026-04-04: opened `S6B` to separate evidence taxonomy, retention classes, generator ownership, and bounded cleanup order from the already-stable `S6A` hard-gate and drills contracts.
- 2026-04-04: `S6B-1A/P0-P1` retained the first formal repo inventory ledger, current scale baseline, and family owner map, so `S6B/P2-P4` can now work from a concrete surface baseline instead of rerunning ad-hoc discovery.
- 2026-04-04: `S6B-1A/P2` fixed the current retention/storage baseline in-place, including retained versus tmp handling for `artifacts`, `docs/issues`, and `docs/labs/_snapshot`, while keeping later cutover work open.
- 2026-04-04: `S6B-1A/P3` fixed the current generator/emission baseline in-place, including which families may emit `fact-source` directly, which are limited to `retained-summary` or `workflow-derived` outputs, and what naming/ownership contract future retained surfaces must satisfy.
- 2026-04-04: `S6B-1A/P4` fixed the bounded cutover baseline in-place, including rollout order, coexistence rules, and stop conditions, so later cleanup work can stay bounded instead of turning into a repo-wide rename wave.
- 2026-04-04: opened `S6B-1B` as the next bounded follow-up under `S6B`, focused on evidence naming readability for retained-summary, tmp-scratch, and snapshot run identity after `S6B-1A` stabilized the family and policy baseline.
- 2026-04-04: `S6B-1B/P0-P1` fixed the first naming baseline for field selection, per-surface grammar split, and retained-summary naming patterns, so later tmp and snapshot naming work can inherit one stable style.
- 2026-04-04: `S6B-1B/P2` fixed the first tmp-scratch naming baseline, including explicit tmp identity, anti-confusion rules, and example patterns, so retained-summary and tmp surfaces now have visibly different naming semantics.
- 2026-04-04: `S6B-1B/P3` fixed the first snapshot run-identity naming baseline, including directory-first identity, stable key file role names, and anti-patterns for fact-source naming under `docs/labs/_snapshot/**`.
- 2026-04-04: `S6B-1B/P4` retained the first bounded rename sample set, mapping representative current names to target shapes across retained-summary, tmp-scratch, and snapshot fact-source surfaces.
