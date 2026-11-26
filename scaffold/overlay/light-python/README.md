# 轻后端应用

后端只做存取（Python 标准库 + SQLite），业务逻辑在前端单页。适合单人或个人自用、业务规则少的场景。

| 路径 | 放什么 |
|---|---|
| `server/app.py` | 存取接口 + 托管 `web/`；零第三方依赖 |
| `web/index.html` | 单页：设计令牌、唯一请求入口 `api()`、业务逻辑 |
| `tests/` | 标准库 unittest |
| `data/` | SQLite 库文件（gitignore；部署脚本绝不删除） |

本地运行：`python3 server/app.py`，浏览器打开显示的地址。测试：`python3 -m unittest discover -s tests -t .`。

升级到标准分离的信号：用户变多、要多人同时编辑、要后端强制权限、页面超过几千行。
