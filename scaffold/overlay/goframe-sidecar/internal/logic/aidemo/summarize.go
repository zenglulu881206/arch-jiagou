package aidemo

import (
	"context"

	"github.com/gogf/gf/v2/frame/g"

	"__APP_MODULE__/api/aidemo/v1"
	"__APP_MODULE__/internal/logic/common"
	"__APP_MODULE__/internal/pkg/sidecar"
)

// Summarize 场景「摘要」：把 Text 转给侧车 /py/v1/demo/summarize，原样返回统计结果。
// 侧车不可用时只记日志，给操作者统一的业务提示，不把内部错误回传前端。
func Summarize(ctx context.Context, req *v1.SummarizeReq) (*v1.SummarizeRes, error) {
	var res v1.SummarizeRes
	err := sidecar.Default().PostJSON(ctx, "/py/v1/demo/summarize", map[string]string{"text": req.Text}, &res)
	if err != nil {
		g.Log().Errorf(ctx, "调用侧车失败：%v", err)
		return nil, common.NewBizError("智能服务暂不可用，请稍后重试")
	}
	return &res, nil
}
