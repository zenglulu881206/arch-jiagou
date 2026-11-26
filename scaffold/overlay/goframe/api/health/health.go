package health

import (
	"context"

	"__APP_MODULE__/api/health/v1"
)

// IHealthV1 存活探针接口集合。
type IHealthV1 interface {
	Health(context.Context, *v1.HealthReq) (*v1.HealthRes, error)
}
