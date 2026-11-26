package demo

import (
	"context"
	"strings"

	"__APP_MODULE__/api/demo/v1"
	"__APP_MODULE__/internal/logic/common"
)

// Greet 场景「问候」：入参来自 GreetReq.Name，返回问候语；名字去空白后为空则报业务错误。
func Greet(ctx context.Context, req *v1.GreetReq) (*v1.GreetRes, error) {
	name := strings.TrimSpace(req.Name)
	if name == "" {
		return nil, common.NewBizError("请填写名字")
	}
	return &v1.GreetRes{Message: "你好，" + name}, nil
}
