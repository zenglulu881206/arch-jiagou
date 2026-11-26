# 全局经验准则与 Harness 完整继承（〔B〕硬门槛）

> 目标：从 GitHub 安装本 skill 的用户，**不依赖**作者机器上的 `~/AGENTS.md`，也能完整继承作者在 §2 / §3 / §4 积累的经验。  
> §1 称呼已在顾问立场 / 选型 `identity.address` 中体现，此处不重复。

## 两层事实源

| 谁 | 文件 | 职责 |
|---|---|---|
| **Skill 携带（对外发布）** | [`templates/AGENTS.inherited.md`](templates/AGENTS.inherited.md) | §2 多 Agent、§3 行为铁律、§4 Karpathy **全文**；GitHub 用户唯一完整来源 |
| **作者本机（可选叠加）** | `~/AGENTS.md` | 作者跨工具全局规则；与项目叠加；**改 §2–4 后须同轮同步进 inherited 模板** |
| **项目落盘** | `agent/AGENTS-继承准则.md` | 生成 harness 时由 inherited 模板整份写出（替换 `{{USER_ADDRESS}}`） |

**禁止**：只用几条子弹摘要冒充「已继承 §2–4」。  
**禁止**：要求下游用户必须先安装作者的 `~/AGENTS.md` 才能用本 skill。

## 叠加与冲突

- 项目根 AGENTS + 分层 AGENT + **继承准则全文** 同时生效。
- 作者本机若还有 `~/AGENTS.md`：再叠加一层；冲突时**更具体者优先**；不得弱化继承准则中的硬禁令（生产零写入、根因、同轮固化、小闭环等）。

## 章节落点

| 章节 | Skill 内 | 项目 Harness |
|---|---|---|
| §1 称呼 | 顾问立场 + interview A1 | 根 AGENTS「顾问立场」 |
| §2 多 Agent 工作流 | `AGENTS.inherited.md` **全文** | `agent/AGENTS-继承准则.md`；研发流程只保留路径选择，细节不另造 |
| §3 行为铁律 | 同上 **全文** | 同上；根 AGENTS 按需加载表登记本文件 |
| §4 编码准则 | 同上 **全文** | 同上 |

## 生成检查清单

- [ ] 已生成 `agent/AGENTS-继承准则.md`，含二级标题：`多 Agent 工作流`、`全局行为准则`、`通用编码准则`（或等价全文标题）
- [ ] 根按需加载表登记该文件；何时读 = 默认始终（与根 AGENTS 同级）
- [ ] 未把 §2–4 缩成摘要后删除 inherited 文件
- [ ] `{{USER_ADDRESS}}` 已替换为选型称呼

## 作者同步（改个人全局时）

1. 改 `~/AGENTS.md` 的 §2 / §3 / §4。  
2. **同轮**把对应正文同步进 `templates/AGENTS.inherited.md`（保留文首说明与 `{{USER_ADDRESS}}` 占位）。  
3. 已发布项目：经确认后回写其 `agent/AGENTS-继承准则.md`。
