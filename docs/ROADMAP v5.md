# ROADMAP v5

## 这份 v5 的定位

这版 roadmap 是 `政府岗适配版`。

它不是推翻你原来的平台路线，而是把重心临时切到更贴近这类岗位的语言和优先级：

- systems / platform operations
- operational support
- backup / recovery / disaster readiness
- documented sustainable architecture
- automation / scripting / reproducible environment

结论先说：

- 你的原路线没有错。
- 但如果要对准这类政府岗位，叙事重点不能再是“平台愿景”优先。
- 更合适的主轴应该是：`systems/platform reliability + automation + operational support + recoverability + documented runtime`。

一句话版本：

> 这份 roadmap 的目标，不是把你包装成云平台专家，而是把 `wordloom-v3` 里已经存在的系统工程骨架，翻译成更贴近 systems/platform support 岗位的能力故事。

---

## 一、先校准：按政府岗语言，你已经有什么

原版 v5 的一个偏差是：容易把你写成“还没开始补平台运行面的人”。

这不准确。

按这个岗位的语境，你已经有几块非常值钱的资产。

### 1. 你已经有结构化的运行与验证思维

`wordloom-v3` 里最强的不是某个单点工具，而是这条骨架：

- drills
- evidence
- hard gates
- verifier
- runbook / operator workflow

这套东西可以直接翻译成政府岗会吃的语言：

- operational support discipline
- post-change verification
- documented runtime behavior
- repeatable checks
- recoverability evidence

也就是说，你不是只会“写代码”，你已经有一套“系统怎么验证、怎么复跑、怎么排障”的习惯。

### 2. 你已经有 backup / recovery / object storage 的最小闭环

`S5A-3B` 其实非常贴这个岗位，因为它天然能讲：

- backup
- upload
- restore
- sanitize
- verify
- evidence JSON

对这类岗位来说，这比你多会一个云服务名更值钱。

它已经可以翻译成：

- backup and recovery narrative
- disaster readiness basics
- recoverability verification
- operational evidence discipline

### 3. 你已经有 documented sustainable architecture 的雏形

虽然你现在的系统工程主线很多是 `projection / outbox / hard gate / tenant / audit`，但换成岗位语言，其实可以讲成：

- documented architecture evolution
- stable contracts
- sustainable operations
- low-cardinality reason taxonomy
- change safety and rollback awareness

这和岗位描述里的 `stable, scalable, optimised, resilient, documented and sustainable ICT architecture` 是对得上的，只是你原来表述得更偏 backend/platform。

### 4. 你已经有 automation mindset，但还缺更直接的 systems 话术

仓库里已经有：

- GitHub workflows
- reusable drills runners
- hard-gate workflows
- scripts / verification entrypoints

这意味着你并不缺“自动化思维”，你缺的是把它重新包装成：

- automation of routine operations
- deployment reliability
- configuration consistency
- operational support tooling

---

## 二、真正要修正的不是方向，而是重心

原来的主线更像：

1. Terraform / IaC
2. AWS 单云运行面
3. Docker + deploy chain
4. observability externalization
5. Kubernetes 第二层表达能力

如果对准这类政府岗，更合适的临时主线应该改成：

1. Linux / Windows / system administration 语言补齐
2. IaC / scripting / automation
3. cloud fundamentals -> hybrid environment awareness
4. observability -> operational reliability

注意，这里不是说你要变成 Windows admin，而是你必须把申请材料和补强顺序调整到对方听得懂的方向。

---

## 三、修正后的优先级

### 第一优先级：systems administration / operational support 语言补齐

这不是让你去转向重运维，而是让你申请时能自然讲出下面这些词，并且能拿 `wordloom-v3` 的实际资产支撑它们：

- installation
- configuration
- maintenance
- monitoring
- backup / recovery
- operational support
- lifecycle management
- documented sustainable architecture

你现在最需要补的，不是大量新概念，而是这套表达和对应的小样本。

#### 这部分具体要补什么

##### A. Bash 优先级提高

这个岗位明确点了 `PowerShell / Bash`。

PowerShell 先不用深挖，但 Bash 应该尽快补到能说得出口。

最小边界：

- 启动 / 停止 / 检查脚本
- 环境准备脚本
- 简单部署脚本
- log / health / backup 相关脚本

##### B. Linux / Windows 语言要补齐，但先不做深水区

你不用把 roadmap 写成“我要成为 Windows 平台管理员”，但应该明确补这些表述：

- system installation and configuration awareness
- service maintenance and lifecycle thinking
- patch / config / backup / recovery language
- on-prem and off-prem operational support awareness

也就是说：补的是 `systems/platform operations` 语言，而不是转成纯基础设施岗。

### 第二优先级：IaC / scripting / automation

这部分原版 v5 是对的，但要改讲法。

保留：

- Terraform
- Bash
- GitHub workflows
- 基础自动化思维

但叙事上不要先讲“大平台愿景”，而要讲：

- reproducible environment
- automation of routine operations
- configuration consistency
- deployment reliability

#### Terraform 在这类岗位里为什么仍然是高优先级

因为它可以直接对应：

- infrastructure scripting and automation
- environment definition
- consistency across deployments
- documented repeatable setup

你最合适的产出仍然是：

`Wordloom Platform Infra Sample`

但这里不要写成“未来平台化样本”，而要写成：

- minimal reproducible runtime environment
- documented infrastructure setup
- configuration consistency and repeatability

### 第三优先级：cloud fundamentals 改写成 hybrid environment awareness

原版写的是 AWS 单云运行面。

如果对准这个政府岗，建议不要删掉这条线，而是改成更稳的表述：

- cloud fundamentals
- hybrid environment awareness
- secrets / config / logging / deploy pipeline basics
- on-prem + cloud bridging mindset

#### 这意味着什么

- 学习主线仍然可以先打 AWS
- 但申请材料不要写成“我在主攻云原生平台”
- 更合适的说法是：`I am building cloud and hybrid runtime awareness on top of a systems/platform operations foundation.`

#### AWS 这一段应该怎么保留

继续保留：

- IAM basics
- VPC basics
- RDS / S3
- CloudWatch
- secrets / config
- deploy / logging / recovery basics

但叙事重心改成：

- hybrid-compatible runtime thinking
- cloud-backed operational support
- recoverability and deployment discipline

### 第四优先级：observability 继续保留，但改成 operational reliability 语言

原版如果只讲 `traces / metrics / dashboards`，会显得太偏平台工具。

对这个岗位，更好的说法是：

- monitoring
- service health
- incident signals
- recoverability
- post-change verification
- operational visibility

这部分你其实已经有不少底子，因为你的 drills / evidence / hard-gate 体系天然能支撑：

- post-change verification
- recoverability checks
- operator-facing evidence
- structured incident clues

所以这部分不是从零学，而是把现有优势翻译成更贴岗位的话术。

---

## 四、如果只按“申请这个岗位最有帮助”来排序

如果不按长期理想，而只按“短期最有助于对准这个政府岗”，优先级我建议这样排。

### 1. Bash + 基础自动化脚本

这是最应该前提的。

理由：

- 岗位明确点了 `PowerShell / Bash`
- 这比你现在去追更深的 K8s 或 Datadog 更直接命中
- 也最容易和 `wordloom-v3` 的现有资产结合

你至少要做出这几个能讲的东西：

- 启动 / 停止 / 检查脚本
- 环境准备脚本
- 简单部署脚本
- log / health / backup 脚本

### 2. Terraform / IaC 最小样本

这部分原版本来就是头号优先级，现在仍然成立。

而且对这个岗位非常现实，因为它直接能对应：

- infrastructure scripting and automation
- IaC practices
- reproducible environment

唯一要变的是表达方式，不是学习顺序。

### 3. Docker + deployable runtime

岗位不一定会直接把 Docker 放在最前，但这块非常有助于证明：

- 你理解 runtime consistency
- 你不是只会本地开发
- 你有 deploy mindset
- 你能支撑系统运行而不是只写功能

### 4. monitoring / recovery / backup-recovery narrative

这类岗位很吃：

- recoverability
- disaster readiness
- monitoring
- sustainable operations

而你的 `S5A-3B` 恰好已经是一块非常像样的资产。

这部分建议故意放大，不要低估它：

- backup
- upload
- restore
- verify
- evidence bookkeeping

它比你现在硬补一个 AzureCLI 小词条更有说服力。

### 5. GitHub / pipeline / deploy-verify-rollback

这块原版 v5 也是对的，而且对这个岗位有实际价值。

应该继续保留：

- build artifact
- package image
- deploy
- smoke verify
- rollback / fallback

这会让你看起来像“能支撑平台运行的人”，而不是只会跑测试的人。

---

## 五、暂时不适合为了这个岗位硬补什么

### 1. 不要把 Kubernetes 提到前面

你原版关于 K8s 的判断其实是对的：

- 它是第二层表达能力
- 不是当前第一层补强项

对这个政府岗来说，它也不是最直接的命中点。

### 2. 不要为了 AzureCLI 去硬装 Azure 工程师

岗位提到 AzureCLI，不等于它要的是成熟 Azure platform admin。

它更像在表达：

- cloud fundamentals
- pipeline
- automation
- operational support

所以更合理的做法是：

- 承认你在补 cloud tooling
- 但不要把自己包装成成熟 Azure 平台管理员

### 3. 不要把重点放在 IDP / org-level DevEx

原版你已经把这两个方向降级了，这对这个岗位更应该继续坚持。

这类岗位通常不会优先吃：

- internal developer platform 愿景叙事
- org-level developer experience ownership

它更吃的是：

- systems support
- operational reliability
- runtime maintenance
- documented sustainable operations

---

## 六、申请这个岗位时，话术主轴要怎么切

如果真要投这类岗位，你的叙事不能继续以：

- complex backend
- async system evolution
- projection / outbox sophistication

作为第一主轴。

这些不是不能讲，而是应该退到“底层能力证明”。

更合适的主轴应该改成：

> systems/platform reliability + automation + operational support + documented sustainable runtime

申请时应该强调的点：

- 我关注系统运行的稳定性、恢复性和可维护性
- 我有结构化文档、evidence、runbook、hard gate 的习惯
- 我在 Wordloom 中已经形成了可验证、可恢复、可审计的工程实践
- 我正在把这套骨架外扩到 IaC、deploy、runtime packaging、observability 这些运行层

也就是说，你要把原来更偏 backend/platform 的资产，翻译成 `operations / support / recoverability / lifecycle / sustainable architecture` 语言。

---

## 七、基于这个岗位改写后的三条路线

### 路线 A：把 Wordloom 现有资产翻译成 systems/platform operations 语言

这条路线不一定要求大量新代码，但很关键。

应该明确写入 roadmap 的既有资产：

- `S0D / S3A / S6A`：drills / evidence / hard gate / runbook
- `S5A / S5B`：policy / audit / authorization / documented governance
- `S5A-3B`：backup / restore / sanitize / verify
- `S2B / S2C / S2D`：稳定 contract、change safety、operator workflow discipline

但对外表达时，优先用这些词：

- operational support
- recoverability
- documented runtime
- post-change verification
- sustainable architecture

### 路线 B：补 systems/platform runtime 底座

这是当前主线。

按顺序：

1. Bash / automation scripts
2. Terraform / IaC sample
3. Docker / runtime packaging
4. deploy / verify / rollback
5. cloud fundamentals with hybrid awareness

### 路线 C：补 operational visibility 和第二层表达能力

在路线 B 有落地样本之后再推进：

- monitoring / service health / operational visibility
- CloudWatch / Datadog basics
- Kubernetes basics
- incident / RCA / SLO basics

这条路线不是当前主线，而是增强层。

---

## 八、推荐的 8 周适配顺序

### Week 1-2：重写表达层 + 补 Bash / operational scripts

目标：先把你已有资产换成更贴岗位的语言，并补最直接命中的 automation 样本。

输出物：

- 一页 `Wordloom systems/platform operations map`
- Bash 脚本样本：启动 / 停止 / health / backup / logs
- 一页“已有资产如何映射岗位要求”表

### Week 3-4：Terraform 最小环境样本

目标：交付一份可重复的基础设施定义样本。

输出物：

- Terraform skeleton
- minimal runtime env definition
- README / runbook
- reproducible environment narrative

### Week 5：Docker + deployable runtime

目标：把系统运行面标准化。

输出物：

- 稳定 Dockerfile
- compose / env / health check
- documented runtime packaging

### Week 6：deploy / verify / rollback 闭环

目标：让你现有的 verification 能力真正贴到运行支持语境。

输出物：

- build artifact
- deploy to test env
- smoke verify
- rollback note

### Week 7：monitoring / recovery / operational visibility

目标：把现有 evidence / drills 习惯翻译成岗位可识别语言。

输出物：

- service health checks
- logs / metrics 基本面
- recovery / post-change verification note
- minimal incident / RCA template

### Week 8：cloud fundamentals with hybrid framing

目标：保留云平台学习主线，但用更贴政府岗的语言来表达。

输出物：

- AWS basics notes mapped to hybrid runtime thinking
- config / secret / logging / deploy bridging note
- on-prem + cloud awareness summary

---

## 九、精简版优先级总结

### 现在就做

- Bash / automation scripts
- Terraform / IaC 最小样本
- Docker / runtime packaging
- deploy / verify / rollback
- backup / recovery / operational support narrative

### 紧接着做

- monitoring / service health / operational visibility
- cloud fundamentals with hybrid awareness
- incident / RCA / post-change verification

### 先不急

- Kubernetes 提前上位
- AzureCLI 深挖
- Datadog 工具化扩面
- internal developer platform from scratch
- org-level DevEx ownership
- 多云深水区

---

## 十、最现实的一句话判断

如果目标是：

`长期往 systems / platform / DevOps engineer 靠拢`

这份 roadmap 仍然非常可行。

如果目标是：

`短期专门对准这个政府岗`

那这份 roadmap 的正确改法不是重做，而是：

- 保留 Terraform / IaC / Docker / deploy / observability
- 提高 Bash / automation / backup-recovery / operational support 的权重
- 降低 K8s / Datadog / IDP / 多云扩面的优先级
- 在申请材料里使用 systems/platform operations 语言，而不是产品平台语言

最后一句话：

> 对准这个岗位，你的核心优势不是“我会很多云平台工具”，而是“我已经在 Wordloom 中形成了可验证、可恢复、可文档化、可支持运行的系统工程习惯，现在正把这套骨架外扩到 IaC、deploy、runtime、monitoring 这一层。”
