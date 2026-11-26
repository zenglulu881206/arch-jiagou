// Package demo 示例业务控制器：一个业务一个文件，每个方法只转调 logic/demo 的同名场景函数。
package demo

import (
	"context"

	"__APP_MODULE__/api/demo"
	"__APP_MODULE__/api/demo/v1"
	logic "__APP_MODULE__/internal/logic/demo"
)

type ControllerV1 struct{}

// NewV1 创建示例业务控制器。
func NewV1() demo.IDemoV1 { return &ControllerV1{} }

// Greet 问候示例。
func (c *ControllerV1) Greet(ctx context.Context, req *v1.GreetReq) (*v1.GreetRes, error) {
	return logic.Greet(ctx, req)
}
