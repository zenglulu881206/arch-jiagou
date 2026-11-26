# 决策轴（13）

每轴必须：**选定** + **否决** + **代价一句**。选定须能在对应架构图中看见边界。

| # | 轴 | 常见选项 | 对应图 / 详文 | 定案提示 |
|---|---|---|---|---|
| 1 | 技术栈 | FE/BE/DB/**接口接入**/加解密/授权/形态；**前后端脚手架必须写入 AGENT**；前后端工程横切（分页/异步/竞态/队列/鉴权态/防抖；并发锁/负载/性能/安全） | 02,03,04,07；[scaffold.md](scaffold.md)；[frontend-engineering.md](frontend-engineering.md)；[backend-engineering.md](backend-engineering.md)；[crypto-license.md](crypto-license.md) | 按 [interview.md](interview.md) B–F 节联动规则定（客户侧首选 Go；数据大选 PG、小选 SQLite）；默认 Vue3+EP+Vite+TS + GoFrame + PG；接口契约进 api/；AGENT 禁缩成口号；工程横切唯一入口须落 AGENT |
| 2 | 业务流程 | 主链；下推自动/手动；**唯一进度事实**；流程衔接/回跳/进行态/行按钮；权限不越界 | 09；[flow-family.md](flow-family.md) | 禁止 BPM 当进度真相；无主观决策→自动下推；第二跨模块链起强制写入流程族 |
| 3 | 样式统一 | 设计令牌唯一入口；header/侧栏/表/钮/报错/标题/抽屉/弹窗/tooltip…；PC+手机 | 04；[frontend-ui.md](frontend-ui.md) | 弹窗三类写死入口；举例非穷举；禁平行皮肤 |
| 4 | 规范调研 | 菜单路径、字段集(编码/名称/示例/含义)、布局、交互；有旧系统则只读四段 | 01；[research-survey.md](research-survey.md) | 生产零写入；字段进 PRD/说明书不进通用 AGENT |
| 5 | 对象约束 | 行业、专业视角、部门、岗位；读者=操作者 | 01,06；[audience.md](audience.md) | 对象错则文案/权限/验收全漂；细表进特化 |
| 6 | 权限 | 菜单粗线、按钮、字段分组、**数据范围金样**（员/主管） | 06；[module-gold.md](module-gold.md) | 员收窄、主管全量；双闸；第二域复用先立金样 |
| 7 | 打包部署 | nginx；版本对齐；部署范围；库更新；回滚；config 深合并 | 08 | 开发自留地不进包 |
| 8 | 复用/手术刀 | 标准目录层级含义+存放路径；高复用低冗余；手术刀精准改、禁扩范围 | 03,04；[surgical-reuse.md](surgical-reuse.md)；[scaffold.md](scaffold.md) | 写前检索；禁打地鼠式扩散 |
| 9 | 数据硬约束 | 模式划分；内部ID(nanoid等)+外部code；落表/删除作废/前缀/业务日/迁移边界；源头同步；**双说明书** | 05；[data-protection.md](data-protection.md)；[dual-source-docs.md](dual-source-docs.md) | 类别可扩展，举例非穷举；ERP 强制双说明书 |
| 10 | 文档唯一入口 | PRD / 双说明书 / 金样 / 架构图 / **项目特化** 分入口；架构 Agent ≠ 特化目录 | 架构图；dual-source；module-gold；[project-specific.md](project-specific.md) | 禁平行副本；特化不进 agent/AGENTS-* |
| 11 | 加解密与授权 | 见 crypto-license.md；后端安全韧性（越权/入参/防重放/留痕/信息收敛）见 backend-engineering §4 | 07；03 | 分场景选型；鉴权后端强制双闸 |
| 12 | 验收与研发流程 | 真实交互、多帐核对、完成审查、log；并发/幂等/越权直调/限流/慢路径/脱敏留痕纳入验收 | —；[backend-engineering.md](backend-engineering.md)；[frontend-engineering.md](frontend-engineering.md) | 测完即清；工程横切类别按链扩展 |
| 13 | 能力装配 | 开闭已登记能力 / 不做 | 09；flow-family | 装配可裁剪讲解图与写路径；不得另起可写流程态 |

## 选型表示例行

```text
轴2 业务流程 | 选定: 唯一进度事实+流程族A–H; 下推按主观决策; 讲解图≠进度 | 否决: 可写process_status; BPM引擎 | 代价: 须维护链builder与升级补数
轴12 | 选定: 先脚本(正/反/部分/超量…)→Chrome有头0.8s；验收含样式/计算/同步/多帐；测完即清 | 否决: 无脚本点测; API造中段冒充交互 | 代价: 脚本维护
轴9/10 | 选定: docs/数据库说明书.md + docs/计算公式说明书.md 双事实源 | 否决: PRD内抄可执行公式; 平行数据字典 | 代价: 改表/改算法必须同轮更新说明书
轴6 | 选定: 模块金样承载数据范围与列表分型 | 否决: 各域私造范围哲学 | 代价: 第二域前先写金样PRD
```
