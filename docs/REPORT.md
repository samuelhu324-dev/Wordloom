这 17 个样本现在可以概括为一句话：

当前样本池的中心已经从“偏 DevOps 的混合工程岗位”扩大成“以 Platform / DevOps / Cloud 为核心，向 Backend 和 Software 延展的企业级工程岗位集合”。

和上一轮相比，最明显的变化有 4 个：

platform_engineering 已经成型，不再只是零散出现
多云、IaC、CI/CD、可观测性，已经从“常见要求”变成“主轴要求”
work rights 相关条件明显增多，已经成为这批样本里的高频现实门槛
当前 taxonomy 对“企业 IT / infrastructure / systems”类岗位的覆盖还不够完整，出现了 2 个 keep_in_intake
二、这批样本现在的结构是什么

本轮 17 份样本的 decision 分布是：

promote_to_reviewed = 14
keep_in_intake = 2
split_multi_role = 1
role family 分布是：

devops = 4
platform_engineering = 3
cloud_engineering = 3
software_engineering = 3
backend_engineering = 2
full_stack_engineering = 1
这个分布非常有意思，因为它说明你现在的样本池已经不是单一方向，而是形成了 3 条主线：

平台与交付主线
云基础设施与运维主线
软件/后端开发与平台交叉主线
其中最值得注意的是 platform_engineering = 3。这说明新样本已经把“平台工程”从隐含概念，推成了一个可以单独观察的岗位族。

三、现在市场主要在要什么技能

本轮 top skills 是：

terraform = 10
aws = 9
work_rights_required = 9
docker = 7
kubernetes = 7
azure = 6
typescript = 5
cloudformation = 5
ec2 = 4
rds = 4
s3 = 4
cloudwatch = 4
gcp = 4
python = 4
datadog = 4
如果把这些词翻译成“真实招聘含义”，当前市场在这批样本里最看重的是下面 5 类能力。

1. IaC 已经是核心底座，不再是附加项

terraform = 10 是这批样本里最重要的信号之一。

这意味着企业越来越希望：

基础设施可定义
环境可重复
变更可管理
平台能力可规模化复制
这不是传统“会配云资源”层面，而是明显在要工程化基础设施能力。

2. 云平台能力是默认前提

aws = 9、azure = 6、gcp = 4，说明：

单云岗位仍然存在
但多云意识越来越强
候选人不能只停留在某个服务名词层面，而要能理解云环境的运行和治理
新样本尤其强化了这一点，例如：

Vicinity 是非常典型的多云平台工程画像
Codex 和 Omega 明显偏 AWS cloud delivery
Yokogawa 更偏 Azure + infrastructure/support
Primary Health 则是 AWS + Kubernetes + backend/platform 混合型
3. 容器与平台运行能力已经常态化

docker = 7、kubernetes = 7 说明容器能力仍然是中心要求。

但现在它不是孤立出现，而是和下面这些要素强耦合：

IaC
CI/CD
观测与告警
生产环境稳定性
开发者自服务
这说明企业要的是“能把运行平台搭起来并长期维护好的人”。

4. 可观测性和可靠性要求明显上升

datadog = 4、cloudwatch = 4，加上 report 里多个岗位强调：

telemetry
monitoring
root cause analysis
reliability metrics
incident response
DORA metrics
这意味着市场对“把服务跑起来”已经不满足了，开始要求：

看得见
定位得准
出问题能追根溯源
能持续优化交付质量
这个趋势在新样本里比上一轮更明显。

5. 软件开发能力仍然在平台岗位里占很重位置

虽然平台和云能力是主轴，但 typescript = 5、python = 4，再加上 nodejs、react、java、kafka 等，说明很多岗位并不是纯运维。

更准确地说：

平台岗越来越要求理解应用层
DevOps 岗越来越要求写代码
后端岗越来越需要理解部署和平台
软件岗开始向平台可靠性和基础设施延伸
所以现在最值钱的不是“单点工具熟练”，而是“软件和平台两边都能做出东西”。

四、常见技能组合现在变成了什么

本轮最有代表性的组合有这些：

devops + aws + kubernetes + terraform + github_actions
platform_engineering + aws + kubernetes + terraform
cloud_engineering + aws + kubernetes + terraform + python
backend_engineering + aws + docker + aws_cdk + nestjs
devops + azure + kubernetes + terraform + azure_devops
full_stack_engineering + react + typescript
这些组合可以大致分成 4 种岗位画像。

1. 平台工程画像

典型组合：

platform_engineering + aws + kubernetes + terraform
这类岗位强调：

平台稳定性
开发者效率
自服务
标准化交付
共享基础设施
Vicinity 是这一类最明显的代表，见 Vicinity-Centres-Platform-Engineer-DevOps.output.json

它不是单纯 DevOps，而是典型“平台团队为多个产品线提供基础能力”的画像。

2. 云工程画像

典型组合：

cloud_engineering + aws + kubernetes + terraform + python
这类岗位更强调：

云平台搭建与治理
AWS 核心服务
IaC
运维支持
客户/项目交付
Codex 和 Omega 把这一类画像拉得更清晰了：
一个偏咨询交付型 cloud engineer，一个偏早期基础设施 owning 型 cloud engineer。

3. DevOps 交付画像

典型组合：

devops + aws + kubernetes + terraform + github_actions
devops + azure + kubernetes + terraform + azure_devops
这类岗位说明当前 DevOps 的真实要求通常包含：

云平台
IaC
容器
CI/CD
脚本自动化
incident / on-call / ownership
PartsCheck 是这个方向的一个很典型样本，见 PartsCheck-Devops-Engineer.output.json

它甚至明确说“这不是 pure ops role”，这很符合你现在样本池的总体趋势。

4. 软件与平台混合画像

典型组合：

backend_engineering + aws + docker + aws_cdk + nestjs
full_stack_engineering + react + typescript
再加上新增的 Primary Health 这种岗位，你会发现很多公司在招的其实不是纯平台，也不是纯软件，而是：

偏软件的人要懂平台
偏平台的人要能写后端
更看重工程闭环而不是岗位标签
Primary Health 就很典型。它当前被归到 software_engineering，但其实明显是 platform / backend / infra 混合型，见 Primary-Health-Co-Pty-Ltd-Senior-Platform-or-Software-Engineer.output.json

这也是为什么本轮出现了 critical_taxonomy_gaps = ["full_stack_role_family"]。

五、新样本带来的最重要变化

1. Platform Engineering 现在是明确主线

之前样本里平台工程是隐含的，这一轮之后已经明确成型。

尤其是这几类新样本在强化这一点：

Vicinity
Auto & General
Primary Health
Department 这类 systems/platform 方向样本
这说明后续分析不应该只盯 DevOps，而应该把 Platform Engineering 单独拉出来作为观察轴。

2. 工作权限已经成为高频现实门槛

work_rights_required = 9，这非常关键。

它现在已经不是边角信息，而是这一批 JD 里的高频条件之一。

这说明如果你未来要把这个项目往“实用型岗位分析”推进，work rights / PR / sponsorship / clearance 这些约束要成为正式分析维度，而不是附注。

3. 现在出现了两类超出当前 rules-first taxonomy 舒适区的样本

keep_in_intake = 2 分别是：

Department of Local Government, Industry Regulation and Safety
Yokogawa Australia & New Zealand
这两个样本很有代表性，因为它们说明你当前 taxonomy 还是偏：

software/platform/devops/cloud application engineering
但对下面这类岗位还不够强：

enterprise IT infrastructure
systems/platform operations
network/storage/virtualisation-heavy infra roles
on-prem + Azure + infrastructure support 型岗位
也就是说，当前 taxonomy 不是坏掉了，而是边界被看清了。

4. 标题和真实角色的偏差越来越明显

这一轮有两个特别典型的信号：

Primary Health 标题是 Senior Platform / Software Engineer，当前归到了 software_engineering，但实际是平台、后端、infra 混合型
Vicinity 当前被识别为 platform_engineering 是合理的，但 seniority = lead 很可能是被正文里的 “Lead post-incident reviews” 这种句子误触发，不一定真的是 title seniority
这说明下一轮如果继续优化 rules，优先级应放在：

title-first seniority 进一步收紧
mixed-role / hybrid-role family 表达
infrastructure-heavy / systems-heavy role family 扩展
六、对新增样本的初步判断

你新加的这批里，我会先这样看：

优先值得保留和继续观察的：

Vicinity
Codex Consulting
PartsCheck
Primary Health
Omega
Yokogawa
原因：

它们把平台、云、企业级基础设施、可观测性、工作权限门槛这些信号拉得更清楚
能明显扩展你现在样本池的结构密度
对后续 taxonomy 调整有直接价值
其中几个特别值得注意：

Vicinity：很强的平台工程样本，但当前 seniority 推断有噪声
Primary Health：明显提示你需要更好处理 platform/software/full-stack/backend 混合角色
Yokogawa：提醒你“企业 IT infra”是一条与云原生平台工程不同但相邻的赛道
Department：提示政府/系统平台样本不能只按软件 JD 的词表去读
七、这批样本反映出的市场信号

如果把这批 17 个样本再压缩成更接近市场判断的话，我会总结成 5 点：

企业越来越想要“平台化交付能力”，不只是传统运维
IaC、容器、CI/CD、云平台已经形成标准底座
软件开发和平台工程的边界正在继续变薄
工作权限、PR、背景审查等现实门槛在澳洲岗位里很常见
平台工程之外，还有一条值得单独追踪的 enterprise IT infrastructure 邻近赛道