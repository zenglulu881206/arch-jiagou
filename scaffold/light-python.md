# 轻后端脚手架：Python 标准库 + SQLite + 单 HTML

用于原型 `light-python-sqlite`（实例 单人办公项目）：单人或个人自用、业务规则少。后端只做存取，业务逻辑在前端单页。
开启方式：`SELECTION.light = {"dir": "app", "port": 8080}`（不写 `frontend`、`backend`）。增量实物在 `scaffold/overlay/light-python/`。

## 1. 基线表（官方）

| 项 | 值 | 说明 |
|---|---|---|
| 命令 | 无 | 只用 Python 标准库（`http.server`、`sqlite3`），没有 init 步骤，也不装第三方依赖 |
| Python | ≥ 3.9（init.py 会检查） | 3.9 起不支持 Win7；轻后端默认部署在云服务器 Ubuntu |
| 前端 | 单个 `index.html`，原生 JS，无构建 | 需要第三方库时走 CDN（单人办公项目用 jsdelivr） |

## 2. 增量表（经验）

| 路径 | 用途 | 种子文件 | 规则 |
|---|---|---|---|
| `server/app.py` | `GET /api/health`、`GET/PUT /api/store/<key>`，同进程托管 `web/` | `app.py` | 每个请求单独开连接；key 只许小写字母、数字、下划线；错误回面向操作者的中文 |
| `web/index.html` | 单页：设计令牌（CSS 变量）、唯一请求入口 `api()`、业务逻辑 | `index.html` | 界面不出现 SQLite、API、缓存等技术词；手机端有断点和 `apple-mobile-web-app-capable` |
| `tests/test_app.py` | 标准库 unittest：起临时端口测健康、存取、非法 key | 同名 | |
| `data/` | SQLite 库文件 | 运行时创建，gitignore | 部署脚本绝不删除 |
| `README.md` | 运行、测试、升级到标准分离的信号 | 同名 | |

## 3. 删改表

无官方产物可删改。

## 4. 已知代价（来自 单人办公项目）

- `PUT` 整个 key 覆盖，多人同时编辑同一 key 会互相覆盖。
- 没有登录：只在 URL 不公开时可接受，暴露到公网前必须补。
- 单页越写越长；出现多份 HTML 副本时要合并成一份。
- 用户变多、要多人编辑、要后端强制权限时，改用 `erp-go-vue-pg` 一类标准分离原型。

## 5. 验收（verify.py）

unittest 通过 → 起服后健康检查通过 → `GET /api/store/Bad-Key` 返回 400 → 浏览器保存备忘显示「已保存」，刷新后内容仍在。2026-11-26 实测通过。
