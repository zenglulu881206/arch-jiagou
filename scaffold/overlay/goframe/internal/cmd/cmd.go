package cmd

import (
	"context"

	"github.com/gogf/gf/v2/frame/g"
	"github.com/gogf/gf/v2/net/ghttp"
	"github.com/gogf/gf/v2/os/gcmd"

	"__APP_MODULE__/internal/controller/demo"
	"__APP_MODULE__/internal/controller/health"
	"__APP_MODULE__/internal/pkg/webhost"
)

var (
	// Main 启动 HTTP 服务：所有业务接口挂在 /api 下，统一响应 {code,message,data}。
	// 新业务在此 Bind 其 controller；启动期幂等补数（Ensure）也在本包挂载，业务规则正文不写在这里。
	Main = gcmd.Command{
		Name:  "main",
		Usage: "main",
		Brief: "start http server",
		Func: func(ctx context.Context, parser *gcmd.Parser) (err error) {
			s := g.Server()
			s.Group("/api", func(group *ghttp.RouterGroup) {
				group.Middleware(ghttp.MiddlewareHandlerResponse)
				group.Bind(
					health.NewV1(),
					demo.NewV1(),
				)
			})
			webhost.Mount(s, g.Cfg().MustGet(ctx, "web.root", "").String())
			s.Run()
			return nil
		},
	}
)
