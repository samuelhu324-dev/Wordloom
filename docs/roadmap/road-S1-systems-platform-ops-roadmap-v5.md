# road-S1-systems-platform-ops-roadmap-v5

---

**id**: `road-S1`
**kind**: `roadmap`
**title**: `S1: Wordloom-v3 systems/platform & SaaS-grade ops roadmap (v5 spine)`
**status**: `draft`
**scope**: `S1`
**tags**: `ROADMAP, systems/platform, planning, v5, government-role`
**links**: ``
  **source**: `legacy/from_structured_docs/from-roadmap/ROADMAP v5.md`
  **child_road_1**: `docs/roadmap/road-S1-1-gov-role-minimal-ops-loop.md`
  **reference_log_1**: `docs/roadmap/road-template-main-roadmap.md`
**created**: `2026-03-21`
**updated**: `2026-03-29`

---

> 说明：这一份 `road-S1` 现在明确作为主线 roadmap 使用，承载长期 backbone；像 `road-S1-1` 这样的 focused branch road 可以突然出现、集中解决一段内容，但它完成的 child logs 仍然可以显式回流记入 `road-S1` 的主线 ledger，而不要求主线正文吸收全部 branch narrative。

## Positioning

**Context / role targeting（总路线视角）**

- `road-S1` 是围绕 wordloom-v3 的长期 systems/platform + SaaS 级产品能力主线。
- 它不只针对某一个岗位，而是覆盖：systems/platform ops、DevOps、平台工程、云工程、后端偏运行面的多种角色族。
- 所有 `road-S1-*`（例如 `road-S1-1` 政府岗最小闭环）都被视为从这条总路线中「抽出一段并做适配」。
- 在当前仓库资产的记账边界上，`road-S1` 应优先承接持续向前演进的 cloud/runtime 主心骨，也就是 `S4C`（cloud services / Terraform / cloud-dev infra）与 `S4D`（cloud runtime deploy / verify / rollback / semi-automated workflow）这两条主线。

**One-sentence goal**

- Build a long-term, SaaS-grade systems/platform ops backbone around wordloom-v3 that can be specialised into different role-focused sub-roadmaps.

## Scope & Audience

- **Primary audience**: 你自己（个人职业路线），以及未来需要了解你平台/运维能力的用人方；不限定在政府岗。
- **Time horizon**: 1–3 年的长期演进，可按 Milestone M* 分阶段前进。
- **Code base**: 以 `wordloom-v3` 为主，必要时可以扩展到 demo/sample 仓库，但总路线优先利用现有 S* spine 资产。
- **Current ownership boundary**: `road-S1` 主体记账应优先覆盖 `S4C + S4D + S4E` 这类继续向 SaaS-grade / cloud-runtime / release-governance 主心骨延伸的资产；像 `S4B` 的本地最小闭环与 `S5A-3B` 的 recovery sample，则更适合作为 `road-S1-1` 这类 role-focused 子路线的主完成面。

## Mainline / Branch Rules

- `road-S1` 是主线 road，负责保留长期 backbone 的 milestone 语言与完成面索引。
- `road-S1-1` 这类支线 road 可以在某个时间点突然出现，用来集中解决一个 focused detour，而不是改写主线的全部 narrative。
- 如果某个 child log 在支线里完成，但本质上也属于 `road-S1` 的一部分，那么 `road-S1` 的 bridge ledger 仍然要显式记住该 child log，并标注 `via road-S1-1`。
- 主线 ledger 的 canonical rows 仍然只能指向 child logs，而不是直接把 branch-road 文件当成完成项。

## Roadmap / Log Bridge Contract

- `road-S1` owns the long-running `M* / M*-P*` language.
- Child logs own implementation and evidence.
- Branch-road outputs may count back to the mainline, but only through explicit child-log mappings.
- `Evidence Pointers` remain supporting pointers only; they do not replace the bridge ledger.

## Branch Road Register

- `road-S1-1`: government-role minimal systems/platform ops loop
  - Why it exists: keep a short, interview-oriented minimal loop from flooding the mainline body.
  - Mainline slots it helps satisfy: `M1`, `M2`, parts of `M3`, parts of `M4`, and the minimal recovery/hybrid framing in `M5`.
  - Concentrated child logs: `S4A-*`, `S4B-*`, and `S5A-3B`.

## Environment strategy snapshot

- 本地 dev/test：继续保留单容器双数据库模式，`wordloom_dev` 面向日常开发，`wordloom_test` 面向 pytest、loadgen 和可销毁 drills。
- 云上样本：M3/S4C 当前先聚焦 `cloud-dev` 单库路径，用来证明 IaC、云上连通、迁移与最小 runtime smoke；不要求同步复制本地 test 环境。
- `cloud-test` 只有在需要云上 CI、共享测试环境或 staging-like drills 时才进入优先级；在此之前，应优先保持本地 test 的低成本与高可重建性。

## Milestone overview (M1–M5)

- **M1. Systems / platform operations language & narrative**
- **M2. Runtime baseline & automation（from-zero dev/test + scripts）**
- **M3. IaC & infrastructure primitives（Terraform + dev/test env → 云基础）**
- **M4. Runtime packaging, deploy / verify / rollback & observability basics**
- **M5. Backup / recovery, governance & hybrid/cloud framing + second-layer capabilities（K8s / multi-cloud 等）**

> 说明：这里的 M1–M5 同时充当「轴线」和「里程碑」：可以横向当作主题，也可以纵向当作阶段。子路线（S1-1 等）通常会从这里挑出 2–3 个 Milestone，做更细的 P0–P3 设计。

## Future capabilities & trigger conditions

> 说明：这一节与 M1-M5 平级，不表示“现在立刻都要做”；它的作用是说明哪些能力属于未来可能自然出现的扩展面，以及什么条件下才值得把它们拉进当前路线。默认策略仍是 `local-first, cloud-selective`，先把本地可重复、可验证、可审计的 operator path 跑稳，再把高价值样本放到云上。

### F1: Productionization automation（避免手工点操作的能力）

- **它是什么**：把 build、artifact tagging、deploy、post-change verify、rollback、evidence capture 从“人工 SSH + 手动命令”收口为脚本、CI/CD 或 GitOps 路径。
- **为什么会自然出现**：当同一条 deploy/verify/rollback 路径重复执行，且手工步骤已经开始成为时间成本、误操作风险和审计缺口时。
- **当前是否已触发**：`已触发`。`S4D` 已证明最小 cloud runtime operator path 可跑通，但也暴露出手工 SSH、镜像操作、verify rerun、结果抄录的效率问题。
- **下一步自然深化**：
  - 把当前 `S4D` 的 deploy / verify / rollback helper 继续收敛成单入口；
  - 为每次运行固定记录 `headSha`、image tag、env target、verify result、rollback result；
  - 后续优先补 CI/CD 或受控 operator workflow，而不是继续依赖纯手工 Ubuntu 操作。

### F2: Cloud service primitives（RDS / object storage / network boundary / IAM / TLS / LB）

- **它们是什么**：
  - `RDS`：托管数据库，减少自建数据库运维；
  - `object storage`：对象存储，如 S3/MinIO，用于备份、静态文件、归档；
  - `network ACL / security group`：网络访问边界控制；
  - `IAM`：身份与权限控制，定义谁能访问什么资源；
  - `TLS certificate`：HTTPS/加密通信所需证书；
  - `load balancer`：把流量分发到一个或多个后端实例，并承担健康检查、TLS 终止等职责。
- **为什么会自然出现**：当系统不再只是本地单机实验，而需要共享环境、真实网络边界、托管依赖、权限分层或更接近生产的访问路径时。
- **当前是否已触发**：`部分触发`。`S4C` / `S4D` 已真实触碰到 RDS、主机网络连通、安全组/IP allowlist；对象存储在 `S5A-3B` 已出现；IAM / TLS / LB 目前还未成为当前主线的阻塞条件。
- **学习策略**：先围绕当前已触发对象补最小闭环认知，再扩展到更完整的云治理模型，而不是一次性补全整套云平台。

### F3: Security / governance / failure taxonomy expansion

- **它是什么**：把“系统怎么坏、谁能做什么、失败后怎么判定和追溯”收敛成低基数 taxonomy、policy、audit、hard gate 与 operator evidence discipline。
- **为什么会自然出现**：当系统开始涉及多租户边界、权限差异、审计要求、真实发布/恢复路径时，failure taxonomy 就不再只是测试技巧，而会变成 verify gate、rollback trigger 和 forensics 的基础。
- **当前是否已触发**：`已触发`。`S5A` / `S5B` 已经把 AuthContext、tenant boundary、policy、audit、hard gate 做成稳定骨架；`S4D` 则把 deploy/verify/rollback failure surface 暴露到真实运行面。
- **当前关系判断**：你之前做的多租户、安全与审计工作，和现在问的 production verify / rollback / traceability 是直接相连的；两边的共同语言就是 contract、reason taxonomy、evidence 和 operator workflow。

### F4: Kubernetes / cluster orchestration

- **它是什么**：用于在多台机器上调度、更新、扩缩容和自愈大量容器化服务的控制平面。
- **什么时候才触发**：
  - 不再是单机或少量容器；
  - 需要多实例高可用；
  - 需要滚动发布、自愈、服务发现、统一调度；
  - `docker compose + 单机脚本` 已经明显吃力。
- **当前是否已触发**：`未触发`。wordloom-v3 当前更自然的重点仍是单机/小规模 runtime、IaC、verify/rollback、governance 与 evidence discipline。
- **当前策略**：Kubernetes 属于 M5 之后或 M5 内的 second-layer capability，不应早于 deploy/verify/rollback automation、failure taxonomy、cloud access boundary 基线。

### F5: Kafka / event streaming / asynchronous platform

- **它是什么**：面向高吞吐、异步解耦、重试、顺序、多个消费者协同的消息/事件流平台能力。
- **什么时候才触发**：
  - 系统有明显异步链路；
  - 单纯 DB/outbox/队列已经成为吞吐或解耦瓶颈；
  - 需要多个消费者独立订阅同类事件；
  - 需要处理重放、顺序、积压和消费组运维。
- **当前是否已触发**：`未触发`。现阶段更优先的是把现有 worker / outbox / evidence / hard-gate 思路继续打稳，而不是提前把 Kafka 作为主线能力。

### F6: Environment choice policy（local-first vs cloud-selective）

- **默认策略**：
  - 本地优先承担开发、破坏性 drill、快速故障注入与大部分验证；
  - 云上只承接本地无法真实模拟的高价值样本，如托管 RDS、网络边界、真实主机 deploy、共享环境、受控权限模型。
- **何时继续本地优先**：
  - 需要快速迭代脚本和 verify gate；
  - 需要低成本做 FAIL -> PASS drills；
  - 问题主要还在应用/runtime contract，而不是云边界。
- **何时提升云上优先级**：
  - 需要共享环境；
  - 需要验证真实网络/IAM/TLS/LB 行为；
  - 需要验证受控 deploy/rollback/operator workflow；
  - 需要更强审计和权限分层。

  ### F7: Runtime access path evolution（target access boundary from local-only to stable cloud path）

  - **它是什么**：把当前 release target 的访问路径从“依赖 operator 本机 local-only / NAT 转发”逐步演进到更稳定、更可自动化、边界更清晰的 runtime access model。
  - **为什么会自然出现**：当 `S4D` 的 stable runner 已经解决了 runner 位置、RDS reachability 与 GitHub Actions shell contract，但 release target 仍依赖本地 VirtualBox / NAT / 临时端口转发时，最后一跳 target access path 就会成为新的主 blocker。
  - **当前可选的三种方式**：
    - 方式 1：把 target 也迁到 cloud / VPC 内，用私网 IP 或 SG-to-SG 通信。
      - 定位：根因级长期方案。
      - 优点：最稳定、最适合自动化、最接近正式 SaaS / cloud runtime 边界。
      - 代价：迁移和环境改造成本最高。
    - 方式 2：给 target 一个 stable overlay network 地址，例如 Tailscale / WireGuard / ZeroTier。
      - 定位：介于本地与全云之间的长期折中方案。
      - 优点：不要求 target 立刻迁入 cloud/VPC，也能摆脱动态公网 IP allowlist 漂移。
      - 代价：要额外引入 overlay network 控制面与运维复杂度。
    - 方式 3：从 local-only target 反向连到 stable runner，建立 reverse tunnel bridge，再让 workflow 打 runner 上暴露出的 tunnel 入口。
      - 定位：最小改动、最快见效的 bridge 方案。
      - 优点：不要求立刻迁移 target；适合先补齐 stable-runner probe / dispatch evidence。
      - 代价：仍依赖 operator/local host 在线与 tunnel 存活，因此更像过渡桥，而不是终局架构。
  - **当前是否已触发**：`已触发`。
  - **当前完成状态**：
    - 方式 3 已完成最小 bridge 样本：`S4D-4C/P1-C3-S1S2` 已通过 reverse tunnel 把 local-only target 的 `127.0.0.1:22022` bridge 到 stable runner host，并把 stable-runner target SSH probe 从 `FAIL` 推到 `PASS`；
    - 方式 1 与方式 2 暂保留为未来演进项，等当前 `S4D` 的 reverse-tunnel-backed dispatch evidence 与 control-plane 收口稳定后，再决定是否继续上升到更长期的 access model。
  - **当前策略**：先把方式 3 作为当前 phase 的可验证 bridge，避免 `S4D` 被本地 NAT target 长期卡住；后续若这条 path 变成长期保留能力，再优先评估方式 1，其次方式 2。

### F8: Release governance implementation follow-through（把已定义的 release governance contract 继续压成仓库实现）

- **它是什么**：把 `S4E` 已完成的 release operating model / governance v1，继续落成仓库内可执行入口，例如 execution decision step、break-glass input contract、external approval decision write-back，以及必要时的 release ledger backend integration。
- **为什么会自然出现**：当 `S4E` 已经把 trigger policy、approval hierarchy、auditability、higher-environment blocking 和 execution-layer contract 固定下来之后，下一阶段最自然的问题不再是“怎么定义”，而是“这些定义如何进入 workflow/script/operator path”。
- **当前是否已触发**：`已触发`。`S4E` 已完成到 `S4E-5B` 并形成稳定 governance spine；当前剩余的是 implementation-oriented follow-up，而不是继续扩写 parent contract。
- **下一步自然深化**：
  - 在现有 release workflow 中增加 operator-visible execution decision step；
  - 在 workflow dispatch / runbook entry 中增加 break-glass input capture；
  - 若后续接入 external approval backend，只允许它增强 decision source，并要求最终 decision 继续回写到现有 governance action / evidence skeleton。

## Milestones (M1–M5)

> 每个 Milestone 内部沿用 phase-log 的 P0–P3 结构：P0 = contract，P1 = implementation，P2–P3 = drills / verification / wording。这里只给出「总路线」级别的框架，具体落地可以在子路线或 logs 中展开。

### M1: Systems / platform operations language & narrative

**Goal**

- 从 backend/platform 叙事升级到 systems/platform operations 叙事，能用 installation / configuration / maintenance / monitoring / backup / recovery / operational support / lifecycle management 等语言讲清楚 wordloom-v3。

**Bridge Ledger (child logs only)**

- `M1-P0`:
  - `docs/logs/log-S4A-1A-ops-scripting-baseline.md` via `road-S1-1`
- `M1-P1`:
  - `docs/logs/log-S4A-5A-operational-visibility-and-post-change-verification.md` via `road-S1-1`
- `M1-P2`:
  - `unmapped`
- `M1-P3`:
  - `unmapped`

**Plan (P0–P3)**

- `P0` Contract: 提炼一份 vocabulary + mapping note，把现有 S4A/S4B/S5A/S6A 资产映射到 systems/platform ops 语言。
- `P1` Implementation: 在 roadmap / logs / runbooks 中落地 1–2 页 cheatsheet 和若干重写过的 Decision / Outcome 段落。
- `P2` Drill: 设计并演练多种场景下的问答（政府岗、私企 DevOps、平台工程等），观察哪些叙事最自然。
- `P3` Drill: 把稳定的话术固化到 `docs/roadmap` 与 `docs/interview`，并在需要的 log 中加 reference。

### M2: Runtime baseline & automation（from-zero dev/test + scripts）

**Goal**

- 以 S4B-1A 为基座，维持一套可从零拉起 dev/test runtime 的脚本与 runbook（env_prep/start/status/health/backup 等），形成可重复、可验证的 automation 最小闭环。

**Bridge Ledger (child logs only)**

- `M2-P0`:
  - `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md` via `road-S1-1`
- `M2-P1`:
  - `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md` via `road-S1-1`
- `M2-P2`:
  - `docs/logs/log-S4B-1A-infra-as-code-and-runtime-packaging-baseline.md` via `road-S1-1`
- `M2-P3`:
  - `docs/logs/log-S4A-1A-ops-scripting-baseline.md` via `road-S1-1`

**Plan (P0–P3)**

- `P0` Contract: 定义「runtime baseline」和「from-zero drill」的标准字段（inputs、outputs、evidence 格式、headSha 等）。
- `P1` Implementation: 收敛并稳定 `scripts/` & `scripts/ops/`，确保有清晰入口和最小文档。
- `P2` Drill: 定期在 WSL/本机做 FAIL→PASS from-zero drill，并更新 evidence/artifacts。
- `P3` Drill: 在 roadmap 与 interview notes 中写出 operator-facing 版本的 runtime baseline 故事。

### M3: IaC & infrastructure primitives（Terraform + dev/test env → 云基础）

**Goal**

- 从 dev/test Terraform skeleton（devtest-db）出发，建立「基础设施定义 + 云基础能力」的长期主线，但不过早假装已是 production 级别。
- 在环境策略上，优先把 cloud sample 收敛为 `cloud-dev` 单库路径，而把破坏性 test/drill 主要留在本地 `wordloom_test`，避免过早引入双云库长期运营负担。

**Bridge Ledger (child logs only)**

- `M3-P0`:
  - `docs/logs/log-S4B-2A-infra-as-code-devtest-db-terraform-skeleton.md` via `road-S1-1`
- `M3-P1`:
  - `docs/logs/log-S4C-2A-cloud-devtest-db-and-storage.md`
- `M3-P2`:
  - `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`
- `M3-P3`:
  - `docs/logs/log-S4C-3A-cloud-devtest-wordloom-integration.md`

**Plan (P0–P3)**

- `P0` Contract: 写清楚 dev/test 与 prod 级别的边界，明确哪些资源只是教学/样本级别。
- `P1` Implementation: 在 `infra/terraform/` 下逐步丰富模块（DB、对象存储、网络等），始终保持简单、可解释。
- `P2` Drill: 定期执行 `init/validate/plan`（必要时加 apply 到本地/轻量云环境），并记录 evidence。
- `P3` Drill: 建立一套 IaC 能力的话术：从「最小样本」到「将来如何扩展到 multi-cloud / enterprise infra」。
- `P3` Extension note: 在 cloud connectivity 话题上，先掌握最小可解释路径（public endpoint + SG/IP allowlist），后续再补 bastion host / SSM port forwarding / 私网 RDS 访问模型。

**Current environment boundary note**

- 对 wordloom-v3 当前最合适的解释是：本地保留 dev/test 双库，云上先只做 `cloud-dev`；
- 这样既能展示真实云基础能力，也不会把 test 数据、破坏性 drills 和临时样本提前绑到长期保留的云资源上。
- 在主线归属上，这一部分的真实样本与后续扩展应继续记在 `S4C`，因为它承接的是 cloud services / Terraform / cloud-dev infra 的长期能力，而不是政府岗最小闭环本身。

### M4: Runtime packaging, deploy / verify / rollback & observability basics

**Goal**

- 让 wordloom-v3 的运行面不仅能在 dev/test 本机跑起来，还能用 Docker/compose/env/health 标准化打包，并且有 deploy → verify → rollback + 基本监控/日志的意识。
- 这条主线在后续由 `S4D` 承接到 cloud/staging deployable runtime，避免 `M4` 长期停留在本地运行基线。
- 当前 `M4` 的实际收口重点，已经不只是“能部署”，而是把 release workflow 中反复出现的 operator 失败面固定为 machine-verifiable gates、low-cardinality failure taxonomy 与结构化 evidence contract；像 `ssh user/key mismatch`、target reachability、dependency connectivity、release input contract、post-change verify、rollback readiness 这类问题，应优先在 `M4/S4D` 内被工程化消化，而不是继续停留在人肉 SSH 排障层面。

**Bridge Ledger (child logs only)**

- `M4-P0`:
  - `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md` via `road-S1-1`
- `M4-P1`:
  - `docs/logs/log-S4D-1A-cloud-runtime-release-path.md`
- `M4-P2`:
  - `docs/logs/log-S4D-2A-post-change-verification-and-operational-checks.md`
- `M4-P3`:
  - `docs/logs/log-S4D-3A-cloud-runtime-rollback-sample.md`

**Plan (P0–P3)**

- `P0` Contract: 定义「deployable runtime（dev/test）」的含义（镜像、配置、health、日志、回滚策略）。
- `P1` Implementation: 梳理 Dockerfile/compose/env 模板与 health/log 入口，确保与 S4B-1A 脚本协同。
- `P2` Drill: 至少完成一套「build → deploy to dev/test → smoke verify」的完整 drill，记录 artifacts 和问题复盘。
- `P3` Drill: 写出 rollback/fallback 的套路与示例，并在 S3A/S6A 等 log 中链接。

**Current completion focus**

- 对当前主线而言，`M4` 应直接把以下 release gates 视为完成面的一部分，而不是未来扩展项：
  - `operator identity / auth gate`：用户名、私钥、非交互 SSH 身份与 host trust 是否满足合同；
  - `target reachability gate`：target host、SSH 端口、远端 shell/docker/runtime prerequisites 是否可达；
  - `dependency connectivity gate`：Ubuntu VM 到 RDS / registry / object storage 等依赖面是否连通；
  - `release contract gate`：image tag、env file、required variables、known-good rollback inputs 是否齐全；
  - `post-change verify gate`：container running、migration、health、read smoke（必要时 write smoke）是否 PASS；
  - `rollback readiness gate`：known-good image/tag、rollback helper 与 rollback verify 入口是否存在。
- 上述 gates 的失败，不应只记为自由文本；它们应被压缩为低基数 failure classes，例如：`identity_auth_failure`、`target_reachability_failure`、`dependency_connectivity_failure`、`contract_validation_failure`、`deploy_execution_failure`、`verify_failure`、`rollback_failure`、`evidence_capture_failure`。
- `M4` 的 evidence 也应从“看日志/看截图”升级为结构化结果：至少固定 `headSha`、target、image tag、gate results、failure class、deploy/verify/rollback result 与 operator guidance。

**Next spine note**

- `M4` 的下一步主承接物是 `S4D`：把 `S4B` 的本地 packaging 基线与 `S4C` 的 cloud infra 连成一条 cloud/staging runtime 的 deploy -> verify -> rollback operator path。
- 因此在 roadmap 记账边界上，`S4D` 与其后续 control-plane / governance spine `S4E` 都应算作 `road-S1` 主心骨的一部分，而不是 `road-S1-1` 的完成面；`road-S1-1` 可以引用它们来说明“将来怎么往上长”，但不应把 `S4D/S4E` 的 cloud-runtime / release-governance 主线吞回最小闭环子路线。
- `F1` 中提到的 productionization automation 与 `F3` 中提到的 failure taxonomy / evidence discipline，在当前阶段不应只作为“触发条件说明”存在；只要它们直接服务于 `S4D` 的 deploy / verify / rollback operator path，就应优先记在 `M4` 当前完成面之内。
- `S4E` 现在已经完成了这一层 release operating model 升级：trigger surface policy、environment promotion、release governance、artifact/release records、approval hierarchy、higher-environment blocking 与 execution-layer enforcement 都已形成 v1 spine；因此 `M4` 当前不再把它视为候选扩展，而是视为已完成的 control-plane 闭环。
- 在此基础上，接下来仍属于 `road-S1` future-capability 的，是把 `S4E/P3` 固定的 execution decision step、break-glass input capture 与 external approval write-back 继续压成仓库实现；这部分优先记在 `F8`，而不是重新回到 parent 定义阶段。

### M5: Backup / recovery, governance & hybrid/cloud + second-layer capabilities

**Goal**

- 以 S5A-3B backup/restore/sanitize/verify 为核心，向外扩成一条「可治理、可恢复、具备 cloud/hybrid 认知」的长期线，包含但不急于完成 Kubernetes、多云等第二层能力。
- `M5` 的重点是把 release/runtime 基线继续外扩到更完整的 access boundary、governance、auditability、hybrid/cloud framing 与 second-layer platform capabilities；它不是当前 release workflow failure taxonomy 的第一归属地。

**Bridge Ledger (child logs only)**

- `M5-P0`:
  - `docs/logs/log-S4A-4A-hybrid-runtime-awareness.md` via `road-S1-1`
- `M5-P1`:
  - `docs/logs/log-S5A-3B-object-storage-backup.md` via `road-S1-1`
- `M5-P2`:
  - `docs/logs/log-S4E-4A-enforcement-auditability-and-environment-approver-policy.md`
- `M5-P3`:
  - `docs/logs/log-S4E-5B-execution-layer-enforcement-and-controlled-exceptions.md`

**Boundary note for completed `S4E`**

- `S4E` 当前已经完成 release operating model / governance v1，因此它在 `road-S1` 里的第一归属仍应视为 `M4`，因为它延续的是 deploy / verify / rollback / release-control-plane 这条 runtime operations 主线；
- `S4E` 中较强的 release governance / approval hierarchy / release records / cross-environment promotion 语义，说明它已经开始触碰 `M5` 的治理边界，但当前第一归属仍不是 `M5`；
- 因此现阶段更准确的写法不是把 `S4E` 继续当 future candidate，而是把它视为 `M4` 已完成的一段治理扩展，并把后续仓库实现压到 `F8` 这类 future capability 中。

**Plan (P0–P3)**

- `P0` Contract: 定义最小 cloud/hybrid 词汇与 scope（IAM/VPC/RDS/S3/CloudWatch basics 等），以及与 backup/recovery/治理的关联。
- `P1` Implementation: 写 mapping note，把现有 S5A/S5B/S2D 资产翻译成 governance / disaster readiness / recoverability narrative。
- `P2` Drill: 在现有 backup/recovery drill 基础上，加一层 cloud/hybrid 视角的解释（可以只是设计级别）。
- `P3` Drill: 为不同岗位族（政府岗、云工程、平台工程）准备 1–2 段稳定话术，说明如何从 dev/test → hybrid/cloud。
- `P3` Extension note: 在这一层逐步引入更安全的访问路径与边界控制，例如 bastion / EC2 jump host / SSM Session Manager / port forwarding，而不是长期依赖临时公网暴露。

## 与子路线的关系

- `road-S1-1-gov-role-minimal-ops-loop`：主要选取 M1–M5 中「对政府岗最直接命中」的一圈，做成 4–8 周的最小闭环。
- 当前更准确的边界是：`road-S1` 主体继续承接 `S4C + S4D + S4E` 这类 cloud/runtime/release-governance 主线，而 `road-S1-1` 主要承接 `S4B` 的最小 runtime / scripting / Terraform baseline，并吸收 `S4A` 的方法论语言与 `S5A-3B` 的 backup/recovery 样本。
- 未来可以新增：`road-S1-2`（例如偏云工程 / 多云）、`road-S1-3`（偏平台工程 / IDP）等，均从本文件的 M1–M5 中选子集并加细节。

## Recent Changes

- 2026-03-29: migrated `road-S1` to the mainline-road bridge-ledger format; branch-road outputs now count back through explicit child-log mappings marked `via road-S1-1` instead of prose-only references.
- 2026-03-27: `S4E` 已完成到 `S4E-5B` 并形成稳定的 release governance / execution-layer spine；当前已把它从 `road-S1` 中的“候选边界”改写为已完成主线，并新增 `F8 release governance implementation follow-through`，专门承接 execution decision step、break-glass input capture 与 external approval write-back 的后续实现。
- 2026-03-27: 已正式打开 `S4E` / `S4E-1A`，把更高一层的 release operating model、trigger policy 与 governance boundary 从 `S4D-4B/4C` 的后续讨论中提升为独立主线；当前在 `road-S1` 中仍以 `M4` 为第一归属。
- 2026-03-27: 明确补充 `S4E` 候选边界：若后续开启新 phase 承接更高一层的 release operating model，它在 `road-S1` 中通常先归 `M4`，只有上升到更完整的 release governance / cross-environment promotion / release records 制度时才开始同时触碰 `M5`；`F1/F3` 继续保留为触发条件说明，而不是主归属。
- 2026-03-26: 新增 `F7 Runtime access path evolution`，明确把 target access boundary 分成三种路径：全云/VPC、overlay network、reverse tunnel bridge；并记录当前已完成的是第 3 种桥接方案，第 1/2 种保留后续演进。
- 2026-03-25: 把当前 `S4D` 暴露出的 release gates / failure taxonomy / evidence discipline 明确下沉到 `M4` 完成面；`F1` 与 `F3` 继续保留为触发条件说明，但不再把这些内容误判为主要属于未来 `M5` 的话题。
- 2026-03-25: 新增 “Future capabilities & trigger conditions” 条目，明确 productionization automation、云服务基础、failure taxonomy、安全治理、Kubernetes、Kafka 与 local-first/cloud-selective 的触发条件，避免把未触发能力过早塞进当前主线。
- 2026-03-25: 明确 roadmap 记账边界：`road-S1` 主体优先承接 `S4C + S4D` 的 cloud/runtime 主线，而 `road-S1-1` 承接政府岗最小闭环中的 `S4B + S5A-3B` 与 `S4A` 方法论引用。