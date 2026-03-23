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
**created**: `2026-03-21`
**updated**: `2026-03-21`

---

> 说明：这一份 road-S1 作为「总路线」模板，可以被以后其他 `road-Sx` 复用。它用统一的 Milestone（M*）+ Phase（P0–P3）结构来描述长期能力路线；具体针对某个岗位或场景的子路线（例如 `road-S1-1`）则继续沿用 `road-template-structured-roadmap.md` 的子路模板，在这条总路线之下选取和裁剪。

## Positioning

**Context / role targeting（总路线视角）**

- `road-S1` 是围绕 wordloom-v3 的长期 systems/platform + SaaS 级产品能力主线。
- 它不只针对某一个岗位，而是覆盖：systems/platform ops、DevOps、平台工程、云工程、后端偏运行面的多种角色族。
- 所有 `road-S1-*`（例如 `road-S1-1` 政府岗最小闭环）都被视为从这条总路线中「抽出一段并做适配」。

**One-sentence goal**

- Build a long-term, SaaS-grade systems/platform ops backbone around wordloom-v3 that can be specialised into different role-focused sub-roadmaps.

## Scope & Audience

- **Primary audience**: 你自己（个人职业路线），以及未来需要了解你平台/运维能力的用人方；不限定在政府岗。
- **Time horizon**: 1–3 年的长期演进，可按 Milestone M* 分阶段前进。
- **Code base**: 以 `wordloom-v3` 为主，必要时可以扩展到 demo/sample 仓库，但总路线优先利用现有 S* spine 资产。

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

## Milestones (M1–M5)

> 每个 Milestone 内部沿用 phase-log 的 P0–P3 结构：P0 = contract，P1 = implementation，P2–P3 = drills / verification / wording。这里只给出「总路线」级别的框架，具体落地可以在子路线或 logs 中展开。

### M1: Systems / platform operations language & narrative

**Goal**

- 从 backend/platform 叙事升级到 systems/platform operations 叙事，能用 installation / configuration / maintenance / monitoring / backup / recovery / operational support / lifecycle management 等语言讲清楚 wordloom-v3。

**Plan (P0–P3)**

- `P0` Contract: 提炼一份 vocabulary + mapping note，把现有 S4A/S4B/S5A/S6A 资产映射到 systems/platform ops 语言。
- `P1` Implementation: 在 roadmap / logs / runbooks 中落地 1–2 页 cheatsheet 和若干重写过的 Decision / Outcome 段落。
- `P2` Drill: 设计并演练多种场景下的问答（政府岗、私企 DevOps、平台工程等），观察哪些叙事最自然。
- `P3` Drill: 把稳定的话术固化到 `docs/roadmap` 与 `docs/interview`，并在需要的 log 中加 reference。

### M2: Runtime baseline & automation（from-zero dev/test + scripts）

**Goal**

- 以 S4B-1A 为基座，维持一套可从零拉起 dev/test runtime 的脚本与 runbook（env_prep/start/status/health/backup 等），形成可重复、可验证的 automation 最小闭环。

**Plan (P0–P3)**

- `P0` Contract: 定义「runtime baseline」和「from-zero drill」的标准字段（inputs、outputs、evidence 格式、headSha 等）。
- `P1` Implementation: 收敛并稳定 `scripts/` & `scripts/ops/`，确保有清晰入口和最小文档。
- `P2` Drill: 定期在 WSL/本机做 FAIL→PASS from-zero drill，并更新 evidence/artifacts。
- `P3` Drill: 在 roadmap 与 interview notes 中写出 operator-facing 版本的 runtime baseline 故事。

### M3: IaC & infrastructure primitives（Terraform + dev/test env → 云基础）

**Goal**

- 从 dev/test Terraform skeleton（devtest-db）出发，建立「基础设施定义 + 云基础能力」的长期主线，但不过早假装已是 production 级别。
- 在环境策略上，优先把 cloud sample 收敛为 `cloud-dev` 单库路径，而把破坏性 test/drill 主要留在本地 `wordloom_test`，避免过早引入双云库长期运营负担。

**Plan (P0–P3)**

- `P0` Contract: 写清楚 dev/test 与 prod 级别的边界，明确哪些资源只是教学/样本级别。
- `P1` Implementation: 在 `infra/terraform/` 下逐步丰富模块（DB、对象存储、网络等），始终保持简单、可解释。
- `P2` Drill: 定期执行 `init/validate/plan`（必要时加 apply 到本地/轻量云环境），并记录 evidence。
- `P3` Drill: 建立一套 IaC 能力的话术：从「最小样本」到「将来如何扩展到 multi-cloud / enterprise infra」。
- `P3` Extension note: 在 cloud connectivity 话题上，先掌握最小可解释路径（public endpoint + SG/IP allowlist），后续再补 bastion host / SSM port forwarding / 私网 RDS 访问模型。

**Current environment boundary note**

- 对 wordloom-v3 当前最合适的解释是：本地保留 dev/test 双库，云上先只做 `cloud-dev`；
- 这样既能展示真实云基础能力，也不会把 test 数据、破坏性 drills 和临时样本提前绑到长期保留的云资源上。

### M4: Runtime packaging, deploy / verify / rollback & observability basics

**Goal**

- 让 wordloom-v3 的运行面不仅能在 dev/test 本机跑起来，还能用 Docker/compose/env/health 标准化打包，并且有 deploy → verify → rollback + 基本监控/日志的意识。
- 这条主线在后续由 `S4D` 承接到 cloud/staging deployable runtime，避免 `M4` 长期停留在本地运行基线。

**Plan (P0–P3)**

- `P0` Contract: 定义「deployable runtime（dev/test）」的含义（镜像、配置、health、日志、回滚策略）。
- `P1` Implementation: 梳理 Dockerfile/compose/env 模板与 health/log 入口，确保与 S4B-1A 脚本协同。
- `P2` Drill: 至少完成一套「build → deploy to dev/test → smoke verify」的完整 drill，记录 artifacts 和问题复盘。
- `P3` Drill: 写出 rollback/fallback 的套路与示例，并在 S3A/S6A 等 log 中链接。

**Next spine note**

- `M4` 的下一步主承接物是 `S4D`：把 `S4B` 的本地 packaging 基线与 `S4C` 的 cloud infra 连成一条 cloud/staging runtime 的 deploy -> verify -> rollback operator path。

### M5: Backup / recovery, governance & hybrid/cloud + second-layer capabilities

**Goal**

- 以 S5A-3B backup/restore/sanitize/verify 为核心，向外扩成一条「可治理、可恢复、具备 cloud/hybrid 认知」的长期线，包含但不急于完成 Kubernetes、多云等第二层能力。

**Plan (P0–P3)**

- `P0` Contract: 定义最小 cloud/hybrid 词汇与 scope（IAM/VPC/RDS/S3/CloudWatch basics 等），以及与 backup/recovery/治理的关联。
- `P1` Implementation: 写 mapping note，把现有 S5A/S5B/S2D 资产翻译成 governance / disaster readiness / recoverability narrative。
- `P2` Drill: 在现有 backup/recovery drill 基础上，加一层 cloud/hybrid 视角的解释（可以只是设计级别）。
- `P3` Drill: 为不同岗位族（政府岗、云工程、平台工程）准备 1–2 段稳定话术，说明如何从 dev/test → hybrid/cloud。
- `P3` Extension note: 在这一层逐步引入更安全的访问路径与边界控制，例如 bastion / EC2 jump host / SSM Session Manager / port forwarding，而不是长期依赖临时公网暴露。

## 与子路线的关系

- `road-S1-1-gov-role-minimal-ops-loop`：主要选取 M1–M5 中「对政府岗最直接命中」的一圈，做成 4–8 周的最小闭环。
- 未来可以新增：`road-S1-2`（例如偏云工程 / 多云）、`road-S1-3`（偏平台工程 / IDP）等，均从本文件的 M1–M5 中选子集并加细节。