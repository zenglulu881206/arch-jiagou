# Python 侧车

承接依赖 Python 生态的能力（RAG、向量库、OCR、文档解析、模型调用）。业务主链、权限、授权仍在 Go 主后端。

| 路径 | 放什么 |
|---|---|
| `app/api/v1/<业务>.py` | 路由，一个业务一个文件，与 Go 的 `api/<业务>/v1` 对应 |
| `app/services/<业务>/<场景>.py` | 能力实现，一个场景一个文件 |
| `app/schemas/<业务>.py` | 请求/响应模型 |
| `app/core/config.py` | 配置，只从环境变量读 |
| `tests/` | pytest |

开发：

```bash
python3 -m venv .venv
.venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"
.venv/bin/python -m pytest -q
```

正常运行时不用单独启动：Go 主后端启动时会拉起侧车（`internal/pkg/sidecar`），退出时关闭。
交付给客户时，自研代码用 Cython 编译后再打包；依赖不编译。
