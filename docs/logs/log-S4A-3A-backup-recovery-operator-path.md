# log-S4A-3A (Phase 3: Backup / Recovery / Disaster Readiness Operator Path)

---

**id**: `S4A-3A`
**kind**: `log`
**title**: `backup / recovery / disaster readiness operator path + drills/evidence v1`
**status**: `stable`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, Operations, Backup, Recovery, DisasterReadiness, Drills, Evidence, epic/s4, epic/s4a, sub/3a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4A-3A-backup-recovery-operator-path.md`
  **parent_log**: `docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md`
  **previous_log**: `docs/logs/log-S4A-2A-deploy-verify-rollback-runtime-path.md`
  **reference_log_1**: `docs/logs/log-S5A-3B-object-storage-backup.md`
  **reference_log_2**: `docs/logs/log-S6A-evidence-drills-spine.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
**created**: `2026-03-21`
**updated**: `2026-03-21`

---

## Decision / Outcome

**Decision**:

- `S4A-3A` 把现有的 backup / restore / object-storage drills 翻译成一条面向 systems/platform operations 岗位的本地备份与恢复 operator path，聚焦 dev/test 环境的运行支撑与灾备准备（disaster readiness）。
- 本 phase 不重新发明新的 backup 平台，而是站在 operator 视角，把 `S5A-3A` / `S5A-3B` / `S6A` 的资产收口成“如何在本地 dev/test 确认 backup 做过、能恢复、能演练”的故事。

**Default choices (phase defaults / v1)**:

- 优先 dev/test：仅覆盖本仓库 dev/test 语境下的 DB / artifacts 备份与恢复样本，不扩展到生产级多区域灾备方案。
- evidence 语义沿用 `S5A-3B` + `S6A`：保留 drills/evidence JSON 的 PASS/FAIL 语义，字段尽量低基数，可机械判定，便于未来接入 hard gate。
- 不引入数据级复杂度：v1 不尝试解决所有数据脱敏、跨环境复制问题，而是先保证“本地有一条可复跑的 backup+restore drill，且 operator 能看懂”。

## Definitions (optional)

- **Backup artifact**：由 `S5A-3A` / `S5A-3B` 产生的 dump 文件与配套 manifest/evidence JSON，不入 git 的 dump、本地或对象存储中的文件。
- **Restore drill**：从 backup artifact 恢复到指定 dev/test 数据库，并通过 SQL / health 检查验证成功的过程。
- **Disaster readiness**：在 dev/test 语境下，证明“即便当前 DB 损坏，仍能从最近一次 backup 恢复到可用状态”的能力；本 phase 不涵盖生产级 RPO/RTO 规划，只讲样本与演练路径。

## Constraints

- 不在本 phase 内重新设计 `S5A-3B` 对象存储 contract；以引用和复用为主。
- 不把 dump 文件纳入 git；仍然通过 `artifacts/` 与对象存储（MinIO/S3 兼容）管理大体量文件。
- 不引入复杂多租户或跨 region 场景；所有样本以本地 docker-compose + MinIO dev/test 为基础。

## Scope

- `P0`: contract（backup/recovery operator 语义、最小 evidence 口径、与 S5A-3B 的接口）
- `P1`: implementation / scripts（把现有 backup/restore drills 对 operator 暴露为最小脚本或命令入口）
- `P2`: drill / verify（至少 1 条 backup+restore+verify path，可在 dev/test 上复跑）
- `P3`: docs / operator wording（将 backup/recovery 链路翻译成 systems/platform operations 语言，补 runbook）

## Success Criteria (DoD)

- 至少定义 1 条典型的 `backup -> store (local or object storage) -> restore -> verify` 路径，并在本 log 中记录 expected/observed 摘要。
- 至少形成 1 套可机械判定的 backup+restore drill evidence（例如基于 `S5A-3B` drills JSON）。
- 明确 operator-facing wording：能用 `backup / restore / disaster readiness / evidence` 语言解释当前能力边界。
- 起草一份 runbook，指引值班/运行支持在 dev/test 语境下确认 backup 状态和执行一次恢复演练。

## Stability (what stable means)

- 本 log 标记为 `stable` 时：
  - `P0-P3` 的 backup/recovery contract、入口脚本与 drills 已稳定，并且不会因后续小调整频繁改写主语义；
  - Evidence 区至少记录 1~2 条成功的 backup+restore 演练样本（包含 headSha + artifact 路径 / CI run URL）；
  - 存在一个可复跑的 operator 路径，用于在 dev/test 上验证“最近一次 backup 能成功恢复”。

## P0 (Contract | v1)

### P0-C1-S1 (Backup/recovery operator contract | v1)

- 对 operator 来说，本 phase 的主问题是：
  - "最近一次备份在哪里？"
  - "如果当前 DB 损坏，我该跑什么命令把它恢复回来？"
  - "我如何证明这条路径最近确实演练过？"
- v1 contract：
  - backup artifact 入口：指向 `S5A-3B` 的对象存储 bucket/key 与本地 `artifacts/` 中的 evidence JSON；
  - restore/verify 入口：沿用现有 `S5A-3B` pipeline drill 或其拆分脚本；
  - operator 只需要知道：在哪个 phase log / runbook 里能找到这些入口，以及如何复跑一次 drill。

### P0-C1-S2 (Evidence contract | v1)

- Evidence 以 `S5A-3B` drills JSON 为基础，S4A-3A 只补充：
  - 与 backup/recovery operator path 相关的 `headSha`；
  - 简要的 `backup_kind`（local dump / object storage）、`restore_target`、`verify_result` 摘要；
  - 在本 log 的 Evidence 区记录 `artifacts/_tmp_s5a3b_*` 等 JSON 路径，以便 operator 追溯。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4A-3A/P<phase>-C<cycle>-S<steps>: <summary>`，其中 `<steps>` 可以是单个 step（`1`）或同一 phase / cycle 下连续 steps 的组合（如 `1S2`）。

**Branch convention**:

- `S4A-3A` 相关实现与文档默认仍落在 `S4A-systems-platform-operations-runtime-foundation` 分支；如有必要，可在其下开短生命周期子分支。

**Commit discipline (recommended)**:

- 每完成一个有明确边界的 `P*-C*-S*` 单元，应尽量及时 `commit/push` 到 `S4A-systems-platform-operations-runtime-foundation`。

## Plan (draft)

### P1 (Implementation / scripts)

### P1-C1-S1 (Existing backup/restore entrypoints | inventory)

- 本地脚本与 drills 层：
  - `scripts/drills/s5a3a_p1c1s2_backup_drill.py`：生成 dev/test 数据库 dump，并在 `artifacts/_tmp_s5a3a_*` 下写入 backup evidence JSON，记录 dump 文件路径等元数据；
  - `scripts/backup/s5a3b_p1c1s2_upload_dump_to_minio.ps1`：将本地 dump 上传至 MinIO（S3 兼容），生成 manifest JSON（bucket/key/sha256/size 等）；
  - `scripts/drills/s5a3b_p1c1s3_upload_drill.py`：Python 层 upload drill，封装 PowerShell upload 脚本并产出上传 evidence JSON；
  - `scripts/backup/s5a3b_p2c1s1_download_dump_from_minio.ps1`：从 MinIO 下载指定 dump 到本地临时路径；
  - `scripts/drills/s5a3b_p2c1s2_restore_verify_from_minio_drill.py`：下载 → restore 到 `wordloom_restore_dev` → verify 的 drill；
  - `scripts/drills/s5a3b_p3c1s2_restore_sanitize_verify_from_minio_drill.py`：下载 → restore 到 `wordloom_restore_sanitized_dev` → sanitize + verify 的扩展 drill；
  - `scripts/drills/s5a3b_p4c1s1_pipeline_drill.py`：一键 pipeline drill，串联 backup → upload → restore+verify → restore+sanitize+verify，并在 `artifacts/_tmp_s5a3b_p4c1s1` 下生成汇总 evidence JSON（包含 bucket/object_key/sha256/size 与 verify 结果）。
- Evidence 与 artifacts：
  - 所有上述 drills 的 evidence JSON 均存放于 `artifacts/_tmp_s5a3a_*` / `artifacts/_tmp_s5a3b_*` 目录下，详细结构见 `log-S5A-3B` Evidence 区；
  - dump 文件本身不会入 git，而是存储在本地磁盘与 MinIO 对象存储中，由 manifest/evidence JSON 提供可追溯性。

### P1-C1-S2 (Minimal operator entry set | design)

- 为 systems/platform operations operator 定义最小入口集合：
  - `backup_db_local`（样例）：
    - 语义：对当前 dev 数据库执行一次 backup drill，生成本地 dump 与 backup evidence JSON；
    - 入口：`python scripts/drills/s5a3a_p1c1s2_backup_drill.py`；
    - 输出：终端最后一行打印 backup evidence JSON 相对路径（`artifacts/_tmp_s5a3a_*/drills_<ts>.json`）。
  - `backup_db_to_object_storage`：
    - 语义：在已有本地 dump 的前提下，将其上传至 MinIO，并产出 upload manifest/evidence JSON；
    - 入口：`python scripts/drills/s5a3b_p1c1s3_upload_drill.py`；
    - 输出：终端最后一行打印 upload evidence JSON 相对路径（`artifacts/_tmp_s5a3b_p1c1s3/drills_<ts>.json`）。
  - `restore_db_verify_from_backup`：
    - 语义：从最近一次（或指定） upload evidence 出发，下载 dump → restore 至 `wordloom_restore_dev` → 运行 verify SQL；
    - 入口：`python scripts/drills/s5a3b_p2c1s2_restore_verify_from_minio_drill.py`（通过环境变量 `WORDLOOM_S5A3B_UPLOAD_EVIDENCE` 接收 upload evidence 路径）；
    - 输出：终端最后一行打印 restore+verify evidence JSON 相对路径（`artifacts/_tmp_s5a3b_p2c1s2/drills_<ts>.json`）。
  - `restore_db_sanitize_verify_from_backup`（可选增强）：
    - 语义：在单纯 restore+verify 之外，执行 sanitize SQL 并再次 verify，适合更接近安全/合规叙事；
    - 入口：`python scripts/drills/s5a3b_p3c1s2_restore_sanitize_verify_from_minio_drill.py`；
  - `backup_pipeline_drill`（推荐单命令样例）：
    - 语义：一条命令完成 backup → upload → restore+verify → sanitize+verify，全程产出汇总 evidence JSON；
    - 入口：`python scripts/drills/s5a3b_p4c1s1_pipeline_drill.py`；
    - 输出：终端最后一行打印 pipeline evidence JSON 路径（`artifacts/_tmp_s5a3b_p4c1s1/drills_<ts>.json`）。
- 设计原则：
  - 不改动现有 S5A-3B 脚本实现，只在 S4A-3A log/runbook 层为 operator 取一套易懂的名字与用途说明；
  - operator 只需掌握 1~2 条主路径（例如 `backup_pipeline_drill`），其他入口可作为细粒度补充。

### P1-C1-S3 (First operator-facing command samples | v1)

- Canonical pipeline 样例（推荐主路径）：
  - 入口：在仓库根目录执行：
    - `python scripts/drills/s5a3b_p4c1s1_pipeline_drill.py`
  - 期望行为：
    - 自动调用 backup drill 生成本地 dump；
    - 自动上传到 MinIO，并记录 bucket/object_key/sha256/size；
    - 自动完成一次 restore+verify drill 和一次 restore+sanitize+verify drill；
    - 在 `artifacts/_tmp_s5a3b_p4c1s1/` 下生成汇总 evidence JSON，并在终端最后一行打印 JSON 相对路径。
- 拆分样例（当 operator 需要分步操作时）：
  - 备份到本地：
    - `python scripts/drills/s5a3a_p1c1s2_backup_drill.py`
  - 从本地 dump 上传到对象存储：
    - `python scripts/drills/s5a3b_p1c1s3_upload_drill.py`（需要通过环境变量或配置指向目标 dump 文件）；
  - 从对象存储恢复并验证：
    - 设置 `WORDLOOM_S5A3B_UPLOAD_EVIDENCE=<upload evidence 相对路径>`；
    - 运行：`python scripts/drills/s5a3b_p2c1s2_restore_verify_from_minio_drill.py`；
  - 如需带 sanitize 的 restore：
    - 同样设置 `WORDLOOM_S5A3B_UPLOAD_EVIDENCE`；
    - 运行：`python scripts/drills/s5a3b_p3c1s2_restore_sanitize_verify_from_minio_drill.py`。

### P2 (Drill / Verify)

- P2-C1-S1: 选定一条 backup+restore+verify 路径，在本地 dev/test 上复跑至少 1 次，并在 Evidence 区记录 expected/observed；
- P2-C1-S2: 若时间允许，增加一条“带 sanitize 或灾难模拟”的扩展演练（例如先破坏目标 DB 再通过 backup 恢复）。

### P3 (Docs / Operator wording)

- P3-C1-S1 (Operator-facing wording | v1):
  - 我们在 `S4A-1A` / `S4A-2A` 已经把本地 dev/test 的运行支持路径拆成两条：
    - `ops scripting baseline`：start / stop / status / health / logs / env_prep；
    - `deploy / verify / rollback runtime path`：以 `deploy_app_verify` 作为 post-deploy gate，配合最小 rollback 样本；
  - `S4A-3A` 在此基础上，给 operator 增加第三条常用路径：
    - `backup / recovery / disaster readiness operator path`：
      - 当 operator 关心“最近一次备份在哪里、能不能恢复、怎么证明演练过”时，有一条可复跑的样本链路；
      - 这条链路默认使用 `S5A-3A` / `S5A-3B` 的 backup+object-storage drills 与 `S6A` 的 evidence 语义，不重新发明一套工具；
  - 用人话总结当前能力边界：
    - 我们能：
      - 在 dev/test 上，对 `wordloom_dev` 做一次备份，并把 dump 放到 MinIO 对象存储；
      - 从这个对象存储里的 dump 恢复到单独的 `wordloom_restore_dev` / `wordloom_restore_sanitized_dev` 数据库；
      - 用最小 SQL + 脱敏校验证明这些恢复过的库是可连通、结构完整，且敏感字段已经被清空或替换；
      - 用 drills/evidence JSON 记录整条链路的 bucket/key/sha256/size 与 verify 结果；
    - 我们暂时还不能：
      - 直接覆盖生产库、跨 region 或多租户场景；
      - 自动决定“哪一次备份”是 RPO / RTO 上最优的，只是提供样本与 evidence；
  - 在 operator-facing 语言中，推荐的关键词是：
    - `backup drill`：指 `s5a3a_p1c1s2_backup_drill.py` 这一类生成 dump + evidence 的脚本；
    - `upload drill`：指把 dump 上传到对象存储并记录 manifest/evidence 的步骤；
    - `restore drill` / `restore+verify drill`：指从对象存储 dump 恢复到目标数据库并做 SQL 检查；
    - `sanitize+verify drill`：指在恢复后做脱敏，确保关键字段全部处于“已脱敏”状态；
    - `disaster readiness sample`：指用 `backup_pipeline_drill` 这条一键链路证明“假如当前 DB 损坏，我们至少有一条可演练的恢复样本”。
- P3-C1-S2 (Runbook path | v1):
  - 本 phase 的 runbook 落在：`docs/runbook/run-S4A-3A-backup-recovery-operator-path.md`；
  - runbook 的角色是：
    - 对值班/运行支持来说，给出一条“如何确认最近备份 + 如何演练恢复路径”的最小入口；
    - 用 1~2 条命令样例和 3~6 条 troubleshooting 提示，把 `S5A-3A` / `S5A-3B` 的细节藏在后面，只暴露必要开关；
  - 典型 operator journey：
    - Step 1：确认自己只在 dev/test 环境操作，了解当前 runbook 不涉及生产库；
    - Step 2：根据 runbook 提示，运行 `backup_pipeline_drill` 或拆分命令，完成一次备份+恢复+脱敏演练；
    - Step 3：根据 runbook 给出的 evidence 路径和字段说明，检查 drills/evidence JSON；
    - Step 4：如遇失败，按 runbook 的 troubleshooting 提示查看 docker compose / MinIO / Postgres 容器与日志；
  - `S4A-3A` 不把 runbook 写成“万能恢复宝典”，而是明确声明边界：
    - 仅覆盖本仓库 dev/test 场景；
    - 仅示范从对象存储备份恢复到新的 dev/test 库；
    - 任何涉及生产级 RPO/RTO、跨环境复制的需求，都应回到 roadmap 与后续 phase。 

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: backup/recovery operator contract
- [x] `P0-C1-S2`: evidence contract

### P1 (Implementation / scripts)

- [x] `P1-C1-S1`: 盘点现有 backup/restore 相关入口
- [x] `P1-C1-S2`: 设计最小 operator 入口集合
- [x] `P1-C1-S3`: 定义首批 operator-facing 命令样本

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: 至少 1 条 backup+restore+verify 演练
- [ ] `P2-C1-S2`: 扩展演练（可选）

### P3 (Docs / Operator wording)

- [x] `P3-C1-S1`: operator-facing wording 收口
- [x] `P3-C1-S2`: runbook 草稿

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### P2-C1-S1 (backup+restore+verify pipeline drill | 2026-03-21)

- headSha: `87e150308b6bab5b8c567c62294846edeb90698f`
- artifacts: `artifacts/_tmp_s5a3b_p4c1s1/drills_1774063161.json`
- expected:
  - 一条通过 `backup_pipeline_drill` 完成 `backup -> upload -> restore+verify -> sanitize+verify` 的演练链路；
  - 对象存储中存在一份最近的 `wordloom_dev` 数据库 dump（带 bucket/key/sha256/size 元数据）；
  - 至少 1 条 restore+verify drill 成功，将 dump 恢复到 `wordloom_restore_dev` 并完成最小 SQL 检查；
  - 至少 1 条 restore+sanitize+verify drill 成功，将 dump 恢复到 `wordloom_restore_sanitized_dev`，并在核心文本/summary/snippet 字段上看到“全部已脱敏”（non_redacted_count == 0）。
- observed:
  - 使用命令：`python scripts/drills/s5a3b_p4c1s1_pipeline_drill.py`；
  - pipeline drill 顺利完成，终端最后一行输出 evidence JSON 路径：`artifacts/_tmp_s5a3b_p4c1s1/drills_1774063161.json`；
  - evidence.summary：
    - bucket: `wordloom-backups-devtest`；
    - object_key: `s5a3a/2026-03-21/wordloom_dev/1774091966.dump`；
    - sha256: `4d58ab20dc4ed92475f3dafa772ec616cb1b421f78bae69dd58cd852c1872dfc`；
    - size_bytes: `482081`；
  - drills.s5a3a_backup.status: `ok`，对应 backup evidence：`artifacts/_tmp_s5a3a_p1c1s2/drills_1774063162.json`；
  - drills.s5a3b_upload.status: `ok`，对应 upload evidence：`artifacts/_tmp_s5a3b_p1c1s3/drills_1774063164.json`；
  - drills.s5a3b_restore_verify.status: `ok`，对应 restore+verify evidence：`artifacts/_tmp_s5a3b_p2c1s2/drills_1774063179.json`；
  - drills.s5a3b_restore_sanitize_verify.status: `ok`，对应 restore+sanitize+verify evidence：`artifacts/_tmp_s5a3b_p3c1s2/drills_1774063189.json`；
  - summary.p3_verify.kind: `s5a3a_sanitization_verify`，stats 中所有受控字段的 `non_redacted_count` 均为 0，`failures` 为空数组，符合“脱敏后仍可通过最小索引/检索验证”的预期。

## Recent changes (for traceability, optional)

- 2026-03-21: scaffolded `S4A-3A` as the third `S4A` phase, focusing on backup / recovery / disaster readiness operator paths, reusing `S5A-3B` object-storage backup drills as the primary evidence source.
