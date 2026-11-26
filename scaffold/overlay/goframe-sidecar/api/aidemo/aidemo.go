package aidemo

import (
	"context"

	"__APP_MODULE__/api/aidemo/v1"
)

// IAidemoV1 侧车示例接口集合。
type IAidemoV1 interface {
	Summarize(context.Context, *v1.SummarizeReq) (*v1.SummarizeRes, error)
}
