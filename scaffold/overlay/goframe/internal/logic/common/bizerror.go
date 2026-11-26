// Package common 跨业务公共逻辑：错误码、状态筛选等多个业务共用、但带业务含义的代码。
// 无业务色彩的纯工具（ID 生成、加解密等）放 internal/pkg/。
package common

import (
	"github.com/gogf/gf/v2/errors/gcode"
	"github.com/gogf/gf/v2/errors/gerror"
)

// CodeBizRejected 业务规则拒绝（校验不过、上下游闸门挡住等）；文案直接给操作者看。
var CodeBizRejected = gcode.New(1001, "业务规则拒绝", nil)

// NewBizError 生成面向操作者的业务错误；经 ghttp.MiddlewareHandlerResponse 统一包成 {code,message,data}。
func NewBizError(message string) error {
	return gerror.NewCode(CodeBizRejected, message)
}
