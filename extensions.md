# 演进扩展轴（bootstrap 之后）

通用 harness 只保证绿场能跑。下列能力在 **erp-go-vue-pg / 样板 ERP** 已证明高价值。

## 已细化进 skill 正文（选型即读）

| 主题 | skill 文件 | 升格时机 |
|---|---|---|
| 流程族 + 唯一进度事实 | [flow-family.md](flow-family.md) | 第二条跨模块链或长进度条 |
| 模块金样 PRD | [module-gold.md](module-gold.md) | 第二域复用范式 / 数据范围 |
| 公式 + 数据库双事实源 | [dual-source-docs.md](dual-source-docs.md) | ERP/账本类立项即建骨架 |
| 数据保护与落表（ID/模式/删除作废…） | [data-protection.md](data-protection.md) | 有持久化即读；类别可扩展 |
| 测试与验收（脚本类别/维度/多帐） | [test-acceptance.md](test-acceptance.md) | 有 UI 闭环即读；清单可扩展 |
| 前端工程横切（分页/异步竞态/队列/鉴权态/防抖防重/缓存） | [frontend-engineering.md](frontend-engineering.md) | 有独立前端即读；类别可扩展 |
| 后端工程横切（并发锁/负载资源/性能高效/对抗审查） | [backend-engineering.md](backend-engineering.md) | 有独立后端即读；类别可扩展 |
| 主屏幕 Web Push（苹果 / PWA） | [web-push-pwa.md](web-push-pwa.md) | 要做系统通知栏推送或事件总线加苹果通道 |

## 仍属「长大再升格」（仅索引）

| 扩展 | 何时升格 | 样板 ERP 入口 |
|---|---|---|
| 能力装配（开闭已登记环） | 一客一流程差异 | 能力装配 PRD |
| 模块流程图（讲解图≠进度） | 要对业务讲清链 | 模块流程图 PRD + moduleflow |
| 新手引导 Tour 同步 | 有引导且改入口 | 新手引导 PRD + check-guides |
| 列表字段配置（跟账号） | 多角色抱怨列 | 列表字段配置 PRD |
| 全局搜索硬约束 | 有顶栏搜索 | 前端 AGENT + 后端命中序 |
| QA 手册（复盘库） | 第二次踩同类坑 | `docs/QA手册/README.md` |
| PRD 文档标准分档 | 多份 PRD 质量漂移 | `docs/文档模板/PRD文档标准要求.md` |
| 数据补齐 / 迁入舱 | 要承接旧账 | 数据补齐 PRD |
| search_path / 非超户运行账号 | PG 多 schema 上线 | 数据 AGENT |
| 业务日 vs 落库日 | 有过账与报表 | 数据 AGENT |
| 结存过账唯一入口 stockpost | 有库存账 | 后端 AGENT + 公式 INV-* |
| 列表状态筛禁草稿 / 默认藏取消作废 | 有单据列表 | 前后端 AGENT |

## 使用规则

1. 绿场：根 AGENTS 对「仍属长大」只留索引行；对「已细化」按升格时机写入摘要 + 指针。
2. 逆向样板 ERP：核对流族/金样/双说明书是否齐；缺架构图套装则补。
3. 禁止 skill 与项目 AGENTS 长期双源抄同一长文——项目落摘要，细节可外链 skill 或项目专节一处。

| 活文档随开发完善 | [living-docs.md](living-docs.md) | 出图后、改表/改链/改壳、完成审查 |
