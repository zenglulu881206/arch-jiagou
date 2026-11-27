# 架构原型（Archetypes）

先选原型，再填轴差分。未知场景：相对最近原型列差分后命名新原型。

## erp-go-vue-pg（金样：样板 ERP）

| 项 | 定案 |
|---|---|
| 场景 | 制造业/贸易 ERP；内网或单机部署；多岗位 |
| FE | Vue 3 + TS + Element Plus + Vite |
| BE | Go + GoFrame（api→controller→logic→dao；logic 按业务场景拆文件，不设 service 层） |
| DB | PostgreSQL 多业务 schema |
| 形态 | nginx 静态 + API 本机端口；标准分离 |
| 授权 | 机器码申请码 + license 验签；私钥仅 admin |
| 自留地 | `admin/` 打包/清洗/签发，不进运行包 |
| 图 | 01–09 全要 |
| Harness | 全套 AGENT + admin/AGENTS；**前后端 AGENT 含完整脚手架树** |
| 代码脚手架 | `scaffold/init.py` 已支持并实测（create-vue 3.24.0 + gf v2.10.5） |
| 金样 | [examples/erp-sample.md](examples/erp-sample.md) |

## intranet-go-exe（实例：Win7 内网项目）

| 项 | 定案 |
|---|---|
| 场景 | 客户 Windows 内网（老旧机房等），常要兼容 Win7 / Server 2008 R2；少量用户 |
| FE | Vue 3 + UI 库，构建产物由后端进程托管（`SetServerRoot`） |
| BE | Go + GoFrame；Win7 线锁 Go 1.20.x + GoFrame v2.7.x，钉 x/sys v0.15.0、otel v1.21.0，用单独工具链交叉编译 |
| DB | SQLite（纯 Go 驱动）存账号配置；业务库 PG；常只读对接客户既有业务库（Oracle / PG） |
| 形态 | 一个 exe + 资源目录交付，无 nginx、无 Docker |
| 授权 | 机器码 + 到期日，RSA 验签（机器码不含程序路径） |
| 图 | 08 画成单进程；02 无 nginx |
| 代码脚手架 | 已支持：`deploy.shape=single-binary`（webhost 托管前端）、Win7 钉版本、SQLite；Win7 实机运行待验证 |

## ai-go-python-sidecar（实例：AI 审核项目）

| 项 | 定案 |
|---|---|
| 场景 | 客户内网私有化；业务主链要稳定，AI 能力依赖 Python 生态 |
| FE | Vue 3 + UI 库 |
| BE | Go 主后端（业务、权限、授权）+ Python FastAPI 侧车（RAG、OCR、模型调用），由 Go 拉起 |
| DB | SQLite 主库 + Chroma 向量库；对接客户库用 PG / Oracle 驱动 |
| AI | 本地 Ollama + 在线 DeepSeek；业务明细不出网，只发聚合指标；SSE 流式 |
| 授权 | 机器码 license + 加密规则数据包；Python 自研代码 Cython 编译 |
| 代码脚手架 | 已支持：`backend.sidecar` 开启后生成 Python 侧车（FastAPI）与 Go 侧进程管理（见 `scaffold/python-sidecar.md`）；Cython 编译只出文档 |

## ai-python-instance（实例：AI 问答项目）

| 项 | 定案 |
|---|---|
| 场景 | AI 问答类产品；一客户一实例，各自独立域名 |
| BE | Python FastAPI 全异步 + Redis（会话、缓存、防重放） |
| DB | 本地 SQLite 主库，单向异步同步到云端 PG；Chroma 多知识库 |
| 形态 | Docker Compose（Linux / macOS） |
| 授权 | 机器码在宿主机校验，容器内只验签名和到期 |
| 代码脚手架 | 可复用 python-sidecar 的目录结构；Redis、Docker Compose 暂只出文档 |

## light-python-sqlite（实例：单人办公项目；原 tool-python-sqlite）

| 项 | 定案 |
|---|---|
| 场景 | 单人或个人自用、业务规则少；单机工具、离线清洗界面也归这类 |
| FE | 单 HTML 或极简 Vue；依赖可走 CDN |
| BE | Python 标准库或 FastAPI，只做存取（轻后端） |
| DB | SQLite 或文件 |
| 授权 | 常 N/A；URL 公开前必须补登录 |
| 图 | 07 可 N/A；02/08 简化 |
| Harness | 精简根 AGENTS + 测试/流程；可无前后端分册 |
| 代码脚手架 | 已支持：`light` 开启后生成标准库后端 + 单 HTML（见 `scaffold/light-python.md`） |

## saas-bff-pg

| 项 | 定案 |
|---|---|
| 场景 | 多租户 SaaS；公有云 |
| FE | Vue3+EP 或同级 |
| BE | Go 或 Node BFF |
| DB | PG（常单库租户隔离或 schema-per-tenant） |
| 授权 | 订阅/租户级，未必锁机器码 |
| 图 | 01 加租户与 IdP；07 按订阅模型改 |
| 差分相对 erp | 多租户、云部署、身份提供商；能力装配仍可用 |
| 代码脚手架 | Go 后端可复用 goframe overlay；Node BFF 暂未提供 overlay |

## 选型规则

1. 单据链 + 库存过账 + 现场包 → 优先 `erp-go-vue-pg`。
2. 单人、无并发写、规则少 → `light-python-sqlite`。
3. 客户 Windows 内网（尤其 Win7）→ `intranet-go-exe`。
4. 客户侧且 AI 依赖 Python 生态 → `ai-go-python-sidecar`；纯 AI 问答、一客一实例 → `ai-python-instance`。
5. 多租户云端 → `saas-bff-pg`，勿生搬锁机器码 license。
6. TinyVue / TDesign：客户或既有产品线指定时用（AI 审核项目、AI 问答项目、授权签发后台用 TinyVue，Win7 内网项目用 TDesign）；否则用 Element Plus。
7. 判定顺序与题目见 [interview.md](interview.md) 第 2 节联动规则。
8. 合同 PDF 岗位脱敏、仓储 2.5D 货位墙等横切能力从 [capabilities.md](capabilities.md) 单独推荐；它们不构成新 archetype，也不默认生成代码。
