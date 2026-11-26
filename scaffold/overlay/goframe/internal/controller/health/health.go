// Package health 存活探针控制器。
package health

import (
	"context"

	"__APP_MODULE__/api/health"
	"__APP_MODULE__/api/health/v1"
)

type ControllerV1 struct{}

// NewV1 创建存活探针控制器。
func NewV1() health.IHealthV1 { return &ControllerV1{} }

// Health 只回 ok，不进 logic、不碰库。
func (c *ControllerV1) Health(ctx context.Context, req *v1.HealthReq) (*v1.HealthRes, error) {
	return &v1.HealthRes{Status: "ok"}, nil
}
