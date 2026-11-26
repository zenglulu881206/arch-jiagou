package main

import (
	_ "__APP_MODULE__/internal/packed"

	_ "github.com/gogf/gf/contrib/drivers/__DB_DRIVER__/v2"

	"github.com/gogf/gf/v2/os/gctx"

	"__APP_MODULE__/internal/cmd"
)

func main() {
	cmd.Main.Run(gctx.GetInitCtx())
}
