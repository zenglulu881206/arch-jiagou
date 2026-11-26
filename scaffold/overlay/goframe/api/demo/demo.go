package demo

import (
	"context"

	"__APP_MODULE__/api/demo/v1"
)

// IDemoV1 示例业务接口集合；手工维护，新增场景时同步加方法。
type IDemoV1 interface {
	Greet(context.Context, *v1.GreetReq) (*v1.GreetRes, error)
}
