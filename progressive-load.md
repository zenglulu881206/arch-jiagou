# 按需读取（省 token）

两层都要按需：**跑 skill 时怎么读 skill 文件**；**生成的项目 harness 怎么让后续 agent 读**。

## A. 跑本 skill 时（agent 读 skill）

默认只读 `SKILL.md`。下表之外的文件**禁止预读整份**。

| 文件 | 何时读 |
|---|---|
| `SKILL.md` | 点名本 skill 后始终先读 |
| `global-agents.md` | 生成/审查 harness 与全局 `~/AGENTS.md` 结合时 |
| `archetypes.md` | 定场景 / 锁原型 |
| `interview.md` | 第 2 步访谈；写 SELECTION.json 时 |
| `scaffold/vue3.md` / `scaffold/goframe.md` | 第 6.5 步生成脚手架；写前后端 AGENT 目录树时 |
| `scaffold/python-sidecar.md` / `scaffold/light-python.md` | 开侧车或选轻后端原型时；写侧车 / 轻后端 AGENT 时 |
| `templates/AGENTS.sidecar.md` / `templates/AGENTS.light.md` | 生成侧车 / 轻后端 AGENT 时整份采用 |
| `scaffold/overlay/**` | 只在改增量文件时读；生成时由 init.py 拷贝，不必预读 |
| `axes.md` | 填选型表 |
| `crypto-license.md` | 轴 11 或出图 07 |
| `flow-family.md` | ERP/多单据链；写流程摘要进 harness |
| `module-gold.md` | 第二域/数据范围/金样入口 |
| `dual-source-docs.md` | ERP 双说明书；写数据 AGENT |
| `data-protection.md` | 轴 9；写数据 AGENT 落表/ID/模式 |
| `test-acceptance.md` | 轴 12；写测试 AGENT |
| `extensions.md` | 根 AGENTS 演进索引行 |
| `project-specific.md` | 生成/检查项目特化隔离时 |
| `scaffold.md` | 写/审任一分层 AGENT 深度时 |
| `frontend-ui.md` | 写前端 UI/PC/手机节时 |
| `frontend-engineering.md` | 写/审前端分页、异步竞态、队列、鉴权态、防抖防重、状态缓存节时 |
| `backend-engineering.md` | 写/审后端并发与锁、负载资源、性能高效、对抗审查与安全韧性节时 |
| `web-push-pwa.md` | 主屏幕 Web Push / 苹果通知 / 推送深链选型或写入前后端 AGENT 时 |
| `templates/项目特化.README.md` | 写入 `docs/项目特化/README.md` 时 |
| `diagrams/README.md` | 出图步骤开始时 |
| `living-docs.md` | 写完成审查/宣称文档完成时；改表/改链/改壳后 |
| `架构设计到AI落地-讲解.html` | 查阅 skill 总览（人读；仅作者本地有，不随仓库发布） |
| `surgical-reuse.md` | 轴8 复用与手术刀 |
| `audience.md` | 轴5 对象约束 |
| `research-survey.md` | 轴4 / 旧系统或字段调研 |
| `diagrams/0N-*.md` | 只读正在填的那一幅模板 |
| `templates/*.md` | 生成对应 harness 文件时 |
| `templates/AGENTS.frontend.md` / `backend` / `test` / `data` / `workflow` | 写对应 AGENT 时**整份采用**（见 scaffold.md，禁止缩成摘要） |
| `examples/erp-sample.md` | 逆向样板 ERP / 金样对照 |
| `COMPARISON.md` | 逆向 diff / 评价缺口 |
| `examples/dry-run-*` | 验收教学，非生产生成路径 |

大文件策略：目标仓已有 `docs/数据库说明书.md` 等，**只 grep/读相关 §**，禁止整篇吞入上下文。

## B. 生成的项目 harness（必须落表）

根 `AGENTS.md` **第一章必须是「0. 按需加载」表**，列：文件 | 职责 | 何时读；表内须含全局 `~/AGENTS.md` 一行。
根文件还须有「与全局叠加 / 继承铁律摘要」节（见 templates + global-agents.md）。

硬要求：

1. 根文件默认始终遵守；分层 AGENT / 说明书 / 金样 / 架构图 **写清触发条件**。
2. 禁止「把各方向细则再抄回根文件」；更新只改唯一入口。
3. 超大说明书（库结构等）在「何时读」中写明：先 grep 再读对应 §。
4. 架构图：对齐边界/分层/部署时读 `docs/架构图/README.md`，再按需开单幅。
5. 金样 PRD：只在写/改该范式时读对应金样，禁止一次预读全部金样。
6. **项目特化**：`docs/项目特化/README.md` 在改本项目词表/范围速查/脚本登记时读；**禁止**把特化正文抄进 `agent/AGENTS-*`。

模板见 `templates/AGENTS.root.md`；样板 ERP 级完整表示例见逆向生成产物。
