# Dry-run 自检（acme-quote）

日期：2026-11-26。环境：macOS、Node 22.23、Go 1.25.7、gf CLI v2.10.0、本机 Chrome。

## 机器检查（以脚本退出码为准）

| 检查 | 命令 | 结果 |
|---|---|---|
| 脚手架生成 | `scaffold/init.py` | 通过（退出码 0） |
| 脚手架验收 | `scaffold/verify.py`（有头浏览器） | 通过：前端类型检查+构建、`go vet`/`go test`/`go build`、`/api/health`、浏览器正常问候与空名字反例 |
| harness 自检 | `scaffold/check-harness.py --target <沙箱>` | 通过 |
| 反例 | 删 `vue/src/utils`、删后端一章、加 `{{FOO}}`、状态改「已出」、加坏链接 | 13 项全部被报出 |

## 人工项

- [x] 选型表 13 轴填齐；`SELECTION.json` 已生成
- [x] 分层 AGENT 整份采用模板，前端 UI / 工程横切落点已按本项目填（未建的写明「首次出现时建在哪」）
- [x] 后端分层与实物一致：controller 直调 logic，不设 service 层
- [x] 架构图 01–09 齐，状态如实标「骨架」；**图质量未通过**（业务未落地）
- [x] 未覆盖样板 ERP 仓库任何文件

结论：**目录齐 + 脚手架可用 + harness 自检通过**；架构图停在「骨架」，按 living-docs 随业务推进。
