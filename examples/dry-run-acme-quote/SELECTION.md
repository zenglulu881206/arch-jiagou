# Dry-run 选型表：acme-quote

- 场景：中小贸易商「询价→报价→客户确认」单机/内网工具，10 人内，要迁入旧 Excel，要机器码授权，有 admin 自留地。
- Archetype：`erp-go-vue-pg`（相对样板 ERP 收缩业务域，技术边界同构）
- 日期：2026-11-24

| 轴 | 选定 | 否决 | 代价 |
|---|---|---|---|
| 1 技术栈 | Vue3+TS+Element Plus+Vite（create-vue 3.24.0）；Go 1.25+GoFrame v2.10.5（controller 直调 logic，不设 service 层）；PG 多 schema；nginx+本机 API；脚手架由 init.py 生成 | TinyVue（无华为约束）；Python 主后端；SQLite | 须守 GF 分层与迁移纪律 |
| 2 业务流程 | 询价→报价→确认；报价确认后自动下推「待归档」草稿；进度现算 | 通用 BPM | 自动下推须幂等 |
| 3 样式统一 | `vue/src/styles/`；弹窗三类入口同样板 ERP 口径 | 页面私造第三套按钮 | 前期要抽壳 |
| 4 规范调研 | 旧 Excel 只读四段进 `docs/旧低代码系统调研记录/` | 在客户表里试写 | 调研成本 |
| 5 对象约束 | 贸易商；读者=业务员/主管；禁开发黑话 | 面向程序员的文案 | — |
| 6 权限 | 页面 can_view/can_edit；业务员按 `bill_manager` 收窄；主管全量 | 仅前端藏菜单 | 后端双闸 |
| 7 打包部署 | admin/release pack；Ubuntu；config 深合并；PG15 | 私钥进包 | 双机流程 |
| 8 手术刀 | 标准目录；复用优先；改动范围闸门 | 顺手重构 | — |
| 9 数据硬约束 | 单据落表；nanoid24；删除作废；源头同步 | 前端算金额当真相 | 要公式入口 |
| 10 文档唯一入口 | PRD/`docs/架构图`/公式各一份 | 平行副本 | — |
| 11 加解密授权 | bcrypt；Bearer session；申请码 RSA-OAEP；license 验签；私钥仅 admin | 明文机器码外传 | 签发流程 |
| 12 验收研发 | 真实浏览器；测完即清；log | 只看代码验收 | — |
| 13 能力装配 | 可关「客户确认环」 | 可视化编排器 | 配置驱动写路径 |
