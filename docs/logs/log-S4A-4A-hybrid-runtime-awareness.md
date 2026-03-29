# log-S4A-4A (Phase 4: Hybrid Runtime Awareness)

---

**id**: `S4A-4A`
**kind**: `log`
**title**: `hybrid runtime awareness (cloud fundamentals, config/secrets/logging, on-prem + cloud bridging) v1`
**status**: `stable`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, Operations, HybridRuntime, Cloud, Logging, Config, Secrets, epic/s4, epic/s4a, sub/4a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S4A-4A-hybrid-runtime-awareness.md`
  **parent_log**: `docs/logs/log-S4A-systems-platform-operations-runtime-foundation.md`
  **previous_log**: `docs/logs/log-S4A-3A-backup-recovery-operator-path.md`
  **reference_log_1**: `docs/logs/log-S5A-security-governance.md`
  **reference_log_2**: `docs/logs/log-S5B-security-governance-hard-gates.md`
  **reference_log_3**: `docs/logs/log-S6A-evidence-drills-spine.md`
**roadmap_path**: `docs/roadmap/road-S1-1-gov-role-minimal-ops-loop.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: `M5-P0`
**roadmap_bridge_refs**: `docs/roadmap/road-S1-1-gov-role-minimal-ops-loop.md#M5-P0, docs/roadmap/road-S1-1-gov-role-minimal-ops-loop.md#M5-P3`
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

### P2 (Drill / Verify)

### P2-C1-S1 (Hybrid runtime awareness sample: Vercel demo static assets | v1)

- 场景主语义：
  - 同一个 `/demo` 入口，在本地 dev/test 与 Vercel 部署上，静态资源的 runtime 行为曾经明显不同：
    - 本地：`frontend/public/demo` 下的截图与视频是正常的二进制文件，通过 Next 静态资源管线直接提供；
    - 云端（Vercel 早期部署）：相同路径下被返回为 Git LFS pointer 文本（`version https://git-lfs.github.com/spec v1 ...`），导致浏览器无法正常展示 demo 资源。
- drill 步骤（可重复）：
  - 本地 dev/test：
    - 启动前端 dev server 或 Docker 模式前端（端口依 README / 现有 quick start 而定，例如 `http://localhost:30001` 或 `http://localhost:31002`）。
    - 打开 `/demo` 页面，确认页面首屏正常渲染；
    - 直接访问下列静态资源 URL 中的任意一个，并记录 `Content-Type` 与响应体大小：
      - `GET /demo/DEMO-main-content-model.png`
      - `GET /demo/DEMO-1.png`
      - `GET /demo/DEMO-gif-1-2x.gif`
      - `GET /demo/DEMO_VIDEO_1.mp4`
    - 期望：
      - 响应为二进制图片或视频（如 `image/png`, `image/gif`, `video/mp4`），size 为几十 KB 到数 MB 不等；
      - 浏览器直接渲染图片 / 播放视频，无报错。
  - 云端（Vercel 部署，示例域名）：
    - 使用默认 fallback 站点 `https://wordloom-v3.vercel.app`，或按 [docs/demo/VERCEL-DEPLOY.md](docs/demo/VERCEL-DEPLOY.md) 中说明配置的 `https://your-wordloom-site.vercel.app`；
    - 访问：
      - `GET https://<site-origin>/demo`
      - `GET https://<site-origin>/demo/DEMO-main-content-model.png` 等与本地相同的资源路径；
    - 历史故障现象（LFS 指针未被正确解包时）：
      - 响应 `Content-Type` 为 `text/plain` 或默认类型，响应体只有几十字节；
      - 内容以 `version https://git-lfs.github.com/spec v1` 开头，后续包含 `oid sha256:...` 与 `size ...` 等元数据，而不是实际图片/视频二进制；
      - `/demo` 页面首屏可能仍然渲染部分文字，但媒体区域空白或报错。
- expected vs observed（样本表达，v1）：
  - `environment_local`：
    - `origin`: `http://localhost:<dev-port>`
    - `asset_path`: `/demo/DEMO-main-content-model.png`（代表性样本之一）
    - `content_type`: `image/png`
    - `size_bytes_approx`: `O(10^5)` 量级（几十 KB 以上）
    - `shape`: 浏览器可直接展示静态图像；`/demo` 页面媒体区域完整。
  - `environment_cloud`（LFS 指针未修复之前的部署）：
    - `origin`: `https://wordloom-v3.vercel.app` 或团队实际使用的 Vercel 项目域名；
    - `asset_path`: `/demo/DEMO-main-content-model.png`
    - `content_type`: `text/plain`（或其他默认类型）
    - `size_bytes_approx`: `O(10^2)` 量级（几十字节左右）
    - `body_prefix`: `"version https://git-lfs.github.com/spec v1"`（Git LFS pointer 文本）；
    - `shape`: 浏览器无法渲染图像，demo 媒体区缺失或报错。
- operator takeaway（对 operator 的启发）：
  - 这是一个典型的 hybrid runtime 问题：
    - 本地 dev/test 直接从工作副本读取二进制资源，行为正常；
    - 云端依赖构建/部署管线正确解包 Git LFS 资源，否则只会拿到文本指针。
  - 诊断路径：
    - 从 `/demo` 页面开始，确认文本区域正常而媒体区域异常；
    - 打开浏览器 devtools，检查网络请求对应的静态资源 URL，观察 `Content-Type` 与响应体内容；
    - 若 body 显示 Git LFS pointer 文本，则需要回到：
      - 仓库 `.gitattributes`（例如针对 `frontend/public/demo/**` 的 LFS 配置）；
      - Vercel 项目设置中是否启用了 Git LFS 支持或有使用 `vercel build` 前的 `git lfs pull` 步骤；
      - 是否可以将 demo 用的公开媒体资源从 LFS 改为常规 Git 跟踪，以降低云端部署复杂度。
  - 与本 phase contract 的关系：
    - 该样本说明：
      - `config & secrets view` 中，静态资源并不只受 `.env` 控制，还受 Git/LFS 与 CI/CD 配置影响；
      - `logging view` 可通过前端日志与 Vercel 部署日志（如构建输出、错误页）来辅助判断；
      - operator 在面对“本地 OK / 云端 demo 媒体异常”时，有一条具体、可重复的排查脚本可走。

### P2-C1-S2 (Hybrid runtime awareness sample: WSL vs Windows dev tooling | v1)

- 场景主语义：
  - 同一份前端 dev 环境，在 WSL2 + bash 与 Windows PowerShell + `npm` 之间，dev server 的启动路径和工具链行为不同：
    - WSL2 场景下，`./scripts/ops/start.sh dev all --no-worker` 依赖 bash / Node toolchain，路径解析与 shebang 正常；
    - Windows 直接运行 `npm run dev:dev` 时，可能出现 `cross-env` 等工具缺失、PATH 差异，导致 dev server 无法按预期启动。
- drill 步骤（可重复）：
  - WSL2 环境：
    - 打开 WSL2 终端，进入 `/mnt/d/Project/wordloom-v3`；
    - 运行：`./scripts/ops/start.sh dev all --no-worker`；
    - 观察：
      - 脚本会按顺序启动 infra / db / app / frontend 等服务；
      - `health.sh dev` 返回成功，前端在目标端口（例如 `http://localhost:30001`）可访问。
  - Windows PowerShell 直连 npm：
    - 在 `D:\Project\wordloom-v3\frontend` 执行：`npm run dev:dev`；
    - 使用之前的故障记录（当前 session 已多次出现 exit code 1）：
      - 前端 dev server 启动失败；
      - 报错信息指向 `cross-env` 不存在或 PATH 中缺失对应可执行文件；
      - 同一仓库在 WSL2 中通过 `start.sh` 能正常拉起 UI，而在 Windows 原生 npm 路径下失败。
- expected vs observed（样本表达，v1）：
  - `environment_wsl2`：
    - `command`: `./scripts/ops/start.sh dev all --no-worker`
    - `shell`: `bash`（WSL2 内）
    - `status`: `ok`
    - `frontend_reachable`: `true`（health check 通过，示例：`Start-Sleep; curl http://127.0.0.1:<port>` 成功）
  - `environment_windows_powershell`：
    - `command`: `npm run dev:dev`
    - `shell`: `powershell`
    - `status`: `failed`
    - `stderr_prefix`: 指向 `cross-env` 或相关 Node 工具缺失 / PATH 配置问题
    - `frontend_reachable`: `false`（health 脚本返回非零退出码）。
- operator takeaway：
  - 这是一个“同一套前端代码在不同 runtime shell + tooling 下表现不同”的样本：
    - hybrid 维度不再是传统意义上的“本地 vs 云”，而是“WSL2 dev shell vs Windows dev shell”；
    - `.env` 和应用代码本身未变，但 node_modules 安装路径、`node_modules/.bin` 暴露方式、`cross-env` 安装位置等导致行为差异。
  - 诊断路径：
    - 先用统一的 `health.sh dev` 脚本确认 dev env 是否健康；
    - 比较同一命令在 WSL2 与 Windows PowerShell 下的行为与 stderr 日志；
    - 根据差异，决定：
      - 优先推荐哪种 dev shell（例如：文档中明确推荐 “WSL2 + bash + start.sh” 作为首选路径）；
      - 是否需要在 Windows 原生路径下增加额外的 `npm install --save-dev cross-env` 或脚本包装层。
  - 与本 phase contract 的关系：
    - 补充说明 `config & secrets view` 之外的 runtime 维度：shell / tooling 自身也是 runtime 的一部分；
    - 为 operator 提供了一个具体的“WSL vs Windows”行为对照样本，说明在多 runtime 混合时如何用同一套脚本（如 `health.sh`）来统一观测口径。

### P3 (Docs / Operator wording)

- P3-C1-S1 (Operator-facing wording | v1):
  - 在前几个 phase 里，S4A spine 已经给 operator 提供了三条本地 dev/test 运行支撑路径：
    - `S4A-1A`：ops scripting baseline（env_prep / start / status / health / logs）；
    - `S4A-2A`：deploy / verify / rollback runtime path（部署 gate + 最小 rollback 样本）；
    - `S4A-3A`：backup / recovery / disaster readiness operator path（backup+restore+sanitize drills + evidence）。
  - `S4A-4A` 在此基础上，提供了一条面向 hybrid runtime 的“本地 vs 云 / 多 runtime shell”意识路径：
    - 对外可以这样解释：
      - 本地 dev/test 和 Vercel demo 部署之间，静态资源的来源与构建路径不完全相同（工作目录 vs 云构建产物 vs Git LFS）；
      - 同一份前端代码，在 WSL2 dev shell 与 Windows PowerShell + npm 之间，依赖的 node 工具链与 PATH 也存在差异；
      - 我们用两条样本（Vercel demo 静态资源 / WSL vs Windows dev tooling）来把这些差异说清楚，并给出最小排查路径。
  - 用人话总结当前 hybrid runtime 能力边界：
    - 我们能：
      - 说明 `/demo` 这条 portfolio 前门在本地和云上的行为差异：本地 demo 资源来自 `frontend/public/demo` 二进制文件，云端 demo 资源依赖 Vercel + Git LFS 正确解包；
      - 通过浏览器 devtools / curl 等手段，对比本地与云端静态资源的 `Content-Type` 和响应体形态，并据此判断 LFS 指针是否泄露到 runtime；
      - 说明在 dev 环境下，推荐使用 `WSL2 + bash + scripts/ops/start.sh` 作为首选路径，并用统一的 `health.sh dev` 检查 dev env；
      - 举例说明 Windows 原生 PowerShell + `npm run dev:dev` 这一路径可能因为 `cross-env` / PATH 等问题而失败，以及如何用 stderr + health check 快速识别；
    - 我们暂时还不能：
      - 提供一套完整的“多云 runtime 策略”和统一配置平台；
      - 自动在 CI 或 Vercel 项目设置中修复所有 Git LFS / 构建管线问题；
      - 在本 phase 内覆盖所有可能的 hybrid 组合（只选了两个最贴近当前 repo 的代表性样本）。
  - 面向 operator 推荐使用的 hybrid runtime 关键词：
    - `config & secrets view`：本地 `.env.*` 与云端环境变量 / app settings / secrets 管理的映射关系；
    - `logging view`：本地 container stdout / 文件日志 vs 云端 log stream / Vercel 构建日志；
    - `connectivity & dependency view`：本地 docker-compose 里的 DB/ES/MinIO vs 云端 managed DB / 对象存储 / 其他依赖；
    - `demo static assets sample`：用 `/demo` 静态资源的 LFS 指针问题作为“本地 vs 云”样本；
    - `WSL vs Windows dev shell sample`：用 `start.sh` vs `npm run dev:dev` 的行为差异作为“多 runtime shell/tooling”样本。
- P3-C1-S2 (Runbook path | v1):
  - 本 phase 的 runbook：`docs/runbook/run-S4A-4A-hybrid-runtime-awareness.md`；
  - runbook 的角色是：
    - 给值班/运行支持一条非常轻量的 hybrid runtime checklist，主要围绕：
      - demo 在 Vercel 上与本地表现不一致时，如何确认是静态资源/LFS 管线问题，而不是 API/后端问题；
      - dev env 在 WSL2 下可以跑起来，而在 Windows 原生 PowerShell + npm 下报错时，如何快速识别是 shell/tooling 维度的差异；
    - 保持格式与 `S4A-3A` runbook 一致，但更聚焦于“意识与排查路径”，而不是大规模脚本执行。
  - 典型 operator journey（hybrid 视角）：
    - Step 1：确认当前问题是“本地 OK / 云上异常”或“WSL dev OK / Windows dev 异常”这一类 hybrid 问题，而非纯粹代码 bug；
    - Step 2：按照 runbook 提示，对 `/demo` 页面和静态资源做一次本地 vs 云端对照（状态码、Content-Type、body 形态）；
    - Step 3：如怀疑是 LFS 指针问题，检查 `.gitattributes`、Vercel 项目设置与 CI 步骤中是否有 `git lfs pull` / 相关配置；
    - Step 4：如怀疑是 dev tooling 差异，按 runbook 提示在 WSL2 和 Windows PowerShell 下分别执行 `start.sh` / `npm run dev:dev` + `health.sh dev`，对比 stdout/stderr；
    - Step 5：根据 runbook 的 Notes & Boundaries，决定是否需要升级到后续 S4A/S5A/S5B phase 或其他 epic。
  - `S4A-4A` 明确声明 runbook 边界：
    - 只覆盖当前 wordloom-v3 repo 的 dev/test + Vercel demo + WSL/Windows dev tooling 场景；
    - 不提供一键修复脚本，也不替代生产级多云/runtime 策略；
    - 若问题涉及安全策略、租户隔离或合规性，应回到 `S5A` / `S5B` 等安全治理 phase。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: hybrid runtime contract
- [x] `P0-C1-S2`: evidence contract

### P1 (Implementation / scaffolding)

- [x] `P1-C1-S1`: 盘点 hybrid runtime 相关资产
- [x] `P1-C1-S2`: 定义 operator-facing hybrid 视图
- [x] `P1-C1-S3`: 预留 evidence hooks

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: 至少 1 条 hybrid runtime awareness 演练样本（Vercel demo 静态资源 vs 本地 dev/test）
- [x] `P2-C1-S2`: 额外 hybrid runtime awareness 演练样本（WSL2 dev shell vs Windows dev shell）

### P3 (Docs / Operator wording)

- [x] `P3-C1-S1`: hybrid runtime wording 收口
- [x] `P3-C1-S2`: （如有必要）runbook 草稿

## Evidence (v1)

- 2026-03-21 — hybrid runtime awareness samples（P2-C1-S1 & P2-C1-S2）
  - `sample_1_vercel_demo_static_assets`：
    - `local_dev`: `/demo` 页面及其静态资源（截图 + 视频）在本地 dev/test 中以正常二进制形式提供，浏览器可直接渲染；
    - `cloud_vercel`: 历史部署中，相同路径在 Vercel 上返回 Git LFS pointer 文本，`Content-Type` 与 body 形态均异常；
    - `takeaway`: 展示了静态资源在“工作目录 vs 云构建产物”之间的差异，以及 Git LFS / CI 配置对 runtime 行为的影响。
  - `sample_2_wsl_vs_windows_dev_tooling`：
    - `wsl2_bash`: `./scripts/ops/start.sh dev all --no-worker` 成功启动 dev env，`health.sh dev` 通过；
    - `windows_powershell`: 多次 `npm run dev:dev` 失败，stderr 中指向 `cross-env`/PATH 问题，`health.sh dev` 返回非零退出码；
    - `takeaway`: 展示了同一前端代码在不同 shell/tooling runtime 下的行为差异，并强化了统一健康检查脚本的价值。

## Recent changes (for traceability, optional)

- 2026-03-21: scaffolded `S4A-4A` as the fourth `S4A` phase, focusing on hybrid runtime awareness across local dev/test and cloud/managed environments.
