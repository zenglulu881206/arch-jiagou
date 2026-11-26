# Python 侧车规则

> **硬门槛**：无「分工边界 + 目录树 + 存放路径 + 调用约定 + 交付编译」视为未完成。仅在 `SELECTION.backend.sidecar` 开启时生成。项目特化不写本文件。

## 分工边界

- 业务主链、权限、数据范围、授权校验、对外接口契约：**只在 Go 主后端**。
- 侧车只承接依赖 Python 生态的能力：{{SIDECAR_CAPABILITIES}}。
- 浏览器不直连侧车：前端 → Go `/api/...` → 侧车 `/py/v1/...`。
- 侧车代码根：`{{SIDECAR_ROOT}}`，端口 `{{SIDECAR_PORT}}`，只监听 127.0.0.1。

## 目录脚手架（必须声明）

```text
{{SIDECAR_ROOT}}
|-- pyproject.toml             # 依赖钉版本；镜像走清华
|-- app/
|   |-- main.py                # 入口；路由统一挂 /py/v1
|   |-- core/config.py         # 只读环境变量（端口、安装根、模型地址与密钥）
|   |-- api/v1/<业务>.py       # 路由，一个业务一个文件，与 Go api/<业务>/v1 对应
|   |-- services/<业务>/<场景>.py   # 能力实现，一个场景一个文件
|   `-- schemas/<业务>.py      # 请求/响应模型，与 Go 侧 Res 字段一一对应
`-- tests/                     # pytest
```

Go 侧对应：`internal/pkg/sidecar/`（拉起、健康等待、JSON 调用、关闭）、`internal/cmd/cmd.go`（先起侧车再起 HTTP）、`internal/controller/<业务>/` 与 `internal/logic/<业务>/`（经侧车完成场景）、`api/<业务>/v1/`（对外契约）。

## 存放路径

| 交付物 | 路径 | 禁止 |
|---|---|---|
| 新能力路由 | `app/api/v1/<业务>.py` | 路由里写计算逻辑 |
| 能力实现 | `app/services/<业务>/<场景>.py` | 一个文件塞全部场景 |
| 模型 | `app/schemas/<业务>.py` | 与 Go 字段名不一致 |
| Go 调用 | Go `internal/logic/<业务>/<场景>.go` 经 `internal/pkg/sidecar` 调用 | controller 直接调侧车；前端直连侧车 |
| 模型缓存 / 向量库 | 安装根 `data/` 下 | 放进代码目录或入库 |

## 调用约定

1. Go 启动时拉起侧车并等 `/py/v1/health` 返回 `healthy=true`；端口上已有健康侧车就复用，不起第二份。
2. 侧车出错时 Go 只记日志，给操作者统一提示，不把 Python 异常回传前端。
3. 模型按 OpenAI 兼容协议调用；在线 / 本地用开关切换，不自动互切。哪些数据可以出网：{{AI_DATA_EGRESS}}。
4. 耗时长的能力（OCR、批量向量化）走任务表或队列，不阻塞请求；流式输出用 SSE，nginx 关缓冲。
5. 启动超时 `sidecar.startTimeoutSec` 要覆盖模型加载时间。

## 交付编译

- 客户侧：自研代码用 Cython 编译后打包，依赖不编译；Windows 包要在 Windows 构建机编译。
- 构建机内存要按依赖体积估算（Nuitka 编全部依赖曾在 8GB 机器上溢出）。

## 验证

- `.venv/bin/python -m pytest -q`；端到端经 Go 接口验证（见测试 AGENT）。
