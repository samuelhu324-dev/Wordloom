# log-S6B-1A（Evidence surface inventory ledger：repo evidence total table + current ownership map）

---

**id**: `S6B-1A`
**kind**: `log`
**title**: `evidence surface inventory ledger (repo evidence total table + current ownership map) v1`
**status**: `draft`
**scope**: `S6`
**tags**: `EVOLUTION, Evidence, Drills, Taxonomy, Inventory, Retention, epic/s6, sub/1a`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/357`
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/_draft/road-S2-.md`
  **parent_log**: `docs/logs/log-S6B-evidence-drills-taxonomy.md`
  **previous_log**: ``
  **reference_log_1**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_2**: `docs/logs/log-S0D-2A-drills-evidence-automation.md`
  **reference_log_3**: `docs/logs/log-S0D-4A-UI-layered-fix-notes.md`
**issue_keyword**: `inventory`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s6/evidence & drills, sub/1`
**issue_module_labels**: ``
**issue_milestone**: `road-S2`
**issue_parent**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/356`
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/_draft/road-S2-.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: `P2`
**roadmap_bridge_refs**: `S6B-1A -> road-S2 / M5 / P2`
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: `road-S2`
**pr_base**: `main`
**pr_development_issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/357`
**created**: `2026-04-04`
**updated**: `2026-04-04`

---

## Decision / Outcome

**Decision**:

- `S6B-1A` 的第一轮交付是 repo 级 evidence total table：先把当前证据面按 family 做成一份结构化 inventory ledger，而不是继续用口头印象描述“证据很多、很乱”。
- v1 盘点以 family-level 为主，不逐个枚举每个文件；优先记录“哪一类东西、落在哪、谁生成、保留意图是什么、operator 从哪里看”。
- 这份 inventory 直接服务于后续 `S6B/P2-P4`：retention policy、generator policy 与 bounded cutover 不能脱离当前 surfaces 直接空想。

**Default choices (phase defaults / v1)**:

- 先按当前真实仓库 surfaces 建账，不先设计理想目录。
- 先记录 major families 与 representative examples，不先追求每个单文件都入表。
- 当前 evidence total table 采用六类 taxonomy：`human-ledger`、`fact-source`、`retained-summary`、`workflow-derived`、`tmp-scratch`、`evidence-lite`。
- counts 只作为当前基线观察值，不作为长期 contract 字段；长期 contract 以 family、owner、retention 和 lookup path 为准。
- `P0/P1` 的 v1 交付必须同时保留 `family owner map`，避免 inventory 只回答“东西在哪”，却回答不了“谁对这类 surface 的 contract 负责”。

## Definitions (optional)

- `family-level inventory`: 以文件族或目录族为单位记账，而不是把每个单独 artifact 都列为一行。
- `owner map`: 记录哪个 log family、script family 或 workflow family 对该 surface 拥有 contract。
- `lookup path`: operator 最先应该去看的入口路径，不等于所有可能存放内容的路径。

## Constraints

- 不把 `docs/logs` 的 `Evidence` 区与 `docs/labs/_snapshot` 下的 run_dir 混为一类；前者是 ledger，后者才是 runtime fact-source。
- 不把 `docs/issues` 的 plan/manifest/apply-result 一律提升为 retained runtime evidence；它们默认是 docs/GitHub automation 派生产物。
- 不把所有 `_tmp_*` 目录都当作垃圾；v1 只标记为 `tmp-scratch`，后续再细分是否存在应升级为 retained lookup bundle 的少数例外。
- `UI evidence-lite` 保持独立记录，不强行并入 heavy track hard-gate taxonomy。

## Scope

- `P0`: inventory contract（表头、分类轴、counts 记录规则）
- `P1`: current evidence total table（当前 major surfaces、owner、retention、lookup path、family owner map）
- `P2`: retention/storage baseline + hotspot list（回答 major surfaces 哪些 retained、哪些 tmp，以及当前最明显的混放面）
- `P3`: generator/emission baseline（回答哪些 family 可以直接写 fact-source、哪些只能写 retained summary 或 workflow-derived output）
- `P4`: bounded cutover baseline（回答收口顺序、coexistence 规则、停止条件，以及哪些面现在不能先动）

## Success Criteria (DoD)

- 当前 repo 的主要 evidence surfaces 至少被收口为一份 family-level total table。
- 对每个 major family 至少能回答：`class`、`current surface`、`representative examples`、`generator/owner`、`retention intent`、`lookup path`。
- 至少记录一组当前 counts/scale baseline，帮助后续区分“主要面”和“尾部面”。
- 至少保留一版 `family owner map`，回答每类 surface 的主 contract owner 是哪条 log/script/workflow family。
- 至少明确回答 `artifacts`、`docs/issues`、`docs/labs/_snapshot` 三个 major surfaces 当前哪些应该 retained、哪些默认 tmp。
- 至少明确回答当前主要 script/workflow families 哪些允许直接产生 `fact-source`，哪些只允许产生 `retained-summary` 或 `workflow-derived` surface。
- 至少明确回答 cutover 的 rollout order、bounded coexistence 规则，以及什么情况下某个旧 surface 才允许停止继续写入。
- 至少识别出 3 个后续最值得治理的 hotspot，而不是只给出泛泛的目录批评。

## Stability (what stable means)

- This log can be marked `stable` when:
  - the first repo-level evidence total table is retained and accepted as the baseline inventory
  - downstream `S6B` work can reference this ledger directly instead of rerunning ad-hoc discovery each time

## PR Summary Inputs (optional)

**PR summary bullets**:

- Retain the first repo-level evidence inventory ledger across `human-ledger`, `fact-source`, `retained-summary`, `workflow-derived`, `tmp-scratch`, and `evidence-lite` surfaces.
- Fix the current retention and storage baseline so `artifacts`, `docs/issues`, and `docs/labs/_snapshot` no longer rely on one implicit evidence bucket.
- Record the current generator/emission policy and bounded cutover order so later `S6B` cleanup can reuse one stable owner-and-migration contract.

## P0 (Contract | v1)

### P0-C1-S1 (Inventory columns fixed | v1)

- v1 total table 统一使用以下列：
  - `class`
  - `current surface`
  - `representative examples`
  - `generator / owner`
  - `retention intent`
  - `lookup path`
  - `notes / current risk`

### P0-C1-S2 (Scale baseline rule fixed | v1)

- counts 只记录当前 snapshot，不进入长期 machine contract。
- v1 允许记录目录级和族级数量，例如：
  - `docs/issues`: 当前约 `720` 个 `.json` 与 `432` 个 `.md`
  - `artifacts/`: 当前顶层约 `61` 个目录与 `49` 个 `.json`
  - `docs/labs/_snapshot`: 当前顶层分为 `auto/` 与 `manual/`

### P0-C1-S3 (Family-level granularity fixed | v1)

- v1 不逐个列出每个 issue artifact、每个 run_dir 或每个 `_tmp_*` 目录。
- 同一类 surface 先按 family 入表，例如 `issue-conclusion-*`、`pr-prep-*`、`*runs.json`、`docs/labs/_snapshot/auto/*`。

### P0-C1-S4 (Primary owner discipline fixed | v1)

- 每类 surface 除了记录 generator，还必须记录 `primary contract owner`。
- `primary contract owner` 回答的是：当后续要判断保留策略、命名规则、lookup 入口或 cutover 边界时，默认应由哪条 log family 或 script/workflow family 负责。
- generator 与 owner 可以不同：例如 `docs/issues/*` 的具体文件由脚本生成，但其 contract owner 仍是 `S0E` 这条 docs/GitHub automation 线，而不是单个脚本文件本身。

## P1 (Current evidence total table | v1)

### P1-C1-S1 (Repo evidence total table retained | v1)

| class | current surface | representative examples | generator / owner | retention intent | lookup path | notes / current risk |
| --- | --- | --- | --- | --- | --- | --- |
| `human-ledger` | `docs/logs/*.md` | `log-S6A-evidence-drills-spine.md`, `log-S0E-docs-management-v5.md` | corresponding log owner slices | retained | start from the owning log or spine log | records headSha + artifact paths, but is not the raw machine fact-source |
| `fact-source` | `docs/labs/_snapshot/auto/**`, `docs/labs/_snapshot/manual/**` | `docs/labs/_snapshot/auto/S3A-2A-3A/<scenario>/<run_id>/`, `docs/labs/_snapshot/manual/_lab-S3A-2A-3A-expB/<run_id>/` | `backend/scripts/cli.py`, `backend/scripts/labs/*`, `cli_app/scenarios/*` | retained for actual drill/run evidence | start from `docs/labs/_snapshot/auto/` or the owning runbook/log | strongest runtime evidence surface; should not be confused with summary ledgers |
| `retained-summary` | `artifacts/*.json` summary and run ledgers | `s5b3a-runs.json`, `s5b4a-runs.json`, `s2d-runs.json`, `write_gate_runs.latest.json` | hard-gate scripts, CI collectors, projection/onboarding wrappers | retained | start from the named ledger file or owning log/runbook | low-cardinality history/index layer; currently mixed with tmp material in the same root |
| `workflow-derived` | `docs/issues/*` docs/GitHub automation outputs | `issue-conclusion-*`, `pr-prep-*`, `issue-relationship-*`, `lifecycle-audit-*`, `publish-verify-*` | docs/GitHub automation scripts and bounded replay tools | retained when they are the accepted workflow artifacts | start from the owning `S0E` log family and the matching file family | currently very large: about `720` `.json` and `432` `.md`; should not be mistaken for runtime drill evidence |
| `tmp-scratch` | `artifacts/_tmp_*`, `_local_*`, downloaded CI inspection bundles, extraction helpers | `_tmp_ci_run_*`, `_tmp_s4d4b_run_*`, `_tmp_pr_prep_*`, `_tmp_extract_*` | ad-hoc operator work, one-off scripts, CI downloads | temporary by default | start from the immediate investigation folder only | current largest ambiguity inside `artifacts/`; some bundles may later deserve bounded retained policy |
| `evidence-lite` | `docs/UI&UX/**` | `UI-FIX-20260313-*.md`, `assets/README.md` | UI fix-note process | retained, but separate from heavy drills flow | start from `docs/UI&UX/README.md` | intentionally separate from `_result.json` / hard-gate / CI artifact contract |

### P1-C1-S2 (Current scale baseline retained | v1)

- `docs/issues/` 当前族级规模：约 `720` 个 `.json`、`432` 个 `.md`。
- `docs/issues/` 当前最大文件族包括：
  - `issue-conclusion-*`: `373`
  - `pr-prep-*`: `202`
  - `pr-live-*`: `96`
  - `pr-body-*`: `88`
  - `issue-relationship-*`: `77`
  - `lifecycle-audit-*`: `72`
- `artifacts/` 当前顶层规模：约 `61` 个目录、`49` 个 `.json`、`10` 个 `.md`、`5` 个 `.txt`，另有少量 `.ps1`、`.graphql`、`.sh`。
- `docs/labs/_snapshot/` 当前顶层为 `auto/` 与 `manual/` 两个根。

### P1-C1-S3 (Family owner map retained | v1)

- 下表记录的是当前 repo 级 evidence surfaces 的 `primary contract owner`，用于回答后续 retention / naming / lookup / cutover 应优先找谁，而不是简单复述“文件是谁生成的”。

| class | family / surface slice | primary contract owner | current generator(s) | primary lookup path | notes |
| --- | --- | --- | --- | --- | --- |
| `human-ledger` | `docs/logs/*.md` parent / phase / spine logs | owning log family itself（如 `S0E`, `S2B`, `S2C`, `S2D`, `S3A`, `S4*`, `S5*`, `S6*`） | human-authored, sometimes tool-assisted | the owning log or parent spine log | ledger layer；记录 artifact path 与结论，但不是 raw fact-source |
| `fact-source` | `docs/labs/_snapshot/auto/**` | owning scenario/runbook/log family | `backend/scripts/cli.py`, `backend/scripts/labs/*`, `cli_app/scenarios/*` | the scenario run directory under `docs/labs/_snapshot/auto/` | strongest machine-facing run evidence；owner 不应退化成单个脚本路径 |
| `fact-source` | `docs/labs/_snapshot/manual/**` | the manual drill owner under the corresponding log/runbook | operator-managed manual capture | the specific run directory under `docs/labs/_snapshot/manual/` | manual track 仍是 fact-source，只是生成方式不同于 auto |
| `retained-summary` | top-level run ledgers such as `*runs.json`, `write_gate_runs.latest.json` | the owning hard-gate / projection / wrapper family | hard-gate scripts, CI collectors, projection/onboarding wrappers | the named retained ledger file | retained summary layer；不应与 `_tmp_*` 调查产物长期混放 |
| `workflow-derived` | `docs/issues/issue-*.md` and `issue-*.json` mirrors | `S0E` docs/GitHub automation family | `scripts/issues/*` generators and rewriters | the matching issue mirror path under `docs/issues/` | mirrors accepted workflow state，不等同于 runtime drill evidence |
| `workflow-derived` | `docs/issues/pr-prep-*`, `pr-live-*`, `pr-body-*`, `lifecycle-*`, `publish-verify-*` | `S0E` PR/lifecycle automation family | `scripts/issues/*`, GitHub write-back helpers, replay tools | the matching family under `docs/issues/` | workflow-derived retained outputs；主要服务 docs/GitHub automation replay 和审计 |
| `tmp-scratch` | `artifacts/_tmp_*`, `_local_*`, downloaded CI inspection bundles | the immediate operator/investigation that created the bundle | ad-hoc scripts, downloads, local extraction helpers | the immediate temp folder itself | default is temporary；除非后续被显式升级为 retained lookup bundle |
| `evidence-lite` | `docs/UI&UX/**` | UI fix-note process / UI owner slice | human-authored fix notes | `docs/UI&UX/README.md` | intentionally outside the heavy drill/hard-gate chain |

## P2 (Retention / storage baseline | v1)

### P2-C1-S1 (Class-to-retention baseline fixed | v1)

- `human-ledger`:
  - default retention: `retained`
  - default storage surface: `docs/logs/*.md`
  - reason: 这些文件是 operator-facing ledger，承担长期 lookup 和 narrative responsibility。
- `fact-source`:
  - default retention: `retained`
  - default storage surface: `docs/labs/_snapshot/auto/**`, `docs/labs/_snapshot/manual/**`
  - reason: 这是最强的 run/drill 事实源，不能按一次性 scratch 处理。
- `retained-summary`:
  - default retention: `retained`
  - default storage surface: named ledgers under `artifacts/` without `_tmp_` prefix
  - reason: 这些文件承担 low-cardinality history/index/summary 角色，应保留稳定 lookup path。
- `workflow-derived`:
  - default retention: `retained`
  - default storage surface: accepted workflow outputs under `docs/issues/*`
  - reason: 它们是 `S0E` docs/GitHub automation 的 replay/audit surface，不应默认视为 tmp。
- `tmp-scratch`:
  - default retention: `tmp`
  - default storage surface: `artifacts/_tmp_*`, `_local_*`, ad-hoc downloaded inspection bundles
  - reason: 这些内容服务于一次性调查或局部实验，除非被显式升级，否则不应视为长期 retained evidence。
- `evidence-lite`:
  - default retention: `retained`
  - default storage surface: `docs/UI&UX/**`
  - reason: 虽然不进入 heavy drill/hard-gate 主链路，但仍属于长期可追溯修复记录。

### P2-C1-S2 (Surface-specific policy fixed | v1)

- `artifacts/`:
  - `retained`: named ledgers and accepted summary surfaces such as `*runs.json`, `write_gate_runs.latest.json`, and other non-`_tmp_` summary/history files.
  - `tmp`: `_tmp_*`, `_local_*`, downloaded CI inspection bundles, one-off extraction outputs, ad-hoc replay scratch bundles.
  - current rule: 若文件名或目录名仍带 `_tmp_` / `_local_` 语义，则默认按 tmp 处理；若要长期保留，后续应升级为稳定命名 surface。
- `docs/issues/`:
  - `retained`: issue mirrors, issue conclusions, PR prep/live/body surfaces, lifecycle audit/gate outputs, publish-verify outputs, roadmap-bridge manifests/plans, and other accepted `S0E` workflow-derived files.
  - `tmp`: 当前不额外指定新的 tmp 子族；若未来出现一次性 scratch/replay 文件，应优先不要直接落在 `docs/issues/` retained surface 下。
  - current rule: 现有 `docs/issues/*` 默认视为 `workflow-derived retained outputs`，直到后续 cutover 明确拆出 tmp lane。
- `docs/labs/_snapshot/`:
  - `retained`: `auto/**` and `manual/**` run directories by default.
  - `tmp`: none by default inside the retained snapshot tree.
  - current rule: `docs/labs/_snapshot` 不承担 scratch lane；如果只是临时调查或下载物，应优先落在 `artifacts/_tmp_*` 而不是伪装成 snapshot run evidence。

### P2-C1-S3 (Operator storage decision shortcuts fixed | v1)

- 如果产物是单次 run/drill 的原始事实源：放到 `docs/labs/_snapshot/...`，默认 `retained`。
- 如果产物是人读的总结、结论、DoD 或 evidence ledger：写回 owning log 的 `docs/logs/*.md`。
- 如果产物是 docs/GitHub automation 的 mirror / prep / apply / audit / publish-verify surface：放到 `docs/issues/*`，默认 `retained`。
- 如果产物是 low-cardinality summary/history/index ledger：放到 `artifacts/` 的稳定命名文件，不要用 `_tmp_` 前缀。
- 如果产物只服务于一次性调查、下载、提取、局部重放：放到 `artifacts/_tmp_*` 或 `_local_*`，默认 `tmp`。

### P2-C1-S4 (Hotspot list retained | v1)

- Hotspot 1: `artifacts/` 根目录当前同时容纳 `retained-summary` 与 `tmp-scratch`，operator 很难仅凭目录层级区分长期 ledger 与一次性调查产物。
- Hotspot 2: `docs/issues/` 规模已足够大，但其默认身份仍容易被误读成“通用 evidence 仓”；实际上它更接近 docs/GitHub automation 的 workflow-derived retained outputs。
- Hotspot 3: `docs/logs` 中的 `Evidence` ledger 与 `docs/labs/_snapshot` 的 fact-source contract 已有明确分层，但 repo 级 vocabulary 还没把这两者公开收口为不同 family。
- Hotspot 4: `docs/issues/` 当前仍没有显式 tmp lane，因此若后续出现一次性 replay scratch 输出，必须避免直接混入 retained workflow surface。
- Hotspot 5: 少量历史/过渡路径仍留下旧 path 痕迹或 CI-only inspection bundle，后续 cutover 需要明确定义哪些例外允许 coexistence，哪些应回收。

## P3 (Generator / emission baseline | v1)

### P3-C1-S1 (Fact-source emission boundary fixed | v1)

- 允许直接写入 `fact-source` 的 family 仅限真正负责一次 run/drill capture 的执行链：
  - `backend/scripts/cli.py`
  - `backend/scripts/labs/*`
  - `cli_app/scenarios/*`
  - 对应 manual drill 的 operator-managed capture 流程
- 这些 family 如果直接产出 run evidence，目标 surface 必须是 `docs/labs/_snapshot/auto/**` 或 `docs/labs/_snapshot/manual/**`。
- 这类 direct emission 的 contract 是：
  - 产物必须按单次 run/drill 可回放地落在 run directory 下
  - 允许后续再派生 summary 或 log ledger，但不能只写 summary 而不保留最小 fact-source
  - 不得把一次 run 的原始事实源直接散落到 `docs/logs/`、`docs/issues/` 或 `artifacts/_tmp_*` 冒充 retained runtime evidence

### P3-C1-S2 (Retained-summary and workflow-derived emission boundary fixed | v1)

- 允许直接写入 `retained-summary` 的 family：
  - hard-gate scripts
  - CI collectors
  - projection / onboarding wrappers
  - 已接受的 low-cardinality history/index aggregators
- 这类 family 的目标 surface 应是 `artifacts/` 下稳定命名的 summary/history ledger，例如 `*runs.json`、`write_gate_runs.latest.json`，而不是 `_tmp_*` scratch path。
- 这类 retained-summary 允许只保留聚合结果，但前提是它们引用或对应的 raw fact-source 已存在于上游 run/drill surface；summary 本身不能冒充底层事实源。
- 允许直接写入 `workflow-derived` 的 family：
  - `scripts/issues/*`
  - GitHub write-back helpers
  - bounded replay / lifecycle audit tools
- 这类 family 的目标 surface 应是 `docs/issues/*`；它们服务于 docs/GitHub automation replay、apply、audit、publish-verify，不应直接产出 runtime fact-source。

### P3-C1-S3 (Naming and ownership expectations fixed | v1)

- 新 surface 在创建前至少要先回答三个 contract 字段：
  - `class`
  - `primary contract owner`
  - `target lookup path`
- 如果产物 intended to be `retained-summary` 或 `workflow-derived retained output`：
  - 名称不得继续使用 `_tmp_` / `_local_` 语义
  - 必须落在已有 retained surface 下，而不是先落临时目录再长期滞留
- 如果产物 intended to be `tmp-scratch`：
  - 应显式保留 `_tmp_` / `_local_` 语义
  - 不得放入 `docs/labs/_snapshot/**`、`docs/issues/*` 或稳定命名的 `artifacts/*.json` 中伪装成 retained surface
- 如果某个 family 想新增 retained surface：
  - 必须能被回挂到 owning log / spine log
  - 必须说明它取代的是哪类旧 lookup path，还是与旧 surface bounded coexistence
  - 若还回答不了 owner / lookup / retention，就默认先按 `tmp-scratch` 处理，而不是直接升级为 retained contract

## P4 (Bounded cutover baseline | v1)

### P4-C1-S1 (Rollout order fixed | v1)

- 当前 cutover 顺序固定为以下四段，而不是并行大清理：
  - Stage 1: 先固定 vocabulary 和 write discipline，只约束新产物不得继续扩大混放面。
  - Stage 2: 优先收口 `artifacts/` 根目录中的 `retained-summary` 与 `tmp-scratch` 命名边界，让 operator 能凭命名直接判断 retained 还是 tmp。
  - Stage 3: 再处理 `docs/issues/*` 的 bounded tmp lane 问题，只在确有 replay scratch 需求时定义独立 tmp surface，避免污染现有 retained workflow outputs。
  - Stage 4: 最后才讨论历史例外、旧 path 和 CI-only inspection bundle 的回收，不要求一次性清空旧目录。
- 这一定序的原因是：`artifacts/` 的混放风险最高、误判成本最低、且不依赖重开 `docs/issues` contract；而 `docs/issues` 与历史例外的收口都更依赖前面几轮 naming / generator discipline 已稳定。

### P4-C1-S2 (Bounded coexistence rules fixed | v1)

- cutover 期间允许 retained surface 与旧 surface bounded coexistence，但必须满足以下规则：
  - 新 retained surface 一旦启用，新的写入默认只能进入新 contract，不再继续向旧 surface 扩张。
  - 旧 surface 在 coexistence 期间仍可保留 lookup 价值，但不应继续承担“默认写入位置”的角色。
  - 任何 coexistence 必须能从 owning log / spine log 解释：新 surface 是替代谁，还是只是补充 lookup layer。
  - coexistence 允许存在历史只读例外，但不允许新增 `_tmp_` 内容伪装成 retained，也不允许新增 retained 内容继续占用旧 tmp 语义路径。
- `docs/labs/_snapshot/**` 当前不进入 cutover 迁移范围：它已被固定为 `fact-source` retained surface，现阶段重点是保护其 contract，不是重命名它。
- `docs/logs/*.md` 当前也不进入目录收口范围：它是 human-ledger layer，后续最多补回挂规则，不应被当作待搬迁的 artifact tree。

### P4-C1-S3 (Stop conditions fixed | v1)

- 某个旧 surface 只有同时满足以下条件，才允许停止继续写入或宣布完成收口：
  - 新 surface 的 `class`、`owner`、`lookup path` 已固定，并在 owning log / spine log 中可被明确引用。
  - 新 surface 已完成至少一轮真实写入，operator 不需要靠口头知识也能找到它。
  - 与旧 surface 对应的 generator/emission policy 已切换，不会在下一轮 run 或 workflow 中继续回写旧路径。
  - 若旧 surface 仍承担历史 lookup 价值，必须明确写成 read-only coexistence，而不是模糊地“先都保留着”。
- 若以上条件有任何一项未满足，则旧 surface 只能继续处于 bounded coexistence，不能强行宣称 cutover 完成。
- 当前 repo 级 stop-condition 结论是：
  - `artifacts/` 可进入第一优先级 bounded cleanup，但目前还未满足“新 retained-summary / tmp-scratch 命名边界被真实执行一轮”的 stop condition。
  - `docs/issues/*` 目前不应启动大规模路径 cutover；在没有明确 tmp lane contract 前，只应继续维持 retained workflow surface discipline。
  - `docs/labs/_snapshot/**` 与 `docs/logs/*.md` 当前不属于需要 cutover away 的对象，应视为需要保护 contract 的稳定 retained layers。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S6B-1A/P<phase>-C<cycle>-S<steps>: <summary>`

## Plan (draft)

### P1 (Current table)

- P1-C1-S1: retain the first repo-level evidence total table
- P1-C1-S2: retain current scale baseline and dominant file families

### P2 (Retention / storage baseline)

- P2-C1-S1: fix the class-to-retention baseline for the current evidence families
- P2-C1-S2: answer which current `artifacts`, `docs/issues`, and `docs/labs/_snapshot` surfaces are retained versus tmp
- P2-C1-S3: retain operator storage shortcuts for new surfaces
- P2-C1-S4: retain the hotspot list and hand it back to later cutover work

### P3 (Generator / emission baseline)

- P3-C1-S1: fix which current generator families may emit `fact-source` directly
- P3-C1-S2: fix which current generator families may only emit `retained-summary` or `workflow-derived` outputs
- P3-C1-S3: fix naming and ownership expectations for future retained versus tmp surfaces

### P4 (Bounded cutover baseline)

- P4-C1-S1: fix the bounded rollout order for current evidence-surface cleanup
- P4-C1-S2: fix coexistence rules so new retained surfaces do not keep expanding old paths
- P4-C1-S3: fix stop conditions for when an old surface may stop receiving writes

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: inventory columns fixed
- [x] `P0-C1-S2`: scale baseline rule fixed
- [x] `P0-C1-S3`: family-level granularity fixed
- [x] `P0-C1-S4`: primary owner discipline fixed

### P1 (Current table)

- [x] `P1-C1-S1`: repo evidence total table retained
- [x] `P1-C1-S2`: current scale baseline retained
- [x] `P1-C1-S3`: family owner map retained

### P2 (Hotspot list)

- [x] `P2-C1-S1`: class-to-retention baseline fixed
- [x] `P2-C1-S2`: surface-specific retained versus tmp policy fixed
- [x] `P2-C1-S3`: operator storage shortcuts fixed
- [x] `P2-C1-S4`: hotspot list retained

### P3 (Generator / emission baseline)

- [x] `P3-C1-S1`: fact-source emission boundary fixed
- [x] `P3-C1-S2`: retained-summary and workflow-derived emission boundary fixed
- [x] `P3-C1-S3`: naming and ownership expectations fixed

### P4 (Bounded cutover baseline)

- [x] `P4-C1-S1`: bounded rollout order fixed
- [x] `P4-C1-S2`: coexistence rules fixed
- [x] `P4-C1-S3`: stop conditions fixed

## Evidence (reserved)

- Artifacts are the source of truth for later machine-facing inventory artifacts; this log currently records the first bounded repo-level total table and hotspot list in human-facing form.
- This section should remain separate from any future retained inventory JSON.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

## Recent changes (for traceability, optional)

- 2026-04-04: opened `S6B-1A` as the first bounded follow-up under `S6B`, focused on retaining one repo-level evidence total table before any storage or cutover discussion widens.
- 2026-04-04: completed `P0/P1` v1 by formalizing the inventory columns, scale baseline, family-level granularity rule, and a first repo-level family owner map so later retention work has a concrete contract baseline.
- 2026-04-04: completed `P2` v1 in the same log by fixing the current class-to-retention baseline, answering retained versus tmp for `artifacts`, `docs/issues`, and `docs/labs/_snapshot`, and recording operator storage shortcuts for future surfaces.
- 2026-04-04: completed `P3` v1 in the same log by fixing which current generator families may emit `fact-source`, which may only emit `retained-summary` or `workflow-derived` outputs, and what naming/ownership contract new retained surfaces must satisfy.
- 2026-04-04: completed `P4` v1 in the same log by fixing the bounded rollout order, coexistence rules, and stop conditions for future evidence-surface cutover work.
