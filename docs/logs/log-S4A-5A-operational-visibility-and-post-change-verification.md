# log-S4A-5A (Phase 5: Operational Visibility & Post-Change Verification)

---

**id**: `S4A-5A`
**kind**: `log`
**title**: `operational visibility & post-change verification (health, logs, drills, dashboards) v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, Operations, Observability, Monitoring, Health, Evidence, epic/s4, epic/s4a, sub/5a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4A-5A-operational-visibility-and-post-change-verification.md`
  **parent_log**: `docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md`
  **previous_log**: `docs/logs/log-S4A-4A-hybrid-runtime-awareness.md`
  **reference_log_1**: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  **reference_log_2**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_3**: `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`
**roadmap_path**: `docs/roadmap/road-S1-1-gov-role-minimal-ops-loop.md`
**roadmap_milestone**: `M1`
**roadmap_phase**: `M1-P1`
**roadmap_bridge_refs**: `docs/roadmap/road-S1-1-gov-role-minimal-ops-loop.md#M1-P1, docs/roadmap/road-S1-1-gov-role-minimal-ops-loop.md#M4-P3`
**created**: `2026-03-21`
**updated**: `2026-03-21`

---

## Decision / Outcome

**Decision**:

- `S4A-5A` 把 `wordloom-v3` 里已经存在的 health 脚本、deploy gate、failure drills、evidence JSON 和任何 dashboard 视图，统一收口成一条 "operational visibility & post-change verification" 路径。
- 本 phase 的目标是：当系统发生变更或出现异常时，operator 有一套可复述的视角和最小步骤，回答下面三个问题：
  - "现在这个系统健康吗？"
  - "最近一次变更之后，我怎么证明它仍然健康？"
  - "如果不健康，我第一时间应该去哪里看 log / evidence / drill 输出？"

**Default choices (phase defaults / v1)**:

- 一切围绕 dev/test 和 demo 场景，不假定已经有大规模集中式监控平台；
- 优先复用现有资产：`health.sh`、deploy gate 脚本、S3A/S6A 的 failure drills & evidence JSON，而不是新造一整套 observability stack；
- 继续坚持低基数字段、可机械判定的 PASS/FAIL 语义，让 operator 可以用很少的信息快速做出判断。

## Constraints

- 不在本 phase 内设计全新的监控平台或日志聚合系统，只做最小可用的视图和路径；
- 不承诺覆盖生产级 SLO/SLA/SRE 体系，仅在 dev/test 语境下提供样本和 operator journey；
- 与 `S5A/S5B` 的边界：本 phase 不负责安全/合规告警，只负责基础 runtime 健康和变更后的可见性。

## Scope

- `P0`: contract / taxonomy（定义 operational visibility & post-change verification 在本 repo 中的语义与边界）；
- `P1`: implementation / scaffolding（梳理和整理 health / logs / drills / dashboards 的入口与资产）；
- `P2`: drill / verify（选择 1~2 条“变更后验证 + 故障排查”样本路径，实际跑通并留下 evidence）；
- `P3`: docs / operator wording（将这些能力翻译成值班/运行支持可以直接使用的语言和 runbook）。

## P0 (Contract | v1)

### P0-C1-S1 (Operational visibility contract | v1)

- 对 operator 来说，本 phase 的核心问题是：
  - "在不依赖个人记忆的前提下，我如何快速判断系统当前是否健康？"
  - "我有哪些入口可以看到 health / logs / failure drills / dashboards？它们之间如何关联？"
- v1 contract：
  - 明确 `health.sh`、deploy gate、关键 HTTP `/health` 端点、failure drills dashboard 之间的关系；
  - 为 dev/test 和 demo 场景定义一个最小的 `health view`：
    - 至少包括：frontend、backend API、DB、ES（如有）、对象存储（如 MinIO）几个组件的状态；
    - 用简单的脚本或页面表达 OK/NOT OK，而不是复杂图表。

### P0-C1-S2 (Post-change verification contract | v1)

- 针对变更（代码变更 / 配置变更 /部署），本 phase 的问题是：
  - "变更之后，我如何证明系统仍然按预期工作？"
  - "哪些检查可以自动化，哪些需要人工 spot check？"
- v1 contract：
  - 复用 `S4A-2A` 的 deploy gate 和 `S3A/S6A` 的 failure drills，把它们视为 post-change verification 的一部分；
  - 要求每一条样本变更路径（例如 deploy、备份演练、hybrid 场景修复）都能指向：
    - 1 条自动化检查（脚本 / CI job / drill）；
    - 1 条人工 sanity check（例如访问 `/demo`、看一眼 dashboard）。

## Plan (draft)

### P1 (Implementation / scaffolding)

#### P1-C1-S1 (Inventory: health / logs / failure drills / dashboards | v1)

- health / status 脚本：
  - `scripts/ops/status.sh <env>`：给出当前 dev/test runtime 的轻量状态视图（`env_file`、`db_container`、`infra_es`、`api_health`、`worker_healthz`、`worker_readyz`、`ui_http`、`es_http`），不强制失败，只负责“快照式摘要”；
  - `scripts/ops/health.sh <env>`：在 devtest DB 未就绪、API/UI/ES HTTP 非预期或 worker 探针异常时直接 `exit 1` 的严格健康检查脚本，语义是“现在是否可以继续在这个 runtime 上做事情”；
- deploy gate：
  - `scripts/ops/deploy_app_verify.sh <env>`：封装一轮 post-deploy gate，串行调用 `status.sh` + `health.sh`，并输出低基数的 `POST_DEPLOY_RESULT=PASS|FAIL status_rc=<rc> health_rc=<rc>`；
- failure drills & evidence：
  - `backend/scripts/cli.py labs run|verify|export|clean <scenario>`：统一的 failure drills 入口，负责按场景触发/校验/导出；
  - `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md` + `docs/runbook/run-S3A-failure-drills-&-gitactions-&-dashboard.md`：记录具体场景、malfunction 以及证据包结构；
  - `docs/labs/_snapshot/auto/**`：由 labs harness 自动落盘的 `_recipe.json` / `_result.json` / metrics / logs / traces 等 evidence；
- 其他可视视图：
  - 健康 HTTP 端点：`/api/v1/health`（API）、`/` / `/demo`（UI/Vercel demo），在本 phase 视为人工 spot-check 的一部分，而非单独构建 dashboard；
  - 任何现有 Jaeger/metrics 面板仍由 S3A / S6A 负责维护，S4A-5A 只在需要时引用。

#### P1-C1-S2 (Dev/test "health summary" view | v1)

- v1 不额外造 UI，而是约定一套基于 `status.sh` + `health.sh` 的文字版 `health summary`：
  - `status.sh` 提供“当前环境有哪些组件、表面上是否在 responding”的快照；
  - `health.sh` 在关键依赖异常时直接 `exit 1`，给出更明确的 `[ops] ... unhealthy` 或 HTTP 异常行；
- 对 dev/test operator 来说，一个“健康”的最小视图可以用下面的组合来判断：
  - `scripts/ops/status.sh dev` 输出：
    - `db_container=healthy`
    - `infra_es=healthy`（如使用 infra ES）
    - `api_health` 为 `200`
    - `ui_http` 为 `200` 或 `30x`（本地 UI / Vercel demo 路由可访问）
    - `es_http` 为 `200`
    - 如果 `SEARCH_OUTBOX_WORKER_ENABLED=0`，可以看到一行 `worker runtime is disabled` 提示；
  - 紧接着 `scripts/ops/health.sh dev` 正常退出（exit code 0），且没有 `unhealthy` / `DOWN` / `unexpected HTTP` 一类错误行；
- 该组合即本 phase 的 `dev/test health summary view` v1：
  - 既可在本地终端手工运行，也可在 CI / 脚本里复用；
  - 不要求 operator 记住所有端口和 URL，只需要会跑 `status` + `health` 并读懂少数字段。

#### P1-C1-S3 (Post-change verification entrypoints | v1)

- 基于现有 phase 的入口，梳理 post-change verification 路径：
  - Deploy 相关（S4A-2A）：
    - `scripts/ops/deploy_app_verify.sh <env>`：对于任何一次本地 dev/test 代码或配置变更，视为默认的 post-change verification gate；
  - 备份/恢复演练（S4A-3A）：
    - S4A-3A 已经定义了从备份 → 上传对象存储 → restore → sanitize 的完整 pipeline drill，本 phase 将其视为“数据层变更后的 post-change verification 样本”；
  - Failure drills（S3A-2A-4B / S6A）：
    - 通过 `backend/scripts/cli.py labs run|verify` 触发的场景（例如 `es_write_block_4xx` 等），在本 phase 中被视为“故障注入后仍然需要回到健康状态”的扩展验证入口；
  - 关键路由 smoke test：
    - API：`curl http://127.0.0.1:<API_PORT>/api/v1/health`；
    - UI：`curl http://127.0.0.1:30002/` 或访问 `/demo`（本地或 Vercel demo）；
- v1 约定：
  - 任一重要变更后，至少要覆盖：`deploy_app_verify` + 一次轻量 HTTP smoke（API 或 UI）；
  - 若变更触及 DB/ES 或 outbox pipeline，则应额外挂一条 labs/failure drill 或 backup pipeline drill。

### P2 (Drill / Verify)

#### P2-C1-S1 (Post-change verification sample drill | v1)

- 目标：给出一条“变更后验证仍然为绿”的样本路径，复用 S4A-2A 已有 evidence，而不重新设计一套 gate。
- 样本选择：
  - 参考 `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md` 中的 happy path 演练：
    - 在 `dev` 环境完成 `env_prep` 和 app 启动；
    - 运行 `bash scripts/ops/deploy_app_verify.sh dev`；
    - 观察输出中包含 `phase=S4A-2A env=dev target_head_sha=<sha>` 与 `POST_DEPLOY_RESULT=PASS`；
  - S4A-5A 将该样本直接视为“变更后（或当前 headSha）通过 post-change verification gate”的 canonical 例子；
- Expected vs Observed（摘要）：
  - Expected：
    - `status.sh` 报告 DB/ES/HTTP 端点均为可接受状态；
    - `health.sh` 正常退出；
    - `deploy_app_verify` 输出 `POST_DEPLOY_RESULT=PASS` 并以 exit 0 结束；
  - Observed：
    - 与 S4A-2A phase log 中记录的 PASS 演练一致（包含具体 `headSha` 字段）；
- Operator takeaway：
  - 对于不涉及 DB schema 或 infra 结构的大部分改动（例如纯代码变更），只要 `deploy_app_verify` 在当前 head 上给出 PASS，就可以作为 dev/test 语境下的 post-change verification 证明；
  - S4A-5A 不新增新脚本，只是把这一条 gate 归类进“operational visibility & post-change verification” 故事里。

#### P2-C1-S2 (Failure → evidence/drill → diagnosis sample | v1)

- 目标：选取一条已经在 S3A-2A-4B 中记录过的故障样本，展示从“发现异常”到“读取 evidence / drill 输出定位根因”的完整链路。
- 样本选择：
  - 参考 `log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md` 中的 malfunction（例如 metrics 端口冲突或 `es_write_block_4xx` 配方缺失前置数据）：
    - 通过 `backend/scripts/cli.py labs run <scenario>` 触发场景；
    - 通过 `labs verify` 或 CI job 观察 FAIL 结果；
    - 查阅对应 `_result.json`、metrics 片段与 logs/traces，定位“为何本次 verify 判定为 FAIL”；
    - 修复配置（例如修正 metrics 端口、补充 `search_index` 前置数据），重新运行并观察 PASS；
- Expected vs Observed（摘要）：
  - Expected：
    - 初始 run/verify 报 FAIL，`_result.json` 明确 WHY 字段（如端口不可用、预期指标 delta 未发生等）；
    - 修复后再 run/verify 报 PASS，相关指标/日志与预期一致；
  - Observed：
    - 与 S3A-2A-4B malfunction 段落中记录的现象/修复路径一致；
- Operator takeaway：
  - 当 post-change verification 涉及复杂场景（如 ES 写入、collector down 等）时，应优先依赖 labs harness 和 evidence 包，而不是凭记忆手动 grep；
  - S4A-5A 的角色是把这类“failure drill + evidence 包”纳入统一的 operational visibility 视角，而不是重写具体场景实现。

### P3 (Docs / Operator wording)

#### P3-C1-S1 (Operator-facing wording | v1)

- 对外讲述时，可以用一条简单主线来概括 S4A-5A：
  - "在 dev/test 里，我不是只写了 health.sh，而是把 status/health/deploy gate 和 failure drills 收口成一条 operational visibility & post-change verification 路径：随时能回答三件事——现在健康不、这次改完之后还健康不、要查问题先去哪看。"
- 三个关键问题的岗位语言答案：
  - **Is the system healthy now?**
    - 运行 `status.sh` + `health.sh` 组合视图：
      - `status.sh` 给出 DB/API/UI/ES/worker 的快照状态；
      - `health.sh` 在关键依赖异常时直接 FAIL，给出低基数的 `OK/NOT OK` 信号；
  - **Did this change keep the system healthy?**
    - 把 `deploy_app_verify` 当作 dev/test 的 post-change verification gate：
      - 每次本地或 demo 级别的 deploy / 配置变更后，跑一遍 gate，看 `POST_DEPLOY_RESULT=PASS|FAIL`；
  - **If not, where do I look first?**
    - 优先看脚本输出和 evidence，而不是散落的日志：
      - 看 `deploy_app_verify` / `health.sh` 的 FAIL 行；
      - 对于更复杂的场景，转到 labs failure drills 的 `_result.json` + `_recipe.json` 与 logs/metrics/traces；
- 在面试或设计文档中，可以把 S4A-5A 和其他 phase 串成一句：
  - "S4A-1A 给了我可重复的启动脚本，S4A-2A 给了 post-deploy gate，S4A-3A 确保有备份/恢复路径，S4A-4A 让本地/云端行为有对齐，而 S4A-5A 则把这些入口收口成一条可以 day-2 运维和 post-change verification 的 operator journey。"

#### P3-C1-S2 (Runbook | v1)

- runbook 位置：`docs/runbook/run-S4A-5A-operational-visibility-and-post-change-verification.md`；
- 该 runbook 为值班/运行支持提供了一套最小化 checklist：
  - 变更前：
    - 可选地先跑一轮 baseline `status.sh` + `health.sh`，确认环境本身健康；
  - 变更后：
    - 按 S4A-1A/S4A-2A 启动 runtime；
    - 跑一轮 `status.sh` + `health.sh` 看 health summary；
    - 跑 `deploy_app_verify` 作为 post-change verification gate；
    - 必要时加一条与本次改动相关的 HTTP smoke（API `/api/v1/health` 或 UI `/`/`/demo`）；
  - 出现异常时：
    - 先看 `deploy_app_verify` / `health.sh` 的输出，确认是哪一类问题（容器 / HTTP / 配置）；
    - 若涉及 ES/collector/outbox 等复杂链路，则调用 labs failure drills，并通过 `_result.json` / `_recipe.json` / logs/metrics/traces 诊断；
  - 升级到 incident 流程的建议触发条件：
    - 多次 post-change verification FAIL 且在既有 runbook 中排查无果；
    - failure drills 持续 FAIL 且 evidence 包显示为 infra 级别问题（例如底层 ES/DB 不可恢复）。

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: operational visibility contract
- [ ] `P0-C1-S2`: post-change verification contract

### P1 (Implementation / scaffolding)

- [x] `P1-C1-S1`: inventory health/logs/drills/dashboards
- [x] `P1-C1-S2`: define dev/test health summary view
- [x] `P1-C1-S3`: map post-change verification entrypoints

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: post-change verification sample drill
- [x] `P2-C1-S2`: failure → evidence/drill → diagnosis sample

### P3 (Docs / Operator wording)

- [x] `P3-C1-S1`: operator-facing wording
- [x] `P3-C1-S2`: runbook (if needed)

## Evidence (v1)

- P2-C1-S1（post-change verification sample drill）：
  - 复用 S4A-2A phase log 中的 happy path 演练：
    - 环境：`dev`；
    - 入口：`bash scripts/ops/deploy_app_verify.sh dev`；
    - 结果：输出中包含 `phase=S4A-2A env=dev target_head_sha=<sha>` 与 `POST_DEPLOY_RESULT=PASS`；
  - 解释：在 dev/test 语境下，该样本证明“当前 head 上，通过唯一一条 post-deploy verification gate 可以确认 runtime 仍然健康”；
- P2-C1-S2（failure → evidence/drill → diagnosis sample）：
  - 复用 S3A-2A-4B 中已记录的 malfunction 与 labs evidence 包（如 metrics 端口冲突或 `es_write_block_4xx` 配方缺失前置数据）；
  - 解释：通过 `labs run/verify` + `_result.json` + logs/metrics/traces，定位故障根因并修复后重新获得 PASS，形成一条“从异常到修复”的完整链路；

## Recent changes (for traceability, optional)

- 2026-03-21: scaffolded `S4A-5A` as the fifth `S4A` phase, focusing on operational visibility and post-change verification on top of the existing runtime spine.
