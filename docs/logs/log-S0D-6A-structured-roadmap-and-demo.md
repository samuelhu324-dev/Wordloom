# log-S0D-6A (Phase 6: Structured roadmap and demo containers)

---

**id**: `S0D-6A`
**kind**: `log`
**title**: `S0D-6A: Structured roadmap + demo containers + v1`
**status**: `stable`
**scope**: `S0D`
**tags**: `EVOLUTION, META, Docs, Roadmap, Demo, epic/S0D, sub/6A`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `docs/logs/log-S0D-epic.md`
  **previous_log**: ``
  **reference_log_1**: `docs/logs/_template-log-phase-drills-evidence.md`
**created**: `2026-03-21`
**updated**: `2026-03-21`

---

## Decision / Outcome

**Decision**:

- 对 roadmap 与 demo 相关资产做一次系统的“结构化容器”调整，形成后续可复用的骨架。
- 将 roadmap 拆分为“主路线 road-Sx-<summary> + 子路线 road-Sx-x-<summary>`，并引入统一模板；同时为 demo 引入分层目录和材料分类。

**Default choices (phase defaults / v1)**:

- roadmap 采用 `road-<Sx>-<summary>` 作为主路线 id，子路线采用 `road-<Sx>-<n>-<summary>`；两者都使用 Milestone (M*) + P0–P3 结构，而不是线性 Phase。
- 主路线优先描述长期能力轴线与 Milestone；子路线从主路线中抽取子集并对特定岗位/场景做适配。
- demo 采用 `docs/demo/demo-<id>/` 作为容器，内部使用 `_cv` / `_materials` / `_repo` / `_conversation` 等子目录按用途分层；具体子目录可演进，但尽量保持“对外材料 / 演示资产 / 源码镜像 / 对话记录”四个维度。
- ADR 旧资产不再作为一等公民结构，而是迁移到 `legacy/` 下以只读方式保留，其语义由 epic/phase logs 接管。

## Definitions

- **Structured roadmap**: 使用统一模板 (`road-template-structured-roadmap.md`) 与 Milestone (M1–M5) 结构，对长期学习/演化路线做文字化和可追踪的规划，而不是零散 v1–v5 文本。
- **Main road / Sub road**: main road `road-Sx-...` 描述长期主心骨；sub road `road-Sx-x-...` 描述针对特定角色/场景的子路线，选取 main road 的部分 Milestone 并加细节。
- **Structured demo**: 将 demo 视为一等公民容器，有固定目录结构与分类（CV、materials、repo 镜像、conversation），为后续自动化生成 CV、同步 README、对外展示页面等打基础。

## Constraints

- 不在本 phase 中实现 demo 自动化（视频录制流水线、CV 自动生成、vercel 自动部署等），仅做结构与归档；这些将由后续 logs 覆盖。
- 不在本 phase 中引入新的运行时依赖或 Infra，只移动/重构文档与 demo 资产。
- 尽量保持对旧路径的可追溯性（通过 legacy 目录和 log 记录），避免“文档凭空消失”。

## Scope

- `P0`: 为 roadmap 与 demo 定义结构化 contract（命名规则、目录结构、Milestone + P* 约定）。
- `P1`: 落地模板与具体实例：
  - 新建/更新 `road-template-structured-roadmap.md`、`road-001-...`、`road-001-01-...` 等；
  - 新建 demo 容器 `docs/demo/demo-001/` 下的 `_cv` 等子目录与 CV Markdown。
- `P2`: 基于当前仓库资产做一次“归类检查”（sanity check）：
  - roadmap：确认原 v1–v5 内容有去处（例如附录/legacy）；
  - demo：确认 CV PDFs 已有对应 Markdown 文本版本。
- `P3`: 收尾与归档：
  - 将旧 ADR 等资产归档到 `legacy/`；
  - 完成本日志与 S0D 分支上的一次 commit/push（按命名规范）。

## Success Criteria (DoD)

- 存在一份可复用的 roadmap 模板文件，并被至少一个 main road 与一个 sub road 采用（S1 / S1-1）。
- demo-001 有清晰的结构化目录和至少一份 CV demo 的 Markdown 版本，与 PDF 内容一致。
- 旧 ADR / roadmap v1–v4 等零散资产被明确迁移到 `legacy/` 或附录中，而不是散落在顶层。
- 本日志标记为 `stable`，并有一次对应的 S0D-6A commit/push 记账。

## Stability (what stable means)

- P0–P3 中定义的 contract、模板文件、demo 目录结构均已在当前仓库状态下落地。
- Evidence 区域记录了与本 phase 对应的一次 commit（通过 commit message 和分支名可追溯），后续如需调整以新的 phase/log 记录。

## P0 (Contract | v1)

### P0-C1-S1 (Roadmap structure contract)

- 主路线与子路线统一使用 `road-template-structured-roadmap.md` 提供的结构：Positioning / Scope & Audience / Milestone overview (M1–M5) / Milestones / Evidence pointers。
- 路线间通过 `links.parent_road` 与 `links.child_road_*` 字段建立父子关系。

### P0-C1-S2 (Demo container contract)

- 每个 demo 使用 `docs/demo/demo-<id>/` 作为根目录；
- 推荐子目录：
  - `_cv/`: 简历与工程补充材料（Markdown/PDF 等）；
  - `_materials/`: 演示脚本、投影片、笔记等；
  - `_repo/`: 与 demo 相关的代码仓库快照说明或子模块；
  - `_conversation/`: 与 demo 准备相关的 chat/export 记录；
- demo 的具体自动化（生成 CV、同步 README、页面与 vercel 管理）不在本 phase 完成，只在这里预留分类位置。

### P0-C1-S3 (Evidence contract | v1)

- 本 phase 的 evidence 主要来自：
  - roadmap/template/demo 目录本身的文件结构与内容；
  - 一次 S0D-6A 命名规范的 git commit，推送到 `S0D` 分支；
- 日志中记录该 commit 的 message 与分支名，便于通过 `git log --grep` 查找。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- 本 phase 推荐使用：`S0D-6A/P1-C1-S1: structured roadmap+demo v1` 作为首次 commit 前缀；后续如有补充，可使用 `S0D-6A/P1-C1-S2: ...` 等。

**Branch convention**:

- 所有与本 phase 相关的更改优先落在 `S0D-*` 分支上；当前具体使用 `S0D` 分支。

**Commit discipline (recommended)**:

- 完成本日志内容与对应文件结构调整后，立即在 `S0D` 分支上进行一次 commit/push，将本 phase 视为一个完整的 `P1-C1-S1` 单元。

## Plan (draft)

### P1 (Implementation)

- P1-C1-S1: 更新 roadmap 模板与 S1/S1-1 结构，统一为 Milestone + P* 结构。
- P1-C1-S2: 搭建 demo-001 容器与 `_cv` 目录，并从现有 PDF 提取两页 CV 为 Markdown。
- P1-C1-S3: 将旧 ADR 与早期 roadmap 文本迁移到 `legacy/` 或附录中。

### P2 (Drill / Verify)

- P2-C1-S1: 人工检查 roadmap 与 demo 目录结构，确保没有悬空引用或丢失内容。

### P3 (Wrap-up)

- P3-C1-S1: 编写本日志并在 `S0D` 分支上以 `S0D-6A/P1-C1-S1: structured roadmap+demo v1` 提交，随后 push。

## Execution Checklist

### P0 (Contract)

- [x] `P0-C1-S1`: 路线结构 contract 已在本日志中写明，并在 road-001 / road-001-01 中落地。
- [x] `P0-C1-S2`: demo 容器 contract 已在本日志中写明，并在 demo-001 中落地。
- [x] `P0-C1-S3`: evidence contract 已写明，将以本次 commit/push 为依据。

### P1 (Implementation)

- [x] `P1-C1-S1`: roadmap 模板与 S1 / S1-1 已按结构化路线重写。
- [x] `P1-C1-S2`: demo-001 `_cv` 目录与 `cv-001-backend-p1/p2.md` 已创建。
- [x] `P1-C1-S3`: 旧 ADR 与部分早期 roadmap 文本已迁移到 legacy/ 或附录。

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: 已人工检查主要文件与引用路径（road-001, road-001-01, demo-001, legacy/），无明显缺失。

### P3 (Wrap-up)

- [x] `P3-C1-S1`: 本日志已编写完毕并标记为 stable，对应的更改将通过一次 S0D-6A 命名的 commit/push 记录在 `S0D` 分支。

## Evidence

### P1-C1-S1 (Structured roadmap + demo containers | 2026-03-21)

- headSha: `<see git log for commit "S0D-6A/P1-C1-S1" on branch S0D>`
- branch: `S0D`
- artifacts:
  - `docs/roadmap/road-template-structured-roadmap.md`
  - `docs/roadmap/road-001-systems-platform-ops-roadmap-v5.md`
  - `docs/roadmap/road-001-01-gov-role-minimal-ops-loop.md`
  - `docs/demo/demo-001/_cv/cv-001-backend-p1.md`
  - `docs/demo/demo-001/_cv/cv-001-backend-p2.md`
  - `docs/roadmap/legacy/` 下的旧 ADR / roadmap 文本（如存在）
- expected:
  - roadmap 与 demo 有清晰结构，并可被后续 logs 复用；
  - 本日志被标记为 stable。
- observed:
  - 当前仓库状态满足上述结构要求，本日志已落地并准备随同本 phase 一起提交。

## Recent changes

- 2026-03-21: 初始化 S0D-6A，记录 structured roadmap 与 structured demo 容器的首个版本，并将本日志标记为 stable。
