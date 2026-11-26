# 选型访谈题库

> 题目和默认值来自 6 个真实项目：样板 ERP（客户内网，Go+PG）、单人办公项目（云，Python 轻后端+SQLite）、AI 审核项目（客户内网，Go 主 + Python AI 侧车）、AI 问答项目（一客户一实例，Python+Redis）、授权签发后台（云，Go）、Win7 内网项目（客户 Windows 7 内网，Go 单 exe）。
> 题目**举例非穷举**：遇到新场景按同样格式增补，并注明出处项目。

## 0. 用法

1. **先问分岔题，后问细节题**：按 A → M 顺序。A–I 节会改原型或技术栈，必须先定；J–M 在原型定了之后再问。
2. **预填默认值**：先按第 2 节的联动规则推出默认值，整张表预填好，只问「何时必问」命中的题，每轮 ≤5 题。用户说「按默认」就全部取默认。
3. **一题一判定**：每题的答案都要落到「影响」列写的产物上：选型表某轴、`SELECTION.json` 某键、某份 AGENT、某幅图。答案不影响任何产物的题，删掉不问。
4. **双写**：答案同时写进 `SELECTION.md`（13 轴：选定 / 否决 / 代价）和 `SELECTION.json`（第 3 节字段）。
5. **惯例不问**：与金样同构的决策（闸门、回写、幂等下推、弹窗三类等）不进访谈，直接按默认定案。

## 1. 题库

### A. 身份与协作

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| A1 | 项目里 agent 怎么称呼你？ | 默认跟随全局规则（如「鲁大师」） | 项目给别人用，或全局规则没定义时 | 写进根 AGENTS「顾问立场」 | `identity.address` |
| A2 | 沟通和界面用什么语言？ | 简体中文 | 有海外用户时 | 根 AGENTS「交流语言」；界面 i18n 要不要做 | `identity.language` |
| A3 | 项目属于什么领域，agent 应以什么专家身份判断？ | 按 B 节推断（ERP 业务、行业合规、信息化…） | 始终 | 根 AGENTS 顾问立场的领域角色 | `identity.expert_roles` |
| A4 | 界面读者是谁，是不是非技术人员？有哪些必须用的行业词、禁用的技术词？ | 业务操作者，非技术人员 | 始终 | 前端 AGENT 文案约定；单人办公项目的教训是界面禁止出现「SQLite / API / 缓存」等词 | `identity.audience` |
| A5 | 有哪些模型可用于多 agent 协作（执行 / 审查 / 测试）？ | 按全局规则 | 要走完整多 agent 时 | 研发流程 AGENT「模型与协作」 | — |

### B. 部署位置（第一个分岔）

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| B1 | 部署在客户侧（客户内网 / 客户机器），还是我方或云服务器？ | 客户侧 / 云服务器 / 本机自用 | 始终 | 决定 C 节语言默认值、G 节是否授权、J 节部署方式 | `deploy.site` |
| B2 | 一个客户一套实例，还是多个客户共用一套（多租户）？ | 客户侧默认一客一套；云端要问 | 云服务器时 | 多租户要在数据层加租户键；AI 问答项目是一客户一实例 + 独立域名 | `deploy.tenancy` |
| B3 | 目标机器能不能上外网？ | 客户侧默认不能 | 客户侧时 | 离线就要整包交付依赖、模型和镜像；在线 AI 能不能用 | `deploy.network` |
| B4 | 需要分开发 / 演示 / 生产三套环境吗？ | 需要 | 有演示环境时 | AI 审核项目用三环境表区分强约束：生产去 sourcemap、日志脱敏、密钥不硬编码 | `deploy.envs` |

### C. 后端语言（Go 还是 Python）

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| C1 | 有多少用户？同时在线和并发写入大概多少？ | 单人 / 10–50 人 / 百人以上 | 云服务器时必问；客户侧也要问（会影响 F 节选库） | 多用户、高并发时选 Go；单人或低并发时 Python 也可以 | `scale.users`、`scale.concurrency` |
| C2 | 交付后要防止源代码泄漏吗？ | 客户侧默认要；我方服务器默认不要 | 云服务器时 | 要防泄漏就首选 Go（编译成二进制，`-trimpath -ldflags "-s -w"`）。Python 只能编译自研代码（Cython 编成 .so/.pyd，或只发 .pyc），而且需要专门的构建机：AI 审核项目用 Nuitka 编译 7GB 依赖时在 8GB 机器上内存溢出，Windows 的 .pyd 还要单独的 Windows 构建机 | `code_protection` |
| C3 | 核心能力是否依赖 Python 生态（RAG、向量库、OCR、文档解析、数据分析）？ | 否 | H 节选了 AI，或有重数据处理时 | 依赖就做成「Go 主后端 + Python 侧车服务」（AI 审核项目：由 Go 启动时拉起 FastAPI 服务），业务主链仍在 Go；纯 AI 问答类产品可以整体用 Python（AI 问答项目） | `backend.sidecar` |
| C4 | 团队维护者熟悉哪门语言？已有可复用的代码在哪门语言里？ | 跟随已有项目 | 有已有代码时 | 复用优先：授权签发后台和 Win7 内网项目共用一套 GoFrame 骨架 | — |

**默认规则**：客户侧首选 Go。云服务器时，只要 C1 是多用户或高并发、C2 要防泄漏，二者中任一项成立就选 Go；否则在 Python 和 Go 之间按 C3、C4 定。

### D. 架构形态

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| D1 | 轻后端还是前后端标准分离？ | 标准分离 | 单人或个人自用、业务规则少时 | **轻后端**：后端只做存取（如 单人办公项目用 Python 标准库加 SQLite 存键值，业务逻辑全在前端单页），零依赖、上手快，代价是多人同时编辑会互相覆盖，权限做不了后端强制。**标准分离**：规则、权限、计算都在后端（样板 ERP） | `shape` |
| D2 | 前端怎么交付：nginx 托管、后端进程直接托管、还是单个 HTML 文件？ | 有 nginx 用 nginx；客户 Windows 内网用后端托管 | J 节不用 nginx 时 | Win7 内网项目用 Go 进程托管前端（`SetServerRoot`），一个 exe 加资源目录就能交付；单人办公项目是单 HTML 文件，必须通过网址同源访问，双击 `file://` 打开时连不上接口 | `deploy.shape` |
| D3 | 前端需要构建流程（Vue + Vite）吗？ | 需要 | 轻后端时 | 不用构建会省事，代价是单文件越写越长、多份副本要手工同步（单人办公项目有两份 HTML 要保持一致） | `frontend.build` |

### E. 终端

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| E1 | 只用 PC、只用手机，还是 PC 和手机都用？ | PC + 手机 | 始终 | 决定前端 AGENT「PC/手机」表，以及布局壳是否要做窄屏 | `clients.pc`、`clients.mobile` |
| E2 | 手机端用什么形式：浏览器 H5、添加到主屏幕（PWA）、App 壳、小程序？ | H5 | E1 含手机时 | 要系统通知栏推送就走 PWA 或 App 壳（样板 ERP 两种都做了，见 web-push-pwa.md）；只是「添加到主屏幕」的话，加几个 meta 标签就够（单人办公项目） | `clients.mobile` |
| E3 | 手机上要扫码、拍照、定位吗？ | 否 | 有现场作业（仓库、巡检）时 | 扫码和拍照要 HTTPS，或者用 App 壳 | `clients.device` |
| E4 | 客户用的浏览器最低是什么版本？ | 近两年的 Chrome / Edge | 客户是老 Windows 时 | Win7 上 Chrome 最高只到 109，要核对 Vite 构建目标和 UI 库的浏览器下限 | `clients.browser_min` |
| E5 | 有没有指定 UI 规范（如华为 OpenTiny、TDesign）？ | Element Plus | 客户或已有项目指定时 | AI 审核项目、AI 问答项目、授权签发后台用 TinyVue，Win7 内网项目用 TDesign，样板 ERP 用 Element Plus；换 UI 库，前端 overlay 要跟着换 | `frontend.ui` |

### F. 数据

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| F1 | 数据量多大，会不会稳定增长？是企业应用还是个人自用？ | 企业、持续增长 | 始终 | 数据量大、企业应用、稳定增长时选 PostgreSQL；数据量小、个人自用时选 SQLite | `database.engine` |
| F2 | 会不会有多人同时写同一批数据？ | 跟 C1 | 想选 SQLite 时 | SQLite 同一时刻只能一个连接写；多人并发写就算数据量小也选 PostgreSQL。单人办公项目是单人使用，所以 SQLite 够用 | `database.engine` |
| F3 | 要对接客户已有的数据库吗（客户业务系统、旧 ERP）？是只读还是要写回？对方是什么库？ | 否 | 替换旧系统或对接客户既有系统时 | Win7 内网项目有两种取数方式：厂商提供视图，或者厂商推送 JSON；客户库可能是 Oracle 或 PG，要另装驱动；连接串必须加密存放 | `integration.customer_db` |
| F4 | 有旧数据要迁入吗？有没有现成的样表？ | 否 | 始终 | 迁入要按旧表原样承接、整行保留不丢列（单人办公项目）；有旧系统时按只读四段调研（research-survey.md） | `data.legacy` |
| F5 | 数据要不要跨设备同步、防止丢失？谁来备份，多久备一次？ | 要；每日备份 | 始终 | 数据只存在浏览器 localStorage 会丢（单人办公项目后来改成服务器保存）；部署脚本绝不能删数据目录 | `data.backup` |
| F6 | 有没有向量检索、全文检索或缓存需求？ | 否 | H 节选了 RAG 时 | 向量库用 Chroma，配 BM25；会话、缓存、防重放用 Redis（AI 问答项目） | `database.extras` |
| F7 | 本地库和云端库要不要同步？ | 否 | 一客一实例且要集中管理时 | AI 问答项目：本地 SQLite 做主库，单向异步同步到云端 PG，云端挂了业务也不受影响 | `database.sync` |

### G. 授权与防泄漏

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| G1 | 需要系统授权吗？按机器绑定、按到期日、还是按模块？ | 客户侧要：机器码 + 到期日；云端不要 | 客户侧时 | 选型轴 11、架构图 07、admin 签发。机器码不要包含程序路径，否则目录一挪授权就失效（Win7 内网项目）；云主机和容器里读不到磁盘序列号或 machine-id，要在宿主机校验（AI 问答项目） | `license.*` |
| G2 | 授权由谁签发？私钥放在哪？ | 签发私钥只放在开发侧自留地或签发中心，运行包只带公钥 | G1 要授权时 | 授权签发后台是集中签发中心，私钥路径走环境变量；禁止像 Win7 内网项目那样把对称密钥写死在源码里 | `license.issuer` |
| G3 | 发布包要不要按客户裁剪功能模块？ | 否 | 一套代码卖多家客户时 | AI 审核项目按 9 个模块裁剪，前端、Go、Python 三端的模块 key 必须一致，不一致就拒绝启动；同时对应能力装配（轴 13） | `license.modules` |
| G4 | 部署包要不要加密，解压密码是不是单独给？ | 客户侧要 | 客户侧时 | AI 审核项目、AI 问答项目都用加密压缩包，密码单独提供 | `release.encrypt` |
| G5 | 有哪些敏感数据要加密存储、日志里要脱敏？ | 密码、密钥、连接串 | 始终 | 生产环境密钥太弱时拒绝启动（AI 审核项目对 JwtSecret 的处理） | `security.sensitive` |

### H. AI 接入

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| H1 | 需要接入 AI 模型或 AI 接口吗？用来做什么？ | 否 | 始终 | 选了就读 C3 判断是否加 Python 侧车 | `ai.enabled` |
| H2 | 用在线大模型、本地模型，还是两者都用？ | 有外网用在线；离线或数据敏感用本地 | H1 为是时 | 在线和本地用一个开关切换，不自动互切（AI 问答项目的 `LLM_BACKEND`）；接口按 OpenAI 兼容协议写，便于换供应商 | `ai.mode` |
| H3 | 哪些数据不能出客户网络？ | 业务明细不出网 | 客户侧加在线模型时 | AI 审核项目只把聚合指标发给在线模型改写报告 | `ai.data_egress` |
| H4 | 本地模型用哪个，跑在什么硬件上？ | Ollama + Qwen；模型从魔塔下载 | H2 含本地时 | 容器里用不了 mlx 模型，要换 GGUF；OCR 要约 10GB 可用内存；模型加载可能要 3–15 分钟，服务启动超时要放宽（AI 问答项目） | `ai.local_model` |
| H5 | 要知识库检索（RAG）、文档解析、OCR 吗？ | 否 | H1 为是时 | 向量库 Chroma + BM25 + 重排；embedding 用 bge-large-zh 并离线加载（`HF_HUB_OFFLINE=1`）；文档解析用 MinerU、PaddleOCR | `ai.rag` |
| H6 | 回答要逐字流式显示吗？ | 要，走 SSE | H1 为是时 | nginx 要关掉 SSE 路径的缓冲 | `ai.stream` |
| H7 | API 密钥放在哪、谁能改？ | 服务器配置文件，权限 0600，不进前端、不进日志 | H2 含在线时 | 运行时可改的密钥存到数据目录（AI 审核项目） | `ai.key_store` |

### I. 开发自留地

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| I1 | 要不要隔离一块开发侧自留地（打包部署、签发私钥、数据清洗、E2E 脚本），保证它不进客户运行包？ | 交付给客户要隔离；纯自用可以不隔离 | 始终 | 要隔离就生成 `admin/` 和 `admin/AGENTS.md`；运行包里没有 admin 也要能跑。Win7 内网项目的教训：项目根目录混放 Go 安装包、exe 和软著材料 | `admin_zone` |
| I2 | 旧数据清洗、预处理脚本放哪？原始文件可以改吗？ | 放在 `admin/`；原始文件只读 | F4 要迁入时 | 数据 AGENT「资产存放路径」 | — |

### J. 部署与运维

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| J1 | 要做一键部署脚本吗？在哪台机器上执行？ | 要；在开发机执行：问答 → 打包 → 上传 → 远程部署 | 始终 | 单人办公项目、样板 ERP、授权签发后台都是这个流程；支持只更新前端、只更新后端或整包 | `deploy.one_click` |
| J2 | 目标服务器是 Linux、Windows 还是 macOS？什么发行版、什么版本？ | Ubuntu 22.04 | 始终 | 部署脚本按系统分开写（AI 审核项目有 ubuntu 和 windows 两套模板）；macOS 用 launchd | `deploy.os`、`deploy.os_version` |
| J3 | 如果是 Windows，是哪个版本？ | Windows 10 / Server 2016 及以上 | J2 为 Windows 时**必问** | **Go 1.21 起不支持 Win7/8 和 Server 2008/2012**。要支持就锁定 Go 1.20.x + GoFrame v2.7.x，并钉 x/sys v0.15.0、otel 全家 v1.21.0，用单独的 1.20 工具链交叉编译（Win7 内网项目实机组合，init.py 自动钉）。Python 3.9 起也不支持 Win7。init.py 会拦下冲突的组合 | `deploy.os_version` |
| J4 | 有域名吗？要 HTTPS 吗？ | 云服务器有域名，用 certbot 申请证书，申请失败就先用 HTTP；客户内网用 IP 加 HTTP | 云服务器，或 E3 需要摄像头时 | 第三方集成、扫码拍照、PWA 推送都要求 HTTPS | `deploy.domain`、`deploy.https` |
| J5 | 用 nginx 吗？ | Linux 用 nginx 托管静态页面并反代 `/api`，后端只监听 127.0.0.1；Windows 内网由后端进程直接托管 | 始终 | 决定 D2 和架构图 08 | `deploy.nginx` |
| J6 | 进程怎么常驻：systemd、Windows 服务、launchd，还是容器？ | Linux 用 systemd | 始终 | 不要用 nohup 常驻（授权签发后台的现状：重启后不会自动拉起）；Windows 要不要注册成服务要问客户 | `deploy.service` |
| J7 | 要用 Docker 吗？ | 否；依赖多（AI 模型、OCR）时用 Docker Compose | H 节有本地 AI，或客户要求容器时 | 镜像源走 daocloud、阿里云；本机 Clash fake-ip 会污染镜像构建（AI 审核项目） | `backend.keep_docker` |
| J8 | 升级时怎么保住现场数据和配置？怎么回滚？ | 保留现场 config，按示例深合并补缺键；数据目录、license 永不覆盖；保留上一版本用于回滚 | 始终 | 架构图 08、admin AGENT | `deploy.upgrade` |
| J9 | 后端和前端用哪个端口？本机这些端口有没有被占用？ | 后端 8000、前端开发服 5173 | 本机已有其它服务时 | `verify.py` 遇到端口被占用直接失败，不换端口另起一份 | `backend.port`、`frontend.port` |

### K. 集成

| # | 题 | 选项 / 默认 | 何时必问 | 判定与影响 | 键 |
|---|---|---|---|---|---|
| K1 | 怎么登录：账号密码、钉钉 / 企业微信、单点登录？ | 账号密码 + JWT | 客户有统一身份系统时 | 样板 ERP 接了钉钉登录；轻后端在 URL 不公开时可以先不做登录（单人办公项目），但暴露到公网前必须补 | `auth.login` |
| K2 | 要给第三方系统开放接口吗？ | 否 | 有对接方时 | AppId + HMAC 签名 + 按 scope 限定路径（授权签发后台、Win7 内网项目）；行业有标准数据协议时优先用标准，不另起私有模型（AI 审核项目、AI 问答项目） | `integration.third_party` |
| K3 | 要推送消息吗？推到哪里：站内、手机通知栏、邮件、钉钉？ | 站内消息 | 有待办、到期提醒时 | 手机通知栏见 E2；到期提醒可以用定时任务发邮件（授权签发后台用 gcron） | `integration.push` |
| K4 | 文件和附件存在哪：本地磁盘还是对象存储？单个文件最大多大？ | 本地磁盘 | 附件多或要长期留档时 | nginx 的 `client_max_body_size` 要和后端上限一致（单人办公项目都是 100MB） | `storage.files` |
| K5 | 要打印、Excel 导入导出、定时任务吗？ | 导入导出要 | 始终 | 导入模板对齐客户现有表格；打印凭证要不要归档 | `features.io` |

### L. 业务与组织（原型定了之后再问）

| 轴 | 题 | 默认 | 何时必问 |
|---|---|---|---|
| 2 业务流程 | 主业务链从哪开始到哪结束？哪些下推是自动的、哪些要手动？有长进度条吗？ | 没有主观决策就自动下推；进度现算 | 始终 |
| 3 样式 | 客户有 VI 色或现成的设计规范吗？ | UI 库默认样式 + 设计令牌 | 客户给了规范时 |
| 4 调研 | 旧系统能只读访问吗？现有样表有哪些？ | 按只读四段采集 | F4 要迁入时 |
| 5 对象 | 有哪些部门和岗位？各自管什么？ | — | 始终 |
| 6 权限 | 员工按什么收窄可见数据？主管看全部吗？ | 员工按经办人收窄，主管看全部 | 有多角色时 |
| 6 枚举 | 哪些下拉选项要让客户自己维护（新增、排序、删除前检查有没有被引用）？ | 状态类写死，业务分类可维护 | 始终（单人办公项目的教训） |
| 12 验收 | 哪些帐必须核对：库存、金额、计数、工资？ | 按主链列出 | 有过账类业务时 |
| 13 能力装配 | 不同客户的流程有差异吗？ | 不做 | 一套代码给多家客户时 |

### M. 研发与验收

| # | 题 | 默认 | 何时必问 | 键 |
|---|---|---|---|---|
| M1 | 浏览器验收要有头还是无头？每步间隔多久？ | 有头，每步 0.8–1 秒 | 始终 | 测试 AGENT |
| M2 | 代码备份到哪？分支怎么管？ | GitHub 私有仓库，只保留 main + 一个过程分支 | 始终 | 研发流程 AGENT |
| M3 | 下载走哪些镜像？ | npmmirror、goproxy.cn、清华 pip、魔塔模型、daocloud 镜像 | 始终 | `.npmrc`、`GOPROXY` |

## 2. 联动规则（先推默认值，再决定问哪些题）

| 前提 | 推出的默认值 | 依据 |
|---|---|---|
| B1 = 客户侧 | 后端用 Go；要授权（G1）；要防泄漏（C2）；要隔离自留地（I1）；默认离线（B3） | 样板 ERP、Win7 内网项目、AI 审核项目 |
| B1 = 云服务器，且 C1 为多用户 / 高并发，或 C2 要防泄漏 | 后端用 Go | 授权签发后台 |
| B1 = 云服务器，且单人 / 低并发、不防泄漏 | 后端可用 Python；业务规则少时考虑轻后端（D1） | 单人办公项目 |
| H1 = 是，且 C3 依赖 Python 生态 | Go 主后端 + Python 侧车；客户侧时 Python 代码要编译（C2） | AI 审核项目 |
| F1 = 数据小 / 个人自用，且 F2 无并发写 | SQLite（纯 Go 驱动，免 CGO 交叉编译） | 单人办公项目、AI 审核项目 |
| F1 = 企业应用 / 稳定增长，或 F2 有并发写 | PostgreSQL，多业务 schema | 样板 ERP |
| J2 = Windows 且 J3 ≤ Win8 / Server 2012 | Go 1.20.x + GoFrame v2.7.x（钉 x/sys、otel）；`deploy.shape=single-binary` 后端托管前端（D2）；`clients.browser_min=chrome-109` | Win7 内网项目 |
| J4 需要 HTTPS，或 E3 要用摄像头，或 E2 = PWA | 必须有域名和证书 | 单人办公项目、授权签发后台 |
| H2 含本地模型 | 考虑 Docker Compose（J7）；核对内存（H4） | AI 问答项目 |

### 原型映射

| 原型 | 典型答案组合 | 实例 | init.py 支持 |
|---|---|---|---|
| `erp-go-vue-pg` | 客户侧、多用户、标准分离、PG、授权、自留地、nginx | 样板 ERP | 已支持 |
| `intranet-go-exe` | 客户 Windows 内网（含 Win7）、后端托管前端、SQLite 或 PG、授权 | Win7 内网项目 | 已支持（`deploy.shape=single-binary` + Win7 钉版本）；Win7 实机待验证 |
| `ai-go-python-sidecar` | 客户侧、Go 主业务 + Python AI 侧车、SQLite + 向量库、本地或在线模型 | AI 审核项目 | 已支持（`backend.sidecar`）；Cython 编译只出文档 |
| `ai-python-instance` | 一客户一实例、Python FastAPI + Redis、Docker、本地或在线模型 | AI 问答项目 | 暂只出文档（目录可参照侧车） |
| `light-python-sqlite` | 云单机、单人、轻后端、单 HTML、SQLite | 单人办公项目 | 已支持（`light`） |
| `saas-bff-pg` | 云端多租户、身份提供商、订阅授权 | — | Go 后端可复用 goframe overlay |

## 3. SELECTION.json 字段

`init.py` 会读取的键标 ★，其余键只用于生成文档（AGENT、架构图）和自检。

```json
{
  "identity": { "address": "鲁大师", "language": "简体中文", "expert_roles": ["ERP 业务", "贸易流程"], "audience": "业务员与主管，非技术人员" },
  "project": { "name": "acme-quote", "title": "报价管理" },
  "archetype": "erp-go-vue-pg",
  "deploy": {
    "site": "customer", "tenancy": "single", "network": "offline", "envs": ["dev", "demo", "prod"],
    "os": "linux", "os_version": "22.04",
    "shape": "nginx-split", "nginx": true, "domain": "", "https": false,
    "service": "systemd", "one_click": true, "upgrade": "keep-config-merge"
  },
  "scale": { "users": "10-50", "concurrency": "low" },
  "code_protection": "go-binary",
  "clients": { "pc": true, "mobile": "h5", "device": [], "browser_min": "chrome-109" },
  "license": { "enabled": true, "bind": "machine", "expire": true, "modules": false, "issuer": "admin" },
  "ai": { "enabled": false, "mode": "none", "data_egress": "aggregate-only", "rag": false, "stream": "sse" },
  "admin_zone": true,
  "frontend": {
    "dir": "vue", "port": 5173, "create_vue": "3.24.0",
    "features": ["ts", "router", "eslint", "prettier"], "element_plus": "2.14.8"
  },
  "backend": {
    "dir": "server", "module": "acme-quote", "port": 8000, "goframe": "v2.10.5",
    "sidecar": false, "keep_docker": false, "keep_kustomize": false
  },
  "light": null,
  "database": { "engine": "pgsql", "name": "acme_quote", "user": "acme_quote" }
}
```

★ init.py 读取的键：`frontend.*`、`backend.*`、`database.engine/name/user`、`deploy.os/os_version`（Win7 校验）、`admin_zone`（决定验收入口放 `admin/scripts/` 还是 `scripts/e2e/`）。

- 后端托管前端（单 exe 交付，无 nginx）：`"deploy": { …, "shape": "single-binary" }`。
- 浏览器下限：`"clients": { …, "browser_min": "chrome-109" }` 会写进前端 `build.target`。
- 开 Python 侧车：`"backend": { …, "sidecar": { "dir": "sidecar", "port": 18002 } }`（需 Python 3.11+）。
- 轻后端：不写 `frontend`、`backend`，改写 `"light": { "dir": "app", "port": 8080 }`（需 Python 3.9+）。

版本号是 2026-11 实测通过的组合：create-vue 3.24.0、Element Plus 2.14.8、GoFrame v2.10.5（Go 1.25）。Win7 线已实测：Go 1.20.14 + GoFrame v2.7.0 + x/sys v0.15.0 + otel v1.21.0 + SQLite，后端托管前端，verify 全过并交叉编译出 Windows exe；Win7 实机运行待验证（验证包步骤见 `scaffold/goframe.md`）。升级任何版本都要重跑 `scaffold/verify.py`，并同步 `scaffold/vue3.md`、`scaffold/goframe.md` 的基线表。
