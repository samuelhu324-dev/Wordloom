一、先说结论

这批 system admin 岗位已经明显超出了当前框架最擅长的那条主线。

当前框架原本更擅长识别的是：

cloud engineering
devops
platform engineering
backend / software / full stack
但你这批新样本更多是在考察另一条岗位带：

systems administration
enterprise infrastructure
desktop / endpoint support
Microsoft environment administration
workplace / identity / endpoint operations
IT support in enterprise environments
所以结论很明确：

现有内容需要补齐。

不是说框架失效，而是说它现在对 system admin / enterprise IT infrastructure 这条线的表达能力还不够，导致大量样本被误压成 unknown、sre 或 devops。

二、本轮 systemadmin 子集的结果

这批共 8 份样本。

decision 分布：

keep_in_intake = 6
promote_to_reviewed = 2
role family 分布：

platform_engineering = 1
sre = 2
devops = 1
其余大量样本其实接近 unknown
top skills：

azure = 5
powershell = 3
work_rights_required = 3
aws = 2
这个结果本身就说明问题：

如果一批明显属于 systems / desktop / Microsoft infra / endpoint admin 的样本，最后只被识别成少量 platform/sre/devops，那不是市场只有这些角色，而是 taxonomy 还没把这条赛道正式建出来。

三、这批岗位的真实结构是什么

这批样本不是云原生平台岗的简单变体，而是另一种很稳定的企业 IT 岗位结构。

我会把它们分成 4 类。

1. 企业系统管理 / Microsoft 基础设施管理

代表样本：

Bowens
Robert Half Systems Administrator
Cadence Connect
MFTE
这一类岗位的核心不是“交付 Kubernetes 平台”，而是：

Microsoft 365
Entra ID / Azure AD
Intune / endpoint manager
Group Policy
Active Directory
PowerShell
Azure infra
backup / VPN / access control
endpoint / identity / device lifecycle
这类岗位更像：

systems_administration
microsoft_infrastructure_admin
identity_endpoint_admin
而不是 devops 或 sre。

2. Desktop / EUC / Endpoint Support

代表样本：

Olympus Desktop Support Engineer
这个岗位非常典型，核心是：

desktop support
MECM / configuration manager
patching
application packaging
Essential 8 compliance
Defender for Endpoint
Service Desk escalation
它本质上更接近：

desktop_support
endpoint_operations
euc_support_engineering
当前框架没有这条 role family，所以只能落成 unknown，这很正常。

3. Enterprise IT Support / Integration Support

代表样本：

Robert Half IT Support Engineer - Enterprise Healthcare Systems
这个岗位也不适合落到 sre。

它的核心是：

enterprise healthcare systems support
remote support
installation / upgrade / integration
client-server software deployment
hardware-software boundary support
enterprise stakeholder handling
这类岗位更像：

it_support_engineering
enterprise_systems_support
technical_support_engineering
不是站点可靠性工程。

4. Hybrid systems / platform / integration administration

代表样本：

UnitingCare
Department of Local Government
这类样本比较混合，带有：

Azure integration platform
systems/platform maintenance
security / patch / change / release
business continuity
user support
operational IT platform ownership
这类岗位介于：

platform_operations
systems_engineering
integration_platform_admin
之间。

它们不是纯 devops，也不完全是软件平台工程。

四、当前框架哪里不够

这次暴露出来的问题很具体，不是抽象上的“不够”。

1. 缺角色族

这是最核心的缺口。

当前 framework 至少需要新增一组 systemadmin 向的 role family，比如：

systems_administration
desktop_support
it_support_engineering
enterprise_infrastructure
endpoint_management
identity_and_access_administration
否则这批岗位会持续被误塞进 sre、devops、platform_engineering，或者干脆掉成 unknown。

2. 缺 Microsoft / enterprise IT 事实层

当前 facts 更偏：

cloud platforms
IaC
containers
observability
CI/CD
backend frameworks
但 system admin 岗真正高频的词是：

Active Directory
Group Policy
Entra ID / Azure AD
Microsoft 365 / Office 365
Intune
MECM / SCCM
Defender for Endpoint
SharePoint
Exchange Online
Teams
VPN
endpoint management
device lifecycle
patching
imaging
service desk
ITIL
VMware / Hyper-V
DNS / DHCP / VLAN / switching / routing
firewall / segmentation
backup / business continuity
这些当前基本没有形成稳定 fact groups。

3. 角色推断有明显误判

几个例子很典型。

MFTE 被判成了 sre，但它其实更像 Windows infrastructure / systems admin。
见 MFTE-Staffing-Service-Systems-Engineer-Window-Infrastructure.output.json

Olympus 被判成 unknown，但它其实非常明确是 desktop support / endpoint support。
见 Olympus-Technology-Services-Pty-Ltd-Desktop-Support-Engineer.output.json

Robert Half 的 Azure & M365 岗也被落成 unknown，但它其实是非常清楚的 Microsoft systems administration。
见 Robert-Half-Systems-Administrator-Azure-Microsoft-365.output.json

Robert Half Enterprise Healthcare Systems 被判成 sre，这个也不对，它更接近 enterprise IT support。
见 Robert-Half-IT-Support-Engineer-Enterprise-Healthcare-Systems.output.json

4. 现有规则还有几类噪音匹配

这批 systemadmin 样本还暴露出几个规则层问题：

lead 会被正文里的 “Lead projects” 误触发 seniority
staff 会被组织介绍或 company text 误触发
remote 会被 “remote support” 误识别成 work arrangement
on_site 会被 “on-site parking” 或场景描述误识别
go 会被普通英文短语误击中，像 UnitingCare 那个 go 很明显不是 Go 语言
所以除了加 role family，还要继续收紧 phrase boundary 和 title-first inference。

五、这批岗位主要在要什么能力

如果只从 system admin 这批样本来看，主轴不是云原生交付，而是“企业基础设施与终端/身份/环境管理”。

最主要的能力块有这些：

1. Microsoft 生态运维与管理

Azure
Microsoft 365
Entra ID / Azure AD
Intune
SharePoint
Exchange
Group Policy
Active Directory
2. 终端与设备管理

MECM / SCCM
packaging
patching
imaging
endpoint protection
desktop fleet maintenance
3. 系统与网络基础设施

Windows server
virtualization
DNS / DHCP
VLAN / routing / switching
VPN
firewalls
backups
4. 自动化与脚本

PowerShell
Python
configuration management
some Ansible exposure
5. 运营与支持能力

escalation
incident handling
BAU support
Service Desk coordination
documentation
operational resilience
business continuity
这说明 system admin 这条线和你前面分析的 DevOps / Platform / Cloud 主线，确实是相邻但不同的能力市场。

六、这批样本给你的真正启发

这批 system admin 样本非常有价值，因为它让边界更清楚了：

你现在的项目，已经不只是“JD 里的云工程与软件工程分析工具”，它开始逼近一个更完整的 “技术岗位能力谱系分析工具”。

也就是说，岗位谱系现在至少有两大片：

第一片：产品/平台/云交付

software engineering
backend engineering
full stack engineering
devops
cloud engineering
platform engineering
第二片：企业基础设施/终端/系统运维

systems administration
desktop support
enterprise IT support
endpoint / identity administration
infrastructure operations
你这批 system admin 样本，实际上是在给第二片补地基。

七、我的判断：现有内容需要怎么补齐

如果按优先级排，我建议补这 3 层。

第一优先级：补 role family
最该加的是：

systems_administration
desktop_support
it_support_engineering
enterprise_infrastructure
这一步最重要，因为现在最大问题不是 facts 少，而是角色落点不对。

第二优先级：补 fact groups
建议新增或扩展：

identity_and_directory
endpoint_management
microsoft_stack
networking_and_datacentre
virtualization_and_server_ops
service_management_and_support
security_and_compliance_ops
第三优先级：修规则噪音
重点修：

seniority 误判
remote/on-site 误判
programming language 噪音触发
support / systems / desktop 相关 title-first inference
八、当前这批 system admin 样本里，哪些最值得作为下一轮规则校准样本

我会优先拿这 5 个做 taxonomy calibration：

MFTE
Olympus
Robert Half Systems Administrator
Robert Half IT Support Engineer
Bowens
原因很简单：

它们覆盖了 system admin 这批里最典型的几种岗位变体
当前误判最明显
一旦把这几份校准好，systemadmin 这条线会立刻清晰很多
九、中文总结

一句话总结这批样本：

这批 system admin 岗位证明，当前工具已经能分析云/平台/软件工程主线，但对“企业 IT 基础设施与终端系统运维”这条岗位谱系还没有正式建模，因此现有内容确实需要补齐，而且应该优先补 role family 与 Microsoft/endpoint/networking 相关事实层。