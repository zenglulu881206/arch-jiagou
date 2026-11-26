# migrations

结构迁移 SQL，按 `NNNN_说明.sql` 递增编号，只追加不改已发布文件。

- 只放 DDL 与幂等的运行种子（字典、菜单等）。
- 禁止：DELETE / TRUNCATE / DROP 业务数据；客户业务补数（放启动 Ensure 或 admin 脚本）。
- 执行器按项目选型落地（如 embed + 启动时执行、或 admin 脚本），选定后写入 `agent/AGENTS-数据.md`。
