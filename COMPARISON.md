# 样板 ERP ↔ arch-jiagou 对照

更新日期：2026-11-24（流程族 / 金样 / 双说明书细化后）

用法：逆向或回写前先读本表；生成 harness 不得静默覆盖样板 ERP。

---

## 列表 A：样板 ERP 已有，skill 仍不足

| # | 缺口 | 说明 |
|---|---|---|
| A1 | 业务域完成量公式编号与实现绑定 | skill 有双说明书**规则**，无样板 ERP 的 PO-*/SO-*/INV-* 正文与源头函数表 |
| A2 | 进行态**全站词表**（备货中/发货中/待备货…） | flow-family 要求「先登记词表」，未内置销售/采购词表行 |
| A3 | 各域数据范围金样正文 | module-gold 有可移植条款；无 ROLE-SALES/QC/FIN/CRAFT 匹配键与排除页细表 |
| A4 | 采购升格分型全文（按行/待办故事线/短长链 scope） | 金样框架有；采购金样 §2 业务细则未搬进 skill（也不应整份搬） |
| A5 | 结存过账 stockpost 唯一入口与守门测试 | extensions 仅索引；无过账批次加锁细则 |
| A6 | search_path / 非超户 / EnsureAppGrants | 仍在 extensions 索引，无操作级条款 |
| A7 | 业务日 vs 落库日 | 同上 |
| A8 | 字段前缀 bill_/line_、明细号现算、nanoid24 迁入规则 | 模板一句带过；样板 ERP 数据 AGENT 有完整硬约束 |
| A9 | 列表状态筛禁「草稿」、默认藏取消/作废、`WhereStatus` | 仅 extensions 点名 |
| A10 | 全局搜索：顶栏精准 vs 列表模糊、命中序 | 未写入 axes/模板正文 |
| A11 | 新手引导同步 + check-guides 闸门 | 仅索引 |
| A12 | 模块流程图（讲解）与能力装配 Schema/白名单 | 轴 13 有原则；无装配配置形状与图册清单 |
| A13 | 数据补齐 / 迁入钩子 / 启动 Ensure 分工 | 仅索引 |
| A14 | QA 手册复盘库与历史根因章节 | 无 |
| A15 | PRD 文档标准 L1/L2 分档与强制章节 | 无（易再次产出缺架构图的 PRD） |
| A16 | 列表字段配置（跟账号） | 仅索引 |
| A17 | Chrome+Playwright 启动硬入口、多帐核对分类表 | 测试模板过粗 |
| A18 | 前端弹窗三类/IconActionButton/表格排序硬禁等交互细则 | 前端模板过粗 |
| A19 | 响应效率 / 禁 N+1 / 批量拉参考数据；并发锁、负载限流、越权与脱敏留痕细则 | 规则框架已进 [backend-engineering.md](backend-engineering.md) / [frontend-engineering.md](frontend-engineering.md)；样板 ERP 项目级阈值、锁粒度与清单仍在其 AGENT，未搬进通用 skill |
| A20 | 钉钉登录等具体集成 | 上下文图可画「可选」；无实现约束 |

---

## 列表 B：skill 已有，样板 ERP 仍不足

| # | 缺口 | 说明 |
|---|---|---|
| B1 | **`docs/架构图/` 唯一入口 + 九幅标准 Mermaid 套装** | 生产根目录仍无；**测试快照**已生成于 样板项目仓内测试快照的 `docs/架构图/` |
| B2 | 根 AGENTS「文档唯一入口」表**未登记架构图索引** | 有 PRD/库说明书/公式等，无架构图行 |
| B3 | 个人级**选型表 13 轴**工件 | 样板 ERP 定案散落 AGENTS，无独立 SELECTION 归档 |
| B4 | **archetype** 显式命名（`erp-go-vue-pg`）与换栈对照表 | 仓库内无 archetype 标签 |
| B5 | 加解密/授权**分场景决策表**（crypto-license）独立成册 | 实现在代码+admin README，缺选型级一页表 |
| B6 | 绿场 **dry-run 三件套范例**（acme-quote） | 属 skill 教学资产，非样板 ERP 缺陷，但仓库无对等「架构验收包」 |
| B7 | 流程族 / 金样 / 双说明书的**可移植摘要**（跨项目复用） | 样板 ERP 写的是项目特化全文；换项目需 skill 摘要，不能直接复制词表 |
| B8 | 「bootstrap vs 演进」分层（extensions） | 样板 ERP 根 AGENTS 已极厚，缺少「哪些是绿场最小集」标记 |
| B9 | 生成 harness 时**禁止静默覆盖**的逆向流程 | 样板 ERP 无对应元流程（因本就是源） |

---

## 本轮已补进 skill 的（自列表 A 迁出）

| 主题 | 文件 |
|---|---|
| 流程族 A–H + 唯一进度事实 | `flow-family.md` |
| 模块金样框架 + 数据范围硬条款 | `module-gold.md` |
| 公式说明书 + 数据库说明书双事实源 | `dual-source-docs.md` |
| 轴 2/6/9/10 指针与模板摘要 | `axes.md`、`templates/AGENTS.*.md` |

仍留在列表 A 的，是**项目特化正文**或**下一层演进能力**，不应全部灌进通用 skill 正文。
