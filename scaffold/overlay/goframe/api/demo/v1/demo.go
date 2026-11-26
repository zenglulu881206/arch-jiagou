package v1

import "github.com/gogf/gf/v2/frame/g"

// GreetReq 示例场景「问候」。api/<业务>/v1/<业务>.go 一个文件收本业务全部 Req/Res；logic/<业务>/ 下按场景拆文件。
// 首个真实业务落地后删除整个 demo 业务（api/controller/logic 与前端 views/api/demo）。
type GreetReq struct {
	g.Meta `path:"/demo/greet" method:"get" tags:"示例" summary:"问候示例"`
	Name   string `json:"name" v:"required|max-length:20#请填写名字|名字最多20个字"`
}

// GreetRes 问候结果。
type GreetRes struct {
	Message string `json:"message"`
}
