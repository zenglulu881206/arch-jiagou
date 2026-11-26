# 轻后端规则

> **硬门槛**：无「适用边界 + 目录树 + 存放路径 + 数据约定 + 升级信号」视为未完成。仅在 `SELECTION.light` 开启时生成（原型 `light-python-sqlite`）。项目特化不写本文件。

## 适用边界

- 场景：{{LIGHT_SCENE}}。后端只做存取，业务逻辑在前端单页。
- 代码根：`{{LIGHT_ROOT}}`，端口 `{{LIGHT_PORT}}`；页面与接口同源，禁止要求用户双击 `file://` 打开。
- 只用 Python 标准库，不引第三方依赖；前端库需要时走 CDN 并钉版本。

## 目录脚手架（必须声明）

```text
{{LIGHT_ROOT}}
|-- server/app.py              # /api/health、/api/store/<key>，同进程托管 web/
|-- web/index.html             # 设计令牌 + 唯一请求入口 api() + 业务逻辑
|-- tests/                     # 标准库 unittest
`-- data/                      # SQLite 库文件；gitignore；部署绝不删除
```

## 存放路径

| 交付物 | 路径 | 禁止 |
|---|---|---|
| 新功能界面与逻辑 | `web/index.html` 内按功能分区 | 复制出第二份 HTML |
| 新数据 | 新的 key（小写字母、数字、下划线） | 一个 key 塞所有业务 |
| 后端能力 | `server/app.py` | 引第三方依赖；写业务规则 |
| 样式 | `:root` 设计令牌 | 写死色值 |

## 数据约定

1. `PUT` 整 key 覆盖：同一 key 只允许一个人编辑；多人编辑前必须升级。
2. 旧数据迁入时整行原样保留，不丢列。
3. 下拉选项由客户维护的，放设置区，删除前检查是否被引用。
4. 备份：{{LIGHT_BACKUP}}。

## 升级信号（出现任一条就改标准分离原型）

- 用户超过一人或要多人同时编辑；
- 要后端强制权限或数据范围；
- URL 要暴露到公网（先补登录）；
- 单页超过几千行或出现多份副本。

## 验证

- `python3 -m unittest discover -s tests -t .`；浏览器验收见测试 AGENT。
