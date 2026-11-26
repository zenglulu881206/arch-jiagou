package cmd

import (
	"context"
	"time"

	"github.com/gogf/gf/v2/frame/g"
	"github.com/gogf/gf/v2/net/ghttp"
	"github.com/gogf/gf/v2/os/gcmd"

	"__APP_MODULE__/internal/controller/aidemo"
	"__APP_MODULE__/internal/controller/demo"
	"__APP_MODULE__/internal/controller/health"
	"__APP_MODULE__/internal/pkg/webhost"
	"__APP_MODULE__/internal/pkg/sidecar"
)

var (
	// Main 启动 HTTP 服务：先拉起 Python 侧车并等它就绪，再对外提供 /api；进程退出时关闭侧车。
	// 新业务在此 Bind 其 controller；启动期幂等补数（Ensure）也在本包挂载，业务规则正文不写在这里。
	Main = gcmd.Command{
		Name:  "main",
		Usage: "main",
		Brief: "start http server",
		Func: func(ctx context.Context, parser *gcmd.Parser) (err error) {
			sc := sidecar.New(
				g.Cfg().MustGet(ctx, "sidecar.dir", "../__SIDECAR_DIR__").String(),
				g.Cfg().MustGet(ctx, "sidecar.port", __SIDECAR_PORT__).Int(),
				time.Duration(g.Cfg().MustGet(ctx, "sidecar.startTimeoutSec", 60).Int())*time.Second,
			)
			if err := sc.Start(ctx); err != nil {
				return err
			}
			defer sc.Stop()
			sidecar.SetDefault(sc)

			s := g.Server()
			s.Group("/api", func(group *ghttp.RouterGroup) {
				group.Middleware(ghttp.MiddlewareHandlerResponse)
				group.Bind(
					health.NewV1(),
					demo.NewV1(),
					aidemo.NewV1(),
				)
			})
			webhost.Mount(s, g.Cfg().MustGet(ctx, "web.root", "").String())
			s.Run()
			return nil
		},
	}
)
