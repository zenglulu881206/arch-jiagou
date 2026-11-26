package v1

import "github.com/gogf/gf/v2/frame/g"

// HealthReq 存活探针：部署脚本、nginx、验收脚本据此判断服务已起。
type HealthReq struct {
	g.Meta `path:"/health" method:"get" tags:"系统" summary:"服务存活检查"`
}

// HealthRes 返回固定 ok；不探数据库，避免库抖动时探针误杀进程。
type HealthRes struct {
	Status string `json:"status"`
}
