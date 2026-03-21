# log-S4A-4A (Phase 4: Hybrid Runtime Awareness)

---

**id**: `S4A-4A`
**kind**: `log`
**title**: `hybrid runtime awareness (cloud fundamentals, config/secrets/logging, on-prem + cloud bridging) v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, Operations, HybridRuntime, Cloud, Logging, Config, Secrets, epic/s4, epic/s4a, sub/4a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md`
  **previous_log**: `docs/logs/log-S4A-3A-backup-recovery-operator-path.md`
  **reference_log_1**: `docs/logs/log-S5A-security-governance.md`
  **reference_log_2**: `docs/logs/log-S5B-security-governance-hard-gates.md`
  **reference_log_3**: `docs/logs/log-S6A-evidence-drills-spine.md`
**created**: `2026-03-21`
**updated**: `2026-03-21`

---

## Decision / Outcome

**Decision**:

- `S4A-4A` 把 `wordloom-v3` 目前已经具备的本地 runtime 能力（ops scripting、deploy safety、backup/recovery samples），向 cloud fundamentals 与 hybrid runtime 叙事延伸：
  - 明确 config / secrets / logging / metrics 在“本地 + 云”语境下的最小 operator 语义；
  - 给出一套 dev/test 级别的 hybrid runtime awareness 样本路径，而不是一整套 IDP 或云平台实现。
- 本 phase 不重新发明云基础设施，而是站在 systems/platform operations 视角，对现有 repo 中与 cloud / secrets / logging / observability 相关的资产进行归档与薄封装。

**Default choices (phase defaults / v1)**:

- 仍然优先 dev/test：只使用本仓库已有的 cloud hooks（如 logging, tracing, metrics, config/secrets integration）构造样本；
- 以 awareness 为主，不追求在本轮内落地完整的多云 runtime 管理；
- evidence 语义继续沿用 `S6A` drills/evidence 的风格：尽量使用低基数字段和可机械判定的 PASS/FAIL 结论。

## Constraints

- 不在本 phase 内设计新的云平台或配置系统；
- 不承诺在 6 天窗口内覆盖所有云产品面，只选取与本 repo 贴合度最高的几个 runtime 主题（logging / config/secrets / hybrid wiring）；
- 保持与 `S5A` / `S5B` 安全治理主题的边界：只做基础 runtime awareness，不替代安全策略或合规治理。

## Scope

- `P0`: contract / taxonomy（定义 hybrid runtime awareness 在本 repo 里的语义、边界与 evidence 口径）；
- `P1`: implementation / scaffolding（盘点现有 runtime 相关资产，定义 operator-facing entrypoints 或视角）；
- `P2`: drill / verify（选取 1~2 条样本路径，证明我们能在 dev/test 上对 hybrid runtime 做基本验证）；
- `P3`: docs / operator wording（将 hybrid runtime awareness 翻译成 systems/platform operations 语言，并视情况补 runbook）。

## Success Criteria (DoD)

- 至少定义一套 hybrid runtime awareness contract：
  - 说明哪些 runtime 维度（logging / config / secrets / tracing / metrics）在当前 repo 中是“可见的”；
  - 明确这些维度在 on-prem dev/test 与云/托管环境之间的差异与共性；
- 盘点出现有与 cloud/hybrid 相关的配置与代码入口，并在本 log 中以 operator 语言记录；
- 至少形成 1 条可复述的“hybrid runtime awareness sample path”，即：
  - operator 能够指出“某个场景在本地和云上的 runtime 行为差异在哪”；
  - 并知道去哪里看 log/config/secrets 来佐证该差异。

## Stability (what stable means)

- 本 log 标记为 `stable` 时：
  - `P0-P3` 的 hybrid runtime awareness 合同与样本路径已固定，不会频繁改写主语义；
  - Evidence 区至少记录 1~2 条可重复的 hybrid runtime awareness 样本；
  - 存在一个简单但清晰的 operator 视角，可以解释“本地 vs 云 / on-prem vs managed”在本 repo 里的 runtime 行为差异。

## P0 (Contract | v1)

### P0-C1-S1 (Hybrid runtime contract | v1)

- 对 operator 来说，本 phase 的核心问题是：
  - "这个系统在本地跑和在云里跑，runtime 上有哪些关键差异？"
  - "我在哪里查看日志、配置、密钥，以及它们在不同环境之间如何切换？"
  - "如果本地 OK、云上异常，我第一时间应该看什么？"
- v1 contract：
  - runtime 维度包括：logging, tracing, metrics（如有）, config, secrets；
  - S4A-4A 只负责说明这些维度在本 repo 中“通过什么方式接出去”（例如 env vars, config files, cloud SDK hooks），不设计新的运行时接口；
  - operator 只需要知道：
    - 在哪几个文件或目录可以看到与环境绑定的配置（例如 `.env.*`, deployment manifests, config modules）；
    - logging/tracing 的主出口与最低限度观察方法；
    - secrets 如何从本地 dummy 值切换到云端安全存储（只需要 awareness 级别，细节由 `S5A/S5B` 承担）。

### P0-C1-S2 (Evidence contract | v1)

- Evidence 以“可解释样本”为主，不强制所有检查都用 JSON drills 表达：
  - 可以采用“本地 vs 云 环境变量对比 snapshot”、“logging 配置对比”、“deployment manifest 片段”等轻量证据；
  - 若有必要，可在 `artifacts/` 下补充 `_tmp_s4a4a_*` 之类的辅助文件（如 config diff、log snippet 集合）。
- 最小 evidence 口径：
  - 记录至少 1 条场景：
    - 说明在 dev/test 本地与目标云/托管环境中，config/logging/secrets 的关键差异；
    - 给出查证步骤（例如“在本地看哪个日志文件，在云上看哪个 dashboard 或 log stream”）。

## Plan (draft)

### P1 (Implementation / scaffolding)

### P1-C1-S1 (Inventory hybrid-related assets | v1)

- 盘点本 repo 中与 hybrid runtime 相关的资产（初版列表，后续可在 P2/P3 迭代细化）：
  - 配置与环境：
    - `.env.*` 文件（如 `.env.dev`, `.env.test` 等）；
    - `docker-compose*.yml` 中关于服务端口、依赖、环境变量的定义；
    - 任意与 cloud/config 相关的 README 或 docs 段落（待在 P2 中具体引用）。
  - 日志与可观测性：
    - backend 中 logging/tracing 配置的入口（如 `logging` 模块、middleware、tracing 集成）；
    - docker-compose 或 runtime 配置中关于日志路径、log level 的设置；
  - 云 / 托管环境：
    - 若已有部署到云的脚本、manifest 或 CI 配置（如 `Procfile`, `docker-compose.infra.yml` 中的云依赖、任何 cloud provider-specific config），在此列出。

### P1-C1-S2 (Define operator-facing views | v1)

- 在本 phase log 中，以 operator 视角定义几个最小 hybrid runtime 视图：
  - `config & secrets view`：
    - 本地：说明 `.env.*` 如何为 dev/test 提供默认值；
    - 云端：说明这些值在云里通常对应哪个配置系统（环境变量、app settings 或 secrets 管理服务），仅 awareness；
  - `logging view`：
    - 本地：日志默认输出到哪里（container stdout / 挂载卷 / 文件）；
    - 云端：日志默认应该被哪类 collector 或 log service 接收；
  - `connectivity & dependency view`：
    - 本地：通过 docker-compose 把 DB / cache / object storage 拉起来；
    - 云端：这些依赖会对应到哪些云服务（例如 managed DB / managed cache），这里只做枚举与映射，不做实现。

### P1-C1-S3 (Seed evidence hooks | v1)

- 预留 evidence hooks：
  - 在后续 P2 中，可以通过以下方式产生最小样本：
    - 拍一份本地 `.env.dev` 与云配置的字段对照表；
    - 抽取一段本地 container 日志与云端 log stream 的样例；
    - 记录一次“本地 OK / 云上异常”的排查路径样本。
- 本阶段只在 log 中标记这些 hooks，不强制立即填满所有样本。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: hybrid runtime contract
- [x] `P0-C1-S2`: evidence contract

### P1 (Implementation / scaffolding)

- [x] `P1-C1-S1`: 盘点 hybrid runtime 相关资产
- [x] `P1-C1-S2`: 定义 operator-facing hybrid 视图
- [x] `P1-C1-S3`: 预留 evidence hooks

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: 至少 1 条 hybrid runtime awareness 演练样本

### P3 (Docs / Operator wording)

- [ ] `P3-C1-S1`: hybrid runtime wording 收口
- [ ] `P3-C1-S2`: （如有必要）runbook 草稿

## Evidence (reserved)

- 预留：后续 P2 阶段再补充具体样本与路径。

## Recent changes (for traceability, optional)

- 2026-03-21: scaffolded `S4A-4A` as the fourth `S4A` phase, focusing on hybrid runtime awareness across local dev/test and cloud/managed environments.
