# 架构 Agent 深度声明（硬门槛）

下列 AGENT **不得**写成三五行口号。缺表或缺树 = 该项 **未完成**。

| AGENT | 最低必备 | 权威模板 |
|---|---|---|
| 前端 | 目录树 + 职责/存放路径 + **全站 UI 统一表** + **PC/手机策略表** + **工程横切表**（分页/异步竞态/队列/鉴权态/防抖防重/缓存）；对齐图 04；专册 [frontend-ui.md](frontend-ui.md)、[frontend-engineering.md](frontend-engineering.md) | [templates/AGENTS.frontend.md](templates/AGENTS.frontend.md) |
| 后端 | 目录树 + 分层表 + 存放路径 + 禁令 + **工程横切表**（并发锁/负载资源/性能/对抗审查）；对齐图 03；专册 [backend-engineering.md](backend-engineering.md) | [templates/AGENTS.backend.md](templates/AGENTS.backend.md) |
| 测试 | 工具/启动入口 + 脚本类别表 + 验收维表 + 多帐表 + 汇报/测完即清；脚本存放路径 | [templates/AGENTS.test.md](templates/AGENTS.test.md) |
| 数据 | 模式表 + 双事实源 + ID/code + 落表/删除作废/前缀/业务日/迁移边界表 + 资产存放路径；对齐图 05 | [templates/AGENTS.data.md](templates/AGENTS.data.md) |
| 侧车（开了才有） | 分工边界 + 目录树 + 存放路径 + 调用约定 + 交付编译 | [templates/AGENTS.sidecar.md](templates/AGENTS.sidecar.md) |
| 轻后端（原型才有） | 适用边界 + 目录树 + 存放路径 + 数据约定 + 升级信号 | [templates/AGENTS.light.md](templates/AGENTS.light.md) |
| 研发流程 | 路径选择 + 阶段表 + 访谈默认 + PRD 分档 + 完成审查清单 + 文档落点（AGENT/PRD/特化） | [templates/AGENTS.workflow.md](templates/AGENTS.workflow.md) |

生成时 **整份采用对应模板**，按项目替换占位符；禁止缩成摘要后再声称 harness 完成。

详则专册（按需读）：[test-acceptance.md](test-acceptance.md)、[data-protection.md](data-protection.md)、[dual-source-docs.md](dual-source-docs.md)、[flow-family.md](flow-family.md)、[frontend-engineering.md](frontend-engineering.md)、[backend-engineering.md](backend-engineering.md)。

## 绿场 vs 逆向

- 绿场：代码脚手架由 `scaffold/init.py` 生成（官方 init + 增量，明细见 `scaffold/vue3.md`、`scaffold/goframe.md`），`scaffold/verify.py` 通过才算可用；测试脚本目录、PRD 目录一并预留。
- 深度由 `scaffold/check-harness.py` 机器检查：分层 AGENT 必须含对应模板全部二级标题。
- 逆向：以实仓核对；多出的目录/帐种/阶段须补进 AGENT。

## 与项目特化隔离

架构 Agent 只放可复用约束；词表/ROLE 细表/脚本清单正文 → `docs/项目特化/`。

复用与手术刀原则见 [surgical-reuse.md](surgical-reuse.md)。
