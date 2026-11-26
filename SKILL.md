---
name: arch-jiagou
description: >-
  架构选型落地与 Agent 约束方法。先用选型访谈题库定 13 轴选型表与架构原型，
  再生成标准架构图套装（docs/架构图 01–09 Mermaid）、分层 AGENTS.md 约束（Agent Harness），
  并用「官方 init + 经验增量」生成可运行的项目脚手架（Vue 3 + Element Plus、GoFrame、Python 侧车、轻后端），
  配套 verify 验收与 check-harness 机器自检。适用：新项目定栈与目录、存量项目补齐 AGENTS 与架构图、换栈前选型。
  点名使用：arch-jiagou、架构选型、选型访谈、生成 AGENTS、架构图套装、agent harness、项目脚手架、Web Push。
disable-model-invocation: true
---

# arch-jiagou

按场景做架构选型，输出**可执行的项目级 agent 约束**，并强制附带**标准架构图套装**。缺图 = 选型未完成。

## 身份与顾问立场（硬闸门）

称呼、不附和、先判后答、按场景切换专家身份，遵循全局 `~/AGENTS.md`。
**Harness 完整继承 §2/§3/§4**：按 [global-agents.md](global-agents.md) 将 [templates/AGENTS.inherited.md](templates/AGENTS.inherited.md) **全文**写入项目 `agent/AGENTS-继承准则.md`（替换称呼占位）。使 GitHub 安装本 skill 的用户无需作者本机 `~/AGENTS.md` 也能继承多 Agent、行为铁律、编码准则。§1 称呼已在顾问立场覆盖。作者本机全局若有，仅叠加、并须同轮同步进 inherited 模板。

## 目标清晰与根因优先（硬闸门）

1. **目标不清则不动手**：成功标准、范围边界、验收口径未说清或互相矛盾时，先澄清再选型/改码/出图；禁止为显得「在推进」而猜测落地。
2. **正视问题**：报错、验收失败、数据不一致须当面说清现象与影响；禁止淡化、跳过、假装未看见。
3. **根因优先**：先解释根因，再动手；从根因改设计/实现。**禁止**表面补丁、绕过、只藏按钮/只改文案掩盖；禁止遗漏已知缺口却标完成。
4. **不靠猜**：结论须有证据（日志、库内事实、代码路径、复现步骤、说明书编号）。不确定就标明假设并提问；禁止把猜测写成定案。
5. **同轮固化**：应急改动须同轮落到正确入口（AGENT/说明书/特化/代码），不允许「先补丁以后再还」。
6. **写入 harness**：根 `AGENTS.md` 顾问立场须含同等条款。

自检：*目标是否可验收？根因是否写清？有无补丁债或靠猜的定案？*

## 何时用

- 新项目定技术栈 / 目录 / 约束
- 已有项目要补齐或回写 `AGENTS.md` 树与架构图
- 换栈、加授权锁机、加部署自留地前先选型

## 产物（缺一不可）

默认五类一并交付（架构图、harness、代码脚手架不可缺；特化入口可先空索引）：

1. **选型表**：13 轴每轴唯一选定 + 一句代价/否决（见 [axes.md](axes.md)）；同时输出 `SELECTION.json` 供脚手架脚本读取（字段见 [interview.md](interview.md) D 节）
2. **标准架构图**：写入目标项目 `docs/架构图/`（见 [diagrams/README.md](diagrams/README.md)）
3. **Agent Harness**：根 `AGENTS.md` + 按需 `agent/AGENTS-*.md` / `admin/AGENTS.md`（见 [templates/](templates/)）
4. **项目特化入口（与架构 Agent 隔离）**：`docs/项目特化/README.md`（见 [project-specific.md](project-specific.md)）——只登记/索引，**禁止**把特化正文写入架构 AGENT
5. **代码脚手架**：官方 init 基线 + 经验增量，由 [scaffold/init.py](scaffold/init.py) 生成、[scaffold/verify.py](scaffold/verify.py) 验收（见 [scaffold/vue3.md](scaffold/vue3.md)、[scaffold/goframe.md](scaffold/goframe.md)、[scaffold/python-sidecar.md](scaffold/python-sidecar.md)、[scaffold/light-python.md](scaffold/light-python.md)）


## 按需读取（硬闸门）

1. **跑 skill**：遵守 [progressive-load.md](progressive-load.md) A 表；未触发勿整文件预读。
2. **产物 harness**：根 `AGENTS.md` 必须以「0. 按需加载」表开头（文件|职责|何时读）；大说明书须注明 grep 后再读 §。
3. 自检未含按需加载表 = 未完成。

禁止：只写散文不做定案；把业务 PRD 细则抄进通用 AGENT；在多处平行复制同一约束。

## 步骤

### 1. 定场景

按 [interview.md](interview.md) A–I 节记录分岔答案：称呼与领域、部署位置、后端语言、架构形态、终端、数据、授权防泄漏、AI 接入、自留地；再用第 2 节联动规则推出默认值。

若鲁大师目标/验收仍模糊：先列澄清问题，**停止**出图与写 harness，直到可验收标准清楚（见「目标清晰与根因优先」）。

完成准则：按 interview.md「原型映射」能指出 1 个候选 archetype（见 [archetypes.md](archetypes.md)）；成功标准可检验。

### 2. 访谈（≤5 题/轮）

读 [interview.md](interview.md)：按 archetype 默认值整表预填，只问「何时必须问」命中的题。与金样同构的决策直接定案，禁止再拆访谈。

完成准则：剩余开放题 ≤2，或鲁大师说「按默认」。

### 3. 填选型表

对 [axes.md](axes.md) 每一轴给出：**选定 / 否决项 / 代价一句**。加密见 [crypto-license.md](crypto-license.md)。

若为 ERP/多单据链：必读 [flow-family.md](flow-family.md)、[module-gold.md](module-gold.md)、[dual-source-docs.md](dual-source-docs.md)、[data-protection.md](data-protection.md)、[test-acceptance.md](test-acceptance.md)；
有独立前端：读 [frontend-engineering.md](frontend-engineering.md)（分页 / 异步竞态 / 队列 / 鉴权态 / 防抖防重 / 缓存）；有独立后端：读 [backend-engineering.md](backend-engineering.md)（并发锁 / 负载资源 / 性能 / 对抗审查）。
选型表轴 1/2/6/9/10/11/12 写明升格范围。**清单均为举例，按场景扩展，禁止当成封闭枚举。**
若要做手机系统通知 / 主屏幕推送：必读 [web-push-pwa.md](web-push-pwa.md)，前后端 AGENT 写入投递总线、订阅跟账号、深链同口径；事件目录与 openPath 落项目特化，禁止把业务事件码抄进通用 AGENT。

完成准则：13 轴无空格；前后矛盾已消解。

### 4. 锁定 archetype

从 [archetypes.md](archetypes.md) 选一；没有则提议新原型名并列出相对最近原型的差分，再生成。

### 5. 出标准图（硬闸门）

1. 读 [diagrams/README.md](diagrams/README.md) 必出清单、**质量闸门**、状态枚举与 Mermaid 约束。
2. 用 `diagrams/0N-*.md` 模板；**Mermaid 内禁止残留 `{{…}}`**（会导致渲染失败）。
3. 写入目标项目并**按真实项目替换节点**（逆向须贴模块/schema/路径，禁止长期玩具图）。
4. 索引每图必须写状态：`测试骨架` / `骨架` / `与现状一致` / `过期` / `N/A`。
5. 轻原型可 N/A；`erp-go-vue-pg` 九幅全要。
6. **活文档**：此后开发中架构图随边界变化同轮完善，见 [living-docs.md](living-docs.md)。

完成准则拆两层：
- **目录齐**：必出文件存在、占位已清、Mermaid 可预览、与选型边界/AGENT 路径不矛盾。
- **图质量通过**：仅当状态为 `与现状一致`（测试快照允许停在 `测试骨架`，但**禁止**把目录齐写成「全部通过」）。

### 6. 生成 Harness

按模板生成（占位符用选型事实替换）：

| 文件 | 何时生成 |
|---|---|
| `AGENTS.md` | 始终 |
| `agent/AGENTS-继承准则.md` | **始终**（§2/§3/§4 全文，模板 `AGENTS.inherited.md`） |
| `agent/AGENTS-前端.md` | 有独立前端 |
| `agent/AGENTS-后端.md` | 有独立后端 |
| `agent/AGENTS-侧车.md` | 开了 Python 侧车（`backend.sidecar`） |
| `agent/AGENTS-轻后端.md` | 轻后端原型（`light`） |
| `agent/AGENTS-数据.md` | 有持久化库 |
| `agent/AGENTS-测试.md` | 始终 |
| `agent/AGENTS-研发流程.md` | 始终 |
| `admin/AGENTS.md` | 有开发自留地/签发/清洗 |
| `docs/项目特化/README.md` | **始终**（可先空表）；与架构 AGENT 隔离 |

分层 AGENT 深度见 [scaffold.md](scaffold.md)：**前端/后端/测试/数据/研发流程**均须整份采用对应模板（目录或类别表 + 存放路径 + 禁令），禁止缩成摘要。前端另须含工程横切表（见 [frontend-engineering.md](frontend-engineering.md)），后端另须含工程横切表（见 [backend-engineering.md](backend-engineering.md)）。

根文件必须：**0. 按需加载表**（含 `agent/AGENTS-继承准则.md`）、**0.2 经验准则完整继承**、文档唯一入口、技术边界、顾问立场、指向分层 AGENT。继承准则须为 §2/§3/§4 **全文**（见 [global-agents.md](global-agents.md)、[templates/AGENTS.inherited.md](templates/AGENTS.inherited.md)），禁止摘要冒充。
按需加载表必须含：分层 AGENT、架构图、双说明书、已有金样 PRD、测试/流程/admin；大文件写明 grep 再读。

**禁止静默覆盖**：目标已有 `AGENTS.md` 时，先 diff 报告，经鲁大师确认再写。

始终创建 `docs/项目特化/README.md`；根 AGENTS **只链入口**，词表/ROLE 细表/脚本清单等写入特化目录（见 [project-specific.md](project-specific.md)）。

ERP 类：根 AGENTS 写入**流程族 A–H 摘要**（或指针 [flow-family.md](flow-family.md)）、**双说明书入口**、**模块金样入口（可先占位）**；其余见 [extensions.md](extensions.md) 索引，勿把样板 ERP 业务词表全文打进绿场模板。

### 6.5 生成代码脚手架（绿场硬闸门）

1. 把选型结果写成目标项目根下的 `SELECTION.json`。
2. 在沙箱目录先跑：`python3 <skill>/scaffold/init.py --selection SELECTION.json --target <沙箱>`，再跑 `verify.py`（默认有头浏览器）；通过后再对真实目标目录执行。
3. `init.py` 同时在项目根建 `admin/scripts/e2e_launch.py`（浏览器验收唯一入口）和 `CLAUDE.md → AGENTS.md` 软链，已存在则不动。
4. `init.py` 不覆盖已存在的前后端目录；逆向/已有仓不跑 init，只按 `scaffold/*.md` 增量表核对差异并报告。
5. 生成后把分层 AGENT 的目录树与实物对齐（`check-harness.py` 会查）。

完成准则：`verify.py` 退出码 0（构建、单测、健康检查、浏览器冒烟全过）。

### 7. 自检

先跑 `python3 <skill>/scaffold/check-harness.py --target <项目根> --render`，退出码 0 才进入下列人工项；脚本已覆盖的项不再人工打勾。`--render` 用真实 mermaid 在浏览器里渲染每一块架构图，语法错误逐条报出。

- [ ] 选型表 13 轴填齐；`SELECTION.json` 已生成
- [ ] `verify.py` 通过（绿场）；`check-harness.py` 通过
- [ ] **架构图目录齐**：必出齐全或 N/A 有理由；无残留 `{{`；Mermaid 可渲染
- [ ] **架构图质量**：索引状态诚实；未把 `测试骨架`/`骨架` 写成「全部通过」；生产开发须持续推到 `与现状一致`
- [ ] 根 AGENTS 链到架构图索引；活文档规则已登记（见 living-docs）
- [ ] **完整继承**：已生成 `agent/AGENTS-继承准则.md`（§2/§3/§4 全文）；根按需加载已登记；非摘要
- [ ] 无平行副本（同一约束只一处）
- [ ] admin / 运行时边界与容器图、部署图一致
- [ ] 分层路径与后端/前端图一致
- [ ] 前端 AGENT：脚手架树 + 职责/存放路径 + 全站 UI 表 + PC/手机策略表 + 工程横切表（分页/异步竞态/队列/鉴权态/防抖防重/缓存）
- [ ] 后端 AGENT：完整脚手架树 + 分层/存放路径/禁令 + 工程横切表（并发锁/负载资源/性能/对抗审查）
- [ ] 测试 AGENT：工具入口 + 类别/维度/多帐表 + 脚本存放路径；含并发幂等、越权直调、限流、慢路径、脱敏留痕用例
- [ ] 数据 AGENT：模式表 + 双事实源 + ID/落表类别表 + 资产路径
- [ ] 研发流程 AGENT：阶段表 + 访谈默认 + 文档落点 + **活文档同轮更新** + 完成审查清单
- [ ] ERP：流程族/唯一进度事实已写入或显式「短链暂缓」
- [ ] ERP：数据库说明书 + 公式说明书入口已登记；**开发中随改表/改算法同轮完善**（非一次生成了事）
- [ ] 有第二域或已规划：模块金样入口已登记
- [ ] 已建 `docs/项目特化/README.md`；按需加载与文档入口已登记
- [ ] 架构 AGENT 无大段项目词表/ROLE 细表（特化内容在项目特化目录）

未勾满不得宣称完成。**目录齐 ≠ 图质量通过 ≠ 活文档已跟开发。**

## 分支

- **绿场**：五类产物全部新建；代码脚手架走 init.py。
- **逆向（已有仓）**：读现有 AGENT/目录/依赖 → 填表 → 出图 → diff harness；默认不覆盖。
- **增量**：只改声明要动的轴与对应图，其余不动。

## 参考

> 全册分两大板块：**〔A 架构设计〕** 从技术栈、业务流程、数据域、授权边界、部署拓扑等系统架构视角定边界；**〔B Harness 工程〕** 从 AI Agent 对话执行视角定约束（怎么读规范、怎么执行、怎么交差）。标注 **〔A/B〕** 为跨板块。

### A · 架构设计（系统架构视角）

- 决策轴：[axes.md](axes.md) 〔A〕
- 原型：[archetypes.md](archetypes.md) 〔A〕
- 图套装：[diagrams/README.md](diagrams/README.md) 〔A〕
- 流程族 + 唯一进度：[flow-family.md](flow-family.md) 〔A〕
- 模块金样：[module-gold.md](module-gold.md) 〔A〕
- 双事实源：[dual-source-docs.md](dual-source-docs.md) 〔A〕
- 数据保护与落表：[data-protection.md](data-protection.md) 〔A〕
- 加解密授权：[crypto-license.md](crypto-license.md) 〔A〕
- 主屏幕 Web Push（苹果/PWA）：[web-push-pwa.md](web-push-pwa.md) 〔A〕
- 样式与 UI：[frontend-ui.md](frontend-ui.md) 〔A〕
- 前端工程横切：[frontend-engineering.md](frontend-engineering.md) 〔A〕
- 后端工程横切：[backend-engineering.md](backend-engineering.md) 〔A〕
- 规范调研：[research-survey.md](research-survey.md) 〔A〕
- 对象约束：[audience.md](audience.md) 〔A〕
- 复用与手术刀：[surgical-reuse.md](surgical-reuse.md) 〔A/B〕
- 活文档：[living-docs.md](living-docs.md) 〔A/B〕

### B · Agent Harness 工程（Agent 对话执行视角）

- 分层 AGENT 深度门槛：[scaffold.md](scaffold.md) 〔B〕
- 代码脚手架（官方 init + 增量）：[scaffold/vue3.md](scaffold/vue3.md)、[scaffold/goframe.md](scaffold/goframe.md)、[scaffold/python-sidecar.md](scaffold/python-sidecar.md)、[scaffold/light-python.md](scaffold/light-python.md)、`scaffold/init.py`、`scaffold/verify.py` 〔A/B〕
- 机器自检：`scaffold/check-harness.py` 〔B〕
- 选型访谈题库：[interview.md](interview.md) 〔A〕
- 按需加载：[progressive-load.md](progressive-load.md) 〔B〕
- 全局 AGENTS 结合：[global-agents.md](global-agents.md) 〔B〕
- 模板：[templates/](templates/) 〔B〕
- 项目特化隔离：[project-specific.md](project-specific.md) 〔B〕
- 测试与验收闸门：[test-acceptance.md](test-acceptance.md) 〔B〕
- 对照清单：[COMPARISON.md](COMPARISON.md) 〔B〕
- 演进扩展索引：[extensions.md](extensions.md) 〔A/B〕
- 配图：[系统架构图.webp](系统架构图.webp)、[流程泳道图.webp](流程泳道图.webp) 〔A/B〕
- 讲解幻灯片 `架构设计到AI落地-讲解.html`：只留作者本地，不随仓库发布 〔A/B〕
- 样板 ERP 金样：[examples/erp-sample.md](examples/erp-sample.md) 〔A/B〕
- 绿场 dry-run：[examples/dry-run-acme-quote/](examples/dry-run-acme-quote/) 〔B〕
- 样板 ERP 逆向测试快照：放在样板项目仓内（不替代根 AGENTS）〔B〕
