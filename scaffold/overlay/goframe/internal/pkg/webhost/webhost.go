// Package webhost 让后端进程直接托管前端构建产物（单 exe 交付、无 nginx 时用）。
package webhost

import (
	"net/http"
	"path/filepath"
	"strings"

	"github.com/gogf/gf/v2/net/ghttp"
)

// Mount 托管 root 下的静态文件；root 为空时不做任何事（由 nginx 托管）。
// 前端用 history 路由：非 /api 的 404 一律回 index.html，接口 404 保持原样。
func Mount(s *ghttp.Server, root string) {
	if root == "" {
		return
	}
	s.SetServerRoot(root)
	index := filepath.Join(root, "index.html")
	s.BindStatusHandler(http.StatusNotFound, func(r *ghttp.Request) {
		if strings.HasPrefix(r.URL.Path, "/api/") {
			return
		}
		r.Response.ClearBuffer()
		r.Response.WriteHeader(http.StatusOK)
		r.Response.ServeFile(index)
	})
}
