// Package aidemo 侧车示例控制器：只转调 logic/aidemo 同名函数。
package aidemo

import (
	"context"

	"__APP_MODULE__/api/aidemo"
	"__APP_MODULE__/api/aidemo/v1"
	logic "__APP_MODULE__/internal/logic/aidemo"
)

type ControllerV1 struct{}

// NewV1 创建侧车示例控制器。
func NewV1() aidemo.IAidemoV1 { return &ControllerV1{} }

// Summarize 侧车摘要示例。
func (c *ControllerV1) Summarize(ctx context.Context, req *v1.SummarizeReq) (*v1.SummarizeRes, error) {
	return logic.Summarize(ctx, req)
}
