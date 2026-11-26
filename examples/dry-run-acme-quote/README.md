# Dry-run：acme-quote

本目录是 **arch-jiagou** 的虚构绿场验收样例（询价→报价→客户确认），不是真实业务仓。
只存文档产物；代码脚手架不入 skill（避免与 `scaffold/overlay/` 成为平行副本），按下方命令随时复现。

| 产物 | 路径 |
|---|---|
| 选型表 | [SELECTION.md](SELECTION.md) + [SELECTION.json](SELECTION.json) |
| 架构图 | [docs/架构图/README.md](docs/架构图/README.md) |
| Harness | [AGENTS.md](AGENTS.md) + `agent/` + `admin/` + [docs/项目特化/README.md](docs/项目特化/README.md) |
| 自检 | [CHECKLIST.md](CHECKLIST.md) |

## 复现（在沙箱目录）

```bash
S=~/.agents/skills/arch-jiagou
T=/tmp/ah-sandbox/acme-quote
python3 $S/scaffold/init.py --selection $S/examples/dry-run-acme-quote/SELECTION.json --target $T
cp -R $S/examples/dry-run-acme-quote/{AGENTS.md,SELECTION.md,SELECTION.json,agent,docs} $T/
cp $S/examples/dry-run-acme-quote/admin/AGENTS.md $T/admin/
python3 $S/scaffold/check-harness.py --target $T
python3 $S/scaffold/verify.py --selection $T/SELECTION.json --target $T
```

端口用 18600 / 15600，避开本机 8000（样板 ERP）与 18000（本地模型服务）。
