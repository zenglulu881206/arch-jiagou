# Python 侧车脚手架：venv 基线 + 经验增量

用于原型 `ai-go-python-sidecar`（实例 AI 审核项目）：业务主链、权限、授权在 Go 主后端，依赖 Python 生态的能力（RAG、向量库、OCR、文档解析、模型调用）放侧车。
开启方式：`SELECTION.backend.sidecar = {"dir": "sidecar", "port": 18002}`。增量实物在 `scaffold/overlay/python-sidecar/`（侧车本体）与 `scaffold/overlay/goframe-sidecar/`（Go 侧）。

## 1. 基线表（官方）

| 项 | 值 | 说明 |
|---|---|---|
| 命令 | `python3 -m venv .venv` + `pip install -e ".[dev]"` | Python 没有类似 create-vue 的官方脚手架；用标准库 venv + PEP 621 `pyproject.toml` |
| Python | ≥ 3.11（init.py 会检查） | 2026-11 用 3.13 实测 |
| 依赖 | `fastapi==0.165.0`、`uvicorn==0.54.0`；开发依赖 `pytest==9.2.0`、`httpx2==2.16.2` | starlette 1.x 的 TestClient 要用 httpx2，用 httpx 会报弃用警告 |
| 镜像 | `https://pypi.tuna.tsinghua.edu.cn/simple` | 模型权重走魔塔 |
| 目录 | 参照 FastAPI 官方「Bigger Applications」：`app/main.py` + 按业务拆路由 | |

## 2. 增量表（经验）

| 路径 | 用途 | 种子文件 | 规则 |
|---|---|---|---|
| `app/main.py` | 入口；路由统一挂 `/py/v1` | `main.py` | 只监听 127.0.0.1，不对浏览器开放 |
| `app/api/v1/<业务>.py` | 路由，一个业务一个文件，与 Go 的 `api/<业务>/v1` 对应 | `health.py`、`demo.py` | 只收参与返回 |
| `app/services/<业务>/<场景>.py` | 能力实现，一个场景一个文件 | `services/demo/summarize.py` | 模型、向量库、OCR 调用都写在这里 |
| `app/schemas/<业务>.py` | 请求 / 响应模型，与 Go 侧 Res 字段一一对应 | `schemas/demo.py` | |
| `app/core/config.py` | 配置，只从环境变量读（端口、安装根、模型地址与密钥） | `config.py` | 模型按 OpenAI 兼容协议配置，换供应商只改环境变量 |
| `tests/` | pytest（服务函数 + TestClient） | `test_summarize.py` | |
| Go：`internal/pkg/sidecar/` | 拉起侧车、等健康、JSON 调用、退出时关闭；端口上已有健康侧车就复用 | `sidecar.go` | 无业务色彩 |
| Go：`internal/cmd/cmd.go` | 覆盖基础版：先起侧车再起 HTTP，`defer` 关闭 | `cmd.go` | |
| Go：`api/aidemo` + `controller/aidemo` + `logic/aidemo/summarize.go` | 示例：Go 校验参数，转给侧车计算；侧车出错只记日志、给操作者统一提示 | 同名文件 | 首个真实能力落地后删除 aidemo |
| Go：`config.example.yaml` 追加 `sidecar` 段 | 目录、端口、启动超时（模型加载慢时调大） | init.py 追加 | |

## 3. 删改表

| 对象 | 动作 | 原因 |
|---|---|---|
| Go `internal/cmd/cmd.go` | 用 `goframe-sidecar` 版本覆盖 | 增加侧车生命周期 |
| Go `manifest/config/config.example.yaml` / `config.yaml` | 追加 `sidecar` 段后重新生成 `config.yaml` | |

## 4. 交付注意（只出文档，不在 init 里做）

- 客户侧交付时，自研 Python 代码用 Cython 编译成 `.so` / `.pyd`，依赖不编译；Nuitka 编译全部依赖会在 8GB 构建机上内存溢出（AI 审核项目）。
- Windows 的 `.pyd` 要在 Windows 构建机上编译。
- 本地模型用 Ollama，模型从魔塔拉取；容器里不能用 mlx 模型（AI 问答项目）。

## 5. 验收（verify.py）

侧车 `pytest` 通过 → Go 起服时自动拉起侧车 → 经 Go 调 `POST /api/aidemo/summarize` 结果正确，空文字被 Go 的 `v:"required"` 拦下 → 关闭 Go 后侧车端口释放。2026-11-26 实测通过。
