# internal/middleware

HTTP 中间件：鉴权、数据范围上下文、请求日志、授权校验等。在 `internal/cmd/cmd.go` 的路由组上挂载。

- 统一响应包装直接用 GoFrame 自带 `ghttp.MiddlewareHandlerResponse`，不另写平行版本。
- 鉴权必须后端强制；前端隐藏按钮不算鉴权。
