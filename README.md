# arch-jiagou · 架构选型落地与 Agent 约束方法

把「怎么做架构选型」固化成 AI Agent 能照着执行、能被脚本检查的一套方法。它是一个 Agent Skill（技能名 `arch-jiagou`），在 Claude Code、Codex 等支持 SKILL.md 的工具里点名使用。

一次运行交付五类产物，缺一项不算完成：

| 产物 | 内容 | 落点 |
|---|---|---|
| 选型表 | 13 个决策轴，每轴写选定、否决、代价 | `SELECTION.md` + `SELECTION.json` |
| 标准架构图 | 上下文、容器、后端分层、前端外壳、数据域、权限、授权、部署、业务主链共 9 幅 Mermaid，索引里标明每幅的状态 | `docs/架构图/` |
| Agent 约束（Harness） | 根 `AGENTS.md`（以按需加载表开头）+ 前端 / 后端 / 数据 / 测试 / 研发流程分层 AGENT | `AGENTS.md`、`agent/` |
| 项目特化入口 | 词表、角色细表、脚本清单，与架构约束隔离 | `docs/项目特化/` |
| 代码脚手架 | 官方 init 基线 + 经验增量，生成后用浏览器真实验收 | `vue/`、`server/` 等 |

## 流程

1. **访谈**：按 [interview.md](interview.md) 先问分岔题（部署在客户侧还是云、Go 还是 Python、轻后端还是标准分离、数据量、授权、AI 接入、目标系统版本……），用联动规则预填默认值，每轮不超过 5 题。
2. **定原型**：从 6 个原型里选一个（[archetypes.md](archetypes.md)），没有匹配的就列差分、命名新原型。
3. **填选型表** → **出架构图** → **生成分层 AGENT**（模板在 [templates/](templates/)）。
4. **生成脚手架并验收**：`scaffold/init.py` 生成，`scaffold/verify.py` 验收。
5. **机器自检**：`scaffold/check-harness.py --render`，退出码为 0 才算完成。

## 原型与脚手架支持

| 原型 | 典型场景 | 技术栈 | init 支持 |
|---|---|---|---|
| `erp-go-vue-pg` | 客户内网 ERP，多岗位单据链 | Vue 3 + Element Plus；GoFrame；PostgreSQL | 支持 |
| `intranet-go-exe` | 客户 Windows 内网（含 Win7），单 exe 交付 | Vue 3；Go 1.20 + GoFrame v2.7（后端托管前端）；SQLite / PG | 支持（Win7 实机待验证） |
| `ai-go-python-sidecar` | 客户侧，AI 能力依赖 Python 生态 | Go 主后端 + FastAPI 侧车 | 支持 |
| `light-python-sqlite` | 单人自用，业务规则少 | Python 标准库 + SQLite + 单 HTML | 支持 |
| `ai-python-instance` | AI 问答，一客户一实例 | FastAPI + Redis + Docker | 只出文档 |
| `saas-bff-pg` | 云端多租户 | Go 或 Node BFF + PG | 只出文档 |

脚手架 = **官方 init**（create-vue、gf init、python -m venv）+ **经验增量**（overlay）。基线随官方升级，skill 只沉淀增量，例如：

- 前端：`layouts/` 唯一外壳、`views/<模块>/<功能>/index.vue`、`api/request.ts` 唯一请求入口、`components/common/` 统一样式组件、`utils/` 纯函数、`styles/` 设计令牌。
- 后端：`api/<业务>/v1/<业务>.go` 一个业务一个文件；controller 一行转调；`logic/<业务>/<场景>.go` 一个场景一个文件，测试放同目录；不设 service 层。

每个增量的明细（基线表 / 增量表 / 删改表）见 `scaffold/*.md`。

## 快速开始

环境：Node 22.18+、Go 1.25+ 与 GoFrame CLI（gf）、Python 3.11+、本机 Chrome、Python Playwright。依赖默认走国内镜像（npmmirror、goproxy.cn、清华 PyPI）。

```bash
S=~/.agents/skills/arch-jiagou        # 本仓库克隆到这里
T=/tmp/demo-project                            # 先在沙箱目录试

python3 $S/scaffold/init.py   --selection $S/examples/dry-run-acme-quote/SELECTION.json --target $T
python3 $S/scaffold/verify.py --selection $S/examples/dry-run-acme-quote/SELECTION.json --target $T
```

`verify.py` 会做这些：前端类型检查与构建；`go vet`、`go test`、`go build`；起服务查健康检查；打开有头浏览器走正例和反例。约定端口被占用时直接失败，不会换端口另起一份。完整演练见 [examples/dry-run-acme-quote/](examples/dry-run-acme-quote/)。

## 目录

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 技能入口：硬闸门、步骤、自检清单 |
| `interview.md` | 选型访谈题库（A–M 节、联动规则、原型映射、SELECTION.json 字段） |
| `axes.md` / `archetypes.md` | 13 个决策轴 / 6 个原型 |
| `diagrams/` | 9 幅标准架构图模板与质量闸门 |
| `templates/` | 分层 AGENT 模板 |
| `global-agents.md` + `templates/AGENTS.inherited.md` | **完整继承**§2/§3/§4（GitHub 用户不依赖作者 `~/AGENTS.md`） |
| `scaffold/` | 脚手架说明、overlay 增量、`init.py` / `verify.py` / `check-harness.py` |
| 其余 `*.md` | 专册：流程族、模块金样、双说明书、数据保护、前后端工程横切、Web Push、测试验收、活文档等 |
| `examples/` | 绿场演练（acme-quote）与样板 ERP 金样说明 |

## 来源

方法和默认值来自作者的多个真实项目：ERP、单人办公项目、AI 审核（Go + Python AI 侧车）、AI 问答（一客户一实例）、授权签发后台、Win7 内网单 exe 交付。所有清单都是**举例而非穷举**，遇到新场景按同样格式增补。
